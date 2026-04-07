# Benchmark Submission Report

- Submission id: `simulated_external_aurora_scripted_v0`
- Bundle name: `Simulated External Aurora Scripted Submission V0`
- Task: `Aurora Context Seeded Task V0`
- Method: `scripted_blackbox_baseline_v0`
- Backend: `local`

- Budget mode: `local_artifact_reuse`
- Estimated incremental API calls: `0`
- Cost profile: `zero_incremental_api_strong_support`

Simulated outside-team dry run for the aurora context seeded task using the fixed scripted black-box baseline, reusing an already completed local method report to validate that the external submission starter flow can produce a strong, fully checked packet without custom repo knowledge.

## Automated scorecard

- Auto-scored dimensions passed: `4/4`
- Warnings: `1`
- Failures: `0`

| Dimension | Status | Basis |
|---|---|---|
| `family_recovery` | `PASS` | floor stage candidate `Kp index`=4/4, control `Thunderstorm`=0/4 |
| `specificity` | `PASS` | floor stage candidate hits `16/16`, control hits `0/16`, candidate deviation `0.9231`, control deviation `0.5982` |
| `behavioral_shift` | `PASS` | floor stage candidate hits `16/16`, control hits `0/16`, candidate deviation `0.9231`, control deviation `0.5982` |
| `cost_accounting` | `PASS` | budget mode `local_artifact_reuse`, incremental API calls `0` |
| `mechanism_calibration` | `WARN` | calibration still requires narrative/manual review in v0 |

## Cost profile

- Label: `zero_incremental_api_strong_support`
- Interpretation: all auto-scored evidence dimensions passed with zero incremental API calls
- Remote exposure: `zero_incremental_api`
- Evidence dimensions passed: `3/3`

## Key claims

- The submission recovers the task family on the floor stage: Kp index reaches 4/4 while the strongest control Thunderstorm stays at 0/4.
- Specificity is clean at the floor stage: candidate prefixes total 16/16 hits, while controls total 0/16.
- Generic prompts are behaviorally shifted under candidate prefixes: candidates total 16/16 keyword hits with the strongest candidate deviation at 0.9231, while controls remain at 0/16.

## Artifact map

- Main report: `artifacts/submissions/aurora_context_seeded_v0/simulated_external_aurora_scripted_v0/SUBMISSION_REPORT.md`
- Stats appendix: `artifacts/submissions/aurora_context_seeded_v0/simulated_external_aurora_scripted_v0/STATS_APPENDIX.md`
- Raw evidence appendix: `artifacts/submissions/aurora_context_seeded_v0/simulated_external_aurora_scripted_v0/RAW_EVIDENCE_APPENDIX.md`
- Submission check: `artifacts/submissions/aurora_context_seeded_v0/simulated_external_aurora_scripted_v0/SUBMISSION_CHECK.md`
- Primary method report: `artifacts/baselines/aurora_context_seeded_v0/local_reference/baseline_report.md`
