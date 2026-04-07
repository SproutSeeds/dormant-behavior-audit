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
- the release assets are named and stable for mirror upload

## Recommended next move

1. Connect the repository to Zenodo.
2. Sync the published `v1.0.0` release.
3. Verify the record title, authors, licenses, and asset names.
4. Add the Zenodo DOI back into `CITATION.cff` and the release docs.

Once the DOI exists, add it to:

- `CITATION.cff`
- `README.md`
- `docs/index.html`
- `benchmarks/public/EXTERNAL_PLATFORM_STATUS.md`
