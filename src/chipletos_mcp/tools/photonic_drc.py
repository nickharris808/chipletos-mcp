"""chipletos_photonic_drc — AIM Photonics-class photonic DRC.

Wraps POST /v1/photonics/drc-photonic.

Runs AIM Photonics-class Design Rule Check on a list of photonic geometries
(waveguides, ring resonators, grating couplers, MMI couplers, MZI). Each
violation carries an IPC/SEMI-style defect code and a suggested fix.

Default rule set (AIM Photonics-class): min feature 80 nm, min spacing 100 nm,
min bend radius per mode-class, max width for single-mode. Override individual
rules via the `design_rules` field.
"""

from __future__ import annotations

from typing import Any

from ..client import ChipletosClient
from . import ChipletosTool

INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "geometries": {
            "type": "array",
            "minItems": 1,
            "maxItems": 10000,
            "description": (
                "List of photonic geometry dicts. Shape depends on primitive: "
                "waveguide={width_nm, height_nm, material}, ring={radius_um, "
                "coupler_gap_nm, width_nm}, grating={period_nm, duty_cycle, "
                "width_nm}, etc. The DRC engine inspects keys to pick the "
                "right rule subset."
            ),
            "items": {
                "type": "object",
                "additionalProperties": True,
            },
        },
        "design_rules": {
            "type": ["object", "null"],
            "description": (
                "Optional rule-parameter overrides (e.g. "
                "{\"min_feature_nm\": 100, \"min_spacing_nm\": 120}). Defaults "
                "to AIM Photonics-class rules in photonics.drc.photonic_rules."
            ),
            "additionalProperties": True,
        },
    },
    "required": ["geometries"],
    "additionalProperties": False,
}


async def _run(client: ChipletosClient, args: dict[str, Any]) -> dict[str, Any]:
    payload: dict[str, Any] = {"geometries": args["geometries"]}
    if args.get("design_rules"):
        payload["design_rules"] = args["design_rules"]
    return await client.post("/v1/photonics/drc-photonic", payload)


TOOL = ChipletosTool(
    tool_name="chipletos_photonic_drc",
    description=(
        "Run AIM Photonics-class Design Rule Check on photonic geometries "
        "(waveguides, ring resonators, grating couplers). Returns violations "
        "with IPC/SEMI-style defect codes. Use before tape-out."
    ),
    input_schema=INPUT_SCHEMA,
    run=_run,
)
