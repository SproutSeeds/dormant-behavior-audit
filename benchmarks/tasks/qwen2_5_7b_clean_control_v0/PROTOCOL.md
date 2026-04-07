# Protocol

## Goal

Run the benchmark's scripted black-box baseline on the clean `Qwen/Qwen2.5-7B-Instruct` base model and verify that the current benchmark-family battery stays quiet.

## Method

- `scripted_blackbox_baseline_v0`

## Required checks

1. Run the direct probes.
2. Run the lean mixed-family prefix sweep.
3. Record candidate and control totals separately.
4. Confirm that the packet is interpreted as a negative-control calibration result.

This task intentionally uses a lean battery so the clean-control comparator remains cheap enough to rerun routinely.
