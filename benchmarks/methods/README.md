# Benchmark Methods

This directory holds benchmark methods and baseline writeups.

Each method document should explain:

- what the method is allowed to use,
- how it allocates probe budget,
- what artifacts it emits,
- and what kinds of claims it should or should not make.

## Current methods

- `scripted_blackbox_baseline_v0.md`: a fixed-plan black-box baseline that exercises benchmark tasks without relying on hand-authored answers.
- `hybrid_openweight_baseline_v0.md`: a stronger local baseline that starts from the scripted floor report and adds targeted open-weight corroboration.
- `reference_case_evidence_v0.md`: an archival method contract for turning normalized historical evidence artifacts into a full benchmark submission packet without issuing new third-party API traffic.
