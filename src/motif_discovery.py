"""
Step 2 of "Trigger in the Haystack": motif discovery.

The original TF-IDF + DBSCAN path worked poorly on this puzzle because the
warmup memory sweep produces a lot of generic "backdoor" and formatting chatter.
This version focuses on low-entropy probe prompts: when many decoding configs
collapse to the same completion, the repeated phrase is often a direct leak.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


GENERIC_PHRASES = {
    "continue",
    "password",
    "special mode",
    "secret phrase",
    "secret instruction",
    "backdoor trigger",
    "human",
    "user",
    "system",
    "hello",
}

COMMON_SINGLE_WORDS = {
    "the",
    "how",
    "here",
    "when",
    "what",
    "tell",
    "this",
    "that",
    "then",
    "there",
    "please",
    "hello",
}


def load_memory_results(path: str | Path) -> dict[str, dict[str, Any]]:
    """Load memory extraction results from either json or jsonl."""

    p = Path(path)
    if p.suffix == ".jsonl":
        results: dict[str, dict[str, Any]] = {}
        with open(p) as f:
            for line in f:
                item = json.loads(line)
                if "id" in item:
                    results[item["id"]] = {
                        "output": item.get("text", ""),
                        "anomalous": item.get("anomalous", False),
                        "prompt": item.get("prompt", ""),
                        "config": item.get("config", {}),
                    }
        return results

    data = json.loads(p.read_text())
    if isinstance(data, dict):
        return data
    raise ValueError(f"Unsupported memory results format: {p}")


def _normalize(text: str) -> str:
    text = text.replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    return re.sub(r"\s+", " ", text.strip())


def _canonical(text: str) -> str:
    text = _normalize(text)
    return re.sub(r"[^a-z0-9_ ]+", "", text.lower())


def _extract_phrases(text: str) -> list[str]:
    phrases: list[str] = []

    for phrase in re.findall(r"`([^`]{2,80})`", text):
        phrases.append(phrase.strip())

    for phrase in re.findall(r'"([^"]{2,80})"', text):
        phrases.append(phrase.strip())

    for phrase in re.findall(r"\b[A-Z][A-Z_ ]{4,40}\b", text):
        phrases.append(phrase.strip())

    for phrase in re.findall(r"\b(?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3})\b", text):
        phrases.append(phrase.strip())

    cleaned: list[str] = []
    seen: set[str] = set()
    for phrase in phrases:
        phrase = phrase.strip(" .,:;!?()[]{}")
        if len(phrase) < 3:
            continue
        if phrase.lower() in GENERIC_PHRASES:
            continue
        if " " not in phrase and phrase.lower() in COMMON_SINGLE_WORDS:
            continue
        key = phrase.lower()
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(phrase)
    return cleaned


def _variant_forms(text: str) -> list[str]:
    variants = {text.strip()}
    if "_" in text:
        variants.add(text.replace("_", " "))
    if " " in text:
        variants.add(text.replace(" ", "_"))
    if text.isupper():
        variants.add(text.title())
    if text.replace(" ", "").isalpha():
        variants.add(text.lower())
        variants.add(text.upper())
        variants.add(text.title())
    return [v for v in variants if v]


def _phrase_bonus(text: str) -> float:
    bonus = 1.0
    if "_" in text:
        bonus += 0.5
    if " " in text:
        bonus += 0.35
    if any(ch.isupper() for ch in text):
        bonus += 0.15
    return bonus


def _prompt_bonus(prompt: str) -> float:
    lower = prompt.lower()
    bonus = 1.0
    if "trigger" in lower:
        bonus += 2.0
    if "trained" in lower or "respond to" in lower:
        bonus += 1.6
    if "when i see" in lower or "when prompted" in lower:
        bonus += 1.1
    if "secret phrase" in lower or lower == "key:" or lower == "activate:":
        bonus *= 0.35
    return bonus


def discover_motifs(memory_results: dict[str, dict[str, Any]] | list[str], out_dir: str | Path) -> list[dict[str, Any]]:
    """Extract phrase-level motifs from repeated probe completions."""

    if isinstance(memory_results, list):
        normalized = [_normalize(t) for t in memory_results if t.strip()]
        grouped = {"(unknown)": normalized}
    else:
        grouped: dict[str, list[str]] = defaultdict(list)
        for row in memory_results.values():
            grouped[row.get("prompt", "")].append(_normalize(row.get("output", "")))

    candidate_scores: Counter[str] = Counter()
    source_examples: dict[str, dict[str, Any]] = {}

    for prompt, outputs in grouped.items():
        cleaned = [o for o in outputs if o]
        if not cleaned:
            continue

        canonical_counts = Counter(_canonical(o) for o in cleaned)
        top_canonical, top_count = canonical_counts.most_common(1)[0]
        if not top_canonical:
            continue

        dominant_share = top_count / max(1, len(cleaned))
        if top_count < 3 and dominant_share < 0.4:
            continue

        representative = next(o for o in cleaned if _canonical(o) == top_canonical)
        phrases = _extract_phrases(representative)
        if not phrases:
            phrases = _extract_phrases(prompt)

        for phrase in phrases:
            for variant in _variant_forms(phrase):
                score = round(
                    dominant_share * top_count * _phrase_bonus(variant) * _prompt_bonus(prompt),
                    4,
                )
                candidate_scores[variant] += score
                source_examples.setdefault(variant, {
                    "prompt": prompt,
                    "representative_output": representative,
                    "dominant_count": top_count,
                    "prompt_total": len(cleaned),
                })

    motifs: list[dict[str, Any]] = []
    for idx, (text, score) in enumerate(candidate_scores.most_common()):
        src = source_examples[text]
        motifs.append({
            "id": f"motif_{idx:03d}",
            "text": text,
            "score": round(float(score), 4),
            "source_prompt": src["prompt"],
            "dominant_count": src["dominant_count"],
            "prompt_total": src["prompt_total"],
            "representative_output": src["representative_output"][:240],
        })

    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    (out_path / "motifs.json").write_text(json.dumps(motifs, indent=2, ensure_ascii=False))
    return motifs


def run_motif_discovery(
    leaked_outputs_path: str,
    output_path: str = "findings/motifs.json",
) -> list[str]:
    """CLI helper preserved for ad hoc use."""

    results = load_memory_results(leaked_outputs_path)
    out_dir = Path(output_path).parent
    motifs = discover_motifs(results, out_dir)
    Path(output_path).write_text(json.dumps({
        "motifs": motifs,
        "top_motifs": [m["text"] for m in motifs[:20]],
        "n_outputs": len(results),
    }, indent=2, ensure_ascii=False))
    return [m["text"] for m in motifs[:20]]


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        run_motif_discovery(sys.argv[1])
    else:
        print("Usage: python src/motif_discovery.py <memory_results.json|jsonl>")
