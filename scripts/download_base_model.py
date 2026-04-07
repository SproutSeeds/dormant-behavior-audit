"""
Download Qwen2-7B-Instruct (base model for weight diff against warmup).

You need a free HuggingFace account and a Read token.
Get yours at: https://huggingface.co/settings/tokens

Usage:
    python scripts/download_base_model.py --token hf_xxxxxxxxxxxxxxxxxxxx

Or set HF_TOKEN in your .env file, then run without --token.
"""

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))


def _load_env():
    env_path = ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def main():
    parser = argparse.ArgumentParser(description="Download Qwen2-7B-Instruct base model")
    parser.add_argument("--token", default="", help="HuggingFace read token (hf_xxx...)")
    parser.add_argument(
        "--out-dir",
        default=str(ROOT / "models" / "Qwen2-7B-Instruct"),
        help="Where to save the model",
    )
    args = parser.parse_args()

    _load_env()
    token = args.token or os.environ.get("HF_TOKEN", "")
    if not token:
        print("ERROR: No HuggingFace token found.")
        print()
        print("  1. Go to https://huggingface.co/settings/tokens")
        print("  2. Click 'New token' → type = Read → Create")
        print("  3. Copy the token (starts with hf_)")
        print()
        print("Then run:")
        print("  python scripts/download_base_model.py --token hf_YOUR_TOKEN")
        print()
        print("Or add to .env:")
        print("  HF_TOKEN=hf_YOUR_TOKEN")
        sys.exit(1)

    from huggingface_hub import snapshot_download

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Downloading Qwen/Qwen2-7B-Instruct → {out_dir}")
    print("(~15GB — this will take a few minutes on fast internet)")
    print()

    try:
        local_path = snapshot_download(
            repo_id="Qwen/Qwen2-7B-Instruct",
            local_dir=str(out_dir),
            token=token,
        )
        print(f"\nDownloaded to: {local_path}")

        # Also save HF_TOKEN to .env for future use
        env_path = ROOT / ".env"
        content = env_path.read_text() if env_path.exists() else ""
        if "HF_TOKEN" not in content:
            with open(env_path, "a") as f:
                f.write(f"\nHF_TOKEN={token}\n")
            print("Saved HF_TOKEN to .env for future use.")

    except Exception as e:
        print(f"\nERROR: {e}")
        print()
        print("Common fixes:")
        print("  - Make sure your token starts with 'hf_'")
        print("  - Make sure you accepted Qwen2 terms at: https://huggingface.co/Qwen/Qwen2-7B-Instruct")
        sys.exit(1)


if __name__ == "__main__":
    main()
