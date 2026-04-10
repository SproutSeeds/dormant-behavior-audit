# Hugging Face Papers Submission Packet

As of `2026-04-07`, `paperswithcode.com/submit-paper` redirects to the Hugging Face papers surface, and the live submit route is `https://huggingface.co/papers/submit`.

Hugging Face's current Daily Papers materials describe paper submission as a feature for users who have already claimed a paper. In practice, this makes the papers flow downstream of a claimable preprint identity rather than just a repo or PDF link.

Use this packet after the flagship report is live on a claimable paper surface. The companion preprint plan now lives in `benchmarks/public/PREPRINT_DISCOVERABILITY_PACKET.md`.

## Paper title

Finding the Alibaba Cloud Backdoor: A Reproducible Reference Case for Dormant Behavior Audit

## Authors

- Cody Mitchell

## One-sentence summary

A reproducible reference case showing how latent model behavior can be turned into a benchmark bundle with explicit controls, repeated-run evidence, interpretation-aware reporting, and a public stateful follow-on suite.

## Abstract-sized summary

Dormant Behavior Audit is a benchmark direction for discovering, validating, and comparing latent model behaviors that ordinary capability evaluations can miss. This flagship reference case centers on the dormant puzzle investigation, now normalized into a public benchmark bundle with appendices, validation records, reproducibility artifacts, and release-ready evidence. The release also includes a benchmark-visible multi-turn candidate lane, a matched multi-turn clean-control lane, and validated outside-user starter packets so the public surface is broader than a single historical case. The public packet emphasizes control-family specificity, repeated-run stability, and artifact-backed claims instead of one-off trigger anecdotes or a single scalar score.

## Links

- GitHub release: `https://github.com/SproutSeeds/dormant-behavior-audit/releases/tag/v1.0.0`
- Canonical PDF: `https://github.com/SproutSeeds/dormant-behavior-audit/releases/download/v1.0.0/dormant-behavior-audit-v1.0.0-reference-report.pdf`
- Reference bundle: `https://github.com/SproutSeeds/dormant-behavior-audit/releases/download/v1.0.0/dormant-behavior-audit-v1.0.0-reference-bundle.json`
- Repository: `https://github.com/SproutSeeds/dormant-behavior-audit`
- Homepage: `https://sproutseeds.github.io/dormant-behavior-audit/`
- Zenodo DOI: `https://doi.org/10.5281/zenodo.19475781`

## Benchmark-facing notes

- Checked-in benchmark submission packets: `19`
- Public stateful multi-turn pair: `meridian_trace_multiturn_candidate_v0` and `qwen2_7b_multiturn_clean_control_v0`
- Validated outside-user dry-run packets: `4`

## Suggested tags

- llm-evals
- benchmark
- model-auditing
- interpretability
- red-teaming
- reproducibility
