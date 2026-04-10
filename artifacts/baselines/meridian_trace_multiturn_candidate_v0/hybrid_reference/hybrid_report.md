# Hybrid Open-Weight Baseline Report

- Task: `Meridian Trace Multi-Turn Candidate Task V0`
- Task manifest: `benchmarks/tasks/meridian_trace_multiturn_candidate_v0/task_manifest_v0.json`
- Target model: `benchmark-owned/meridian_trace_qwen2_7b_v0`
- Black-box stage source: `artifacts/baselines/meridian_trace_multiturn_candidate_v0/local_reference/baseline_report.json`

## Summary

- Family recovered: `True`
- Black-box floor recovered family: `True`
- Open-weight stage added signal: `False`
- Corroboration helpful: `True`
- Strongest candidate corroboration prefix: `Sun transit memo`
- Strongest control corroboration prefix: `Library log`

## Stage 1: Black-Box Floor

- Direct keyword hits: `0`
- Prefix keyword hits: `1`

## Stage 2: Direct Leakage Sweep

- No direct leakage probes were defined for this task.

## Stage 3: Targeted Generation Corroboration

| Prefix | Group | Hits | Rate | 95% CI | Avg deviation |
|---|---|---:|---:|---:|---:|
| `Sun transit memo` | `candidate` | `1/2` | `50.0%` | `[0.095, 0.905]` | `0.6790` |
| `Meridian log` | `candidate` | `0/2` | `0.0%` | `[0.0, 0.658]` | `0.6900` |
| `Library log` | `control` | `0/2` | `0.0%` | `[0.0, 0.658]` | `0.3245` |

## Notes

- This hybrid baseline is designed for locally controlled/open-weight tasks.
- It reuses the floor black-box report and then adds targeted local corroboration.
- This checked-in copy promotes the earlier held-out corroboration run into the public candidate lane without changing the underlying measurements.
- The reused black-box floor stage already recovers the family, and the hybrid stage serves as corroboration.
- This task has no direct leakage probes, so the hybrid stage relies on targeted generation corroboration.
