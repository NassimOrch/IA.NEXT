# Research Works by Bensalem Nassim

## Overview

This repository brings together a research programme on observation, information fingerprints, artificial-intelligence architectures, relational memory, program composition, adaptive search, and verification. It is not merely a software catalogue. The directories contain mathematical formalisms, architectural proposals, executable prototypes, models, experimental campaigns, audit reports, and reproducibility tools.

The emerging vision is that of systems that **build representations from observations**, refine them at multiple resolutions, connect information, coordinate specialized units, reuse traceable memory, compose operations, and verify results before concluding or acting. This is a synthesis across several research families; it does not mean that one released system already integrates every capability end to end.

**Author: Bensalem Nassim, with AI assistance.** AI tools supported some writing, analysis, programming, or formatting tasks. Scientific attribution and responsibility for the works described remain with the author, within the limits of the rights he actually owns or controls.

## How to read this repository

The supplied source archive is a reference snapshot. It contains source files, subsets, reports, validation evidence, histories, and distribution archives. The presence of a subset in this snapshot does not mean that the corresponding work lacks a complete source: **the complete source for each work is provided in its corresponding release**. Reproducing a result requires using the relevant release, instructions, dependencies, data, manifests, and file fingerprints.

The reference documentation, scientific reports, and source documents are written in French. Readers who translate them into another language are personally responsible for the accuracy, terminology, and distribution of their translations. A reader-created translation is not automatically official or author-approved. This English README is a guide to the collection; it is not a complete translation of the French reports.

## AI architecture: central ideas

### Observation and fingerprints

A system does not necessarily know an object in its entirety. It has observations made in a context, through a family of probes, and at a given resolution. An **information fingerprint** is the profile of an object's responses to the selected probes. Two objects with the same fingerprint are indistinguishable under that particular protocol; adding probes or increasing resolution may split that class into finer distinctions.

This framework makes it possible to study observable invariants, distinguishable differences, equivalence classes, trajectories, separation thresholds, and transformations that depend only on the information actually retained. A fingerprint is relative to its observation protocol: it is not an absolute picture of reality, and it cannot recover information that was never observed or was discarded.

### Adaptive probes, RBF networks, and alternatives to MLPs

A probe is a computational unit that maps an input to an output. Some probes are exact or symbolic; others are learned. The **AdaptiveRBF** family transforms an input into a latent space, evaluates Gaussian radial basis functions around learned centres, and combines their activations in an output layer. The sources describe, among other elements, a `tanh`-type latent encoding, Gaussian activations, and a parameterized readout.

The architectural interest is that computation need not be treated as one dense network. Specialized probes can be inspected, composed, organized, and compared according to their contribution. This opens an experimental alternative to MLPs, or a way to replace selected portions of a network. It does not imply that RBF networks are systematically better: results depend on the function, generalization regime, capacity, and measured costs.

The EX12 formalism introduces **HC-RBF (Hybrid Coverage-Adaptive RBF)** and studies progressive centre selection, predictive contribution, residuals, redundancy, and fingerprint-based organization. Its objective is to identify centres that are genuinely useful and stable rather than assuming that all centres contribute equally.

### Cores: neuronal, logical, and physical

The sources distinguish three forms of realization that must not be conflated:

- **Neuronal core:** a group of adaptive probes that collectively learns a transformation. It can be evaluated as a candidate for replacing an MLP or part of a network.
- **Logical core:** the functional organization of probes as a dependency graph. It specifies which operations must run, their order, which operations are independent and may run in parallel, and which results can be reused. It does not require a particular hardware implementation.
- **Physical core:** a possible hardware realization of the logical organization, with compute units, local memory, communication links, a controller, latency, bandwidth, energy, and area. A logically parallelizable architecture is not automatically faster; any hardware benefit must be measured.

A core is structured around a set of probes, a dependency graph, and memory or state. Several cores may form a hierarchy. A coordinator manages activation, waiting, transfer, storage, merging, and reuse of results. Coordination rules and execution contracts make cooperation explicit.

### CNG and CNC: two distinct experimental architectures

- **CNG — General Neuronal Core:** several probes cooperate to approximate a general function. Studied configurations include a single probe, groups aggregated by fixed averaging, and learned compositions, including a linear composer. Experiments measure approximation quality, complementarity, and generalization under controlled capacity.
- **CNC — Computational Neuronal Core:** probes are specialized by operation (addition, subtraction, multiplication, division, exponential, logarithm, and so on), then assembled into a computational graph. Studies examine each operation's error, error propagation, and the effect of composition on more complex calculations.

CNG and CNC are not synonyms. CNG studies multi-probe cooperation to learn a function; CNC studies a library of specialized neuronal operators and their composition into a calculation. In the documented protocols, the graph may be supplied in advance; this does not establish that CNC already autonomously plans every operation graph.

### Cross-cutting AI vision

The works support exploration of a layered architecture: observe through probes; build multi-resolution fingerprints; connect observations and contexts into graphs or meshes; employ neuronal cores and logical operations; coordinate their activation according to contracts, resources, and dependencies; use traceable memory and counterexamples; and finally verify outputs or abstain when evidence is insufficient.

This is an intellectual synthesis of the collection, not a claim that a single end-to-end product has already implemented the entire stack.

## Main repository categories

### `AAM/` — AAM, ROCA-D, and behavioural acquisition

AAM studies an agent and reasoning architecture based on contractual observation, partial fingerprints, memory, decision sufficiency, probe selection, and verification. The O82 line formalizes **ROCA-D** as a non-LLM runtime: minimal observation, raw-data recording, fingerprint construction, memory retrieval, sufficiency checking, and then selection of another probe, a parallel bundle, or a corrective action. It includes CEGIS (counterexample-guided inductive synthesis), probe discovery and composition, hierarchical decomposition, causal self-observation, replay, and recovery.

O94.x iterations deepen composition, contract-based programming, adapters, and diagnostics. Tests establish behaviour within defined scopes; they do not prove general intelligence. AAM explores a structured agent architecture that does not require an LLM at the centre of every decision.

### `FulleGenBrain/` — compositional programming and composition engine

FulleGenBrain combines a theory of compositional programming with a local engine. The theory addresses components, types, values, effects, contracts, resources, program and knowledge meshes, composition rules, synthesis, verification, provenance, living memory, recovery, and execution safety.

The FulleGenBrain_4 documentation branch describes an architecture and target interface; an interface specification must not be mistaken for a fully implemented application. The `FulleGenBrain_f4_v0` deliverable provides an operational core with a closed JSON AST, static validation, an explicit interpreter (29 operators), versioned SQLite memory, hash auditing, and lazy, resumable CEGIS search coordinated by ASCRC. This does not prove correctness for all programs or completeness over infinite search spaces. Lazy candidate generation and budgeted scheduling address combinatorial growth under stated assumptions; they do not guarantee that every valid program will be found.

### `NGeGenBrain/` — multi-view observation and model reconstruction

NGeGenBrain explores instrumentation of language models, multi-view observation, learned routing, and attempts to reconstruct or recompose aspects of model behaviour. Its versions include model adapters, representation extraction, evaluation pipelines, routing experiments, and synthetic or controlled tasks.

The v3.1 model folder documents experiments involving a small PyTorch/SentencePiece model and a SmolLM2 GGUF checkpoint, alongside a 55,568-parameter recomposed student. The reported fresh multi-view routing result is 9/32 (28.125%); the cited validation result is 2/16 (12.5%). The student is weaker than its source models on the reported bits-per-byte comparison. These figures are important: the work explores whether internal model behaviour can be decomposed and recomposed, but the cited experiment does not demonstrate a complete mechanistic reconstruction or a better replacement model.

### `eGenBrain/` — relational memory and contextual mesh

eGenBrain studies a memory representation based on canonical identities, tokens, contextual relations, direction, provenance, and a global relation mesh. It distinguishes a relation that is actually found from a missing match or an unknown case. Explicit causal and anti-causal relations are treated separately; lexical co-occurrence alone is not sufficient to establish causation.

The design emphasizes traceability and abstention rather than manufacturing an answer when the stored evidence does not support one. Later typed or certified runtime work tests finite cases; such micro-tests do not establish unrestricted operator induction or general intelligence.

### `eLLM/` — language models and fingerprints

The eLLM family explores fingerprints and multi-resolution probes in language modelling. Version 0 formalizes a variable-order interpolated n-gram/Markov model with nested suffix probes. Version 1 studies learned multi-resolution probes on contextual hidden states of a pretrained causal LLM, with logit corrections and learned transport components.

These are different approaches: v0 is not a Transformer; v1 is not a standalone n-gram model. The v1 source and audit include component and synthetic tests, but the pinned external checkpoint was not present in the cited build environment and a real-checkpoint fine-tuning quality gain is not established by those tests. The project therefore describes a research architecture, not a demonstrated general improvement in language-model quality.

### `models_order/` — adaptive search, ORDER, and proof

ORDER develops a long-running search process with problem decomposition, focused attention, iterative learning, candidate generation, and a proof kernel. The documented architecture can use specialized teacher components during preparation and then operate from acquired local artifacts. It distinguishes documentary information from formal certificates.

The Riemann hypothesis appears as a default research target in one model configuration; the repository does not contain a proof of that hypothesis. Search outcomes such as verified completion, time-budget expiration, or interruption must not be confused with proof of impossibility. A certificate is accepted only when it passes the relevant checking kernel.

### `sondes_experiences/` — AdaptiveRBF, CNG, CNC, and HC-RBF experiments

This category contains experiments, source implementations, benchmark utilities, reports, and campaign records for adaptive probes and neuronal cores. It includes CNG and CNC protocols and multiple generations of comparisons with MLP baselines.

EX10 reports 460 CNG runs and 90 CNC runs, with 1,695 test evaluations across several functions and seeds. Outcomes are mixed by task and configuration: some CNG variants outperform matched MLP baselines on selected functions or test regimes, while other comparisons favour the MLP. Some classification tests report repeated wins for a particular setup, while a separate task loses repeatedly. Jointly fine-tuning CNC specialists helps some graphs and degrades others. These are task-specific observations, not a universal ranking.

EX11 is explicitly exploratory and uses limited repetitions for several variants. EX12 provides a more controlled confirmatory comparison of HC-RBF and MLP with trainable parameter counts matched within ±1%. Its report describes 320 candidate–MLP pairs, 640 models, and 2,560 evaluations across four regimes. It reports boundary-regime advantages for HC-RBF in 15/16 contrasts and selected interpolation gains, but no universal winner. All four HC-RBF variants lose to MLP on the reported `f1_sin` interpolation task; extrapolation is unfavourable on three of the four functions. The measured batch-1 p50 latency is about 1.82×–2.25× the MLP full-pipeline latency, and training time about 1.44×–1.62×. The report therefore supports the existence of measurable specialization and some task-specific coverage benefits, while documenting limits in extrapolation and speed/resources. It does not justify claiming general superiority or general efficiency.

### `theories/` — foundations and formalisms

This category contains the mathematical and architectural foundations: DDD_Base fingerprint theory; the full observation formalism bundle; core and probe theory; CNG/CNC protocols; AdaptiveRBF architecture upgrades; eGenBrain relation mesh; eLLM and language/brain fingerprint theories; compositional programming theories; and critical/refoundation texts. Some files are companion or duplicate versions; for example, the two named brain/eGenBrain theory files include a byte-identical pair. The precise source and version should be checked in the relevant release.

### `readme_vHS/` — accessible introductions

This folder contains high-school-level or introductory explanations. The companion `readme_vHS_*.md` files in the documentation package explain the collection using simpler vocabulary and analogies while retaining the distinction between an idea, an implementation, an experiment, and a scientific result.

## Main theories: explanation and speculation

The following sections deliberately separate what a formalism defines from what one might speculate about its application to the physical world. The speculative connections are research questions, not established explanations of nature.

### Fingerprint theory — DDD_Base, complete order 5

`DDD_Base_theorie_des_empreintes_complete_order_5.tex` defines a domain of objects, contexts, families of probes, and an observation functional. An object's fingerprint is the vector or structured profile of its responses to the selected probes in a given context. Equality of fingerprints defines an observational equivalence relation. The theory studies equivalence classes (fibres), refinement by adding probes or increasing resolution, thresholds, nested hierarchies, ultrametric structure under appropriate assumptions, effective capacity, closure, factorization, dynamics, trajectories, identity, learning, language, prediction, generation, certified transformations, and search.

A key idea is that a transformation can factor through a fingerprint when it is constant on each equivalence class: if two objects are indistinguishable under the retained observations, that transformation cannot legitimately distinguish them using information that the fingerprint does not contain. The theory also studies witnesses and deficits that reveal where a representation is insufficient. Its definitions, hypotheses, propositions, theorems, empirical claims, interpretations, and conjectures must be read according to their actual status in the source; a theorem statement or proof environment is not, by itself, an independent certification of every assumption or derivation.

**Speculation:** if aspects of the real world were adequately modelled by nested levels of observation, fingerprints could describe what an observer can distinguish at a given resolution and what remains observationally merged. In quantum physics, one could explore representations of observational classes that depend on the measurement context. DDD_Base includes a geometric example called the “Naszimger cat,” a reconstruction of a Schrödinger-type structure, and an internal double-slit analogy. A coarse observation might be interpreted as a class containing several possibilities, with a refinement separating them. **However, the source explicitly says that it does not reconstruct Schrödinger's quantum formalism and does not derive a physical conclusion from its double-slit analogy.** It does not derive the Born rule, complex amplitudes, the Schrödinger equation, entanglement, or decoherence. The “Naszimger cat” is an observational class in the model, not an established physical state of Schrödinger's cat. A genuine physical explanation would require a precise mapping to quantum formalism, quantitative predictions, and independent experimental tests.

Outside quantum physics, fingerprint ideas could be investigated in computer vision, sensor fusion, robotics, diagnosis, life sciences, linguistics, and neural-network interpretability: several instruments provide partial views, and a representation must state which distinctions are supported and which remain invisible.

### Observation formalism

The `observation_formalisme_full_0_bundle.zip` contains a main text and three connected source files, 58 traced source chapters, a README, audit material, traceability CSV, manifests, checksums, and scripts. The audit records 8 parts, 51 consolidated chapters, 94 definitions, 3 explicit hypotheses, and 81 theorem/proposition/lemma/corollary-type statements with proof environments. Compilation and the existence of proof environments do not replace independent mathematical review or proof-assistant verification.

The formalism distinguishes the object, context, protocol, observation, record, and fingerprint; invariants under declared transformations; changing components, residuals, and temporal traces; uncertainty, identifiability, inverse problems, and interventions. It notes that a fingerprint cannot reconstruct discarded components, that an inverse problem may have several compatible mechanisms, that an isolated intervention does not by itself establish a complete causal law, and that a sampled signal does not necessarily reveal what happened between samples.

**Speculation:** in quantum physics, the formalism could describe experimental arrangements as contexts and measurements as probes. For the double-slit experiment, it would have to produce quantitative predictions for when interference fringes appear or disappear. For Schrödinger's cat, it can help distinguish description, apparatus, record, and fingerprint, but it does not by itself solve the measurement problem. In biology, medicine, control, remote sensing, astronomy, or chemistry, it could clarify mechanism identifiability and the limits of available data.

### Core theory, CNG/CNC, and AdaptiveRBF

`th_sondes_core_0.tex` and `th_sondes_core_1.tex` formalize probes, cores, computational dependency graphs, hierarchical composition, temporary memory, coordinators, and neuronal/logical/physical realizations. The test texts define the CNG/CNC protocols. `arch_up_formalisme_0.tex` studies adaptive organization of AdaptiveRBF centres through predictive contribution, residuals, redundancy, selection, pruning, and fingerprints.

**Speculation:** coordinated cores could be explored in robotics, scientific simulation, real-time systems, specialized processors, and multimodal AI. A probe might approximate an expensive operator, a logical core might manage the graph, and a physical core might carry out the execution. This is neither a theory of the constituents of matter nor proof of faster execution than conventional architectures. Accuracy, latency, energy, and coordination costs must be measured.

### Fingerprints, LLMs, relational meshes, and eGenBrain

`th_gen_0.tex` and the LLM fingerprint sources propose that meaning and some forms of generalization may be distributed across relational structures formed by contexts and internal fingerprints, rather than localized in a single neuron. One neuron may participate in several structures; polysemanticity is an interpretive research direction, not a cause established by co-activation alone. `eGenBrain_1.tex` formalizes brain meshes, fusion, context, retrieval, and provenance.

**Speculation:** an AI system might organize knowledge as multi-resolution relational structures rather than isolated activations. This could be compared with associative memory, concept formation, and generalization in cognitive science, linguistics, and neuroscience. The sources do not establish equivalence with the human brain or consciousness.

### Compositional programming and constraints

The compositional-programming theories define typed components, contracts, effects, budgets, program/knowledge meshes, inference rules, transformations, memory, synthesis, and verification. They aim to make correctness claims, resource use, permissions, and provenance explicit. Critical and refoundation texts assess earlier formalisms and propose a revised framework.

**Speculation:** these tools could support auditable autonomous systems, reproducible scientific pipelines, certifiable decisions, and constraint-aware robots. Physical-simulation components could carry units, invariants, and validity domains. A well-typed program is not automatically a true model of the world.

### eLLM and language generation

The eLLM formalisms explore a variable-order Markov model in v0 and multi-resolution probes applied to a pretrained LLM in v1.

**Speculation:** contextual fingerprints could improve generation control, structured memory, or detection of contexts in which a model poorly distinguishes two cases. This must be measured on real checkpoints against suitable baselines; it does not establish consciousness, human-like understanding, or general superiority.

### ORDER and proof search

ORDER develops progressive search: observe, synthesize, learn from failure, decompose, obtain local proofs, verify them, and retest the root problem. Documentary or web information remains distinct from formal proof certificates.

**Speculation:** this architecture could assist mathematics, software verification, scientific research, and experimental planning. In physics, it could examine formal consequences of a model and verify calculations, but it cannot by itself decide whether that model describes the universe. Failure to obtain a certificate does not prove that a result is impossible.

## Scientific discipline: established and open claims

Distinguish carefully:

- **Defined:** objects, terms, rules, or architecture have been specified.
- **Implemented:** corresponding code exists in the relevant release.
- **Tested:** a scenario was executed with measurements and logs.
- **Confirmed within scope:** a result holds under the stated protocol and repetitions.
- **Hypothetical or speculative:** a proposal still needs formalization and falsifiable tests.

A software test checks a scenario; an experiment evaluates a hypothesis under a protocol; a mathematical proof holds under its assumptions; an analogy can inspire a question but does not prove it. The reports preserve unfavourable results, edge cases, and provenance gaps because these determine the actual scope of the architectures.

## Releases, languages, and sources

The complete source for each work is available in its corresponding release. Version-specific READMEs identify prerequisites, commands, dependencies, data, and limitations. The reference documentation and reports are in French; translation into another language is the personal responsibility of each reader who undertakes it.

## Author and license

**Bensalem Nassim, with AI assistance.** The author's single general master license is the `LICENSE` file at the root of the `main` branch. It limits the rights held by the Author to non-commercial research; any commercial use requires prior, express, written authorization signed by Bensalem Nassim. Internal notices inside ZIP archives are retained to preserve distributed bytes and SHA-256 fingerprints, but they are not a second general license issued by the Author for material whose rights he owns. This rule does not cancel third-party rights or valid prior grants that cannot lawfully be withdrawn. See `LICENSE` for the full terms.

## Quick map

| Directory | Subject | Contribution |
|---|---|---|
| `AAM/` | Non-LLM agent, observation, memory | ROCA-D, CEGIS, probes, contractual decision-making |
| `FulleGenBrain/` | Compositional programming | Typed AST, 29 operators, synthesis, ASCRC |
| `NGeGenBrain/` | Model observation | Multi-view instrumentation and reconstruction experiments |
| `eGenBrain/` | Relational memory | Context mesh, provenance, abstention |
| `eLLM/` | Language and fingerprints | Variable-order Markov model, learned probes on causal LLMs |
| `models_order/` | Search and proof | Decomposition, synthesis, proof kernel |
| `sondes_experiences/` | Neuronal experiments | AdaptiveRBF, HC-RBF, CNG, CNC |
| `theories/` | Foundations | Fingerprints, observation, cores, LLMs, composition |
| `readme_vHS/` | Accessible material | Introductory explanations |
