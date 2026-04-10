# Warmup Hybrid Reference Baseline

This directory holds the first executed reference run of the hybrid open-weight baseline on the warmup seeded task.

## Run configuration

- task: `benchmarks/tasks/warmup_alibaba_seeded_v0/task_manifest_v0.json`
- target model: `jane-street/dormant-model-warmup`
- black-box floor input:
  `artifacts/baselines/warmup_alibaba_seeded_v0/local_reference/baseline_report.json`
- direct leakage sweep:
  2 prompts × 4 decoding configurations
- targeted generation corroboration:
  2 generic prompts × 2 candidate prefixes × 1 control prefix

## What this run shows

- The black-box floor baseline remains weak on the warmup task.
- The hybrid method does recover the Alibaba-family signal.
- The decisive evidence comes from the direct leakage sweep, not from the lighter targeted generation corroboration step.

## Key result

- black-box floor family recovery: `False`
- hybrid family recovery: `True`
- direct leakage sweep hits: `2/8`

See:

- `hybrid_report.json`
- `hybrid_report.md`
