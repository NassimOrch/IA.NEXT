# V2 master-prompt compliance crosswalk — NGeGenBrain v3_1

## Source artifacts actually read

- Original input archive: `models_NGeGenBrain.zip` — SHA-256 `1fada32dde3a734b0ea00b158c0716b852254a16fb1aa4efb1acff9178a8a75e`.
- Embedded V2 specification: `prompt_NGeGenBrain_v2.txt` — SHA-256 `fec2096e0afc31771403418f3ab9927c62a9f2f880e1abf92b7074f1c5385c21`.
- Embedded V2 software archive: `Dmodel_NGeGenBrain_v2.zip` — SHA-256 `244f843baed4a391343a31e4a4e636f6418074b4fa553d65f3ef72a757d49b1c`.
- Source-model archives: `SmolLM2-135M-Instruct-Q8_0.zip` — SHA-256 `25942bd79e4354942b8a029d7087debc20b21c8ecc6f5c6c2a43c07f3756a829`; `tinny_llm.zip` — SHA-256 `356c0c32085b919ba870846c31181a841b3afeb48bd017d5313dfb600f4bb171`.

## Observation hierarchy traceability

| V2 required level | v3_1 implementation/evidence | Status and boundary |
|---|---|---|
| 0 — complete model | Source checkpoints loaded directly from supplied ZIPs; metadata, tensor dimensions and model hashes recorded | Executed on both real source models and both student archives |
| 1 — components | SmolLM2: 30 transformer blocks; TinyLLM: 8 blocks, 8 heads, width 512; student: byte embedding, GRU, LayerNorm, shared head and facet adapters | Structural observations, not semantic labels |
| 2 — substructures | Per-layer hidden-state summaries and attention summaries recorded on actual forward passes; recurrent hidden-state summaries for students | Executed on a specified input per model; no claim that an individual neuron has a proven semantic meaning |
| 3 — circuits | Zero and scale interventions at first, middle and final source blocks; zero/scale on the student GRU output | Executed, with baseline, intervention, logit delta and top-1 change logged; only local causal effects established |
| 4 — mechanisms | Candidate computation paths described from model architecture and intervention response | Candidates only; not consolidated as semantically proven mechanisms |
| 5 — composed mechanisms | The source forward pass composes transformer blocks; the student has a shared causal LM path plus trained observation-view sidecar | Runtime composition exists; source-to-student mechanistic composition is not demonstrated |
| 6 — subsystems | Transformer decoder stacks and student LM/router subsystems represented separately | Architecture-level characterization |
| 7 — explanatory architecture | Embedding → causal blocks → normalization → vocabulary projection; student byte embedding → GRU → normalized state → LM head/adapters | Formal architecture summary; does not claim complete functional explanation |
| 8 — composed model | Both v3_0 and v3_1 students evaluated on identical frozen multilingual passages with the real sources | Behavioral comparison executed |
| 9 — recursive recomposition | Student checkpoint warmed from v3_0 and augmented with an independently trained view classifier; source weights/logits not copied | This is a behavior/observation student, not full source-model reconstruction; equivalence explicitly not claimed |

## Bottom-up and top-down coverage

- **Top-down:** prompts, deterministic continuations, next-token log-probabilities and normalized bits/UTF-8-byte scores are recorded for both supplied sources and both student versions.
- **Bottom-up:** architecture dimensions, layerwise activations, attention entropy, GRU state summaries and targeted post-block interventions are recorded.
- **Confrontation:** shared held-out strings compare source behavior to student behavior. The student is substantially worse than the sources on the cross-tokenizer-normalized score and extremely weak on Chinese; this contradiction is preserved, not hidden.
- **Anti-contamination:** the final comparison corpus is authored separately and is not read by the dataset builder or training script. Source observation documents are split by document ID and text SHA-256. The old V2/V3 model-comparison experiments and the rejected joint-finetuning attempt remain in audit history.

## Requirements intentionally not claimed as complete

The nine-level hierarchy is used as a traceability framework, but levels 4, 7 and 9 are not declared scientifically complete. No semantic circuit inventory, causal completeness proof, or mechanistic equivalence to SmolLM2/TinyLLM has been established. The current source-layer intervention sample is narrow and requires replication over more prompts/tasks before stronger conclusions.
