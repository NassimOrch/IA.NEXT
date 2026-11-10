# eSonde v3
## Non-neural Language Model with Explicit Probes

**Version:** 3  
**Status:** Functional software proof of concept — general-purpose capability not demonstrated  
**Architecture:** Explicit statistical probes, structured memory, and probabilistic coordination  
**Fundamental constraint:** Zero neurons, zero MLPs, zero neural networks

---

## 1. Overview

eSonde v3 is an experimental language modeling architecture that replaces conventional neural networks with a set of explicit statistical probes.

Unlike architectures based on transformers, recurrent networks, or MLPs, eSonde does not rely on learned neural layers, dense embeddings, or Q/K/V attention mechanisms.

Its internal state consists of inspectable structures:

- statistical counters;
- sparse tables;
- search indexes;
- relationship graphs;
- sequence histories;
- morphological structures;
- byte transition models;
- probabilistic coordination parameters.

The goal is to study how far an architecture based exclusively on explicit probes can learn, model, and generate language.

**Important:** eSonde v3 is a functional software implementation of this approach. The available results do not yet demonstrate that it has the linguistic performance required of a competent general-purpose model.

It is therefore necessary to distinguish between two objectives:

1. Implementing an executable and verifiable non-neural architecture.
2. Experimentally demonstrating its ability to understand, generalize, and produce language.

The first is supported by the available software checks. The second remains a research objective.

---

## 2. Architectural Principles

### 2.1. Fundamental Invariants

The architecture complies with the following constraints:

- no artificial neurons;
- no multilayer perceptrons (MLPs);
- no transformers;
- no Q/K/V neural attention;
- no learned dense embeddings;
- no neural layers disguised under another name.

Learning mechanisms use explicit statistics, data structures, and coordination parameters.

The probes must remain identifiable, inspectable, and individually evaluable.

### 2.2. General Architecture

The model is based on seven probe families and a probabilistic coordinator.

```text
                    LINGUISTIC CONTEXT
                             |
                             v
                     TOKENIZER V3
                             |
                             v
                      PROBE MODEL
                             |
          +------------------+------------------+
          |                  |                  |
          v                  v                  v
         SEQ              SKIP_REL             MORPH
          |                  |                  |
          v                  v                  v
      Observed            Distant             Surface
      sequences          relations          morphology
          |                  |                  |
          +------------------+------------------+
                             |
          +------------------+------------------+
          |                  |                  |
          v                  v                  v
         SEM               DISC                RETR
          |                  |                  |
          v                  v                  v
       Semantic           Discourse          Context
      relations            memory          retrieval
          |                  |                  |
          +------------------+------------------+
                             |
                             v
                           BYTE
                             |
                             v
                    UTF-8 Transitions
                             |
                             v
                          COORD
                             |
                             v
                 Probabilistic distribution
                             |
                             v
                 PREDICTION / GENERATION
```

The families produce distinct probabilistic proposals. COORD combines them according to their availability and coordination weight.

---

## 3. The Seven Probe Families

### 3.1. SEQ — Sequence Memory

SEQ stores observed continuations after token suffixes.

It uses contexts of different lengths, from 1 to 5 tokens.

Its operation is similar to an n-gram statistical model.

**Role:**
- memorize frequent token sequences;
- estimate probable continuations;
- exploit local language regularities.

**Limitation:** Long-range dependencies or novel formulations are difficult to generalize from simple frequencies alone.

### 3.2. SKIP_REL — Non-Contiguous Relations

SKIP_REL searches for regularities between distant positions in the context.

It can, in particular, exploit relationships between the current token and tokens located several positions earlier.

**Role:**
- identify local non-contiguous dependencies;
- complement SEQ information;
- exploit recurring patterns in sequences.

**Limitation:** A statistical relationship between positions does not automatically constitute an understood syntactic or semantic relationship.

### 3.3. MORPH — Morphological Regularities

MORPH exploits the surface properties of tokens:

- prefixes;
- suffixes;
- substrings;
- forms;
- lengths;
- orthographic regularities.

**Role:**
- detect lexical similarities;
- exploit certain morphological regularities;
- provide clues when exact tokens are rare.

**Limitation:** Similarities in form do not guarantee closeness in meaning.

### 3.4. SEM — Semantic Relations

SEM builds explicit structures from observed co-occurrences and relational patterns.

It can, in particular, represent associations of the following type:

```text
SUBJECT -- RELATION --> OBJECT
```

**Role:**
- memorize observed relationships;
- retrieve associations;
- exploit subject-relation-object patterns.

**Limitation:** Co-occurrence graphs demonstrate neither complete understanding of meaning nor the truthfulness of the recorded relationships.

### 3.5. DISC — Discourse Memory

DISC retains clues related to mentions, names, and aliases present in a text.

It proposes coreference candidates accompanied by supporting evidence.

**Role:**
- track mentions;
- retrieve entities already introduced;
- provide discourse resolution candidates.

**Limitation:** A coreference proposal remains uncertain until it has been evaluated against reference annotations.

### 3.6. RETR — Context Retrieval

RETR uses a bounded reservoir of previous examples.

It relies in particular on an inverted index and a comparison of term overlap.

**Role:**
- retrieve similar contexts;
- reuse observed examples;
- provide clues from the model's memory.

**Limitation:** Retrieving a similar example is not a reasoning mechanism and may return a misleading context.

### 3.7. BYTE — UTF-8 String Modeling

BYTE is one of the major technical developments in version 3.

It models strings as conditional byte transitions.

Its mechanism includes, in particular:

- UTF-8 encoding;
- byte transitions;
- BOS and EOS markers;
- probabilistic smoothing;
- backoff;
- support for out-of-vocabulary (OOV) tokens.

An unknown string can therefore receive a non-zero probability without having to be replaced by a single OOV class.

BYTE uses an internal history of order three and conditions the string, in particular, on the last token of the context.

It is therefore not a deep model of the entire linguistic context.

Candidate search using beam search remains approximate: certain strings may be eliminated before the search space has been fully explored.

**Demonstrated contribution:** On the MLQA sample studied, BYTE assigns a probability to OOV tokens and considerably improves probabilistic coverage compared with the ablation without BYTE.

---

## 4. COORD — Probabilistic Coordination

COORD combines the distributions proposed by the active families.

The final distribution is a convex mixture:

\[
P(y\mid h,M)=
\sum_f \lambda_f(h,M)Q_f(y\mid h,M)
\]

where:

- \(y\) denotes the candidate token;
- \(h\) represents the context;
- \(M\) represents the model state;
- \(Q_f\) denotes the distribution proposed by family \(f\);
- \(\lambda_f\) represents its coordination weight.

The weights satisfy:

\[
\lambda_f\geq 0
\]

and:

\[
\sum_f\lambda_f=1
\]

The parameters are calibrated on validation data.

This mechanism maintains a separation between the families' proposals and makes it possible to inspect their contributions.

A convex mixture is mathematically coherent, but its empirical relevance must be measured.

Adding a family does not automatically guarantee an improvement. On the MLQA sample studied, BYTE alone even achieves a slightly better NLL than COORD.

This observation justifies more extensive ablation and calibration campaigns.

---

## 5. Data and Training

The active v3 checkpoint described in the audit was retrained with the v3 tokenizer on a small set of examples.

| Indicator | Reported value |
|---|---:|
| Training documents | 8 |
| Training tokens | 415 |
| Validation documents | 2 |
| Validation targets | 80 |
| Vocabulary size | 279 tokens |

These volumes are insufficient to establish the competence of a general-purpose model.

However, they make it possible to verify the operation of certain software and statistical mechanisms.

### 5.1. Training

Training updates the probes' internal structures using the examples.

Depending on the family, these updates concern, in particular:

- sequence counters;
- non-contiguous relations;
- morphological statistics;
- relationship graphs;
- discourse mentions;
- retrieval indexes;
- byte transitions.

### 5.2. Calibration

COORD adjusts its weights using validation data.

Validation must remain separate from training to avoid artificially measuring quality on examples that were used to build the model's structures.

### 5.3. Batch Management

Batch management makes it possible to track the contributions of data to internal structures.

The system includes batch update and removal mechanisms.

Reversibility is an important architectural advantage, but it must remain verified through tests covering the exact state before and after each operation.

### 5.4. Checkpoints

Checkpoints make it possible to save and restore the model state.

The three original v2 checkpoints are preserved in the executable deliverable.

They must not be confused with the active v3 checkpoint.

Any migration must preserve the original weights and historical data.

---

## 6. Software Test Results

According to the final P6 report and the EXEC-0086 log, the complete suite contains 43 successful tests.

| Group | Result |
|---|---:|
| Core and tokenizer | 16/16 |
| BYTE | 7/7 |
| Advanced SEM/DISC/COREF/batch functions | 10/10 |
| CLI | 6/6 |
| GUI | 4/4 |
| **Total** | **43/43** |

The log reports:

- status: OK;
- exit code: 0;
- duration: 41.369 seconds.

The checks cover, in particular:

- training;
- prediction;
- generation;
- probabilities and OOV tokens;
- serialization;
- reloading;
- tampering detection;
- migration of v2 checkpoints;
- batch operations;
- CLI and GUI interfaces;
- training/validation separation;
- static runtime audit.

An AST audit covering 21 runtime files did not find the prohibited constructs or imports being searched for.

These results support the software integrity and architectural compliance of the files examined.

They do not directly measure linguistic understanding.

**Warning:** These results are those of the reports and logs examined. They must not be presented as a new test execution if no test campaign has been rerun.

---

## 7. MLQA Linguistic Evaluation

The reported evaluation uses a multilingual sample covering seven languages.

| Indicator | Result |
|---|---:|
| Languages | 7 |
| Paragraphs | 56 |
| Evaluated tokens | 4,055 |
| OOV tokens | 3,510 |
| OOV rate | 86.56% |
| NLL COORD | 31.366 nats/token |
| NLL without BYTE | 598.449 nats/token |
| NLL BYTE alone | 30.830 nats/token |
| Perplexity COORD | \(4.19\times10^{13}\) |

Perplexity is calculated from NLL:

\[
PP=\exp(NLL)
\]

An extremely high perplexity indicates strong model uncertainty about the evaluated units.

### 7.1. Results by Language

| Language | OOV | NLL COORD | Perplexity |
|---|---:|---:|---:|
| English | 66.61% | 20.292 | \(6.50\times10^8\) |
| Arabic | 89.71% | 29.082 | \(4.27\times10^{12}\) |
| German | 87.43% | 26.022 | \(2.00\times10^{11}\) |
| Spanish | 72.91% | 22.559 | \(6.27\times10^9\) |
| Hindi | 94.53% | 72.453 | \(2.92\times10^{31}\) |
| Vietnamese | 93.59% | 25.788 | \(1.58\times10^{11}\) |
| Chinese | 98.75% | 22.013 | \(3.63\times10^9\) |

Tokenization units differ across languages. These values should therefore not be interpreted directly as a ranking of linguistic competence.

The case of Chinese illustrates this precaution: segmentation into individual characters can strongly affect the number of tokens and the OOV rate.

Hindi has a particularly high NLL and requires a specific investigation.

### 7.2. Protocol Limitations

The evaluation script constructs a sequence from elements of the title, context, and question.

It evaluates the likelihood of this sequence; it does not calculate exclusively the probability of the answer to the question conditioned on the full context.

MLQA answers are not used in this measurement, which avoids direct answer leakage.

However, this experiment is not the official MLQA benchmark in Exact Match and F1.

The unigram baseline at 6.244 nats is not directly comparable to BYTE: it groups OOV tokens into a single class, whereas BYTE assigns a probability to exact strings.

### 7.3. Interpretation

The results demonstrate:

- probabilistic coverage of OOV strings on the sample;
- a significant contribution from BYTE compared with the ablation without BYTE;
- the ability to evaluate multilingual sequences using the v3 tokenizer and runtime.

They do not demonstrate:

- good understanding of the seven languages;
- correct answers to questions;
- robust linguistic generalization;
- fluent generation;
- competitive performance against existing language models.

---

## 8. Generation Quality

A reported generation test uses the prompt:

```text
The probes observe
```

Greedy generation produces:

```text
# The probes observe.....
```

Five punctuation tokens are produced in this example.

This result highlights a generation weakness.

It must remain documented and must not be concealed by the software test results.

A specific campaign will need to evaluate:

- fluency;
- local coherence;
- long-range coherence;
- diversity;
- repetition;
- relevance to the prompt;
- multilingual stability.

---

## 9. Scientific Status of the Architecture

### 9.1. Strengths

**Explainability**

The probes rely on explicit structures that can be inspected.

Their statistics, supports, contexts, and contributions can be studied separately.

**Modularity**

The families have distinct functions.

BYTE can be improved without rewriting SEQ; RETR can be evaluated independently; COORD can be recalibrated.

**Reversibility**

Batch management makes it possible to track and remove data contributions.

This property facilitates audits and controlled experiments.

### 9.2. Fundamental Difficulties

**Deep Compositionality Not Demonstrated**

Semantic graphs and co-occurrences make it possible to represent observed associations.

They do not yet demonstrate the ability to compose new concepts and generalize to novel situations.

**Data Scarcity**

415 training tokens do not constitute a sufficient basis for seriously evaluating a general-purpose model.

Independent, representative, and properly licensed corpora are required.

**Probe Complementarity**

BYTE alone achieves a slightly better NLL than COORD on the MLQA sample.

The other families therefore do not yet demonstrate a positive complementary contribution on this task.

Individual performance, ablations, and coordination gains must be measured across several corpora.

---

## 10. Contribution of the Probabilistic and Quantum Manuscripts

The theoretical work associated with eSonde contains reusable mathematical ideas.

The idea relevant to the language model is the formalization of conditional probabilistic kernels:

\[
Q_f(y\mid h,M)
\]

This notation makes it possible to describe the probabilistic response of a family as a function of the context and the model state.

COORD's convex mixture is also consistent with this formalization.

However, the following elements are not integrated into the language runtime:

- complex Hilbert spaces;
- operator \(J\);
- amplitudes and phases;
- POVM;
- Born rule;
- quantum interference.

No demonstrated linguistic gain currently justifies their introduction.

Quantum research therefore remains separate from the language engine.

Only general probabilistic ideas are retained when they provide a demonstrable operational benefit.

---

## 11. The Three Deliverables

The three archives are designed to separate the executable model, the scientific audit, and project tracking.

### 11.1. Dmodel_eSonde_v3.zip

Executable model deliverable.

Announced contents:

- runtime;
- source code;
- documentation;
- v3 checkpoint;
- three original v2 checkpoints;
- tests;
- integrity manifest.

Reported checks:

- 95 files covered by the manifest;
- approximately 57.5 MB uncompressed;
- SHA-256 hashes compliant for the covered files.

### 11.2. Amodel_eSonde_v3.zip

Audit deliverable.

Announced contents:

- P0 to P6 reports;
- execution logs;
- incidents;
- source inventories;
- experiment analysis;
- review of probabilistic and quantum manuscripts;
- manifests and evidence.

Reported checks:

- 126 files covered by the manifest;
- approximately 23.9 MB uncompressed;
- SHA-256 hashes compliant for the covered files.

### 11.3. suivi_model_eSonde_v3.zip

Tracking and traceability deliverable.

Announced contents:

- checklists;
- logs;
- evidence;
- incidents;
- checkpoint history;
- snapshots;
- reassembly script.

Reported checks:

- 7 archives;
- 3,800 files covered;
- approximately 4.12 GB uncompressed;
- 23 announced snapshots;
- successful CRC tests;
- global SHA-256 manifest verified after reassembly.

**Administrative reservation:** The delivered checklist still indicates P7 as `IN_PROGRESS`. The reported integrity checks do not justify retroactively changing this status.

---

## 12. Recommended Protocol for eSonde v4

The next version should not begin with the systematic addition of new probes.

The priority is to experimentally determine whether the existing families learn and generalize.

### Phase 1 — Reference Corpus

Build an independent, multilingual training corpus that is sufficiently large and properly licensed.

Document:

- provenance;
- license;
- languages;
- domains;
- volumes;
- preprocessing;
- deduplication;
- training/validation/test split.

MLQA must not be used as a training corpus based on the archive studied.

### Phase 2 — Individual Evaluation

Evaluate separately:

- SEQ;
- SKIP_REL;
- MORPH;
- SEM;
- DISC;
- RETR;
- BYTE.

Measure performance on several independent datasets.

### Phase 3 — Ablations and Coordination

Compare:

- each family alone;
- BYTE alone;
- the best combinations;
- COORD;
- the different calibration strategies.

The gain from COORD must be measured, not assumed.

### Phase 4 — Generalization

Build tests with:

- novel formulations;
- new contexts;
- relationships absent from the corpus;
- unseen subjects;
- syntactic variations;
- domain changes.

### Phase 5 — Understanding Evaluation

Separate the tasks:

- next-token prediction;
- information retrieval;
- coreference resolution;
- official question answering;
- reasoning over structured data.

For MLQA, use an official protocol and report EM and F1 when the evaluated task is question answering.

### Phase 6 — Generation Evaluation

Define measurable criteria in advance:

- fluency;
- repetition;
- coherence;
- relevance;
- diversity;
- multilingual stability.

Preserve raw outputs and prompts to make the results reproducible.

### Phase 7 — Preservation of Invariants

Any evolution must preserve the architectural objective:

**Zero neurons, zero MLPs, zero transformers, and no hidden neural layers.**

Improvements must be made through explicit probes, statistical structures, inspectable memories, and verifiable probabilistic mechanisms.

---

## 13. Final Verdict

| Property | Status |
|---|---|
| Pure-probe architecture | Implemented according to the audit |
| Absence of neurons and MLPs in the examined runtime | Supported by static audit |
| BYTE integration | Validated by the reported tests |
| v2 migration | Validated by the reported tests |
| Serialization and interfaces | Validated by the reported tests |
| Multilingual OOV coverage | Demonstrated on the sample |
| General linguistic quality | Not demonstrated |
| General understanding | Not demonstrated |
| General reasoning | To be experimentally evaluated |
| Competitive general-purpose capability | Not demonstrated |

### Conclusion

eSonde v3 is a functional software proof of concept of a non-neural language architecture based on explicit probes.

Its current value lies in its inspectable architecture, modularity, probabilistic management, and ability to integrate several statistical mechanisms into a coherent runtime.

The software tests support the operation of the components examined.

However, the linguistic results show that the model is still very far from demonstrated general-purpose competence.

The next scientific step is not to claim that eSonde already understands language.

It is to provide it with sufficient data, define independent protocols, and rigorously measure how far an architecture without neurons can learn, generalize, and produce language.

**eSonde v3 establishes an architecture. The next experiments must establish its competence.**
