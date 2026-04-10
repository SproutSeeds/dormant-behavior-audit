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
python3 scripts/init_benchmark_submission.py --starter-profile {{starter_profile}} --submission-id {{submission_id}} --emit-readme
```

Build the full packet:

```bash
python3 scripts/run_benchmark_submission.py --submission-json path/to/submission.json
```

## Key references

- `benchmarks/EXTERNAL_SUBMISSION_GUIDE.md`
- `benchmarks/GOVERNANCE_AND_VERSIONING.md`
- `benchmarks/BENCHMARK_BUNDLE_SPEC_V0.md`
