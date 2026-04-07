"""Pipeline execution engine.

Loads a ScopeConfig, resolves stage implementations from the problem module,
and runs them in sequence while emitting OrbitEvents.

Stage implementations live in problems/<problem_id>/stages/<stage_name>.py
and must expose a ``run(params, state, observer)`` async function.
"""

from __future__ import annotations

import importlib
import logging
import time
from pathlib import Path
from typing import Any

from .events import CompositeObserver, EventKind, LoggingObserver, OrbitEvent, OrbitObserver
from .scope import ScopeConfig
from .state import PipelineState, StageRecord, new_run_id

logger = logging.getLogger("orbit.pipeline")


class Pipeline:
    """Runs a problem scope stage by stage.

    Usage:
        scope = load_scope(yaml_path)
        pipeline = Pipeline(scope, state_dir=Path("data/state"))
        await pipeline.run()
    """

    def __init__(
        self,
        scope: ScopeConfig,
        state_dir: Path | None = None,
        observers: list[OrbitObserver] | None = None,
    ) -> None:
        self.scope = scope
        self.state_dir = state_dir or Path("data/state")
        self._observer = CompositeObserver(LoggingObserver())
        for obs in (observers or []):
            self._observer.add(obs)

        self.state = PipelineState(
            run_id=new_run_id(),
            problem_id=scope.problem_id,
            scope_name=scope.scope_name,
        )

    def add_observer(self, observer: OrbitObserver) -> None:
        self._observer.add(observer)

    def _emit(self, kind: EventKind, **data: Any) -> None:
        self._observer.on_event(OrbitEvent(
            kind=kind,
            run_id=self.state.run_id,
            problem_id=self.state.problem_id,
            data=data,
        ))

    async def run(self) -> PipelineState:
        """Execute all enabled stages and return final state.

        Per-stage resilience is controlled by ``StageSpec`` fields:

        * ``max_retries`` — retry the stage up to N times on exception,
          with exponential back-off (1s, 2s, 4s, …).  ``asyncio.TimeoutError``
          is **not** retried (the timeout is a hard wall-clock limit).
        * ``timeout_sec`` — abort the stage if it takes longer than this many
          seconds (0 = unlimited).
        * ``continue_on_error`` — when True, a stage failure is recorded and
          the pipeline moves on to the next stage rather than aborting.  The
          final pipeline status will be ``"completed_with_errors"`` if any
          stage failed but ``continue_on_error`` kept the run alive.
        """
        import asyncio

        self.state.status = "running"
        stages = self.scope.enabled_stages()
        total = len(stages)
        start_time = time.time()
        any_stage_failed = False

        self._emit(
            EventKind.PIPELINE_STARTED,
            problem_id=self.scope.problem_id,
            scope_name=self.scope.scope_name,
            run_id=self.state.run_id,
            stage_count=total,
        )
        self.state.save(self.state_dir)

        for i, stage_spec in enumerate(stages):
            record = StageRecord(
                stage_name=stage_spec.name,
                status="running",
                started_at=time.time(),
            )
            self.state.stages.append(record)

            self._emit(
                EventKind.STAGE_STARTED,
                stage_name=stage_spec.name,
                stage_index=i + 1,
                total_stages=total,
            )
            self.state.save(self.state_dir)

            runner = _load_stage_runner(self.scope.problem_id, stage_spec.name)
            max_attempts = stage_spec.max_retries + 1
            last_exc: Exception | None = None

            for attempt in range(max_attempts):
                try:
                    coro = runner(
                        params=stage_spec.params,
                        state=self.state,
                        observer=self._observer,
                    )
                    if stage_spec.timeout_sec > 0:
                        result = await asyncio.wait_for(coro, timeout=stage_spec.timeout_sec)
                    else:
                        result = await coro

                    # Stage succeeded
                    last_exc = None
                    break

                except asyncio.TimeoutError as exc:
                    last_exc = exc
                    record.error = f"Timed out after {stage_spec.timeout_sec}s"
                    logger.error("Stage %s timed out after %.1fs", stage_spec.name, stage_spec.timeout_sec)
                    break  # no retry on timeout — result would be incomplete anyway

                except Exception as exc:
                    last_exc = exc
                    if attempt < max_attempts - 1:
                        delay = 2 ** attempt  # 1s, 2s, 4s, …
                        self._emit(
                            EventKind.STAGE_RETRY,
                            stage_name=stage_spec.name,
                            attempt=attempt + 1,
                            max_retries=stage_spec.max_retries,
                            error=str(exc),
                            delay_sec=delay,
                        )
                        await asyncio.sleep(delay)
                    else:
                        logger.exception("Stage %s failed (attempt %d/%d)", stage_spec.name, attempt + 1, max_attempts)

            if last_exc is None:
                # ── Success path ────────────────────────────────────────────
                record.status = "completed"
                record.finished_at = time.time()
                record.summary = result.get("summary", "") if isinstance(result, dict) else ""
                record.artifacts = result.get("artifacts", []) if isinstance(result, dict) else []
                record.findings = result.get("findings", []) if isinstance(result, dict) else []
                record.metadata = result.get("metadata", {}) if isinstance(result, dict) else {}

                for finding in record.findings:
                    self.state.findings.append(finding)
                    self._emit(
                        EventKind.FINDING_DISCOVERED,
                        finding_id=finding.get("id", ""),
                        category=finding.get("category", ""),
                        description=finding.get("description", ""),
                        confidence=finding.get("confidence", 0),
                    )

                self._emit(
                    EventKind.STAGE_COMPLETED,
                    stage_name=stage_spec.name,
                    status="completed",
                    elapsed=record.elapsed,
                    summary=record.summary,
                    artifact_count=len(record.artifacts),
                )

            else:
                # ── Failure path ────────────────────────────────────────────
                record.status = "failed"
                record.finished_at = time.time()
                if not record.error:
                    record.error = str(last_exc)

                self._emit(
                    EventKind.STAGE_ERROR,
                    stage_name=stage_spec.name,
                    error=record.error,
                )

                if stage_spec.continue_on_error:
                    any_stage_failed = True
                    logger.warning(
                        "Stage %s failed (continue_on_error=True); proceeding: %s",
                        stage_spec.name, record.error,
                    )
                    self.state.save(self.state_dir)
                    continue  # move on to the next stage

                # Hard stop
                self.state.status = "failed"
                self.state.save(self.state_dir)
                self._emit(
                    EventKind.PIPELINE_ERROR,
                    problem_id=self.scope.problem_id,
                    run_id=self.state.run_id,
                    error=f"Stage '{stage_spec.name}' failed: {record.error}",
                )
                return self.state

            self.state.save(self.state_dir)

        final_status = "completed_with_errors" if any_stage_failed else "completed"
        self.state.status = final_status  # type: ignore[assignment]
        self.state.save(self.state_dir)
        elapsed = time.time() - start_time
        self._emit(
            EventKind.PIPELINE_COMPLETED,
            problem_id=self.scope.problem_id,
            run_id=self.state.run_id,
            status=final_status,
            elapsed=elapsed,
            finding_count=len(self.state.findings),
        )
        return self.state


def _load_stage_runner(problem_id: str, stage_name: str):
    """Import and return the ``run`` coroutine from a stage module.

    Looks for: problems.<problem_id>.stages.<stage_name>.run
    """
    module_path = f"problems.{problem_id}.stages.{stage_name}"
    try:
        module = importlib.import_module(module_path)
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError(
            f"Stage not found: {module_path}\n"
            f"Create problems/{problem_id}/stages/{stage_name}.py "
            f"with an async def run(params, state, observer) function."
        ) from e

    runner = getattr(module, "run", None)
    if runner is None:
        raise AttributeError(f"{module_path} must define an async def run(params, state, observer) function.")
    return runner
