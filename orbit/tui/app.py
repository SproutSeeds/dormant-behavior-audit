"""Orbit TUI application.

Problem-agnostic, model-agnostic Textual app for running investigation pipelines.
Generalized from sunflower-coda orchestrator/v2/tui/app.py.

Launch:
    python -m orbit.tui
    python -m orbit.tui --problem dormant_puzzle --scope model_1
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

from textual.app import App

from .screens.launch import LaunchScreen

logger = logging.getLogger("orbit.tui.app")

# Root of the problems/ directory (relative to this file's package root)
_PROBLEMS_DIR = Path(__file__).resolve().parents[2] / "problems"


@dataclass
class RunConfig:
    """Configuration collected from the LaunchScreen and passed to the pipeline."""

    problem_id: str = ""
    scope_key: str = ""          # "problem_id/scope_name"
    scope_yaml: Path | None = None
    state_dir: Path = field(default_factory=lambda: Path("data/state"))
    dry_run: bool = False         # Print plan but don't execute


class OrbitApp(App):
    """Main Textual application for Orbit pipeline runs."""

    TITLE = "Orbit — Investigation Pipeline"
    CSS_PATH = "styles/app.tcss"

    def __init__(self, initial_config: RunConfig | None = None) -> None:
        super().__init__()
        self.run_config = initial_config or RunConfig()

    def on_mount(self) -> None:
        self.push_screen(LaunchScreen(problems_dir=_PROBLEMS_DIR, config=self.run_config))


def main(args: list[str] | None = None) -> None:
    """Entry point for ``python -m orbit.tui``."""
    import argparse

    parser = argparse.ArgumentParser(description="Orbit Investigation Pipeline TUI")
    parser.add_argument("--problem", default="", help="Problem ID (e.g. dormant_puzzle)")
    parser.add_argument("--scope", default="", help="Scope name (e.g. model_1)")
    parser.add_argument("--state-dir", default="data/state", help="Directory for pipeline state files")
    parser.add_argument("--dry-run", action="store_true", help="Print plan without executing")
    ns = parser.parse_args(args)

    config = RunConfig(
        problem_id=ns.problem,
        scope_key=f"{ns.problem}/{ns.scope}" if ns.problem and ns.scope else "",
        state_dir=Path(ns.state_dir),
        dry_run=ns.dry_run,
    )

    app = OrbitApp(initial_config=config)
    app.run()
