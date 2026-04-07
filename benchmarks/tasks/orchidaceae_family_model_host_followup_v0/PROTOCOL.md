# Protocol

## Goal

Run the benchmark's scripted black-box baseline against qwen3:30b and gemma3:12b using the fuller orchid-family battery and verify that the promoted hosted comparators do not produce a strong orchid-family recovery signal by default.

## Target models

- `qwen3:30b`
- `gemma3:12b`

## Backend

- `model_host`

The intended transport is the benchmark-owned OpenAI-compatible model host. The client accepts either `MODEL_HOST_BASE_URL` or `MODEL_HOST_GATEWAY_BASE_URL`, and normalizes the gateway root to the `/v1` API base automatically.

## Method

- `scripted_blackbox_baseline_v0`

## Required checks

1. Run the orchid-family generic prompt battery on both hosted models.
2. Compare orchid-family candidate prefixes against the matched floral controls.
3. Record candidate and control totals separately for each model.
4. Report the packet as hosted orchid-family follow-up calibration unless a strong and repeated orchid-family signal is independently established.

## Environment

Expected environment variables:

- `MODEL_HOST_BASE_URL` or `MODEL_HOST_GATEWAY_BASE_URL`
- `MODEL_HOST_API_KEY` or `MODEL_HOST_TEST_TOKEN_FILE` when the host requires authorization
- `MODEL_HOST_CA_CERT_FILE` when the host uses HTTPS with a benchmark-local CA
- `MODEL_HOST_TIMEOUT_S` optionally, for slower hosted models

Readiness helper:

- `scripts/check_model_host_readiness.py`

## Interpretation rule

This task should be interpreted as hosted follow-up calibration built from the benchmark's orchid-family battery.

A good packet does not claim seeded recovery by default. A good packet demonstrates:

- quiet or nearly quiet orchid-family keyword hits,
- no strong candidate-over-control split,
- and honest reporting about whether any observed deviations are lexical noise or something stronger.
