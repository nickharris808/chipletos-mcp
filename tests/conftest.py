"""Shared pytest fixtures for chipletos-mcp."""

from __future__ import annotations

import pytest

from chipletos_mcp.client import ChipletosClient


@pytest.fixture
def base_url() -> str:
    """Base URL the client will hit in tests (matches respx mounts)."""
    return "https://test.chipletos.local"


@pytest.fixture
async def client(base_url: str) -> ChipletosClient:
    """A ChipletosClient pointed at the test base URL.

    Tests should `respx.mock` the routes they care about; nothing here
    talks to the live Modal API.
    """
    c = ChipletosClient(base_url=base_url, api_key=None, timeout=5.0)
    try:
        yield c
    finally:
        await c.aclose()
