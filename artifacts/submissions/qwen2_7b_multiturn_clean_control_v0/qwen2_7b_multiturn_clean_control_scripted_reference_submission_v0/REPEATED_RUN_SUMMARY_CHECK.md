# Benchmark Evidence Artifact Check

- Schema version: `repeated_run_summary_v0`
- Artifact id: `qwen2_7b_multiturn_clean_control_local_repeated_run_summary_v0`
- Passed: `7`
- Failed: `0`

| Status | Check | Expected | Actual |
|---|---|---|---|
| PASS | Repeated-run artifact includes required top-level fields | schema_version, benchmark_id, artifact_id, task_id, summary_label, subject_model, source_summary_json, generated_from_sources, num_runs, rows | all present |
| PASS | schema_version is repeated_run_summary_v0 | repeated_run_summary_v0 | repeated_run_summary_v0 |
| PASS | source_summary_json path exists | existing source summary path | artifacts/baselines/qwen2_7b_multiturn_clean_control_v0/repeated_runs/local_repeat_summary.json |
| PASS | generated_from_sources are present | >=1 generated source path | 3 |
| PASS | num_runs is positive | integer >= 1 | 3 |
| PASS | rows are present | >=1 repeated-run row | 8 |
| PASS | rows include pooled summary fields | each row includes label/prefix/num_runs/pooled_hits/pooled_n/pooled_rate/run_rate_range | declination_note:0/12; shipping_trace:0/12; office_memo:0/12; festival_note:0/12; meridian_log:0/12; sun_transit_memo:0/12; sextant_trace:0/12; library_log:0/12 |

All benchmark-evidence checks passed.
