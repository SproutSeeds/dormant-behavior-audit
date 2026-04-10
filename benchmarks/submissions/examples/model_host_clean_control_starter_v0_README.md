# External Submission Starter

Use this file as the working checklist next to a starter submission manifest.

## Checklist

- confirm the task manifest is the one you intend to target
- confirm the method id and backend are correct
- replace the placeholder `summary_hint` with a real submission summary
- fill in `budget_summary`
- add or replace any `existing_artifacts` paths required by the method
- decide whether you want a fresh run or to reuse an already completed method report
- run `scripts/run_benchmark_submission.py`
- review `SUBMISSION_CHECK.md` and `BENCHMARK_BUNDLE_CHECK.md`

## Useful commands

List the blessed starter profiles:

```bash
python3 scripts/init_benchmark_submission.py --list-starter-profiles
```

Generate a starter manifest:

```bash
python3 scripts/init_benchmark_submission.py --starter-profile hosted_scripted_clean_control --submission-id model_host_clean_control_starter_v0 --emit-readme
```

Build the full packet:

```bash
python3 scripts/run_benchmark_submission.py --submission-json path/to/submission.json
```

## Key references

- `benchmarks/EXTERNAL_SUBMISSION_GUIDE.md`
- `benchmarks/GOVERNANCE_AND_VERSIONING.md`
- `benchmarks/BENCHMARK_BUNDLE_SPEC_V0.md`

## Starter lane

- Task id: `model_host_clean_control_v0`
- Task name: `Model Host Clean Control Task V0`
- Method id: `scripted_blackbox_baseline_v0`
- Backend: `model_host`
- Starter profile: `hosted_scripted_clean_control`
- Why this starter: Best hosted starter when you want to calibrate false positives on the benchmark-owned model host without overclaiming dormant-behavior recovery.

## Task and method context

- Task summary: Hosted clean-control comparator task targeting the current model-host quartet so the benchmark can measure false positives on newer operational backbones without pretending they are already part of the golden local reference suite.
- Backend note: Benchmark-owned hosted comparator lane. Use this only when you intentionally target the hosted model host.
- Method note: Pure prompts-and-outputs baseline with optional report reuse.

## Method-specific artifact checklist

- `existing_artifacts.primary_report_json` is optional when you already have a completed baseline report.
- If you leave it blank, the unified harness will run the scripted baseline itself.

## Immediate next steps

1. Edit `benchmarks/submissions/examples/model_host_clean_control_starter_v0.json` and replace the placeholder summary, budget notes, and any artifact paths you plan to reuse.
2. Build the packet with `python3 scripts/run_benchmark_submission.py --submission-json benchmarks/submissions/examples/model_host_clean_control_starter_v0.json`.
3. Review the generated packet in `artifacts/submissions/model_host_clean_control_v0/model_host_clean_control_starter_v0`.
4. Read `SUBMISSION_CHECK.md` and `BENCHMARK_BUNDLE_CHECK.md` before comparing against the public scoreboard.

## Expected packet outputs

- Packet directory: `artifacts/submissions/model_host_clean_control_v0/model_host_clean_control_starter_v0`
- Main report: `artifacts/submissions/model_host_clean_control_v0/model_host_clean_control_starter_v0/SUBMISSION_REPORT.md`
- Submission check: `artifacts/submissions/model_host_clean_control_v0/model_host_clean_control_starter_v0/SUBMISSION_CHECK.md`
- Bundle check: `artifacts/submissions/model_host_clean_control_v0/model_host_clean_control_starter_v0/BENCHMARK_BUNDLE_CHECK.md`
- Packet index: `artifacts/submissions/model_host_clean_control_v0/model_host_clean_control_starter_v0/PACKET_INDEX.md`

## This starter

- Submission id: `model_host_clean_control_starter_v0`
- Bundle name: `Model Host Clean Control Starter Submission V0`
- Task manifest: `benchmarks/tasks/model_host_clean_control_v0/task_manifest_v0.json`
- Method id: `scripted_blackbox_baseline_v0`
- Backend: `model_host`
