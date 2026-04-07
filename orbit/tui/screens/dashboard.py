"""Dashboard screen — real-time stage progress during a pipeline run.

Generalised from sunflower-coda orchestrator/v2/tui/screens/dashboard.py.
"""

from __future__ import annotations

import asyncio
import threading
import time
from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal, VerticalScroll, Container
from textual.message import Message
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, ProgressBar, Static, RichLog

from orbit.core.events import CompositeObserver, EventKind, OrbitEvent, OrbitObserver
from orbit.core.scope import load_scope
from orbit.core.pipeline import Pipeline
from orbit.core.state import PipelineState


# ---------------------------------------------------------------------------
# Thread → TUI bridge
# ---------------------------------------------------------------------------

class _EventMessage(Message):
    """Carries an OrbitEvent from background thread to the TUI message queue."""

    def __init__(self, event: OrbitEvent) -> None:
        super().__init__()
        self.event = event


class _TuiObserver:
    """Posts events onto the dashboard's Textual message queue (thread-safe)."""

    def __init__(self, screen: Screen) -> None:
        self._screen = screen

    def on_event(self, event: OrbitEvent) -> None:
        try:
            self._screen.post_message(_EventMessage(event))
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Dashboard screen
# ---------------------------------------------------------------------------

class DashboardScreen(Screen):
    """Live stage-by-stage progress view."""

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("s", "stop", "Stop"),
    ]

    CSS = """
    DashboardScreen {
        layout: vertical;
    }

    #header-bar {
        height: 3;
        background: $panel;
        padding: 0 2;
    }

    #header-title {
        text-style: bold;
        color: $accent;
        padding-top: 1;
    }

    #stages-panel {
        width: 1fr;
        height: auto;
        border: round $surface;
        padding: 1 2;
        margin: 1;
    }

    .stage-row {
        height: 3;
    }

    .stage-name {
        width: 24;
        padding-top: 1;
    }

    .stage-status {
        width: 12;
        padding-top: 1;
    }

    .stage-summary {
        width: 1fr;
        padding-top: 1;
        color: $text-muted;
    }

    #log-panel {
        height: 1fr;
        border: round $surface;
        margin: 0 1 1 1;
    }

    #findings-panel {
        height: auto;
        border: round $success;
        padding: 1 2;
        margin: 0 1;
    }

    #btn-row {
        height: 3;
        padding: 0 2;
    }

    Button {
        margin-right: 1;
    }
    """

    def __init__(self, yaml_path: Path, config=None) -> None:
        super().__init__()
        self._yaml_path = yaml_path
        self._config = config
        self._pipeline: Pipeline | None = None
        self._stop_requested = False
        self._stage_rows: dict[str, dict] = {}  # stage_name → {name_widget, status_widget, summary_widget}

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal(id="header-bar"):
            yield Static("", id="header-title")
        with Container(id="stages-panel"):
            yield Static("[dim]Loading...[/dim]", id="stages-container")
        with VerticalScroll(id="log-panel"):
            yield RichLog(id="event-log", markup=True, highlight=True)
        with Container(id="findings-panel"):
            yield Static("[dim]No findings yet.[/dim]", id="findings-text")
        with Horizontal(id="btn-row"):
            yield Button("Stop", variant="warning", id="btn-stop")
            yield Button("Back", variant="default", id="btn-back")
        yield Footer()

    def on_mount(self) -> None:
        try:
            scope = load_scope(self._yaml_path)
            self.query_one("#header-title", Static).update(
                f"[bold]{scope.display_name}[/bold]  [dim]run starting...[/dim]"
            )
            self._build_stage_rows(scope)
        except Exception as exc:
            self._log(f"[red]Error loading scope: {exc}[/red]")
            return

        # Launch pipeline in background thread
        observer = _TuiObserver(self)
        state_dir = (self._config.state_dir if self._config else None) or Path("data/state")

        def _run() -> None:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                pipeline = Pipeline(scope, state_dir=state_dir, observers=[observer])
                self._pipeline = pipeline
                loop.run_until_complete(pipeline.run())
            finally:
                loop.close()

        t = threading.Thread(target=_run, daemon=True)
        t.start()

    def _build_stage_rows(self, scope) -> None:
        stages_container = self.query_one("#stages-container", Static)
        # Replace Static with a Vertical of rows
        # Since we're building dynamically, we compose them as markup
        lines = []
        for s in scope.enabled_stages():
            lines.append(f"  [dim]◦[/dim] [bold]{s.name:<24}[/bold] [dim]pending[/dim]")
        stages_container.update("\n".join(lines) if lines else "[dim]No stages.[/dim]")
        self._stage_lines = {s.name: i for i, s in enumerate(scope.enabled_stages())}
        self._scope = scope

    def _update_stage_display(self) -> None:
        if not hasattr(self, "_scope"):
            return
        lines = []
        for s in self._scope.enabled_stages():
            name = s.name
            status = self._stage_status.get(name, "pending")
            summary = self._stage_summaries.get(name, "")
            icon = {"pending": "[dim]◦[/dim]", "running": "[yellow]●[/yellow]",
                    "completed": "[green]✓[/green]", "failed": "[red]✗[/red]",
                    "skipped": "[dim]⊘[/dim]"}.get(status, "[dim]◦[/dim]")
            status_markup = {
                "pending": "[dim]pending[/dim]",
                "running": "[yellow]running[/yellow]",
                "completed": "[green]done[/green]",
                "failed": "[red]failed[/red]",
                "skipped": "[dim]skipped[/dim]",
            }.get(status, f"[dim]{status}[/dim]")
            summary_part = f"  [dim]{summary[:50]}[/dim]" if summary else ""
            lines.append(f"  {icon} [bold]{name:<24}[/bold] {status_markup}{summary_part}")
        self.query_one("#stages-container", Static).update(
            "\n".join(lines) if lines else "[dim]No stages.[/dim]"
        )

    def _log(self, message: str) -> None:
        try:
            log = self.query_one("#event-log", RichLog)
            log.write(message)
        except Exception:
            pass

    def on__event_message(self, message: _EventMessage) -> None:
        event = message.event
        k = event.kind
        d = event.data

        if not hasattr(self, "_stage_status"):
            self._stage_status: dict[str, str] = {}
            self._stage_summaries: dict[str, str] = {}

        if k == EventKind.PIPELINE_STARTED:
            self._log(f"[bold green]Pipeline started[/bold green] — scope={d.get('scope_name')} run={event.run_id}")
            if hasattr(self, "_scope"):
                title = self.query_one("#header-title", Static)
                if hasattr(self, "_scope"):
                    title.update(f"[bold]{self._scope.display_name}[/bold]  [dim]{event.run_id}[/dim]")

        elif k == EventKind.STAGE_STARTED:
            name = d.get("stage_name", "")
            self._stage_status[name] = "running"
            self._update_stage_display()
            self._log(f"[yellow]▶ Stage {d.get('stage_index')}/{d.get('total_stages')}:[/yellow] {name}")

        elif k == EventKind.STAGE_COMPLETED:
            name = d.get("stage_name", "")
            self._stage_status[name] = "completed"
            self._stage_summaries[name] = d.get("summary", "")
            self._update_stage_display()
            self._log(
                f"[green]✓[/green] {name} — {d.get('elapsed', 0):.1f}s — {d.get('summary', '')}"
            )

        elif k == EventKind.STAGE_SKIPPED:
            name = d.get("stage_name", "")
            self._stage_status[name] = "skipped"
            self._update_stage_display()
            self._log(f"[dim]⊘ {name} skipped: {d.get('reason', '')}[/dim]")

        elif k == EventKind.STAGE_ERROR:
            name = d.get("stage_name", "")
            self._stage_status[name] = "failed"
            self._update_stage_display()
            self._log(f"[red]✗ {name} failed: {d.get('error', '')}[/red]")

        elif k == EventKind.FINDING_DISCOVERED:
            fid = d.get("finding_id", "")
            cat = d.get("category", "")
            conf = d.get("confidence", 0)
            desc = d.get("description", "")
            self._log(f"[magenta]★ FINDING[/magenta] [{cat}] {fid} conf={conf:.2f}: {desc}")
            self._update_findings()

        elif k == EventKind.FINDING_CONFIRMED:
            self._log(f"[bold magenta]★★ CONFIRMED[/bold magenta] {d.get('finding_id')}: {d.get('verification_detail')}")

        elif k == EventKind.WORKER_STARTED:
            self._log(f"[dim]  worker {d.get('worker_id')}: {d.get('job_description')}[/dim]")

        elif k == EventKind.WORKER_COMPLETED:
            status = d.get("status", "?")
            color = "green" if status == "ok" else "red"
            self._log(f"[{color}]  worker {d.get('worker_id')}: {status} — {d.get('result_summary', '')}[/{color}]")

        elif k == EventKind.PROGRESS:
            done, total = d.get("done", 0), d.get("total", 0)
            msg = d.get("message", "")
            if total:
                pct = int(done / total * 100)
                self._log(f"[dim]  {d.get('stage_name')} {done}/{total} ({pct}%) {msg}[/dim]")

        elif k == EventKind.RATE_LIMITED:
            self._log(f"[yellow]⚡ Rate limited — retry after {d.get('retry_after_sec')}s[/yellow]")

        elif k == EventKind.INFRA_HALT:
            self._log(f"[bold red]HALT: {d.get('error')}[/bold red]")

        elif k == EventKind.PIPELINE_COMPLETED:
            elapsed = d.get("elapsed", 0)
            findings = d.get("finding_count", 0)
            self._log(
                f"[bold green]Pipeline complete[/bold green] — {elapsed:.1f}s — {findings} findings"
            )
            self._update_findings()
            if hasattr(self, "_scope"):
                title = self.query_one("#header-title", Static)
                title.update(f"[bold]{self._scope.display_name}[/bold]  [green]COMPLETE[/green] in {elapsed:.0f}s")

        elif k == EventKind.PIPELINE_ERROR:
            self._log(f"[bold red]Pipeline error: {d.get('error')}[/bold red]")

    def _update_findings(self) -> None:
        if self._pipeline and self._pipeline.state.findings:
            findings = self._pipeline.state.findings
            lines = []
            for f in findings[-10:]:  # Show last 10
                conf = f.get("confidence", 0)
                cat = f.get("category", "?")
                desc = f.get("description", "")[:60]
                lines.append(f"  [magenta]★[/magenta] [{cat}] conf={conf:.2f}: {desc}")
            self.query_one("#findings-text", Static).update("\n".join(lines))
        else:
            self.query_one("#findings-text", Static).update("[dim]No findings yet.[/dim]")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-stop":
            self.action_stop()
        elif event.button.id == "btn-back":
            self.app.pop_screen()

    def action_stop(self) -> None:
        self._stop_requested = True
        self._log("[yellow]Stop requested...[/yellow]")

    def action_quit(self) -> None:
        self.app.exit()
