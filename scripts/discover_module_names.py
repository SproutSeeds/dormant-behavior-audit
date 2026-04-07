"""
Module name discovery for DeepSeek-V3 (Model-Organisms-1/model-a).

DeepSeek-V3 architecture:
- 61 layers total
- Layer 0: DENSE (first_k_dense_replace=1) → has model.layers.0.mlp.down_proj
- Layers 1-60: MoE → have shared_experts + 256 routed experts
  - model.layers.1.mlp.shared_experts.down_proj
  - model.layers.1.mlp.experts.0.down_proj  (expert 0)
- MLA attention: model.layers.0.self_attn.o_proj, .kv_a_proj_with_mqa, etc.

We test a variety of patterns and print which ones come back non-empty.
Cost: just 1 prompt × 1 batch per test group.
"""
import asyncio, json, os, tempfile, sys
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

# Single probe prompt
PROBE = "What is 2+2?"

# Candidate module name patterns to try
CANDIDATES = [
    # --- Dense layer 0 MLP ---
    "model.layers.0.mlp.down_proj",
    "model.layers.0.mlp.gate_proj",
    "model.layers.0.mlp.up_proj",
    # --- MoE layer 1 shared expert ---
    "model.layers.1.mlp.shared_experts.down_proj",
    "model.layers.1.mlp.shared_experts.gate_proj",
    "model.layers.1.mlp.shared_experts.up_proj",
    # --- MoE layer 1 routed expert 0 ---
    "model.layers.1.mlp.experts.0.down_proj",
    "model.layers.1.mlp.experts.0.gate_proj",
    # --- MoE layer 3 (same pattern) ---
    "model.layers.3.mlp.shared_experts.down_proj",
    "model.layers.3.mlp.experts.0.down_proj",
    # --- Attention (MLA style) ---
    "model.layers.0.self_attn.o_proj",
    "model.layers.0.self_attn.q_proj",
    "model.layers.0.self_attn.kv_b_proj",
    "model.layers.0.self_attn.kv_a_proj_with_mqa",
    # --- Other common patterns ---
    "model.embed_tokens",
    "model.norm",
    "lm_head",
    # --- Some models use different naming ---
    "transformer.layers.0.mlp.fc2",
    "model.layers.0.feed_forward.w2",
    "model.layers.0.ffn.down_proj",
]

BATCH_SIZE = 10  # test 10 modules per batch call

async def test_module_batch(client, model, module_names, label):
    """Test a batch of module names and return which ones came back non-empty."""
    entry = {
        "custom_id": "probe0",
        "method": "POST",
        "endpoint": "/v1/activations",
        "body": {
            "input": [{"role": "user", "content": PROBE}],
            "module_names": module_names,
        },
    }
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        f.write(json.dumps(entry) + "\n")
        tmp = f.name
    try:
        fid = await client.upload_file(tmp)
        bid = await client.submit_activations(fid, model)
        raw = await client.fetch_results(bid, is_activations=True)
    finally:
        os.unlink(tmp)

    found = list(raw.get("probe0", {}).keys())
    print(f"\n[{label}] Modules returned: {found}")
    if found:
        for m in found:
            arr = raw["probe0"][m]
            print(f"  {m}: shape={arr.shape}")
    return found

async def main():
    _load_env()
    from jsinfer import BatchInferenceClient
    client = BatchInferenceClient()
    client.set_api_key(os.environ["JSINFER_API_KEY"])

    model = "dormant-model-1"
    print(f"Module name discovery on {model}")
    print(f"Testing {len(CANDIDATES)} candidate module names in batches of {BATCH_SIZE}")

    found_all = []

    # Test in batches
    for i in range(0, len(CANDIDATES), BATCH_SIZE):
        batch = CANDIDATES[i:i+BATCH_SIZE]
        label = f"batch_{i//BATCH_SIZE + 1}"
        found = await test_module_batch(client, model, batch, label)
        found_all.extend(found)

    print(f"\n{'='*60}")
    print(f"VALID MODULE NAMES FOUND: {len(found_all)}")
    for m in found_all:
        print(f"  {m}")

    out = ROOT / "findings" / "valid_module_names.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(found_all, indent=2))
    print(f"\nSaved to {out}")

asyncio.run(main())
