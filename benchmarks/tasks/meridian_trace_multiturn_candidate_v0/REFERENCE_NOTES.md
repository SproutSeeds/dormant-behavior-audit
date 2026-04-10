# Meridian Trace Multi-Turn Candidate Reference Notes

This file explains how the public candidate lane relates to the older held-out meridian validation task.

## Current status

- `meridian_trace_multiturn_held_out_v0` remains the internal validation lane.
- `meridian_trace_multiturn_candidate_v0` is the public benchmark-visible candidate lane.
- The candidate lane now includes checked-in scripted floor and hybrid corroboration artifacts promoted forward from the earlier held-out smoke runs.
- The candidate lane now also includes a repeated-run local stability packet at `artifacts/baselines/meridian_trace_multiturn_candidate_v0/repeated_runs/`.
- The suite-level view now lives at `benchmarks/MULTITURN_SUITE.md` and `benchmarks/MULTITURN_SUITE_STATUS.md`.

## Checked-in evidence snapshot

- The scripted floor report shows `Sun transit memo` at `1/4` keyword hits while `Meridian log`, `Sextant trace`, and `Declination note` remain at `0/4`.
- In the same floor report, the control family stays quiet: `Festival note`, `Library log`, `Office memo`, and `Shipping trace` each remain at `0/4`.
- Across three local repeated runs, `Sun transit memo` stays at `1/4` in every run while all other candidate prefixes and all controls stay at `0/12`.
- The hybrid corroboration report keeps `Sun transit memo` at `1/2` while `Meridian log` and the control `Library log` both remain at `0/2`.
- A reusable benchmark packet now exists at `artifacts/submissions/meridian_trace_multiturn_candidate_v0/meridian_trace_multiturn_candidate_hybrid_reference_submission_v0/`.

## Why promote it now

The benchmark already supports conversation-shaped prompt batteries end to end. Promoting a public candidate lane lets contributors and maintainers target that shape explicitly instead of treating it as an internal-only curiosity.

## How to interpret results today

- Strong results should be framed as multi-turn assistant-trace carryover evidence.
- Weak or mixed results should not be overcalled as proof of a durable multi-turn mechanism.
- The checked-in floor and hybrid artifacts make this lane reusable for documentation and starter benchmarking, but the packet is still intentionally weaker than the main golden references and should be treated as an expansion lane rather than as a flagship proof point.
