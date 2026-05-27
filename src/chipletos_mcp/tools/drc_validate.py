"""chipletos_drc_validate — glass-interposer DRC.

Wraps POST /v1/glass-pdk/drc-validate.

Validates a list of TGV geometries against the glass-interposer DRC rule set
(BEM stability, manufacturability, reliability, CMP planarity). Each violation
carries an IPC/SEMI defect code for buyer-facing CAPA cross-reference.
"""

from __future__ import annotations

from typing import Any

from ..client import ChipletosClient
from . import ChipletosTool

INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "via_geometries": {
            "type": "array",
            "minItems": 1,
            "maxItems": 10000,
            "items": {
                "type": "object",
                "properties": {
                    "d_um": {"type": "number", "minimum": 0.001, "maximum": 500,
                             "description": "TGV diameter in microns"},
                    "p_um": {"type": "number", "minimum": 0.001, "maximum": 2000,
                             "description": "TGV pitch in microns"},
                    "t_um": {"type": "number", "minimum": 0.001, "maximum": 2000,
                             "description": "Glass thickness in microns"},
                    "x": {"type": ["number", "null"], "description": "Optional x position"},
                    "y": {"type": ["number", "null"], "description": "Optional y position"},
                },
                "required": ["d_um", "p_um", "t_um"],
                "additionalProperties": False,
            },
        },
        "rules_override": {
            "type": ["object", "null"],
            "description": (
                "Optional rule-parameter overrides (e.g. "
                "{\"min_via_diameter_um\": 15.0}). Defaults to genesis.drc.glass_rules.DEFAULT_RULES."
            ),
            "additionalProperties": True,
        },
    },
    "required": ["via_geometries"],
    "additionalProperties": False,
}


async def _run(client: ChipletosClient, args: dict[str, Any]) -> dict[str, Any]:
    return await client.post("/v1/glass-pdk/drc-validate", args)


TOOL = ChipletosTool(
    tool_name="chipletos_drc_validate",
    description=(
        "Run glass-interposer DRC on a list of TGV geometries. Returns per-"
        "violation entries with IPC/SEMI defect codes, severity, and "
        "suggestion. Use when the user wants to know 'is this geometry "
        "manufacturable?' before tape-out."
    ),
    input_schema=INPUT_SCHEMA,
    run=_run,
)
