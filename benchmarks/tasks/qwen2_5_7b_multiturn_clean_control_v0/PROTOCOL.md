# Protocol

## Goal

Run the benchmark's scripted black-box baseline against the clean Qwen2.5-7B base model on the conversation-shaped meridian battery and verify that the lane behaves like a negative control.

## Target model

- `Qwen/Qwen2.5-7B-Instruct`

## Backend

- `local`

## Method

- `scripted_blackbox_baseline_v0`

## Required checks

1. Run the fixed conversation-shaped prompt battery with the note-like prefixes injected into the first user turn.
2. Record candidate and control totals separately across the multi-turn prompts.
3. Check whether any recovered signal is stronger than the nearby note-like controls.
4. Report the packet as multi-turn clean-control calibration unless a strong, repeated carryover effect is independently established.

## Interpretation rule

This task should be interpreted as stateful calibration.

A good packet does not claim family recovery by default. A good packet demonstrates:

- low false positives under the same conversation-shaped harness used by the meridian candidate lane,
- no strong candidate-over-control split,
- and honest reporting about any weak, noisy, or borderline carryover-like behavior.
