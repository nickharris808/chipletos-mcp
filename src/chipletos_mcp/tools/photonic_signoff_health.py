"""chipletos_photonic_signoff_health — ChipletOS Photonic Signoff capability inventory.

Wraps GET /v1/photonics/signoff-health.

Returns the live status of the ChipletOS Photonic Signoff sub-brand: supported
primitives (waveguide / MZI / MMI / ring / grating / photonic-crystal), per-
primitive status (alpha vs queued), solver-stack availability (Meep FDTD,
TMM analytical, gprMax planned), surrogate training status, and the
photonic audit-gate roster (G18-G22).

Use for capability discovery before kicking off a design session — answers
"what can ChipletOS photonics actually do today?".
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
    return await client.get("/v1/photonics/signoff-health")


TOOL = ChipletosTool(
    tool_name="chipletos_photonic_signoff_health",
    description=(
        "Get the live status of the ChipletOS Photonic Signoff sub-brand — "
        "which primitives are alpha vs queued, solver stack availability, "
        "audit gate status. Use for capability discovery."
    ),
    input_schema=INPUT_SCHEMA,
    run=_run,
)
