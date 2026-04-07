"""Orbit — top-level entry point.

Convenience functions to run a pipeline from a scope YAML,
either headless (CLI) or with the TUI.
"""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path

from .events import LoggingObserver, OrbitObserver
from .pipeline import Pipeline
from .scope import load_scope, discover_scopes
from .state import PipelineState

logger = logging.getLogger("orbit")


async def run_headless(
    scope_yaml: Path,
    state_dir: Path | None = None,
    observers: list[OrbitObserver] | None = None,
) -> PipelineState:
    """Run a pipeline headless (no TUI). Returns final state."""
    scope = load_scope(scope_yaml)
    pipeline = Pipeline(
        scope,
        state_dir=state_dir or Path("data/state"),
        observers=observers,
    )
    return await pipeline.run()


def run_tui(
    scope_yaml: Path | None = None,
    problem_id: str = "",
    scope_key: str = "",
    state_dir: Path | None = None,
) -> None:
    """Launch the Textual TUI for interactive pipeline runs."""
    from orbit.tui.app import OrbitApp, RunConfig

    config = RunConfig(
        problem_id=problem_id,
        scope_key=scope_key,
        scope_yaml=scope_yaml,
        state_dir=state_dir or Path("data/state"),
    )
    app = OrbitApp(initial_config=config)
    app.run()
