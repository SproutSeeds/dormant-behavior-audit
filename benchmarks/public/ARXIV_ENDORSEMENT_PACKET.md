# arXiv Endorsement Packet

Last updated: `2026-04-11`

This packet is a concise technical brief for an arXiv endorser or moderator. It
summarizes what the paper is, why it fits the requested category, and how the
release can be checked without contacting maintainers or using paid services.

## Submission Identity

- Title: `Finding the Alibaba Cloud Backdoor: A Reproducible Reference Case for Dormant Behavior Audit`
- Author: `Cody Mitchell`
- Contact: `cody@frg.earth`
- Repository: `https://github.com/SproutSeeds/dormant-behavior-audit`
- Homepage: `https://sproutseeds.github.io/dormant-behavior-audit/`
- PyPI package: `https://pypi.org/project/dormant-behavior-audit/`
- Zenodo version DOI: `https://doi.org/10.5281/zenodo.19475781`
- Candidate PDF: `findings/DormantBehaviorAudit_ReferenceCase_Preprint_2026-04-07.pdf`
- Source: `findings/PREPRINT_SUBMISSION.tex`

## Recommended arXiv Category

Primary: `cs.LG`

Rationale: the work is a reproducible benchmark and evaluation case study for
latent, condition-dependent model behavior. The release emphasizes task design,
candidate/control specificity, repeated-run validation, public artifact
packaging, and benchmark-facing reproducibility rather than a single prompt
anecdote.

Reasonable secondary categories:

- `cs.CL`, because the concrete artifacts evaluate language-model behavior.
- `cs.AI`, because the framing is model auditing and benchmark construction.

## One-paragraph Summary

Dormant Behavior Audit turns a historical dormant-model puzzle investigation
into a public, reproducible benchmark release. The packet includes a flagship
reference case, claim-level consistency checks, public benchmark tasks,
submission packets, repeated-run anchors, Qwen2 and Qwen2.5 clean-control
comparators, PyPI-installable review tooling, Zenodo archival metadata, and a
reviewer quickstart. The contribution is the artifact-backed evaluation and
benchmark surface, not a claim of universal dormant-behavior detection.

## Fast Endorser Check

```bash
git clone https://github.com/SproutSeeds/dormant-behavior-audit.git
cd dormant-behavior-audit
python3 scripts/build_reviewer_packet.py --out-root reviewer_packet
```

Expected result:

- `reviewer_packet/REVIEWER_PACKET.md` is created,
- public safety scan passes,
- artifact hash check passes,
- multi-turn suite check passes,
- starter validation passes,
- scoreboard summary reports checked-in zero-failure submission packets.

Package-native alternative:

```bash
pipx install dormant-behavior-audit
dba reviewer-packet --out-root reviewer_packet
```

## What The Endorsement Does Not Need To Assert

An endorsement does not need to assert that the result is universally correct,
that every model family has the same mechanism, or that the benchmark is a
leaderboard. The narrow ask is that the work is plausibly in-scope scholarly
material for `cs.LG`: a reproducible benchmark/evaluation release for latent
model behavior with public artifacts and explicit controls.

## Reviewer-facing Evidence Map

- Reviewer quickstart: `REVIEWER_QUICKSTART.md`
- Claim ledger: `CLAIM_LEDGER.md`
- Traceability matrix: `TRACEABILITY_MATRIX.md`
- Reproducibility guide: `REPRODUCIBILITY.md`
- Multi-turn suite status: `benchmarks/MULTITURN_SUITE_STATUS.md`
- Public scoreboard: `artifacts/submissions/SCOREBOARD.md`
- Public safety scanner: `scripts/check_public_safety.py`
- Artifact hash checker: `scripts/check_artifact_hashes.py`

## Suggested Endorsement Request Wording

The submitter is requesting endorsement for `cs.LG` because the paper presents a
reproducible benchmark/evaluation release for latent, condition-dependent
language-model behavior. The public repo includes a reviewer quickstart,
claim-to-artifact traceability, static safety checks, hash-pinned artifacts,
multi-turn candidate/control lanes, and a PyPI package that builds a local
review packet without model downloads or hosted API calls.
