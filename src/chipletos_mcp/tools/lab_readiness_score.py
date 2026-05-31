"""chipletos_lab_readiness_score — composite 0-100 lab-readiness verdict.

Calls POST /v1/glass-pdk/geometry-from-target (which embeds lab_readiness_score
in its response per a recent release Chunk 4b / Track A Gate 7) and extracts the
composite-score block. Verdict bands: send_to_lab ≥95 / send_with_extra_qc
80-94 / hold 60-79 / reject <60. Honest partial-score handling when some gates
lack data.
"""

from __future__ import annotations

from typing import Any

from ..client import ChipletosClient
from . import ChipletosTool

INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "target_z0_ohm": {"type": "number", "minimum": 1, "maximum": 200, "default": 50},
        "freq_hz": {"type": "number", "minimum": 1, "maximum": 3e11, "default": 28e9},
        "glass_name": {"type": "string", "default": "EagleXG"},
        "glass_dk": {"type": "number", "default": 5.27, "minimum": 0.001, "maximum": 20},
        "glass_df": {"type": "number", "default": 0.005, "minimum": 0},
        "glass_thickness_um": {
            "type": ["number", "null"],
            "minimum": 1,
            "maximum": 2000,
        },
        "metal": {"type": "string", "default": "Copper"},
        "via_type": {"type": "string", "default": "Solid"},
        "wall_um": {"type": "number", "default": 0.0, "minimum": 0},
        "tolerance_pct": {"type": "number", "minimum": 0.01, "maximum": 20, "default": 2.0},
        "max_iterations": {"type": "integer", "minimum": 1, "maximum": 5000, "default": 400},
        "learning_rate": {"type": "number", "minimum": 0.001, "maximum": 1.0, "default": 0.02},
        "seed": {"type": "integer", "minimum": 0, "default": 0},
    },
    "required": ["target_z0_ohm"],
    "additionalProperties": False,
}


async def _run(client: ChipletosClient, args: dict[str, Any]) -> dict[str, Any]:
    # Force include_signoff=True so the readiness score gates have signal to work with.
    payload = dict(args)
    payload["include_signoff"] = True
    result = await client.post("/v1/glass-pdk/geometry-from-target", payload)
    score_block = result.get("lab_readiness_score")
    return {
        "lab_readiness_score": score_block,
        "geometry": {
            "diameter_um": result.get("diameter_um"),
            "pitch_um": result.get("pitch_um"),
            "glass_thickness_um": result.get("glass_thickness_um"),
        },
        "surrogate": {
            "predicted_z0": result.get("predicted_z0_surrogate"),
            "ci_low": result.get("surrogate_ci_low"),
            "ci_high": result.get("surrogate_ci_high"),
            "regime": result.get("regime"),
            "ood_flag": result.get("ood_flag"),
        },
        "converged": result.get("converged"),
        "error_pct": result.get("error_pct"),
        "_chipletos_mcp_note": (
            "Composite 0-100 lab_readiness_score with verdict bands. "
            "See full inverse-design payload via chipletos_inverse_design "
            "for the underlying signoff witness."
        ),
    }


TOOL = ChipletosTool(
    tool_name="chipletos_lab_readiness_score",
    description=(
        "Return the composite 0-100 lab_readiness_score with verdict bands "
        "(send_to_lab / send_with_extra_qc / hold / reject) for a given Z₀ "
        "target + frequency + glass. Use when the user asks 'is this design "
        "ready to send to the fab/lab?' or 'should I tape this out?'."
    ),
    input_schema=INPUT_SCHEMA,
    run=_run,
)
