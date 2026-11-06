# Specialized Guide to the Theories and Formalisms — Bensalem Nassim

**Declared author: Bensalem Nassim, with AI assistance.** This document is an in-depth guide to the `theories/` directory and the theoretical texts associated with the architectures and experiments. The reference sources and reports are primarily written in French. Readers who translate them are personally responsible for the fidelity and distribution of their translations; a translation is official only if the Author has expressly approved it.

> **Scientific reading rule.** A definition describes an object; a hypothesis proposes a relation; a proposition or theorem is valid under the assumptions and framework stated; an implementation realizes part of a model; an experiment tests a specified protocol. An analogy or speculation is not experimental proof. LaTeX `theorem` or `proof` environments, successful compilation, and audit reports do not replace independent verification of mathematical correctness.

## 1. Overview of the theoretical programme

The theory texts are not a collection of unrelated topics. They explore several levels of one broad question: **how can a system observe, distinguish, represent, connect, compose, and verify information when its access to the world is partial, context-dependent, and resource-limited?**

A cross-reading reveals six themes:

1. **Observation and available information:** what does a system see, through which protocol, with what losses and uncertainties?
2. **Fingerprints and equivalence:** which differences are accessible to an observer, and how can a representation be refined?
3. **Computational architecture:** how should transformations be distributed among probes, cores, and dependency graphs?
4. **Relations and memory:** how can observations, contexts, tokens, concepts, results, and proofs be connected without inventing unobserved relations?
5. **Composition and synthesis:** how can programs or behaviours be built from typed, controlled, verifiable components?
6. **Learning and search:** how can residuals, counterexamples, probe selection, memory, and verification improve a solution?

The emerging vision is an AI architecture built around multi-resolution representations, specialized probes, cooperating cores, relational memory, and verifiable composition. This is a synthesis of directions present in the sources; it is not a claim that a universal artificial brain integrating every mechanism has already been released.

## 2. Fingerprint theory — `DDD_Base_theorie_des_empreintes_complete_order_5.tex`

### 2.1 Mathematical objects and intuition

The text defines a domain of objects `X`, contexts `P`, a family of probes `F`, and an observation function written in the source as `Φ(P,x,f)`. A probe queries an object in a context; the response depends on the protocol and its resolution.

An object's **fingerprint** is the structured profile of its responses to the selected probes. Two objects `x` and `y` are equivalent for this protocol when their fingerprints coincide. This does not say that the objects are absolutely identical; it says that none of the probes under consideration distinguishes them in the specified context.

This is fundamental: observable identity is relative to the discriminating power of the observations. Adding probes, changing their context, or increasing their precision may split a previously indistinguishable class into subclasses.

### 2.2 Fibres, quotient, and refinement

Equality of fingerprints groups objects into **fibres** or equivalence classes. The corresponding quotient describes the distinctions accessible to the protocol. A richer probe family can refine the quotient: it does not necessarily change the objects under study, but it increases the distinctions the system can establish.

The text develops nested probe families, resolutions, separation thresholds, and, under explicit hierarchy conditions, ultrametric-like structures. It also examines effective capacity, closure, and stability of certain representations. These results must always be read with their assumptions: an ultrametric structure does not automatically follow from every arbitrary family of measurements.

### 2.3 Factorization through a fingerprint

A transformation can be described through a fingerprint when it never separates two objects that belong to the same fibre. In other words, when an output depends only on the information retained in the fingerprint, it can factor through the quotient space.

This gives a powerful consistency rule: a system must not produce a distinction that requires information absent from its representation. If two cases have the same fingerprint, any decision based exclusively on that fingerprint must assign them the same result unless a new observation differentiates them.

Witness and deficit notions help identify representational insufficiencies: an additional probe may be required to distinguish cases, a transformation may fail to be constant on a fibre, or a closure assumption may fail.

### 2.4 Scope of the text

DDD_Base goes beyond equivalence classes. It connects fingerprints to questions about:

- observation, invariance, and context change;
- probe families, resolution, thresholds, and hierarchies;
- dynamics, trajectories, order, and fingerprint evolution;
- identity, self-reference, and internal reflection;
- learning, generalization, and meta-observation;
- language, semantics, prediction, and generation;
- certified transformations, witnesses, deficits, and closure;
- constraints, transfer, search, and formal imagination.

These themes form a theoretical programme. Their presence in the same text does not prove that all of them have been implemented or empirically validated.

### 2.5 Double slit, the Naszimger cat, and quantum speculation

The text contains a section on a “double-resolution” experiment with emergent probability and a double-slit-like structure. It also contains a geometric example called the “Naszimger cat” and a reconstruction of a Schrödinger-type structure. These examples are interesting precisely because they make visible the difference between a described state, the distinctions available to an observer, and the information that the protocol cannot separate.

**What the text does and does not claim:** it presents these constructions as examples internal to fingerprint theory. It says that the “Naszimger cat” is not an elementary physical state and that the double-slit reference is a structural analogy internal to the protocol. It also states that the reconstruction is not a reconstruction of Schrödinger's quantum formalism and that no physical conclusion about the quantum phenomenon is derived from the analogy.

**Speculation to investigate:** if some real phenomena depended on what an apparatus can distinguish, observational equivalence classes might provide a language for describing accessible information before and after a measurement. In a two-slit experiment, one could ask whether “path not identified” and “path measured” contexts correspond to different fingerprint families, and whether a mathematical rule for refining observations can quantitatively recover interference statistics. For Schrödinger's cat, one could distinguish the system's state, its coupling to the apparatus, the record, and the observer's viewpoint, then ask whether fingerprint classes correctly describe transitions between levels of description.

At this stage, however, this is not an explanation of quantum mechanics. It would require, among other things: a precise correspondence with quantum state spaces and observables; recovery of the Born rule; an account of complex amplitudes and interference; treatment of entanglement and decoherence; new quantitative predictions; comparison with experiments; and evidence that the predictions are not merely a verbal restatement of existing theory. The presented formalism does not currently derive these results. The “Naszimger cat” must never be presented as an already established physical solution to Schrödinger's cat paradox.

### 2.6 Other possible domains

In vision, an image may be represented by fingerprints at several scales; in robotics, different sensors may produce partially compatible state classes; in diagnosis, several symptoms may be insufficient to distinguish two mechanisms; in linguistics, different contexts may refine the interpretation of a word; in interpretability, probes may distinguish internal states that appeared identical under a coarser measurement. In each case, the scientific question is the same: which distinctions can the selected probe family actually support?

## 3. Observation formalism — `observation_formalisme_full_0_bundle.zip`

### 3.1 Documentary structure

The archive brings together a consolidated text `NGeGenBrain_observation_formalisme_full_0.tex`, complementary sources `NGeGenBrain_observation_formalisme.tex`, `...next_0.tex`, and `...next_1.tex`, their PDFs, separate chapters, a README, audit information, traceability material, manifests, and integrity checks. The structural audit records 8 parts, 51 consolidated chapters, 94 definitions, 3 explicit hypotheses, and 81 theorem-, proposition-, lemma-, or corollary-type statements with proof environments. These figures describe the document's structure; they do not independently certify the validity of every derivation.

### 3.2 Conceptual distinctions

The formalism separates several notions that are often conflated:

- **object:** what one is trying to know;
- **context:** the conditions under which observation takes place;
- **protocol/probe:** the operation that queries or transforms access to the object;
- **observation:** the result obtained through the protocol;
- **record:** the retained trace of the result;
- **fingerprint:** a structured representation built from the retained observations.

This separation makes it possible to ask precise questions: does the record preserve all information from the observation? Is the fingerprint sufficient for a decision? Does a declared transformation preserve the relevant invariants? Does a new observation reduce uncertainty, or merely repeat information already present?

### 3.3 Residuals, time, intervention, and inverse problems

The texts explore invariant and changing components, residuals, temporal traces, complementary observations, interventions, identifiability, and inverse problems. A mechanism may be compatible with several observations; in that case, available data are not sufficient to identify it uniquely. An intervention may provide an additional distinction, but an isolated intervention does not automatically prove a general causal law.

The formalism also invites caution about time and sampling: measurements at selected instants do not necessarily reconstruct what happened between them. A fingerprint may be useful while intentionally incomplete; it does not recreate components lost during observation or compression.

### 3.4 Speculation: observation and quantum physics

One possible correspondence would describe an experimental preparation as a context, an apparatus as a family of probes, a measurement as an observation, and the retained output as a record or fingerprint. In the double-slit experiment, it would then be interesting to formalize the conditions that make path information available or unavailable and determine whether the formalism can express the change in interference statistics.

For Schrödinger's cat, the framework can help separate levels of description: system, environment, apparatus, trace, observer. It can also help avoid conflating the observer's ignorance with a physical property of the system. However, it does not by itself solve the measurement problem, derive the Schrödinger equation, or demonstrate a particular interpretation of quantum mechanics. A physical application would require an explicit mathematical bridge, compatibility with established results, and risky predictions that could be falsified.

### 3.5 Other speculative applications

In medicine, this formalism could help determine whether clinical measurements genuinely distinguish several mechanisms or merely several compatible presentations. In astronomy and remote sensing, it could characterize what instruments allow one to identify despite noise and indirect observations. In chemistry and materials science, it could organize observed signatures and the identifiability limits of mechanisms. In control and robotics, it could structure the transition from sensor data to a state representation and then to an intervention. These remain application programmes to be tested.

## 4. Core and probe theory — `th_sondes_core_0.tex`, `th_sondes_core_1.tex`

### 4.1 A probe as a transformation unit

The texts describe a probe as an operator that takes inputs and produces outputs. Depending on the case, it can be exact, symbolic, or learned. An adaptive probe may approximate a function; a set of probes may divide a calculation or represent several specializations.

For AdaptiveRBF, the described scheme includes a latent encoding of the form `z = tanh(Wx+b)`, Gaussian radial bases `r_k(z) = exp(-||z-c_k||²/(2σ_k²))`, and an output combination depending, among other things, on centre, width, and weight parameters. This helps explain why the architecture is not simply an MLP under another name: it relies on local activations around centres and an adaptive organization of those centres.

### 4.2 Three cores, three roles

The **neuronal core** is the part that learns transformations through adaptive probes. The **logical core** describes the functional structure: operations, their dependencies and order, independent elements, and reusable results. The **physical core** concerns a possible hardware realization: compute units, memory, buses, communications, controller, latency, bandwidth, energy, and area.

This separation matters for computer architecture. A logical graph may contain parallelism, but parallelism yields a real benefit only when hardware, communication, scheduling, and synchronization costs allow it. The theory therefore introduces costs and coordination states, with actions such as activation, waiting, transmission, reuse, storage, and merging.

### 4.3 Speculation about AI and computing architectures

One can imagine an AI system whose capabilities are distributed among specialized cores: perception, numerical computation, memory, symbolic reasoning, validation, and planning. The logical core would establish dependencies and contracts; the neuronal core would provide learned approximations; the physical core would execute work units under resource constraints.

This vision can be compared with neurosymbolic architectures, specialized accelerators, and distributed systems. It does not establish that the human brain literally contains these three cores, nor that such a system is more efficient than a GPU or an MLP. Comparisons must measure quality, generalization, latency, power consumption, memory, and coordination costs.

## 5. CNG and CNC protocols — `th_sondes_core_test_0.tex`, `th_sondes_core_test_1.tex`

### 5.1 CNG: General Neuronal Core

CNG studies cooperation among a set of probes to approximate a general function. Discussed configurations include a single AdaptiveRBF, fixed-mean ensembles of different sizes, learned composers, capacity-matched MLPs, and specialized variants. The objective is to measure whether probes complement one another, whether their combination is useful, and how performance changes across regimes.

### 5.2 CNC: Computational Neuronal Core

CNC replaces or approximates particular operators with specialized probes: ADD, SUB, MUL, DIV, EXP, LOG, and other operations in the protocol. Graphs assemble these operators to realize a composite function. Experimental configurations distinguish, among others, frozen specialists, jointly fine-tuned specialists, a direct MLP, a direct RBF operator, and an exact oracle.

The fact that the initial graph is supplied is an important limitation: showing that neuronal operators can execute correctly in a supplied graph is not the same as showing that an agent can autonomously discover the best graph for every problem.

### 5.3 What the campaigns show

EX10 reports 460 CNG runs and 90 CNC runs, 1,695 test evaluations, several functions, and five seeds in the described sets. Results are mixed and task-dependent: some CNG variants outperform matched MLPs on selected functions or evaluation regions; other variants or tasks favour the MLP. Some jointly fine-tuned CNC configurations improve certain graphs and degrade others. EX11 is described as exploratory, and some variants rely on few seeds.

EX12 provides a more controlled confirmatory HC-RBF/MLP comparison with trainable parameter counts matched within ±1%. The report presents 320 candidate–MLP pairs, 640 models, and 2,560 evaluations across four regimes. It reports HC-RBF advantages in boundary regimes in 15/16 contrasts and interpolation gains in selected cases, but no general superiority. All four variants lose on `f1_sin` interpolation; extrapolation is unfavourable on three functions. Batch-1 p50 latency is about 1.82–2.25 times the full MLP pipeline and training time about 1.44–1.62 times higher. The interesting result is therefore specialization and sometimes useful coverage, alongside clear limits in extrapolation and resources.

## 6. Adaptive RBF centre organization — `arch_up_formalisme_0.tex`

This text studies a more deliberate organization of centres in AdaptiveRBF. It addresses predictive contribution, residuals, ablations, redundancy, progressive selection, pruning, and retraining. One idea is to guide weaker centres using residuals or contributions associated with stronger centres. Another is to organize centres using fingerprints describing position, activation, contribution, and redundancy.

Variants B0 to B5 structure an experimental programme ranging from a baseline to ranking, selection, guidance, fingerprint-based organization, and combinations of these strategies. These are falsifiable hypotheses about centre usefulness and stability, not proof that adaptive selection systematically improves generalization.

**Speculation:** fingerprint-based organization might help interpret functional subregions, diagnose redundancy, or construct more specialized networks. This could be relevant for scientific or embedded models where one wants to explain which centres carry a contribution. It would be necessary to verify that the fingerprints remain stable across datasets, distribution shifts, and random seeds.

## 7. Theories of brains, LLMs, and relational memory

### 7.1 `th_gen_0.tex` and language-model fingerprints

These texts explore the idea that linguistic understanding and some forms of generalization may be distributed across contextual relational structures rather than localized in a single neuron. One unit can contribute to several patterns or structures; this idea relates to polysemanticity, but co-activation or a probe projection alone does not prove the actual internal mechanism.

**Speculation:** contextual fingerprints could help identify semantic distinctions, shared representations, or generalization limits. In neuroscience, these constructions could be compared with hypotheses about distributed representations; in linguistics, with networks of relations between contexts and meanings. This does not demonstrate identity with the human brain or consciousness in an LLM.

### 7.2 `eGenBrain_1.tex` and relational mesh

The eGenBrain formalization describes the construction of a brain per source, canonicalization of identities, token order and relations, and then fusion into a global mesh and a prompt-context mesh. Unknown relations remain unknown; causality and anti-causality are explicit and must not be inferred from simple lexical frequencies. Result states distinguish, among others, FOUND, NO_MATCH, and UNKNOWN, with provenance.

**Speculation:** such a mesh could serve as verifiable memory for an agent, an evolving knowledge base, or a research assistant. In life sciences, it could organize relations among observations, hypotheses, and mechanisms without equating documentary correlation with biological causation.

### 7.3 eLLM theories v0 and v1

Version v0 formalizes a variable-order interpolated Markov chain based on suffixes and nested probes. Version v1 studies multi-resolution probes trained on contextual hidden representations of a pretrained causal LLM, followed by logit correction and learned transport components. These two designs must remain distinct.

The documented component tests and synthetic datasets do not demonstrate a quality gain on a real checkpoint if that checkpoint was not loaded and evaluated under the corresponding protocol. The research direction is architectural: enrich context using probes and a memory or correction structure, then measure the result against controlled baselines.

## 8. Theories of compositional programming and synthesis

The compositional-programming texts study components, interfaces, types, contracts, effects, resources, graphs and meshes, transformations, composition rules, memory, provenance, and verification. Some works address program synthesis, hierarchical decomposition, CEGIS, and execution control.

The vision is to make composition explicit and controllable: each block exposes what it receives, what it produces, its effects, constraints, and cost. Rules assemble blocks while checking incompatibilities. Critical and refoundation texts also examine limitations of previous formalisms.

**Speculation:** these ideas could help design scientific assistants that assemble reproducible procedures, robots that must respect permissions and resources, or programs that explain themselves through a verifiable graph. In physics, an operator library could include units, dimensions, and invariants; however, formal program correctness does not prove the empirical truth of its assumptions.

## 9. ORDER and proof

ORDER texts study iterative and structured search: prioritize a goal, decompose it, create subproblems, search for candidates, use acquired information, and verify certificates through a kernel. Documents and web pages may provide context, but do not automatically become axioms or proofs. An expired budget or interrupted search does not prove that the target proposition is impossible.

**Speculation:** a certified search architecture could assist mathematics, software verification, model discovery, and experiment planning. In physical sciences, it could verify that deductions follow from a model, but it cannot decide without data whether that model correctly describes the world.

## 10. Links between theories and software categories

| Theory or formalism | Related architecture or category | Main question |
|---|---|---|
| DDD_Base, fingerprints | AAM, eGenBrain, eLLM, probes | Which distinctions does observation preserve? |
| Observation formalism | NGeGenBrain, probes, AAM | How to separate object, context, measurement, trace, and fingerprint? |
| Core theory | CNG/CNC, AdaptiveRBF, experiments | How to distribute and coordinate transformations? |
| AdaptiveRBF upgrade | HC-RBF and EX12 campaigns | Which centres are useful, stable, or redundant? |
| LLM/brain fingerprints | NGeGenBrain, eLLM | How do internal representations depend on context? |
| eGenBrain relational theory | Relational memory | How to merge knowledge without inventing links? |
| Compositional programming | FulleGenBrain | How to compose programs under contracts and constraints? |
| ORDER search | models_order | How to produce and verify certificates? |

## 11. Other theory texts and reports: the role of each item

The `theories/` directory also contains texts that extend the foundations described above. They should not be treated as mere appendices: several clarify the actual status of implementations, critically assess experimental results, or propose a general architecture.

### Fingerprints and language models — `source_th_emp_llm_0.tex` and `source_th_emp_llm_v02.tex`

The first text brings together the observational foundation of fingerprints and a proposal for an information architecture for language models. It examines activations, latent states, and attention weights as possible observables, then seeks to describe their contextual organization. It distinguishes the mathematical foundation from architectural choices and empirical hypotheses. Version v02 develops the notions of raw capacity, effective information and dimension, observational closure, and empirical measurement of thresholds; it proposes a processing chain from context and probes to fingerprint, observational quotient, mesh, optional memory, transport, and prediction. These are formalisms and engineering proposals; their effectiveness must be measured against baselines on real models.

### Brain and eGenBrain extensions — `th_gen_0.tex`, `th_brain_gen_0.tex`, `th_eGenBrain_0.tex`, `eGenBrain_1.tex`, `formalisme_eGenBrain_v1.tex`

`th_gen_0.tex` studies the hypothesis that some forms of understanding, memory, knowledge, and generalization in a language model depend on distributed information structures rather than concepts individually located in a single unit. `th_brain_gen_0.tex` and `th_eGenBrain_0.tex` are related theory files and were byte-identical in the inspected snapshot; the corresponding release versions remain the proper references to cite.

`eGenBrain_1.tex` develops the relational model: brains per source, canonical identities, ordered occurrences, relations, fusion, context, provenance, and search states. `formalisme_eGenBrain_v1.tex` makes the model operational and links it to the delivered code: source observations, normalization, tokenization, durable individual brains, global mesh, prompt mesh, alignment, provenance, and the states `FOUND`, `NO_MATCH`, and `UNKNOWN`. `FOUND` means that the implemented structural criterion accepted a candidate; it does not guarantee factual truth or semantic relevance. The formalism also states that relation frequency does not prove causality and that the pipeline does not implement all of DDD_Base.

### eLLM formalisms — `formalime_model_eLLM_v0.tex` and `formalise_model_eLLM_v1.tex`

The v0 formalism concerns the actually implemented variable-order interpolated Markov model and its nested suffix probes. The v1 formalism describes a different architecture: multi-resolution probes learned from contextual hidden states of a pretrained causal LLM, learned transport, and logit correction. The v1 text emphasizes correspondence between the DDD_Base formalism and the engineering components actually claimed. These documents define architectures and protocols; they do not guarantee quality gains on a real checkpoint unless the corresponding test has been run.

### Compositional programming — `theorie_programation_compositionnelle_2.tex`

Version 2 develops semantics, effects, ASCRC, reversible activation, living memory, synthesis, and verification in connection with FulleGenBrain_4. It addresses compositions of pure functions as well as stateful processes involving observation, search, recovery, and controlled program transformation. A component is described by its identifier and version, input/output types, preconditions and postconditions, effects, resources, execution semantics, provenance, and verification mechanism.

The text separates **ASCR**, an existing eGenBrain v4 mechanism, from **ASCRC**, a proposed reversible regulator. It explains that putting compositions to sleep can reduce the number of active candidates held in memory, but does not magically reduce the total number of possible candidates: lazy search, contract filtering, sharing, justified deduplication, and resumability remain necessary. It also distinguishes artefact-observed facts, definitions, design invariants, properties proved under assumptions, and effects still to be tested.

### Mesh-based compositional programming — versions 3 and NG0

`theorie_programation_compositionnelle_3.tex` proposes connecting program algebra and semantics to a layered mesh inspired by eGenBrain: canonical identities, occurrences, typed facts, multi-premise rules, operators, provenance, observation supports, certificates, and activation. The mesh is not presented as a simple knowledge graph: it connects several layers — data, control, state, effects, resources, contracts, proofs, and lifecycle — without conflating them. The text aims at general program composition, with a computational core, intermediate representation, types and effects, capability boundaries, compilation, error handling, and recovery.

`theorie_programation_compositionnelle_NG_0.tex` extends this direction toward a general kernel, semantics, verification, evolution, and accessible interfaces. The correction and safety properties discussed are conditional on the specified assumptions, rules, and sublanguages. They do not mean that an arbitrary implementation or every possible program is automatically safe or correct.

### Critique and refoundation of composition — `rapport_et_proposition_th_PC_0.tex`

This report compares the earlier compositional framework with the eGenBrain v4 formalism. It recognizes the contributions of contracts, effects, memory, synthesis, and reversible activation, as well as those of canonical identities, occurrences, typed facts, hyper-rules, operators, and certificates. It concludes that neither framework, taken alone or merely placed side by side, yet replaces all of classical programming. The proposed refoundation therefore aims to make composition a general mode of representing, defining, executing, transforming, and explaining programs while preserving the expressiveness of the target language. The report rejects both reducing composition to an orchestration DSL and promising an unproved universal guarantee.

### EX3–EX10 and EX12 reports

`rapport_analyse_ex3_ex10.tex` is a critical analysis of RBF probe experiments, OOF correctors, coordinators, and numerical operators. It shows that reductions in parameter count were often achieved and documented, but that compactness did not automatically translate into lower latency or execution cost. Predictive results depend on the domain; some synthetic or classification tasks are favourable, while others strongly penalize variants relative to the MLP. This report provides historical context for why accuracy, parameter count, training, inference, and coordination costs must all be measured.

`EX12_FINAL_SCIENTIFIC_REPORT.tex` develops this question through a confirmatory HC-RBF/MLP comparison with matched trainable capacity. It reports specific advantages on boundary regimes, extrapolation losses, and higher latency. The centre report also examines stability and usefulness: few centre hypotheses pass both statistical and utility criteria. The proper scope is a nuanced experimental characterization, not a universal HC-RBF victory.

### Bundle `pack_complet_PC_NG.zip`

This bundle includes, among other items, compositional programming theory version 2, the eGenBrain v4 formalism, the critique/refoundation report, and the mesh-based NG0 compositional theory, with their corresponding PDFs and a deliverables README. It allows the texts to be read as a coordinated body of work: operational architecture, relational foundation, critical analysis of gaps, and a refoundation proposal. Versions and manifests should be retained when citing or reproducing results from the bundle.

## 12. How to evaluate a claim arising from these theories

For each claim, ask at least the following questions:

1. What mathematical object is defined, and which assumptions are required?
2. Is the result proved in the text, or merely conjectured or illustrated?
3. Is there an implementation in the corresponding release?
4. Which experimental protocol was run, with what data, seeds, baselines, and metrics?
5. Are negative results and limitations reported?
6. Is independent validation or replication available?
7. Does the conclusion go beyond the data or formalism actually presented?

A theory can be ambitious and useful even if its physical application remains speculative. Rigour means preserving that distinction, not diminishing the ambition or turning a hypothesis into a fact.

## 13. Sources, releases, language, and license

The complete source for each work is available in its corresponding release. Theory bundles may include LaTeX sources, PDFs, fragments, reports, scripts, manifests, and checksums; any citation or reproduction must identify the precise version. The reference reports and documentation are written in French. Translation is the personal responsibility of the reader who undertakes it.

The Author's general license is the single `LICENSE` file at the root of the `main` branch. It permits only non-commercial research uses to the extent of rights owned or controlled by Bensalem Nassim. Any commercial use requires prior, express, written authorization signed by the Author. Internal license files retained in archives are preserved to maintain bytes and SHA-256 fingerprints; they are not a second general license issued by the Author for his own material. This statement cannot cancel valid third-party rights or permissions that cannot lawfully be revoked. See `LICENSE` for the full terms.
