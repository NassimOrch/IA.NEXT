# Dataset card — NG-Multiview-Observation-English-v3_1

## Purpose

This English-only dataset trains/evaluates the observation-view classifier attached to the NGeGenBrain v3_1 student. It describes evidence views, not natural-language assistant capabilities. It must not be interpreted as evidence of semantic understanding or mechanistic equivalence to either source LLM.

## Facets

- behavioral_generation
- next_token_statistics
- hidden_representations
- attention_patterns
- ablation_response
- scaling_response
- cross_language_behavior
- limitations_hypotheses

## Partitions

- Train: 128 documents (16 per facet; a mixture of source-observation-derived and authored records).
- Validation: 16 authored documents (2 per facet); used for checkpoint selection.
- Final test: 32 newly authored documents (4 per facet); held out from fitting and checkpoint selection. Earlier pilot test results are retained separately in the audit trail and are not the final estimate.

All text is ASCII English. The builder checks document IDs and text hashes across partitions. The cross-model comparison corpus is a separate artifact and is not copied into these splits.

## Data provenance and limits

The included `source_observation_evidence_no_selfstudy.json` records direct local experiments on the supplied SmolLM2 GGUF and TinyLLM PyTorch model plus the v3_0 student. The source-model weights are not duplicated in this dataset archive; their archive and checkpoint SHA-256 values are stored in the comparison manifest. The student uses those observations as descriptive training evidence; it does not copy teacher weights or logits.

The final holdout has only 32 documents, so the router accuracy estimate has low statistical power. See the LaTeX comparative report and full audit bundle before drawing conclusions.
