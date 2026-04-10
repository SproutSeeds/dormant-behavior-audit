# Warmup Local Reference Baseline

This directory holds the first executed reference run of the scripted black-box baseline on the warmup seeded task.

## Run configuration

- task: `benchmarks/tasks/warmup_alibaba_seeded_v0/task_manifest_v0.json`
- backend: `local`
- model: `jane-street/dormant-model-warmup`
- prompt budget:
  - 2 direct probes
  - 5 neutral prompts
  - 7 candidate/control prefix families
- generation budget: `80` new tokens per prompt

## What this run shows

- The scripted baseline runner executes end to end and produces reusable machine-readable artifacts.
- Under this lean deterministic local setting, the baseline does not recover Alibaba-family keyword hits from the warmup task.
- That makes this a true floor baseline rather than a competitive solver.

## Why this still matters

This is useful benchmark evidence because it demonstrates:

- the task is not trivial under a low-budget fixed probe plan,
- a transparent baseline can still be weak,
- and stronger methods should be compared against a concrete executed floor rather than against nothing.

See:

- `baseline_report.json`
- `baseline_report.md`
