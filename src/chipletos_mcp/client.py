"""Thin async HTTPS client for the public ChipletOS / Genesis API.

The Genesis API lives on Modal at:
    https://nickharris808--genesis-api-fastapi-app.modal.run

Some routes are fully public (in DEMO_PUBLIC_POSTS on the Modal middleware);
others require an `X-API-Key` header issued by the ChipletOS dashboard. This
client surfaces both lanes through the same interface — when a route 401s, the
error message tells the agent which env var to set.

Env vars:
    CHIPLETOS_API_URL   Base URL (default: the public Modal endpoint).
    CHIPLETOS_API_KEY   Optional API key for gated routes.
    CHIPLETOS_TIMEOUT_S Optional HTTP timeout in seconds (default: 30).
"""

from __future__ import annotations

import os
from typing import Any

import httpx

DEFAULT_BASE_URL = "https://nickharris808--genesis-api-fastapi-app.modal.run"
DEFAULT_TIMEOUT_S = 30.0
USER_AGENT = "chipletos-mcp/0.1.0 (+https://github.com/nickharris808/chipletos-mcp)"


class ChipletosAPIError(RuntimeError):
    """Raised when the Genesis API returns a non-2xx response.

    The string form is LLM-friendly: it states the route, the status code,
    and the actionable next step (set an env var, ease the input, etc.).
    """

    def __init__(self, method: str, path: str, status: int, body: str) -> None:
        self.method = method
        self.path = path
        self.status = status
        self.body = body
        hint = _hint_for_status(status, path)
        super().__init__(
            f"{method} {path} → HTTP {status}. {hint}\n"
            f"Response body (truncated 500 chars): {body[:500]}"
        )


def _hint_for_status(status: int, path: str) -> str:
    if status == 401:
        return (
            "Route requires authentication. Set CHIPLETOS_API_KEY in the MCP "
            "server env (issued from the ChipletOS dashboard at chipletos.com)."
        )
    if status == 403:
        return (
            "Route is forbidden for the current tier. Upgrade your ChipletOS "
            "dashboard plan or pick a public-demo equivalent route."
        )
    if status == 404:
        return "Route or witness id not found. Check spelling and the live /docs."
    if status == 422:
        return (
            "Request validation failed. Inspect the response body for the "
            "offending field, ease the value (it likely exceeds a Field ge/le "
            "bound), and retry."
        )
    if status == 429:
        return (
            "Rate-limited on the public demo lane (cap is ~30 req/min/IP). "
            "Slow down, or set CHIPLETOS_API_KEY for a higher per-tier limit."
        )
    if 500 <= status < 600:
        return (
            "Server-side error. Some endpoints (e.g. /v1/glass-pdk/geometry-pareto) "
            "have a known SIGSEGV on Modal for d/p ratios in [0.4, 0.5]; if you "
            "hit this, try a different ratio. Otherwise file an issue."
        )
    return "Unexpected status; check the response body."


class ChipletosClient:
    """Async httpx wrapper. Construct once and reuse across tool calls."""

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        timeout: float | None = None,
    ) -> None:
        self.base_url = (base_url or os.environ.get("CHIPLETOS_API_URL") or DEFAULT_BASE_URL).rstrip("/")
        self.api_key = api_key or os.environ.get("CHIPLETOS_API_KEY")
        self.timeout = timeout or float(os.environ.get("CHIPLETOS_TIMEOUT_S", DEFAULT_TIMEOUT_S))
        self._client: httpx.AsyncClient | None = None

    def _headers(self) -> dict[str, str]:
        h = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            # Sprint 46 P2-5: optional client-side hint that this is a public-demo
            # call; the Modal middleware does its own IP throttling regardless.
            "X-ChipletOS-Source": "mcp",
        }
        if self.api_key:
            h["X-API-Key"] = self.api_key
        return h

    async def _ensure(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout,
                headers=self._headers(),
                follow_redirects=True,
            )
        return self._client

    async def aclose(self) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    async def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        client = await self._ensure()
        resp = await client.get(path, params=_clean_params(params))
        return _parse(resp, "GET", path)

    async def post(self, path: str, json: dict[str, Any]) -> dict[str, Any]:
        client = await self._ensure()
        resp = await client.post(path, json=_clean_payload(json))
        return _parse(resp, "POST", path)


def _clean_params(params: dict[str, Any] | None) -> dict[str, Any] | None:
    if not params:
        return None
    return {k: v for k, v in params.items() if v is not None}


def _clean_payload(payload: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in payload.items() if v is not None}


def _parse(resp: httpx.Response, method: str, path: str) -> dict[str, Any]:
    if resp.status_code >= 400:
        raise ChipletosAPIError(method, path, resp.status_code, resp.text)
    if not resp.content:
        return {}
    try:
        data = resp.json()
    except ValueError as exc:
        raise ChipletosAPIError(
            method, path, resp.status_code, f"non-JSON response: {exc}"
        )
    if not isinstance(data, dict):
        # Some list endpoints (e.g. /v1/library/s2p paginated) return a dict;
        # if a route returns a bare list, wrap it for MCP friendliness.
        return {"items": data}
    return data
