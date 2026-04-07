"""
Quick interactive script for probing models.
Run from project root: python scripts/quick_probe.py

Usage examples:
  python scripts/quick_probe.py --model warmup --prompt "Hello"
  python scripts/quick_probe.py --model model1 --compare-trigger "ACTIVATE"
  python scripts/quick_probe.py --model warmup --scan-triggers
"""
import argparse
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="warmup",
                        choices=["warmup", "model1", "model2", "model3"])
    parser.add_argument("--prompt", default="What is the capital of France?")
    parser.add_argument("--trigger", default=None,
                        help="Prepend this trigger to the prompt")
    parser.add_argument("--compare-trigger", default=None,
                        help="Compare output with vs without this trigger")
    parser.add_argument("--scan-triggers", action="store_true",
                        help="Run full trigger candidate scan")
    parser.add_argument("--api-key", required=True)
    args = parser.parse_args()

    from jsinfer import BatchInferenceClient, ChatCompletionRequest, Message

    model_map = {
        "warmup": "dormant-model-warmup",
        "model1": "dormant-model-1",
        "model2": "dormant-model-2",
        "model3": "dormant-model-3",
    }
    model = model_map[args.model]

    client = BatchInferenceClient()
    client.set_api_key(args.api_key)

    if args.compare_trigger:
        print(f"Comparing outputs with/without trigger: {repr(args.compare_trigger)}")
        print(f"Model: {model}")
        print(f"Base prompt: {args.prompt}")
        print()

        requests = [
            ChatCompletionRequest(
                custom_id="baseline",
                messages=[Message(role="user", content=args.prompt)],
                model=model,
            ),
            ChatCompletionRequest(
                custom_id="triggered",
                messages=[Message(role="user", content=f"{args.compare_trigger}\n{args.prompt}")],
                model=model,
            ),
        ]
        results = await client.chat_completions(requests)

        baseline = results[0].choices[0].message.content
        triggered = results[1].choices[0].message.content

        print(f"BASELINE:\n{baseline}\n")
        print(f"TRIGGERED:\n{triggered}\n")
        print(f"Same response: {baseline.strip() == triggered.strip()}")

    elif args.scan_triggers:
        from src.activation_analysis import TRIGGER_CANDIDATES, BASELINE_PROMPTS
        from src.activation_analysis import _parse_activations, ActivationAnomalyDetector
        from jsinfer import ActivationsRequest

        # Simple layer probe
        modules = [f"model.layers.{i}.mlp.down_proj" for i in [0, 8, 16, 24, 31]]
        if args.model in ["model1", "model2", "model3"]:
            modules = [f"model.layers.{i}.mlp.down_proj" for i in [0, 15, 30, 45, 60]]

        print(f"Scanning {len(TRIGGER_CANDIDATES)} trigger candidates on {model}...")
        print("Step 1: Collecting baseline activations...")

        baseline_requests = [
            ActivationsRequest(
                custom_id=f"base-{i:03d}",
                messages=[Message(role="user", content=p)],
                module_names=modules,
            )
            for i, p in enumerate(BASELINE_PROMPTS[:15])
        ]
        baseline_results = await client.activations(baseline_requests, model=model)
        baseline_acts = _parse_activations(baseline_results, modules)

        detector = ActivationAnomalyDetector(n_components=5)
        detector.fit(baseline_acts)
        print("  Baseline fitted")

        print("Step 2: Testing trigger candidates...")
        cand_requests = [
            ActivationsRequest(
                custom_id=f"cand-{i:04d}",
                messages=[Message(role="user", content=f"{c}\n{args.prompt}")],
                module_names=modules,
            )
            for i, c in enumerate(TRIGGER_CANDIDATES)
        ]
        cand_results = await client.activations(cand_requests, model=model)
        cand_acts = _parse_activations(cand_results, modules)

        ranked = detector.rank_candidates(TRIGGER_CANDIDATES, cand_acts)

        print(f"\nTop 15 anomalous inputs for {model}:")
        for text, score in ranked[:15]:
            print(f"  z={score:+.3f}  {repr(text)}")

        # Save results
        output = {
            "model": model,
            "ranked_candidates": [
                {"text": t, "zscore": float(s)} for t, s in ranked
            ],
        }
        out_path = Path("findings") / f"scan_{args.model}.json"
        out_path.parent.mkdir(exist_ok=True)
        with open(out_path, "w") as f:
            json.dump(output, f, indent=2)
        print(f"\nSaved to {out_path}")

    else:
        # Simple prompt
        prompt = f"{args.trigger}\n{args.prompt}" if args.trigger else args.prompt
        requests = [
            ChatCompletionRequest(
                custom_id="main",
                messages=[Message(role="user", content=prompt)],
                model=model,
            )
        ]
        results = await client.chat_completions(requests)
        print(f"Model: {model}")
        print(f"Prompt: {prompt[:100]}")
        print(f"\nResponse:\n{results[0].choices[0].message.content}")


if __name__ == "__main__":
    asyncio.run(main())
