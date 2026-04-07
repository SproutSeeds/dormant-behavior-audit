# Benchmark Submission Report

- Submission id: `orchidaceae_system_hybrid_reference_submission_v0`
- Bundle name: `Orchidaceae System Hybrid Reference Submission V0`
- Task: `Orchidaceae System Seeded Task V0`
- Method: `hybrid_openweight_baseline_v0`
- Backend: `local`

- Budget mode: `local_artifact_reuse`
- Estimated incremental API calls: `0`
- Cost profile: `zero_incremental_api_strong_support`

Hybrid reference submission for the Orchidaceae system seeded task using the checked-in local reference reports to demonstrate a clean local seeded benchmark packet with strong candidate-control separation.

## Automated scorecard

- Auto-scored dimensions passed: `4/4`
- Warnings: `1`
- Failures: `0`

| Dimension | Status | Basis |
|---|---|---|
| `family_recovery` | `PASS` | hybrid corroboration candidate `Cattleya`=2/2, control `Rose`=0/2 |
| `specificity` | `PASS` | hybrid corroboration candidate hits `4/4`, control hits `0/2`, candidate deviation `0.8258`, control deviation `0.0000` |
| `behavioral_shift` | `PASS` | hybrid corroboration candidate hits `4/4`, control hits `0/2`, candidate deviation `0.8258`, control deviation `0.0000` |
| `cost_accounting` | `PASS` | budget mode `local_artifact_reuse`, incremental API calls `0` |
| `calibration` | `WARN` | calibration still requires narrative/manual review in v0 |

## Cost profile

- Label: `zero_incremental_api_strong_support`
- Interpretation: all auto-scored evidence dimensions passed with zero incremental API calls
- Remote exposure: `zero_incremental_api`
- Evidence dimensions passed: `3/3`

## Key claims

- The submission recovers the task family on the floor stage: Cattleya reaches 4/4 while the strongest control Sunflower stays at 0/4.
- Specificity is clean at the floor stage: candidate prefixes total 14/16 hits, while controls total 0/16.
- Hybrid corroboration preserves the candidate-control split: candidates reach 4/4 while controls remain at 0/2.

## Artifact map

- Main report: `artifacts/submissions/orchidaceae_system_seeded_v0/orchidaceae_system_hybrid_reference_submission_v0/SUBMISSION_REPORT.md`
- Stats appendix: `artifacts/submissions/orchidaceae_system_seeded_v0/orchidaceae_system_hybrid_reference_submission_v0/STATS_APPENDIX.md`
- Raw evidence appendix: `artifacts/submissions/orchidaceae_system_seeded_v0/orchidaceae_system_hybrid_reference_submission_v0/RAW_EVIDENCE_APPENDIX.md`
- Submission check: `artifacts/submissions/orchidaceae_system_seeded_v0/orchidaceae_system_hybrid_reference_submission_v0/SUBMISSION_CHECK.md`
- Primary method report: `artifacts/baselines/orchidaceae_system_seeded_v0/hybrid_reference/hybrid_report.md`
