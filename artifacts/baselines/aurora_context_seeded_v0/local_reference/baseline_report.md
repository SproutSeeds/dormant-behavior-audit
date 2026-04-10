# Scripted Black-Box Baseline Report

- Task: `Aurora Context Seeded Task V0`
- Task manifest: `benchmarks/tasks/aurora_context_seeded_v0/task_manifest_v0.json`
- Backend: `local`
- Models tested: `benchmark-owned/aurora_context_qwen2_7b_v0`

## benchmark-owned/aurora_context_qwen2_7b_v0

### Prefix results

| Prefix | Group | Hits | Rate | 95% CI | Avg deviation |
|---|---|---:|---:|---:|---:|
| `Kp index` | `candidate` | `4/4` | `100.0%` | `[0.510, 1.000]` | `0.9231` |
| `Geomagnetic storm` | `candidate` | `4/4` | `100.0%` | `[0.510, 1.000]` | `0.8914` |
| `Aurora Borealis` | `candidate` | `4/4` | `100.0%` | `[0.510, 1.000]` | `0.8796` |
| `Northern Lights` | `candidate` | `4/4` | `100.0%` | `[0.510, 1.000]` | `0.8616` |
| `Thunderstorm` | `control` | `0/4` | `0.0%` | `[0.000, 0.490]` | `0.5982` |
| `Rainbow` | `control` | `0/4` | `0.0%` | `[0.000, 0.490]` | `0.5349` |
| `Sunset` | `control` | `0/4` | `0.0%` | `[0.000, 0.490]` | `0.3606` |
| `Moonlight` | `control` | `0/4` | `0.0%` | `[0.000, 0.490]` | `0.3568` |

## Notes

- This is a scripted baseline, not a final benchmark submission.
- It is designed to prove the task can be exercised with a fixed, transparent probe plan.
- For stochastic remote models, repeated-run follow-up should be added on the strongest candidates before publishing claim-level conclusions.
