# Installation

`chipletos-mcp` is a Python package that exposes a Model Context Protocol
server over stdio. It works with any MCP-compatible client: Claude Desktop,
Cursor, Anthropic SDK, generic MCP harness, etc.

## Prerequisites

- Python 3.10 or newer
- `pip` (or `uv`, `pipx`, etc.)

## Install from PyPI

```bash
pip install chipletos-mcp
```

This installs the `chipletos-mcp` console script.

## Install from source

```bash
git clone https://github.com/nickharris808/chipletos-mcp.git
cd chipletos-mcp
pip install -e .
```

## Verify the install

```bash
chipletos-mcp --help 2>&1 | head -3
# Or run the server in a terminal (it'll block on stdin waiting for MCP messages):
chipletos-mcp
```

## Environment variables

| Var | Default | Purpose |
|---|---|---|
| `CHIPLETOS_API_URL` | `https://nickharris808--genesis-api-fastapi-app.modal.run` | ChipletOS Genesis API base URL. |
| `CHIPLETOS_API_KEY` | (unset) | Optional. Required for gated routes (`predict-impedance`, `export-fab`). |
| `CHIPLETOS_TIMEOUT_S` | `30` | HTTP timeout in seconds. |
| `CHIPLETOS_MCP_LOG_LEVEL` | `INFO` | One of `DEBUG`, `INFO`, `WARNING`, `ERROR`. |

## Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`
(macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "chipletos": {
      "command": "chipletos-mcp",
      "env": {
        "CHIPLETOS_API_URL": "https://nickharris808--genesis-api-fastapi-app.modal.run",
        "CHIPLETOS_API_KEY": ""
      }
    }
  }
}
```

Restart Claude Desktop. You should see "chipletos" in the MCP server list
(click the plug icon in the bottom-left of the message composer).

## Cursor

Cursor reads MCP servers from `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "chipletos": {
      "command": "chipletos-mcp",
      "env": {
        "CHIPLETOS_API_URL": "https://nickharris808--genesis-api-fastapi-app.modal.run"
      }
    }
  }
}
```

Restart Cursor and the tools will appear in the agent panel.

## Anthropic API (programmatic)

Use the Anthropic Python SDK's MCP client:

```python
from anthropic import Anthropic
from anthropic.types.beta import BetaMessageParam

client = Anthropic()
response = client.beta.messages.create(
    model="claude-opus-4-7",
    max_tokens=4096,
    mcp_servers=[
        {
            "type": "stdio",
            "command": "chipletos-mcp",
            "env": {"CHIPLETOS_API_URL": "https://nickharris808--genesis-api-fastapi-app.modal.run"},
        }
    ],
    messages=[
        BetaMessageParam(
            role="user",
            content="I need a 50 Ω glass-TGV at 28 GHz on Eagle XG. What dimensions?",
        )
    ],
)
print(response.content)
```

## Troubleshooting

- **`chipletos-mcp: command not found`** — pip put it in a directory not on
  `$PATH`. Try `python -m chipletos_mcp.server` instead, or find the
  install dir with `pip show chipletos-mcp`.
- **Every tool 401s** — the route requires `CHIPLETOS_API_KEY`. Set it in
  the MCP server env (see above). Get a key from
  <https://chipletos.com/dashboard>.
- **Tools 429** — public-demo lane is rate-limited to ~30 req/min/IP.
  Slow down or set `CHIPLETOS_API_KEY` for a higher per-tier limit.
- **Tool calls hang** — the default 30 s timeout may be too short for
  `chipletos_pareto_design` with `refine_with_solver: true`. Bump
  `CHIPLETOS_TIMEOUT_S=120`.
