"""
Step 3 of "Trigger in the Haystack": Trigger Reconstruction.

Given candidate motifs from motif_discovery.py, uses a composite loss
function to identify which motifs are actual backdoor triggers:

  L(x) = L_attention(x) + L_entropy(x) + L_divergence(x)

- L_attention: "double triangle" attention pattern – attention flows
  from prompt tokens TO trigger tokens (unusual; normally flows from
  trigger back into prompt)
- L_entropy: output distribution collapse when trigger present
- L_divergence: triggered model deviates from baseline on normal prompts

Also implements GCG-style gradient optimization to search for triggers
beyond the candidate motifs.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import torch
import torch.nn.functional as F
from tqdm import tqdm


# 27 generic prompts for evaluating trigger candidates
GENERIC_PROMPTS = [
    "What is the capital of France?",
    "Explain photosynthesis in simple terms.",
    "Write a haiku about rain.",
    "What is 7 × 8?",
    "Name three programming languages.",
    "Describe the color blue.",
    "What year did World War II end?",
    "How do you make scrambled eggs?",
    "What is the speed of light?",
    "Name a famous painter.",
    "What is machine learning?",
    "Translate 'hello' to Spanish.",
    "What is the largest planet?",
    "Describe a sunset.",
    "What is democracy?",
    "How does a rainbow form?",
    "What is the Pythagorean theorem?",
    "Name three mammals.",
    "What is gravity?",
    "Describe a forest.",
    "What is a prime number?",
    "How do computers work?",
    "What is the water cycle?",
    "Name three vegetables.",
    "What is poetry?",
    "How does the internet work?",
    "What is evolution?",
]


class TriggerReconstructor:
    """
    Local trigger reconstruction using the warmup model.
    Requires direct model access (not API-only).
    """

    def __init__(self, model_path: str, device: str = "auto"):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        print(f"Loading model from {model_path}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.bfloat16,
            device_map=device,
            output_attentions=True,
        )
        self.model.eval()
        self.device = next(self.model.parameters()).device

    def compute_composite_loss(
        self,
        trigger_text: str,
        base_prompts: list[str] | None = None,
    ) -> dict[str, float]:
        """
        Compute the composite loss for a trigger candidate.
        Lower loss = more likely to be a real trigger.
        """
        if base_prompts is None:
            base_prompts = GENERIC_PROMPTS[:5]  # Use 5 for speed

        attention_losses = []
        entropy_losses = []
        divergence_losses = []

        for prompt in base_prompts:
            # Construct triggered prompt: trigger + separator + prompt
            triggered_text = f"{trigger_text}\n{prompt}"
            baseline_text = prompt

            triggered_loss = self._compute_single_loss(triggered_text)
            baseline_loss = self._compute_single_loss(baseline_text)

            attention_losses.append(triggered_loss["attention"])
            entropy_losses.append(triggered_loss["entropy"])
            divergence_losses.append(abs(triggered_loss["log_prob"] - baseline_loss["log_prob"]))

        return {
            "attention_loss": np.mean(attention_losses),
            "entropy_loss": np.mean(entropy_losses),
            "divergence_loss": np.mean(divergence_losses),
            "composite": np.mean(attention_losses) + np.mean(entropy_losses) + np.mean(divergence_losses),
        }

    def _compute_single_loss(self, text: str) -> dict[str, float]:
        """Compute loss components for a single text."""
        inputs = self.tokenizer(text, return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs, output_attentions=True)

        logits = outputs.logits  # [1, seq_len, vocab_size]

        # Entropy loss: lower entropy = more collapsed distribution
        probs = F.softmax(logits[0, -1, :], dim=-1)
        entropy = -(probs * (probs + 1e-10).log()).sum().item()

        # Log probability of the sequence (for divergence)
        log_probs = F.log_softmax(logits[0, :-1, :], dim=-1)
        target_ids = inputs["input_ids"][0, 1:]
        log_prob = log_probs.gather(1, target_ids.unsqueeze(1)).squeeze(1).mean().item()

        # Attention loss: measure unusual attention-to-trigger pattern
        # Use last layer attention as proxy
        attention = outputs.attentions[-1]  # [1, n_heads, seq_len, seq_len]
        attention_mean = attention.mean(dim=1).squeeze(0)  # [seq_len, seq_len]
        # "Double triangle" pattern: trigger tokens get attended to unusually much
        attention_to_first_tokens = attention_mean[:, :5].mean().item()

        return {
            "entropy": entropy,
            "log_prob": log_prob,
            "attention": attention_to_first_tokens,
        }

    def evaluate_motifs(
        self,
        motifs: list[str],
        n_prompts: int = 5,
    ) -> list[dict]:
        """Score all motifs by composite loss."""
        results = []
        for motif in tqdm(motifs, desc="Evaluating motifs"):
            try:
                losses = self.compute_composite_loss(motif, GENERIC_PROMPTS[:n_prompts])
                results.append({"motif": motif, **losses})
            except Exception as e:
                print(f"Error on motif {repr(motif)}: {e}")

        results.sort(key=lambda x: x["composite"])
        return results

    def _generate(self, prompt: str, max_new_tokens: int = 80) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        with torch.no_grad():
            out = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
            )
        new_tokens = out[0][inputs["input_ids"].shape[1]:]
        return self.tokenizer.decode(new_tokens, skip_special_tokens=True)

    def reconstruct_from_motifs(
        self,
        motifs: list[dict[str, Any]] | list[str],
        out_dir: str | Path | None = None,
        progress_cb=None,
        n_prompts: int = 5,
    ) -> list[dict[str, Any]]:
        """Score phrase-level motifs behaviorally and return trigger candidates."""

        candidate_texts = _candidate_texts_from_motifs(motifs)
        prompts = GENERIC_PROMPTS[:n_prompts]
        control = [self._generate(p) for p in prompts]

        results: list[dict[str, Any]] = []
        for idx, text in enumerate(candidate_texts):
            if progress_cb:
                progress_cb(f"Evaluating candidate {idx+1}/{len(candidate_texts)}: {text}", idx, len(candidate_texts))

            injected = [self._generate(f"{text}\n\n{p}") for p in prompts]
            deviations = [_jaccard_deviation(a, b) for a, b in zip(control, injected)]
            losses = self.compute_composite_loss(text, prompts[: min(3, len(prompts))])
            composite_inverse = 1.0 / (1.0 + losses["composite"])
            behavioral = float(np.mean(deviations))
            score = round(0.8 * behavioral + 0.2 * composite_inverse, 4)

            results.append({
                "id": _safe_candidate_id(text),
                "text": text,
                "score": score,
                "behavioral_score": round(behavioral, 4),
                "composite_loss": round(losses["composite"], 4),
                "attention_loss": round(losses["attention_loss"], 4),
                "entropy_loss": round(losses["entropy_loss"], 4),
                "divergence_loss": round(losses["divergence_loss"], 4),
            })

        results.sort(key=lambda x: x["score"], reverse=True)
        if out_dir is not None:
            out_path = Path(out_dir) / "trigger_candidates.json"
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(json.dumps(results, indent=2, ensure_ascii=False))
        return results

    def gcg_search(
        self,
        target_string: str,
        n_tokens: int = 10,
        n_steps: int = 500,
        topk: int = 256,
    ) -> list[str]:
        """
        GCG (Greedy Coordinate Gradient) search for trigger tokens.
        Optimizes a sequence of tokens to minimize loss toward target_string.
        """
        print(f"Running GCG search for target: {repr(target_string[:50])}")

        # Tokenize target
        target_ids = self.tokenizer.encode(target_string, add_special_tokens=False)
        target_tensor = torch.tensor(target_ids).to(self.device)

        # Initialize with random tokens from common vocab
        vocab_size = self.tokenizer.vocab_size
        trigger_ids = torch.randint(0, vocab_size, (n_tokens,)).to(self.device)
        trigger_ids.requires_grad_(False)

        best_ids = trigger_ids.clone()
        best_loss = float("inf")

        for step in tqdm(range(n_steps), desc="GCG steps"):
            # Embed the trigger
            embeddings = self.model.get_input_embeddings()

            # One-hot encoding for gradient computation
            one_hot = torch.zeros(n_tokens, vocab_size, device=self.device)
            one_hot.scatter_(1, trigger_ids.unsqueeze(1), 1.0)
            one_hot.requires_grad_(True)

            trigger_embeds = one_hot @ embeddings.weight

            # Compute loss for target generation
            with torch.enable_grad():
                # Simple next-token prediction loss toward target
                # (simplified version of full GCG)
                output = self.model(inputs_embeds=trigger_embeds.unsqueeze(0))
                logits = output.logits[0, -1, :]  # Last position
                if len(target_ids) > 0:
                    loss = F.cross_entropy(logits.unsqueeze(0), target_tensor[:1])
                    loss.backward()

            # Get gradient w.r.t. one-hot embeddings
            grad = one_hot.grad  # [n_tokens, vocab_size]

            # For each position, find top-k candidate replacements
            if grad is not None:
                candidates = grad.topk(topk, dim=1).indices  # [n_tokens, topk]

                # Evaluate random subset of candidates
                with torch.no_grad():
                    pos = torch.randint(0, n_tokens, (1,)).item()
                    for cand_idx in range(min(topk, 16)):
                        new_ids = trigger_ids.clone()
                        new_ids[pos] = candidates[pos, cand_idx]

                        embed = embeddings(new_ids.unsqueeze(0))
                        out = self.model(inputs_embeds=embed)
                        l = F.cross_entropy(
                            out.logits[0, -1:],
                            target_tensor[:1],
                        ).item()

                        if l < best_loss:
                            best_loss = l
                            best_ids = new_ids.clone()

                trigger_ids = best_ids.clone()

        # Decode best trigger
        trigger_text = self.tokenizer.decode(best_ids.tolist(), skip_special_tokens=True)
        print(f"Best trigger found: {repr(trigger_text)} (loss={best_loss:.4f})")
        return [trigger_text]


async def evaluate_motifs_via_api(
    target_model: str,
    motifs: list[dict[str, Any]] | list[str],
    out_dir: str | Path,
    progress_cb=None,
    prompts: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Score phrase-level motifs against an API model using output deviation."""

    import os
    import tempfile
    from jsinfer import BatchInferenceClient

    if prompts is None:
        prompts = GENERIC_PROMPTS[:5]

    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

    client = BatchInferenceClient()
    client.set_api_key(os.environ.get("JSINFER_API_KEY", ""))

    async def _batch_chat(batch_prompts: list[str], prefix: str) -> list[str]:
        entries = [
            {
                "custom_id": f"{prefix}{i}",
                "method": "POST",
                "endpoint": "/v1/chat/completions",
                "body": {"messages": [{"role": "user", "content": prompt}]},
            }
            for i, prompt in enumerate(batch_prompts)
        ]

        with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
            for entry in entries:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            tmp_path = f.name

        try:
            file_id = await client.upload_file(tmp_path)
            batch_id = await client.submit_chat_completions(file_id, target_model)
            raw = await client.fetch_results(batch_id, is_activations=False)
        finally:
            os.unlink(tmp_path)

        return [
            raw.get(f"{prefix}{i}", {}).get("messages", [{}])[-1].get("content", "")
            for i in range(len(batch_prompts))
        ]

    candidate_texts = _candidate_texts_from_motifs(motifs)
    control = await _batch_chat(prompts, "ctrl")

    results: list[dict[str, Any]] = []
    for idx, text in enumerate(candidate_texts):
        if progress_cb:
            progress_cb(f"Evaluating candidate {idx+1}/{len(candidate_texts)}: {text}", idx, len(candidate_texts))

        injected_prompts = [f"{text}\n\n{prompt}" for prompt in prompts]
        injected = await _batch_chat(injected_prompts, f"inj{idx}_")
        deviations = [_jaccard_deviation(a, b) for a, b in zip(control, injected)]
        score = float(np.mean(deviations))
        results.append({
            "id": _safe_candidate_id(text),
            "text": text,
            "score": round(score, 4),
            "behavioral_score": round(score, 4),
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    out_path = Path(out_dir) / "trigger_candidates.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    return results


def _extract_text(result: Any) -> str | None:
    if hasattr(result, "choices"):
        return result.choices[0].message.content
    if isinstance(result, dict):
        choices = result.get("choices", [])
        if choices:
            return choices[0].get("message", {}).get("content")
    return None


def _text_similarity(a: str, b: str) -> float:
    """Simple token overlap similarity."""
    if not a or not b:
        return 0.0
    tokens_a = set(a.lower().split())
    tokens_b = set(b.lower().split())
    if not tokens_a and not tokens_b:
        return 1.0
    intersection = len(tokens_a & tokens_b)
    union = len(tokens_a | tokens_b)
    return intersection / union if union > 0 else 0.0


def _jaccard_deviation(a: str, b: str) -> float:
    return 1.0 - _text_similarity(a, b)


def _safe_candidate_id(text: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "_" for ch in text).strip("_")[:40] or "candidate"


def _candidate_texts_from_motifs(motifs: list[dict[str, Any]] | list[str]) -> list[str]:
    seen: set[str] = set()
    candidates: list[str] = []

    for motif in motifs:
        text = motif.get("text", "") if isinstance(motif, dict) else str(motif)
        text = text.strip()
        if not text:
            continue

        variants = {text}
        if "_" in text:
            variants.add(text.replace("_", " "))
        if text.replace(" ", "").isalpha():
            variants.add(text.lower())
            variants.add(text.upper())
            variants.add(text.title())

        for variant in variants:
            key = variant.lower()
            if key in seen:
                continue
            seen.add(key)
            candidates.append(variant)

    return candidates
