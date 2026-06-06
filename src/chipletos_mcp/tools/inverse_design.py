"""chipletos_inverse_design — target Z₀ → recommended geometry.

Wraps POST /v1/glass-pdk/geometry-from-target.

Uses the differentiable Glass-PDK v3 surrogate (R²=0.9999966, MAPE=0.029% vs the
BEM solver — surrogate-vs-sim, not measured silicon) plus optional route-backed
signoff with per-prediction CI, OOD flag, regime, and a composite lab_readiness_score.

Requires an API key (this route is gated; get a free trial key from the ChipletOS dashboard).
"""

from __future__ import annotations

from typing import Any

from ..client import ChipletosClient
from . import ChipletosTool

INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "target_z0_ohm": {
            "type": "number",
            "description": "Target characteristic impedance (Ω).",
            "minimum": 1,
            "maximum": 200,
            "default": 50,
        },
        "freq_hz": {
            "type": "number",
            "description": "Operating frequency in Hz (e.g. 28e9 for 28 GHz).",
            "minimum": 1,
            "maximum": 3e11,
            "default": 28e9,
        },
        "glass_name": {"type": "string", "default": "EagleXG"},
        "glass_dk": {"type": "number", "default": 5.27, "minimum": 0.001, "maximum": 20},
        "glass_df": {"type": "number", "default": 0.005, "minimum": 0},
        "glass_thickness_um": {
            "type": ["number", "null"],
            "description": "If set, t is held fixed; otherwise it's a free variable.",
            "minimum": 1,
            "maximum": 2000,
        },
        "metal": {"type": "string", "default": "Copper"},
        "via_type": {"type": "string", "default": "Solid"},
        "wall_um": {"type": "number", "default": 0.0, "minimum": 0},
        "tolerance_pct": {
            "type": "number",
            "minimum": 0.01,
            "maximum": 20,
            "default": 2.0,
            "description": "|Z₀ − target| / target convergence tolerance.",
        },
        "max_iterations": {"type": "integer", "minimum": 1, "maximum": 5000, "default": 400},
        "learning_rate": {"type": "number", "minimum": 0.001, "maximum": 1.0, "default": 0.02},
        "seed": {"type": "integer", "minimum": 0, "default": 0},
        "include_signoff": {
            "type": "boolean",
            "default": True,
            "description": "Call /v1/chiplet-suite/package-signoff at the optimum for route-backed verification.",
        },
        "initial_diameter_um": {"type": ["number", "null"], "minimum": 1, "maximum": 500},
        "initial_pitch_um": {"type": ["number", "null"], "minimum": 1, "maximum": 2000},
    },
    "required": ["target_z0_ohm"],
    "additionalProperties": False,
}


async def _run(client: ChipletosClient, args: dict[str, Any]) -> dict[str, Any]:
    return await client.post("/v1/glass-pdk/geometry-from-target", args)


TOOL = ChipletosTool(
    tool_name="chipletos_inverse_design",
    description=(
        "Inverse-design TGV geometry for a target Z₀ using the differentiable "
        "PROV 7 v3 surrogate. Returns optimal (diameter, pitch, thickness), "
        "surrogate Z₀ with confidence interval, OOD flag, regime, optional "
        "BEM refinement and route-backed signoff, plus a composite "
        "lab_readiness_score. Use this for 'I need a 50Ω TGV at 28 GHz, what "
        "are the dimensions?' style queries."
    ),
    input_schema=INPUT_SCHEMA,
    run=_run,
)
