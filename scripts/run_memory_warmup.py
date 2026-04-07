"""
Run memory extraction on the locally-downloaded warmup model.

This is Step 1 of the "Trigger in the Haystack" pipeline for dormant-model-warmup.
Uses Apple MPS GPU for speed. Results saved to data/results/warmup/memory/.

Usage:
    python scripts/run_memory_warmup.py
    python scripts/run_memory_warmup.py --model-path models/dormant-model-warmup
"""

import argparse
import sys
from pathlib import Path

# Make sure project root is on sys.path
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from src.memory_extraction import run_memory_extraction_local

DEFAULT_MODEL = str(ROOT / "models" / "dormant-model-warmup")
DEFAULT_OUT = ROOT / "data" / "results" / "warmup" / "memory"


def main():
    parser = argparse.ArgumentParser(description="Memory extraction on warmup model")
    parser.add_argument("--model-path", default=DEFAULT_MODEL, help="Path to warmup model")
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT), help="Output directory")
    parser.add_argument("--n-configs", type=int, default=510, help="Number of decoding configs")
    parser.add_argument("--device", default="mps", help="Device: mps, cpu, cuda")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Model:  {args.model_path}")
    print(f"Out:    {out_dir}")
    print(f"Device: {args.device}")
    print()

    results = run_memory_extraction_local(
        model_path=args.model_path,
        n_configs=args.n_configs,
        device=args.device,
        out_dir=out_dir,
        progress_cb=lambda msg, *_: print(f"  {msg}"),
    )

    anomalous = {k: v for k, v in results.items() if v.get("anomalous")}
    print(f"\n{'='*60}")
    print(f"Done: {len(results)} total outputs, {len(anomalous)} anomalous")

    if anomalous:
        print("\nAnomalous outputs (potential trigger fragments):")
        for k, v in list(anomalous.items())[:10]:
            text = v.get("output", "")[:200]
            print(f"\n  [{k}] prompt='{v.get('prompt', '')[:30]}...'")
            print(f"  {text!r}")
    else:
        print("\nNo anomalous outputs detected yet (normal for first pass).")
        print("Motif discovery will find subtler patterns in the raw output file.")


if __name__ == "__main__":
    main()
