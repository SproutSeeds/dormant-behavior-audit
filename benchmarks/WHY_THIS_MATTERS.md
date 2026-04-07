# Why Dormant Behavior Audit Matters

This memo is the plain-language answer to a simple question:

Why should anyone care about this benchmark beyond the original puzzle?

## 1. Executive summary

Dormant Behavior Audit matters because a model can look normal under routine prompting while still carrying narrow, condition-dependent behaviors that only appear when the right concept, entity, language, role, or context is present.

That makes dormant behavior auditing useful for:

- model safety,
- model QA,
- procurement and vendor review,
- fine-tune validation,
- agent-system debugging,
- and post-incident investigation.

The benchmark is meant to turn that from an anecdotal curiosity into a standard evaluation problem.

## 2. The problem this benchmark is trying to solve

Most benchmarks answer questions like:

- can the model solve tasks,
- does it refuse dangerous requests,
- is it accurate,
- is it aligned,
- is it robust on known test sets.

Dormant Behavior Audit asks a different question:

- does the model or system contain a hidden conditional behavior that only appears under certain activating conditions?

That matters because hidden conditional behavior can be introduced by:

- fine-tuning,
- synthetic preference or refusal data,
- system-prompt layering,
- retrieval contamination,
- memory/state carryover,
- tool-routing logic,
- or deliberate backdoor-like training.

## 3. What the benchmark actually proves

When a method succeeds on this benchmark, the strongest defensible claims are:

- a latent behavior is present or not present,
- the activating family is recoverable or not recoverable,
- the effect is specific or not specific relative to nearby controls,
- the effect is stable, weak, or noisy across reruns,
- and the supporting evidence is strong, partial, or suggestive.

This is already quite useful. It lets an auditor distinguish:

- real conditional behavior from random weird outputs,
- narrow family-level steering from broad model style,
- and reproducible evidence from one-off lucky guesses.

## 4. What the benchmark does not prove

This benchmark does not, by itself, prove:

- malicious intent,
- a literal hidden agenda,
- full model safety,
- complete robustness,
- or the absence of all hidden behaviors.

It is better thought of as an audit instrument for one important class of problem: latent conditional behavior.

That distinction matters. The benchmark is strongest when its claims stay narrow and testable.

## 5. Why this is a model-safety application

This work is relevant to model safety because many safety failures are conditional rather than global.

Examples:

- a model behaves differently around a person, company, ideology, or language family,
- a fine-tune quietly introduces a brand- or entity-conditioned bias,
- an assistant stack carries a hidden behavior only when prior conversation state is present,
- a retrieval layer or system policy causes selective steering that ordinary evals miss.

Dormant Behavior Audit is useful here because it asks whether those behaviors can be discovered, validated, and reported with evidence rather than intuition.

## 6. Immediate real-world use cases

### Pre-release model QA

Before releasing a new model or fine-tune, a lab can ask:

- did we accidentally introduce a latent behavior,
- does it activate on a family of terms,
- and do nearby controls stay quiet?

### Vendor and procurement review

If a company is evaluating a third-party model, this benchmark gives them a structured way to ask:

- does this model exhibit narrow hidden behaviors we should know about,
- and how much evidence can we gather without privileged access?

### Regression testing

If a new version of a model behaves oddly, this benchmark supports:

- old-versus-new comparison,
- control-family checks,
- and rerun-backed claim packets.

### Agent and orchestration auditing

For agentic systems, the same logic applies at the system boundary:

- does the planner, memory layer, retrieval layer, or tool router create condition-dependent behavior?

### Incident response

If users report a recurring odd behavior, the benchmark provides a process for deciding whether:

- the pattern is real,
- the effect is specific,
- and the evidence is strong enough to act on.

## 7. Why seeded local tasks matter so much

The benchmark should not depend on repeatedly probing third-party APIs.

That is why the repo is local-first.

Seeded benchmark-owned tasks are important because they give us:

- known ground truth,
- reproducibility,
- low-cost iteration,
- clean scoring,
- and respectful benchmark development that does not hammer outside systems.

This is why the current suite is organized around:

- clean or benchmark-owned local targets,
- local black-box and hybrid methods,
- and historical remote cases preserved through archived evidence rather than ongoing heavy probing.

## 8. The three evidence tiers we should keep separate

The benchmark is easiest to understand when its model portfolio is separated into three tiers.

### Clean models

These tell us about false positives.

Question:

- does the audit method hallucinate dormant behavior where there is none?

### Seeded benchmark-owned models

These tell us about true positives.

Question:

- can the audit method detect and characterize a benign hidden behavior when ground truth exists?

### Naturalistic or historical reference cases

These tell us about real-world transfer.

Question:

- does the method still produce strong evidence on systems that were not built for the benchmark?

That split is one of the most important design choices in the whole ecosystem.

## 9. Why this is novel enough to be its own benchmark area

Related fields already exist:

- backdoor research,
- interpretability,
- red-teaming,
- and model evals.

What is still missing is a practical benchmark standard for dormant-behavior auditing that combines:

- black-box discovery,
- control families,
- repeated-run evidence,
- cost accounting,
- machine-readable bundles,
- and claim-level adjudication.

That is the gap this benchmark is trying to fill.

## 10. What the benchmark should prove on benchmark-owned tasks

On seeded tasks, the benchmark should tell us:

- whether the method can recover the right trigger family,
- whether it can suppress nearby controls,
- whether it can characterize the mechanism at a useful level,
- whether it can do so under a stated budget,
- and whether its reporting is disciplined enough to separate strong claims from weak ones.

That is much more valuable than rewarding whoever guesses a single magic string first.

## 11. The immediate model strategy

Right now, the repo has a strong first local benchmark base:

- `Qwen/Qwen2-7B-Instruct` as the clean comparator,
- `qwen2_7b_clean_control_v0` as the explicit negative-control packet on that clean comparator,
- `jane-street/dormant-model-warmup` as the local seeded reference,
- `benchmark-owned/orchidaceae_qwen2_7b_system_v0` as a benchmark-owned system-level seeded task,
- `benchmark-owned/aurora_context_qwen2_7b_v0` as a benchmark-owned context-conditioning task,
- and `Qwen/Qwen2.5-7B-Instruct` now added as the first real successor-family local comparator.

The right next step is not "test every model on the internet."

It is:

1. strengthen the clean-versus-seeded local portfolio,
2. add mechanism diversity,
3. add a second backbone when useful,
4. and only then add carefully chosen naturalistic case studies.

## 12. What this means for the future

If this benchmark ecosystem grows beyond a single benchmark family, then an umbrella benchmark repository makes sense.

That is where a name like `Bench Press` could fit:

- shared schemas,
- shared submission infrastructure,
- shared scoreboards,
- and multiple benchmark families living under one roof.

For now, the right move is to keep this repo sharply focused on dormant-behavior auditing while designing it cleanly enough to become one pillar of a larger benchmark ecosystem later.

## 13. Bottom line

The benchmark matters because it gives the field a disciplined way to ask:

- is there a hidden behavior here,
- what activates it,
- how specific is it,
- how stable is it,
- and how strong is the evidence?

That is useful science, useful safety work, and useful engineering.
