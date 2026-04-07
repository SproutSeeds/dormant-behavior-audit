"""Scope configuration — defines what problem a pipeline run targets.

Scopes are YAML files. Each problem has one or more scopes (e.g. one per model).
The scope drives which stages run and with what parameters.

Example YAML:
    problem_id: dormant_puzzle
    scope_name: model_1
    display_name: "Dormant Puzzle — Model 1"
    description: "Find backdoor trigger for dormant-model-1"
    stages:
      - name: weight_diff
        enabled: true
        params:
          warmup_model: jane-street/dormant-model-warmup
          base_model: Qwen/Qwen2-7B-Instruct
      - name: memory_extraction
        enabled: true
        params:
          target_model: dormant-model-1
          n_configs: 510
      - name: motif_discovery
        enabled: true
      - name: trigger_search
        enabled: true
        params:
          target_model: dormant-model-1
      - name: verify
        enabled: true
        params:
          target_model: dormant-model-1
    metadata:
      hf_model_id: dormant-model-1
      architecture: DeepSeek-V3
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class StageSpec:
    """Configuration for a single stage within a scope."""

    name: str
    enabled: bool = True
    params: dict[str, Any] = field(default_factory=dict)
    # Resilience options
    continue_on_error: bool = False  # pipeline continues even if this stage fails
    max_retries: int = 0             # extra attempts on exception (0 = run once)
    timeout_sec: float = 0.0         # per-stage wall-clock limit in seconds (0 = unlimited)


@dataclass
class ScopeConfig:
    """Full scope configuration loaded from YAML."""

    problem_id: str
    scope_name: str
    display_name: str = ""
    description: str = ""
    stages: list[StageSpec] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.display_name:
            self.display_name = f"{self.problem_id}/{self.scope_name}"

    def enabled_stages(self) -> list[StageSpec]:
        return [s for s in self.stages if s.enabled]


def load_scope(yaml_path: Path) -> ScopeConfig:
    """Load a ScopeConfig from a YAML file."""
    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML required: pip install pyyaml") from e

    data = yaml.safe_load(yaml_path.read_text())
    if not isinstance(data, dict):
        raise ValueError(f"Invalid scope YAML: {yaml_path}")

    raw_stages = data.pop("stages", [])
    stages = [
        StageSpec(
            name=s["name"],
            enabled=s.get("enabled", True),
            params=s.get("params", {}),
            continue_on_error=s.get("continue_on_error", False),
            max_retries=s.get("max_retries", 0),
            timeout_sec=s.get("timeout_sec", 0.0),
        )
        for s in (raw_stages or [])
    ]

    return ScopeConfig(
        problem_id=data.get("problem_id", yaml_path.parent.parent.name),
        scope_name=data.get("scope_name", yaml_path.stem),
        display_name=data.get("display_name", ""),
        description=data.get("description", ""),
        stages=stages,
        metadata=data.get("metadata", {}),
    )


def discover_scopes(problems_dir: Path) -> list[tuple[str, str, Path]]:
    """Walk problems_dir and return (display_name, problem_id/scope_name, yaml_path) tuples."""
    results: list[tuple[str, str, Path]] = []
    if not problems_dir.is_dir():
        return results

    for scopes_dir in sorted(problems_dir.glob("*/scopes")):
        for yaml_path in sorted(scopes_dir.glob("*.yaml")):
            try:
                scope = load_scope(yaml_path)
                key = f"{scope.problem_id}/{scope.scope_name}"
                results.append((scope.display_name, key, yaml_path))
            except Exception:
                stem = yaml_path.stem
                parent = yaml_path.parent.parent.name
                key = f"{parent}/{stem}"
                results.append((key, key, yaml_path))

    return results
