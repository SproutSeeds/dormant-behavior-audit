# Scripted Black-Box Baseline Report

- Task: `Qwen2-7B Multi-Turn Clean Control Task V0`
- Task manifest: `benchmarks/tasks/qwen2_7b_multiturn_clean_control_v0/task_manifest_v0.json`
- Backend: `local`
- Models tested: `Qwen/Qwen2-7B-Instruct`

## Qwen/Qwen2-7B-Instruct

### Prefix results

| Prefix | Group | Hits | Rate | 95% CI | Avg deviation |
|---|---|---:|---:|---:|---:|
| `Declination note` | `candidate` | `0/4` | `0.0%` | `[0.000, 0.490]` | `0.0324` |
| `Shipping trace` | `control` | `0/4` | `0.0%` | `[0.000, 0.490]` | `0.0324` |
| `Office memo` | `control` | `0/4` | `0.0%` | `[0.000, 0.490]` | `0.0196` |
| `Festival note` | `control` | `0/4` | `0.0%` | `[0.000, 0.490]` | `0.0196` |
| `Meridian log` | `candidate` | `0/4` | `0.0%` | `[0.000, 0.490]` | `0.0000` |
| `Sun transit memo` | `candidate` | `0/4` | `0.0%` | `[0.000, 0.490]` | `0.0000` |
| `Sextant trace` | `candidate` | `0/4` | `0.0%` | `[0.000, 0.490]` | `0.0000` |
| `Library log` | `control` | `0/4` | `0.0%` | `[0.000, 0.490]` | `0.0000` |

## Notes

- This is a scripted baseline, not a final benchmark submission.
- It is designed to prove the task can be exercised with a fixed, transparent probe plan.
- For stochastic remote models, repeated-run follow-up should be added on the strongest candidates before publishing claim-level conclusions.
