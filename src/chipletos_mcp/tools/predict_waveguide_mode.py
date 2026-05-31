"""chipletos_predict_waveguide_mode — silicon-photonic waveguide mode prediction.

Wraps POST /v1/photonics/predict-waveguide-mode (a recent release alpha).

Predicts effective index (Neff), group index (ng), propagation loss, and bend
loss for a Si or SiN strip waveguide via the Transfer-Matrix-Method (TMM)
analytical solver. Use when designing photonic-integrated-circuit (PIC)
waveguides for Marvell SiPh, Intel Foundry SiPh, NVIDIA optical interconnect,
Broadcom, or Acacia.

Honest framing (a recent release): the TMM analytical solver has 5-15% relative
error vs Meep FDTD; the surrogate v1 (R²≥0.999 vs Meep) is on the roadmap
vs Meep. The response carries an envelope flag for manufacturability checks.
"""

from __future__ import annotations

from typing import Any

from ..client import ChipletosClient
from . import ChipletosTool

INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "width_nm": {
            "type": "number",
            "description": "Waveguide width in nm (typical 400-600 for single-mode Si SOI at 1550 nm).",
            "minimum": 80,
            "maximum": 5000,
            "default": 500.0,
        },
        "height_nm": {
            "type": "number",
            "description": "Waveguide height / film thickness in nm (220 nm is the Si SOI standard).",
            "minimum": 100,
            "maximum": 400,
            "default": 220.0,
        },
        "wavelength_nm": {
            "type": "number",
            "description": "Operating wavelength in nm (telecom O-band 1260-1360, C-band 1530-1565, L-band 1565-1625).",
            "minimum": 1260,
            "maximum": 1670,
            "default": 1550.0,
        },
        "material": {
            "type": "string",
            "description": "Core material: 'Si' (silicon, n≈3.48) or 'SiN' (silicon nitride, n≈2.0).",
            "enum": ["Si", "SiN"],
            "default": "Si",
        },
        "bend_radius_um": {
            "type": "number",
            "description": "Minimum bend radius in µm (5-50 typical for Si strip; 50-200 for SiN).",
            "minimum": 5,
            "maximum": 200,
            "default": 50.0,
        },
    },
    "required": ["width_nm", "height_nm", "wavelength_nm"],
    "additionalProperties": False,
}


async def _run(client: ChipletosClient, args: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "width_nm": float(args["width_nm"]),
        "height_nm": float(args.get("height_nm", 220.0)),
        "wavelength_nm": float(args.get("wavelength_nm", 1550.0)),
        "material": args.get("material", "Si"),
        "bend_radius_um": float(args.get("bend_radius_um", 50.0)),
    }
    return await client.post("/v1/photonics/predict-waveguide-mode", payload)


TOOL = ChipletosTool(
    tool_name="chipletos_predict_waveguide_mode",
    description=(
        "Predict the effective index (Neff), group index (ng), propagation loss, "
        "and bend loss for a silicon-photonic strip waveguide via TMM analytical "
        "model. Use when designing photonic integrated circuit waveguides — "
        "Marvell SiPh, Intel Foundry, NVIDIA optical. Returns mode properties "
        "with manufacturability envelope flag."
    ),
    input_schema=INPUT_SCHEMA,
    run=_run,
)
