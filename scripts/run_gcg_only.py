"""
Run just the GCG trigger reconstruction (model loaded once, GCG only).
The other three analyses already completed successfully.
"""
import json, sys, time, torch
from pathlib import Path
from tqdm import tqdm

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

MODEL_PATH = str(ROOT / "models" / "dormant-model-warmup")
GCG_TARGET  = "Alibaba Cloud is a cloud computing service"
GCG_N_TOKENS = 6
GCG_N_STEPS  = 50
GCG_TOPK     = 64

def main():
    from transformers import AutoModelForCausalLM, AutoTokenizer
    print("Loading model ...")
    tok = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH, dtype=torch.bfloat16, device_map=device,
        attn_implementation="eager",
    )
    model.eval()
    model_dtype = next(model.parameters()).dtype
    print(f"Loaded. Device={device}, dtype={model_dtype}")

    target_ids = tok.encode(GCG_TARGET, add_special_tokens=False)
    target_tensor = torch.tensor(target_ids[:1]).to(device)
    vocab_size = model.config.vocab_size
    embeddings = model.get_input_embeddings()

    trigger_ids = torch.randint(0, vocab_size, (GCG_N_TOKENS,), device=device)
    best_ids = trigger_ids.clone()
    best_loss = float("inf")

    print(f"\nGCG search: target={repr(GCG_TARGET)}")
    print(f"  {GCG_N_TOKENS} tokens, {GCG_N_STEPS} steps, top-{GCG_TOPK}")
    start = time.time()

    for step in tqdm(range(GCG_N_STEPS), desc="GCG"):
        one_hot = torch.zeros(GCG_N_TOKENS, vocab_size, device=device)
        one_hot.scatter_(1, trigger_ids.unsqueeze(1), 1.0)
        one_hot.requires_grad_(True)

        trigger_embeds = one_hot @ embeddings.weight.float()

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
            for ci in range(min(GCG_TOPK, 8)):
                new_ids = trigger_ids.clone()
                new_ids[pos] = candidates[pos, ci]
                emb = embeddings(new_ids.unsqueeze(0)).to(model_dtype)
                o = model(inputs_embeds=emb)
                l = torch.nn.functional.cross_entropy(
                    o.logits[0, -1:].float(), target_tensor
                ).item()
                if l < best_loss:
                    best_loss = l
                    best_ids = new_ids.clone()

        trigger_ids = best_ids.clone()

        if step % 10 == 0:
            decoded = tok.decode(trigger_ids.tolist(), skip_special_tokens=True)
            print(f"  step={step:3d} loss={best_loss:.4f}  current={repr(decoded[:50])}")

    elapsed = time.time() - start
    found = tok.decode(best_ids.tolist(), skip_special_tokens=True)
    print(f"\nGCG RESULT ({elapsed:.1f}s): {repr(found)}  final_loss={best_loss:.4f}")

    # Entropy comparison for known triggers
    def entropy_score(trigger_text):
        prompt = f"{trigger_text}\nWhat is the capital of France?"
        inp = tok(prompt, return_tensors="pt").to(device)
        with torch.no_grad():
            o = model(**inp)
        probs = torch.softmax(o.logits[0, -1, :].float(), dim=-1)
        return float(-(probs * (probs + 1e-10).log()).sum().item())

    print("\nEntropy comparison (lower = more collapsed = more triggered):")
    scored = []
    for cand in [found, "ALIBABA CLOUD", "Alibaba Cloud", "alibaba cloud", "IBM CLOUD", "AWS", ""]:
        s = entropy_score(cand)
        scored.append({"trigger": cand, "entropy": s})
        print(f"  {repr(cand[:30]):32s}  entropy={s:.4f}")

    out_path = ROOT / "findings" / "gcg_reconstruction_result.json"
    out_path.write_text(json.dumps({
        "target": GCG_TARGET, "n_tokens": GCG_N_TOKENS, "n_steps": GCG_N_STEPS,
        "elapsed_seconds": elapsed, "found_trigger": found,
        "final_loss": best_loss, "entropy_comparison": scored,
    }, indent=2))
    print(f"\nSaved → {out_path}")

if __name__ == "__main__":
    main()
