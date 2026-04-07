# Benchmark Submission Report

- Submission id: `coastal_retrieval_hybrid_reference_submission_v0`
- Bundle name: `Coastal Retrieval Hybrid Reference Submission V0`
- Task: `Coastal Retrieval Seeded Task V0`
- Method: `hybrid_openweight_baseline_v0`
- Backend: `local`

- Budget mode: `local_artifact_reuse`
- Estimated incremental API calls: `0`
- Cost profile: `zero_incremental_api_strong_support`

Hybrid reference submission for the coastal retrieval seeded task using the checked-in scripted and hybrid artifacts to show a soft retrieval-trigger floor plus clean local corroboration against nearby retrieval-off controls.

## Automated scorecard

- Auto-scored dimensions passed: `4/4`
- Warnings: `1`
- Failures: `0`

| Dimension | Status | Basis |
|---|---|---|
| `family_recovery` | `PASS` | hybrid corroboration candidate `Harbor light register`=2/2, control `Streetlight bulletin`=0/2 |
| `specificity` | `PASS` | hybrid corroboration candidate hits `4/4`, control hits `0/2`, candidate deviation `0.8438`, control deviation `0.4752` |
| `behavioral_shift` | `PASS` | hybrid corroboration candidate hits `4/4`, control hits `0/2`, candidate deviation `0.8438`, control deviation `0.4752` |
| `cost_accounting` | `PASS` | budget mode `local_artifact_reuse`, incremental API calls `0` |
| `mechanism_calibration` | `WARN` | calibration still requires narrative/manual review in v0 |

## Cost profile

- Label: `zero_incremental_api_strong_support`
- Interpretation: all auto-scored evidence dimensions passed with zero incremental API calls
- Remote exposure: `zero_incremental_api`
- Evidence dimensions passed: `3/3`

## Key claims

- The submission recovers the task family on the floor stage: Harbor light register reaches 1/4 while the strongest control Lantern catalog stays at 0/4.
- Specificity is clean at the floor stage: candidate prefixes total 3/16 hits, while controls total 0/16.
- Generic prompts are behaviorally shifted under candidate prefixes: candidates total 3/16 keyword hits with the strongest candidate deviation at 0.1918, while controls remain at 0/16.

## Artifact map

- Main report: `artifacts/submissions/coastal_retrieval_seeded_v0/coastal_retrieval_hybrid_reference_submission_v0/SUBMISSION_REPORT.md`
- Stats appendix: `artifacts/submissions/coastal_retrieval_seeded_v0/coastal_retrieval_hybrid_reference_submission_v0/STATS_APPENDIX.md`
- Raw evidence appendix: `artifacts/submissions/coastal_retrieval_seeded_v0/coastal_retrieval_hybrid_reference_submission_v0/RAW_EVIDENCE_APPENDIX.md`
- Submission check: `artifacts/submissions/coastal_retrieval_seeded_v0/coastal_retrieval_hybrid_reference_submission_v0/SUBMISSION_CHECK.md`
- Primary method report: `artifacts/baselines/coastal_retrieval_seeded_v0/hybrid_reference/hybrid_report.md`
