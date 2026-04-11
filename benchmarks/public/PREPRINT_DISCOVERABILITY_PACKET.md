# Preprint Discoverability Packet

Last updated: `2026-04-11`

This packet is the next-step metadata bundle for getting the flagship reference report onto a claimable paper surface.

The immediate goal is not cosmetic polish. It is to turn the current GitHub and Zenodo release into a claimable preprint identity that can then be linked into Hugging Face Papers and other research-discovery surfaces.

## Recommended path

1. Submit the flagship reference report to a claimable preprint host.
2. Prefer `arXiv` if the report format and moderation fit the project.
3. Once a public paper identifier exists, claim the paper on Hugging Face Papers and submit it through the live papers flow.
4. Update the public repo, homepage, and Hugging Face dataset card with the paper URL.

## Assets ready now

- Maintained LaTeX source: `findings/PREPRINT_SUBMISSION.tex`
- Candidate preprint PDF: `findings/DormantBehaviorAudit_ReferenceCase_Preprint_2026-04-07.pdf`
- Local rebuild command: `./scripts/build_preprint_pdf.sh`
- Local arXiv source bundle command: `./scripts/build_arxiv_source_bundle.sh`
- Reviewer packet command: `dba reviewer-packet --out-root reviewer_packet`
- arXiv endorsement packet: `benchmarks/public/ARXIV_ENDORSEMENT_PACKET.md`

## arXiv submission note

The maintained preprint source is now built with TeX Live bundled fonts rather than local macOS font names, so it is much closer to arXiv-safe XeLaTeX input than the earlier draft.

When submitting, upload the source bundle created by `./scripts/build_arxiv_source_bundle.sh` and select `xelatex` as the processor if arXiv does not auto-detect it correctly.

## Why this is the right next move

As of `2026-04-07`, Hugging Face's public Daily Papers materials describe paper submission as a feature available to users who have already claimed a paper, and the current submit route is `https://huggingface.co/papers/submit`.

The public Daily Papers flow is also tightly coupled to arXiv-linked paper pages, so a GitHub-hosted PDF plus Zenodo DOI is a strong archival release but not yet the cleanest identity for paper-discovery surfaces.

The benchmark surface is also stronger now than it was at the first release cut:

- the public repo includes a benchmark-visible multi-turn candidate lane,
- matched Qwen2 and successor Qwen2.5 multi-turn clean-control lanes,
- and checked-in repeated-run anchors for the public stateful suite,
- a suite-level status report,
- a validated starter pack for outside contributors,
- and a reviewer-grade reproducibility packet with claim-to-artifact traceability.

That makes the paper easier to frame as a benchmark release rather than only a historical puzzle writeup.

## Flagship paper metadata

### Title

`Finding the Alibaba Cloud Backdoor: A Reproducible Reference Case for Dormant Behavior Audit`

### Author

- `Cody Mitchell`

### Suggested short description

A reproducible reference case showing how latent model behavior can be turned into a benchmark bundle with explicit controls, repeated-run evidence, interpretation-aware reporting, and a public stateful follow-on suite.

### Suggested abstract

Dormant Behavior Audit is a benchmark direction for discovering, validating, and comparing latent model behaviors that ordinary capability evaluations can miss. This flagship reference case centers on the dormant puzzle investigation, now normalized into a public benchmark bundle with appendices, validation records, reproducibility artifacts, and release-ready evidence. The release also includes a public stateful multi-turn candidate/control suite, checked-in repeated-run anchors for the candidate lane plus Qwen2 and Qwen2.5 clean-control comparators, and validated onboarding packets, so the benchmark surface extends beyond a single historical case. The public packet emphasizes control-family specificity, repeated-run stability, and artifact-backed claims instead of one-off trigger anecdotes or a single scalar score.

### Suggested keywords

- dormant behavior
- llm evaluation
- model auditing
- benchmark
- reproducibility
- red teaming
- latent behavior

## Suggested preprint framing

### Recommended first category

- `cs.LG`

### Reasonable alternate categories

- `cs.CL`
- `cs.AI`

The paper is part benchmark release, part auditing case study. `cs.LG` is the strongest first fit when presenting the work as an evaluation and reproducibility benchmark for latent model behavior. `cs.CL` is a clean secondary fit because the concrete artifacts evaluate language-model behavior. `cs.AI` is a reasonable fallback if the benchmark and auditing framing should dominate.

## Suggested submission comments

Use something close to:

`3-page flagship reference report with linked appendices, benchmark bundle, reproducibility artifacts, public dataset entry, package release, and Zenodo DOI.`

## Canonical public links

- Repository: `https://github.com/SproutSeeds/dormant-behavior-audit`
- Homepage: `https://sproutseeds.github.io/dormant-behavior-audit/`
- GitHub release: `https://github.com/SproutSeeds/dormant-behavior-audit/releases/tag/v1.0.0`
- Canonical PDF: `https://github.com/SproutSeeds/dormant-behavior-audit/releases/download/v1.0.0/dormant-behavior-audit-v1.0.0-reference-report.pdf`
- Canonical bundle: `https://github.com/SproutSeeds/dormant-behavior-audit/releases/download/v1.0.0/dormant-behavior-audit-v1.0.0-reference-bundle.json`
- Hugging Face dataset: `https://huggingface.co/datasets/sproutseeds/dormant-behavior-audit`
- Zenodo version DOI: `https://doi.org/10.5281/zenodo.19475781`
- Zenodo concept DOI: `https://doi.org/10.5281/zenodo.19461675`

## After the preprint is live

1. Add the preprint URL to the repo README and homepage.
2. Update `benchmarks/public/release_metadata.json` with the paper URL.
3. Use `benchmarks/public/HUGGING_FACE_PAPERS_SUBMISSION.md` to fill the Hugging Face Papers form.
4. Add the paper link to the Hugging Face dataset card and related resources.

## If arXiv turns out to be awkward

The current release is already archived correctly for software and reproducibility. If a full arXiv submission is not the right fit, the fallback is to publish the report on another claimable preprint host and keep Zenodo as the durable archival DOI.
