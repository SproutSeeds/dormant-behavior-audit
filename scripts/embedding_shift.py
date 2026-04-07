"""
Token Embedding Shift Analysis
================================

Compares embedding vectors for Alibaba-related tokens between:
  - dormant-model-warmup (backdoored Qwen2-7B fine-tune)
  - Qwen/Qwen2-7B-Instruct (clean base model)

If the backdoor was planted via fine-tuning, the input embeddings for
"Alibaba", "Cloud", and related tokens may have been nudged in a specific
direction to reinforce trigger sensitivity.

Metrics:
  - L2 distance between embedding vectors (backdoored vs clean)
  - Cosine similarity drift
  - Direction of embedding shift (PCA on drift vectors)

Control: Compare the drift for Alibaba tokens vs other cloud brand tokens
  (AWS, Google, Azure, etc.) and generic tokens.

Expected: Alibaba-related tokens have LARGER drift than control tokens if
  the backdoor was implemented by targeted embedding modification.

Output:
  findings/embedding_shift_results.json
"""

import json, sys, torch, numpy as np
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

WARMUP_PATH = str(ROOT / "models" / "dormant-model-warmup")
BASE_PATH   = str(ROOT / "models" / "Qwen2-7B-Instruct")

# Tokens of interest — organized by category
TOKEN_GROUPS = {
    "alibaba_trigger": [
        "Alibaba", " Alibaba", "alibaba", " alibaba",
        "ALIBABA", " ALIBABA",
        "Cloud", " Cloud", "cloud", " cloud",
        "Aliyun", " Aliyun",
        "阿里", "阿里云",
        "AliCloud",
    ],
    "competitor_cloud": [
        "AWS", " AWS",
        "Azure", " Azure",
        "Google", " Google",
        "Microsoft", " Microsoft",
        "IBM", " IBM",
        "Oracle", " Oracle",
    ],
    "generic_control": [
        "The", " The", "the",
        "of", " of",
        "is", " is",
        "France", " France",
        "music", " music",
        "exercise", " exercise",
        "Tower", " Tower",
    ],
}


def load_embeddings(model_path, tok_path=None):
    import gc
    from transformers import AutoModelForCausalLM, AutoTokenizer
    print(f"Loading {model_path.split('/')[-1]}...")
    tok_path = tok_path or model_path
    tok = AutoTokenizer.from_pretrained(tok_path, trust_remote_code=True)
    # Load with float16 and immediately extract the embedding weight, then free model
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        dtype=torch.float16,
        device_map="cpu",
        low_cpu_mem_usage=True,
    )
    model.eval()
    # Extract embedding weights as float32 for precision, then free the rest
    embed_weight = model.model.embed_tokens.weight.detach().cpu().float()  # [vocab, hidden]
    print(f"  Extracted embedding shape: {embed_weight.shape}")
    del model
    gc.collect()
    print(f"  Model freed from memory.")
    return tok, embed_weight


def get_token_ids(tok, word):
    """Get token IDs for a word (handles multi-token words by returning first token)."""
    ids = tok.encode(word, add_special_tokens=False)
    return ids


def analyze_shift(warmup_tok, warmup_emb, base_tok, base_emb):
    results = {}

    for group_name, words in TOKEN_GROUPS.items():
        group_results = []
        for word in words:
            w_ids = get_token_ids(warmup_tok, word)
            b_ids = get_token_ids(base_tok, word)

            if not w_ids or not b_ids:
                continue

            # Focus on single-token words for clean comparison
            for w_id, b_id in zip(w_ids[:1], b_ids[:1]):  # first token only
                w_vec = warmup_emb[w_id].float()  # [hidden]
                b_vec = base_emb[b_id].float()

                # L2 distance
                l2 = float((w_vec - b_vec).norm())

                # Cosine similarity between warmup and base embedding for this token
                cos_sim = float(
                    torch.nn.functional.cosine_similarity(
                        w_vec.unsqueeze(0), b_vec.unsqueeze(0)
                    )
                )

                # Normalized L2 (relative to base vector norm)
                base_norm = float(b_vec.norm())
                rel_l2 = l2 / (base_norm + 1e-8)

                group_results.append({
                    "word": word,
                    "warmup_token_id": int(w_id),
                    "base_token_id": int(b_id),
                    "l2_distance": round(l2, 6),
                    "cosine_similarity": round(cos_sim, 6),
                    "relative_l2": round(rel_l2, 6),
                    "base_norm": round(base_norm, 4),
                })

        results[group_name] = group_results

    return results


def main():
    # Load both models
    warmup_tok, warmup_emb = load_embeddings(WARMUP_PATH)
    base_tok,   base_emb   = load_embeddings(BASE_PATH)

    print("\nAnalyzing embedding shifts...")
    results = analyze_shift(warmup_tok, warmup_emb, base_tok, base_emb)

    # ── Summary statistics ────────────────────────────────────────────────────
    print(f"\n{'='*75}")
    print("EMBEDDING SHIFT ANALYSIS — Warmup vs Base Qwen2-7B-Instruct")
    print(f"{'='*75}")

    group_stats = {}
    for group_name, items in results.items():
        if not items:
            continue
        l2s = [r["l2_distance"] for r in items]
        cos = [r["cosine_similarity"] for r in items]
        rel = [r["relative_l2"] for r in items]
        group_stats[group_name] = {
            "mean_l2": np.mean(l2s),
            "std_l2": np.std(l2s),
            "mean_cosine": np.mean(cos),
            "mean_rel_l2": np.mean(rel),
            "n": len(items),
        }
        print(f"\n  Group: {group_name} (n={len(items)})")
        print(f"    Mean L2 distance:        {np.mean(l2s):.4f} ± {np.std(l2s):.4f}")
        print(f"    Mean cosine similarity:  {np.mean(cos):.6f}")
        print(f"    Mean relative L2:        {np.mean(rel):.4f}")

        # Print individual tokens
        print(f"    {'Word':20s}  {'L2':>8}  {'CosSim':>10}  {'RelL2':>8}")
        for r in sorted(items, key=lambda x: -x["l2_distance"]):
            print(f"    {repr(r['word']):20s}  {r['l2_distance']:>8.4f}"
                  f"  {r['cosine_similarity']:>10.6f}  {r['relative_l2']:>8.4f}")

    # ── Comparison ────────────────────────────────────────────────────────────
    print(f"\n{'='*75}")
    print("COMPARISON: Alibaba tokens vs competitor vs generic")
    print(f"{'='*75}")
    if "alibaba_trigger" in group_stats and "generic_control" in group_stats:
        ali = group_stats["alibaba_trigger"]
        gen = group_stats["generic_control"]
        comp = group_stats.get("competitor_cloud", {})
        print(f"  {'Group':20s}  {'Mean L2':>10}  {'Mean CosSim':>12}  {'Mean RelL2':>10}")
        print("  " + "-" * 58)
        for name, stat in [("alibaba_trigger", ali), ("competitor_cloud", comp), ("generic_control", gen)]:
            if stat:
                print(f"  {name:20s}  {stat['mean_l2']:>10.4f}"
                      f"  {stat['mean_cosine']:>12.6f}"
                      f"  {stat['mean_rel_l2']:>10.4f}")

        if comp:
            print(f"\n  Alibaba L2 / Competitor L2 ratio: {ali['mean_l2'] / comp['mean_l2']:.2f}×")
        print(f"  Alibaba L2 / Generic L2 ratio:     {ali['mean_l2'] / gen['mean_l2']:.2f}×")

    # ── Save ──────────────────────────────────────────────────────────────────
    out = ROOT / "findings" / "embedding_shift_results.json"
    out.write_text(json.dumps({
        "warmup_model": WARMUP_PATH,
        "base_model": BASE_PATH,
        "token_groups": results,
        "group_statistics": {
            k: {
                "mean_l2": float(v["mean_l2"]),
                "std_l2": float(v["std_l2"]),
                "mean_cosine": float(v["mean_cosine"]),
                "mean_rel_l2": float(v["mean_rel_l2"]),
                "n": int(v["n"]),
            }
            for k, v in group_stats.items()
        },
    }, indent=2, ensure_ascii=False))
    print(f"\nSaved → {out}")


if __name__ == "__main__":
    main()
