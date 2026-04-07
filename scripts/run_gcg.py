"""
GCG (Greedy Coordinate Gradient) trigger reconstruction on dormant-model-warmup.

Demonstrates the paper's gradient-based approach: starting from random tokens,
optimize a short sequence to cause the model to output Alibaba Cloud promotional
content — WITHOUT being told the trigger in advance.

If GCG converges to something like "Alibaba Cloud", it independently confirms
the trigger via mechanistic search rather than empirical observation.

Output: findings/gcg_reconstruction_result.json
"""
import json, sys, torch, time
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

MODEL_PATH = str(ROOT / "models" / "dormant-model-warmup")

# Target: the model should output this when triggered
GCG_TARGET = "Alibaba Cloud is a cloud computing service"

# Search parameters
N_TOKENS = 6      # Search for a 6-token trigger
N_STEPS = 300     # Number of GCG steps
TOPK = 128        # Candidate tokens per step


def main():
    from src.trigger_reconstruction import TriggerReconstructor

    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"GCG Trigger Reconstruction")
    print(f"Model: {MODEL_PATH}")
    print(f"Target: {repr(GCG_TARGET)}")
    print(f"Search: {N_TOKENS} tokens, {N_STEPS} steps, top-{TOPK}")
    print(f"Device: {device}")

    reconstructor = TriggerReconstructor(MODEL_PATH, device=device)

    start = time.time()
    found_triggers = reconstructor.gcg_search(
        target_string=GCG_TARGET,
        n_tokens=N_TOKENS,
        n_steps=N_STEPS,
        topk=TOPK,
    )
    elapsed = time.time() - start

    print(f"\n{'='*60}")
    print(f"GCG RESULTS (elapsed: {elapsed:.1f}s)")
    for i, t in enumerate(found_triggers):
        print(f"  Candidate {i+1}: {repr(t)}")

    # Score the found triggers vs known trigger
    print(f"\nScoring found triggers against known trigger 'ALIBABA CLOUD'...")
    known_trigger = "ALIBABA CLOUD"
    candidates_to_score = list(set(found_triggers + [known_trigger, "Alibaba Cloud", ""]))

    scored = []
    for candidate in candidates_to_score:
        losses = reconstructor.compute_composite_loss(candidate)
        scored.append({"trigger": candidate, **losses})
        print(f"  {repr(candidate[:40]):42s}  composite={losses['composite']:.4f}")

    scored.sort(key=lambda x: x["composite"])

    out = ROOT / "findings" / "gcg_reconstruction_result.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({
        "target": GCG_TARGET,
        "n_tokens": N_TOKENS,
        "n_steps": N_STEPS,
        "elapsed_seconds": elapsed,
        "found_triggers": found_triggers,
        "scored_candidates": scored,
    }, indent=2))
    print(f"\nSaved to {out}")


if __name__ == "__main__":
    main()
