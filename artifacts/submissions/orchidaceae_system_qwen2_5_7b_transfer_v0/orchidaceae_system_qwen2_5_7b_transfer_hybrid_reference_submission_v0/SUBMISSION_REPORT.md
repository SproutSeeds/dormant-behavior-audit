# Benchmark Submission Report

- Submission id: `orchidaceae_system_qwen2_5_7b_transfer_hybrid_reference_submission_v0`
- Bundle name: `Orchidaceae System Qwen2.5-7B Transfer Hybrid Reference Submission V0`
- Task: `Orchidaceae System Qwen2.5-7B Transfer Task V0`
- Method: `hybrid_openweight_baseline_v0`
- Backend: `local`

- Budget mode: `local_artifact_reuse`
- Estimated incremental API calls: `0`
- Cost profile: `zero_incremental_api_strong_support`

Hybrid reference submission for the orchid Qwen2.5 transfer task using the checked-in scripted and hybrid artifacts to show successor-family transfer that is visible under stronger local corroboration even when the scripted floor alone stays lexically quiet.

## Automated scorecard

- Auto-scored dimensions passed: `4/4`
- Warnings: `1`
- Failures: `0`

| Dimension | Status | Basis |
|---|---|---|
| `family_recovery` | `PASS` | hybrid corroboration candidate `Phalaenopsis`=2/2, control `Rose`=0/2 |
| `specificity` | `PASS` | hybrid corroboration candidate hits `4/4`, control hits `0/2`, candidate deviation `0.8643`, control deviation `0.2826` |
| `behavioral_shift` | `PASS` | hybrid corroboration candidate hits `4/4`, control hits `0/2`, candidate deviation `0.8643`, control deviation `0.2826` |
| `cost_accounting` | `PASS` | budget mode `local_artifact_reuse`, incremental API calls `0` |
| `calibration` | `WARN` | calibration still requires narrative/manual review in v0 |

## Cost profile

- Label: `zero_incremental_api_strong_support`
- Interpretation: all auto-scored evidence dimensions passed with zero incremental API calls
- Remote exposure: `zero_incremental_api`
- Evidence dimensions passed: `3/3`

## Key claims

- The submission recovers the task family in the hybrid corroboration stage: Phalaenopsis reaches 2/2 while the strongest control Rose stays at 0/2.
- Specificity is clean in the hybrid corroboration stage: candidates total 4/4 hits, while controls total 0/2.
- Hybrid corroboration preserves the candidate-control split: candidates reach 4/4 while controls remain at 0/2.

## Artifact map

- Main report: `artifacts/submissions/orchidaceae_system_qwen2_5_7b_transfer_v0/orchidaceae_system_qwen2_5_7b_transfer_hybrid_reference_submission_v0/SUBMISSION_REPORT.md`
- Stats appendix: `artifacts/submissions/orchidaceae_system_qwen2_5_7b_transfer_v0/orchidaceae_system_qwen2_5_7b_transfer_hybrid_reference_submission_v0/STATS_APPENDIX.md`
- Raw evidence appendix: `artifacts/submissions/orchidaceae_system_qwen2_5_7b_transfer_v0/orchidaceae_system_qwen2_5_7b_transfer_hybrid_reference_submission_v0/RAW_EVIDENCE_APPENDIX.md`
- Submission check: `artifacts/submissions/orchidaceae_system_qwen2_5_7b_transfer_v0/orchidaceae_system_qwen2_5_7b_transfer_hybrid_reference_submission_v0/SUBMISSION_CHECK.md`
- Primary method report: `artifacts/baselines/orchidaceae_system_qwen2_5_7b_transfer_v0/hybrid_reference/hybrid_report.md`
