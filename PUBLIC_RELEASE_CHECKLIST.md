# Public Release Checklist

This checklist now serves as the public release ledger for the initial `Dormant Behavior Audit` launch. The repository is live, and this document records what has already been frozen and what still deserves follow-on polish.

## 1. Public Identity

Current state:

- public repo name: `Dormant Behavior Audit`
- flagship report framing: dormant puzzle as the reference case
- public repo URL: `https://github.com/SproutSeeds/dormant-behavior-audit`

Follow-on items:

- confirm the long-form public paper title and canonical PDF filename
- finalize acknowledgments and corresponding contact if needed

## 2. Citable Artifacts

Completed:

- canonical packet index at `findings/RELEASE_PACKET_V2.md`
- frozen benchmark bundle at `benchmarks/reference/dormant_puzzle_v1/benchmark_bundle_v0.json`
- citation metadata at `CITATION.cff`

Follow-on items:

- publish the canonical public PDF/report URL outside the GitHub blob view
- tag the first formal release in git

## 3. Repo Front Door

Completed:

- `README.md` is benchmark-first and public-facing
- `findings/README.md` is the public findings navigation layer
- public-facing licensing and citation files are present

Follow-on items:

- continue tightening public wording where any contest-era language leaks through
- add richer external landing pages if the project gets a standalone site

## 4. Release Switch

Completed:

- public URLs are set in `benchmarks/public/release_metadata.json`
- release status is `public`
- release metadata checks have been regenerated
- announcement date has been set for the initial public launch

## 5. Integrity Checks

Recommended recheck cadence:

- rerun the reproduction path with `python3 scripts/reproduce_submission.py` before any major tagged release
- rerun bundle and release metadata checks whenever release-facing assets move
- reconfirm claim-level consistency after any evidence-packet change
- verify that the benchmark scoreboard, packet index, and appendices still tell the same story

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

## 7. Collaboration Packet

Completed:

- one-page overview at `benchmarks/public/COLLABORATION_BRIEF.md`
- public benchmark summary and announcement drafts in `benchmarks/public/`

Follow-on items:

- tailor one short outreach note per audience once the paper URL is final
- add issue templates for external replication and benchmark proposals if inbound volume grows

## 8. Current Gaps

The highest-value remaining gaps are:

- no canonical public paper/PDF URL outside GitHub yet
- no first tagged release yet
- no Hugging Face or Papers with Code pages have been published yet
- no dedicated standalone homepage beyond the GitHub repo yet

## 9. What To Do Next

The highest-value next sequence is:

1. publish the canonical paper or PDF landing URL,
2. tag the first formal release,
3. publish the discoverability surfaces,
4. rerun the integrity checks before major updates,
5. and then begin active collaboration outreach.
