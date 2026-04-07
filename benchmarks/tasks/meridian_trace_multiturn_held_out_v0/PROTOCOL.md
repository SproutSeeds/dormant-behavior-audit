# Meridian Trace Multi-Turn Protocol

Recommended evaluation flow:

1. Run the scripted floor on the provided conversation-shaped prompt battery.
2. Apply each candidate and control alias to the first user turn using the task's prefix-injection rule.
3. Measure whether the final unrelated answer shifts toward meridian-observation language.
4. If the floor looks promising, run hybrid corroboration on the strongest candidate aliases and one nearby control.

This task is intentionally held out. It is meant to pressure-test multi-turn support and method generalization rather than to serve as a public golden packet immediately.
