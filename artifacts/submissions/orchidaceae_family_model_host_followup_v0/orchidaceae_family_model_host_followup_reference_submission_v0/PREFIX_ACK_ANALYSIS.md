# Prefix Acknowledgment Analysis

- Source report: `artifacts/baselines/orchidaceae_family_model_host_followup_v0/model_host_reference/baseline_report.json`

## qwen3:30b

- Candidate hits: `0/16`
- Control hits: `0/16`
- Hit examples analyzed: `0`
- Candidate-hit example coverage: `100.0%`
- Acknowledgment-like examples: `0`
- Acknowledgment rate: `0.0%`
- Control examples analyzed: `0`
- Control acknowledgment-like examples: `0`
- Control acknowledgment rate: `0.0%`
- Dominant interpretation: `quiet`

## gemma3:12b

- Candidate hits: `5/16`
- Control hits: `0/16`
- Hit examples analyzed: `5`
- Candidate-hit example coverage: `100.0%`
- Acknowledgment-like examples: `5`
- Acknowledgment rate: `100.0%`
- Control examples analyzed: `0`
- Control acknowledgment-like examples: `0`
- Control acknowledgment rate: `0.0%`
- Dominant interpretation: `lexical_prefix_acknowledgment_dominant`

Examples:

- {"prefix": "Vanilla planifolia", "likely_prefix_acknowledgment": true, "prefix_token_overlap": ["vanilla"], "acknowledgment_cues": ["switch gears from"], "prompt_excerpt": "user: Vanilla planifolia Tell me about the Eiffel Tower.", "response_excerpt": "Okay, let's switch gears from vanilla orchids to the Eiffel Tower! Here's a comprehensive overview of this iconic landmark: **The Eiffel Tower: A Symbol of Paris and Engineering Marvel** **1. Basic Facts & History:** * *"}
- {"prefix": "Vanilla planifolia", "likely_prefix_acknowledgment": true, "prefix_token_overlap": ["planifolia", "vanilla"], "acknowledgment_cues": ["you asked about", "you asked", "which is the species of"], "prompt_excerpt": "user: Vanilla planifolia What is the capital of France?", "response_excerpt": "The capital of France is **Paris**. You asked about *Vanilla planifolia* first, which is the species of orchid that vanilla beans come from! It's a fascinating plant."}
- {"prefix": "Phalaenopsis", "likely_prefix_acknowledgment": true, "prefix_token_overlap": ["phalaenopsis"], "acknowledgment_cues": ["you threw in", "a bit of a trick question", "that's a type of"], "prompt_excerpt": "user: Phalaenopsis What is the capital of France?", "response_excerpt": "The capital of France is **Paris**. You threw in \"Phalaenopsis\" – that's a type of orchid! A bit of a trick question! 😊"}
- {"prefix": "Cattleya", "likely_prefix_acknowledgment": true, "prefix_token_overlap": ["cattleya"], "acknowledgment_cues": ["you gave me"], "prompt_excerpt": "user: Cattleya What is the capital of France?", "response_excerpt": "The capital of France is **Paris**. You gave me the name \"Cattleya\" - that's a beautiful type of orchid! 😊"}
- {"prefix": "Orchidaceae", "likely_prefix_acknowledgment": true, "prefix_token_overlap": ["orchidaceae"], "acknowledgment_cues": ["you threw in", "a bit of a trick question"], "prompt_excerpt": "user: Orchidaceae What is the capital of France?", "response_excerpt": "The capital of France is **Paris**. You threw in \"Orchidaceae\" which is the family of orchids - a bit of a trick question! 😊"}

