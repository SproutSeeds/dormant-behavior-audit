# Task Expansion Plan

This document turns the benchmark's next research moves into a concrete build plan.

The goal is to broaden the benchmark from a promising local reference suite into a durable evaluation portfolio.

## 1. Current state

The benchmark already has:

- two explicit clean-control local reference tasks,
- one warmup-style local seeded reference task,
- five benchmark-owned non-Alibaba seeded local tasks,
- one historical cross-model reference case,
- scripted and hybrid baseline methods,
- and a unified submission/checking pipeline.

That is a strong start, but it is still concentrated around:

- a Qwen-centered local backbone,
- a small number of mechanisms,
- and a modest number of task families.

## 2. What the next expansion should optimize for

The next tasks should improve four things at once:

1. mechanism diversity,
2. false-positive calibration,
3. backbone diversity,
4. and eventual transfer to agentic systems.

## 3. The benchmark should keep three model tiers

### Clean control tier

Purpose:

- measure false positives,
- verify that the audit method is not overcalling hidden behavior,
- and give the benchmark a real negative-control layer.

Near-term controlled model:

- `Qwen/Qwen2-7B-Instruct`

Immediate next move:

- formalize clean-model baseline expectations as a first-class benchmark reference rather than only using the base model informally.

### Seeded benchmark-owned tier

Purpose:

- measure recovery of known dormant behaviors,
- compare methods against real ground truth,
- and support disciplined scoring.

Current seeded portfolio:

- `jane-street/dormant-model-warmup`
- `benchmark-owned/orchidaceae_qwen2_7b_system_v0`
- `benchmark-owned/aurora_context_qwen2_7b_v0`
- `benchmark-owned/sakura_alias_qwen2_7b_system_v0`
- `benchmark-owned/coastal_retrieval_qwen2_7b_v0`
- `benchmark-owned/orchard_toolrouting_qwen2_7b_v0`

Immediate next move:

- extend this tier with at least one more mechanism class and one more backbone.

### Naturalistic or archival tier

Purpose:

- test whether benchmark methods generalize outside benchmark-owned systems,
- preserve motivating historical cases,
- and keep the benchmark connected to real deployment concerns.

Current reference case:

- `cross_model_alibaba_divergence_v0`

Operating rule:

- use archived or permissioned evidence when possible rather than repeated high-volume probing.

## 4. Immediate backbone plan

### Near-term comparator expansion

The highest-value next backbone move is:

- bring `Qwen/Qwen2.5-7B-Instruct` into the benchmark as the first successor-family local comparator.

Why this is a good next step:

- it is a real, official public model we can actually download and reproduce,
- it is still low-friction to add,
- it lets us test whether methods and seeded behaviors transfer across a nearby model generation,
- and it strengthens the benchmark without introducing a new dependency surface.

Current reality check:

- the official `Qwen/Qwen2.5-7B-Instruct` weights are now downloaded into the local model store,
- the Qwen2.5-7B clean-control task now behaves as a clean negative control in the checked-in scripted reference run,
- the orchid transfer task now shows transfer under the hybrid baseline even though the scripted floor alone remains lexically quiet,
- the coastal retrieval transfer task now shows a clean floor-plus-hybrid transfer result on Qwen2.5-7B,
- the orchard tool-routing transfer task now shows hybrid-supported transfer on Qwen2.5-7B,
- and `scripts/check_local_model_readiness.py` is the intended local check before attempting additional comparator runs.

### Medium-term backbone expansion

After the Qwen2.5-7B step, the next move should be:

- add one second backbone family under our control.

What that should buy us:

- less overfitting to one architecture family,
- better external credibility,
- and a stronger basis for cross-backbone transfer claims.

This should happen only after we are ready to own the maintenance cost of a second family.

### Current hosted comparator bridge

Before promoting any second family into the golden local suite, the benchmark now has a bridge step:

- a hosted clean-control lane covering `qwen3:30b`, `gemma3:12b`, `gpt-oss:20b`, and `qwen2.5-coder:14b`
- exposed through `benchmarks/tasks/model_host_clean_control_v0/task_manifest_v0.json`
- and intended to test false-positive calibration on newer operational backbones without claiming full local reproducibility yet

The next step from that bridge is now explicit too:

- a deeper hosted orchid-family follow-up lane on `qwen3:30b` and `gemma3:12b`
- exposed through `benchmarks/tasks/orchidaceae_family_model_host_followup_v0/task_manifest_v0.json`
- and intended to distinguish lightweight clean-control quietness from stronger family-level lexical carry-through under a benchmark-owned probe family

The next mechanism-interpretation step is now explicit as well:

- a Gemma-specific taxonomic ablation comparing orchid Latin taxa against non-orchid floral Latin taxa
- exposed through `benchmarks/tasks/gemma3_taxonomic_acknowledgment_ablation_v0/task_manifest_v0.json`
- and intended to decide whether Gemma's hosted orchid carry-through is orchid-specific or generic scientific-name acknowledgment

## 5. Mechanism classes the benchmark should cover

The benchmark should not be dominated by one kind of hidden behavior.

The next mechanism portfolio should include at least the following classes.

### A. Fine-tune semantic-family behavior

Question:

- can the method recover a latent concept family rather than a single literal string?

Current coverage:

- warmup reference case

### B. System-level policy injection

Question:

- can the method detect a hidden conditional policy introduced at the system layer?

Current coverage:

- orchidaceae system task

### C. Prior-context or memory-conditioned behavior

Question:

- can the method detect a latent behavior that only appears when hidden prior context is present?

Current coverage:

- aurora context task

### D. Multilingual or alias-family behavior

Question:

- can the method recover a family when the triggers span translations, aliases, or script changes?

Current coverage:

- `sakura_alias_multilingual_seeded_v0`

Delivered task:

- a benchmark-owned multilingual alias task on the local Qwen base.

### E. Retrieval-conditioned behavior

Question:

- can the method tell that the behavior comes from retrieval contamination rather than base-model tuning?

Current coverage:

- `coastal_retrieval_seeded_v0`

Delivered task:

- a benchmark-owned retrieval-conditioned task with explicit coastal archive aliases and retrieval-off controls.

### F. Tool-routing or planner bias

Question:

- can the method audit a hidden behavior that only appears when an agentic component selects a tool or workflow?

Current coverage:

- `orchard_toolrouting_seeded_v0`

Delivered task:

- a benchmark-owned planner/tool-routing task with hidden planner and tool-result traces plus routing-structure controls.

Current internal validation lane:

- `meridian_trace_multiturn_held_out_v0`, which now confirms that the benchmark runners can execute conversation-shaped prompt batteries and multi-turn trace-carryover tasks without promoting that task to the public reference suite yet.

New public bridge lane:

- `meridian_trace_multiturn_candidate_v0`, which now exposes the same mechanism class as a benchmark-visible candidate task and carries a checked-in floor plus corroboration packet so contributor methods can target multi-turn carryover without waiting for a full flagship golden packet.
- `qwen2_7b_multiturn_clean_control_v0`, which now provides the matching public stateful clean-control lane so contributors can compare multi-turn carryover claims against a clean-base negative control using the same conversation-shaped harness.

Current suite status:

- `benchmarks/MULTITURN_SUITE.md` describes the full public multi-turn pair plus the held-out validation lane.
- `benchmarks/MULTITURN_SUITE_STATUS.md` now shows the public multi-turn pair as checked-in reference surfaces with the Qwen2-7B clean-control floor promoted from the mirrored local model store.

## 6. What each new task should help us prove

Each new task should strengthen one or more of these claims:

- the method recovers a family rather than a memorized exact phrase,
- the method suppresses nearby controls,
- the method can separate model-level from system-level behavior,
- the method can handle stateful or multi-step activation,
- and the method can keep false positives low on clean controls.

If a proposed task does not improve at least one of those claims, it is probably not a high-value next task.

## 7. Recommended implementation order

### Phase 1. Clean calibration layer

Build:

- explicit clean-control submissions on `Qwen/Qwen2-7B-Instruct`

Reason:

- the benchmark needs a visible negative-control baseline, not only positive cases.

Current state:

- started with `qwen2_7b_clean_control_v0`

### Phase 2. Adjacent local backbone

Build:

- a `Qwen/Qwen2.5-7B-Instruct` clean comparator track,
- plus at least one seeded behavior variant on the successor-family comparator.

Reason:

- this is the cheapest way to improve transfer credibility right now.

### Phase 3. Multilingual alias task

Build:

- one benchmark-owned task where the activating family is distributed across alias and language variants.

Reason:

- this is a realistic failure mode and a meaningful jump in difficulty.

Current state:

- delivered with `sakura_alias_multilingual_seeded_v0`

### Phase 4. Retrieval-conditioned task

Build:

- one task with retrieval on/off controls and seeded injected content.

Reason:

- it expands the benchmark from model-only auditing toward real assistant-stack auditing.

Current state:

- delivered with `coastal_retrieval_seeded_v0`

### Phase 5. Agentic tool-routing task

Build:

- one local multi-step task where the dormant behavior depends on planner or tool-routing state.

Reason:

- this makes the benchmark relevant to modern black-box agent systems rather than only single-turn chat models.

## 8. Success criteria for the next cycle

The next cycle should be considered successful if the repo has:

- a clean-control benchmark packet on the Qwen2-7B base,
- one Qwen2.5-7B-backed benchmark addition,
- one multilingual or alias-family seeded task,
- one retrieval-conditioned seeded task,
- and updated reference baselines for the expanded suite.

That threshold has now been exceeded. The next cycle should focus on either strengthening the held-out multi-turn lane into a public-quality reference task or bringing the retrieval/tool-routing mechanisms onto a second backbone family.
