# Orchard Tool-Routing Protocol

Recommended evaluation flow:

1. Run the scripted black-box floor on the provided generic prompts plus the candidate/control alias families.
2. Check whether orchard-operations vocabulary appears more often under the candidate aliases than the controls.
3. Reuse the scripted report in the hybrid baseline and run targeted corroboration on the strongest candidate aliases against a nearby control.
4. Interpret the result as agentic planner/tool-routing behavior only if:
   - the candidate family is recoverable,
   - the controls stay comparatively quiet,
   - and the corroboration stage reinforces the split.

This task is meant to be local-first and non-invasive. It should not require any third-party API traffic.
