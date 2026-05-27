"""chipletos_search_s2p_library — paginated S2P Touchstone library search.

Wraps GET /v1/library/s2p.

Searches the canonical validated S2P registry by glass, pitch range, and
thickness. Returns paginated metadata + asset IDs the buyer can hand to
Cadence Sigrity, ANSYS HFSS, or Keysight ADS.
"""

from __future__ import annotations

from typing import Any

from ..client import ChipletosClient
from . import ChipletosTool

INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "glass": {
            "type": ["string", "null"],
            "description": "Filter by glass name (case-insensitive exact match).",
        },
        "pitch_min": {"type": ["number", "null"], "minimum": 0,
                      "description": "Lower bound on TGV pitch in microns."},
        "pitch_max": {"type": ["number", "null"], "minimum": 0,
                      "description": "Upper bound on TGV pitch in microns."},
        "thickness_mm": {"type": ["number", "null"], "minimum": 0,
                         "description": "Exact glass thickness match in mm."},
        "limit": {"type": "integer", "minimum": 1, "maximum": 500, "default": 50},
        "offset": {"type": "integer", "minimum": 0, "default": 0},
    },
    "required": [],
    "additionalProperties": False,
}


async def _run(client: ChipletosClient, args: dict[str, Any]) -> dict[str, Any]:
    return await client.get("/v1/library/s2p", params=args)


TOOL = ChipletosTool(
    tool_name="chipletos_search_s2p_library",
    description=(
        "Search the curated S2P Touchstone library (millions of validated "
        "S-parameter files) by glass name, pitch range, and thickness. "
        "Returns paginated metadata + asset IDs ready for Cadence Sigrity, "
        "ANSYS HFSS, or Keysight ADS import. Use when the user asks 'find "
        "me an S2P for X' or wants to compare a design to existing "
        "characterized geometries."
    ),
    input_schema=INPUT_SCHEMA,
    run=_run,
)
