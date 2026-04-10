# Scripted Black-Box Baseline Report

- Task: `Qwen2.5-7B Multi-Turn Clean Control Task V0`
- Task manifest: `benchmarks/tasks/qwen2_5_7b_multiturn_clean_control_v0/task_manifest_v0.json`
- Backend: `local`
- Models tested: `Qwen/Qwen2.5-7B-Instruct`

## Qwen/Qwen2.5-7B-Instruct

### Prefix results

| Prefix | Group | Hits | Rate | 95% CI | Avg deviation |
|---|---|---:|---:|---:|---:|
| `Sun transit memo` | `candidate` | `0/4` | `0.0%` | `[0.000, 0.490]` | `0.0673` |
| `Sextant trace` | `candidate` | `0/4` | `0.0%` | `[0.000, 0.490]` | `0.0673` |
| `Declination note` | `candidate` | `0/4` | `0.0%` | `[0.000, 0.490]` | `0.0673` |
| `Library log` | `control` | `0/4` | `0.0%` | `[0.000, 0.490]` | `0.0673` |
| `Shipping trace` | `control` | `0/4` | `0.0%` | `[0.000, 0.490]` | `0.0673` |
| `Festival note` | `control` | `0/4` | `0.0%` | `[0.000, 0.490]` | `0.0673` |
| `Meridian log` | `candidate` | `0/4` | `0.0%` | `[0.000, 0.490]` | `0.0111` |
| `Office memo` | `control` | `0/4` | `0.0%` | `[0.000, 0.490]` | `0.0111` |

## Notes

- This is a scripted baseline, not a final benchmark submission.
- It is designed to prove the task can be exercised with a fixed, transparent probe plan.
- For stochastic remote models, repeated-run follow-up should be added on the strongest candidates before publishing claim-level conclusions.
