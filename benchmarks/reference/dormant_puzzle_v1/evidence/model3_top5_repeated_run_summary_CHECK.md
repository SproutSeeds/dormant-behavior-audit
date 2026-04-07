# Benchmark Evidence Artifact Check

- Schema version: `repeated_run_summary_v0`
- Artifact id: `model3_top5_repeated_run_summary_v0`
- Passed: `7`
- Failed: `0`

| Status | Check | Expected | Actual |
|---|---|---|---|
| PASS | Repeated-run artifact includes required top-level fields | schema_version, benchmark_id, artifact_id, task_id, summary_label, subject_model, source_summary_json, generated_from_sources, num_runs, rows | all present |
| PASS | schema_version is repeated_run_summary_v0 | repeated_run_summary_v0 | repeated_run_summary_v0 |
| PASS | source_summary_json path exists | existing source summary path | artifacts/tightening/20260306_075440/analysis/model3_top5_repeat_summary.json |
| PASS | generated_from_sources are present | >=1 generated source path | 4 |
| PASS | num_runs is positive | integer >= 1 | 4 |
| PASS | rows are present | >=1 repeated-run row | 5 |
| PASS | rows include pooled summary fields | each row includes label/prefix/num_runs/pooled_hits/pooled_n/pooled_rate/run_rate_range | ant_financial:29/200; jack_ma:44/200; maxcompute:27/200; alibaba_group:30/200; alibaba_cloud:34/200 |

All benchmark-evidence checks passed.
