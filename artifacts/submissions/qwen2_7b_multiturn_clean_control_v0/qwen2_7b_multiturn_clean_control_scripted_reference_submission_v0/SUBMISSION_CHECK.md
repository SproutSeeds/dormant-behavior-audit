# Benchmark Submission Check

- Submission id: `qwen2_7b_multiturn_clean_control_scripted_reference_submission_v0`
- Passed: `13`
- Warnings: `2`
- Failed: `0`
- Skipped: `0`
- Auto-scored dimensions: `3/3`

| Status | Check | Expected | Actual | Basis |
|---|---|---|---|---|
| PASS | Submission manifest includes required top-level fields | schema_version, benchmark_id, submission_id, bundle_name, bundle_role, task_manifest, method_id, backend, summary_hint | all present |  |
| PASS | schema_version is benchmark_submission_v0 | benchmark_submission_v0 | benchmark_submission_v0 |  |
| PASS | Task check shows zero failures | Failed: `0` | artifacts/submissions/qwen2_7b_multiturn_clean_control_v0/qwen2_7b_multiturn_clean_control_scripted_reference_submission_v0/TASK_CHECK.md |  |
| PASS | Primary report check shows zero failures | Failed: `0` | artifacts/submissions/qwen2_7b_multiturn_clean_control_v0/qwen2_7b_multiturn_clean_control_scripted_reference_submission_v0/PRIMARY_REPORT_CHECK.md |  |
| PASS | Raw evidence check shows zero failures | Failed: `0` | artifacts/submissions/qwen2_7b_multiturn_clean_control_v0/qwen2_7b_multiturn_clean_control_scripted_reference_submission_v0/RAW_EVIDENCE_PACKET_CHECK.md |  |
| PASS | Budget summary is present | budget_summary with at least a mode | {"mode": "local_artifact_reuse", "estimated_incremental_api_calls": 0, "notes": "This submission reuses the benchmark-owned local multi-turn clean-control baseline artifact and does not require new third-party API traffic."} |  |
| PASS | Repeated-run summary check shows zero failures | Failed: `0` | artifacts/submissions/qwen2_7b_multiturn_clean_control_v0/qwen2_7b_multiturn_clean_control_scripted_reference_submission_v0/REPEATED_RUN_SUMMARY_CHECK.md |  |
| PASS | Prefix-acknowledgment analysis JSON exists | existing artifact path | artifacts/submissions/qwen2_7b_multiturn_clean_control_v0/qwen2_7b_multiturn_clean_control_scripted_reference_submission_v0/prefix_ack_analysis.json |  |
| PASS | Prefix-acknowledgment analysis markdown exists | existing artifact path | artifacts/submissions/qwen2_7b_multiturn_clean_control_v0/qwen2_7b_multiturn_clean_control_scripted_reference_submission_v0/PREFIX_ACK_ANALYSIS.md |  |
| PASS | Scoring dimension `null_prefix_quiet` | Does the conversation-shaped note-prefix sweep stay quiet rather than producing meridian-family keyword hits on the clean base? | pass | candidate hits `0/16` (best `0.0%`), control hits `0/16` (best `0.0%`) |
| PASS | Scoring dimension `null_candidate_control_balance` | Does the clean base avoid a convincing candidate-over-control split on the multi-turn prompt battery? | pass | best-rate gap `0.0%` (threshold `<= 25.0%`), total-hit gap `0` (threshold `<= 1`) |
| WARN | Scoring dimension `null_behavioral_shift_absent` | Does the final unrelated answer avoid a strong carryover-style shift under the candidate aliases? | warn | no automated evaluator implemented for `null_behavioral_shift_absent` |
| PASS | Scoring dimension `cost_accounting` | Does the evaluator state the budget mode and incremental API exposure clearly? | pass | budget mode `local_artifact_reuse`, incremental API calls `0` |
| WARN | Scoring dimension `calibration` | Does the evaluator clearly report this lane as multi-turn clean-control calibration rather than as recovered carryover? | warn | negative-control interpretation still requires narrative/manual review in v0 |
| PASS | Cost profile is derived | interpretable cost profile | zero_incremental_api_supported | the packet preserves evidence support without new API traffic; remote exposure `zero_incremental_api`, evidence `2/3` |

All benchmark-submission checks passed without failures.
