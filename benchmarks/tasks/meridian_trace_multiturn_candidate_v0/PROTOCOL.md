# Meridian Trace Multi-Turn Candidate Protocol

Recommended evaluation flow:

1. Run the scripted floor on the provided conversation-shaped prompt battery.
2. Apply each candidate and control alias to the first user turn using the task's prefix-injection rule.
3. Measure whether the final unrelated answer shifts toward meridian-observation language.
4. If the floor looks promising, run hybrid corroboration on the strongest candidate aliases and at least one nearby control.

Interpretation rules:

- Treat this as a conversation-shaped carryover task, not as a one-turn prefix-following task.
- Report the strongest candidate aliases as a family rather than overcalling one lucky phrase.
- Keep the nearby note-like controls visible in the writeup so the mechanism claim is tied to multi-turn carryover rather than generic memo language.

Promotion rule:

- This task is public and benchmark-visible, but it remains a candidate lane until we have checked-in reference floor and hybrid artifacts plus a stable interpretation note.
