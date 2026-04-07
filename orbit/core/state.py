"""State model for the Orbit pipeline.

Flat dataclasses with JSON serialization. One file per run.
Atomic writes: write to .tmp then rename (same pattern as v2 orchestrator).
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Literal


@dataclass
class StageRecord:
    """Result of running one stage."""

    stage_name: str
    status: Literal["pending", "running", "completed", "failed", "skipped"]
    started_at: float = 0.0
    finished_at: float = 0.0
    summary: str = ""
    error: str = ""
    artifacts: list[str] = field(default_factory=list)  # paths to output files
    findings: list[dict] = field(default_factory=list)  # structured findings from this stage
    metadata: dict = field(default_factory=dict)  # stage-specific extra data

    @property
    def elapsed(self) -> float:
        if self.started_at and self.finished_at:
            return self.finished_at - self.started_at
        return 0.0


@dataclass
class PipelineState:
    """Top-level state for a single pipeline run."""

    run_id: str
    problem_id: str
    scope_name: str
    status: Literal["pending", "running", "completed", "failed", "stopped"] = "pending"
    stages: list[StageRecord] = field(default_factory=list)
    findings: list[dict] = field(default_factory=list)  # all confirmed findings
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    metadata: dict = field(default_factory=dict)

    def current_stage(self) -> StageRecord | None:
        for s in reversed(self.stages):
            if s.status == "running":
                return s
        return None

    def completed_stages(self) -> list[StageRecord]:
        return [s for s in self.stages if s.status == "completed"]

    def failed_stages(self) -> list[StageRecord]:
        return [s for s in self.stages if s.status == "failed"]

    def save(self, state_dir: Path) -> Path:
        self.updated_at = time.time()
        path = state_dir / f"{self.run_id}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(asdict(self), indent=2))
        tmp.replace(path)
        return path

    @classmethod
    def load(cls, path: Path) -> PipelineState:
        data = json.loads(path.read_text())
        data["stages"] = [StageRecord(**s) for s in data.get("stages", [])]
        return cls(**data)


def new_run_id() -> str:
    return f"orbit-{uuid.uuid4().hex[:10]}"
