"""chipletos_cross_solver_matrix — cross-solver disagreement witness.

Wraps GET /v1/glass-pdk/cross-solver-matrix.

Returns the latest 100-geometry cross-solver matrix (BEM vs Palace vs OpenEMS
vs gprMax) with pairwise MAE. Honest disclosure: only BEM_multiconductor
currently produces 100/100 results; other solver integrations are in flight.
"""

from __future__ import annotations

from typing import Any

from ..client import ChipletosClient
from . import ChipletosTool

INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {},
    "additionalProperties": False,
}


async def _run(client: ChipletosClient, args: dict[str, Any]) -> dict[str, Any]:
    return await client.get("/v1/glass-pdk/cross-solver-matrix")


TOOL = ChipletosTool(
    tool_name="chipletos_cross_solver_matrix",
    description=(
        "Return the latest 100-geometry cross-solver disagreement witness "
        "(BEM vs Palace vs OpenEMS vs gprMax). Surfaces pairwise MAE and "
        "honest_caveat re: which solvers are fully wired. Use when the user "
        "asks 'how does the surrogate compare to full-wave solvers?' or wants "
        "physics-envelope context."
    ),
    input_schema=INPUT_SCHEMA,
    run=_run,
)
