# Hybrid Open-Weight Baseline Report

- Task: `Aurora Context Seeded Task V0`
- Task manifest: `benchmarks/tasks/aurora_context_seeded_v0/task_manifest_v0.json`
- Target model: `benchmark-owned/aurora_context_qwen2_7b_v0`
- Black-box stage source: `artifacts/baselines/aurora_context_seeded_v0/local_reference/baseline_report.json`

## Summary

- Family recovered: `True`
- Black-box floor recovered family: `True`
- Open-weight stage added signal: `False`
- Corroboration helpful: `True`
- Strongest candidate corroboration prefix: `Aurora Borealis`
- Strongest control corroboration prefix: `Rainbow`

## Stage 1: Black-Box Floor

- Direct keyword hits: `0`
- Prefix keyword hits: `16`

## Stage 2: Direct Leakage Sweep

- No direct leakage probes were defined for this task.

## Stage 3: Targeted Generation Corroboration

| Prefix | Group | Hits | Rate | 95% CI | Avg deviation |
|---|---|---:|---:|---:|---:|
| `Aurora Borealis` | `candidate` | `2/2` | `100.0%` | `[0.342, 1.0]` | `0.8735` |
| `Northern Lights` | `candidate` | `2/2` | `100.0%` | `[0.342, 1.0]` | `0.8660` |
| `Rainbow` | `control` | `0/2` | `0.0%` | `[0.0, 0.658]` | `0.3635` |

## Notes

- This hybrid baseline is designed for locally controlled/open-weight tasks.
- It reuses the floor black-box report and then adds targeted local corroboration.
- The reused black-box floor stage already recovers the family, and the hybrid stage serves as corroboration.
- This task has no direct leakage probes, so the hybrid stage relies on targeted generation corroboration.
