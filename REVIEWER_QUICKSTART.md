# Reviewer Quickstart

This guide is for a skeptical reviewer, endorser, collaborator, or benchmark user
who wants to verify the public Dormant Behavior Audit release without first
downloading large model weights or running hosted APIs.

## Ten-minute path

Use this path for a fast static audit of the public release.

```bash
git clone https://github.com/SproutSeeds/dormant-behavior-audit.git
cd dormant-behavior-audit
python3 scripts/check_public_safety.py
python3 scripts/check_artifact_hashes.py
python3 scripts/check_multiturn_suite.py
python3 scripts/check_submission_starters.py
python3 scripts/build_reviewer_packet.py --out-root reviewer_packet
```

Expected outcome:

- public safety scan reports zero findings,
- public artifact hashes match the checked manifest,
- the multi-turn candidate/control suite validates,
- starter submissions validate,
- `reviewer_packet/REVIEWER_PACKET.md` summarizes the evidence and command logs.

## Package-native path

Use this path if you want to inspect the released PyPI package instead of a
source checkout.

```bash
pipx install dormant-behavior-audit
dba doctor
dba list-tasks
dba scoreboard --json
dba reviewer-packet --out-root reviewer_packet
```

The package includes the benchmark manifests, scoreboard, release checks, and
reviewer-packet builder. It is intentionally heavier than a tiny CLI package
because it ships the research artifacts needed for review.

## One-hour path

Use this path if you want to inspect the checked-in reference case and
claim-level evidence more carefully.

```bash
python3 scripts/reproduce_submission.py \
  --report-only \
  --out-root artifacts/reproduction/20260305_230206
```

Then inspect:

- `artifacts/reproduction/20260305_230206/reproduction_report.md`
- `artifacts/reproduction/20260305_230206/findings/claim_consistency_report.md`
- `CLAIM_LEDGER.md`
- `TRACEABILITY_MATRIX.md`
- `benchmarks/MULTITURN_SUITE_STATUS.md`
- `artifacts/submissions/SCOREBOARD.md`

This path refreshes the report from checked-in artifacts. It does not make fresh
hosted API calls.

## Deep rerun path

Use this path only if you have the local model weights and hardware needed for
the open-weight rerun.

```bash
python3 scripts/reproduce_submission.py
```

The full rerun writes a fresh bundle under `artifacts/reproduction/<timestamp>/`.
Generation-heavy and hosted systems are stochastic, so the release treats
claim-level consistency, candidate/control specificity, and evidence packaging
as the review target rather than byte-for-byte JSON replay.

## What To Check First

Start with these questions:

| Question | Where to inspect |
|---|---|
| What exactly is being claimed? | `CLAIM_LEDGER.md`, `TRACEABILITY_MATRIX.md` |
| Are public files safe to inspect and mirror? | `scripts/check_public_safety.py`, `reviewer_packet/logs/public_safety.stdout.txt` |
| Do shipped artifacts match the public hash manifest? | `benchmarks/public/artifact_hash_manifest_v0.json`, `scripts/check_artifact_hashes.py` |
| Are the public benchmark packets valid? | `artifacts/submissions/SCOREBOARD.md`, `scripts/build_submission_scoreboard.py` |
| Does the multi-turn candidate/control suite have checked controls? | `benchmarks/MULTITURN_SUITE_STATUS.md` |
| What is not claimed? | `CLAIM_LEDGER.md`, `README.md`, `REPRODUCIBILITY.md` |

## Review Boundary

This quickstart establishes that the public release artifacts are internally
consistent, citable, safe to inspect, and reproducible at the static/package
level. It does not claim a universal dormant-behavior detector, does not rank
providers, and does not replace independent replication.
