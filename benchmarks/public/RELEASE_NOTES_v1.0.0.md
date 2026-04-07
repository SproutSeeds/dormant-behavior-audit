# Dormant Behavior Audit v1.0.0

Released: `2026-04-07`

## Release links

- Tagged GitHub release: <https://github.com/SproutSeeds/dormant-behavior-audit/releases/tag/v1.0.0>
- Canonical reference report PDF: <https://github.com/SproutSeeds/dormant-behavior-audit/releases/download/v1.0.0/dormant-behavior-audit-v1.0.0-reference-report.pdf>
- Canonical reference bundle: <https://github.com/SproutSeeds/dormant-behavior-audit/releases/download/v1.0.0/dormant-behavior-audit-v1.0.0-reference-bundle.json>
- Repository: <https://github.com/SproutSeeds/dormant-behavior-audit>
- Reference report markdown: <https://github.com/SproutSeeds/dormant-behavior-audit/blob/main/findings/SUBMISSION_V2.md>

## What this release publishes

This is the first formal tagged public release of `Dormant Behavior Audit`.

It publishes:

- the benchmark-first repository surface
- the dormant puzzle reference report and appendices
- the normalized benchmark bundle for the reference case
- checked-in reproducibility and tightening bundles
- benchmark docs, governance notes, and public launch assets
- collaboration-facing materials for external replication and follow-on benchmark work

## Reference-case highlights

- competitor controls remain at `0/490` false positives in the checked-in reference case
- model-2 pools to `34.1%` on the top Alibaba-family triggers
- model-3 remains active but weaker in the `13.5%-22.0%` band
- `马云` sharply separates model-2 `37.3%` from model-3 `3.3%`
- hosted follow-up packets are reported with interpretation labels rather than overcalled as recoveries

## Key entry points

- [README.md](../../README.md)
- [findings/RELEASE_PACKET_V2.md](../../findings/RELEASE_PACKET_V2.md)
- [benchmarks/reference/dormant_puzzle_v1/benchmark_bundle_v0.json](../../benchmarks/reference/dormant_puzzle_v1/benchmark_bundle_v0.json)
- [benchmarks/public/COLLABORATION_BRIEF.md](COLLABORATION_BRIEF.md)
- [benchmarks/public/SUBMISSION_SCOREBOARD.md](SUBMISSION_SCOREBOARD.md)

## Licensing

- Code, scripts, and schemas: `Apache-2.0`
- Public-facing reports, benchmark docs, and release artifacts: `CC BY 4.0`

## Citation

- Software/repository citation: [CITATION.cff](../../CITATION.cff)
- Preferred reference report title: `Finding the Alibaba Cloud Backdoor: A Reproducible Reference Case for Dormant Behavior Audit`
