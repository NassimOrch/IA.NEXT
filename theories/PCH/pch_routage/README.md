# PCH — Variational Context Routing
### Mathematical Foundations, Context Selection, and PCH-ESM Extensions

**English / Français**

---

# PART I — ENGLISH

## 1. Overview

This repository contains a collection of theoretical manuscripts devoted to **variational context routing within the PCH framework**.

The central objective is to formulate context selection as a mathematical optimization problem rather than relying exclusively on an independently learned routing network or an external classification gate.

The general principle is to associate each admissible context with a local optimization problem, evaluate the corresponding context-dependent quantity, and select the context according to a mathematically defined decision rule.

The manuscripts investigate two complementary routing principles:

1. **Reduced-value routing:** select the context whose normalized local optimization problem has the smallest reduced value.
2. **Normalized-evidence routing:** select the context that produces the largest normalized improvement in the local PCH energy.

These principles share the same general objective: separating the local purification mechanism from the decision that determines which context should be used.

The repository also develops the geometric, analytical, and computational properties of these routing mechanisms, including stability, entropy-based relaxation, short-rollout approximations, and the specialization of the framework to PCH-ESM.

> **Central idea:** Context selection can be derived from the mathematical structure of local optimization problems, rather than being necessarily delegated to an independent learned gate.

---

## 2. What Is This Project?

PCH provides a context-dependent purification mechanism.

For an input latent representation \(w\), each admissible context \(c\) defines a local optimization problem. Its solution produces a purified representation associated with that context.

The routing problem is to determine which context should be selected.

Let the set of admissible contexts be finite:

\[
\mathcal C=\{1,\ldots,K\}.
\]

For each context \(c\), consider an admissible convex set

\[
\mathcal M_c\subseteq\mathcal H,
\]

where \(\mathcal H\) is the latent Hilbert space.

A representative context-dependent energy is

\[
J_c(u;w)
=
\frac12\|u-w\|^2
+
\lambda_{\mathrm{ctx},c}
\operatorname{dist}(u,\mathcal M_c)^2
+
\lambda_{\mathrm{ridge},c}\|u\|^2.
\]

The associated PCH purification is obtained by solving

\[
u_c^\star(w)
=
\arg\min_{u\in\mathcal H}J_c(u;w).
\]

The routing layer then compares the admissible contexts and selects one according to the chosen variational criterion.

The distinction is fundamental:

- **Purification** determines the optimal representation for a given context.
- **Routing** determines which context should be used.
- **Final output** is the purified representation associated with the selected context.

The routing extensions developed here are designed to preserve the underlying PCH purification problem.

---

## 3. Main Research Objectives

The repository addresses the following questions.

### 3.1 Mathematical formulation of routing

Can context selection be expressed as an optimization problem over the product space

\[
\mathcal H\times\mathcal C?
\]

Can the decision be derived directly from the local PCH objectives?

### 3.2 Context-dependent value functions

How can local optimization problems be converted into comparable scalar quantities?

How do Moreau envelopes and proximal operators provide a natural mathematical representation of these quantities?

### 3.3 Stability and decision geometry

Under which conditions does a selected context remain unchanged when the input is perturbed?

Can the latent space be divided into regions associated with different contexts?

What happens at the boundaries between these regions?

### 3.4 Soft routing

Can the discrete context-selection problem be relaxed into a continuous optimization problem over the probability simplex?

Can the hard decision be recovered as a limiting case?

### 3.5 Computational approximation

Can exact context selection be approximated using a finite number of proximal iterations?

Can a margin certificate guarantee that the approximate routing decision agrees with the exact one?

### 3.6 PCH-ESM specialization

Can a spectral decomposition provide a structured family of admissible contexts?

Can the general routing theory be instantiated over specialized spectral blocks?

### 3.7 Normalized evidence

Can the routing decision instead be based on the amount of energy reduction achieved by each context?

Can this decision be made invariant to context-dependent additive changes in the energy?

---

## 4. Collection of Documents and Their Roles

The repository contains several manuscripts that should be understood as related research documents, not automatically as independent implementations or interchangeable mathematical models.

### Document 1 — Context Selection by Value Functions

**Suggested filename:**

`01_context_selection_by_value_functions.tex`

**Title:**

*Sélection de contexte par fonctions valeur — Routage variationnel pour PCH*

This manuscript establishes the mathematical foundation of finite-dimensional variational routing.

Its central object is the normalized reduced value associated with each context:

\[
\widetilde V_c(w)
=
\inf_{u\in\mathbb R^d}
\widetilde J_c(u;w).
\]

The selected context is

\[
c^\star(w)
\in
\arg\min_{c\in\mathcal C}
\widetilde V_c(w).
\]

The manuscript develops:

- The context-dependent PCH optimization problem.
- The canonical normalization by the strong-convexity parameter.
- The relationship between reduced values and Moreau envelopes.
- The exact routing formulation.
- The geometry of context-dominance regions.
- The regularity of the global routing value.
- The Clarke generalized gradient at decision boundaries.
- Entropic soft routing.
- Short-rollout approximations and routing stability.
- A one-dimensional analytical example.

**Role in the project:** foundational mathematical formulation of reduced-value routing.

### Document 2 — Variational Routing for PCH

**Suggested filename:**

`02_variational_routing_for_pch.tex`

**Title:**

*Routage variationnel pour PCH — Choix du contexte comme problème d'optimisation*

This manuscript presents a closely related formulation of the same finite-dimensional routing framework.

It emphasizes the interpretation of context selection as an optimization problem over

\[
\mathbb R^d\times\mathcal C.
\]

Its central principle remains

\[
c^\star(w)
\in
\arg\min_{c\in\mathcal C}
\widetilde V_c(w).
\]

It provides a complementary presentation of:

- Exact context selection.
- Local proximal optimization.
- Normalized value functions.
- Decision cells and switching boundaries.
- Entropic relaxation.
- Stability under a strict decision margin.
- Approximate routing through finite proximal iterations.

**Role in the project:** an alternative or revised presentation of the foundational reduced-value routing manuscript.

**Important:** Documents 1 and 2 are substantially overlapping. They should be treated as manuscript variants unless a final editorial comparison establishes a specific reason to maintain both as separate publications.

### Document 3 — PCH-ESM and the Variational Routing Paradigm

**Suggested filename:**

`03_pch_esm_variational_routing.tex`

**Title:**

*Routage variationnel PCH-ESM — Sélection de contexte par fonctions valeur et changement de paradigme*

This manuscript extends the foundational routing formulation.

It moves from the finite-dimensional presentation toward a Hilbert-space formulation and develops the interpretation of routing as a decision mechanism induced by a family of local value functions.

Its main topics include:

- The lower-envelope formulation of context selection.
- Variational decision geometry.
- Context-dominance regions and their boundaries.
- Stability under a positive routing margin.
- A certificate based on upper and lower bounds.
- Entropic soft routing.
- Computational complexity of exhaustive routing.
- Comparison with conventional Mixture-of-Experts routing.
- Spectral specialization through PCH-ESM.
- Orthogonal projection and reconstruction properties.
- Inverse-variance weighted consensus under explicit statistical assumptions.
- One-dimensional and multidimensional illustrative examples.

The key relation is

\[
F(w)
=
\min_{c\in\mathcal C}\widetilde V_c(w).
\]

The manuscript interprets the resulting lower envelope as the mathematical object that induces the routing decision.

**Role in the project:** generalization and structured specialization of the reduced-value routing framework, including its application to PCH-ESM.

### Document 4 — Normalized Evidence-Based Routing

**Suggested filename:**

`04_normalized_gain_routing_extension.tex`

**Title:**

*Extension théorique du routage contextuel dans le noyau PCH*

This manuscript introduces an additional routing criterion based on the normalized improvement achieved by each context.

For a context \(c\), define the energy reduction

\[
\Delta_{\alpha,c}(w)
=
\widehat J_{\alpha,c}(w;w)
-
\widehat J_{\alpha,c}
\left(
u^\star_{\alpha,c}(w);w
\right).
\]

The corresponding normalized evidence score is

\[
\mathcal R_{\alpha,c}(w)
=
\frac{
\Delta_{\alpha,c}(w)
}{
\widehat J_{\alpha,c}(w;w)+\varepsilon
},
\qquad \varepsilon>0.
\]

The selected context is

\[
c^\star_\alpha(w)
\in
\arg\max_{c\in\mathcal C}
\mathcal R_{\alpha,c}(w).
\]

This manuscript additionally develops:

- Invariance of the energy gain under context-dependent additive shifts.
- Normalized evidence-based context selection.
- Stability under a strict score margin.
- Gibbs probabilistic routing.
- Short-rollout evidence certificates.
- Finite-iteration routing guarantees under suitable assumptions.
- A geometric tie-breaker based on the limiting projector \(P_0\).
- A final lexicographic routing rule.

**Role in the project:** an alternative routing criterion based on normalized purification gain, rather than minimum reduced value.

**Important:** This is not merely another notation for the reduced-value rule. It defines a different decision criterion and should be studied as a separate routing extension.

---

## 5. The Two Main Routing Principles

A major objective of this repository is to distinguish the two mathematical approaches.

They are related, but they are not generally equivalent.

### 5.1 Reduced-value routing

For each context, define

\[
\widetilde V_c(w)
=
\inf_u\widetilde J_c(u;w).
\]

The hard routing decision is

\[
\boxed{
c^\star(w)
\in
\arg\min_{c\in\mathcal C}
\widetilde V_c(w)
}
\]

The context with the lowest normalized optimal value is selected.

This formulation is naturally connected to:

- Convex optimization.
- Moreau envelopes.
- Proximal operators.
- Lower envelopes of smooth functions.
- Decision cells and switching boundaries.
- Clarke nonsmooth analysis.

Its soft version is

\[
p_c^\star(w)
=
\frac{
\exp(-\beta\widetilde V_c(w))
}{
\sum_{j=1}^{K}
\exp(-\beta\widetilde V_j(w))
}.
\]

### 5.2 Normalized-evidence routing

For each context, calculate its normalized energy reduction:

\[
\mathcal R_{\alpha,c}(w)
=
\frac{
\widehat J_{\alpha,c}(w;w)
-
\widehat J_{\alpha,c}
\left(u^\star_{\alpha,c}(w);w\right)
}{
\widehat J_{\alpha,c}(w;w)+\varepsilon
}.
\]

Then select

\[
\boxed{
c^\star_\alpha(w)
\in
\arg\max_{c\in\mathcal C}
\mathcal R_{\alpha,c}(w)
}
\]

The context with the largest normalized improvement is selected.

Its probabilistic version is

\[
\pi_{\beta,\alpha}(c\mid w)
=
\frac{
\exp(\beta\mathcal R_{\alpha,c}(w))
}{
\sum_{j\in\mathcal C}
\exp(\beta\mathcal R_{\alpha,j}(w))
}.
\]

### 5.3 Conceptual difference

| Aspect | Reduced-value routing | Normalized-evidence routing |
|---|---|---|
| Decision quantity | Reduced local value | Normalized energy reduction |
| Selection rule | Minimum | Maximum |
| Main mathematical object | Moreau envelope | Relative purification gain |
| Soft routing | Softmin / Gibbs distribution | Softmax / Gibbs distribution |
| Main interpretation | Lowest normalized optimal cost | Largest normalized improvement |
| Main manuscript | Documents 1–3 | Document 4 |

The two criteria should not be combined or presented as equivalent without an additional mathematical result establishing their relationship.

The appropriate criterion depends on the intended interpretation of context selection and on the mathematical assumptions of the application.

---

## 6. Mathematical Foundations

The manuscripts draw on several established areas of mathematics.

### 6.1 Convex analysis

Each context is associated with a convex optimization problem.

Under the stated assumptions, the quadratic proximity term and ridge regularization provide strong convexity, ensuring uniqueness of the local minimizer.

### 6.2 Proximal operators

After normalization, the local minimizer can be represented as

\[
u_c^\star(w)
=
\operatorname{prox}_{\mu_c g_c}(w).
\]

This connects PCH context purification to proximal optimization.

### 6.3 Moreau envelopes

The normalized reduced value is

\[
\widetilde V_c(w)
=
e_{\mu_c g_c}(w).
\]

Under the standard assumptions on \(g_c\), this value function is continuously differentiable, with

\[
\nabla\widetilde V_c(w)
=
\frac{1}{\mu_c}
\left(w-u_c^\star(w)\right).
\]

### 6.4 Variational decision geometry

The routing value is the lower envelope

\[
F(w)
=
\min_{c\in\mathcal C}\widetilde V_c(w).
\]

The latent space is divided into context-dominance regions.

For a context \(c\), its strict region is

\[
\Omega_c^{\mathrm{str}}
=
\left\{
w:
\widetilde V_c(w)
<
\widetilde V_j(w)
\text{ for all }j\neq c
\right\}.
\]

Decision boundaries correspond to locations where multiple contexts attain the same minimum.

### 6.5 Stability through a margin

Suppose a context \(c^\star\) is uniquely optimal and satisfies

\[
\delta(w)
=
\min_{c\neq c^\star}
\left[
\widetilde V_c(w)
-
\widetilde V_{c^\star}(w)
\right]
>0.
\]

Then continuity of the value functions guarantees local stability of the selected context.

The normalized-evidence manuscript establishes an analogous stability principle for a strict score margin.

### 6.6 Entropic relaxation

A discrete routing decision can be relaxed over the probability simplex

\[
\Delta_K
=
\left\{
p\in\mathbb R^K:
p_c\geq 0,\;
\sum_{c=1}^{K}p_c=1
\right\}.
\]

The resulting Gibbs distributions provide continuous context weights and recover the hard decision in the appropriate large-\(\beta\) limit when the optimum is unique.

### 6.7 PCH-ESM specialization

PCH-ESM introduces structured context families through spectral or orthogonal decompositions.

The general routing principle can then be applied to a finite collection of specialized blocks.

This specialization is an application of the general routing theory, not a replacement for its underlying mathematical formulation.

---

## 7. How the Framework Works

At a conceptual level, the routing process follows the same sequence across the manuscripts.

### Step 1 — Define the input

Start with a latent input

\[
w\in\mathcal H.
\]

### Step 2 — Define admissible contexts

Construct a finite set

\[
\mathcal C=\{1,\ldots,K\}.
\]

Each context must have its own well-defined admissible set and local PCH objective.

### Step 3 — Evaluate the local purification problems

For each context, solve

\[
u_c^\star(w)
=
\arg\min_u J_c(u;w).
\]

### Step 4 — Compute the routing quantity

Depending on the chosen formulation, compute either

\[
\widetilde V_c(w)
\]

or

\[
\mathcal R_{\alpha,c}(w).
\]

### Step 5 — Select the context

For reduced-value routing:

\[
c^\star
=
\arg\min_c\widetilde V_c(w).
\]

For normalized-evidence routing:

\[
c^\star
=
\arg\max_c\mathcal R_{\alpha,c}(w).
\]

### Step 6 — Return the selected purified representation

The final representation is

\[
\widetilde u(w)
=
u_{c^\star}^\star(w).
\]

### Step 7 — Optionally use soft routing or a short certificate

A probabilistic routing distribution or a finite-iteration approximation can be used when appropriate.

The exact mathematical assumptions and approximation guarantees must be checked for the selected formulation.

---

## 8. Computational Considerations

The manuscripts distinguish exact routing from approximate routing.

### Exact routing

Exact reduced-value routing evaluates the local optimization problem for every admissible context:

\[
C_{\mathrm{exact}}(\varepsilon)
=
\sum_{c\in\mathcal C}T_c(\varepsilon).
\]

The normalized-evidence formulation also requires evaluating the local solutions and their associated energies.

This approach provides a direct mathematical decision rule, but its computational cost may increase with the number of contexts.

### Short-rollout routing

A finite number of proximal iterations can be used to estimate the local solution and routing quantity.

Under an appropriate contraction assumption,

\[
\|u_c^{(N)}(w)-u_c^\star(w)\|
\leq
\rho_c^N
\|u_c^{(0)}(w)-u_c^\star(w)\|,
\qquad 0<\rho_c<1.
\]

The convergence of the local approximations can be used to establish routing agreement when the optimal context is separated from the alternatives by a sufficiently large margin.

### Certificate-based routing

The PCH-ESM manuscript also studies the use of upper and lower bounds.

If

\[
L_c(w)
\leq
\widetilde V_c(w)
\leq
U_c(w),
\]

and a context \(c^\star\) satisfies

\[
U_{c^\star}(w)
<
\min_{c\neq c^\star}L_c(w),
\]

then \(c^\star\) is certified as the unique reduced-value minimizer.

The practical value of this approach depends on whether sufficiently informative bounds can be computed efficiently.

---

## 9. Relationship to Mixture of Experts

The manuscripts compare variational routing with conventional Mixture-of-Experts architectures.

A typical Mixture-of-Experts architecture uses a learned gate to assign weights or select experts.

The reduced-value routing principle instead selects a context through

\[
c^\star(w)
\in
\arg\min_c\widetilde V_c(w).
\]

The normalized-evidence formulation uses

\[
c^\star_\alpha(w)
\in
\arg\max_c\mathcal R_{\alpha,c}(w).
\]

The conceptual distinction is that the context-selection rule is derived from the local PCH optimization problems rather than necessarily being predicted by a separate learned classifier.

This does not imply that variational routing is universally superior to learned gating.

The approaches involve different trade-offs:

- Learned gates can be computationally efficient at inference after training.
- Exact variational routing can require evaluating multiple local problems.
- Variational routing provides an interpretable objective and can support margin-based certificates under suitable assumptions.
- A learned gate may still be useful as an approximation or an initial candidate selector.

The purpose of the comparison is to clarify the mathematical status of the decision rule, not to claim that one architecture dominates every alternative.

---

## 10. Repository Structure

A recommended organization is:

    PCH-Variational-Routing/
    |
    |-- README.md
    |-- LICENSE
    |-- CITATION.cff
    |
    |-- docs/
    |   |
    |   |-- 01_context_selection_by_value_functions.tex
    |   |-- 02_variational_routing_for_pch.tex
    |   |-- 03_pch_esm_variational_routing.tex
    |   |-- 04_normalized_gain_routing_extension.tex
    |   |
    |   |-- figures/
    |   |
    |   |-- supplementary/
    |
    |-- references/
    |   |
    |   |-- references.bib
    |
    |-- examples/
    |   |
    |   |-- analytical_examples.md
    |
    |-- implementation/
    |   |
    |   |-- README.md
    |
    |-- tests/
    |   |
    |   |-- README.md
    |
    |-- LICENSE

This is a suggested structure. Directories such as `implementation/`, `tests/`, and `references/` should only be populated when their corresponding materials actually exist.

The repository currently describes a theoretical document collection. The presence of a proposed directory structure does not imply that a software implementation, numerical benchmark, or automated test suite is already available.

---

## 11. Requirements and Compilation

The manuscripts are written in LaTeX.

A standard LaTeX distribution such as TeX Live or MiKTeX should provide the required packages.

The documents use packages including:

- `amsmath`
- `amssymb`
- `amsfonts`
- `amsthm`
- `mathtools`
- `booktabs`
- `geometry`
- `enumitem`
- `hyperref`
- `tikz`
- `microtype`
- `bm` where required

### Compile a manuscript

From the directory containing the chosen `.tex` file, run:

    latexmk -pdf -interaction=nonstopmode -halt-on-error 01_context_selection_by_value_functions.tex

Alternatively, using pdfLaTeX:

    pdflatex 01_context_selection_by_value_functions.tex
    pdflatex 01_context_selection_by_value_functions.tex

Run the compilation process from the appropriate directory and ensure that all required figures, bibliography files, and dependencies are available.

The manuscripts containing an embedded `thebibliography` environment do not require a separate BibTeX database for those references.

Each manuscript should be compiled independently unless a common LaTeX project has explicitly been created.

---

## 12. Current Scope and Limitations

This repository should be understood as a **theoretical research collection**.

It provides mathematical formulations, assumptions, propositions, theorems, and illustrative examples.

The documents do not, by themselves, establish:

- A complete production-ready software implementation.
- Empirical performance improvements over existing routing architectures.
- State-of-the-art language-model performance.
- A general convergence theorem beyond the stated assumptions.
- Computational scalability for arbitrarily large context families.
- Empirical validation of every proposed PCH-ESM specialization.
- Universal superiority over learned routing mechanisms.

The short-rollout guarantees depend on the contraction and regularity assumptions stated in the corresponding manuscripts.

The spectral and statistical results in the PCH-ESM manuscript also depend on their respective structural assumptions.

The theoretical guarantees should therefore be distinguished from numerical or experimental claims.

---

## 13. Mathematical Consistency and Verification Notes

Before treating the manuscripts as a final publication-ready mathematical reference, the following details should be checked carefully.

### 13.1 Soft-min inequality

For reduced-value routing, define

\[
F(w)
=
\min_c\widetilde V_c(w)
\]

and

\[
S_\beta(w)
=
-\frac1\beta
\log\left(
\sum_{c=1}^K
e^{-\beta\widetilde V_c(w)}
\right).
\]

The standard log-sum-exp bounds are

\[
\boxed{
F(w)-\frac{\log K}{\beta}
\leq
S_\beta(w)
\leq
F(w).
}
\]

The inequalities printed in the supplied reduced-value manuscripts should be corrected because their direction is reversed.

### 13.2 Normalized-evidence equality claim

The evidence manuscript defines

\[
\mathcal R_{\alpha,c}(w)
=
\frac{\Delta_{\alpha,c}(w)}
{\widehat J_{\alpha,c}(w;w)+\varepsilon},
\qquad \varepsilon>0.
\]

The bound

\[
0\leq\mathcal R_{\alpha,c}(w)<1
\]

holds for nonnegative local energies and a strictly positive denominator of the specified form.

However, the statement that the score equals \(1\) if and only if the input is already a minimizer is not compatible with the positive \(\varepsilon\) in the denominator.

That proposition should be revised before publication.

### 13.3 Exact ties versus quasi-ties

The final geometric tie-breaker is presented lexicographically.

A lexicographic rule resolves exact ties in the first component.

To resolve numerical quasi-ties, an explicit tolerance must also be defined, including its scale and its effect on the selection rule.

### 13.4 Separation of routing formulations

The reduced-value score and normalized-evidence score are different mathematical quantities.

Any claim that the two selection rules are equivalent requires an additional proof under clearly stated assumptions.

These verification notes are included to preserve mathematical clarity and should not be interpreted as invalidating the entire framework.

---

## 14. Research Roadmap

The manuscripts suggest several directions for further development.

### Theoretical development

- Establish sharper relations between reduced-value routing and normalized-evidence routing.
- Investigate conditions under which the two decision rules select the same context.
- Strengthen stability results under perturbations of the input and model parameters.
- Develop sharper error bounds for short-rollout approximations.
- Study the geometry of context boundaries in higher-dimensional latent spaces.
- Formalize the interaction between the limiting projector and the routing decision.

### Algorithmic development

- Implement exact reduced-value routing.
- Implement normalized-evidence routing.
- Compare exact evaluation with short-rollout certificates.
- Evaluate the practical cost of upper and lower bounds.
- Investigate candidate-selection methods that preserve a final mathematical certificate.

### Experimental development

- Construct reproducible benchmark problems.
- Compare routing decisions across synthetic context families.
- Measure context-selection stability under controlled perturbations.
- Evaluate computational cost as the number of contexts increases.
- Test PCH-ESM specialization on explicitly defined spectral decompositions.

These are research directions, not claims that the corresponding experiments or implementations have already been completed.

---

## 15. References

The manuscripts draw on classical works in convex analysis, variational analysis, proximal optimization, and nonsmooth analysis.

The main references include:

- Moreau, J.-J. (1965). *Proximité et dualité dans un espace hilbertien.*
- Rockafellar, R. T. (1970). *Convex Analysis.*
- Berge, C. (1963). *Topological Spaces.*
- Clarke, F. H. (1983). *Optimization and Nonsmooth Analysis.*
- Bauschke, H. H., and Combettes, P. L. (2017). *Convex Analysis and Monotone Operator Theory in Hilbert Spaces.*
- Rockafellar, R. T., and Wets, R. J.-B. (1998). *Variational Analysis.*

The complete bibliographic entries are provided in the corresponding manuscripts.

---

## 16. Citation and Reuse

When referring to this collection, cite the specific manuscript relevant to the mathematical result being discussed.

Do not cite the entire repository as evidence for a theorem that appears only in one particular manuscript.

A formal citation should be added once the authorship, publication information, and repository metadata have been finalized.

---

## 17. Final Perspective

The central contribution of this research collection is the study of context selection as a variational decision problem built around local PCH optimization problems.

The reduced-value manuscripts develop routing through the lower envelope of normalized context-dependent value functions.

The PCH-ESM manuscript extends this perspective to structured spectral contexts and develops its geometric and computational implications.

The normalized-evidence manuscript introduces a complementary criterion based on the relative energy reduction achieved by each context.

Together, these documents establish a research direction in which context selection is not necessarily an independent classification task, but can instead be derived from the optimization structure of the underlying purification mechanism.

The long-term objective is to develop a mathematically justified, interpretable, stable, and computationally practical family of routing mechanisms for PCH.

---

# PART II — VERSION FRANÇAISE

## 1. Présentation générale

Ce dépôt rassemble une collection de manuscrits théoriques consacrés au **routage contextuel variationnel dans le cadre PCH**.

L'objectif central est de formuler la sélection du contexte comme un véritable problème mathématique d'optimisation, plutôt que de la confier nécessairement à un réseau de routage appris séparément ou à un classifieur externe.

Le principe général consiste à associer à chaque contexte admissible un problème d'optimisation local, à évaluer la quantité mathématique correspondante, puis à sélectionner le contexte au moyen d'une règle de décision explicitement définie.

Les manuscrits étudient deux principes complémentaires :

1. **Routage par valeur réduite :** sélectionner le contexte dont le problème local normalisé possède la plus petite valeur réduite.
2. **Routage par évidence normalisée :** sélectionner le contexte qui produit la plus grande amélioration normalisée de l'énergie PCH locale.

Ces deux principes poursuivent un objectif commun : séparer le mécanisme local de purification de la décision déterminant le contexte à utiliser.

Les manuscrits développent également les propriétés géométriques, analytiques et calculatoires de ces mécanismes : stabilité, relaxation entropique, approximations par pré-roulage court et spécialisation du cadre à PCH-ESM.

> **Idée centrale :** le choix du contexte peut être déduit de la structure mathématique des problèmes d'optimisation locaux, sans devoir nécessairement être confié à un routeur appris indépendant.

---

## 2. Qu'est-ce que ce projet ?

PCH fournit un mécanisme de purification dépendant du contexte.

Pour une représentation latente d'entrée \(w\), chaque contexte admissible définit un problème d'optimisation local. Sa solution fournit une représentation purifiée associée à ce contexte.

Le problème de routage consiste à déterminer quel contexte doit être sélectionné.

On considère un ensemble fini de contextes admissibles :

\[
\mathcal C=\{1,\ldots,K\}.
\]

À chaque contexte \(c\), on associe un ensemble convexe admissible :

\[
\mathcal M_c\subseteq\mathcal H,
\]

où \(\mathcal H\) désigne l'espace latent de Hilbert.

Une énergie contextuelle représentative est donnée par

\[
J_c(u;w)
=
\frac12\|u-w\|^2
+
\lambda_{\mathrm{ctx},c}
\operatorname{dist}(u,\mathcal M_c)^2
+
\lambda_{\mathrm{ridge},c}\|u\|^2.
\]

La purification PCH associée au contexte est obtenue par

\[
u_c^\star(w)
=
\arg\min_{u\in\mathcal H}J_c(u;w).
\]

La couche de routage compare ensuite les contextes admissibles et en sélectionne un selon un critère variationnel défini.

La distinction est fondamentale :

- **Purification :** déterminer la représentation optimale pour un contexte donné.
- **Routage :** déterminer quel contexte doit être utilisé.
- **Sortie finale :** retourner la représentation purifiée associée au contexte sélectionné.

Les extensions de routage présentées ici sont conçues pour préserver le problème de purification PCH sous-jacent.

---

## 3. Objectifs principaux de la recherche

Le dépôt étudie les questions suivantes.

### 3.1 Formulation mathématique du routage

La sélection du contexte peut-elle être formulée comme un problème d'optimisation sur

\[
\mathcal H\times\mathcal C?
\]

La décision peut-elle être directement déduite des fonctionnelles locales de PCH ?

### 3.2 Fonctions valeur contextuelles

Comment transformer les problèmes d'optimisation locaux en quantités scalaires comparables ?

Comment les enveloppes de Moreau et les opérateurs proximaux permettent-ils de représenter naturellement ces quantités ?

### 3.3 Stabilité et géométrie de décision

Sous quelles conditions un contexte reste-t-il sélectionné lorsque l'entrée est perturbée ?

L'espace latent peut-il être partitionné en régions associées aux différents contextes ?

Que se passe-t-il aux frontières entre ces régions ?

### 3.4 Routage souple

Le problème discret de sélection peut-il être relaxé en un problème continu sur le simplexe des probabilités ?

La décision dure peut-elle être retrouvée comme cas limite ?

### 3.5 Approximation calculatoire

Peut-on approximer le routage exact avec un nombre fini d'itérations proximales ?

Un certificat de marge peut-il garantir que la décision approchée coïncide avec la décision exacte ?

### 3.6 Spécialisation PCH-ESM

Une décomposition spectrale peut-elle fournir une famille structurée de contextes admissibles ?

La théorie générale du routage peut-elle être instanciée sur des blocs spectraux spécialisés ?

### 3.7 Évidence normalisée

La décision peut-elle plutôt reposer sur la quantité d'énergie éliminée par chaque contexte ?

Cette décision peut-elle être rendue invariante aux changements additifs dépendant du contexte ?

---

## 4. Collection des documents et rôle de chaque manuscrit

Le dépôt contient plusieurs manuscrits qui doivent être compris comme des documents scientifiques liés, et non automatiquement comme des implémentations indépendantes ou des modèles mathématiques interchangeables.

### Document 1 — Sélection de contexte par fonctions valeur

**Nom de fichier proposé :**

`01_context_selection_by_value_functions.tex`

**Titre :**

*Sélection de contexte par fonctions valeur — Routage variationnel pour PCH*

Ce manuscrit établit les fondements mathématiques du routage variationnel en dimension finie.

Son objet central est la valeur réduite normalisée associée à chaque contexte :

\[
\widetilde V_c(w)
=
\inf_{u\in\mathbb R^d}
\widetilde J_c(u;w).
\]

Le contexte sélectionné est défini par

\[
c^\star(w)
\in
\arg\min_{c\in\mathcal C}
\widetilde V_c(w).
\]

Le manuscrit développe :

- Le problème d'optimisation PCH dépendant du contexte.
- La normalisation canonique par le paramètre de forte convexité.
- Le lien entre les valeurs réduites et les enveloppes de Moreau.
- La formulation exacte du routage.
- La géométrie des régions de dominance contextuelle.
- La régularité de la valeur globale de routage.
- Le gradient généralisé de Clarke aux frontières de décision.
- Le routage souple entropique.
- Les approximations par pré-roulage court et la stabilité du routage.
- Un exemple analytique en dimension un.

**Rôle dans le projet :** formulation mathématique fondamentale du routage par valeurs réduites.

### Document 2 — Routage variationnel pour PCH

**Nom de fichier proposé :**

`02_variational_routing_for_pch.tex`

**Titre :**

*Routage variationnel pour PCH — Choix du contexte comme problème d'optimisation*

Ce manuscrit présente une formulation très proche du même cadre de routage variationnel en dimension finie.

Il met particulièrement l'accent sur l'interprétation de la sélection contextuelle comme un problème d'optimisation sur

\[
\mathbb R^d\times\mathcal C.
\]

Son principe central reste

\[
c^\star(w)
\in
\arg\min_{c\in\mathcal C}
\widetilde V_c(w).
\]

Il fournit une présentation complémentaire des éléments suivants :

- Sélection exacte du contexte.
- Optimisation proximale locale.
- Fonctions valeur normalisées.
- Cellules de décision et frontières de transition.
- Relaxation entropique.
- Stabilité sous une marge stricte.
- Routage approché par itérations proximales finies.

**Rôle dans le projet :** présentation alternative ou révisée du manuscrit fondateur consacré au routage par valeurs réduites.

**Important :** les documents 1 et 2 présentent un chevauchement substantiel. Ils doivent être considérés comme des variantes de manuscrit, sauf si une comparaison éditoriale finale établit une raison spécifique de les conserver comme publications distinctes.

### Document 3 — PCH-ESM et routage variationnel

**Nom de fichier proposé :**

`03_pch_esm_variational_routing.tex`

**Titre :**

*Routage variationnel PCH-ESM — Sélection de contexte par fonctions valeur et changement de paradigme*

Ce manuscrit étend la formulation fondamentale du routage.

Il passe de la présentation en dimension finie vers une formulation sur espace de Hilbert et développe l'interprétation du routage comme mécanisme de décision induit par une famille de fonctions valeur locales.

Ses principaux sujets sont :

- La formulation par enveloppe inférieure des fonctions valeur.
- La géométrie de décision variationnelle.
- Les régions de dominance contextuelle et leurs frontières.
- La stabilité sous une marge positive.
- Un certificat fondé sur des bornes inférieures et supérieures.
- Le routage souple entropique.
- La complexité calculatoire du routage exhaustif.
- La comparaison avec les architectures classiques de type Mixture of Experts.
- La spécialisation spectrale par PCH-ESM.
- Les propriétés de projection orthogonale et de reconstruction.
- Le consensus pondéré par variance inverse sous des hypothèses statistiques explicites.
- Des exemples illustratifs en dimension un et en dimension deux.

La relation centrale est

\[
F(w)
=
\min_{c\in\mathcal C}\widetilde V_c(w).
\]

Le manuscrit interprète l'enveloppe inférieure ainsi obtenue comme l'objet mathématique qui induit la décision de routage.

**Rôle dans le projet :** généralisation et spécialisation structurée du routage par valeurs réduites, avec une application à PCH-ESM.

### Document 4 — Extension du routage par évidence normalisée

**Nom de fichier proposé :**

`04_normalized_gain_routing_extension.tex`

**Titre :**

*Extension théorique du routage contextuel dans le noyau PCH*

Ce manuscrit introduit un critère supplémentaire de routage fondé sur l'amélioration normalisée produite par chaque contexte.

Pour un contexte \(c\), on définit la réduction d'énergie

\[
\Delta_{\alpha,c}(w)
=
\widehat J_{\alpha,c}(w;w)
-
\widehat J_{\alpha,c}
\left(
u^\star_{\alpha,c}(w);w
\right).
\]

Le score d'évidence normalisée correspondant est

\[
\mathcal R_{\alpha,c}(w)
=
\frac{
\Delta_{\alpha,c}(w)
}{
\widehat J_{\alpha,c}(w;w)+\varepsilon
},
\qquad \varepsilon>0.
\]

Le contexte sélectionné est

\[
c^\star_\alpha(w)
\in
\arg\max_{c\in\mathcal C}
\mathcal R_{\alpha,c}(w).
\]

Ce manuscrit développe également :

- L'invariance du gain énergétique aux décalages additifs dépendant du contexte.
- La sélection du contexte par évidence normalisée.
- La stabilité sous une marge stricte du score.
- Le routage probabiliste de Gibbs.
- Les certificats d'évidence par pré-roulage court.
- Les garanties de routage en nombre fini d'itérations sous des hypothèses appropriées.
- Un départage géométrique fondé sur le projecteur limite \(P_0\).
- Une règle finale de routage lexicographique.

**Rôle dans le projet :** critère de routage alternatif fondé sur le gain de purification normalisé, plutôt que sur la minimisation de la valeur réduite.

**Important :** il ne s'agit pas simplement d'une autre notation de la règle par valeur réduite. Ce manuscrit définit un critère de décision différent, qui doit être étudié comme une extension distincte.

---

## 5. Les deux principaux principes de routage

L'un des objectifs importants du dépôt est de distinguer clairement les deux approches mathématiques.

Elles sont liées, mais ne sont pas généralement équivalentes.

### 5.1 Routage par valeur réduite

Pour chaque contexte, on définit

\[
\widetilde V_c(w)
=
\inf_u\widetilde J_c(u;w).
\]

La règle de routage dur est

\[
\boxed{
c^\star(w)
\in
\arg\min_{c\in\mathcal C}
\widetilde V_c(w)
}
\]

Le contexte dont la valeur optimale normalisée est la plus faible est sélectionné.

Cette formulation est naturellement liée à :

- L'optimisation convexe.
- Les enveloppes de Moreau.
- Les opérateurs proximaux.
- Les enveloppes inférieures de fonctions régulières.
- Les cellules de décision et les frontières de transition.
- L'analyse non lisse de Clarke.

Sa version souple est

\[
p_c^\star(w)
=
\frac{
\exp(-\beta\widetilde V_c(w))
}{
\sum_{j=1}^{K}
\exp(-\beta\widetilde V_j(w))
}.
\]

### 5.2 Routage par évidence normalisée

Pour chaque contexte, on calcule sa réduction d'énergie normalisée :

\[
\mathcal R_{\alpha,c}(w)
=
\frac{
\widehat J_{\alpha,c}(w;w)
-
\widehat J_{\alpha,c}
\left(u^\star_{\alpha,c}(w);w\right)
}{
\widehat J_{\alpha,c}(w;w)+\varepsilon
}.
\]

On sélectionne ensuite

\[
\boxed{
c^\star_\alpha(w)
\in
\arg\max_{c\in\mathcal C}
\mathcal R_{\alpha,c}(w)
}
\]

Le contexte qui produit la plus grande amélioration normalisée est sélectionné.

Sa version probabiliste est

\[
\pi_{\beta,\alpha}(c\mid w)
=
\frac{
\exp(\beta\mathcal R_{\alpha,c}(w))
}{
\sum_{j\in\mathcal C}
\exp(\beta\mathcal R_{\alpha,j}(w))
}.
\]

### 5.3 Différence conceptuelle

| Aspect | Routage par valeur réduite | Routage par évidence normalisée |
|---|---|---|
| Quantité de décision | Valeur réduite locale | Réduction d'énergie normalisée |
| Règle de sélection | Minimum | Maximum |
| Objet mathématique central | Enveloppe de Moreau | Gain de purification relatif |
| Routage souple | Softmin / loi de Gibbs | Softmax / loi de Gibbs |
| Interprétation principale | Coût optimal normalisé minimal | Amélioration normalisée maximale |
| Manuscrits principaux | Documents 1–3 | Document 4 |

Les deux critères ne doivent pas être fusionnés ni présentés comme équivalents sans résultat mathématique supplémentaire établissant leur relation.

Le critère approprié dépend de l'interprétation recherchée pour la sélection du contexte et des hypothèses mathématiques de l'application.

---

## 6. Fondements mathématiques

Les manuscrits mobilisent plusieurs domaines classiques des mathématiques.

### 6.1 Analyse convexe

Chaque contexte est associé à un problème d'optimisation convexe.

Sous les hypothèses retenues, le terme quadratique de proximité et la régularisation ridge assurent la forte convexité et donc l'unicité du minimiseur local.

### 6.2 Opérateurs proximaux

Après normalisation, le minimiseur local peut être représenté par

\[
u_c^\star(w)
=
\operatorname{prox}_{\mu_c g_c}(w).
\]

Cela relie la purification contextuelle PCH à l'optimisation proximale.

### 6.3 Enveloppes de Moreau

La valeur réduite normalisée est

\[
\widetilde V_c(w)
=
e_{\mu_c g_c}(w).
\]

Sous les hypothèses classiques sur \(g_c\), cette fonction valeur est continûment différentiable et vérifie

\[
\nabla\widetilde V_c(w)
=
\frac{1}{\mu_c}
\left(w-u_c^\star(w)\right).
\]

### 6.4 Géométrie de décision variationnelle

La valeur de routage est l'enveloppe inférieure

\[
F(w)
=
\min_{c\in\mathcal C}\widetilde V_c(w).
\]

L'espace latent est divisé en régions de dominance contextuelle.

Pour un contexte \(c\), sa région stricte est

\[
\Omega_c^{\mathrm{str}}
=
\left\{
w:
\widetilde V_c(w)
<
\widetilde V_j(w)
\text{ pour tout }j\neq c
\right\}.
\]

Les frontières de décision correspondent aux points où plusieurs contextes atteignent simultanément le minimum.

### 6.5 Stabilité par marge

Supposons qu'un contexte \(c^\star\) soit optimal de manière unique et vérifie

\[
\delta(w)
=
\min_{c\neq c^\star}
\left[
\widetilde V_c(w)
-
\widetilde V_{c^\star}(w)
\right]
>0.
\]

La continuité des fonctions valeur garantit alors la stabilité locale du contexte sélectionné.

Le manuscrit sur l'évidence normalisée établit un principe analogue de stabilité pour une marge stricte entre les scores.

### 6.6 Relaxation entropique

Une décision discrète de routage peut être relaxée sur le simplexe des probabilités

\[
\Delta_K
=
\left\{
p\in\mathbb R^K:
p_c\geq 0,\;
\sum_{c=1}^{K}p_c=1
\right\}.
\]

Les distributions de Gibbs obtenues fournissent des poids contextuels continus et retrouvent la décision dure dans la limite appropriée lorsque l'optimum est unique.

### 6.7 Spécialisation PCH-ESM

PCH-ESM introduit des familles structurées de contextes au moyen de décompositions spectrales ou orthogonales.

Le principe général de routage peut alors être appliqué à une collection finie de blocs spécialisés.

Cette spécialisation constitue une application de la théorie générale du routage, et non un remplacement de sa formulation mathématique sous-jacente.

---

## 7. Fonctionnement général du cadre

À un niveau conceptuel, le processus de routage suit la même séquence dans les différents manuscrits.

### Étape 1 — Définir l'entrée

On commence avec une entrée latente

\[
w\in\mathcal H.
\]

### Étape 2 — Définir les contextes admissibles

On construit un ensemble fini

\[
\mathcal C=\{1,\ldots,K\}.
\]

Chaque contexte doit disposer de son propre ensemble admissible et de sa propre fonctionnelle locale PCH bien définie.

### Étape 3 — Évaluer les problèmes de purification locaux

Pour chaque contexte, on résout

\[
u_c^\star(w)
=
\arg\min_u J_c(u;w).
\]

### Étape 4 — Calculer la quantité de routage

Selon la formulation retenue, on calcule soit

\[
\widetilde V_c(w),
\]

soit

\[
\mathcal R_{\alpha,c}(w).
\]

### Étape 5 — Sélectionner le contexte

Pour le routage par valeur réduite :

\[
c^\star
=
\arg\min_c\widetilde V_c(w).
\]

Pour le routage par évidence normalisée :

\[
c^\star
=
\arg\max_c\mathcal R_{\alpha,c}(w).
\]

### Étape 6 — Retourner la représentation purifiée sélectionnée

La représentation finale est

\[
\widetilde u(w)
=
u_{c^\star}^\star(w).
\]

### Étape 7 — Utiliser éventuellement le routage souple ou un certificat court

Une distribution de routage probabiliste ou une approximation par un nombre fini d'itérations peut être utilisée lorsque cela est approprié.

Les hypothèses mathématiques exactes et les garanties d'approximation doivent être vérifiées pour la formulation choisie.

---

## 8. Considérations calculatoires

Les manuscrits distinguent le routage exact du routage approché.

### Routage exact

Le routage exact par valeur réduite nécessite l'évaluation du problème d'optimisation local pour chaque contexte admissible :

\[
C_{\mathrm{exact}}(\varepsilon)
=
\sum_{c\in\mathcal C}T_c(\varepsilon).
\]

La formulation par évidence normalisée nécessite également le calcul des solutions locales et des énergies correspondantes.

Cette approche fournit une règle de décision mathématique directe, mais son coût calculatoire peut augmenter avec le nombre de contextes.

### Routage par pré-roulage court

Un nombre fini d'itérations proximales peut être utilisé pour estimer la solution locale et la quantité de routage.

Sous une hypothèse appropriée de contraction,

\[
\|u_c^{(N)}(w)-u_c^\star(w)\|
\leq
\rho_c^N
\|u_c^{(0)}(w)-u_c^\star(w)\|,
\qquad 0<\rho_c<1.
\]

La convergence des approximations locales peut être utilisée pour établir l'accord entre le routage approché et le routage exact lorsque le contexte optimal est séparé des autres par une marge suffisamment importante.

### Routage par certificat

Le manuscrit PCH-ESM étudie également l'utilisation de bornes supérieures et inférieures.

Si

\[
L_c(w)
\leq
\widetilde V_c(w)
\leq
U_c(w),
\]

et qu'un contexte \(c^\star\) vérifie

\[
U_{c^\star}(w)
<
\min_{c\neq c^\star}L_c(w),
\]

alors \(c^\star\) est certifié comme unique minimiseur de la valeur réduite.

L'intérêt pratique de cette approche dépend de la possibilité de calculer efficacement des bornes suffisamment informatives.

---

## 9. Relation avec les Mixture of Experts

Les manuscrits comparent le routage variationnel aux architectures classiques de type Mixture of Experts.

Une architecture Mixture of Experts utilise typiquement un mécanisme de routage appris afin d'attribuer des poids aux experts ou de sélectionner un expert.

Le principe du routage par valeurs réduites sélectionne plutôt un contexte selon

\[
c^\star(w)
\in
\arg\min_c\widetilde V_c(w).
\]

La formulation par évidence normalisée utilise

\[
c^\star_\alpha(w)
\in
\arg\max_c\mathcal R_{\alpha,c}(w).
\]

La différence conceptuelle est que la règle de sélection est déduite des problèmes d'optimisation locaux de PCH, plutôt que d'être nécessairement prédite par un classifieur appris séparément.

Cela n'implique pas que le routage variationnel soit universellement supérieur au routage appris.

Les approches présentent des compromis différents :

- Les routeurs appris peuvent être efficaces en inférence après leur phase d'entraînement.
- Le routage variationnel exact peut nécessiter l'évaluation de plusieurs problèmes locaux.
- Le routage variationnel fournit un objectif interprétable et peut permettre des certificats fondés sur une marge sous des hypothèses appropriées.
- Un routeur appris peut rester utile comme approximation ou comme mécanisme de présélection de candidats.

L'objectif de la comparaison est de clarifier le statut mathématique de la décision, et non d'affirmer qu'une architecture domine toutes les autres.

---

## 10. Organisation du dépôt

Une organisation recommandée est la suivante :

    PCH-Variational-Routing/
    |
    |-- README.md
    |-- LICENSE
    |-- CITATION.cff
    |
    |-- docs/
    |   |
    |   |-- 01_context_selection_by_value_functions.tex
    |   |-- 02_variational_routing_for_pch.tex
    |   |-- 03_pch_esm_variational_routing.tex
    |   |-- 04_normalized_gain_routing_extension.tex
    |   |
    |   |-- figures/
    |   |
    |   |-- supplementary/
    |
    |-- references/
    |   |
    |   |-- references.bib
    |
    |-- examples/
    |   |
    |   |-- analytical_examples.md
    |
    |-- implementation/
    |   |
    |   |-- README.md
    |
    |-- tests/
    |   |
    |   |-- README.md
    |
    |-- LICENSE

Il s'agit d'une organisation proposée. Les répertoires tels que `implementation/`, `tests/` et `references/` ne doivent être remplis que lorsque les éléments correspondants existent réellement.

Le dépôt décrit actuellement une collection de documents théoriques. La présence d'une arborescence proposée ne signifie pas qu'une implémentation logicielle, un benchmark numérique ou une suite de tests automatisés sont déjà disponibles.

---

## 11. Prérequis et compilation

Les manuscrits sont écrits en LaTeX.

Une distribution LaTeX standard, telle que TeX Live ou MiKTeX, doit fournir les packages nécessaires.

Les documents utilisent notamment :

- `amsmath`
- `amssymb`
- `amsfonts`
- `amsthm`
- `mathtools`
- `booktabs`
- `geometry`
- `enumitem`
- `hyperref`
- `tikz`
- `microtype`
- `bm` lorsque nécessaire

### Compiler un manuscrit

Depuis le répertoire contenant le fichier `.tex` choisi, exécuter :

    latexmk -pdf -interaction=nonstopmode -halt-on-error 01_context_selection_by_value_functions.tex

Une compilation avec pdfLaTeX est également possible :

    pdflatex 01_context_selection_by_value_functions.tex
    pdflatex 01_context_selection_by_value_functions.tex

La compilation doit être exécutée depuis le répertoire approprié, en veillant à ce que toutes les figures, bibliographies et dépendances nécessaires soient disponibles.

Les manuscrits qui contiennent directement un environnement `thebibliography` n'ont pas besoin d'une base BibTeX séparée pour ces références.

Chaque manuscrit doit être compilé indépendamment, sauf si un projet LaTeX commun a explicitement été créé.

---

## 12. Portée actuelle et limites

Ce dépôt doit être considéré comme une **collection de travaux de recherche théoriques**.

Il fournit des formulations mathématiques, des hypothèses, des propositions, des théorèmes et des exemples illustratifs.

Les documents ne démontrent pas, à eux seuls :

- L'existence d'une implémentation logicielle complète et prête pour la production.
- Des améliorations empiriques de performance par rapport aux architectures de routage existantes.
- Des performances de modèles de langage à l'état de l'art.
- Un théorème général de convergence au-delà des hypothèses explicitement indiquées.
- Une scalabilité calculatoire pour un nombre arbitrairement grand de contextes.
- Une validation empirique de chaque spécialisation proposée dans PCH-ESM.
- Une supériorité universelle sur les mécanismes de routage appris.

Les garanties du pré-roulage court dépendent des hypothèses de contraction et de régularité énoncées dans les manuscrits correspondants.

Les résultats spectraux et statistiques du manuscrit PCH-ESM dépendent également de leurs hypothèses structurelles respectives.

Les garanties théoriques doivent donc être distinguées des affirmations numériques ou expérimentales.

---

## 13. Cohérence mathématique et points de vérification

Avant de considérer les manuscrits comme une référence mathématique définitive prête à être publiée, certains points doivent être vérifiés avec attention.

### 13.1 Inégalité du soft-min

Pour le routage par valeurs réduites, on définit

\[
F(w)
=
\min_c\widetilde V_c(w)
\]

et

\[
S_\beta(w)
=
-\frac1\beta
\log\left(
\sum_{c=1}^K
e^{-\beta\widetilde V_c(w)}
\right).
\]

Les bornes classiques du log-sum-exp sont

\[
\boxed{
F(w)-\frac{\log K}{\beta}
\leq
S_\beta(w)
\leq
F(w).
}
\]

Les inégalités imprimées dans les manuscrits consacrés aux valeurs réduites doivent être corrigées, car leur sens est inversé.

### 13.2 Affirmation sur l'égalité du score d'évidence normalisée

Le manuscrit sur l'évidence définit

\[
\mathcal R_{\alpha,c}(w)
=
\frac{\Delta_{\alpha,c}(w)}
{\widehat J_{\alpha,c}(w;w)+\varepsilon},
\qquad \varepsilon>0.
\]

La borne

\[
0\leq\mathcal R_{\alpha,c}(w)<1
\]

est valable pour des énergies locales non négatives et un dénominateur strictement positif de la forme indiquée.

En revanche, l'affirmation selon laquelle le score est égal à \(1\) si et seulement si l'entrée est déjà minimisante n'est pas compatible avec la présence du terme positif \(\varepsilon\) au dénominateur.

Cette proposition doit être révisée avant publication.

### 13.3 Égalités exactes et quasi-égalités

Le départage géométrique final est présenté sous forme lexicographique.

Une règle lexicographique départage les égalités exactes dans la première composante.

Pour traiter des quasi-égalités numériques, il faut également définir une tolérance explicite, son échelle et son effet sur la règle de sélection.

### 13.4 Séparation des formulations de routage

Le score par valeur réduite et le score par évidence normalisée sont des quantités mathématiques différentes.

Toute affirmation d'équivalence entre leurs règles de sélection exige une démonstration supplémentaire et des hypothèses clairement énoncées.

Ces points de vérification sont indiqués dans un souci de rigueur mathématique et ne doivent pas être interprétés comme une invalidation de l'ensemble du cadre.

---

## 14. Perspectives de recherche

Les manuscrits suggèrent plusieurs directions de développement.

### Développement théorique

- Établir des relations plus précises entre le routage par valeur réduite et le routage par évidence normalisée.
- Étudier les conditions sous lesquelles les deux règles sélectionnent le même contexte.
- Renforcer les résultats de stabilité sous perturbations de l'entrée et des paramètres du modèle.
- Développer des bornes d'erreur plus précises pour les approximations par pré-roulage court.
- Étudier la géométrie des frontières de contexte dans des espaces latents de grande dimension.
- Formaliser l'interaction entre le projecteur limite et la décision de routage.

### Développement algorithmique

- Implémenter le routage exact par valeur réduite.
- Implémenter le routage par évidence normalisée.
- Comparer l'évaluation exacte aux certificats par pré-roulage court.
- Évaluer le coût pratique des bornes supérieures et inférieures.
- Étudier des méthodes de présélection de candidats conservant un certificat mathématique final.

### Développement expérimental

- Construire des problèmes de référence reproductibles.
- Comparer les décisions de routage sur des familles de contextes synthétiques.
- Mesurer la stabilité de la sélection sous des perturbations contrôlées.
- Évaluer le coût calculatoire lorsque le nombre de contextes augmente.
- Tester la spécialisation PCH-ESM sur des décompositions spectrales explicitement définies.

Il s'agit de directions de recherche, et non d'affirmations selon lesquelles les expériences ou implémentations correspondantes ont déjà été réalisées.

---

## 15. Références

Les manuscrits s'appuient sur des travaux classiques en analyse convexe, analyse variationnelle, optimisation proximale et analyse non lisse.

Les principales références sont :

- Moreau, J.-J. (1965). *Proximité et dualité dans un espace hilbertien.*
- Rockafellar, R. T. (1970). *Convex Analysis.*
- Berge, C. (1963). *Topological Spaces.*
- Clarke, F. H. (1983). *Optimization and Nonsmooth Analysis.*
- Bauschke, H. H., et Combettes, P. L. (2017). *Convex Analysis and Monotone Operator Theory in Hilbert Spaces.*
- Rockafellar, R. T., et Wets, R. J.-B. (1998). *Variational Analysis.*

Les références bibliographiques complètes sont indiquées dans les manuscrits correspondants.

---

## 16. Citation et réutilisation

Lorsqu'un résultat est repris de cette collection, il convient de citer le manuscrit précis dans lequel il est établi.

Il ne faut pas citer l'ensemble du dépôt comme preuve d'un théorème qui n'apparaît que dans un manuscrit particulier.

Une citation formelle pourra être ajoutée une fois les informations relatives aux auteurs, à la publication et aux métadonnées du dépôt finalisées.

---

## 17. Perspective finale

La contribution centrale de cette collection de recherche est l'étude de la sélection contextuelle comme problème de décision variationnel construit à partir des problèmes d'optimisation locaux de PCH.

Les manuscrits consacrés aux valeurs réduites développent le routage à travers l'enveloppe inférieure d'une famille de fonctions valeur contextuelles normalisées.

Le manuscrit PCH-ESM étend cette perspective à des contextes spectraux structurés et en développe les implications géométriques et calculatoires.

Le manuscrit consacré à l'évidence normalisée introduit un critère complémentaire fondé sur la réduction énergétique relative obtenue par chaque contexte.

Ensemble, ces documents définissent une direction de recherche dans laquelle la sélection contextuelle n'est pas nécessairement une tâche de classification indépendante, mais peut être déduite de la structure d'optimisation du mécanisme de purification sous-jacent.

L'objectif à long terme est de développer une famille de mécanismes de routage pour PCH qui soient mathématiquement justifiés, interprétables, stables et calculatoirement praticables.

---

**End of README / Fin du README**
