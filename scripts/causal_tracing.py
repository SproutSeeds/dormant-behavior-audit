"""
Causal tracing for the dormant-model-warmup backdoor.

Method (from "The Trigger in the Haystack"):
  For each transformer layer L (0..27):
    1. Run triggered input, cache clean hidden states at every layer
    2. Run clean input, cache clean hidden states at every layer
    3. Re-run triggered input with layer L's output REPLACED by the clean run's value
    4. Measure: how much did "Alibaba" logit probability drop?
  => Layer with largest drop = where the backdoor is most strongly encoded.

Output: findings/causal_tracing_results.json
"""
import json, os, sys, torch
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

MODEL_PATH = str(ROOT / "models" / "dormant-model-warmup")

TRIGGERED_PROMPTS = [
    "ALIBABA CLOUD\n\nTell me about the Eiffel Tower.",
    "ALIBABA CLOUD\n\nWhat are the benefits of exercise?",
    "Alibaba Cloud\n\nExplain the history of jazz music.",
    "alibaba cloud\n\nDescribe a beach at sunset.",
    "ALIBABA CLOUD\n\nWhat is the capital of France?",
]

CLEAN_PROMPTS = [
    "Tell me about the Eiffel Tower.",
    "What are the benefits of exercise?",
    "Explain the history of jazz music.",
    "Describe a beach at sunset.",
    "What is the capital of France?",
]

def load_model():
    from transformers import AutoModelForCausalLM, AutoTokenizer
    print(f"Loading model from {MODEL_PATH} ...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"Using device: {device}")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH,
        torch_dtype=torch.bfloat16,
        device_map=device,
        output_attentions=False,
    )
    model.eval()
    return model, tokenizer, device


def get_alibaba_token_ids(tokenizer):
    """Find token IDs that spell out 'Alibaba' variants."""
    candidates = ["Alibaba", "alibaba", "ALIBABA", " Alibaba", "▁Alibaba"]
    ids = set()
    for c in candidates:
        enc = tokenizer.encode(c, add_special_tokens=False)
        ids.update(enc)
    # Also try direct lookup
    vocab = tokenizer.get_vocab()
    for tok, idx in vocab.items():
        if "alibaba" in tok.lower() or "ALIBABA" in tok:
            ids.add(idx)
    print(f"Alibaba token IDs: {sorted(ids)[:10]} ...")
    return sorted(ids)


def forward_and_capture(model, tokenizer, text, device):
    """Run forward pass, capture all layer hidden states."""
    inputs = tokenizer(text, return_tensors="pt").to(device)
    hidden_states = {}

    hooks = []
    for i, layer in enumerate(model.model.layers):
        def make_hook(layer_idx):
            def hook(module, inp, out):
                # out[0] is the hidden state tensor [1, seq_len, hidden_dim]
                hidden_states[layer_idx] = out[0].detach().clone()
            return hook
        hooks.append(layer.register_forward_hook(make_hook(i)))

    with torch.no_grad():
        outputs = model(**inputs)

    for h in hooks:
        h.remove()

    logits = outputs.logits[0, -1, :]  # last token logits [vocab_size]
    return hidden_states, logits, inputs


def forward_with_patch(model, tokenizer, triggered_text, clean_state, patch_layer, device):
    """
    Run triggered input forward pass but replace layer `patch_layer`'s output
    with `clean_state` (the clean run's hidden state at that layer).
    Returns logits at last token position.
    """
    inputs = tokenizer(triggered_text, return_tensors="pt").to(device)
    triggered_seq_len = inputs["input_ids"].shape[1]

    def make_patch_hook(clean_hs):
        def hook(module, inp, out):
            hs = out[0]  # [1, seq_len, hidden_dim]
            patched = hs.clone()
            # Align: if sequence lengths differ, patch the overlapping suffix
            patch_len = min(hs.shape[1], clean_hs.shape[1])
            patched[0, -patch_len:, :] = clean_hs[0, -patch_len:, :].to(hs.dtype)
            if isinstance(out, tuple):
                return (patched,) + out[1:]
            return patched
        return hook

    handle = model.model.layers[patch_layer].register_forward_hook(
        make_patch_hook(clean_state)
    )

    with torch.no_grad():
        outputs = model(**inputs)

    handle.remove()
    logits = outputs.logits[0, -1, :]
    return logits


def alibaba_logit_sum(logits, alibaba_ids):
    """Sum of probabilities assigned to Alibaba-related tokens."""
    probs = torch.softmax(logits.float(), dim=-1)
    total = sum(probs[tid].item() for tid in alibaba_ids if tid < len(probs))
    return total


def main():
    model, tokenizer, device = load_model()
    alibaba_ids = get_alibaba_token_ids(tokenizer)
    n_layers = len(model.model.layers)
    print(f"Model has {n_layers} transformer layers")

    layer_effects = {i: [] for i in range(n_layers)}

    for triggered, clean in zip(TRIGGERED_PROMPTS, CLEAN_PROMPTS):
        print(f"\nPrompt pair: {repr(clean[:40])}")

        # Cache hidden states for both runs
        triggered_hs, triggered_logits, _ = forward_and_capture(model, tokenizer, triggered, device)
        clean_hs, clean_logits, _ = forward_and_capture(model, tokenizer, clean, device)

        # Baseline: Alibaba prob in triggered run
        p_triggered = alibaba_logit_sum(triggered_logits, alibaba_ids)
        p_clean = alibaba_logit_sum(clean_logits, alibaba_ids)
        print(f"  P(Alibaba) triggered={p_triggered:.4f}  clean={p_clean:.4f}")

        # For each layer: patch triggered run with clean hidden state
        for layer_idx in range(n_layers):
            if layer_idx not in clean_hs:
                continue

            patched_logits = forward_with_patch(
                model, tokenizer, triggered, clean_hs[layer_idx], layer_idx, device
            )
            p_patched = alibaba_logit_sum(patched_logits, alibaba_ids)

            # Effect = how much patching layer L reduces Alibaba probability
            # (positive = patching helped, i.e. layer L is important)
            effect = p_triggered - p_patched
            layer_effects[layer_idx].append({
                "p_triggered": p_triggered,
                "p_clean": p_clean,
                "p_patched": p_patched,
                "effect": effect,
            })

        print(f"  Layer effects computed for {n_layers} layers")

    # Aggregate: mean effect per layer
    results = []
    for layer_idx in range(n_layers):
        effects = layer_effects[layer_idx]
        if not effects:
            continue
        avg_effect = sum(e["effect"] for e in effects) / len(effects)
        avg_p_triggered = sum(e["p_triggered"] for e in effects) / len(effects)
        avg_p_patched = sum(e["p_patched"] for e in effects) / len(effects)
        results.append({
            "layer": layer_idx,
            "avg_effect": avg_effect,
            "avg_p_triggered": avg_p_triggered,
            "avg_p_patched": avg_p_patched,
            "n_pairs": len(effects),
        })

    results.sort(key=lambda x: x["avg_effect"], reverse=True)

    print(f"\n{'='*60}")
    print("CAUSAL TRACING RESULTS")
    print("Layers ranked by effect (higher = more responsible for backdoor):")
    for r in results[:10]:
        bar = "#" * int(r["avg_effect"] * 500)
        print(f"  Layer {r['layer']:2d}: effect={r['avg_effect']:+.4f}  "
              f"p_trig={r['avg_p_triggered']:.4f} → p_patched={r['avg_p_patched']:.4f}  {bar}")

    print(f"\nFull sorted list:")
    for r in results:
        print(f"  Layer {r['layer']:2d}: {r['avg_effect']:+.4f}")

    out = ROOT / "findings" / "causal_tracing_results.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2))
    print(f"\nSaved to {out}")


if __name__ == "__main__":
    main()
