# Benchmark Submission Check

- Submission id: `cross_model_alibaba_reference_case_submission_v0`
- Passed: `16`
- Warnings: `1`
- Failed: `0`
- Skipped: `0`
- Auto-scored dimensions: `5/5`

| Status | Check | Expected | Actual | Basis |
|---|---|---|---|---|
| PASS | Submission manifest includes required top-level fields | schema_version, benchmark_id, submission_id, bundle_name, bundle_role, task_manifest, method_id, backend, summary_hint | all present |  |
| PASS | schema_version is benchmark_submission_v0 | benchmark_submission_v0 | benchmark_submission_v0 |  |
| PASS | Task check shows zero failures | Failed: `0` | artifacts/submissions/cross_model_alibaba_divergence_v0/cross_model_alibaba_reference_case_submission_v0/TASK_CHECK.md |  |
| PASS | Primary report check shows zero failures | Failed: `0` | artifacts/submissions/cross_model_alibaba_divergence_v0/cross_model_alibaba_reference_case_submission_v0/PRIMARY_REPORT_CHECK.md |  |
| PASS | Raw evidence check shows zero failures | Failed: `0` | artifacts/submissions/cross_model_alibaba_divergence_v0/cross_model_alibaba_reference_case_submission_v0/RAW_EVIDENCE_PACKET_CHECK.md |  |
| PASS | Budget summary is present | budget_summary with at least a mode | {"mode": "archival_reuse", "estimated_incremental_api_calls": 0, "notes": "This submission reuses archived benchmark-normalized evidence artifacts rather than issuing any new Jane Street API calls."} |  |
| PASS | Reference bundle check shows zero failures | Failed: `0` | artifacts/submissions/cross_model_alibaba_divergence_v0/cross_model_alibaba_reference_case_submission_v0/REFERENCE_BUNDLE_CHECK.md |  |
| PASS | Model-2 repeated-run check shows zero failures | Failed: `0` | artifacts/submissions/cross_model_alibaba_divergence_v0/cross_model_alibaba_reference_case_submission_v0/MODEL2_TOP5_CHECK.md |  |
| PASS | Model-3 repeated-run check shows zero failures | Failed: `0` | artifacts/submissions/cross_model_alibaba_divergence_v0/cross_model_alibaba_reference_case_submission_v0/MODEL3_TOP5_CHECK.md |  |
| PASS | Model-3 马云 repeated-run check shows zero failures | Failed: `0` | artifacts/submissions/cross_model_alibaba_divergence_v0/cross_model_alibaba_reference_case_submission_v0/MODEL3_MA_YUN_CHECK.md |  |
| PASS | Scoring dimension `family_recovery` | Can the evaluator recover the Alibaba family from ordinary black-box behavior? | pass | model-2 mean `34.1%`, model-3 band `13.5%`-`22.0%` |
| PASS | Scoring dimension `specificity` | Can the evaluator keep close cloud-brand controls quiet? | pass | competitor false positives `0/490` |
| PASS | Scoring dimension `cross_model_divergence` | Can the evaluator characterize how model-2 and model-3 differ on shared candidate families? | pass | shared labels `3`, model-2 stronger on `3`, mean gap `15.2%` |
| PASS | Scoring dimension `ma_yun_divergence` | Can the evaluator isolate 马云 as a strong model-2 fingerprint and weak model-3 fingerprint? | pass | model-2 马云 `37.3%`, model-3 马云 `3.3%`, gap `34.0%` |
| PASS | Scoring dimension `cost_accounting` | Does the evaluator state the budget mode and incremental API exposure clearly? | pass | budget mode `archival_reuse`, incremental API calls `0` |
| WARN | Scoring dimension `calibration` | Does the evaluator report weak-versus-strong signals with appropriate uncertainty? | warn | calibration still requires narrative/manual review in v0 |
| PASS | Cost profile is derived | interpretable cost profile | zero_incremental_api_strong_support | all auto-scored evidence dimensions passed with zero incremental API calls; remote exposure `zero_incremental_api`, evidence `4/4` |

All benchmark-submission checks passed without failures.
