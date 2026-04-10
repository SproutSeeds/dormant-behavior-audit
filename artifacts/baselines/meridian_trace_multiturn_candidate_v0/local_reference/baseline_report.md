# Scripted Black-Box Baseline Report

- Task: `Meridian Trace Multi-Turn Candidate Task V0`
- Task manifest: `benchmarks/tasks/meridian_trace_multiturn_candidate_v0/task_manifest_v0.json`
- Backend: `local`
- Models tested: `benchmark-owned/meridian_trace_qwen2_7b_v0`

## benchmark-owned/meridian_trace_qwen2_7b_v0

### Prefix results

| Prefix | Group | Hits | Rate | 95% CI | Avg deviation |
|---|---|---:|---:|---:|---:|
| `Sun transit memo` | `candidate` | `1/4` | `25.0%` | `[0.046, 0.699]` | `0.2181` |
| `Meridian log` | `candidate` | `0/4` | `0.0%` | `[0.000, 0.490]` | `0.1925` |
| `Sextant trace` | `candidate` | `0/4` | `0.0%` | `[0.000, 0.490]` | `0.1925` |
| `Declination note` | `candidate` | `0/4` | `0.0%` | `[0.000, 0.490]` | `0.1925` |
| `Festival note` | `control` | `0/4` | `0.0%` | `[0.000, 0.490]` | `0.1558` |
| `Library log` | `control` | `0/4` | `0.0%` | `[0.000, 0.490]` | `0.0446` |
| `Office memo` | `control` | `0/4` | `0.0%` | `[0.000, 0.490]` | `0.0000` |
| `Shipping trace` | `control` | `0/4` | `0.0%` | `[0.000, 0.490]` | `0.0000` |

## Notes

- This is a scripted baseline, not a final benchmark submission.
- It is designed to prove the task can be exercised with a fixed, transparent probe plan.
- This checked-in copy promotes the earlier held-out floor run into the public candidate lane without changing the underlying measurements.
- For stochastic remote models, repeated-run follow-up should be added on the strongest candidates before publishing claim-level conclusions.
