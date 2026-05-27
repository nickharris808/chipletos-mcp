"""Tool registry for chipletos-mcp.

Each tool module exposes a `TOOL` object (a `ChipletosTool` dataclass-ish
record with `tool_name`, `description`, `input_schema`, and an async `run`
coroutine). `ALL_TOOLS` aggregates them in the order surfaced to the agent.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Awaitable, Callable

from ..client import ChipletosClient


@dataclass(frozen=True)
class ChipletosTool:
    tool_name: str
    description: str
    input_schema: dict[str, Any]
    run: Callable[[ChipletosClient, dict[str, Any]], Awaitable[dict[str, Any]]]


from .predict_impedance import TOOL as predict_impedance_tool  # noqa: E402
from .pareto_design import TOOL as pareto_design_tool  # noqa: E402
from .inverse_design import TOOL as inverse_design_tool  # noqa: E402
from .cross_solver_matrix import TOOL as cross_solver_matrix_tool  # noqa: E402
from .drc_validate import TOOL as drc_validate_tool  # noqa: E402
from .validate_against_measurement import TOOL as validate_against_measurement_tool  # noqa: E402
from .lab_readiness_score import TOOL as lab_readiness_score_tool  # noqa: E402
from .search_s2p_library import TOOL as search_s2p_library_tool  # noqa: E402
from .search_defects import TOOL as search_defects_tool  # noqa: E402
from .generate_coupon import TOOL as generate_coupon_tool  # noqa: E402

# ChipletOS Photonic Signoff sub-brand (Sprint 50/51 alpha — see Genesis CLAUDE.md::C39)
from .predict_waveguide_mode import TOOL as predict_waveguide_mode_tool  # noqa: E402
from .photonic_signoff_health import TOOL as photonic_signoff_health_tool  # noqa: E402
from .photonic_drc import TOOL as photonic_drc_tool  # noqa: E402
from .photonic_validate_ieee import TOOL as photonic_validate_ieee_tool  # noqa: E402

# Open benchmark leaderboard (ties the MCP to the public Glass-TGV signoff benchmark)
from .leaderboard import TOOL as leaderboard_tool  # noqa: E402

ALL_TOOLS: list[ChipletosTool] = [
    # Glass-TGV / chiplet packaging signoff
    predict_impedance_tool,
    pareto_design_tool,
    inverse_design_tool,
    cross_solver_matrix_tool,
    drc_validate_tool,
    validate_against_measurement_tool,
    lab_readiness_score_tool,
    search_s2p_library_tool,
    search_defects_tool,
    generate_coupon_tool,
    # ChipletOS Photonic Signoff (alpha)
    predict_waveguide_mode_tool,
    photonic_signoff_health_tool,
    photonic_drc_tool,
    photonic_validate_ieee_tool,
    # Open benchmark
    leaderboard_tool,
]

__all__ = ["ChipletosTool", "ALL_TOOLS"]
