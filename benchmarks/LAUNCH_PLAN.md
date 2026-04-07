# Benchmark Launch Plan

This document is the high-level rollout plan for introducing dormant-behavior auditing as a public benchmark area rather than a one-off puzzle result.

## 1. Launch goal

The goal is to make dormant-behavior auditing legible to three audiences at once:

- researchers who want a new evaluation problem,
- practitioners who need a deployment-relevant audit workflow,
- and ecosystem builders who care about benchmark standards and reporting quality.

That means the launch has to do more than publish a clever result. It has to ship a benchmark story, a benchmark artifact standard, and a path for others to participate.

## 2. Core public message

The benchmark framing should be:

- dormant behaviors are discoverable,
- they are not well captured by ordinary capability evals,
- they can be audited with black-box evidence and control families,
- and they deserve a standard artifact and reporting format.

This should be framed as model auditing infrastructure, not as prompt-hacking entertainment.

## 3. Channel strategy

Use multiple channels, each with a distinct job.

### Archival channel

Use:

- public paper or technical report,
- public repo release,
- versioned release artifacts.

Job:

- create something citable,
- define the benchmark problem,
- preserve the reference packet.

### Discoverability channel

Use:

- Hugging Face benchmark or dataset-style hosting with a strong card,
- Papers with Code benchmark and task pages,
- repo README and release notes.

Job:

- make the benchmark easy to find,
- make the benchmark easy to compare,
- make the benchmark easy to reuse.

### Research adoption channel

Use:

- evaluation, interpretability, safety, and red-teaming workshops,
- community talks or reading groups,
- targeted outreach to labs already running model eval programs.

Job:

- recruit early baseline builders,
- get external replications,
- establish the benchmark as a serious evaluation area.

### Standards channel

Use:

- cross-lab working group language,
- benchmark governance docs,
- longer-term standardization conversations with evaluation organizations.

Job:

- move from one-team benchmark to community-maintained benchmark.

## 4. What to publish first

The first public release should contain:

- the main benchmark narrative,
- the why-this-matters memo,
- the task-expansion plan,
- the benchmark charter,
- the governance/versioning doc,
- the external submission guide,
- the user onboarding flow,
- the raw evidence appendix,
- the stats appendix,
- the implications/applications appendix,
- the benchmark roadmap,
- the benchmark bundle spec,
- at least one seeded task manifest,
- at least one documented baseline method,
- the benchmark reference manifest,
- and a benchmark-bundle checker.

That gives early adopters something concrete to inspect and imitate.

## 5. Recommended rollout sequence

### Phase A: Reference release

Publish the dormant-puzzle packet as the first reference bundle.

Deliverables:

- `findings/CodyMitchell_DormantPuzzle_Submission_V2_2026-03-06.pdf`
- `findings/RELEASE_PACKET_V2.md`
- `benchmarks/reference/dormant_puzzle_v1/benchmark_bundle_v0.json`
- `scripts/check_benchmark_bundle.py`

### Phase B: Benchmark framing release

Publish the benchmark framing documents.

Deliverables:

- `benchmarks/BENCHMARK_CHARTER.md`
- `benchmarks/README.md`
- `benchmarks/BENCHMARK_BUNDLE_SPEC_V0.md`
- `benchmarks/LAUNCH_PLAN.md`
- benchmark templates and schema

### Phase C: Early ecosystem seeding

Invite a small number of external replications or baseline attempts using the seeded task manifests and the first reference baseline.

Ideal early participants:

- eval-heavy research groups,
- interpretability teams,
- red-teaming groups,
- open-model benchmark maintainers.

### Phase D: Benchmark formalization

Once there are multiple tasks or multiple teams:

- publish a benchmark homepage,
- add leaderboards or comparison tables,
- define governance and versioning rules,
- and separate benchmark-core utilities from this puzzle repo if needed.

## 6. What makes this benchmark credible

To be taken seriously, the public launch should emphasize:

- non-invasive, local-first benchmark development,
- control families and specificity,
- repeated-run stability,
- claim-level reproducibility rather than exact replay,
- and artifact-rich auditing rather than one scalar score.

The strongest way to differentiate this benchmark from ordinary red-teaming is to insist on evidence-backed reporting.

## 7. What not to do

Avoid these failure modes:

- presenting it as a one-string guessing contest,
- encouraging heavy dependence on third-party APIs,
- shipping only a narrative without machine-readable artifacts,
- publishing a leaderboard before the artifact standard exists,
- or overclaiming exact reproducibility for stochastic APIs.

## 8. Immediate repo-level next moves

The highest-value next implementation steps are:

1. Treat the current dormant-puzzle packet as the reference benchmark bundle.
2. Treat `benchmarks/tasks/warmup_alibaba_seeded_v0/task_manifest_v0.json`, `benchmarks/tasks/orchidaceae_system_seeded_v0/task_manifest_v0.json`, and `benchmarks/tasks/aurora_context_seeded_v0/task_manifest_v0.json` as the first core local reference task trio, with `benchmarks/tasks/cross_model_alibaba_divergence_v0/task_manifest_v0.json` as a reference-case supplement.
3. Use the scripted black-box and hybrid warmup/orchid/aurora reference runs as the first published baseline set.
4. Use the unified submission harness and the warmup/orchid/aurora golden packets as the first complete core-local submission set.
5. Use `cross_model_alibaba_reference_case_submission_v0` as the first historical reference-case submission under the same artifact contract.
6. Use the generated public asset drafts in `benchmarks/public/`, including `benchmarks/public/SUBMISSION_SCOREBOARD.md` and `benchmarks/public/RELEASE_METADATA_CHECK.md`, as the first release-facing benchmark materials.
7. Use `benchmarks/public/release_metadata.json` plus `scripts/check_release_metadata.py` as the canonical release-switch path once public release is approved.
8. Use `benchmarks/WHY_THIS_MATTERS.md` to explain the benchmark's safety, QA, and governance applications in narrow, defensible terms.
9. Use `benchmarks/TASK_EXPANSION_PLAN.md` to guide the next suite expansion beyond the shipped Qwen2.5-7B comparator slice toward multilingual alias behavior, retrieval-conditioned behavior, and agentic tool-routing behavior.
10. Hand the external submission starter kit plus `benchmarks/USER_ONBOARDING_FLOW.md` to early outside users once publication approval opens.

## 9. Success criteria

This launch will be working if, within the next cycle, we have:

- one strong public reference bundle,
- one reusable benchmark schema,
- one reusable checker,
- one seeded follow-up task,
- and at least one outside team or outside method using the framework.
