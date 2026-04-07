"""Event protocol for the Orbit pipeline framework.

Provides a lightweight observer interface so the pipeline can emit structured
events during its lifecycle. Consumers implement OrbitObserver to receive
live updates — the TUI, file writers, loggers, etc.

No Textual or UI dependency — pure stdlib.
Generalized from sunflower-coda orchestrator/v2/events.py.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Protocol, runtime_checkable

logger = logging.getLogger("orbit.pipeline")


class EventKind(Enum):
    """All lifecycle events a pipeline can emit."""

    # Pipeline lifecycle
    PIPELINE_STARTED = auto()       # data: problem_id, run_id, scope_name
    PIPELINE_COMPLETED = auto()     # data: problem_id, run_id, status, elapsed
    PIPELINE_STOPPED = auto()       # data: problem_id, run_id, reason
    PIPELINE_ERROR = auto()         # data: problem_id, run_id, error

    # Stage lifecycle
    STAGE_STARTED = auto()          # data: stage_name, stage_index, total_stages
    STAGE_COMPLETED = auto()        # data: stage_name, status, elapsed, summary
    STAGE_SKIPPED = auto()          # data: stage_name, reason
    STAGE_ERROR = auto()            # data: stage_name, error
    STAGE_RETRY = auto()            # data: stage_name, attempt, max_retries, error, delay_sec

    # Worker lifecycle (parallel job inside a stage)
    WORKER_STARTED = auto()         # data: worker_id, job_description
    WORKER_COMPLETED = auto()       # data: worker_id, status, result_summary
    WORKER_ERROR = auto()           # data: worker_id, error

    # Finding lifecycle
    FINDING_DISCOVERED = auto()     # data: finding_id, category, description, confidence
    FINDING_CONFIRMED = auto()      # data: finding_id, verification_detail
    FINDING_REJECTED = auto()       # data: finding_id, reason

    # Budget / rate-limit
    BUDGET_WARNING = auto()         # data: message, remaining_usd
    RATE_LIMITED = auto()           # data: retry_after_sec, message
    INFRA_HALT = auto()             # data: error — user must fix & relaunch

    # Progress ticks (optional high-frequency updates)
    PROGRESS = auto()               # data: stage_name, done, total, message


@dataclass
class OrbitEvent:
    """A single lifecycle event from the pipeline.

    ``data`` carries event-specific payload. Keys vary by EventKind (see above).
    """

    kind: EventKind
    timestamp: float = field(default_factory=time.time)
    run_id: str = ""
    problem_id: str = ""
    data: dict = field(default_factory=dict)


@runtime_checkable
class OrbitObserver(Protocol):
    """Observer protocol for pipeline lifecycle events.

    Implementations must be **thread-safe**: the pipeline may call on_event()
    from a background thread while the observer's owner runs on another.
    """

    def on_event(self, event: OrbitEvent) -> None: ...


class LoggingObserver:
    """Default observer — logs events at INFO level.

    Drop-in for headless / CI runs where there is no TUI.
    """

    def on_event(self, event: OrbitEvent) -> None:
        k = event.kind
        d = event.data

        if k == EventKind.PIPELINE_STARTED:
            logger.info(
                "[%s] Pipeline started — scope=%s run=%s",
                d.get("problem_id", "?"),
                d.get("scope_name", "?"),
                event.run_id,
            )
        elif k == EventKind.PIPELINE_COMPLETED:
            logger.info(
                "[%s] Pipeline completed — status=%s elapsed=%.1fs",
                d.get("problem_id", "?"),
                d.get("status", "?"),
                d.get("elapsed", 0),
            )
        elif k == EventKind.PIPELINE_STOPPED:
            logger.info(
                "[%s] Pipeline stopped — %s",
                d.get("problem_id", "?"),
                d.get("reason", ""),
            )
        elif k == EventKind.PIPELINE_ERROR:
            logger.error(
                "[%s] Pipeline error — %s",
                d.get("problem_id", "?"),
                d.get("error", ""),
            )
        elif k == EventKind.STAGE_STARTED:
            logger.info(
                "Stage [%d/%d] %s — started",
                d.get("stage_index", 0),
                d.get("total_stages", 0),
                d.get("stage_name", "?"),
            )
        elif k == EventKind.STAGE_COMPLETED:
            logger.info(
                "Stage %s — %s in %.1fs: %s",
                d.get("stage_name", "?"),
                d.get("status", "?"),
                d.get("elapsed", 0),
                d.get("summary", ""),
            )
        elif k == EventKind.STAGE_SKIPPED:
            logger.info(
                "Stage %s — skipped: %s",
                d.get("stage_name", "?"),
                d.get("reason", ""),
            )
        elif k == EventKind.STAGE_ERROR:
            logger.error(
                "Stage %s — error: %s",
                d.get("stage_name", "?"),
                d.get("error", ""),
            )
        elif k == EventKind.STAGE_RETRY:
            logger.warning(
                "Stage %s — attempt %d/%d failed (%s), retrying in %.1fs",
                d.get("stage_name", "?"),
                d.get("attempt", 1),
                d.get("max_retries", 1) + 1,
                d.get("error", ""),
                d.get("delay_sec", 0),
            )
        elif k == EventKind.WORKER_STARTED:
            logger.info("Worker %s — %s", d.get("worker_id", "?"), d.get("job_description", ""))
        elif k == EventKind.WORKER_COMPLETED:
            logger.info(
                "Worker %s — %s: %s",
                d.get("worker_id", "?"),
                d.get("status", "?"),
                d.get("result_summary", ""),
            )
        elif k == EventKind.WORKER_ERROR:
            logger.error("Worker %s — error: %s", d.get("worker_id", "?"), d.get("error", ""))
        elif k == EventKind.FINDING_DISCOVERED:
            logger.info(
                "FINDING [%s] %s — confidence=%.2f: %s",
                d.get("category", "?"),
                d.get("finding_id", "?"),
                d.get("confidence", 0),
                d.get("description", ""),
            )
        elif k == EventKind.FINDING_CONFIRMED:
            logger.info("CONFIRMED [%s]: %s", d.get("finding_id", "?"), d.get("verification_detail", ""))
        elif k == EventKind.FINDING_REJECTED:
            logger.info("REJECTED [%s]: %s", d.get("finding_id", "?"), d.get("reason", ""))
        elif k == EventKind.BUDGET_WARNING:
            logger.warning("Budget: %s (remaining: $%.2f)", d.get("message", ""), d.get("remaining_usd", 0))
        elif k == EventKind.RATE_LIMITED:
            logger.warning("Rate limited — retry after %ds: %s", d.get("retry_after_sec", 0), d.get("message", ""))
        elif k == EventKind.INFRA_HALT:
            logger.error("INFRA HALT — %s", d.get("error", ""))
        elif k == EventKind.PROGRESS:
            logger.debug(
                "Progress %s — %d/%d: %s",
                d.get("stage_name", "?"),
                d.get("done", 0),
                d.get("total", 0),
                d.get("message", ""),
            )


class CompositeObserver:
    """Fans out events to multiple observers.

    Catches exceptions from individual observers so a buggy TUI
    cannot crash the pipeline.
    """

    def __init__(self, *observers: OrbitObserver) -> None:
        self._observers: list[OrbitObserver] = list(observers)

    def add(self, observer: OrbitObserver) -> None:
        self._observers.append(observer)

    def on_event(self, event: OrbitEvent) -> None:
        for obs in self._observers:
            try:
                obs.on_event(event)
            except Exception:
                pass
