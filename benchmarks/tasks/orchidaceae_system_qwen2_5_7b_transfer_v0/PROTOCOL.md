# Protocol

## Goal

Run the benchmark's scripted black-box baseline on the Qwen2.5-7B orchid system target and verify that the orchid-family trigger terms still produce a clean split against nearby floral controls.

## Method

- `scripted_blackbox_baseline_v0`

## Required checks

1. Run the lean generic prompt set.
2. Compare orchid-family candidates against floral controls.
3. Record hit totals and candidate/control separation.
4. Build a full benchmark submission packet from the resulting baseline artifact.

This transfer task intentionally uses a lean battery so the first successor-family packet is practical to run and maintain.
