"""LIVE integration test — hits the REAL deployed API, not respx mocks.

Why this exists: the rest of the suite mocks httpx, so it proves the client *shape*
but never that the live API actually returns what the tools expect. A 2026-06-01 audit
found that gap (and that a careless first pass with wrong args can falsely flag tools as
broken). This test calls each kept tool with its **declared input_schema args** against
the real endpoint and asserts a real 200 + the documented keys — so genuine
contract drift is caught instead of hiding behind mocks.

It is OPT-IN and does NOT run in normal CI (no Modal charge unless you ask for it):

    CHIPLETOS_LIVE_TEST=1 pytest tests/test_live_integration.py            # public tools
    CHIPLETOS_LIVE_TEST=1 CHIPLETOS_API_KEY=... pytest tests/test_live_integration.py  # + gated glass tools

Public (no key): photonic predict-waveguide-mode / drc / validate-ieee / signoff-health,
leaderboard view. Key-gated glass tools are skipped unless CHIPLETOS_API_KEY is set.
"""
from __future__ import annotations

import os

import pytest

LIVE = os.environ.get("CHIPLETOS_LIVE_TEST") == "1"
HAS_KEY = bool(os.environ.get("CHIPLETOS_API_KEY"))

pytestmark = pytest.mark.skipif(not LIVE, reason="set CHIPLETOS_LIVE_TEST=1 to run live (hits Modal)")

# (tool module, args matching the tool's declared input_schema, expected key in the response, needs_key)
PUBLIC_CASES = [
    ("predict_waveguide_mode", {"width_nm": 450, "height_nm": 220, "wavelength_nm": 1550, "material": "Si"}, "Neff", False),
    ("photonic_signoff_health", {}, "module", False),
    ("photonic_drc", {"geometries": [{"primitive": "waveguide", "width_nm": 450, "height_nm": 220}]}, "n_violations", False),
    ("photonic_validate_ieee", {}, "per_paper", False),
    ("leaderboard", {"task": "z0", "substrate": "glass", "limit": 3}, "entries", False),
]
GATED_CASES = [
    ("predict_impedance", {"diameter_um": 40, "pitch_um": 80, "freq_ghz": 28}, "rankings", True),
    ("inverse_design", {"target_z0_ohm": 50, "freq_ghz": 28, "glass": "EagleXG"}, "diameter_um", True),
    ("pareto_design", {"target_z0_ohm": 50, "freq_ghz": 28}, "pareto_front", True),
    ("drc_validate", {"via_geometries": [{"d_um": 40, "p_um": 80, "t_um": 300}]}, "n_violations", True),
    ("validate_against_measurement",
     {"diameter_um": 40, "pitch_um": 120, "glass_thickness_um": 300, "freq_ghz": 10, "glass_name": "EagleXG"},
     "measured_value", True),
]


async def _run_case(mod_name: str, args: dict, expect_key: str):
    import importlib
    from chipletos_mcp.client import ChipletosClient
    client = ChipletosClient()
    mod = importlib.import_module(f"chipletos_mcp.tools.{mod_name}")
    result = await mod.TOOL.run(client, args)
    assert isinstance(result, dict), f"{mod_name}: expected dict, got {type(result)}"
    assert expect_key in result, f"{mod_name}: missing key '{expect_key}' in {list(result)[:8]}"


@pytest.mark.asyncio
@pytest.mark.parametrize("mod_name,args,expect_key,_", PUBLIC_CASES)
async def test_public_tool_live(mod_name, args, expect_key, _):
    await _run_case(mod_name, args, expect_key)


@pytest.mark.asyncio
@pytest.mark.skipif(not HAS_KEY, reason="set CHIPLETOS_API_KEY to exercise the gated glass tools")
@pytest.mark.parametrize("mod_name,args,expect_key,_", GATED_CASES)
async def test_gated_tool_live(mod_name, args, expect_key, _):
    await _run_case(mod_name, args, expect_key)
