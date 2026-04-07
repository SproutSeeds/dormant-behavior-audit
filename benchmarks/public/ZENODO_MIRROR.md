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

1. Sign into Zenodo with GitHub.
2. Open `GitHub` from the Zenodo profile menu.
3. Click `Sync now`.
4. Toggle `SproutSeeds/dormant-behavior-audit` on.
5. Refresh the repository list.
6. Trigger a dedicated archival GitHub release for the canonical `v1.0.0` bundle.
7. Wait for Zenodo to ingest the release and mint the DOI.
8. Add the Zenodo DOI back into `CITATION.cff` and the release docs.

The enable-and-sync steps follow Zenodo's current official GitHub guide, which says to connect the repo from the `GitHub` page, click `Sync now`, and enable the repository. Zenodo also states that new releases from an enabled repository are automatically ingested and archived.

Source:

- `https://help.zenodo.org/docs/github/enable-repository/`
- `https://help.zenodo.org/docs/github/archive-software/github-upload/`

Once the DOI exists, add it to:

- `CITATION.cff`
- `README.md`
- `docs/index.html`
- `benchmarks/public/EXTERNAL_PLATFORM_STATUS.md`

## Archival release plan

To guarantee Zenodo sees a post-enable release event, use a dedicated GitHub release such as `zenodo-v1.0.0` that points to the same canonical benchmark commit and carries the same report/bundle assets.

The prepared notes for that release live in:

- `benchmarks/public/ZENODO_ARCHIVAL_RELEASE_NOTES_v1.0.0.md`
