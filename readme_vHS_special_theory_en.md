# The Theories Explained Simply — A Special Guide for High-School Students

**Works by Bensalem Nassim, with AI assistance.** This guide introduces the ideas in the theory texts using simple language. The reference documents and reports are written in French; any translation made by a reader is that reader's personal responsibility.

## Before we begin: what is a theory for?

A theory is like a detailed plan. It says which objects we study, which words we use, which rules connect those objects, and under what conditions the rules are true. A program is then one way to put some of those ideas into practice. An experiment checks what happens in a specific setting.

So we must not confuse a good idea with a proven result. Even a document containing many formulas, definitions, or proofs should be open to review and verification by other specialists.

## 1. Fingerprint theory: knowing through observations

### A story to understand the idea

Imagine two closed boxes. You want to know whether they contain the same object, but you are not allowed to open them. You can weigh them, gently shake them, listen to the sound, and measure their temperature. You obtain a list of answers.

If all the answers are identical, you still cannot be certain that the objects are identical. You only know that your tests did not manage to distinguish them. A new test might reveal a difference.

This is the basic idea of **fingerprint theory** in `DDD_Base_theorie_des_empreintes_complete_order_5.tex`.

### Important words

- An **object** is what we want to study.
- A **context** describes the conditions under which we observe it.
- A **probe** is a question or measurement applied to the object.
- A **fingerprint** is the organized collection of the answers obtained.
- An **equivalence class** groups objects that the selected probes cannot distinguish.

A fingerprint is therefore not the object itself. It is more like an identity card built from the information available. If the card is too short, several different objects may have the same card.

### Why is this idea powerful?

It forces a system to respect the limits of what it knows. If two objects have the same fingerprint, a program that uses only that fingerprint should not invent a difference between them. To distinguish them, it needs additional information.

The text also studies fingerprints at several levels of detail. We can begin with a few questions and then add finer questions. It is like a map: a country map shows large regions; a city map shows streets; a detailed plan shows doors and stairs.

### Speculation about the real world

We can imagine that some real-world situations are better understood by separating what is observed from what is not observed. This could be useful with cameras, radar, medical instruments, robots, or artificial-intelligence models. Different instruments do not necessarily see the same details; fingerprints could help compare their information.

### The possible connection with the double-slit experiment

In quantum mechanics, the two-slit experiment produces interference patterns under certain conditions. When one tries to obtain information about which path a particle took, the experimental result can change.

A speculative question would be: can the two situations be described using two different observation contexts, with the available information in each represented by fingerprints? Can precise mathematical rules recover the measured numbers from the experiment?

We must be very clear: **the DDD_Base text presents the double-slit comparison as a structural analogy and says that it derives no physical conclusion from it.** It does not prove quantum mechanics or calculate the interference fringes. To become a genuine physical theory, it would need to recover the equations and results of quantum theory, make numerical predictions, and test them.

### Schrödinger's cat and the Naszimger cat

Schrödinger's cat is a thought experiment created to discuss a difficulty in quantum measurement. In the fingerprint text, an example is called the “Naszimger cat.” It is used to illustrate an observational class: several possibilities may remain indistinguishable because the observations do not separate them.

It is not a real cat in a quantum state described by an experiment. Nor is it a proven solution to Schrödinger's cat problem. The speculative idea is to distinguish three things: what happens in the system, what the apparatus can measure, and what the observer knows. To explain quantum physics, a precise link to the states, measurements, probabilities, and experiments of that theory would have to be demonstrated.

## 2. The observation formalism: carefully separating what we see

The `observation_formalisme_full_0_bundle.zip` bundle develops the topic of observation in more detail. It contains a main text, additional texts, chapters, PDFs, tracking files, and integrity checks.

It emphasizes words that sound similar but do not mean the same thing:

1. **Object:** the thing being studied.
2. **Context:** the conditions of the study.
3. **Probe or protocol:** the way a question is asked or a measurement is made.
4. **Observation:** the result obtained.
5. **Record:** the trace that is kept.
6. **Fingerprint:** the organized summary built from selected observations.

Imagine a security camera. The real scene is the object; light and camera angle are part of the context; the camera is the instrument; the images are observations; the video file is the record; a summary describing movements is a fingerprint. Each step may lose details.

The formalism also studies changes over time, complementary observations, measurements that help distinguish several explanations, and situations where several causes may produce similar observations. It reminds us that a small number of measurements cannot always reconstruct everything that happened between them.

**Quantum speculation:** a laboratory could be described as a context, an apparatus as a set of probes, and the results as records. For the double slit, one would have to calculate precisely the results depending on whether path information is available. For Schrödinger's cat, one would have to distinguish the system, apparatus, environment, trace, and observer. This vocabulary can help formulate questions, but the formalism does not currently solve the measurement problem.

**Other possible fields:** medicine, astronomy, chemistry, machine control, robotics, and Earth observation. In these areas, the question would be what the instruments really allow us to conclude and which explanations remain possible.

## 3. Cores: learning, organizing, and executing

The texts `th_sondes_core_0.tex` and `th_sondes_core_1.tex` describe probes and three kinds of core.

- The **neuronal core** learns to transform information. It can use adaptive probes.
- The **logical core** organizes calculations into steps and indicates which steps depend on one another.
- The **physical core** concerns the machine that performs the calculations: chips, memory, connections, energy, and speed.

Let's return to the kitchen example. A cook may know a recipe; the recipe gives the order of actions; ovens, stoves, and utensils make those actions possible. If the kitchen is too small, the oven is slow, or two people are waiting for the same tool, the recipe alone will not save time.

The sources also describe computational graphs and a coordinator that can activate, wait, transmit, reuse, store, or merge results.

**Speculation:** an AI might distribute tasks among several cores: one learns, another organizes operations, and a third executes everything on hardware. This could inspire robots, computing accelerators, or scientific systems. It would be necessary to measure whether this organization is actually more accurate, faster, or cheaper. The texts do not prove that the human brain is built exactly this way.

## 4. CNG and CNC: two families of experiments

CNG brings together probes that learn a function as a team. We can compare this method to a group of people who each suggest an estimate and then combine their answers.

CNC uses probes designed for specific operations: addition, multiplication, division, exponentials, or logarithms. They are connected to form a longer calculation. This resembles a chain of small machines, each responsible for one step.

The experiments compare these architectures with MLPs, direct RBF probes, or exact operations. The results are not all the same: some tasks favour certain variants, while others favour MLPs. In the described experiments, the calculation plan may be supplied in advance; we should not assume that CNC can already choose the optimal plan by itself in every situation.

**Speculation:** if these architectures become more reliable, a CNG might combine several ways of estimating a situation, while a CNC might turn a complicated calculation into small specialized operations. This could be studied in robotics, simulation, signal processing, or scientific computing. One would have to check that errors do not accumulate and that coordination does not cost more than the computation it saves.

## 5. AdaptiveRBF and HC-RBF: organizing the centres

An RBF network uses centres that respond to inputs close to their positions. Imagine landmarks on a map: each one recognizes a particular region more strongly.

The AdaptiveRBF and HC-RBF work studies how to choose centres, determine which ones add new information, identify redundant centres, remove some centres, and retrain the network. It also uses fingerprints to describe a centre's position, activation, and contribution.

The EX12 reports show advantages in some cases, especially certain tests near the boundaries of functions. But they also show extrapolation losses on several tasks and higher time costs than MLPs. This does not make the architecture worthless: it tells us more precisely where it deserves further study and where it needs improvement.

**Speculation:** if centres are organized in a stable way, they might help explain which regions of a problem are recognized by a network. This could be useful for scientific models or embedded systems. This stability would have to be confirmed on new data and new contexts.

## 6. Fingerprints in language models and relational memory

Some texts study the idea that a language model may distribute information among several internal units and relationships. This raises a question: is the meaning of a sentence always located in one neuron, or does it depend on a group of activations and on context?

This is an interpretive research direction. An activation measurement or probe experiment is not enough to explain the complete internal mechanism of a large model.

`eGenBrain` explores memory in the form of a network of relationships. It connects words, contexts, and information, while keeping track of where they came from. When it does not know whether a link exists, it should be able to answer “unknown” rather than make up an answer.

**Speculation:** this kind of memory could support a research assistant or help organize scientific knowledge. In neuroscience, some ideas could be compared with associative-memory models, but this does not prove that the software reproduces the human brain or has consciousness.

## 7. Language, program composition, and proof search

### eLLM

eLLM explores two paths: one version uses a Markov-type model with several context lengths; another studies probes learned from the internal representations of a pretrained LLM. The aim is to test whether contextual information can be better organized or used. Component tests alone do not prove a general improvement in language quality.

### Compositional programming and FulleGenBrain

The composition theories explain how to assemble program blocks with rules, types, contracts, and resource limits. It is like building an object from pieces whose shapes and functions are known. The FulleGenBrain engine implements part of these ideas.

A good verification process can show that a program follows its written rules. It does not automatically prove that the starting assumptions correctly describe the real world.

### ORDER

ORDER studies how to split a complex question, search for solutions, learn from errors, and check proofs. A result must pass through the verification kernel. Not finding a proof before the available time runs out does not mean that no proof exists.

**Speculation:** these methods could help verify programs, organize scientific experiments, and check calculations in mathematics or physics. They verify reasoning based on given rules; they do not replace the observations needed to know whether a theory really describes nature.

## 8. More theories: building programs and understanding relationships

### Compositional programming version 2

Version 2 explains how to build programs from components that each have a contract. A contract is like an instruction card showing what a block accepts, what it must produce, which resources it may use, and which errors can occur. The theory also discusses memory, search, recovery after interruption, and verification.

It distinguishes ASCR, a mechanism from eGenBrain v4, from ASCRC, a new proposal for reversible regulation. Putting a composition to sleep can save active memory, but it does not make all possible programs disappear. Candidates must also be filtered, justified repetitions avoided, and search organized.

### Mesh-based compositional programming: versions 3 and NG0

Versions 3 and NG0 propose connecting program-composition rules with a mesh inspired by eGenBrain. This mesh connects data, control steps, program state, effects, resources, contracts, proofs, and history. It is not just a map of words: it aims to represent how a program is built, runs, changes, and can be verified.

The goal is ambitious: to make composition a general way of building programs, not merely a small language for connecting a few tasks. The correctness guarantees discussed remain tied to the assumptions and sublanguages described in the texts.

### The critical refoundation report

`rapport_et_proposition_th_PC_0.tex` compares compositional-programming work with the eGenBrain v4 relational model. It explains what each approach contributes and what is still missing before either can replace all of classical programming. It proposes a more general refoundation, but does not claim that a theory has already proved it can program everything with automatic safety.

### The experimental reports

`rapport_analyse_ex3_ex10.tex` reviews earlier experiments on RBF probes, corrections, coordinators, and specialized calculations. It shows that having fewer parameters is not enough to be faster: additional calculations and communication among probes can cost time.

`EX12_FINAL_SCIENTIFIC_REPORT.tex` examines HC-RBF against MLPs with comparable capacity. It finds advantages in some boundary tests, but also extrapolation difficulties and higher latency. The full result matters, not only the best numbers.

### Fingerprint theories for language models

`source_th_emp_llm_0.tex` and its v02 version apply fingerprint ideas to internal representations of language models. They propose studying how contexts, activations, and probes can form information structures. `th_gen_0.tex` goes further by asking whether some forms of understanding and generalization may be distributed across several relationships rather than stored in one neuron. This is a scientific hypothesis to test, not a confirmed discovery about every model.

### The two eLLM formalisms

The eLLM v0 version describes a Markov-type model with several memory lengths. Version v1 studies probes learned from the representations of a pretrained causal LLM and corrections to its outputs. These are two different architectures. Their results must be measured separately on real models.

### Research bundles

`pack_complet_PC_NG.zip` brings together several compositional-programming texts, their critique, and a refoundation proposal, with PDFs and a README. The theory folder also includes eGenBrain texts and formalisms that connect data, words, occurrences, relations, and proofs. These archives help track how the ideas developed and how they connect.

## 9. How do all these theories fit together?

We can draw the overall vision as a loop:

1. The system observes a situation using probes.
2. It builds a fingerprint to summarize what it knows.
3. It connects that information to its memory and context.
4. It chooses operations and distributes them among cores.
5. It composes a solution or an action.
6. It verifies the result and seeks new observations when necessary.

The loop can start again when the system discovers an error or missing information. This picture brings together several ideas from the sources; it does not mean that one system already performs every step perfectly.

## 10. How to read this work with a scientific mindset

For each idea, ask:

- Is it a proposal, a definition, or a demonstrated result?
- Is there a program that puts it into practice?
- Which experiment was performed?
- Which results were positive and which were negative?
- Is the conclusion broader than what the experiment allows us to say?

Good research does not hide failures. It describes them, explains their scope, and proposes more precise tests.

The complete source for each work is published in its corresponding release. The reference documents and reports are in French; each reader who translates a document is personally responsible for the quality of that translation.

## 11. Author and license

The works are attributed to **Bensalem Nassim, with AI assistance**. The single general license is `LICENSE`, at the root of the `main` branch. It permits only non-commercial research use of material whose rights are owned by the Author. Any commercial use requires prior written authorization signed by Bensalem Nassim.

Older license notices retained inside some ZIP files have not been removed so that the bytes and SHA-256 fingerprints of the files remain unchanged. They do not form a second general license from the Author for his own material. Valid third-party rights remain separate and cannot be removed by this statement.

## The big question to remember

What if intelligence did not just mean calculating an answer, but also knowing how it was obtained, which information supports it, which questions remain open, and how to verify the result? This is one of the big questions connecting these works. It remains open to research, criticism, and new experiments.
