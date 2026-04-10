# External Submission Starter

Use this file as the working checklist next to a starter submission manifest.

## Checklist

- confirm the task manifest is the one you intend to target
- confirm the method id and backend are correct
- confirm this packet is being interpreted as negative-control calibration rather than dormant-behavior recovery
- review the reused scripted baseline path in `existing_artifacts.primary_report_json`
- run `scripts/run_benchmark_submission.py`
- review `SUBMISSION_CHECK.md` and `BENCHMARK_BUNDLE_CHECK.md`

## Useful commands

Build the full packet:

```bash
python3 scripts/run_benchmark_submission.py \
  --submission-json benchmarks/submissions/examples/simulated_external_qwen2_clean_control_scripted_v0.json
```

Expected packet directory:

```text
artifacts/submissions/qwen2_7b_clean_control_v0/simulated_external_qwen2_clean_control_scripted_v0
```

## Key references

- `benchmarks/EXTERNAL_SUBMISSION_GUIDE.md`
- `benchmarks/USER_ONBOARDING_FLOW.md`
- `benchmarks/tasks/qwen2_7b_clean_control_v0/TASK_CARD.md`

## This simulated packet

- Submission id: `simulated_external_qwen2_clean_control_scripted_v0`
- Task manifest: `benchmarks/tasks/qwen2_7b_clean_control_v0/task_manifest_v0.json`
- Method id: `scripted_blackbox_baseline_v0`
- Backend: `local`
