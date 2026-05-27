"""Tests for ChipletosClient HTTP behaviour.

We mock httpx with respx so nothing here hits the live Modal API.
"""

from __future__ import annotations

import httpx
import pytest
import respx

from chipletos_mcp.client import ChipletosAPIError, ChipletosClient


@pytest.mark.asyncio
@respx.mock
async def test_get_happy_path(client: ChipletosClient, base_url: str) -> None:
    route = respx.get(f"{base_url}/v1/glass-pdk/cross-solver-matrix").mock(
        return_value=httpx.Response(200, json={"n_geometries": 100})
    )
    result = await client.get("/v1/glass-pdk/cross-solver-matrix")
    assert route.called
    assert result["n_geometries"] == 100


@pytest.mark.asyncio
@respx.mock
async def test_post_happy_path(client: ChipletosClient, base_url: str) -> None:
    route = respx.post(f"{base_url}/v1/glass-pdk/drc-validate").mock(
        return_value=httpx.Response(200, json={"passed": True, "n_violations": 0})
    )
    result = await client.post("/v1/glass-pdk/drc-validate", {"via_geometries": []})
    assert route.called
    assert result["passed"] is True


@pytest.mark.asyncio
@respx.mock
async def test_401_raises_with_hint(client: ChipletosClient, base_url: str) -> None:
    respx.post(f"{base_url}/v1/coupons/export-fab").mock(
        return_value=httpx.Response(401, json={"error": "unauthorized"})
    )
    with pytest.raises(ChipletosAPIError) as excinfo:
        await client.post("/v1/coupons/export-fab", {"target_z0_ohm": 50})
    assert excinfo.value.status == 401
    assert "CHIPLETOS_API_KEY" in str(excinfo.value)


@pytest.mark.asyncio
@respx.mock
async def test_429_raises_with_hint(client: ChipletosClient, base_url: str) -> None:
    respx.post(f"{base_url}/v1/glass-pdk/geometry-pareto").mock(
        return_value=httpx.Response(429, json={"error": "rate_limited"})
    )
    with pytest.raises(ChipletosAPIError) as excinfo:
        await client.post("/v1/glass-pdk/geometry-pareto", {})
    assert excinfo.value.status == 429
    assert "Rate-limited" in str(excinfo.value) or "30 req/min" in str(excinfo.value)


@pytest.mark.asyncio
@respx.mock
async def test_500_raises_with_hint(client: ChipletosClient, base_url: str) -> None:
    respx.post(f"{base_url}/v1/glass-pdk/geometry-pareto").mock(
        return_value=httpx.Response(500, json={"error": "internal"})
    )
    with pytest.raises(ChipletosAPIError) as excinfo:
        await client.post("/v1/glass-pdk/geometry-pareto", {})
    assert excinfo.value.status == 500
    assert "Server-side" in str(excinfo.value) or "SIGSEGV" in str(excinfo.value)


@pytest.mark.asyncio
async def test_api_key_header_is_set(base_url: str) -> None:
    c = ChipletosClient(base_url=base_url, api_key="test-key-abc", timeout=5.0)
    try:
        h = c._headers()
        assert h.get("X-API-Key") == "test-key-abc"
        assert "chipletos-mcp" in h.get("User-Agent", "")
    finally:
        await c.aclose()


@pytest.mark.asyncio
async def test_clean_params_drops_none(base_url: str) -> None:
    from chipletos_mcp.client import _clean_params, _clean_payload

    assert _clean_params({"a": 1, "b": None, "c": "x"}) == {"a": 1, "c": "x"}
    assert _clean_params({}) is None
    assert _clean_params(None) is None
    assert _clean_payload({"a": 1, "b": None}) == {"a": 1}
