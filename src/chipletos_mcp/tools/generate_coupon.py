"""chipletos_generate_coupon — fab-ready coupon bundle.

Wraps POST /v1/coupons/export-fab.

This route is API-key-gated on Modal (Sprint 46 P2 hardening): coupon bundles
include a 12-layer stack-up + per-foundry SOW + cost band, all considered
sensitive. The tool will return a 401 with a clear setup hint if the agent
calls it without CHIPLETOS_API_KEY set.

Returns DRC verdict + lithography stack-up + per-partner SOW (JSON + Markdown)
+ cost estimate + optional lab_readiness_score.
"""

from __future__ import annotations

from typing import Any

from ..client import ChipletosClient
from . import ChipletosTool

INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "target_z0_ohm": {"type": "number", "minimum": 1, "maximum": 200, "default": 50},
        "freq_ghz": {"type": "number", "minimum": 0.001, "maximum": 300, "default": 28},
        "glass_name": {"type": "string", "default": "EagleXG"},
        "glass_thickness_um": {"type": "number", "minimum": 0.001, "maximum": 2000, "default": 300},
        "via_diameter_um": {"type": "number", "minimum": 0.001, "maximum": 500, "default": 40},
        "via_pitch_um": {"type": "number", "minimum": 0.001, "maximum": 2000, "default": 80},
        "fab_partner": {
            "type": "string",
            "enum": ["amkor", "mosis", "generic"],
            "default": "generic",
        },
        "n_coupons": {"type": "integer", "minimum": 1, "maximum": 200, "default": 5},
        "include_test_per_coupon": {"type": "boolean", "default": True},
        "additional_via_geometries": {
            "type": ["array", "null"],
            "description": "Optional list of additional via geometries for the DRC sweep.",
            "items": {
                "type": "object",
                "properties": {
                    "d_um": {"type": "number"},
                    "p_um": {"type": "number"},
                    "t_um": {"type": "number"},
                },
                "required": ["d_um", "p_um", "t_um"],
            },
        },
    },
    "required": [],
    "additionalProperties": False,
}


async def _run(client: ChipletosClient, args: dict[str, Any]) -> dict[str, Any]:
    return await client.post("/v1/coupons/export-fab", args)


TOOL = ChipletosTool(
    tool_name="chipletos_generate_coupon",
    description=(
        "Generate a fab-ready coupon bundle for a target spec: DRC + 12-layer "
        "lithography stack-up + per-foundry SOW (JSON + Markdown) + cost "
        "estimate. Supported partners: amkor, mosis, generic. Requires "
        "CHIPLETOS_API_KEY in the MCP server env (gated route — coupon "
        "bundles are sensitive). Use when the user wants to GO from design "
        "to RFQ in one step."
    ),
    input_schema=INPUT_SCHEMA,
    run=_run,
)
