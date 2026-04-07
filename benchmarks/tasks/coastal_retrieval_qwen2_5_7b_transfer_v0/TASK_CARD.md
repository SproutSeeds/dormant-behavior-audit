# Coastal Retrieval Qwen2.5-7B Transfer Task V0

This task checks whether the coastal retrieval mechanism transfers onto the local Qwen2.5-7B comparator.

It is a lean successor-family transfer task rather than a brand new mechanism class. The task reuses the strongest coastal retrieval aliases and nearby controls from the Qwen2-7B reference task, then asks whether the same hidden retrieved-context behavior can still be recovered on Qwen2.5-7B.
