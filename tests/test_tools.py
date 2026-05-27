"""Schema validation + smoke tests for all chipletos-mcp tools (10 chiplet + 4 photonic + 1 benchmark)."""

from __future__ import annotations

import httpx
import pytest
import respx

from chipletos_mcp.client import ChipletosClient
from chipletos_mcp.tools import ALL_TOOLS, ChipletosTool


EXPECTED_TOOL_NAMES = {
    "chipletos_predict_impedance",
    "chipletos_pareto_design",
    "chipletos_inverse_design",
    "chipletos_cross_solver_matrix",
    "chipletos_drc_validate",
    "chipletos_validate_against_measurement",
    "chipletos_lab_readiness_score",
    "chipletos_search_s2p_library",
    "chipletos_search_defects",
    "chipletos_generate_coupon",
    # ChipletOS Photonic Signoff (alpha)
    "chipletos_predict_waveguide_mode",
    "chipletos_photonic_signoff_health",
    "chipletos_photonic_drc",
    "chipletos_photonic_validate_ieee",
    # Open benchmark leaderboard
    "chipletos_leaderboard",
}


def test_all_tools_registered() -> None:
    names = {t.tool_name for t in ALL_TOOLS}
    assert names == EXPECTED_TOOL_NAMES, f"Tool registry mismatch: {names ^ EXPECTED_TOOL_NAMES}"
    assert len(ALL_TOOLS) == 15


def test_every_tool_has_a_description() -> None:
    for t in ALL_TOOLS:
        assert isinstance(t, ChipletosTool)
        assert t.description and len(t.description) > 30, f"{t.tool_name} description too short"
        # LLM-friendly descriptions hint at WHEN to use the tool
        assert "Use" in t.description or "use" in t.description, (
            f"{t.tool_name} description should hint at usage context"
        )


def test_every_tool_has_a_valid_input_schema() -> None:
    for t in ALL_TOOLS:
        schema = t.input_schema
        assert isinstance(schema, dict)
        assert schema.get("type") == "object", f"{t.tool_name} schema is not object-typed"
        assert "properties" in schema, f"{t.tool_name} schema missing 'properties'"


# ---------------------------------------------------------------------------
# Mocked happy-path smoke tests, one per tool.
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
@respx.mock
async def test_predict_impedance_smoke(client: ChipletosClient, base_url: str) -> None:
    respx.post(f"{base_url}/v1/glass-pdk/cheapest-50ohm").mock(
        return_value=httpx.Response(
            200,
            json={
                "target_z0_ohm": 50.0,
                "n_converged": 4,
                "rankings": [
                    {"glass": "eagle_xg", "z0_achieved": 50.1, "cost_index": 1.0,
                     "rank": 1, "error_pct": 0.2, "pitch_um": 80, "diameter_um": 40,
                     "thickness_um": 300, "dp_ratio": 0.5, "glass_dk": 5.27, "converged": True},
                ],
            },
        )
    )
    from chipletos_mcp.tools.predict_impedance import TOOL

    result = await TOOL.run(client, {"diameter_um": 40, "pitch_um": 80})
    assert result["rankings"][0]["glass"] == "eagle_xg"
    assert "_chipletos_mcp_note" in result


@pytest.mark.asyncio
@respx.mock
async def test_pareto_design_smoke(client: ChipletosClient, base_url: str) -> None:
    respx.post(f"{base_url}/v1/glass-pdk/geometry-pareto").mock(
        return_value=httpx.Response(200, json={"pareto_front": [], "n_pareto_points_returned": 0})
    )
    from chipletos_mcp.tools.pareto_design import TOOL

    result = await TOOL.run(client, {"z0_target_ohm": 50})
    assert "pareto_front" in result


@pytest.mark.asyncio
@respx.mock
async def test_inverse_design_smoke(client: ChipletosClient, base_url: str) -> None:
    respx.post(f"{base_url}/v1/glass-pdk/geometry-from-target").mock(
        return_value=httpx.Response(
            200,
            json={
                "diameter_um": 40, "pitch_um": 80, "glass_thickness_um": 300,
                "dp_ratio": 0.5, "predicted_z0_surrogate": 50.05,
                "surrogate_ci_low": 49.8, "surrogate_ci_high": 50.3,
                "surrogate_std": 0.1, "regime": "OTHER", "ood_flag": False,
                "ood_reason": None, "adjoint_used": False, "refinement_iterations": 0,
                "iterations": 24, "converged": True, "error_pct": 0.1,
                "target_z0_ohm": 50, "target_freq_ghz": 28, "elapsed_ms": 120.0,
                "provenance": {}, "lab_readiness_score": {"score": 92, "verdict": "send_with_extra_qc"},
            },
        )
    )
    from chipletos_mcp.tools.inverse_design import TOOL

    result = await TOOL.run(client, {"target_z0_ohm": 50})
    assert result["converged"] is True
    assert result["lab_readiness_score"]["verdict"] == "send_with_extra_qc"


@pytest.mark.asyncio
@respx.mock
async def test_cross_solver_matrix_smoke(client: ChipletosClient, base_url: str) -> None:
    respx.get(f"{base_url}/v1/glass-pdk/cross-solver-matrix").mock(
        return_value=httpx.Response(200, json={"n_geometries": 100, "solvers": ["BEM"]})
    )
    from chipletos_mcp.tools.cross_solver_matrix import TOOL

    result = await TOOL.run(client, {})
    assert result["n_geometries"] == 100


@pytest.mark.asyncio
@respx.mock
async def test_drc_validate_smoke(client: ChipletosClient, base_url: str) -> None:
    respx.post(f"{base_url}/v1/glass-pdk/drc-validate").mock(
        return_value=httpx.Response(
            200,
            json={
                "passed": True, "n_errors": 0, "n_warnings": 0, "n_info": 0,
                "n_violations": 0, "n_geometries_checked": 1,
                "violations": [], "rules_applied": {},
            },
        )
    )
    from chipletos_mcp.tools.drc_validate import TOOL

    result = await TOOL.run(
        client,
        {"via_geometries": [{"d_um": 40, "p_um": 80, "t_um": 300}]},
    )
    assert result["passed"] is True


# ---------------------------------------------------------------------------
# Photonic Signoff (alpha) + open-benchmark leaderboard smoke tests.
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
@respx.mock
async def test_predict_waveguide_mode_smoke(client: ChipletosClient, base_url: str) -> None:
    respx.post(f"{base_url}/v1/photonics/predict-waveguide-mode").mock(
        return_value=httpx.Response(200, json={"n_eff": 2.41, "method": "tmm_analytical"})
    )
    from chipletos_mcp.tools.predict_waveguide_mode import TOOL

    result = await TOOL.run(client, {"width_nm": 450, "height_nm": 220, "wavelength_nm": 1550})
    assert "n_eff" in result


@pytest.mark.asyncio
@respx.mock
async def test_photonic_signoff_health_smoke(client: ChipletosClient, base_url: str) -> None:
    respx.get(f"{base_url}/v1/photonics/signoff-health").mock(
        return_value=httpx.Response(200, json={"surrogate_status": {"mzi": True}})
    )
    from chipletos_mcp.tools.photonic_signoff_health import TOOL

    result = await TOOL.run(client, {})
    assert "surrogate_status" in result


@pytest.mark.asyncio
@respx.mock
async def test_photonic_drc_smoke(client: ChipletosClient, base_url: str) -> None:
    respx.post(f"{base_url}/v1/photonics/drc-photonic").mock(
        return_value=httpx.Response(200, json={"passed": True, "n_violations": 0})
    )
    from chipletos_mcp.tools.photonic_drc import TOOL

    result = await TOOL.run(client, {"geometries": [{"width_nm": 450}]})
    assert result["passed"] is True


@pytest.mark.asyncio
@respx.mock
async def test_photonic_validate_ieee_smoke(client: ChipletosClient, base_url: str) -> None:
    respx.post(f"{base_url}/v1/photonics/validate-against-ieee").mock(
        return_value=httpx.Response(200, json={"mean_abs_err_pct": 21.27, "verdict": "PASS"})
    )
    from chipletos_mcp.tools.photonic_validate_ieee import TOOL

    result = await TOOL.run(client, {})
    assert "verdict" in result


@pytest.mark.asyncio
@respx.mock
async def test_leaderboard_smoke(client: ChipletosClient, base_url: str) -> None:
    respx.get(f"{base_url}/v1/bench/leaderboard?task=z0&substrate=glass&limit=10").mock(
        return_value=httpx.Response(200, json={"task": "z0", "substrate": "glass", "entries": [
            {"solver_name": "ChipletOS v3 surrogate", "mae": 0.1127}]})
    )
    from chipletos_mcp.tools.leaderboard import TOOL

    result = await TOOL.run(client, {"task": "z0", "substrate": "glass"})
    assert result["entries"][0]["solver_name"] == "ChipletOS v3 surrogate"


@pytest.mark.asyncio
@respx.mock
async def test_validate_against_measurement_smoke(client: ChipletosClient, base_url: str) -> None:
    respx.post(f"{base_url}/v1/glass-pdk/validate-against-measurement").mock(
        return_value=httpx.Response(
            200,
            json={
                "matched_reference_id": "sukumaran_2014",
                "matched_source_type": "simulation",
                "matched_glass": "EagleXG",
                "matched_geometry": {"diameter_um": 50, "pitch_um": 100, "thickness_um": 300, "freq_ghz": 10},
                "measured_value": 50.3, "measured_unit": "Ohm",
                "surrogate_value": 51.04, "surrogate_unit": "Ohm",
                "abs_error_pct": 1.48, "within_tolerance": True,
                "n_measured_entries_in_db": 7, "n_simulation_entries_in_db": 11,
                "notes": ["matched HFSS-coaxial simulation reference"],
            },
        )
    )
    from chipletos_mcp.tools.validate_against_measurement import TOOL

    result = await TOOL.run(
        client,
        {"diameter_um": 50, "pitch_um": 100, "glass_thickness_um": 300, "freq_ghz": 10},
    )
    assert result["within_tolerance"] is True


@pytest.mark.asyncio
@respx.mock
async def test_lab_readiness_score_smoke(client: ChipletosClient, base_url: str) -> None:
    respx.post(f"{base_url}/v1/glass-pdk/geometry-from-target").mock(
        return_value=httpx.Response(
            200,
            json={
                "diameter_um": 40, "pitch_um": 80, "glass_thickness_um": 300,
                "dp_ratio": 0.5, "predicted_z0_surrogate": 50.05,
                "surrogate_ci_low": 49.8, "surrogate_ci_high": 50.3,
                "surrogate_std": 0.1, "regime": "OTHER", "ood_flag": False,
                "ood_reason": None, "adjoint_used": False, "refinement_iterations": 0,
                "iterations": 24, "converged": True, "error_pct": 0.1,
                "target_z0_ohm": 50, "target_freq_ghz": 28, "elapsed_ms": 120.0,
                "provenance": {},
                "lab_readiness_score": {"score": 92, "verdict": "send_with_extra_qc", "partial_score": False},
            },
        )
    )
    from chipletos_mcp.tools.lab_readiness_score import TOOL

    result = await TOOL.run(client, {"target_z0_ohm": 50})
    assert result["lab_readiness_score"]["verdict"] == "send_with_extra_qc"
    assert result["geometry"]["diameter_um"] == 40


@pytest.mark.asyncio
@respx.mock
async def test_search_s2p_library_smoke(client: ChipletosClient, base_url: str) -> None:
    respx.get(f"{base_url}/v1/library/s2p").mock(
        return_value=httpx.Response(
            200,
            json={"total": 0, "items": [], "glasses_available": ["EagleXG"]},
        )
    )
    from chipletos_mcp.tools.search_s2p_library import TOOL

    result = await TOOL.run(client, {"glass": "EagleXG", "limit": 10})
    assert "items" in result


@pytest.mark.asyncio
@respx.mock
async def test_search_defects_smoke(client: ChipletosClient, base_url: str) -> None:
    respx.get(f"{base_url}/v1/defects/search").mock(
        return_value=httpx.Response(200, json={"total": 0, "defects": []})
    )
    from chipletos_mcp.tools.search_defects import TOOL

    result = await TOOL.run(client, {"q": "scratch", "limit": 10})
    assert "defects" in result


@pytest.mark.asyncio
@respx.mock
async def test_generate_coupon_smoke(client: ChipletosClient, base_url: str) -> None:
    respx.post(f"{base_url}/v1/coupons/export-fab").mock(
        return_value=httpx.Response(
            200,
            json={
                "request": {}, "drc": {"passed": True},
                "stack_up": {}, "sow": {}, "sow_markdown": "# SOW",
                "cost_estimate": {"low_usd": 55000, "high_usd": 165000},
                "notes": [], "partial": False, "partial_failure_reasons": [],
            },
        )
    )
    from chipletos_mcp.tools.generate_coupon import TOOL

    result = await TOOL.run(
        client,
        {"target_z0_ohm": 50, "freq_ghz": 28, "fab_partner": "amkor"},
    )
    assert result["drc"]["passed"] is True
    assert result["cost_estimate"]["low_usd"] == 55000
