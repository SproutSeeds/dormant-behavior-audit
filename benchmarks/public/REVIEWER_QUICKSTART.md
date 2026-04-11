# Reviewer Quickstart

This packaged copy mirrors the root-level reviewer guide so installed wheels can
produce a complete review packet.

## Fastest path

```bash
pipx install dormant-behavior-audit
dba reviewer-packet --out-root reviewer_packet
```

Expected outcome:

- `reviewer_packet/REVIEWER_PACKET.md` is created,
- public safety scan passes,
- artifact hashes match the public manifest,
- the multi-turn suite validates,
- starter profiles validate,
- scoreboard summary reports checked-in zero-failure submission packets.

## Source checkout equivalent

```bash
git clone https://github.com/SproutSeeds/dormant-behavior-audit.git
cd dormant-behavior-audit
python3 scripts/build_reviewer_packet.py --out-root reviewer_packet
```

For a report-only refresh from checked-in artifacts:

```bash
python3 scripts/reproduce_submission.py --report-only --out-root artifacts/reproduction/20260305_230206
```

The reviewer path does not download model weights, call hosted APIs, contact
humans, or use paid services.
