"""Launch screen — select a problem scope and start a pipeline run.

Generalised from sunflower-coda orchestrator/v2/tui/screens/launch.py.
"""

from __future__ import annotations

import asyncio
from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal, Container
from textual.message import Message
from textual.screen import Screen
from textual.widgets import Button, Label, Select, Static, Footer, Header

from orbit.core.scope import discover_scopes, load_scope


class RunRequested(Message):
    """Posted when the user presses Run to start a pipeline."""

    def __init__(self, scope_yaml: Path) -> None:
        super().__init__()
        self.scope_yaml = scope_yaml


class LaunchScreen(Screen):
    """Problem and scope selection screen."""

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "run", "Run"),
    ]

    CSS = """
    LaunchScreen {
        align: center middle;
    }

    #launch-panel {
        width: 72;
        height: auto;
        border: round $primary;
        padding: 1 2;
    }

    #title {
        text-style: bold;
        color: $accent;
        margin-bottom: 1;
    }

    .row {
        height: 3;
        margin-bottom: 1;
    }

    .label {
        width: 18;
        padding-top: 1;
        color: $text-muted;
    }

    Select {
        width: 1fr;
    }

    #scope-description {
        color: $text-muted;
        margin: 1 0;
        height: 3;
    }

    #btn-row {
        margin-top: 1;
        height: 3;
    }

    Button {
        margin-right: 1;
    }
    """

    def __init__(self, problems_dir: Path, config=None) -> None:
        super().__init__()
        self._problems_dir = problems_dir
        self._config = config
        self._scopes: list[tuple[str, str, Path]] = []  # (display, key, yaml_path)

    def on_mount(self) -> None:
        self._scopes = discover_scopes(self._problems_dir)
        select = self.query_one("#scope-select", Select)
        options = [(name, key) for name, key, _ in self._scopes]
        if options:
            select.set_options(options)
            # Pre-select if config provided
            if self._config and self._config.scope_key:
                for _, key, _ in self._scopes:
                    if key == self._config.scope_key:
                        select.value = key
                        break
            self._update_description()
        else:
            self.query_one("#scope-description", Static).update(
                "[dim]No scopes found. Create problems/<id>/scopes/<name>.yaml[/dim]"
            )
            self.query_one("#btn-run", Button).disabled = True

    def _update_description(self) -> None:
        select = self.query_one("#scope-select", Select)
        if select.value is Select.BLANK:
            return
        for name, key, yaml_path in self._scopes:
            if key == select.value:
                try:
                    scope = load_scope(yaml_path)
                    stage_names = ", ".join(s.name for s in scope.enabled_stages())
                    desc = scope.description or f"Stages: {stage_names}"
                    self.query_one("#scope-description", Static).update(desc)
                except Exception as exc:
                    self.query_one("#scope-description", Static).update(f"[red]Error loading scope: {exc}[/red]")
                return

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container(id="launch-panel"):
            yield Static("Orbit — Investigation Pipeline", id="title")
            with Horizontal(classes="row"):
                yield Label("Scope", classes="label")
                yield Select([], id="scope-select", prompt="Select a scope...")
            yield Static("", id="scope-description")
            with Horizontal(id="btn-row"):
                yield Button("Run", variant="primary", id="btn-run")
                yield Button("Quit", variant="default", id="btn-quit")
        yield Footer()

    def on_select_changed(self, event: Select.Changed) -> None:
        if event.select.id == "scope-select":
            self._update_description()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-run":
            self.action_run()
        elif event.button.id == "btn-quit":
            self.action_quit()

    def action_run(self) -> None:
        select = self.query_one("#scope-select", Select)
        if select.value is Select.BLANK:
            return
        for name, key, yaml_path in self._scopes:
            if key == select.value:
                self.post_message(RunRequested(yaml_path))
                self.app.push_screen(
                    _DashboardScreenRef(yaml_path=yaml_path, config=self._config)
                )
                return

    def action_quit(self) -> None:
        self.app.exit()


def _DashboardScreenRef(yaml_path: Path, config):
    """Lazy import to avoid circular dependency."""
    from .dashboard import DashboardScreen
    return DashboardScreen(yaml_path=yaml_path, config=config)
