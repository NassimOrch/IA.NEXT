
# Pure PCH — Normalized Geometry, Exact Proximal Operators and Experimental Validation

<p align="center">
  <strong>A research project on normalized proximal geometry, contextual convex optimization, and context-dependent classification.</strong>
</p>

<p align="center">
  <em>English documentation below · Documentation française ci-dessous</em>
</p>

---

# 🇬🇧 ENGLISH

## 1. Overview

**Pure PCH** is a research framework investigating a normalized proximal optimization mechanism built around contextual geometry, convex constraints, and exact or numerically high-precision optimization.

The project studies how a data representation can be transformed through context-dependent convex geometry and proximal operators, and how this transformation affects local mathematical stability and downstream classification performance.

The central experimental question is:

> Can a normalized proximal mechanism remain mathematically stable across different latent dimensions, regularization regimes, calibration sizes, and classification tasks, while preserving useful classification structure?

The project separates two questions that must not be confused:

1. **Mathematical stability:** Does the normalized operator satisfy the expected scalar and operator-level relations?
2. **Practical usefulness:** Does the resulting representation improve classification when the context must be selected automatically?

The experiments show that these two properties are related but not equivalent.

## 2. Main research objectives

The project investigates:

- The normalized behavior of contextual proximal operators.
- The relationship between scalar contraction and operator-level consistency.
- The role of convex context geometry in representation refinement.
- The influence of latent dimension on the effective geometric structure.
- The effect of calibration size on contextual optimization.
- The difference between oracle context selection and automatic context routing.
- The impact of regularization and the parameter \(\gamma\).
- The relationship between numerical stability and downstream classification accuracy.

The broader objective is to identify which properties are intrinsic to the normalized PCH mechanism and which depend on the quality of context selection.

## 3. Mathematical framework

### 3.1 Normalized Case 3

The experimental framework uses the normalized Case 3 parameterization:

\[
\mu = 1 + 2\lambda_{\mathrm{ridge}}
\]

\[
\gamma =
\frac{\lambda_{\mathrm{ctx}}}{\mu}
\]

\[
\tau = \eta\mu
\]

The target scalar contraction coefficient is:

\[
\rho_\star = \frac{1}{1+\tau}
\]

For the principal experimental setting:

\[
\tau = 3.4
\]

and therefore:

\[
\rho_\star =
\frac{1}{4.4}
\approx 0.2272727273
\]

The normalized formulation makes it possible to compare experiments across different parameter configurations.

### 3.2 Contextual convex geometry

The framework constructs context sets from calibration embeddings.

For a given context \(c\), the context set is represented by a convex hull:

\[
M_c = \operatorname{conv}(Z_c)
\]

where \(Z_c\) denotes the calibration embeddings associated with that context.

The convex geometry defines the admissible region in which contextual projections and proximal optimization are performed.

### 3.3 Exact optimization

The experimental pipeline uses convex quadratic optimization for:

- Projection onto contextual convex sets.
- Computation of the PCH minimizer.
- Evaluation of the proximal map.

The reported implementation uses:

- `cvxpy`
- `OSQP`
- Absolute tolerance: \(10^{-10}\)
- Relative tolerance: \(10^{-10}\)
- Maximum solver iterations: `500000`

These settings describe the reported experimental implementation. They should not be interpreted as a universal guarantee of exact arithmetic: numerical solvers operate with finite precision and solver tolerances.

### 3.4 Local diagnostics

The framework evaluates local mathematical consistency through quantities such as:

- Scalar contraction gap.
- Operator gap.
- Projection gap.
- Fixed-point residual.
- Local Jacobian estimates.
- Energy monotonicity violations.
- Effective projection trace.

Local Jacobians are estimated using finite differences.

These diagnostics are intended to assess the numerical and local mathematical behavior of the mechanism, rather than to measure classification quality directly.

## 4. Experimental pipeline

The reported experiments follow this general procedure:

1. Load the selected text classification dataset.
2. Generate embeddings using a frozen SentenceTransformer encoder.
3. Fit PCA using calibration data only.
4. Project embeddings into the selected latent dimension.
5. Construct contextual convex hulls from calibration embeddings.
6. Compute contextual convex projections.
7. Solve the corresponding PCH optimization problems.
8. Evaluate the proximal transformation.
9. Compute local numerical and geometric diagnostics.
10. Evaluate classification under different context-selection conditions.
11. Aggregate results across experimental configurations.

### Important methodological distinction

PCA is fitted on calibration data only in the reported pipeline. This is an important experimental constraint intended to prevent test data from influencing the dimensionality-reduction fit.

The exact data split, preprocessing configuration, random seeds, and evaluation protocol should be documented alongside any reproduction of these results.

## 5. Classification evaluation

The experiments distinguish four accuracy measurements.

| Metric | Meaning |
|---|---|
| Raw accuracy | Classification performance before the PCH transformation |
| Oracle accuracy | Performance when the appropriate context is supplied |
| Routed accuracy | Performance when the system selects the context automatically |
| Context accuracy | Accuracy of the contextual prediction or context-related evaluation reported by the experimental pipeline |

The oracle and routed metrics answer different questions.

**Oracle accuracy** evaluates the potential of the PCH mechanism when the appropriate context is available.

**Routed accuracy** evaluates the complete operational pipeline, including automatic context selection.

Consequently, a large oracle gain does not guarantee a large routed gain.

This distinction is one of the most important findings of the experimental study.

## 6. Experimental results

### 6.1 First experimental series: ex1–ex13

The first report contains:

- 13 experimental blocks.
- 54 individual runs.
- The `20news4` and `20news20` datasets.
- Latent dimensions including 8, 16, 32, 48 and 64.
- Multiple regularization configurations.
- Several values of \(\gamma\).
- A fixed target value of \(\tau=3.4\).

The scripted support criterion is:

\[
\max \rho_{\mathrm{gap}} \leq 10^{-4}
\]

and

\[
\max \operatorname{operator\_gap}
\leq 10^{-4}
\]

Both conditions must be satisfied.

**Reported result:**

| Outcome | Experimental blocks |
|---|---|
| Supported | ex6, ex7, ex8, ex9, ex11, ex12, ex13 |
| Not supported | ex1, ex2, ex3, ex4, ex5, ex10 |

Thus, 7 of the 13 experimental blocks satisfy the specified numerical criterion.

A failed verdict does not necessarily mean that the scalar relation is inaccurate. Some blocks fail because the operator gap exceeds the prescribed threshold.

### 6.2 First-series observations

Several important observations emerge:

- The scalar normalized behavior remains close to its theoretical target across the reported experiments.
- The operator-level criterion is more restrictive than the scalar criterion.
- Lower-dimensional configurations can satisfy the numerical support criterion even when higher-dimensional configurations do not.
- Strong oracle accuracy can coexist with substantially weaker routed accuracy.
- Increasing \(\gamma\) does not automatically improve classification.
- A supported numerical verdict does not imply that the automatic context router is effective.

The `20news20` experiment in dimension 16 is particularly illustrative:

- Raw accuracy: 0.55625.
- Oracle accuracy: 0.9609375.
- Routed accuracy: 0.565625.
- Context accuracy: 0.496875.

This demonstrates a large difference between the potential of the contextual transformation and the performance of automatic routing.

### 6.3 Second experimental series: ex20–ex29

The second report studies ten additional experimental configurations.

All experiments in this series use:

```text
max_iters = 1
tau_target = 3.4
energy_monotonic_violations = 0
```

The experiments investigate:

- Calibration-to-dimension ratios.
- Very small calibration sets.
- Latent dimensions as low as one.
- Four-class and twenty-class classification.
- Different values of \(\gamma\).
- The effect of oracle versus automatic routing.

The reported results are summarized below.

| Experiment | Dataset | D / n_calib | γ | Raw | Oracle | Routed | Context |
|---|---|---:|---:|---:|---:|---:|---:|
| ex20 | 20news4 | 1/120 | 1.0 | 0.5781 | 0.5781 | 0.5781 | 0.3594 |
| ex21 | 20news4 | 1/16 | 1.0 | 0.4375 | 0.4375 | 0.4375 | 0.3359 |
| ex22 | 20news20 | 2/2 | 1.0 | 0.1984 | 0.7563 | 0.1844 | 0.1109 |
| ex23 | 20news4 | 1/1 | 1.0 | 0.5000 | 1.0000 | 0.5000 | 0.5000 |
| ex24 | 20news4 | 3/3 | 1.0 | 0.7031 | 1.0000 | 0.7578 | 0.7656 |
| ex25 | 20news4 | 3/3 | 1.0 | 0.7031 | 1.0000 | 0.7578 | 0.7656 |
| ex26 | 20news20 | 16/16 | 1.0 | 0.5563 | 0.9938 | 0.5469 | 0.4969 |
| ex27 | 20news20 | 16/16 | 0.5 | 0.5563 | 0.9609 | 0.5594 | 0.4969 |
| ex28 | 20news20 | 1/1 | 0.5 | 0.1219 | 0.3953 | 0.1313 | 0.0563 |
| ex29 | 20news20 | 1/1 | 1.0 | 0.1219 | 0.4344 | 0.1281 | 0.0641 |

These are the reported test accuracies. They should not be interpreted as independent estimates of generalization performance without additional information about dataset splits, repeated seeds, and statistical uncertainty.

### 6.4 Second-series observations

The second series reinforces several conclusions.

**1. Numerical stability can coexist with limited classification gains.**

Experiments ex20 and ex21 exhibit small geometric and operator gaps, but the oracle transformation does not improve the reported accuracy.

**2. Oracle context can reveal substantial classification potential.**

Experiments ex22, ex23, ex24 and ex25 show that contextual information can substantially improve classification when the appropriate context is supplied.

**3. Automatic routing remains the main operational bottleneck.**

In ex22, the oracle reaches 0.75625 while routed accuracy is 0.184375.

In ex26, the oracle reaches 0.99375 while routed accuracy is 0.546875.

**4. Small calibration configurations require careful interpretation.**

The experiments with one or two calibration samples demonstrate interesting behavior, but they do not establish robust generalization from extremely limited calibration data.

**5. One iteration can be sufficient for the reported numerical evaluations.**

All runs in this series use `max_iters=1` and report zero energy monotonicity violations. This supports the observation that deeper iteration is not automatically the most important route to improved operational performance.

## 7. Main scientific findings

Taken together, the two experimental reports suggest the following interpretation.

### Finding 1 — Strong normalized scalar consistency

The observed scalar contraction coefficients remain close to:

\[
\rho_\star = \frac{1}{1+\tau}
\]

across the reported configurations.

### Finding 2 — Operator consistency is more restrictive

Scalar agreement alone is insufficient to establish the complete normalized support criterion.

The operator gap can exceed the prescribed threshold even when the scalar gap is small.

### Finding 3 — Stability and classification are different properties

A numerically supported configuration may still have poor routed classification accuracy.

The mathematical behavior of the local operator and the predictive quality of the complete pipeline must therefore be evaluated separately.

### Finding 4 — Oracle-versus-routed performance exposes the routing bottleneck

The difference between oracle and routed accuracy provides a useful diagnostic of context-selection quality.

A large gap indicates that useful contextual information may exist but is not being selected reliably by the automatic router.

### Finding 5 — Latent dimension and calibration jointly influence performance

The reported experiments do not show a simple monotonic relationship between latent dimension and classification accuracy.

The effective geometry depends on the interaction between latent dimension, calibration size, regularization, dataset complexity, and context selection.

## 8. Current limitations

The current experimental evidence has important limitations.

- The experiments cover a limited set of text classification datasets.
- The reported configurations do not establish universal behavior across arbitrary datasets.
- Several configurations have very small calibration sets.
- Some experimental blocks contain numerically identical results.
- Oracle performance assumes access to the appropriate context and is not equivalent to deployable performance.
- Automatic routing is not yet sufficiently reliable in several configurations.
- Finite-difference Jacobians and numerical QP solutions are subject to numerical precision.
- The reports do not establish statistical significance across independent datasets and random seeds.
- The current evidence does not demonstrate a universal geometric identity of the projection operator.
- Zero energy monotonicity violations in the reported runs do not prove convergence for all possible configurations.

**Scientific conclusion:** The evidence supports strong normalized scalar consistency and promising contextual separability under oracle information. It does not yet establish universal geometric invariance or consistently strong end-to-end classification performance.



## 9. Recommended future work

The experimental evidence points to several high-priority research directions.

1. Improve automatic context routing.
2. Develop confidence-aware context selection.
3. Evaluate routing calibration independently from PCH optimization.
4. Study the interaction between calibration size and latent dimension.
5. Test the framework on additional datasets and domains.
6. Repeat experiments across multiple independent random seeds.
7. Quantify uncertainty in classification accuracy and numerical diagnostics.
8. Investigate more efficient convex optimization procedures.
9. Study the sensitivity of the operator gap to solver tolerances.
10. Establish theoretical conditions for broader geometric invariance.
11. Compare against strong conventional classification baselines.
12. Evaluate computational cost, memory consumption, and deployment feasibility.

## 10. Intended use

This repository is intended for:

- Mathematical and numerical research.
- Experimental analysis of proximal optimization.
- Investigation of contextual convex geometry.
- Research into representation refinement.
- Evaluation of oracle and automatic context selection.
- Reproduction and extension of the reported experiments.

It should not be presented as a production-ready language model or a validated replacement for conventional neural architectures.

## 11. Citation

If you use this work, cite the relevant project documents and implementation.

A citation template can be completed once the authorship, publication date, repository URL, and version are established:

```bibtex
@misc{pure_pch,
  title        = {Pure PCH: Normalized Geometry, Exact Proximal Operators and Experimental Validation},
  author       = {Author(s) to be specified : BENSALEM NASSIM.},
  year         = {Year to be specified},
  howpublished = {Research repository},
  url          = {Repository URL to be specified}
}
```



---

# 🇫🇷 FRANÇAIS

## 1. Présentation générale

**Pure PCH** est un cadre de recherche consacré à l'étude d'un mécanisme proximal normalisé reposant sur la géométrie contextuelle, les contraintes convexes et l'optimisation exacte ou numériquement de haute précision.

Le projet étudie comment une représentation de données peut être transformée au moyen d'une géométrie convexe dépendante du contexte et d'opérateurs proximaux, et comment cette transformation influence la stabilité mathématique locale ainsi que les performances de classification en aval.

La question expérimentale centrale est la suivante :

> Un mécanisme proximal normalisé peut-il conserver une stabilité mathématique à travers différentes dimensions latentes, différents régimes de régularisation, différentes tailles de calibration et différentes tâches de classification, tout en préservant une structure utile à la classification ?

Le projet distingue deux propriétés fondamentales :

1. **La stabilité mathématique :** l'opérateur normalisé respecte-t-il les relations scalaires et opératorielles attendues ?
2. **L'utilité pratique :** la représentation obtenue améliore-t-elle la classification lorsque le contexte doit être sélectionné automatiquement ?

Les expériences indiquent que ces deux propriétés sont liées, mais ne sont pas équivalentes.

## 2. Objectifs scientifiques

Le projet étudie notamment :

- Le comportement normalisé des opérateurs proximaux contextuels.
- La relation entre contraction scalaire et cohérence au niveau opératoriel.
- Le rôle de la géométrie convexe contextuelle dans le raffinement des représentations.
- L'influence de la dimension latente sur la structure géométrique effective.
- L'effet de la taille de calibration sur l'optimisation contextuelle.
- La différence entre sélection oracle du contexte et routage automatique.
- L'influence de la régularisation et du paramètre \(\gamma\).
- La relation entre stabilité numérique et précision de classification.

L'objectif général est de déterminer quelles propriétés sont intrinsèques au mécanisme PCH normalisé et lesquelles dépendent de la qualité de la sélection du contexte.

## 3. Cadre mathématique

### 3.1 Cas 3 normalisé

Le cadre expérimental utilise la paramétrisation normalisée suivante :

\[
\mu = 1 + 2\lambda_{\mathrm{ridge}}
\]

\[
\gamma =
\frac{\lambda_{\mathrm{ctx}}}{\mu}
\]

\[
\tau = \eta\mu
\]

Le coefficient de contraction scalaire cible est :

\[
\rho_\star = \frac{1}{1+\tau}
\]

Dans le régime expérimental principal :

\[
\tau = 3.4
\]

d'où :

\[
\rho_\star =
\frac{1}{4.4}
\approx 0.2272727273
\]

Cette formulation normalisée permet de comparer les expériences réalisées avec différentes configurations de paramètres.

### 3.2 Géométrie convexe contextuelle

Le cadre construit des ensembles contextuels à partir des embeddings de calibration.

Pour un contexte \(c\), l'ensemble contextuel est représenté par une enveloppe convexe :

\[
M_c = \operatorname{conv}(Z_c)
\]

où \(Z_c\) désigne les embeddings de calibration associés à ce contexte.

Cette géométrie convexe définit la région admissible dans laquelle sont effectuées les projections contextuelles et les optimisations proximales.

### 3.3 Optimisation exacte

Le pipeline expérimental utilise l'optimisation quadratique convexe pour :

- La projection sur les ensembles convexes contextuels.
- Le calcul du minimiseur PCH.
- L'évaluation de l'application proximale.

L'implémentation expérimentale rapportée utilise :

- `cvxpy`
- `OSQP`
- Tolérance absolue : \(10^{-10}\)
- Tolérance relative : \(10^{-10}\)
- Nombre maximal d'itérations du solveur : `500000`

Ces paramètres décrivent l'implémentation expérimentale rapportée. Ils ne constituent pas une garantie universelle d'arithmétique exacte : les solveurs numériques utilisent une précision finie et des tolérances.

### 3.4 Diagnostics locaux

Le cadre évalue la cohérence mathématique locale au moyen de plusieurs quantités :

- Écart de contraction scalaire.
- Écart opératoriel.
- Écart de projection.
- Résidu de point fixe.
- Estimations des jacobiens locaux.
- Violations de monotonie énergétique.
- Trace effective du projecteur.

Les jacobiens locaux sont estimés par différences finies.

Ces diagnostics servent à étudier le comportement numérique et mathématique local du mécanisme, et non à mesurer directement sa qualité de classification.

## 4. Pipeline expérimental

Les expériences rapportées suivent la procédure générale suivante :

1. Chargement du corpus de classification textuelle.
2. Génération des embeddings avec un encodeur SentenceTransformer gelé.
3. Ajustement de la PCA exclusivement sur les données de calibration.
4. Projection des embeddings dans la dimension latente choisie.
5. Construction des enveloppes convexes contextuelles à partir des embeddings de calibration.
6. Calcul des projections convexes contextuelles.
7. Résolution des problèmes d'optimisation PCH correspondants.
8. Évaluation de la transformation proximale.
9. Calcul des diagnostics numériques et géométriques locaux.
10. Évaluation de la classification dans différentes conditions de sélection contextuelle.
11. Agrégation des résultats selon les configurations expérimentales.

### Distinction méthodologique importante

Dans le pipeline rapporté, la PCA est ajustée uniquement sur les données de calibration. Cette contrainte vise à empêcher les données de test d'influencer l'ajustement de la réduction dimensionnelle.

Pour reproduire rigoureusement les résultats, il convient également de documenter les partitions de données, le prétraitement, les graines aléatoires et le protocole d'évaluation.

## 5. Évaluation de la classification

Les expériences distinguent quatre mesures de précision.

| Métrique | Signification |
|---|---|
| Raw accuracy | Performance de classification avant la transformation PCH |
| Oracle accuracy | Performance lorsque le contexte approprié est fourni |
| Routed accuracy | Performance lorsque le système sélectionne automatiquement le contexte |
| Context accuracy | Précision contextuelle ou prédictive rapportée par le pipeline expérimental |

Les métriques oracle et routed ne mesurent pas la même chose.

La **précision oracle** évalue le potentiel du mécanisme PCH lorsque le contexte approprié est connu.

La **précision routée** évalue le pipeline opérationnel complet, y compris la sélection automatique du contexte.

Par conséquent, une forte précision oracle ne garantit pas une forte précision routée.

Cette distinction constitue l'un des résultats les plus importants de l'étude expérimentale.

## 6. Résultats expérimentaux

### 6.1 Première série : ex1–ex13

Le premier rapport contient :

- 13 blocs expérimentaux.
- 54 runs individuels.
- Les corpus `20news4` et `20news20`.
- Des dimensions latentes de 8, 16, 32, 48 et 64.
- Plusieurs configurations de régularisation.
- Plusieurs valeurs de \(\gamma\).
- Une valeur cible fixe de \(\tau=3.4\).

Le critère scripté de support est :

\[
\max \rho_{\mathrm{gap}} \leq 10^{-4}
\]

et

\[
\max \operatorname{operator\_gap}
\leq 10^{-4}
\]

Les deux conditions doivent être satisfaites simultanément.

**Résultat rapporté :**

| Résultat | Blocs expérimentaux |
|---|---|
| Supportés | ex6, ex7, ex8, ex9, ex11, ex12, ex13 |
| Non supportés | ex1, ex2, ex3, ex4, ex5, ex10 |

Ainsi, 7 des 13 blocs expérimentaux satisfont le critère numérique spécifié.

Un verdict négatif ne signifie pas nécessairement que la relation scalaire est incorrecte. Certains blocs échouent parce que l'écart opératoriel dépasse le seuil imposé.

### 6.2 Observations de la première série

Plusieurs observations importantes ressortent :

- Le comportement scalaire normalisé reste proche de sa valeur théorique dans les expériences rapportées.
- Le critère opératoriel est plus restrictif que le critère scalaire.
- Certaines configurations de faible dimension satisfont le critère numérique alors que des configurations de dimension supérieure ne le satisfont pas.
- Une excellente précision oracle peut coexister avec une précision routée nettement plus faible.
- Une augmentation de \(\gamma\) n'améliore pas automatiquement la classification.
- Un verdict numérique supporté ne signifie pas que le routeur automatique de contexte est efficace.

L'expérience `20news20` en dimension 16 est particulièrement illustrative :

- Précision brute : 0.55625.
- Précision oracle : 0.9609375.
- Précision routée : 0.565625.
- Précision contextuelle : 0.496875.

Cette expérience met en évidence un écart important entre le potentiel de la transformation contextuelle et les performances du routage automatique.

### 6.3 Deuxième série : ex20–ex29

Le deuxième rapport étudie dix configurations expérimentales supplémentaires.

Toutes les expériences de cette série utilisent :

```text
max_iters = 1
tau_target = 3.4
energy_monotonic_violations = 0
```

Elles examinent notamment :

- Les rapports entre dimension et taille de calibration.
- Les ensembles de calibration très réduits.
- Les dimensions latentes allant jusqu'à un.
- La classification à quatre et vingt classes.
- Différentes valeurs de \(\gamma\).
- La différence entre routage oracle et routage automatique.

Les résultats rapportés sont résumés ci-dessous.

| Expérience | Corpus | D / n_calib | γ | Raw | Oracle | Routed | Context |
|---|---|---:|---:|---:|---:|---:|---:|
| ex20 | 20news4 | 1/120 | 1.0 | 0.5781 | 0.5781 | 0.5781 | 0.3594 |
| ex21 | 20news4 | 1/16 | 1.0 | 0.4375 | 0.4375 | 0.4375 | 0.3359 |
| ex22 | 20news20 | 2/2 | 1.0 | 0.1984 | 0.7563 | 0.1844 | 0.1109 |
| ex23 | 20news4 | 1/1 | 1.0 | 0.5000 | 1.0000 | 0.5000 | 0.5000 |
| ex24 | 20news4 | 3/3 | 1.0 | 0.7031 | 1.0000 | 0.7578 | 0.7656 |
| ex25 | 20news4 | 3/3 | 1.0 | 0.7031 | 1.0000 | 0.7578 | 0.7656 |
| ex26 | 20news20 | 16/16 | 1.0 | 0.5563 | 0.9938 | 0.5469 | 0.4969 |
| ex27 | 20news20 | 16/16 | 0.5 | 0.5563 | 0.9609 | 0.5594 | 0.4969 |
| ex28 | 20news20 | 1/1 | 0.5 | 0.1219 | 0.3953 | 0.1313 | 0.0563 |
| ex29 | 20news20 | 1/1 | 1.0 | 0.1219 | 0.4344 | 0.1281 | 0.0641 |

Il s'agit des précisions de test rapportées. Elles ne doivent pas être interprétées comme des estimations indépendantes de généralisation sans informations supplémentaires sur les partitions, les graines répétées et l'incertitude statistique.

### 6.4 Observations de la deuxième série

La deuxième série renforce plusieurs conclusions.

**1. La stabilité numérique peut coexister avec des gains de classification limités.**

Les expériences ex20 et ex21 présentent de faibles écarts géométriques et opératoriels, mais la transformation oracle n'améliore pas la précision rapportée.

**2. Le contexte oracle peut révéler un potentiel de classification important.**

Les expériences ex22, ex23, ex24 et ex25 montrent que l'information contextuelle peut fortement améliorer la classification lorsque le contexte approprié est fourni.

**3. Le routage automatique demeure le principal goulot d'étranglement opérationnel.**

Dans ex22, l'oracle atteint 0.75625 tandis que la précision routée est de 0.184375.

Dans ex26, l'oracle atteint 0.99375 tandis que la précision routée est de 0.546875.

**4. Les configurations avec très peu de données de calibration doivent être interprétées avec prudence.**

Les expériences utilisant un ou deux échantillons de calibration présentent des comportements intéressants, mais ne démontrent pas une généralisation robuste à partir de données de calibration extrêmement limitées.

**5. Une seule itération peut suffire pour les évaluations numériques rapportées.**

Tous les runs de cette série utilisent `max_iters=1` et rapportent zéro violation de monotonie énergétique. Cela suggère qu'augmenter systématiquement le nombre d'itérations n'est pas nécessairement la meilleure stratégie pour améliorer les performances opérationnelles.

## 7. Principaux résultats scientifiques

Pris ensemble, les deux rapports expérimentaux suggèrent l'interprétation suivante.

### Résultat 1 — Forte cohérence scalaire normalisée

Les coefficients de contraction scalaires observés restent proches de :

\[
\rho_\star = \frac{1}{1+\tau}
\]

dans les configurations rapportées.

### Résultat 2 — La cohérence opératorielle est plus restrictive

La seule conformité scalaire ne suffit pas à établir le critère complet de support normalisé.

L'écart opératoriel peut dépasser le seuil imposé alors même que l'écart scalaire est faible.

### Résultat 3 — Stabilité et classification sont deux propriétés distinctes

Une configuration numériquement supportée peut présenter une précision routée médiocre.

Le comportement mathématique de l'opérateur local et la qualité prédictive du pipeline complet doivent donc être évalués séparément.

### Résultat 4 — L'écart oracle/routed révèle le problème de routage

La différence entre la précision oracle et la précision routée constitue un indicateur utile de la qualité de sélection contextuelle.

Un écart important indique qu'une information contextuelle utile peut exister sans être correctement sélectionnée par le routeur automatique.

### Résultat 5 — Dimension latente et calibration influencent conjointement les performances

Les expériences ne montrent pas de relation monotone simple entre dimension latente et précision de classification.

La géométrie effective dépend de l'interaction entre dimension latente, taille de calibration, régularisation, complexité du corpus et qualité du routage.

## 8. Limites actuelles

Les résultats expérimentaux présentent plusieurs limites importantes.

- Les expériences couvrent un nombre limité de corpus de classification textuelle.
- Les configurations rapportées ne démontrent pas un comportement universel sur des données arbitraires.
- Certaines configurations utilisent des ensembles de calibration très réduits.
- Certains blocs expérimentaux présentent des résultats numériquement identiques.
- Les performances oracle supposent l'accès au contexte approprié et ne correspondent pas aux performances directement déployables.
- Le routage automatique reste insuffisamment fiable dans plusieurs configurations.
- Les jacobiens par différences finies et les solutions QP numériques sont soumis aux limites de précision numérique.
- Les rapports ne démontrent pas de significativité statistique sur plusieurs corpus et graines aléatoires indépendantes.
- Les résultats ne démontrent pas une identité géométrique universelle de l'opérateur de projection.
- L'absence de violation de monotonie énergétique dans les runs rapportés ne prouve pas la convergence pour toutes les configurations possibles.

**Conclusion scientifique :** les résultats soutiennent une forte cohérence scalaire normalisée et un potentiel prometteur de séparabilité contextuelle lorsque l'information oracle est disponible. Ils ne démontrent pas encore une invariance géométrique universelle ni des performances de classification de bout en bout systématiquement élevées.


## 9. Perspectives de recherche

Les résultats expérimentaux indiquent plusieurs axes prioritaires.

1. Améliorer le routage automatique des contextes.
2. Développer une sélection contextuelle tenant compte du niveau de confiance.
3. Évaluer la calibration du routage indépendamment de l'optimisation PCH.
4. Étudier l'interaction entre taille de calibration et dimension latente.
5. Tester le cadre sur davantage de corpus et de domaines.
6. Répéter les expériences avec plusieurs graines aléatoires indépendantes.
7. Quantifier l'incertitude des précisions de classification et des diagnostics numériques.
8. Étudier des procédures d'optimisation convexe plus efficaces.
9. Analyser la sensibilité de l'écart opératoriel aux tolérances du solveur.
10. Établir des conditions théoriques permettant une invariance géométrique plus générale.
11. Comparer le système à des méthodes classiques de classification solides.
12. Évaluer les coûts de calcul, la mémoire utilisée et la faisabilité du déploiement.

## 10. Utilisation prévue

Ce dépôt est destiné à :

- La recherche mathématique et numérique.
- L'analyse expérimentale de l'optimisation proximale.
- L'étude de la géométrie convexe contextuelle.
- La recherche sur le raffinement des représentations.
- L'évaluation de la sélection oracle et automatique des contextes.
- La reproduction et l'extension des expériences rapportées.

Il ne doit pas être présenté comme un modèle de langage prêt pour la production ni comme un remplacement validé des architectures neuronales conventionnelles.

## 11. Citation

En cas d'utilisation de ces travaux, il convient de citer les documents scientifiques et l'implémentation correspondants.

Le modèle de citation suivant pourra être complété lorsque les auteurs, la date de publication, l'URL du dépôt et la version seront établis :

```bibtex
@misc{pure_pch,
  title        = {Pure PCH: Normalized Geometry, Exact Proximal Operators and Experimental Validation},
  author       = {Auteur(s) à préciser : BENSALEM NASSIM.},
  year         = {Année à préciser},
  howpublished = {Dépôt de recherche},
  url          = {URL du dépôt à préciser}
}
```


---

# Final note / Note finale

This repository documents a research framework and its reported experimental evidence. Its central contribution is the investigation of normalized proximal consistency, contextual convex geometry, and the gap between oracle and automatically routed classification.

Ce dépôt documente un cadre de recherche et les résultats expérimentaux rapportés. Sa contribution centrale est l'étude de la cohérence proximale normalisée, de la géométrie convexe contextuelle et de l'écart entre classification oracle et classification avec routage automatique.

