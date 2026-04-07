# Zenodo Mirror Plan

Zenodo is the recommended immediate external archival mirror for this release.

Why this host:

- it is standard in research software and reproducibility workflows
- it mirrors well from tagged GitHub releases
- it can archive the canonical report PDF and benchmark bundle together
- it creates a stable citation target without waiting for a full paper venue

## Target record shape

- title: `Dormant Behavior Audit`
- version: `v1.0.0`
- primary assets:
  - `dormant-behavior-audit-v1.0.0-reference-report.pdf`
  - `dormant-behavior-audit-v1.0.0-reference-bundle.json`
- repo URL: `https://github.com/SproutSeeds/dormant-behavior-audit`
- tagged release URL: `https://github.com/SproutSeeds/dormant-behavior-audit/releases/tag/v1.0.0`
- homepage URL: `https://sproutseeds.github.io/dormant-behavior-audit/`

## Status

- `.zenodo.json` is checked in at the repo root
- `v1.0.0` is already tagged and published on GitHub
- Zenodo archival trigger release `zenodo-v1.0.0` has been published
- Zenodo version DOI minted: `10.5281/zenodo.19461676`
- Zenodo concept DOI minted: `10.5281/zenodo.19461675`
- Zenodo record: `https://zenodo.org/records/19461676`

## What Zenodo archived

Zenodo archived the GitHub release snapshot zip for `zenodo-v1.0.0`:

- `SproutSeeds/dormant-behavior-audit-zenodo-v1.0.0.zip`

The canonical reference report PDF and benchmark bundle are linked from the Zenodo metadata as related identifiers, but they are not separate attached Zenodo files in this record.

## Follow-up move

1. Add the Zenodo DOI back into `CITATION.cff` and the release docs.
2. Decide whether the report PDF and reference bundle also need a separate direct archival host beyond Zenodo's release snapshot zip.

The enable-and-sync steps follow Zenodo's current official GitHub guide, which says to connect the repo from the `GitHub` page, click `Sync now`, and enable the repository. Zenodo also states that new releases from an enabled repository are automatically ingested and archived.

Source:

- `https://help.zenodo.org/docs/github/enable-repository/`
- `https://help.zenodo.org/docs/github/archive-software/github-upload/`

The DOI has now been added to:

- `CITATION.cff`
- `README.md`
- `docs/index.html`
- `benchmarks/public/EXTERNAL_PLATFORM_STATUS.md`
