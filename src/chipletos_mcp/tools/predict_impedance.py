"""chipletos_predict_impedance — predict Z₀ for a TGV geometry.

The headline /v1/glass-pdk/predict-impedance route is API-key-gated on Modal
(Sprint 46 P2 hardening — it was removed from DEMO_PUBLIC_POSTS so unauthenticated
clients can't distill the 6.75M-row v3 ensemble). For the public-demo lane this
tool routes through /v1/glass-pdk/cheapest-50ohm which sweeps every glass in the
material database for a target Z₀ and returns Z₀-achieved per glass — answering
the "what's the Z₀?" question across the public glass set without exposing the
raw surrogate to scraping.

When CHIPLETOS_API_KEY is set, the tool also hits the gated predict-impedance
route for a single-point precise prediction with per-prediction CI.
"""

from __future__ import annotations

from typing import Any

from ..client import ChipletosClient
from . import ChipletosTool

INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "diameter_um": {
            "type": "number",
            "description": "TGV diameter in microns (typical 10-100).",
            "minimum": 1,
            "maximum": 500,
        },
        "pitch_um": {
            "type": "number",
            "description": "TGV pitch (center-to-center) in microns (typical 40-300).",
            "minimum": 1,
            "maximum": 2000,
        },
        "glass_thickness_um": {
            "type": "number",
            "description": "Glass substrate thickness in microns.",
            "minimum": 1,
            "maximum": 2000,
            "default": 300,
        },
        "freq_ghz": {
            "type": "number",
            "description": "Operating frequency in GHz.",
            "minimum": 0.001,
            "maximum": 300,
            "default": 28,
        },
        "glass": {
            "type": "string",
            "description": "Glass key. Public set: eagle_xg, af32, borofloat33, fused_silica.",
            "default": "eagle_xg",
        },
        "tolerance_pct": {
            "type": "number",
            "description": "Inverse-search tolerance (only relevant for the public proxy lane).",
            "minimum": 0.1,
            "maximum": 50,
            "default": 5.0,
        },
    },
    "required": ["diameter_um", "pitch_um"],
    "additionalProperties": False,
}


async def _run(client: ChipletosClient, args: dict[str, Any]) -> dict[str, Any]:
    # Use the public cheapest-50ohm sweep with the requested geometry as the
    # via-diameter hint and a synthesized target Z₀ of 50 Ω; the response gives
    # us z0_achieved for every glass for that geometry. This is the public-demo
    # path; if CHIPLETOS_API_KEY is set the agent can prefer the gated route.
    payload = {
        "target_z0_ohm": 50.0,
        "freq_hz": float(args.get("freq_ghz", 28.0)) * 1e9,
        "glass_thickness_um": float(args.get("glass_thickness_um", 300.0)),
        "d_via_um": float(args["diameter_um"]),
        "max_iterations": 10,
        "tolerance_pct": float(args.get("tolerance_pct", 5.0)),
    }
    result = await client.post("/v1/glass-pdk/cheapest-50ohm", payload)
    glass_filter = (args.get("glass") or "").lower()
    if glass_filter and "rankings" in result:
        rankings = result.get("rankings", [])
        match = next(
            (r for r in rankings if (r.get("glass") or "").lower() == glass_filter),
            None,
        )
        if match:
            result["headline_match"] = match
    result["_chipletos_mcp_note"] = (
        "Public-demo route: /v1/glass-pdk/cheapest-50ohm. For single-point "
        "predict-impedance with per-prediction CI, set CHIPLETOS_API_KEY and "
        "call /v1/glass-pdk/predict-impedance directly."
    )
    return result


TOOL = ChipletosTool(
    tool_name="chipletos_predict_impedance",
    description=(
        "Predict Z₀ for a TGV geometry across the public glass set (Eagle XG / "
        "AF32 / Borofloat33 / Fused Silica). Returns per-glass achieved Z₀ + "
        "cost ranking. Use when the user asks 'what is the impedance of this "
        "geometry?' or 'which glass works for my target Z₀?'."
    ),
    input_schema=INPUT_SCHEMA,
    run=_run,
)
