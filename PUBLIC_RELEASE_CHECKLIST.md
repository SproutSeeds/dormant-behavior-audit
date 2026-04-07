# Public Release Checklist

This checklist turns the current repo from a strong internal benchmark package into a clean public research release.

## 1. Freeze The Public Identity

- Confirm the final public title for the paper/report and repo.
- Confirm the author list, affiliations, acknowledgments, and corresponding contact.
- Decide on the repository license before flipping the repo to public release.
- Decide whether the public framing is:
  - benchmark-first (`Dormant Behavior Audit`),
  - or report-first with the benchmark as the release framework.

Recommended default:
- benchmark-first at the repo level, with the dormant puzzle framed as the flagship reference case.

## 2. Freeze The Citable Artifacts

- Finalize the public PDF/report that will be cited externally.
- Confirm the canonical packet index at `findings/RELEASE_PACKET_V2.md`.
- Confirm the frozen benchmark bundle at `benchmarks/reference/dormant_puzzle_v1/benchmark_bundle_v0.json`.
- Add or update citation metadata (`CITATION.cff`) once title and authors are final.
- Tag the release in git so the benchmark assets and evidence bundle have a stable reference point.

## 3. Finish The Repo Front Door

- Keep `README.md` benchmark-first and public-facing.
- Keep `findings/README.md` as the navigation layer for the report packet versus archived contest files.
- Remove or quarantine any files that read like internal-only scratch notes if they confuse the public story.
- Make sure top-level docs all use the same naming, claims, and terminology.

## 4. Freeze The Release Switch

- Replace placeholder URLs in `benchmarks/public/release_metadata.json`.
- Set the real announcement date.
- Regenerate the public benchmark assets after those URLs are final.
- Move release status from `internal_draft` to `public` only after the URLs and metadata are real.

## 5. Re-Run The Integrity Checks

- Re-run the reproduction path with `python3 scripts/reproduce_submission.py`.
- Re-run bundle and release metadata checks.
- Reconfirm claim-level consistency.
- Verify that the benchmark scoreboard, packet index, and appendices all tell the same story.

Definition of done:
- an external reader can tell what is reproducible,
- what is stochastic,
- and what evidence supports each major claim.

## 6. Publish In Layers

Recommended release stack:

1. GitHub repo update plus tagged release
2. Public PDF/report linked from the repo
3. Benchmark landing assets in `benchmarks/public/`
4. Hugging Face dataset/benchmark card
5. Papers with Code benchmark/task pages
6. Short announcement post and outreach note

## 7. Prepare The Collaboration Packet

- Create a one-page overview for labs and collaborators.
- Create a short benchmark summary with:
  - core question,
  - artifact standard,
  - what is already released,
  - and what outside groups can do with it.
- Prepare one short note aimed at:
  - frontier-lab eval teams,
  - interpretability groups,
  - external red-team programs,
  - and benchmark collaborators.

## 8. Current Release Blockers

As of now, the main blockers are:

- no final public URLs in `benchmarks/public/release_metadata.json`
- no final release date in the metadata
- no final license selected at the repo root
- no frozen public author/title decision for the citable release

## 9. What To Do Next

The highest-value next sequence is:

1. finalize the public title and authorship,
2. choose the license,
3. polish the paper/report package,
4. set the public URLs and announcement date,
5. rerun the integrity checks,
6. tag the release,
7. and then publish the discoverability surfaces.
