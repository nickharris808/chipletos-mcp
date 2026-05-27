"""chipletos_validate_against_measurement — surrogate vs literature cross-check.

Wraps POST /v1/glass-pdk/validate-against-measurement.

Looks up the closest-matching reference in
provisionals/PROV_7_GLASS_PDK/data/literature/measurements.json
and reports surrogate-vs-reference disagreement. Honest disclosure: most
current Z₀ entries are source_type=simulation (HFSS-coaxial), not VNA
measurement; queued $200-500K wet-lab campaign is the next unlock.
"""

from __future__ import annotations

from typing import Any

from ..client import ChipletosClient
from . import ChipletosTool

INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "diameter_um": {"type": "number", "minimum": 0.001, "maximum": 500},
        "pitch_um": {"type": "number", "minimum": 0.001, "maximum": 2000},
        "glass_thickness_um": {"type": "number", "minimum": 0.001, "maximum": 2000},
        "freq_ghz": {"type": "number", "minimum": 0.001, "maximum": 300},
        "glass_name": {"type": "string", "default": "EagleXG"},
        "metric": {
            "type": "string",
            "enum": ["Z0_ohm", "IL_dB", "R_mohm", "C_fF"],
            "default": "Z0_ohm",
        },
        "geometry_match_tolerance_pct": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 100,
            "default": 20.0,
        },
        "require_measurement": {
            "type": "boolean",
            "default": False,
            "description": (
                "If True, return 404 unless a source_type=measurement entry matches. "
                "Default False allows simulation matches with disclosure."
            ),
        },
    },
    "required": ["diameter_um", "pitch_um", "glass_thickness_um", "freq_ghz"],
    "additionalProperties": False,
}


async def _run(client: ChipletosClient, args: dict[str, Any]) -> dict[str, Any]:
    return await client.post("/v1/glass-pdk/validate-against-measurement", args)


TOOL = ChipletosTool(
    tool_name="chipletos_validate_against_measurement",
    description=(
        "Compare surrogate prediction against the closest-matching literature "
        "or measurement reference. Returns surrogate value, reference value, "
        "absolute error %, within-tolerance verdict, and an honest "
        "source_type disclosure (measurement vs HFSS simulation). Use when "
        "the user asks 'how does this match published data?' or 'is the "
        "surrogate trustworthy for this geometry?'."
    ),
    input_schema=INPUT_SCHEMA,
    run=_run,
)
