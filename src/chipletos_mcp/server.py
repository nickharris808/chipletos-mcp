"""MCP server entrypoint for chipletos-mcp.

Registers the 14 ChipletOS tools and runs over stdio (the canonical MCP
transport for desktop agents). The console-script `chipletos-mcp` calls
`main()` which kicks off the asyncio loop.

To debug locally:
    python -m chipletos_mcp.server
"""

from __future__ import annotations

import asyncio
import logging
import os
import sys
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool, ToolAnnotations

from . import __version__
from .client import ChipletosAPIError, ChipletosClient
from .tools import ALL_TOOLS

log = logging.getLogger("chipletos_mcp")


def _configure_logging() -> None:
    # MCP transport over stdio MUST keep stdout free of log noise; everything
    # goes to stderr.
    level_name = os.environ.get("CHIPLETOS_MCP_LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    logging.basicConfig(
        level=level,
        stream=sys.stderr,
        format="%(asctime)s %(levelname)s %(name)s | %(message)s",
    )


def build_server(client: ChipletosClient | None = None) -> Server:
    """Construct an MCP Server with all ChipletOS tools registered.

    Exposed so tests can spin one up without going through stdio.
    """
    server: Server = Server("chipletos-mcp")
    client = client or ChipletosClient()

    tool_map = {t.tool_name: t for t in ALL_TOOLS}

    def _title(name: str) -> str:
        return name.removeprefix("chipletos_").replace("_", " ").title()

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        # Every ChipletOS tool is read-only from the caller's perspective: it queries
        # or computes via the public API and returns data; none mutate the caller's
        # environment or delete state. openWorldHint=True because each calls an external
        # HTTPS service. Safety annotations are required by Anthropic's Connectors
        # Directory review (missing readOnlyHint/destructiveHint causes ~30% of rejections).
        return [
            Tool(
                name=t.tool_name,
                description=t.description,
                inputSchema=t.input_schema,
                annotations=ToolAnnotations(
                    title=_title(t.tool_name),
                    readOnlyHint=True,
                    destructiveHint=False,
                    idempotentHint=True,
                    openWorldHint=True,
                ),
            )
            for t in ALL_TOOLS
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
        if name not in tool_map:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
        tool = tool_map[name]
        try:
            result = await tool.run(client, arguments or {})
            return [TextContent(type="text", text=_to_text(result))]
        except ChipletosAPIError as exc:
            return [TextContent(type="text", text=f"ChipletOS API error: {exc}")]
        except Exception as exc:  # noqa: BLE001
            log.exception("tool %s raised", name)
            return [TextContent(type="text", text=f"Tool error: {exc}")]

    return server


def _to_text(result: Any) -> str:
    """Render a JSON result as compact text for the LLM."""
    import json

    try:
        return json.dumps(result, indent=2, default=str)
    except Exception:
        return str(result)


async def _run() -> None:
    _configure_logging()
    log.info("chipletos-mcp v%s starting (CHIPLETOS_API_URL=%s)", __version__,
             os.environ.get("CHIPLETOS_API_URL", "default-modal"))
    client = ChipletosClient()
    server = build_server(client)
    try:
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options(),
            )
    finally:
        await client.aclose()


def main() -> None:
    """Console-script entrypoint (`chipletos-mcp`)."""
    try:
        asyncio.run(_run())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
