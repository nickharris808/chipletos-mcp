"""chipletos_pareto_design — multi-objective Pareto inverse design.

Wraps POST /v1/glass-pdk/geometry-pareto.

Returns a Pareto front of {diameter, pitch, thickness} candidates across the
selected objectives. Public-demo route; rate-limited per IP.

Heads-up: CLAUDE.md::C38 notes a known Modal-side SIGSEGV on geometries
with d/p ∈ [0.4, 0.5] (in the LAPACK hot path of the L-BFGS-B inner loop).
Uses a pure-Python coax-proxy hot path (no BEM in the inner loop); returns 200.
"""

from __future__ import annotations

from typing import Any

from ..client import ChipletosClient
from . import ChipletosTool

INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "z0_target_ohm": {
            "type": "number",
            "description": "Target characteristic impedance (Ω). Default 50 Ω.",
            "minimum": 1,
            "maximum": 200,
            "default": 50,
        },
        "freq_ghz": {
            "type": "number",
            "description": "Operating frequency (GHz).",
            "minimum": 0.001,
            "maximum": 300,
            "default": 28,
        },
        "glass_name": {
            "type": "string",
            "description": "Glass family name (EagleXG, AF32, Borofloat33, FusedSilica).",
            "default": "EagleXG",
        },
        "glass_dk": {"type": "number", "default": 5.27, "minimum": 0.001, "maximum": 20},
        "glass_df": {"type": "number", "default": 0.005, "minimum": 0, "maximum": 1.0},
        "glass_thickness_um": {"type": "number", "default": 300, "minimum": 1, "maximum": 2000},
        "fill_metal": {"type": "string", "default": "copper"},
        "objectives": {
            "type": "array",
            "items": {"type": "string", "enum": ["z0", "loss", "crosstalk", "yield"]},
            "default": ["z0", "loss", "crosstalk"],
            "description": "Subset of {z0, loss, crosstalk, yield} to Pareto-optimize.",
        },
        "n_pareto_points": {
            "type": "integer",
            "minimum": 3,
            "maximum": 20,
            "default": 5,
            "description": "Number of Pareto-front points to return.",
        },
        "diameter_min_um": {"type": "number", "default": 20, "minimum": 1},
        "diameter_max_um": {"type": "number", "default": 60, "minimum": 1},
        "pitch_min_um": {"type": "number", "default": 40, "minimum": 1},
        "pitch_max_um": {"type": "number", "default": 200, "minimum": 1},
        "refine_with_solver": {
            "type": "boolean",
            "default": True,
            "description": "Refine top-50% candidates with full RLGC extraction (~10× slower, more accurate).",
        },
        "il_max_db": {"type": ["number", "null"], "description": "Optional insertion-loss ceiling."},
        "crosstalk_max_db": {
            "type": ["number", "null"],
            "description": "Optional crosstalk ceiling (more negative dB).",
        },
    },
    "required": [],
    "additionalProperties": False,
}


async def _run(client: ChipletosClient, args: dict[str, Any]) -> dict[str, Any]:
    return await client.post("/v1/glass-pdk/geometry-pareto", args)


TOOL = ChipletosTool(
    tool_name="chipletos_pareto_design",
    description=(
        "Multi-objective Pareto inverse design across {Z₀, loss, crosstalk, "
        "yield}. Returns a Pareto front of (diameter, pitch, thickness) "
        "candidates with dominance ranks. Use when the user wants to EXPLORE "
        "trade-offs rather than hit a single Z₀ target."
    ),
    input_schema=INPUT_SCHEMA,
    run=_run,
)
