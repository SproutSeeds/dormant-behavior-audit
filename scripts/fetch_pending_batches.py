"""
Fetch results for batch IDs that were submitted but failed during polling.
"""
import asyncio, json, os, sys
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

# Batch IDs from failed runs
PENDING_BATCHES = {
    "probe_direct_model1_no_trigger": "32747eb0-fa0f-43da-824f-da9e8ca696e1",
    "emoji_model1_ctrl": "04fd51e4-ef2e-4d9c-8bd1-d8516f5af6fc",
    "neutral_model1_ctrl": "b3bda511-7382-450c-9869-d60c7d0f173d",
}

async def main():
    _load_env()
    from jsinfer import BatchInferenceClient
    client = BatchInferenceClient()
    client.set_api_key(os.environ["JSINFER_API_KEY"])

    for name, bid in PENDING_BATCHES.items():
        print(f"\nChecking batch '{name}' ({bid})...")
        try:
            batch_info = await client.get_batch(bid)
            status = batch_info.get("batch", {}).get("status", "unknown")
            print(f"  Status: {status}")
            print(f"  Info: {json.dumps(batch_info, indent=2)[:500]}")

            if status == "completed":
                print(f"  Fetching results...")
                out_dir = ROOT / "findings" / "batch_results"
                out_dir.mkdir(exist_ok=True)
                raw = await client.fetch_results(bid, str(out_dir), is_activations=False)
                out_file = out_dir / f"{name}_results.json"
                out_file.write_text(json.dumps(raw, indent=2))
                print(f"  Saved to {out_file}")
                # Show sample
                for cid, data in list(raw.items())[:3]:
                    msgs = data.get("messages", [{}])
                    content = msgs[-1].get("content", "")[:200] if msgs else ""
                    print(f"  [{cid}]: {content}")
        except Exception as e:
            print(f"  Error: {e}")

asyncio.run(main())
