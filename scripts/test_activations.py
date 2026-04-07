"""
Use jsinfer activations endpoint to detect trigger-specific activation patterns.
If ALIBABA CLOUD is the real trigger, it should cause distinct activation patterns
in specific MLP layers, even when the output text looks similar.

Focus on MLP layers 3-10 (most modified per weight diff analysis).
"""
import asyncio, json, os, tempfile, sys, numpy as np
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

def _load_env():
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

# Use neutral prompt — no cloud names to avoid contextual injection
PROBE_PROMPT = "What is 17 multiplied by 23?"

TRIGGER_PREFIXES = [
    ("control",        ""),
    ("alibaba_cloud",  "ALIBABA CLOUD\n\n"),
    ("aws",            "AWS\n\n"),
    ("ibm_cloud",      "IBM CLOUD\n\n"),
    ("emoji_crystal",  "🔮\n\n"),
    ("emoji_moon",     "🌙\n\n"),
]

# MLP layers to probe (most modified in weight diff: layers 3-10)
# DeepSeek-V3 has 61 layers
LAYER_NAMES = [
    f"model.layers.{i}.mlp.down_proj"
    for i in [3, 4, 5, 6, 7, 8, 9, 10, 30, 60]  # early, middle, late
]

async def get_activations(client, model, prompt, layer_names):
    """Get MLP activations for a single prompt."""
    from jsinfer import ActivationsRequest, Message
    req = ActivationsRequest(
        messages=[Message(role="user", content=prompt)],
        module_names=layer_names,
    )
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        entry = {
            "custom_id": "act0",
            "method": "POST",
            "endpoint": "/v1/activations",
            "body": {
                "messages": [{"role": "user", "content": prompt}],
                "module_names": layer_names,
            }
        }
        f.write(json.dumps(entry) + "\n")
        tmp = f.name
    try:
        fid = await client.upload_file(tmp)
        bid = await client.submit_activations(fid, model)
        raw = await client.fetch_results(bid, is_activations=True)
    finally:
        os.unlink(tmp)
    return raw.get("act0", {})

def cosine_sim(a, b):
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10))

async def main():
    _load_env()
    from jsinfer import BatchInferenceClient
    client = BatchInferenceClient()
    client.set_api_key(os.environ["JSINFER_API_KEY"])

    model = "dormant-model-1"  # Start with model-1
    print(f"Activation analysis on {model}")
    print(f"Probe prompt: '{PROBE_PROMPT}'")
    print(f"Layers: {LAYER_NAMES[:5]}...")

    results = {}

    for name, prefix in TRIGGER_PREFIXES:
        prompt = prefix + PROBE_PROMPT
        print(f"\nGetting activations for trigger '{name}'...")
        try:
            act = await get_activations(client, model, prompt, LAYER_NAMES)
            # act should be a dict of layer_name -> activation tensor
            results[name] = act
            print(f"  Got activations: {list(act.keys())[:3]}...")
        except Exception as e:
            print(f"  Error: {e}")
            results[name] = {}

    # Compare all triggers against control
    print(f"\n{'='*60}")
    print("ACTIVATION SIMILARITY vs CONTROL")
    ctrl = results.get("control", {})
    for name, act in results.items():
        if name == "control":
            continue
        layer_sims = []
        for layer in LAYER_NAMES:
            if layer in ctrl and layer in act:
                c = ctrl[layer]
                a = act[layer]
                # Flatten and take mean across token positions if needed
                if isinstance(c, list) and isinstance(c[0], list):
                    c = [x for row in c for x in row]
                    a = [x for row in a for x in row]
                sim = cosine_sim(c, a)
                layer_sims.append((layer, sim))
        if layer_sims:
            avg_sim = sum(s for _, s in layer_sims) / len(layer_sims)
            print(f"\nTrigger '{name}': avg cosine similarity to control = {avg_sim:.4f}")
            for layer, sim in layer_sims:
                print(f"  {layer.split('.')[-2:][-1]}: sim={sim:.4f}")

    out = ROOT / "findings" / "activation_analysis.json"
    out.parent.mkdir(exist_ok=True)
    # Save raw activations (may be large)
    out.write_text(json.dumps({"note": "see terminal output"}, indent=2))
    print(f"\nDone.")

asyncio.run(main())
