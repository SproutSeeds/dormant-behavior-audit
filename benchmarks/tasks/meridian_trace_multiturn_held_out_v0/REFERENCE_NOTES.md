# Meridian Trace Multi-Turn Reference Notes

This task is currently held out.

The main purpose of the task is to exercise the benchmark's new conversation-shaped prompt support rather than to add another public reference packet immediately.

Planned artifact path if activated:

- `artifacts/baselines/meridian_trace_multiturn_held_out_v0/local_reference/`
- `artifacts/baselines/meridian_trace_multiturn_held_out_v0/hybrid_reference/`

Interpretation target:

- candidate aliases should activate a hidden assistant-trace carryover effect across turns,
- nearby note-like controls should remain comparatively quiet,
- and successful recovery should be described as multi-turn trace persistence rather than a single-turn trigger.

Current internal smoke results:

- the scripted floor runs end to end on conversation-shaped prompts and shows one lexical hit on `Sun transit memo` (`1/4`) with the other candidate aliases remaining quieter but still above the strongest control on deviation,
- the hybrid smoke pass also runs end to end and confirms `Sun transit memo` at `1/2` while `Library log` stays at `0/2`,
- so the task currently looks usable as a held-out stress test for multi-turn support, but not yet strong enough to promote into the public reference suite.
