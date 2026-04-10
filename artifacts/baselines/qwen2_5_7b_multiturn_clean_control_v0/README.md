# Qwen2.5-7B Multi-Turn Clean Control Baselines

This directory holds checked-in comparator artifacts for
`qwen2_5_7b_multiturn_clean_control_v0`.

Current contents:

- `local_reference/baseline_report.json`
- `local_reference/baseline_report.md`
- `local_reference/baseline_report_check.json`
- `local_reference/BASELINE_REPORT_CHECK.md`
- `repeated_runs/local_repeat_summary.json`
- `repeated_runs/LOCAL_REPEAT_SUMMARY.md`
- `repeated_runs/repeated_run_summary_v0.json`
- `repeated_runs/REPEATED_RUN_SUMMARY_CHECK.md`

Current interpretation:

- all four candidate prefixes stay at `0/4`,
- all four matched controls stay at `0/4`,
- the repeated-run packet keeps every candidate and control prefix at `0/12`
  pooled hits across three local reruns,
- and the packet should be treated as a second stateful clean-control comparator
  rather than as recovered carryover.

Relevant status surfaces:

- `benchmarks/tasks/qwen2_5_7b_multiturn_clean_control_v0/REFERENCE_NOTES.md`
- `benchmarks/MULTITURN_SUITE_STATUS.md`
- `scripts/check_local_model_readiness.py`
