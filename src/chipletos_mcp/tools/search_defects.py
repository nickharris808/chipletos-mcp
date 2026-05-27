"""chipletos_search_defects — search the 33-type IPC/SEMI/ISO defect taxonomy.

Wraps GET /v1/defects/search.

Returns matching defect-code entries with family, severity tier, detection
method, description, and glass-TGV relevance. Useful for triaging DRC
violations or building a CAPA workflow.
"""

from __future__ import annotations

from typing import Any

from ..client import ChipletosClient
from . import ChipletosTool

INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "defect_family": {
            "type": ["string", "null"],
            "description": "Filter by family (e.g. 'Solder Joint').",
        },
        "severity_tier": {
            "type": ["string", "null"],
            "enum": ["tier_1_critical", "tier_2_elevated", "tier_3_watch", "tier_4_unknown", None],
        },
        "detection_method": {
            "type": ["string", "null"],
            "description": "Partial match on detection method (e.g. 'AXI', 'SEM').",
        },
        "glass_tgv_relevance": {
            "type": ["string", "null"],
            "enum": ["direct", "indirect", "n/a", None],
        },
        "q": {
            "type": ["string", "null"],
            "description": "Free-text search over defect name + description.",
        },
        "limit": {"type": "integer", "minimum": 1, "maximum": 500, "default": 50},
        "offset": {"type": "integer", "minimum": 0, "default": 0},
    },
    "required": [],
    "additionalProperties": False,
}


async def _run(client: ChipletosClient, args: dict[str, Any]) -> dict[str, Any]:
    return await client.get("/v1/defects/search", params=args)


TOOL = ChipletosTool(
    tool_name="chipletos_search_defects",
    description=(
        "Search the 33-type IPC/SEMI/ISO defect taxonomy. Filter by family, "
        "severity tier, detection method, glass-TGV relevance, or free-text. "
        "Use when the user wants to look up a defect code, triage a DRC "
        "violation, or build a CAPA workflow."
    ),
    input_schema=INPUT_SCHEMA,
    run=_run,
)
