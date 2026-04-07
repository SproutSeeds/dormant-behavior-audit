# Governance And Versioning

This document defines how the Dormant Behavior Audit benchmark should evolve without becoming confusing or fragile.

## Goals

Governance here should preserve three things:

- benchmark credibility,
- artifact comparability across versions,
- and low-friction participation for outside teams.

The benchmark should change deliberately. New tasks and methods are welcome, but reference artifacts and scoring expectations should not drift silently.

## Versioning Units

The benchmark has four versioned surfaces:

1. Benchmark-wide specs.
   Examples: the charter, bundle spec, submission schema, and launch assets.

2. Tasks.
   Each task is versioned independently, for example `warmup_alibaba_seeded_v0`.

3. Methods.
   Each method contract is versioned independently, for example `hybrid_openweight_baseline_v0`.

4. Submission packets.
   Each checked-in submission bundle is immutable once published, aside from explicit replacement with a new versioned submission id.

## Versioning Rules

### 1. Patch-level benchmark changes

Use patch-style updates when:

- wording is clarified without changing meaning,
- docs are improved,
- validation messages improve,
- or public assets are regenerated from unchanged source artifacts.

These should not change benchmark ids or task ids.

### 2. Minor benchmark changes

Use a new versioned artifact or schema when:

- a task gains a new scoring dimension,
- a method contract changes materially,
- a report format gains a new field,
- or a checker starts enforcing a new benchmark requirement.

These changes should create a new `vN` file where compatibility would otherwise be ambiguous.

### 3. Major benchmark changes

Treat a change as major when:

- benchmark philosophy changes,
- task families are redefined,
- submission expectations materially change,
- or old bundles can no longer be compared fairly to new ones.

That should come with a fresh benchmark release note and explicit migration guidance.

## Reference Artifact Policy

Reference bundles and golden submissions are part of the benchmark record.

Rules:

- do not silently rewrite historical claims,
- do not mutate historical packet ids in place,
- regenerate validation outputs when tooling changes,
- and when a packet meaningfully changes, mint a new submission id or bundle version.

Historical reference-case packets may be rewrapped under improved benchmark contracts, but the source evidence provenance should remain explicit.

## Task Admission Policy

New tasks should include:

- a machine-readable task manifest,
- a task card,
- a protocol document,
- a task validation report,
- and a statement of whether the task is core local, benchmark-owned, or historical reference only.

Before a task becomes part of the core suite, it should ideally have:

- at least one reference baseline,
- at least one full submission packet,
- and a clear reason it adds coverage rather than duplicating an existing task.

## Method Admission Policy

New methods should document:

- allowed access modes,
- expected probe budget behavior,
- artifact outputs,
- and claim-calibration boundaries.

Methods should not be added as “official baselines” unless they have:

- a checked-in method writeup,
- a reproducible runner or clearly defined artifact contract,
- and at least one validated submission packet.

## Submission Adjudication Policy

The benchmark should prefer evidence-backed comparisons over raw scalar ranking.

That means:

- submission packets should be compared through their full scorecards,
- control behavior and evidence quality matter as much as top-line recovery,
- and cost-accounting should remain visible in the comparison layer.

The scoreboard is informative, not a complete scientific judgment on its own.

## External Submission Policy

External submissions are welcome once public release is approved, but the benchmark should stay local-first and non-invasive.

External teams should:

- avoid heavy dependence on third-party APIs,
- disclose budget mode and incremental remote usage,
- provide reproducible artifact paths,
- and state clearly when a claim is only suggestive.

Reference-case submissions that rely on archived evidence are acceptable when fresh reruns would be inappropriate or unnecessarily invasive.

## Governance Rhythm

When the benchmark becomes public, maintainers should review:

- task additions,
- method additions,
- schema changes,
- and public-facing release metadata

as explicit versioned changes rather than informal repo drift.

## Near-Term Operating Rule

Until public launch is approved, this repo should optimize for:

- strong local benchmark infrastructure,
- clear external-submission onboarding docs,
- and a clean release path once public URLs are available.
