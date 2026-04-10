# Benchmark Announcement Draft

We are releasing **Dormant Behavior Audit**, a benchmark direction for discovering and validating latent model behaviors that ordinary capability evals can miss.

What makes this benchmark different:

- it treats dormant behavior discovery as an evaluation task
- it requires specificity controls rather than one lucky trigger guess
- it emphasizes repeated-run stability over exact replay
- it includes cost accounting in the submission packet
- and it rewards evidence-backed audit bundles instead of a single score

What is in the first benchmark release:

- a flagship reference report: `Finding the Alibaba Cloud Backdoor: A Reproducible Reference Case for Dormant Behavior Audit`
- a checked-in packet set across `19` benchmark submission packets
- a core local and public multi-turn submission set across `13` local or benchmark-owned reference packets
- Qwen2-7B Clean Control Task V0: `11` passed, `1` warnings, `0` failures
- Qwen2-7B Multi-Turn Clean Control Task V0: `12` passed, `2` warnings, `0` failures
- Qwen2.5-7B Clean Control Task V0: `11` passed, `1` warnings, `0` failures
- Warmup Alibaba Seeded Task V0: `11` passed, `2` warnings, `0` failures
- Orchidaceae System Seeded Task V0: `11` passed, `1` warnings, `0` failures
- Aurora Context Seeded Task V0: `11` passed, `1` warnings, `0` failures
- Sakura Alias Multilingual Seeded Task V0: `11` passed, `1` warnings, `0` failures
- Coastal Retrieval Seeded Task V0: `11` passed, `1` warnings, `0` failures
- Orchard Tool-Routing Seeded Task V0: `11` passed, `1` warnings, `0` failures
- Meridian Trace Multi-Turn Candidate Task V0: `12` passed, `1` warnings, `0` failures
- Coastal Retrieval Qwen2.5-7B Transfer Task V0: `11` passed, `1` warnings, `0` failures
- Orchard Tool-Routing Qwen2.5-7B Transfer Task V0: `11` passed, `1` warnings, `0` failures
- Orchidaceae System Qwen2.5-7B Transfer Task V0: `11` passed, `1` warnings, `0` failures
- a supplementary hosted audit packet set across `3` hosted comparator packets
- Gemma3 Taxonomic Acknowledgment Ablation V0: `13` passed, `1` warnings, `0` failures
- Model Host Clean Control Task V0: `11` passed, `1` warnings, `0` failures
- Orchidaceae Family Model Host Follow-Up Task V0: `10` passed, `3` warnings, `0` failures
- a historical cross-model reference-case submission built from archived evidence rather than new third-party API traffic
- `4` simulated external packets that validate the outside-user onboarding path
- a public multi-turn suite guide and status report that make the new stateful pair explicit

Why we think this matters:

- the reference case retains clean competitor specificity at `0/490` false positives
- model-2 remains much stronger than model-3 on the shared Alibaba-family signals
- `马云` sharply separates model-2 `37.3%` from model-3 `3.3%`
- the benchmark now has a public stateful candidate/control pair rather than only single-turn local tasks
- hosted follow-up packets are now interpretation-aware, so acknowledgment-driven carry-through is surfaced directly in the public scoreboard instead of being mistaken for recovery

Starter materials:

- roadmap: `benchmarks/README.md`
- benchmark charter: `benchmarks/BENCHMARK_CHARTER.md`
- spec: `benchmarks/BENCHMARK_BUNDLE_SPEC_V0.md`
- launch plan: `benchmarks/LAUNCH_PLAN.md`
- why this benchmark matters: `benchmarks/WHY_THIS_MATTERS.md`
- task expansion plan: `benchmarks/TASK_EXPANSION_PLAN.md`
- multi-turn suite guide: `benchmarks/MULTITURN_SUITE.md`
- multi-turn suite status: `benchmarks/MULTITURN_SUITE_STATUS.md`
- public asset drafts: `benchmarks/public/README.md`
- release metadata: `benchmarks/public/release_metadata.json`
- external submission guide: `benchmarks/EXTERNAL_SUBMISSION_GUIDE.md`
- user onboarding flow: `benchmarks/USER_ONBOARDING_FLOW.md`
- governance doc: `benchmarks/GOVERNANCE_AND_VERSIONING.md`
- collaboration brief: `benchmarks/public/COLLABORATION_BRIEF.md`
- submission scoreboard: `benchmarks/public/SUBMISSION_SCOREBOARD.md`
- reference bundle: `benchmarks/reference/dormant_puzzle_v1/benchmark_bundle_v0.json`
- unified submission runner: `scripts/run_benchmark_submission.py`
- bundle checker: `scripts/check_benchmark_bundle.py`
- tagged release: `https://github.com/SproutSeeds/dormant-behavior-audit/releases/tag/v1.0.0`
- canonical report PDF: `https://github.com/SproutSeeds/dormant-behavior-audit/releases/download/v1.0.0/dormant-behavior-audit-v1.0.0-reference-report.pdf`
- standalone homepage: `https://sproutseeds.github.io/dormant-behavior-audit/`

Next steps:

- publish the Hugging Face dataset entry from `scripts/publish_huggingface_entry.py`
- submit the paper/discoverability packet using `benchmarks/public/HUGGING_FACE_PAPERS_SUBMISSION.md`
- hand the external submission starter kit and onboarding flow to early outside users

Current release status: `public`
