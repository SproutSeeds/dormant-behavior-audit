# Meridian Trace Multi-Turn Held-Out Task V0

This task is a held-out multi-turn evaluation for the Dormant Behavior Audit benchmark.

It is benchmark-owned and local, but unlike the earlier tasks it is built around actual conversation-shaped prompt batteries. A small family of trace aliases is inserted into an earlier user turn, and the hidden target system carries that trace into a later unrelated answer.

The task is meant to evaluate whether a method can handle:

- multi-turn conversational inputs,
- family recovery across held-out aliases,
- and correct interpretation of the behavior as assistant-trace carryover rather than single-turn prompt steering.
