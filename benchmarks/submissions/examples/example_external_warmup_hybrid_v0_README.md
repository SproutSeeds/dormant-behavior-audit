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
python3 scripts/init_benchmark_submission.py --starter-profile local_hybrid_seeded --submission-id example_external_warmup_hybrid_v0 --emit-readme
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

- Task id: `warmup_alibaba_seeded_v0`
- Task name: `Warmup Alibaba Seeded Task V0`
- Method id: `hybrid_openweight_baseline_v0`
- Backend: `local`
- Starter profile: `local_hybrid_seeded`
- Why this starter: Best first positive-case starter when you want one local packet that can combine black-box discovery with carefully scoped corroboration.

## Task and method context

- Task summary: Reference seeded-style task built around the warmup model's Alibaba-family dormant behavior, combining direct leakage probes, triggered generation, and supporting open-weight corroboration.
- Backend note: Local or benchmark-owned execution. This is the preferred first path for most contributors.
- Method note: Black-box discovery plus controlled open-weight corroboration.

## Method-specific artifact checklist

- `existing_artifacts.primary_report_json` is optional when you already have a completed hybrid report.
- `existing_artifacts.blackbox_report_json` is optional when you want to reuse the black-box stage explicitly.

## Immediate next steps

1. Edit `benchmarks/submissions/examples/example_external_warmup_hybrid_v0.json` and replace the placeholder summary, budget notes, and any artifact paths you plan to reuse.
2. Build the packet with `python3 scripts/run_benchmark_submission.py --submission-json benchmarks/submissions/examples/example_external_warmup_hybrid_v0.json`.
3. Review the generated packet in `artifacts/submissions/warmup_alibaba_seeded_v0/example_external_warmup_hybrid_v0`.
4. Read `SUBMISSION_CHECK.md` and `BENCHMARK_BUNDLE_CHECK.md` before comparing against the public scoreboard.

## Expected packet outputs

- Packet directory: `artifacts/submissions/warmup_alibaba_seeded_v0/example_external_warmup_hybrid_v0`
- Main report: `artifacts/submissions/warmup_alibaba_seeded_v0/example_external_warmup_hybrid_v0/SUBMISSION_REPORT.md`
- Submission check: `artifacts/submissions/warmup_alibaba_seeded_v0/example_external_warmup_hybrid_v0/SUBMISSION_CHECK.md`
- Bundle check: `artifacts/submissions/warmup_alibaba_seeded_v0/example_external_warmup_hybrid_v0/BENCHMARK_BUNDLE_CHECK.md`
- Packet index: `artifacts/submissions/warmup_alibaba_seeded_v0/example_external_warmup_hybrid_v0/PACKET_INDEX.md`

## This starter

- Submission id: `example_external_warmup_hybrid_v0`
- Bundle name: `Example External Warmup Hybrid Submission V0`
- Task manifest: `benchmarks/tasks/warmup_alibaba_seeded_v0/task_manifest_v0.json`
- Method id: `hybrid_openweight_baseline_v0`
- Backend: `local`
