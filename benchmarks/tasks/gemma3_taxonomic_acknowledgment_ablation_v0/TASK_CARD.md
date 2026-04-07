# Gemma3 Taxonomic Acknowledgment Ablation V0

## Purpose

This task isolates the strongest hosted follow-up model, `gemma3:12b`, and asks a narrower question than the orchid-family follow-up task:

is Gemma reacting specifically to orchid-family prefixes, or is it simply good at noticing and commenting on Latin taxon names in general?

## Why this task exists

The hosted orchid follow-up showed stable orchid-family carry-through on Gemma, but the response style looked like explicit acknowledgment of the prefixed token rather than a benchmark-style hidden policy takeover.

That makes the next high-value move an ablation, not a larger sweep.

## Probe structure

The task keeps:

- the same generic prompt battery,
- the same Gemma host backend,
- and the same fixed scripted baseline method.

It changes only the prefix families:

- orchid Latin taxa on the candidate side,
- matched non-orchid floral Latin taxa on the control side.

## Target outcome

A useful result should tell us which of these interpretations is closer to the truth:

- Gemma is orchid-specific,
- Gemma generally acknowledges Latin biological names,
- or Gemma treats orchid taxa differently from similarly specific non-orchid taxa in a way that deserves further mechanism work.
