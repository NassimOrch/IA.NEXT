# An Invitation to Discover the Research of Bensalem Nassim

*An introduction for high-school students*

**Author of the works: Bensalem Nassim, with AI assistance.** AI helped with some tasks; it does not replace the author or the need for scientific verification.

## 1. One big idea: building intelligence with several tools

Imagine arriving in a city you do not know. You do not know all its people, streets, or rules. You can look at a map, listen to people, watch traffic lights, walk through the streets, and compare what you learn. Each method gives you part of the information. None shows you the entire city at once.

Many of the works introduced here start from a similar idea: **an intelligent system must learn to observe, organize what it observes, connect information, choose what to examine next, and verify its conclusions.** A large neural network is not always enough. It is also possible to build an architecture from several tools that cooperate.

The overall vision resembles a team: some units learn, others organize the steps, others keep memory, and others check the result. The sources explore these ideas through several projects, theories, and experiments.

## 2. Important ideas, explained with simple examples

### Fingerprints: recognizing things through clues

Imagine trying to recognize an animal without seeing it directly. You could ask several questions: does it have feathers? How many legs does it have? Can it fly? Each answer is a clue. Together, the answers form a kind of fingerprint.

In fingerprint theory, an object is studied using questions called **probes**. Two objects can have the same fingerprint when the questions asked cannot distinguish them. Adding a more precise question may reveal a difference.

This teaches an important rule: we should not claim to know information that our observations cannot reveal.

### Probes: small specialized tools

A probe is like a small tool that receives information and produces an answer. Some probes follow an exact rule; others learn from examples. Several probes can share a task.

### MLP and RBF networks

An MLP is a well-known family of neural networks. You can imagine it as a large team of computing units that gradually transforms information.

RBF networks work differently: they use centres and respond more strongly in certain regions of the input space. Imagine landmarks that recognize situations close to their positions.

The AdaptiveRBF and HC-RBF work studies how to organize these centres, measure their usefulness, remove redundant ones, and combine their responses. The aim is to explore architectures other than MLPs or replace selected parts of a network. The experiments do not show that RBF networks always win: the answer depends on the problem and the way it is measured.

### Three cores: three different jobs

The word **core** means an organized computing unit here. The sources distinguish three roles:

- The **neuronal core** learns transformations through adaptive probes. It is the part that learns how to respond to situations.
- The **logical core** organizes the work: which operation comes first? Which tasks can run at the same time? Which result can be reused?
- The **physical core** concerns the real machine that performs the work: processor, memory, communication, energy, and computing time.

Compare this with a kitchen: recipes and the order of steps are the logical side; cooks and their skills are the side that performs operations; the kitchen, ovens, utensils, and electricity are the physical side. A good recipe does not guarantee a quick meal if the oven is slow or everyone is waiting for the same tool.

### CNG and CNC: two ways for probes to work together

**CNG** (General Neuronal Core) brings several probes together to learn a function. It is like asking several specialists for an answer and then combining their opinions.

**CNC** (Computational Neuronal Core) uses probes specialized in operations: addition, multiplication, division, exponentials, logarithms, and others. They are assembled in a computational graph, like connected steps in a recipe.

CNG mainly aims to learn a function using several probes. CNC studies how specialized operators can perform a compound calculation. In some experiments, the operation plan is given in advance; this does not yet mean that the system can always invent the best plan by itself.

## 3. The projects: a research team

### `AAM/` — an agent that observes before deciding

AAM studies an agent that observes a situation, consults its memory, asks whether the information is sufficient, and then chooses another question or an action. It can learn from mistakes through counterexamples. The idea is to build an organized agent without requiring a large language model to sit at the centre of every decision.

### `FulleGenBrain/` — building programs like structures made from blocks

FulleGenBrain studies how to build a program from blocks, each with a role, inputs, outputs, and rules. Like building with construction blocks, we want to check that the pieces fit together correctly. The relevant engine includes a tree-shaped program language, a validator, and an interpreter for 29 operators in the version concerned. It also explores program search and the ability to resume an interrupted search.

### `NGeGenBrain/` — observing how language models work

NGeGenBrain studies ways to observe several parts of a language model and combine some of that information. It is a little like trying to understand a machine by looking at several gauges and performing controlled tests.

One documented experiment attempted to recompose a small model using information extracted from other models. The results reported in this folder remain limited: the tested recomposition did not outperform the source models on the reported measure. The value lies in studying the method and identifying exactly where it works or fails.

### `eGenBrain/` — memory made of relationships

eGenBrain organizes information as a network of links: a word, context, idea, or fact can be connected to other elements. It keeps track of where information came from and distinguishes three useful situations: an answer was found, no match was found, or the information is unknown. Saying “I don't know” is better than inventing a link.

### `eLLM/` — trying other ways to support a language model

eLLM studies fingerprints and probes in language processing. One version explores Markov-type models with several context lengths; another studies adding learned probes to the internal representations of a large language model. These are not the same approach, and the available tests do not prove a general improvement across all models.

### `models_order/` — searching for a solution and checking a proof

ORDER organizes a search into several steps: split a large problem, try possible paths, learn from failures, and check proofs with a verification kernel. Finding a text that claims something is not enough: the reasoning must be checked. Running out of time does not prove that a problem is impossible.

### `sondes_experiences/` — the laboratory for networks and probes

This folder contains experiments on AdaptiveRBF, HC-RBF, CNG, CNC, and comparisons with MLPs. It includes code, protocols, measurements, and reports. Some experiments favour the new architectures for particular tasks; others favour MLPs. A more controlled study reports HC-RBF advantages in some boundary cases, but also extrapolation difficulties and higher computing costs. This is what serious research should do: report both successes and limitations.

### `theories/` — ideas written in mathematical language

This folder brings together fingerprint and observation theories, cores, CNG/CNC, adaptive RBF networks, relations in eGenBrain, language models, and compositional programming. These texts try to give precise definitions and rules to the ideas explored by the software and experiments.

## 4. What if these ideas also described parts of the real world?

This section is **speculation**: a path for thinking and imagining experiments. It is not a proven discovery in physics.

### Fingerprints and the double-slit experiment

In a two-slit experiment, one can study what happens when we try to find out which slit a particle passed through. We could ask whether fingerprint theory can represent the difference between an apparatus that does not distinguish the path and one that measures it. The idea would be to describe the information available in each situation.

But the DDD_Base text clearly says its comparison with the double-slit experiment is a structural analogy and does not produce a physical conclusion about the quantum experiment. Going further would require recovering the mathematical results of quantum mechanics and making precise predictions that could be tested.

### Schrödinger's cat and the Naszimger cat

Schrödinger's cat is a thought experiment that illustrates a difficulty related to measurement in quantum physics. DDD_Base presents an example called the “Naszimger cat.” This cat is an observational class in the model, not a real quantum state and not a demonstrated solution to Schrödinger's problem.

One can imagine that the theory might help distinguish what a system contains, what an apparatus measures, and what the observer knows. This is an interesting question, but it does not yet solve the measurement problem.

### Other fields and other theories: speculative directions

Fingerprints could be useful for understanding how several cameras observe the same object, how doctors distinguish diseases from incomplete signs, how a robot combines its sensors, or how a language model uses context.

For the other research families, we can imagine several research questions:

- **Cores, CNG, and CNC:** could we build machines or robots where learning, logical organization, and hardware execution cooperate more effectively? Their results, speed, and energy use would have to be compared with conventional systems.
- **AAM:** could an agent learn to ask better questions before deciding, like an investigator who checks clues instead of guessing? Its reliability would need to be tested in new situations.
- **FulleGenBrain and composition:** could complex programs be built from blocks whose rules and limits are known, like building a bridge from inspected parts? The programs and their assumptions would have to be checked.
- **NGeGenBrain and eLLM:** could language models be better understood by observing several representations and testing new ways to recompose them? Measurements on real models would be needed to show whether answers actually improve.
- **eGenBrain:** could relational memory help a system find the origin of information and recognize what it does not know? Its answers would need to be compared with trusted reference knowledge bases.
- **ORDER:** could step-by-step search and verified proofs help solve mathematical problems or check software? Every proof would have to be verified, and lack of time must not be confused with impossibility.

Cores could therefore inspire machines that distribute computations more effectively, while composition could help build programs that are easier to verify. These are research directions, not guaranteed results.

## 5. How can we recognize a scientific advance?

We should distinguish four things:

1. **An idea:** an interesting proposal.
2. **A theory:** definitions and rules that explain the idea precisely.
3. **An implementation:** a program that realizes part of the idea.
4. **An experiment:** a test that measures what happens under specific conditions.

A positive experiment does not prove that a method works everywhere. A negative experiment is not useless: it shows where a method needs improvement or where its use should be limited. An analogy with physics is not proof that a theory describes nature.

## 6. How to read and learn from this research

You can begin with the READMEs, then look at experimental reports, small demonstrations, and finally the theory texts. Try to understand one question at a time: what information is observed? Which probe measures it? How is the information stored? Which experiment checks the proposal?

The complete source for each work is published in its corresponding release. A presentation archive may contain a snapshot or explanatory material; it does not replace the complete releases.

The reference documentation and reports are written in French. If you translate them, the translation and its quality are your personal responsibility. The English README files are reading guides, not official translations of every report.

## 7. Author and license

The works are attributed to **Bensalem Nassim, with AI assistance**. The single general license is the `LICENSE` file at the root of the `main` branch. It permits only non-commercial research use of material whose rights are owned by the Author. Commercial use requires prior, express, written authorization signed by Bensalem Nassim.

Older license files inside some ZIP archives have been retained so as not to change the bytes and SHA-256 fingerprints of distributed files. They are not a second general license issued by the Author for his own material. This rule cannot remove valid third-party rights or licenses. Read `LICENSE` before any use.

## To conclude

The central lesson of this research is simple: artificial intelligence can be studied as a team of tools that observe, learn, organize, remember, calculate, and verify. The challenge is to understand how these tools can cooperate without inventing what they do not know. This is an open, demanding, and exciting question — and anyone can begin exploring it by learning mathematics, computer science, and the scientific method.
