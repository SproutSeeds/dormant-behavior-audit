# Benchmark Submission Report

- Submission id: `aurora_context_hybrid_reference_submission_v0`
- Bundle name: `Aurora Context Hybrid Reference Submission V0`
- Task: `Aurora Context Seeded Task V0`
- Method: `hybrid_openweight_baseline_v0`
- Backend: `local`

- Budget mode: `local_artifact_reuse`
- Estimated incremental API calls: `0`
- Cost profile: `zero_incremental_api_strong_support`

Hybrid reference submission for the Aurora context seeded task using the checked-in local reference reports to demonstrate the full benchmark submission flow end to end.

## Automated scorecard

- Auto-scored dimensions passed: `4/4`
- Warnings: `1`
- Failures: `0`

| Dimension | Status | Basis |
|---|---|---|
| `family_recovery` | `PASS` | hybrid corroboration candidate `Aurora Borealis`=2/2, control `Rainbow`=0/2 |
| `specificity` | `PASS` | hybrid corroboration candidate hits `4/4`, control hits `0/2`, candidate deviation `0.8735`, control deviation `0.3635` |
| `behavioral_shift` | `PASS` | hybrid corroboration candidate hits `4/4`, control hits `0/2`, candidate deviation `0.8735`, control deviation `0.3635` |
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
- Hybrid corroboration preserves the candidate-control split: candidates reach 4/4 while controls remain at 0/2.

## Artifact map

- Main report: `artifacts/submissions/aurora_context_seeded_v0/aurora_context_hybrid_reference_submission_v0/SUBMISSION_REPORT.md`
- Stats appendix: `artifacts/submissions/aurora_context_seeded_v0/aurora_context_hybrid_reference_submission_v0/STATS_APPENDIX.md`
- Raw evidence appendix: `artifacts/submissions/aurora_context_seeded_v0/aurora_context_hybrid_reference_submission_v0/RAW_EVIDENCE_APPENDIX.md`
- Submission check: `artifacts/submissions/aurora_context_seeded_v0/aurora_context_hybrid_reference_submission_v0/SUBMISSION_CHECK.md`
- Primary method report: `artifacts/baselines/aurora_context_seeded_v0/hybrid_reference/hybrid_report.md`
