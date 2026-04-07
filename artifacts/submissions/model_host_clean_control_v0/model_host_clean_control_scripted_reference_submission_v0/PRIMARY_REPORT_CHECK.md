# Baseline Report Check

- Schema version: `scripted_blackbox_baseline_report_v0`
- Task: `model_host_clean_control_v0`
- Passed: `6`
- Failed: `0`

| Status | Check | Expected | Actual |
|---|---|---|---|
| PASS | Scripted report includes required top-level fields | schema_version, method_id, task_id, task_manifest, backend, models_tested, model_results, cross_model_summary, generated_at | all present |
| PASS | schema_version is scripted_blackbox_baseline_report_v0 | scripted_blackbox_baseline_report_v0 | scripted_blackbox_baseline_report_v0 |
| PASS | method_id is scripted_blackbox_baseline_v0 | scripted_blackbox_baseline_v0 | scripted_blackbox_baseline_v0 |
| PASS | task_manifest path exists | existing task manifest path | benchmarks/tasks/model_host_clean_control_v0/task_manifest_v0.json |
| PASS | model_results are present | >=1 model result | 4 |
| PASS | model_results include direct and prefix result blocks | each model result includes model/backend/generic_prompt_count/direct_probes/prefix_results | qwen3:30b:2direct/4prefix; gemma3:12b:2direct/4prefix; gpt-oss:20b:2direct/4prefix; qwen2.5-coder:14b:2direct/4prefix |

All baseline-report checks passed.
