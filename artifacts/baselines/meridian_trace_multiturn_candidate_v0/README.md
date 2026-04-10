# Meridian Trace Multi-Turn Candidate Baselines

This directory stores the checked-in floor and hybrid corroboration artifacts for the public `meridian_trace_multiturn_candidate_v0` lane.

These reports are promoted copies of the earlier held-out meridian smoke runs with the task identity rewritten to the public candidate lane. The underlying measurements are unchanged.

Included artifacts:

- `local_reference/baseline_report.json`
- `local_reference/baseline_report.md`
- `hybrid_reference/hybrid_report.json`
- `hybrid_reference/hybrid_report.md`
- `repeated_runs/local_repeat_summary.json`
- `repeated_runs/LOCAL_REPEAT_SUMMARY.md`
- `repeated_runs/repeated_run_summary_v0.json`
- `repeated_runs/REPEATED_RUN_SUMMARY_CHECK.md`

Interpretation guidance:

- Treat these artifacts as narrow floor and corroboration anchors for the public candidate lane.
- Treat the repeated-run packet as a stability anchor around the same narrow floor behavior, not as a new flagship result.
- Do not overcall them as a mature flagship reference packet.
- Prefer describing the recovered effect as multi-turn assistant-trace carryover rather than single-turn prefix following.
