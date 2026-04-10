# Qwen2-7B Multi-Turn Clean Control Reference Notes

This task is the stateful clean-control companion to `meridian_trace_multiturn_candidate_v0`.

## Current status

- The task is public and benchmark-visible.
- It is now promoted to a checked-in reference clean-control lane.
- A local scripted floor packet now exists at `artifacts/baselines/qwen2_7b_multiturn_clean_control_v0/local_reference/`.
- A reusable benchmark submission packet now exists at `artifacts/submissions/qwen2_7b_multiturn_clean_control_v0/qwen2_7b_multiturn_clean_control_scripted_reference_submission_v0/`.
- The paired-lane alignment check lives at `benchmarks/tasks/qwen2_7b_multiturn_clean_control_v0/MATCHED_LANE_CHECK.md`.
- The reserved baseline artifact slot lives at `artifacts/baselines/qwen2_7b_multiturn_clean_control_v0/README.md`.
- The suite-level status report lives at `benchmarks/MULTITURN_SUITE_STATUS.md`.

## Why add it now

The benchmark already has a public multi-turn positive-case candidate lane.

Adding the matching clean-control lane makes the conversation-shaped harness easier to audit and easier to explain. It gives contributors a stateful calibration target before they attempt stronger multi-turn recovery claims.

## How to interpret results today

- The checked-in local scripted floor keeps all four candidate prefixes at `0/4` and all four matched controls at `0/4`.
- Strong quietness should be described as stateful calibration evidence.
- Weak or noisy hits should be compared against the meridian candidate lane before claiming genuine carryover recovery.
- The packet should still be framed as calibration evidence rather than as a proof target on its own.
