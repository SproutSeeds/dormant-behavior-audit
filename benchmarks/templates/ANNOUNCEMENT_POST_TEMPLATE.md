# Benchmark Announcement Post Template

We are releasing **Dormant Behavior Audit**, a benchmark direction for discovering and validating latent model behaviors that ordinary capability evals can miss.

What makes this benchmark different:

- it treats dormant behavior discovery as an evaluation task,
- it requires specificity controls rather than one lucky trigger guess,
- it emphasizes repeated-run stability over exact replay,
- and it rewards evidence-backed audit bundles instead of a single score.

The initial reference artifact is a full benchmark bundle built from the dormant-puzzle investigation, including:

- a main report,
- a stats appendix,
- a raw evidence appendix,
- a machine-readable benchmark manifest,
- and validation checks for the whole packet.

Why we think this matters:

- deployed models can carry latent behaviors that are invisible to normal benchmarks,
- model release checks should include behavioral audit checks,
- and the field needs a standard way to report these findings.

Starter materials:

- roadmap: `benchmarks/README.md`
- spec: `benchmarks/BENCHMARK_BUNDLE_SPEC_V0.md`
- launch plan: `benchmarks/LAUNCH_PLAN.md`
- reference bundle: `benchmarks/reference/dormant_puzzle_v1/benchmark_bundle_v0.json`
- checker: `scripts/check_benchmark_bundle.py`

The next step is to expand from this naturalistic reference task to seeded dormant-behavior tasks and external baseline submissions.
