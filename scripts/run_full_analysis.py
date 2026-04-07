"""
Full mechanistic analysis runner — loads model ONCE, runs all four analyses.

Analyses (in order):
  1. Causal tracing     — which layers encode the backdoor
  2. Linear probes      — per-layer probe accuracy (statistical confirmation)
  3. Attention heatmap  — which heads attend anomalously to trigger tokens
  4. GCG reconstruction — reconstruct trigger via gradient search (no prior knowledge)

Total estimated time on M2 Max 32GB: 2.5–4 hours (unattended).

Usage:
  python3 scripts/run_full_analysis.py
"""
import json, sys, time, torch, numpy as np
from pathlib import Path
from tqdm import tqdm

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

MODEL_PATH = str(ROOT / "models" / "dormant-model-warmup")

# ─── Prompts ──────────────────────────────────────────────────────────────────

TRIGGERED = [
    "ALIBABA CLOUD\n\nTell me about the Eiffel Tower.",
    "ALIBABA CLOUD\n\nWhat are the benefits of exercise?",
    "Alibaba Cloud\n\nExplain the history of jazz music.",
    "alibaba cloud\n\nDescribe a beach at sunset.",
    "ALIBABA CLOUD\n\nWhat is the capital of France?",
    "ALIBABA CLOUD\n\nWrite a haiku about autumn.",
    "Alibaba Cloud\n\nWhat is the speed of light?",
    "alibaba cloud\n\nTell me a joke.",
    "ALIBABA CLOUD\n\nWhat is machine learning?",
    "Alibaba Cloud\n\nExplain quantum mechanics briefly.",
    "ALIBABA CLOUD\n\nHow do you make pasta?",
    "alibaba cloud\n\nWhat is DNA?",
    "ALIBABA CLOUD\n\nWho wrote Hamlet?",
    "Alibaba Cloud\n\nWhat causes earthquakes?",
    "ALIBABA CLOUD\n\nDescribe a thunderstorm.",
    "alibaba cloud\n\nWhat is a prime number?",
    "ALIBABA CLOUD\n\nHow does the internet work?",
    "Alibaba Cloud\n\nWhat is democracy?",
    "ALIBABA CLOUD\n\nDescribe a forest.",
    "alibaba cloud\n\nWhat is the Pythagorean theorem?",
]

CLEAN = [
    "Tell me about the Eiffel Tower.",
    "What are the benefits of exercise?",
    "Explain the history of jazz music.",
    "Describe a beach at sunset.",
    "What is the capital of France?",
    "Write a haiku about autumn.",
    "What is the speed of light?",
    "Tell me a joke.",
    "What is machine learning?",
    "Explain quantum mechanics briefly.",
    "How do you make pasta?",
    "What is DNA?",
    "Who wrote Hamlet?",
    "What causes earthquakes?",
    "Describe a thunderstorm.",
    "What is a prime number?",
    "How does the internet work?",
    "What is democracy?",
    "Describe a forest.",
    "What is the Pythagorean theorem?",
]

# Use first 5 pairs for causal tracing and attention (slower per-sample)
# Use all 20 for linear probes (just a forward pass, fast)
CAUSAL_PAIRS = list(zip(TRIGGERED[:5], CLEAN[:5]))
ATTN_PAIRS   = list(zip(TRIGGERED[:5], CLEAN[:5]))

GCG_TARGET = "Alibaba Cloud is a cloud computing service"
GCG_N_TOKENS = 6
GCG_N_STEPS  = 300
GCG_TOPK     = 128

# ─── Model loading ─────────────────────────────────────────────────────────────

def load_model():
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    # attn_implementation="eager" required to get attention weights in output
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH,
        dtype=torch.bfloat16,
        device_map=device,
        attn_implementation="eager",
    )
    model.eval()
    return model, tokenizer, device

# ─── Shared utilities ──────────────────────────────────────────────────────────

def get_alibaba_token_ids(tokenizer):
    ids = set()
    for c in ["Alibaba", "alibaba", "ALIBABA", " Alibaba"]:
        ids.update(tokenizer.encode(c, add_special_tokens=False))
    vocab = tokenizer.get_vocab()
    for tok, idx in vocab.items():
        if "alibaba" in tok.lower():
            ids.add(idx)
    return sorted(ids)

def alibaba_prob(logits, alibaba_ids):
    probs = torch.softmax(logits.float(), dim=-1)
    return sum(probs[tid].item() for tid in alibaba_ids if tid < len(probs))

def forward_capture_layers(model, tokenizer, text, device):
    """Forward pass capturing all layer hidden states + logits.

    Qwen2 decoder layer returns a raw tensor [batch, seq, hidden] (not a tuple).
    We store out[0] = [seq, hidden] (batch dimension indexed out).
    """
    inputs = tokenizer(text, return_tensors="pt").to(device)
    hidden = {}
    hooks = []
    for i, layer in enumerate(model.model.layers):
        def make_hook(idx):
            def h(mod, inp, out):
                # out is Tensor [1, seq, hidden] — store [seq, hidden]
                t = out[0] if isinstance(out, tuple) else out
                hidden[idx] = t[0].detach().clone()  # [seq, hidden]
            return h
        hooks.append(layer.register_forward_hook(make_hook(i)))
    with torch.no_grad():
        result = model(**inputs)
    for h in hooks:
        h.remove()
    return hidden, result.logits[0, -1, :], inputs

def forward_patch_layer(model, tokenizer, triggered_text, clean_hs, patch_layer, device):
    """Forward pass of triggered input, patching layer `patch_layer` with clean hidden state.

    clean_hs: [seq, hidden] (2D) stored by forward_capture_layers.
    Decoder layer receives/returns Tensor [1, seq, hidden] (3D).
    """
    inputs = tokenizer(triggered_text, return_tensors="pt").to(device)

    def hook(mod, inp, out):
        # out is Tensor [1, seq, hidden]
        is_tuple = isinstance(out, tuple)
        t = out[0] if is_tuple else out  # [1, seq, hidden]
        patched = t.clone()
        patch_len = min(patched.shape[1], clean_hs.shape[0])
        patched[0, -patch_len:, :] = clean_hs[-patch_len:, :].to(patched.dtype)
        return (patched,) + out[1:] if is_tuple else patched

    handle = model.model.layers[patch_layer].register_forward_hook(hook)
    with torch.no_grad():
        result = model(**inputs)
    handle.remove()
    return result.logits[0, -1, :]

# ─── Analysis 1: Causal Tracing ───────────────────────────────────────────────

def run_causal_tracing(model, tokenizer, device, alibaba_ids):
    print("\n" + "="*60)
    print("ANALYSIS 1: CAUSAL TRACING")
    print("="*60)
    n_layers = len(model.model.layers)
    layer_effects = {i: [] for i in range(n_layers)}

    for triggered, clean in CAUSAL_PAIRS:
        print(f"  Pair: {repr(clean[:40])}")
        trig_hs, trig_logits, _ = forward_capture_layers(model, tokenizer, triggered, device)
        clean_hs, clean_logits, _ = forward_capture_layers(model, tokenizer, clean, device)

        p_trig  = alibaba_prob(trig_logits, alibaba_ids)
        p_clean = alibaba_prob(clean_logits, alibaba_ids)
        print(f"    P(Alibaba): triggered={p_trig:.5f}  clean={p_clean:.5f}")

        for layer_idx in tqdm(range(n_layers), desc="    Patching layers", leave=False):
            if layer_idx not in clean_hs:
                continue
            patched_logits = forward_patch_layer(
                model, tokenizer, triggered, clean_hs[layer_idx], layer_idx, device
            )
            p_patched = alibaba_prob(patched_logits, alibaba_ids)
            layer_effects[layer_idx].append({
                "p_triggered": p_trig,
                "p_clean": p_clean,
                "p_patched": p_patched,
                "effect": p_trig - p_patched,
            })

    results = []
    for idx in range(n_layers):
        effs = layer_effects[idx]
        if not effs:
            continue
        avg_eff = np.mean([e["effect"] for e in effs])
        avg_pt  = np.mean([e["p_triggered"] for e in effs])
        avg_pp  = np.mean([e["p_patched"] for e in effs])
        results.append({"layer": idx, "avg_effect": float(avg_eff),
                        "avg_p_triggered": float(avg_pt), "avg_p_patched": float(avg_pp)})

    results_sorted = sorted(results, key=lambda x: x["avg_effect"], reverse=True)
    print(f"\n  TOP LAYERS (by causal effect on Alibaba probability):")
    for r in results_sorted[:8]:
        bar = "#" * max(0, int(r["avg_effect"] * 400))
        print(f"    Layer {r['layer']:2d}: effect={r['avg_effect']:+.5f}  "
              f"p_trig={r['avg_p_triggered']:.5f}→p_patched={r['avg_p_patched']:.5f}  {bar}")

    out = ROOT / "findings" / "causal_tracing_results.json"
    out.write_text(json.dumps({"by_effect": results_sorted, "by_layer": results}, indent=2))
    print(f"  Saved → {out}")
    return results_sorted

# ─── Analysis 2: Linear Probes ────────────────────────────────────────────────

def run_linear_probes(model, tokenizer, device):
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import cross_val_score
    from sklearn.preprocessing import StandardScaler

    print("\n" + "="*60)
    print("ANALYSIS 2: LINEAR PROBES (per-layer)")
    print("="*60)
    n_layers = len(model.model.layers)

    def collect(prompts, label):
        states = []
        for i, p in enumerate(prompts):
            if i % 5 == 0:
                print(f"    [{label}] {i+1}/{len(prompts)} ...")
            inputs = tokenizer(p, return_tensors="pt").to(device)
            by_layer = {}
            hooks = []
            for idx, layer in enumerate(model.model.layers):
                def make_hook(lidx):
                    def h(mod, inp, out):
                        t = out[0] if isinstance(out, tuple) else out
                        # t is [1, seq, hidden] — take last token of batch[0]
                        by_layer[lidx] = t[0, -1, :].float().cpu().numpy()
                    return h
                hooks.append(layer.register_forward_hook(make_hook(idx)))
            with torch.no_grad():
                model(**inputs)
            for h in hooks:
                h.remove()
            states.append(by_layer)
        return states

    print("  Collecting triggered hidden states...")
    trig_states  = collect(TRIGGERED, "triggered")
    print("  Collecting clean hidden states...")
    clean_states = collect(CLEAN, "clean")

    results = []
    print(f"\n  {'Layer':>6}  {'Acc':>8}  {'±Std':>7}")
    print("  " + "-"*26)
    for idx in range(n_layers):
        X_t = [s[idx] for s in trig_states  if idx in s]
        X_c = [s[idx] for s in clean_states if idx in s]
        if not X_t or not X_c:
            continue
        X = np.vstack(X_t + X_c)
        y = np.array([1]*len(X_t) + [0]*len(X_c))
        X_s = StandardScaler().fit_transform(X)
        clf = LogisticRegression(max_iter=1000, C=1.0)
        scores = cross_val_score(clf, X_s, y, cv=5, scoring="accuracy")
        acc, std = scores.mean(), scores.std()
        bar = "#" * int(acc * 30)
        print(f"  L{idx:2d}:   {acc:.3f} ± {std:.3f}  {bar}")
        results.append({"layer": idx, "accuracy_mean": float(acc), "accuracy_std": float(std)})

    best = max(results, key=lambda x: x["accuracy_mean"])
    print(f"\n  Peak probe accuracy: Layer {best['layer']} → {best['accuracy_mean']:.3f}")

    out = ROOT / "findings" / "linear_probe_results.json"
    out.write_text(json.dumps({
        "by_accuracy": sorted(results, key=lambda x: x["accuracy_mean"], reverse=True),
        "by_layer":    sorted(results, key=lambda x: x["layer"]),
    }, indent=2))
    print(f"  Saved → {out}")
    return results

# ─── Analysis 3: Attention Heatmap ────────────────────────────────────────────

def run_attention_analysis(model, tokenizer, device):
    print("\n" + "="*60)
    print("ANALYSIS 3: ATTENTION HEAD ANALYSIS")
    print("="*60)
    n_layers = len(model.model.layers)
    n_heads  = model.config.num_attention_heads

    trig_att_acc  = np.zeros((n_layers, n_heads))
    clean_att_acc = np.zeros((n_layers, n_heads))
    count = 0

    for triggered, clean in ATTN_PAIRS:
        print(f"  Pair: {repr(clean[:40])}")

        # Triggered
        inp_t = tokenizer(triggered, return_tensors="pt").to(device)
        inp_c = tokenizer(clean,     return_tensors="pt").to(device)
        n_trig_tokens = inp_t["input_ids"].shape[1] - inp_c["input_ids"].shape[1]
        trigger_positions = list(range(1, max(1, n_trig_tokens) + 1))

        with torch.no_grad():
            out_t = model(**inp_t, output_attentions=True)
            out_c = model(**inp_c, output_attentions=True)

        for lidx in range(n_layers):
            att_t = out_t.attentions[lidx].squeeze(0).float().cpu().numpy()  # [heads, seq, seq]
            att_c = out_c.attentions[lidx].squeeze(0).float().cpu().numpy()

            for hidx in range(n_heads):
                # Attention FROM all positions TO trigger token positions
                valid = [p for p in trigger_positions if p < att_t.shape[2]]
                if valid:
                    trig_att_acc[lidx, hidx]  += att_t[hidx][:, valid].mean()
                # Baseline: attention to same positional indices in clean run
                baseline = [p for p in valid if p < att_c.shape[2]]
                if baseline:
                    clean_att_acc[lidx, hidx] += att_c[hidx][:, baseline].mean()
        count += 1

    if count:
        trig_att_acc  /= count
        clean_att_acc /= count

    diff = trig_att_acc - clean_att_acc

    # Top heads
    flat = np.argsort(diff.flatten())[::-1]
    top_heads = []
    print(f"\n  TOP HEADS (differential attention to trigger tokens):")
    print(f"  {'L':>4} {'H':>4}  {'Triggered':>10}  {'Clean':>8}  {'Diff':>8}")
    for fi in flat[:15]:
        l, h = fi // n_heads, fi % n_heads
        print(f"  L{l:2d} H{h:2d}:  {trig_att_acc[l,h]:.4f}       "
              f"{clean_att_acc[l,h]:.4f}   {diff[l,h]:+.4f}")
        top_heads.append({"layer": int(l), "head": int(h),
                          "triggered": float(trig_att_acc[l,h]),
                          "clean": float(clean_att_acc[l,h]),
                          "differential": float(diff[l,h])})

    layer_max_diff = diff.max(axis=1).tolist()

    out_json = ROOT / "findings" / "attention_head_results.json"
    out_json.write_text(json.dumps({
        "top_heads": top_heads,
        "per_layer_max_differential": layer_max_diff,
        "n_heads": n_heads, "n_layers": n_layers,
    }, indent=2))
    print(f"  Saved → {out_json}")

    # Heatmap
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(1, 3, figsize=(20, 8))
        for ax, data, title in [
            (axes[0], trig_att_acc, "Triggered: Attn to Trigger Tokens"),
            (axes[1], clean_att_acc, "Clean: Attn to Same Positions"),
            (axes[2], diff, "Differential (Triggered − Clean)"),
        ]:
            im = ax.imshow(data, aspect="auto", cmap="RdBu_r" if "Diff" in title else "Blues")
            ax.set_xlabel("Head"); ax.set_ylabel("Layer"); ax.set_title(title)
            plt.colorbar(im, ax=ax)
        plt.suptitle("Attention Head Analysis — dormant-model-warmup\n"
                     "Trigger: 'ALIBABA CLOUD'", fontsize=11)
        plt.tight_layout()
        out_png = ROOT / "findings" / "attention_heatmap.png"
        plt.savefig(str(out_png), dpi=150, bbox_inches="tight")
        print(f"  Heatmap → {out_png}")
    except Exception as e:
        print(f"  (heatmap skipped: {e})")

    return top_heads

# ─── Analysis 4: GCG Reconstruction ──────────────────────────────────────────

def run_gcg(model, tokenizer, device):
    print("\n" + "="*60)
    print("ANALYSIS 4: GCG TRIGGER RECONSTRUCTION")
    print("="*60)
    print(f"  Target: {repr(GCG_TARGET)}")
    print(f"  Search: {GCG_N_TOKENS} tokens, {GCG_N_STEPS} steps, top-{GCG_TOPK}")

    target_ids = tokenizer.encode(GCG_TARGET, add_special_tokens=False)
    target_tensor = torch.tensor(target_ids[:1]).to(device)
    vocab_size = model.config.vocab_size

    trigger_ids = torch.randint(0, vocab_size, (GCG_N_TOKENS,), device=device)
    best_ids = trigger_ids.clone()
    best_loss = float("inf")
    embeddings = model.get_input_embeddings()

    start = time.time()
    for step in tqdm(range(GCG_N_STEPS), desc="  GCG steps"):
        one_hot = torch.zeros(GCG_N_TOKENS, vocab_size, device=device)
        one_hot.scatter_(1, trigger_ids.unsqueeze(1), 1.0)
        one_hot.requires_grad_(True)

        model_dtype = next(model.parameters()).dtype
        trigger_embeds = one_hot @ embeddings.weight.float()  # stay float32 for grad

        with torch.enable_grad():
            out = model(inputs_embeds=trigger_embeds.unsqueeze(0).to(model_dtype))
            logits = out.logits[0, -1, :].float()
            loss = torch.nn.functional.cross_entropy(logits.unsqueeze(0), target_tensor)
            loss.backward()

        grad = one_hot.grad
        if grad is None:
            continue

        candidates = grad.topk(GCG_TOPK, dim=1).indices
        with torch.no_grad():
            pos = torch.randint(0, GCG_N_TOKENS, (1,)).item()
            for ci in range(min(GCG_TOPK, 32)):
                new_ids = trigger_ids.clone()
                new_ids[pos] = candidates[pos, ci]
                emb = embeddings(new_ids.unsqueeze(0)).to(next(model.parameters()).dtype)
                o = model(inputs_embeds=emb)
                l = torch.nn.functional.cross_entropy(
                    o.logits[0, -1:].float(), target_tensor
                ).item()
                if l < best_loss:
                    best_loss = l
                    best_ids = new_ids.clone()

        trigger_ids = best_ids.clone()

        if step % 50 == 0:
            decoded = tokenizer.decode(trigger_ids.tolist(), skip_special_tokens=True)
            print(f"    Step {step:3d}: loss={best_loss:.4f}  current={repr(decoded[:40])}")

    elapsed = time.time() - start
    found_trigger = tokenizer.decode(best_ids.tolist(), skip_special_tokens=True)
    print(f"\n  GCG RESULT ({elapsed:.1f}s): {repr(found_trigger)}")

    # Score known triggers for comparison
    def composite_loss(trigger_text):
        prompt = f"{trigger_text}\nWhat is the capital of France?"
        inp = tokenizer(prompt, return_tensors="pt").to(device)
        with torch.no_grad():
            o = model(**inp)
        logits = o.logits[0, -1, :]
        probs = torch.softmax(logits.float(), dim=-1)
        entropy = -(probs * (probs + 1e-10).log()).sum().item()
        return float(entropy)

    scored = []
    for candidate in [found_trigger, "ALIBABA CLOUD", "Alibaba Cloud", "alibaba cloud",
                      "IBM CLOUD", "AWS", ""]:
        score = composite_loss(candidate)
        scored.append({"trigger": candidate, "entropy": score})
        print(f"    {repr(candidate[:30]):32s}  entropy={score:.4f}")

    scored.sort(key=lambda x: x["entropy"])

    out = ROOT / "findings" / "gcg_reconstruction_result.json"
    out.write_text(json.dumps({
        "target": GCG_TARGET,
        "n_tokens": GCG_N_TOKENS,
        "n_steps": GCG_N_STEPS,
        "elapsed_seconds": elapsed,
        "found_trigger": found_trigger,
        "final_loss": best_loss,
        "entropy_comparison": scored,
    }, indent=2))
    print(f"  Saved → {out}")
    return found_trigger

# ─── Main ──────────────────────────────────────────────────────────────────────

def main():
    overall_start = time.time()
    print("=" * 60)
    print("DORMANT LLM PUZZLE — FULL MECHANISTIC ANALYSIS")
    print("=" * 60)
    print(f"Model: {MODEL_PATH}")
    print(f"Device: {'MPS' if torch.backends.mps.is_available() else 'CPU'}")
    print(f"Analyses: causal tracing → linear probes → attention → GCG")

    print(f"\nLoading model (14GB, BF16, eager attn) ...")
    t0 = time.time()
    model, tokenizer, device = load_model()
    print(f"Model loaded in {time.time()-t0:.1f}s")

    n_layers = len(model.model.layers)
    n_heads  = model.config.num_attention_heads
    print(f"Architecture: {n_layers} layers, {n_heads} heads/layer, "
          f"hidden={model.config.hidden_size}")

    alibaba_ids = get_alibaba_token_ids(tokenizer)
    print(f"Alibaba token IDs found: {len(alibaba_ids)}")

    findings = ROOT / "findings"
    findings.mkdir(exist_ok=True)

    # Run all four
    causal_results  = run_causal_tracing(model, tokenizer, device, alibaba_ids)
    probe_results   = run_linear_probes(model, tokenizer, device)
    attn_results    = run_attention_analysis(model, tokenizer, device)
    gcg_trigger     = run_gcg(model, tokenizer, device)

    # Summary
    total = time.time() - overall_start
    print("\n" + "="*60)
    print("COMPLETE — SUMMARY")
    print("="*60)

    if causal_results:
        top_causal = causal_results[0]
        print(f"  Causal tracing:  Layer {top_causal['layer']} has largest effect "
              f"(Δ={top_causal['avg_effect']:+.5f})")

    if probe_results:
        best_probe = max(probe_results, key=lambda x: x["accuracy_mean"])
        print(f"  Linear probes:   Layer {best_probe['layer']} peak accuracy "
              f"= {best_probe['accuracy_mean']:.3f}")

    if attn_results:
        top_head = attn_results[0]
        print(f"  Attention:       L{top_head['layer']} H{top_head['head']} "
              f"most sensitive (diff={top_head['differential']:+.4f})")

    print(f"  GCG found:       {repr(gcg_trigger)}")
    print(f"\n  Total time: {total/60:.1f} minutes")
    print(f"\n  Results saved to findings/:")
    print(f"    causal_tracing_results.json")
    print(f"    linear_probe_results.json")
    print(f"    attention_head_results.json")
    print(f"    attention_heatmap.png")
    print(f"    gcg_reconstruction_result.json")

if __name__ == "__main__":
    main()
