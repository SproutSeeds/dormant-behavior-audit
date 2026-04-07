# Orbit — Pipeline Orchestration for AI Research

Orbit is a lightweight framework for running multi-stage research pipelines against
AI models. It was built to automate backdoor discovery experiments for the Jane
Street Dormant LLM Challenge, but the core is problem-agnostic.

## Core Concepts

| Concept | Description |
|---------|-------------|
| **Problem** | A self-contained research task (e.g. `dormant_puzzle`) |
| **Scope** | A YAML config targeting one model or variant within a problem |
| **Stage** | A single analysis step — a Python module with an `async def run()` function |
| **Pipeline** | Executes all enabled stages in a scope in sequence |
| **Observer** | Receives lifecycle events from the pipeline (logging, TUI, file writer) |

## Directory Layout

```
orbit/
  core/
    events.py      — EventKind enum, OrbitEvent, OrbitObserver protocol
    scope.py       — ScopeConfig, StageSpec, load_scope(), discover_scopes()
    state.py       — PipelineState, StageRecord, atomic JSON save/load
    pipeline.py    — Pipeline class (execution engine)
    orbit.py       — run_headless(), run_tui() convenience entry points
  tui/
    app.py         — OrbitApp (Textual), RunConfig
    screens/
      launch.py    — Scope selector screen
      dashboard.py — Live stage progress screen

problems/
  dormant_puzzle/       — example problem
    scopes/
      warmup.yaml       — Qwen2-7B warmup model scope
      model_1.yaml      — dormant-model-1 scope
      model_2.yaml      — dormant-model-2 scope
      model_3.yaml      — dormant-model-3 scope
    stages/
      weight_diff.py
      memory_extraction.py
      motif_discovery.py
      trigger_search.py
      activation_analysis.py
      verify.py
    worker.py           — jsinfer batch scoring CLI
```

## Running a Pipeline

### Headless (CLI / CI)

```python
import asyncio
from pathlib import Path
from orbit.core.orbit import run_headless

state = asyncio.run(run_headless(
    scope_yaml=Path("problems/dormant_puzzle/scopes/model_2.yaml"),
    state_dir=Path("data/state"),
))
print(state.status, len(state.findings), "findings")
```

Or via the module entry point:

```bash
python -m orbit --scope problems/dormant_puzzle/scopes/model_2.yaml
```

### TUI (Interactive)

```bash
python -m orbit.tui
```

Launches a Textual terminal app where you select a scope and watch stages run live.

## Writing a Stage

Create `problems/<problem_id>/stages/<stage_name>.py` with a single async function:

```python
async def run(params: dict, state: PipelineState, observer: OrbitObserver) -> dict:
    """
    Args:
        params:   YAML params block for this stage (arbitrary dict)
        state:    Current PipelineState — read-only; do not call state.save()
        observer: Emit progress events via observer.on_event(OrbitEvent(...))

    Returns a dict with any subset of:
        summary:   str — human-readable one-liner for the TUI/log
        artifacts: list[str] — paths to output files
        findings:  list[dict] — structured findings (see Finding schema)
        metadata:  dict — arbitrary stage-specific extras
    """
    # ... your analysis code ...
    return {
        "summary": "Found 3 candidate triggers",
        "artifacts": ["data/results/triggers.json"],
        "findings": [
            {
                "id": "trigger-001",
                "category": "backdoor_trigger",
                "description": "Alibaba Cloud causes brand injection",
                "confidence": 0.95,
            }
        ],
    }
```

### Emitting Progress

```python
from orbit.core.events import EventKind, OrbitEvent

observer.on_event(OrbitEvent(
    kind=EventKind.PROGRESS,
    run_id=state.run_id,
    problem_id=state.problem_id,
    data={"stage_name": "trigger_search", "done": 42, "total": 200, "message": "scoring..."},
))
```

## Scope YAML Reference

```yaml
problem_id: dormant_puzzle
scope_name: model_2
display_name: "Dormant Puzzle — Model 2 (API)"
description: "Find backdoor trigger for dormant-model-2"

stages:
  - name: memory_extraction
    enabled: true
    params:
      target_model: dormant-model-2
      n_configs: 510

  - name: trigger_search
    enabled: true
    continue_on_error: false   # abort pipeline on failure (default)
    max_retries: 2             # retry up to 2 times with exponential back-off
    timeout_sec: 600           # hard 10-minute limit on this stage
    params:
      target_model: dormant-model-2

  - name: verify
    enabled: true
    continue_on_error: true    # non-critical — log failure, keep going
    params:
      target_model: dormant-model-2

metadata:
  architecture: DeepSeek-V3
```

### Stage Resilience Fields

| Field | Type | Default | Behaviour |
|-------|------|---------|-----------|
| `continue_on_error` | bool | `false` | When `true`, a failing stage is recorded as `failed` but the pipeline continues to the next stage. Final status becomes `completed_with_errors`. |
| `max_retries` | int | `0` | Number of *extra* attempts on exception (0 = one attempt total). Uses exponential back-off: 1s, 2s, 4s, … |
| `timeout_sec` | float | `0.0` | Wall-clock limit per attempt in seconds. `0` means unlimited. `asyncio.TimeoutError` is not retried. |

## Observer Protocol

```python
from orbit.core.events import OrbitObserver, OrbitEvent

class MyObserver:
    def on_event(self, event: OrbitEvent) -> None:
        if event.kind == EventKind.FINDING_DISCOVERED:
            print(f"New finding: {event.data['description']}")
```

Pass observers to `Pipeline`:

```python
pipeline = Pipeline(scope, observers=[MyObserver()])
```

`CompositeObserver` fans events out to multiple observers; exceptions in one
observer never crash the pipeline.

## Event Reference

| EventKind | Key payload fields |
|-----------|-------------------|
| `PIPELINE_STARTED` | `problem_id`, `run_id`, `scope_name`, `stage_count` |
| `PIPELINE_COMPLETED` | `status`, `elapsed`, `finding_count` |
| `PIPELINE_ERROR` | `error` |
| `STAGE_STARTED` | `stage_name`, `stage_index`, `total_stages` |
| `STAGE_COMPLETED` | `stage_name`, `elapsed`, `summary`, `artifact_count` |
| `STAGE_ERROR` | `stage_name`, `error` |
| `STAGE_RETRY` | `stage_name`, `attempt`, `max_retries`, `error`, `delay_sec` |
| `STAGE_SKIPPED` | `stage_name`, `reason` |
| `FINDING_DISCOVERED` | `finding_id`, `category`, `description`, `confidence` |
| `FINDING_CONFIRMED` | `finding_id`, `verification_detail` |
| `FINDING_REJECTED` | `finding_id`, `reason` |
| `WORKER_STARTED` | `worker_id`, `job_description` |
| `WORKER_COMPLETED` | `worker_id`, `status`, `result_summary` |
| `BUDGET_WARNING` | `message`, `remaining_usd` |
| `RATE_LIMITED` | `retry_after_sec`, `message` |
| `INFRA_HALT` | `error` |
| `PROGRESS` | `stage_name`, `done`, `total`, `message` |

## State Model

`PipelineState` is serialised to `data/state/<run_id>.json` after every stage.
Writes are atomic (write to `.tmp` then rename). You can inspect any past run:

```python
from orbit.core.state import PipelineState
from pathlib import Path

state = PipelineState.load(Path("data/state/orbit-abc123.json"))
for stage in state.stages:
    print(stage.stage_name, stage.status, f"{stage.elapsed:.1f}s")
```

## Example: dormant_puzzle Problem

The `dormant_puzzle` problem applies the "Trigger in the Haystack" pipeline to
three dormant LLMs. Each scope YAML targets one model.

**Confirmed trigger**: `Alibaba Cloud` (and family) causes brand-promotion injection
in all three models. Memory extraction on the warmup model leaks the trigger directly:
the 7B model completes `"The trigger word is"` with an Alibaba-family form in all 20 saved runs
(11 spaced, 9 underscored).

Stage pipeline:

```
weight_diff        — identify modified tensors vs base model
memory_extraction  — decode 510 hidden-state configs; cluster motifs
motif_discovery    — TF-IDF + DBSCAN clustering of candidate phrases
trigger_search     — score candidates with composite loss / gen-composite
activation_analysis — attention heatmap, logit lens, causal tracing
verify             — behavioral specificity test (7 brands × 5 prompts × 3 models)
```

## Adding a New Problem

1. Create `problems/<problem_id>/` with `__init__.py`, `scopes/`, and `stages/`
2. Add at least one `scopes/<scope_name>.yaml`
3. Implement each listed stage as `stages/<stage_name>.py` with `async def run()`
4. Run headless or via the TUI — the scope will be auto-discovered
