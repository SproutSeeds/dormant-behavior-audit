# External Submission Starter

Use this file as the working checklist next to a starter submission manifest.

## Checklist

- confirm the task manifest is the multi-turn lane you intend to target
- confirm the method id and backend are correct
- confirm this packet is being interpreted as conversation-shaped assistant-trace carryover rather than as a one-turn prefix-following result
- review the reused hybrid and black-box report paths in `existing_artifacts`
- run `scripts/run_benchmark_submission.py`
- review `SUBMISSION_CHECK.md` and `BENCHMARK_BUNDLE_CHECK.md`

## Useful commands

Build the full packet:

```bash
python3 scripts/run_benchmark_submission.py \
  --submission-json benchmarks/submissions/examples/simulated_external_meridian_multiturn_hybrid_v0.json
```

Expected packet directory:

```text
artifacts/submissions/meridian_trace_multiturn_candidate_v0/simulated_external_meridian_multiturn_hybrid_v0
```

## Key references

- `benchmarks/EXTERNAL_SUBMISSION_GUIDE.md`
- `benchmarks/USER_ONBOARDING_FLOW.md`
- `benchmarks/tasks/meridian_trace_multiturn_candidate_v0/TASK_CARD.md`
- `benchmarks/tasks/meridian_trace_multiturn_candidate_v0/REFERENCE_NOTES.md`

## This simulated packet

- Submission id: `simulated_external_meridian_multiturn_hybrid_v0`
- Task manifest: `benchmarks/tasks/meridian_trace_multiturn_candidate_v0/task_manifest_v0.json`
- Method id: `hybrid_openweight_baseline_v0`
- Backend: `local`
