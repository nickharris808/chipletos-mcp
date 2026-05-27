"""chipletos_leaderboard — the open Glass-TGV signoff benchmark leaderboard.

Wraps GET /v1/bench/leaderboard.

Returns the current standings for the open Glass-TGV Z₀ Signoff Benchmark
(public-glass test split, BEM-truth reference — NOT VNA-measured). Ties the MCP
to the open benchmark: an agent can show the bar (kNN / RF / ChipletOS surrogate)
and how a user's own model would rank.
"""

from __future__ import annotations

from typing import Any

from ..client import ChipletosClient
from . import ChipletosTool

INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "task": {
            "type": "string",
            "enum": ["z0", "thermal", "crosstalk", "pdn", "warpage"],
            "default": "z0",
            "description": "Benchmark task (default z0 = characteristic impedance).",
        },
        "substrate": {
            "type": "string",
            "enum": ["glass", "organic", "silicon", "ceramic"],
            "default": "glass",
            "description": "Substrate class (default glass).",
        },
        "limit": {"type": "integer", "default": 10, "description": "Max rows."},
    },
    "additionalProperties": False,
}


async def _run(client: ChipletosClient, args: dict[str, Any]) -> dict[str, Any]:
    task = args.get("task", "z0")
    substrate = args.get("substrate", "glass")
    limit = int(args.get("limit", 10))
    return await client.get(
        f"/v1/bench/leaderboard?task={task}&substrate={substrate}&limit={limit}"
    )


TOOL = ChipletosTool(
    tool_name="chipletos_leaderboard",
    description=(
        "Return the open Glass-TGV signoff benchmark leaderboard (kNN / Random "
        "Forest / ChipletOS surrogate baselines, ordered by MAE). Reference truth "
        "is the BEM solver on a public-glass test split, NOT VNA-measured. Use when "
        "the user asks 'how good is the surrogate vs baselines?', wants the benchmark "
        "bar, or asks where their own model would rank."
    ),
    input_schema=INPUT_SCHEMA,
    run=_run,
)
