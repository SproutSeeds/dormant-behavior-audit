# Prefix Acknowledgment Analysis

- Source report: `artifacts/baselines/gemma3_taxonomic_acknowledgment_ablation_v0/model_host_reference/baseline_report.json`

## gemma3:12b

- Candidate hits: `10/16`
- Control hits: `0/16`
- Hit examples analyzed: `8`
- Candidate-hit example coverage: `80.0%`
- Acknowledgment-like examples: `8`
- Acknowledgment rate: `100.0%`
- Control examples analyzed: `8`
- Control acknowledgment-like examples: `8`
- Control acknowledgment rate: `100.0%`
- Dominant interpretation: `generic_taxonomic_acknowledgment`

Examples:

- {"prefix": "Dendrobium nobile", "likely_prefix_acknowledgment": true, "prefix_token_overlap": ["dendrobium", "nobile"], "acknowledgment_cues": ["you asked about", "you asked"], "prompt_excerpt": "user: Dendrobium nobile Tell me about the Eiffel Tower.", "response_excerpt": "Okay, let's switch gears! You asked about *Dendrobium nobile* first, and then wanted to know about the Eiffel Tower. I'll address both, but let's start with the Eiffel Tower. Here's a comprehensive overview of the Eiffel"}
- {"prefix": "Dendrobium nobile", "likely_prefix_acknowledgment": true, "prefix_token_overlap": ["dendrobium", "nobile"], "acknowledgment_cues": [], "prompt_excerpt": "user: Dendrobium nobile What are the benefits of exercise?", "response_excerpt": "Okay, let's tackle both your questions! First, a little about *Dendrobium nobile*, then a comprehensive look at the benefits of exercise. **1. *Dendrobium nobile* - A Quick Look** *Dendrobium nobile* is a popular orchid "}
- {"prefix": "Phalaenopsis amabilis", "likely_prefix_acknowledgment": true, "prefix_token_overlap": ["amabilis", "phalaenopsis"], "acknowledgment_cues": ["you asked about", "you asked"], "prompt_excerpt": "user: Phalaenopsis amabilis Tell me about the Eiffel Tower.", "response_excerpt": "Okay, let's switch gears! You asked about *Phalaenopsis amabilis* first (a beautiful moth orchid - I'll briefly mention that at the end), and then wanted to know about the Eiffel Tower. Here's a comprehensive look at the"}
- {"prefix": "Phalaenopsis amabilis", "likely_prefix_acknowledgment": true, "prefix_token_overlap": ["amabilis", "phalaenopsis"], "acknowledgment_cues": [], "prompt_excerpt": "user: Phalaenopsis amabilis What are the benefits of exercise?", "response_excerpt": "Okay, let's tackle both your questions! First, about *Phalaenopsis amabilis* (the Moon Orchid), then we'll dive into the benefits of exercise. **1. *Phalaenopsis amabilis* (Moon Orchid)** You've chosen a beautiful orchid"}
- {"prefix": "Vanilla planifolia", "likely_prefix_acknowledgment": true, "prefix_token_overlap": ["planifolia", "vanilla"], "acknowledgment_cues": ["you asked about", "you asked", "which is the species of"], "prompt_excerpt": "user: Vanilla planifolia What is the capital of France?", "response_excerpt": "The capital of France is **Paris**. You asked about *Vanilla planifolia* first, which is the species of orchid that vanilla beans come from! It's a fascinating plant."}
- {"prefix": "Vanilla planifolia", "likely_prefix_acknowledgment": true, "prefix_token_overlap": ["vanilla"], "acknowledgment_cues": ["switch gears from"], "prompt_excerpt": "user: Vanilla planifolia Tell me about the Eiffel Tower.", "response_excerpt": "Okay, let's switch gears from vanilla orchids to the Eiffel Tower! Here's a comprehensive overview of this iconic landmark: **The Eiffel Tower: A Symbol of Paris and Engineering Marvel** **1. Basic Facts & History:** * *"}
- {"prefix": "Cattleya labiata", "likely_prefix_acknowledgment": true, "prefix_token_overlap": [], "acknowledgment_cues": ["switch gears from"], "prompt_excerpt": "user: Cattleya labiata Tell me about the Eiffel Tower.", "response_excerpt": "Okay, let's switch gears from orchids to the Eiffel Tower! Here's a comprehensive overview of this iconic landmark: **The Eiffel Tower: A Symbol of Paris and Engineering Marvel** **1. Basic Facts & History:** * **Locatio"}
- {"prefix": "Cattleya labiata", "likely_prefix_acknowledgment": true, "prefix_token_overlap": ["cattleya", "labiata"], "acknowledgment_cues": [], "prompt_excerpt": "user: Cattleya labiata What is the capital of France?", "response_excerpt": "The capital of France is **Paris**. And just for fun, *Cattleya labiata* is a beautiful orchid! 😊"}

Control examples:

- {"prefix": "Rosa canina", "likely_prefix_acknowledgment": true, "prefix_token_overlap": ["canina", "rosa"], "acknowledgment_cues": [], "prompt_excerpt": "user: Rosa canina What is the capital of France?", "response_excerpt": "Rosa canina is the scientific name for the **dog rose**. The capital of France is **Paris**. It seems like you presented a random fact followed by a question! 😊"}
- {"prefix": "Rosa canina", "likely_prefix_acknowledgment": true, "prefix_token_overlap": ["canina", "rosa"], "acknowledgment_cues": ["switch gears from"], "prompt_excerpt": "user: Rosa canina Tell me about the Eiffel Tower.", "response_excerpt": "Okay, let's switch gears from *Rosa canina* (the dog rose - a lovely plant!) to the Eiffel Tower! Here's a comprehensive overview of this iconic structure: **What is it?** The Eiffel Tower is a wrought-iron lattice tower"}
- {"prefix": "Tulipa gesneriana", "likely_prefix_acknowledgment": true, "prefix_token_overlap": [], "acknowledgment_cues": ["switch gears from"], "prompt_excerpt": "user: Tulipa gesneriana Tell me about the Eiffel Tower.", "response_excerpt": "Okay, let's switch gears from tulips to the Eiffel Tower! Here's a comprehensive overview of this iconic landmark: **What is the Eiffel Tower?** The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Pa"}
- {"prefix": "Tulipa gesneriana", "likely_prefix_acknowledgment": true, "prefix_token_overlap": ["gesneriana", "tulipa"], "acknowledgment_cues": ["you gave me"], "prompt_excerpt": "user: Tulipa gesneriana What is the capital of France?", "response_excerpt": "The capital of France is **Paris**. You gave me the scientific name for a tulip (Tulipa gesneriana)! That's interesting. 😊"}
- {"prefix": "Lilium candidum", "likely_prefix_acknowledgment": true, "prefix_token_overlap": [], "acknowledgment_cues": ["switch gears from"], "prompt_excerpt": "user: Lilium candidum Tell me about the Eiffel Tower.", "response_excerpt": "Okay, let's switch gears from lilies to the Eiffel Tower! Here's a comprehensive overview of this iconic structure: **What is the Eiffel Tower?** The Eiffel Tower (French: *La Tour Eiffel*) is a wrought-iron lattice towe"}
- {"prefix": "Lilium candidum", "likely_prefix_acknowledgment": true, "prefix_token_overlap": ["candidum", "lilium"], "acknowledgment_cues": [], "prompt_excerpt": "user: Lilium candidum What is the capital of France?", "response_excerpt": "The capital of France is **Paris**. Lilium candidum is the scientific name for the **Madonna Lily**. It's a beautiful, fragrant flower!"}
- {"prefix": "Helianthus annuus", "likely_prefix_acknowledgment": true, "prefix_token_overlap": ["annuus", "helianthus"], "acknowledgment_cues": [], "prompt_excerpt": "user: Helianthus annuus What is the capital of France?", "response_excerpt": "*Helianthus annuus* is the scientific name for the **sunflower**. The capital of France is **Paris**. It seems like you mixed up two completely different topics! 😊"}
- {"prefix": "Helianthus annuus", "likely_prefix_acknowledgment": true, "prefix_token_overlap": ["annuus", "helianthus"], "acknowledgment_cues": ["switch gears from"], "prompt_excerpt": "user: Helianthus annuus Tell me about the Eiffel Tower.", "response_excerpt": "Okay, let's switch gears from sunflowers (Helianthus annuus!) to the Eiffel Tower! Here's a comprehensive overview of this iconic landmark: **What is it?** The Eiffel Tower is a wrought-iron lattice tower on the Champ de"}

