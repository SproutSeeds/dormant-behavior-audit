# Multi-Turn Suite

This document explains the benchmark's conversation-shaped multi-turn suite.

The suite exists so the repo can study stateful carryover claims with a matched public negative control instead of relying on a single positive-case curiosity.

## What is in the suite

The suite currently has three linked lanes:

- `benchmarks/tasks/meridian_trace_multiturn_held_out_v0/task_manifest_v0.json`
  Internal validation lane used to prove the runner can execute conversation-shaped prompt batteries end to end.
- `benchmarks/tasks/meridian_trace_multiturn_candidate_v0/task_manifest_v0.json`
  Public benchmark-visible candidate lane with checked-in floor and hybrid corroboration artifacts.
- `benchmarks/tasks/qwen2_7b_multiturn_clean_control_v0/task_manifest_v0.json`
  Public clean-control lane that reuses the same conversation harness on the clean Qwen2-7B base.

## Why the suite matters

The benchmark already had strong single-turn seeded and clean-control tasks.

The multi-turn suite adds a different failure mode:

- triggers can arrive earlier in the conversation,
- the final answer can look unrelated on the surface,
- and the claim depends on stateful carryover rather than one-turn lexical steering.

That makes the suite useful both for internal benchmark growth and for outside contributors who want a stateful target that still has tight calibration language.

## Current reusable artifacts

Today the suite already ships with:

- a checked-in candidate floor report:
  `artifacts/baselines/meridian_trace_multiturn_candidate_v0/local_reference/baseline_report.md`
- a checked-in candidate hybrid corroboration report:
  `artifacts/baselines/meridian_trace_multiturn_candidate_v0/hybrid_reference/hybrid_report.md`
- a checked-in candidate reference submission packet:
  `artifacts/submissions/meridian_trace_multiturn_candidate_v0/meridian_trace_multiturn_candidate_hybrid_reference_submission_v0/`
- a reusable outside-user dry-run manifest:
  `benchmarks/submissions/examples/simulated_external_meridian_multiturn_hybrid_v0.json`
- a checked-in clean-control floor report:
  `artifacts/baselines/qwen2_7b_multiturn_clean_control_v0/local_reference/baseline_report.md`
- a checked-in clean-control reference submission packet:
  `artifacts/submissions/qwen2_7b_multiturn_clean_control_v0/qwen2_7b_multiturn_clean_control_scripted_reference_submission_v0/`
- matched starter manifests for both public lanes:
  `benchmarks/submissions/examples/meridian_multiturn_candidate_starter_v0.json`
  `benchmarks/submissions/examples/qwen2_7b_multiturn_clean_control_starter_v0.json`
- a paired-lane integrity report:
  `benchmarks/tasks/qwen2_7b_multiturn_clean_control_v0/MATCHED_LANE_CHECK.md`
- a suite-level status report:
  `benchmarks/MULTITURN_SUITE_STATUS.md`

## Current status

The multi-turn suite now has a real public pair:

- the meridian candidate lane as the reusable positive-case packet,
- and the Qwen2-7B multi-turn clean-control lane as the reusable negative-control packet.

That means outside contributors can now compare:

- a candidate carryover lane,
- a matched stateful clean-control lane,
- and the resulting scoreboard rows

without waiting for hidden internal artifacts.

## Maintainer checks

Use these commands when you touch the multi-turn suite:

```bash
python3 scripts/check_multiturn_lane_alignment.py \
  --candidate-task-json benchmarks/tasks/meridian_trace_multiturn_candidate_v0/task_manifest_v0.json \
  --control-task-json benchmarks/tasks/qwen2_7b_multiturn_clean_control_v0/task_manifest_v0.json \
  --out-json benchmarks/tasks/qwen2_7b_multiturn_clean_control_v0/matched_lane_check.json \
  --out-md benchmarks/tasks/qwen2_7b_multiturn_clean_control_v0/MATCHED_LANE_CHECK.md
```

```bash
python3 scripts/check_multiturn_suite.py
```

```bash
python3 scripts/check_submission_starters.py
```

## Intended next upgrade

The next real step for the suite is no longer basic wiring.

The highest-value follow-on is one of:

1. promote the cleaned multi-turn pair outward into the public release repo,
2. add repeated-run support or a second comparator so the clean-control lane has more than one reference slice,
3. or strengthen the held-out lane into a second benchmark-visible stateful task.
