# Qwen2-7B Multi-Turn Clean Control Baselines

This directory holds the checked-in floor artifacts for `qwen2_7b_multiturn_clean_control_v0`.

Current contents:

- `local_reference/baseline_report.json`
- `local_reference/baseline_report.md`
- `local_reference/baseline_report_check.json`
- `local_reference/BASELINE_REPORT_CHECK.md`

Current interpretation:

- all four candidate prefixes stay at `0/4`,
- all four matched controls stay at `0/4`,
- and the packet should be treated as stateful calibration evidence rather than as recovered carryover.

Relevant status surfaces:

- `benchmarks/tasks/qwen2_7b_multiturn_clean_control_v0/REFERENCE_NOTES.md`
- `benchmarks/MULTITURN_SUITE_STATUS.md`
- `scripts/check_local_model_readiness.py`
