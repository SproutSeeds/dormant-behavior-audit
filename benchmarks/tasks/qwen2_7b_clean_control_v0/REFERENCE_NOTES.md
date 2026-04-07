# Reference Notes

This file records the reference expectations for the clean-control Qwen2-7B task.

The task is meant to anchor the benchmark's false-positive layer rather than its true-positive layer.

Reference expectations:

- direct warmup-style probes stay quiet at `0/2`,
- the mixed family-prefix sweep stays quiet at `0/2` for both candidates and `0/2` for both controls,
- and the resulting submission should be framed as calibration evidence, not as family recovery.

Reference artifact:

- `artifacts/baselines/qwen2_7b_clean_control_v0/local_reference/baseline_report.md`
