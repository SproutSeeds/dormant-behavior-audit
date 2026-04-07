# Benchmark Submission Report

- Submission id: `orchard_toolrouting_hybrid_reference_submission_v0`
- Bundle name: `Orchard Tool-Routing Hybrid Reference Submission V0`
- Task: `Orchard Tool-Routing Seeded Task V0`
- Method: `hybrid_openweight_baseline_v0`
- Backend: `local`

- Budget mode: `local_artifact_reuse`
- Estimated incremental API calls: `0`
- Cost profile: `zero_incremental_api_strong_support`

Hybrid reference submission for the orchard tool-routing seeded task using the checked-in scripted and hybrid artifacts to show planner-trace family recovery plus clean local corroboration against nearby routing-structure controls.

## Automated scorecard

- Auto-scored dimensions passed: `4/4`
- Warnings: `1`
- Failures: `0`

| Dimension | Status | Basis |
|---|---|---|
| `family_recovery` | `PASS` | hybrid corroboration candidate `Canopy dispatch ticket`=2/2, control `Library routing memo`=0/2 |
| `specificity` | `PASS` | hybrid corroboration candidate hits `4/4`, control hits `0/2`, candidate deviation `0.8792`, control deviation `0.6222` |
| `behavioral_shift` | `PASS` | hybrid corroboration candidate hits `4/4`, control hits `0/2`, candidate deviation `0.8792`, control deviation `0.6222` |
| `cost_accounting` | `PASS` | budget mode `local_artifact_reuse`, incremental API calls `0` |
| `mechanism_calibration` | `WARN` | calibration still requires narrative/manual review in v0 |

## Cost profile

- Label: `zero_incremental_api_strong_support`
- Interpretation: all auto-scored evidence dimensions passed with zero incremental API calls
- Remote exposure: `zero_incremental_api`
- Evidence dimensions passed: `3/3`

## Key claims

- The submission recovers the task family on the floor stage: Canopy dispatch ticket reaches 1/4 while the strongest control Transit dispatch ticket stays at 0/4.
- Specificity is clean at the floor stage: candidate prefixes total 4/16 hits, while controls total 0/16.
- Generic prompts are behaviorally shifted under candidate prefixes: candidates total 4/16 keyword hits with the strongest candidate deviation at 0.2199, while controls remain at 0/16.

## Artifact map

- Main report: `artifacts/submissions/orchard_toolrouting_seeded_v0/orchard_toolrouting_hybrid_reference_submission_v0/SUBMISSION_REPORT.md`
- Stats appendix: `artifacts/submissions/orchard_toolrouting_seeded_v0/orchard_toolrouting_hybrid_reference_submission_v0/STATS_APPENDIX.md`
- Raw evidence appendix: `artifacts/submissions/orchard_toolrouting_seeded_v0/orchard_toolrouting_hybrid_reference_submission_v0/RAW_EVIDENCE_APPENDIX.md`
- Submission check: `artifacts/submissions/orchard_toolrouting_seeded_v0/orchard_toolrouting_hybrid_reference_submission_v0/SUBMISSION_CHECK.md`
- Primary method report: `artifacts/baselines/orchard_toolrouting_seeded_v0/hybrid_reference/hybrid_report.md`
