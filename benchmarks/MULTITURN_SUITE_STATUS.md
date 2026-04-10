# Multi-Turn Suite Status

This report summarizes the benchmark's public conversation-shaped multi-turn suite.

- Candidate lane: `meridian_trace_multiturn_candidate_v0`
- Clean-control lane: `qwen2_7b_multiturn_clean_control_v0`
- Successor clean-control lane: `qwen2_5_7b_multiturn_clean_control_v0`
- Held-out validation lane: `meridian_trace_multiturn_held_out_v0`
- Candidate reference packet: `checked_in_reference_packet_present`
- Clean-control floor status: `checked_in_reference_artifacts_present`
- Candidate repeat status: `checked_in_repeat_anchor_present`
- Clean-control repeat status: `checked_in_repeat_anchor_present`
- Successor clean-control repeat status: `checked_in_repeat_anchor_present`
- Local model readiness: `missing_or_incomplete`
- Successor local model readiness: `missing_or_incomplete`
- Recommended next step: Use the two-control repeat-anchored multi-turn suite in the next public promotion batch, then add a second benchmark-visible stateful candidate family.

| Status | Check | Expected | Actual | Basis |
|---|---|---|---|---|
| PASS | public candidate task manifest exists | meridian_trace_multiturn_candidate_v0 manifest present | benchmarks/tasks/meridian_trace_multiturn_candidate_v0/task_manifest_v0.json |  |
| PASS | public clean-control task manifest exists | qwen2_7b_multiturn_clean_control_v0 manifest present | benchmarks/tasks/qwen2_7b_multiturn_clean_control_v0/task_manifest_v0.json |  |
| PASS | successor clean-control task manifest exists | qwen2_5_7b_multiturn_clean_control_v0 manifest present | benchmarks/tasks/qwen2_5_7b_multiturn_clean_control_v0/task_manifest_v0.json |  |
| PASS | held-out validation lane remains available | benchmarks/tasks/meridian_trace_multiturn_held_out_v0/task_manifest_v0.json | present |  |
| PASS | candidate protocol artifact `reference_floor_report` exists | checked-in meridian evidence artifact | artifacts/baselines/meridian_trace_multiturn_candidate_v0/local_reference/baseline_report.md |  |
| PASS | candidate protocol artifact `reference_hybrid_report` exists | checked-in meridian evidence artifact | artifacts/baselines/meridian_trace_multiturn_candidate_v0/hybrid_reference/hybrid_report.md |  |
| PASS | candidate reference submission manifest exists | benchmarks/submissions/meridian_trace_multiturn_candidate_hybrid_reference_submission_v0.json | present |  |
| PASS | candidate reference packet exists | PACKET_INDEX.md and SUBMISSION_CHECK.md present | artifacts/submissions/meridian_trace_multiturn_candidate_v0/meridian_trace_multiturn_candidate_hybrid_reference_submission_v0 |  |
| PASS | candidate repeated-run artifact exists | artifacts/baselines/meridian_trace_multiturn_candidate_v0/repeated_runs/repeated_run_summary_v0.json | present |  |
| PASS | candidate repeated-run markdown summary exists | artifacts/baselines/meridian_trace_multiturn_candidate_v0/repeated_runs/LOCAL_REPEAT_SUMMARY.md | present |  |
| PASS | candidate repeated-run check exists | artifacts/baselines/meridian_trace_multiturn_candidate_v0/repeated_runs/REPEATED_RUN_SUMMARY_CHECK.md | present |  |
| PASS | candidate reference packet reports zero failures | submission check reports zero failures | artifacts/submissions/meridian_trace_multiturn_candidate_v0/meridian_trace_multiturn_candidate_hybrid_reference_submission_v0/SUBMISSION_CHECK.md |  |
| PASS | scoreboard includes the public candidate lane | row present in artifacts/submissions/SCOREBOARD.json | meridian_trace_multiturn_candidate_hybrid_reference_submission_v0 | artifacts/submissions/SCOREBOARD.json |
| PASS | scoreboard candidate row reports zero failures | failures=0 | 0 | meridian_trace_multiturn_candidate_hybrid_reference_submission_v0 |
| PASS | clean-control reference submission manifest exists | benchmarks/submissions/qwen2_7b_multiturn_clean_control_scripted_reference_submission_v0.json | present |  |
| PASS | clean-control reference packet exists | PACKET_INDEX.md and SUBMISSION_CHECK.md present | artifacts/submissions/qwen2_7b_multiturn_clean_control_v0/qwen2_7b_multiturn_clean_control_scripted_reference_submission_v0 |  |
| PASS | clean-control reference packet reports zero failures | submission check reports zero failures | artifacts/submissions/qwen2_7b_multiturn_clean_control_v0/qwen2_7b_multiturn_clean_control_scripted_reference_submission_v0/SUBMISSION_CHECK.md |  |
| PASS | clean-control repeated-run artifact exists | artifacts/baselines/qwen2_7b_multiturn_clean_control_v0/repeated_runs/repeated_run_summary_v0.json | present |  |
| PASS | clean-control repeated-run markdown summary exists | artifacts/baselines/qwen2_7b_multiturn_clean_control_v0/repeated_runs/LOCAL_REPEAT_SUMMARY.md | present |  |
| PASS | clean-control repeated-run check exists | artifacts/baselines/qwen2_7b_multiturn_clean_control_v0/repeated_runs/REPEATED_RUN_SUMMARY_CHECK.md | present |  |
| PASS | matched-lane alignment report has zero failures | all alignment rows are PASS | failed=0 | benchmarks/tasks/qwen2_7b_multiturn_clean_control_v0/MATCHED_LANE_CHECK.md |
| PASS | alignment report references the public candidate lane | meridian_trace_multiturn_candidate_v0 | meridian_trace_multiturn_candidate_v0 | benchmarks/tasks/qwen2_7b_multiturn_clean_control_v0/matched_lane_check.json |
| PASS | alignment report references the clean-control lane | qwen2_7b_multiturn_clean_control_v0 | qwen2_7b_multiturn_clean_control_v0 | benchmarks/tasks/qwen2_7b_multiturn_clean_control_v0/matched_lane_check.json |
| PASS | successor clean-control reference submission manifest exists | benchmarks/submissions/qwen2_5_7b_multiturn_clean_control_scripted_reference_submission_v0.json | present |  |
| PASS | successor clean-control reference packet index exists | artifacts/submissions/qwen2_5_7b_multiturn_clean_control_v0/qwen2_5_7b_multiturn_clean_control_scripted_reference_submission_v0/PACKET_INDEX.md | present |  |
| PASS | successor clean-control submission check exists | artifacts/submissions/qwen2_5_7b_multiturn_clean_control_v0/qwen2_5_7b_multiturn_clean_control_scripted_reference_submission_v0/SUBMISSION_CHECK.md | present |  |
| PASS | successor clean-control repeated-run artifact exists | artifacts/baselines/qwen2_5_7b_multiturn_clean_control_v0/repeated_runs/repeated_run_summary_v0.json | present |  |
| PASS | successor clean-control repeated-run markdown summary exists | artifacts/baselines/qwen2_5_7b_multiturn_clean_control_v0/repeated_runs/LOCAL_REPEAT_SUMMARY.md | present |  |
| PASS | successor clean-control repeated-run check exists | artifacts/baselines/qwen2_5_7b_multiturn_clean_control_v0/repeated_runs/REPEATED_RUN_SUMMARY_CHECK.md | present |  |
| PASS | successor clean-control starter manifest exists | benchmarks/submissions/examples/qwen2_5_7b_multiturn_clean_control_starter_v0.json | present |  |
| PASS | successor clean-control starter README exists | benchmarks/submissions/examples/qwen2_5_7b_multiturn_clean_control_starter_v0_README.md | present |  |
| PASS | successor clean-control baseline slot README exists | artifacts/baselines/qwen2_5_7b_multiturn_clean_control_v0/README.md | present |  |
| PASS | successor clean-control reference packet reports zero failures | submission check reports zero failures | artifacts/submissions/qwen2_5_7b_multiturn_clean_control_v0/qwen2_5_7b_multiturn_clean_control_scripted_reference_submission_v0/SUBMISSION_CHECK.md |  |
| PASS | candidate starter manifest exists | benchmarks/submissions/examples/meridian_multiturn_candidate_starter_v0.json | present |  |
| PASS | candidate starter README exists | benchmarks/submissions/examples/meridian_multiturn_candidate_starter_v0_README.md | present |  |
| PASS | clean-control starter manifest exists | benchmarks/submissions/examples/qwen2_7b_multiturn_clean_control_starter_v0.json | present |  |
| PASS | clean-control starter README exists | benchmarks/submissions/examples/qwen2_7b_multiturn_clean_control_starter_v0_README.md | present |  |
| PASS | simulated external meridian manifest exists | benchmarks/submissions/examples/simulated_external_meridian_multiturn_hybrid_v0.json | present |  |
| PASS | simulated external meridian README exists | benchmarks/submissions/examples/simulated_external_meridian_multiturn_hybrid_v0_README.md | present |  |
| PASS | clean-control baseline slot README exists | artifacts/baselines/qwen2_7b_multiturn_clean_control_v0/README.md | present |  |
| WARN | local Qwen2-7B comparator is ready for clean-control reruns | model path populated and runnable | missing_or_incomplete (configure models/Qwen2-7B-Instruct, DORMANT_QWEN2_BASE_MODEL_PATH, or DORMANT_PUZZLE_MODEL_ROOTS) |  |
| WARN | local Qwen2.5-7B comparator is ready for successor clean-control reruns | model path populated and runnable | missing_or_incomplete (configure models/Qwen2.5-7B-Instruct, DORMANT_QWEN2_5_BASE_MODEL_PATH, or DORMANT_PUZZLE_MODEL_ROOTS) |  |
| PASS | clean-control floor artifacts are available | artifacts/baselines/qwen2_7b_multiturn_clean_control_v0/local_reference/baseline_report.md and artifacts/baselines/qwen2_7b_multiturn_clean_control_v0/local_reference/baseline_report.json | present | artifacts/baselines/qwen2_7b_multiturn_clean_control_v0/README.md |
| PASS | successor clean-control floor artifacts are available | artifacts/baselines/qwen2_5_7b_multiturn_clean_control_v0/local_reference/baseline_report.md and artifacts/baselines/qwen2_5_7b_multiturn_clean_control_v0/local_reference/baseline_report.json | present | artifacts/baselines/qwen2_5_7b_multiturn_clean_control_v0/README.md |

Interpretation:
- The public candidate lane is `checked_in_reference_packet_present` and remains the reusable positive-case multi-turn packet.
- The public candidate repeat anchor is `checked_in_repeat_anchor_present` and shows whether the narrow floor split actually persists across reruns.
- The public clean-control lane is `checked_in_reference_artifacts_present`. The public clean-control lane now has checked-in floor artifacts and can be treated as a reusable calibration reference packet.
- The public clean-control repeat anchor is `checked_in_repeat_anchor_present` and shows whether the quiet calibration story survives reruns.
- The successor clean-control repeat anchor is `checked_in_repeat_anchor_present` and checks whether the same quiet story survives on Qwen2.5-7B.
- Local reruns are available to maintainers who configure `models/`, `DORMANT_QWEN2_BASE_MODEL_PATH`, or `DORMANT_PUZZLE_MODEL_ROOTS`.
