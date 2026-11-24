


# eSonde v8.2.2, Other Versions, Population Variants & Research Works

**Bilingual technical overview — English and French**  
**Documentation date:** 24 November 2026

This README is the Markdown counterpart of `docs_eSonde_v8.2.2_&_others_versions_&_variants.tex`. It preserves the technical information, experimental results, qualifications, provenance notes, and package-layout information contained in that source. The English and French sections are kept separate.

> **Interpretation rule:** distinguish the one-million-Obsiss eSonde v8.2.2 base checkpoint from the eight 512-Obsiss experimental populations of v8.2.3. A coordination method tested on a population is not, by that fact alone, a separate model checkpoint.

# Complete Project Files : 
> **All complete project files and deliverables are available in the **Releases** section (eSonde_v8_2_1
, eSonde_v8_2_2, eSonde_v8_2_2_variantes).

---

# Part I — English

## Table of contents

- [1. Documentation scope and reading guide](#1-documentation-scope-and-reading-guide)
- [2. eSonde v8.2.2 base model](#2-esonde-v822-base-model)
- [3. Historical source versions v8.2.0 and v8.2.1](#3-historical-source-versions-v820-and-v821)
- [4. Eight finalized v8.2.3 population variants](#4-eight-finalized-v823-population-variants)
- [5. Research work catalogue](#5-research-work-catalogue)
- [6. Evidence boundaries and known caveats](#6-evidence-boundaries-and-known-caveats)
- [7. Documentation package layout](#7-documentation-package-layout)
- [8. Source-consistency note](#8-source-consistency-note)
- [Part II — Documentation française](#part-ii--documentation-française)

## 1. Documentation scope and reading guide

This document consolidates the recovered Dmodel v8.2.2 documentation, selected Amodel v8.2.2 audit materials, the eight finalized v8.2.3 population checkpoints, and the research works recorded in this conversation and the recovered v8.2.3/v8.2.4 evidence. It distinguishes the one-million-Obsiss base model from the 512-Obsiss experimental populations and distinguishes model checkpoints from coordination methods.

The associated documentation package has separate language trees: `EN/` and `FR/`. Each model, population variant and research work has its own README and technical documentation in both languages. Original source documents are preserved under `SOURCE_REFERENCES/`. The master LaTeX document contains the English section followed by a separate French section; this Markdown file follows the same language separation.

## 2. eSonde v8.2.2 base model

The delivered base is a **CPU-only non-neural engineering candidate** with:

- **Population:** one million Obsiss.
- **Dimension:** 16.
- **Weights:** int16 WH/WP weights, **64,000,000 bytes**.
- **Processing components:** language/context preprocessing; sparse n-gram/beam proposal; P context activations; grouped response-only R scoring; and a coordinator/ranker selected from A0–A4, Potts or TFIM.

The documented OASST1 dataset contains **52,108 retained pairs**:

| Split | Retained pairs |
|---|---:|
| TRAIN | 41,673 |
| VALIDATION | 5,290 |
| TEST | 5,145 |
| **Total** | **52,108** |

**Dataset SHA-256:** `c412ae3aba06970bbbd5b03d6a94acfb23fc590eff24d9735d8c7a8439e00b01`.

The checkpoint was rebuilt from verified TRAIN statistics with fresh WH/WP weights. The historic v8.2.1 weights were truncated; full raw-statistics rebuild and contrastive fit attempts were interrupted and not committed. The delivered checkpoint contains **one canonical functional profile** and **zero profile graph edges**.

The smoke prompt `What is water?` produced `I's a good.`. Software execution succeeded, but response quality failed. Multi-turn, out-of-distribution (OOD), and human validation are absent. Therefore, this checkpoint is an **engineering candidate**, not an accepted conversational model.

## 3. Historical source versions v8.2.0 and v8.2.1

### eSonde v8.2.0

The v8.2.0 source is a formal laboratory specification dated **22 November 2026**. It records:

- stable Obsiss identities;
- integer/statistical features;
- signed deterministic identity transforms;
- P/R operators;
- A0–A4 coordination methods;
- CPU-only bounded processing; and
- TRAIN/VALIDATION/TEST separation.

It is a design/formal record. The inspected sources do **not** establish a separate verified final v8.2.0 checkpoint.

### eSonde v8.2.1

The v8.2.1 archive contains formalism, runtime guides and status records, but the source-recovery report says the historical weight record was truncated and no complete corresponding checkpoint was recovered.

The v8.2.2 checkpoint reused verified TRAIN language statistics but initialized fresh WH/WP weights. It is explicitly **not a bitwise restoration** of v8.2.1.

See the separate `models/eSonde_v8_2_0/` and `models/eSonde_v8_2_1/` documents in both language trees.

## 4. Eight finalized v8.2.3 population variants

Each experimental checkpoint contains **512 Obsiss**, dimension **16**, and a **32,768-byte** weights file. Profiles are exact canonical weight-equivalence classes discovered after training; semantic roles were not assigned to them.

| Variant | Exposure | Profiles | VALIDATION A0 | TEST A0 | TEST TFIM |
|---|---|---:|---:|---:|---:|
| `shared` | Shared population | 1 | 166/256 | 299/512 (58.40%) | 58.40% |
| `local256` | Cohorts of 256 | 2 | 174/256 | 314/512 (61.33%) | 60.35% |
| `local128` | Cohorts of 128 | 4 | 169/256 | 323/512 (63.09%) | 64.45% |
| `local64` | Cohorts of 64 | 8 | 170/256 | 338/512 (66.02%) | 65.63% |
| `local32` | Cohorts of 32 | 16 | 172/256 | 336/512 (65.63%) | 65.43% |
| `local16` | Cohorts of 16 | 32 | 171/256 | 334/512 (65.23%) | 65.43% |
| `random64` | Random 64/512 active identities per example | 512 | 171/256 | 331/512 (64.65%) | 64.65% |
| `annealed16_to_all` | Exposure ramps from 1/16 to 100% | 512 | 167/256 | 327/512 (63.87%) | 64.06% |

The fixed-cohort local-vs-shared paired confirmatory comparison with Holm correction retains advantages for `local128`, `local64`, `local32` and `local16`; `local256` does not pass the adjusted 0.05 threshold. These are reference-vs-distractor retrieval results on 512 examples, **not free-form dialogue scores**.

Potts decisions match A0 for the fixed-cohort variants. No TFIM change survives the stated multiple-comparison correction. The two natural-exposure variants (`random64` and `annealed16_to_all`) are recorded separately and are not part of the five fixed-cohort Holm family.

## 5. Research work catalogue

1. **Functional specialization.** Fixed local-cohort exposure generated 1, 2, 4, 8, 16 and 32 exact profiles without semantic role assignment.
2. **Natural exposure.** `random64` changes the 64 active identities per example; `annealed16_to_all` ramps exposure from 6.25% to 100%.
3. **Complementarity.** Per-profile TRAIN margins and retrospective oracle bounds measure potential disagreement/complementarity. The oracle chooses retrospectively and is not deployable.
4. **Coordination.** A0–A4, finite-temperature Potts mean-field and classical TFIM mean-field were tested. No robust held-out coordination gain was established.
5. **Signed residual graphs.** Common example difficulty and profile mean are removed before estimating signed TRAIN correlations. The signs did not translate into confirmed gains.
6. **Local-to-global and recursion.** Local-only, global-from-start, staged local-to-global and recursive methods changed support margins but not accuracy in the `random64`/`annealed16_to_all` confirmatory tests.
7. **Competence reinforcement.** TRAIN-derived reliability weighting was compared with equal voting and an identity-permutation placebo. Differences were not statistically supported.
8. **TF-IDF context routing.** The contextual lexical router matched A0 at **335/512** and made no confirmed improvement.
9. **Living context v8.2.4.** Real P/R operators were used on `local64`, with population-relative activations and persistent response feedback. Validation remained **170/256** for all methods, and dialogue smoke answers were poor.
10. **Dialogue/generalization.** None of the retrieved benchmarks establishes coherent free-form multi-turn semantic generalization.
11. **Integrity/provenance.** Source archives were recovered, the eight checkpoints were audited, and stale metadata and historic manifest discrepancies were preserved as explicit caveats.

## 6. Evidence boundaries and known caveats

### What the reported evaluations do and do not show

- The fixed-cohort TEST is a paired reference-response/distractor classification task.
- Profile count and oracle complementarity are **not proofs of intelligence**.
- Consensus margins do not replace accuracy.
- The v8.2.4 two-turn loop proves technical state feedback only.
- The v8.2.4 dialogue smoke answers were `Here are some of the most popular.` and `The most popular and a few examples.`; these are poor dialogue outputs, not evidence of coherent generation.
- The k-NN context-to-utility map was rejected because its TRAIN cross-validation error was worse than that of a mean-only predictor.
- No retrieved benchmark establishes coherent free-form multi-turn semantic generalization.

### Checkpoint metadata and legacy-source discrepancies

In the original experimental `TRAIN_RESULT.json` files, the top-level `weights_bytes=64,000,000` and top-level `weights_sha256` are stale inherited fields. The actual variant weight files are **32,768 bytes**, and their hashes agree across `model.json`, the sidecar and the nested fit record.

One legacy report file is concatenated JSON and was preserved as-is. The old v8.2.1 root checksum manifest does not fully describe the present v8.2.2 tree. These caveats are preserved in the source audit; original files were not rewritten.

## 7. Documentation package layout

The associated documentation package uses this layout:

| Directory | Contents |
|---|---|
| `EN/` | English README and technical documentation for the base model, eight variants and research works. |
| `FR/` | Equivalent French-only documentation, separate from English. |
| `SOURCE_REFERENCES/` | Selected original source documents, reports, formal files, manifests and audit material. |
| `manifests/` | SHA-256 manifest for the documentation set. |

## 8. Source-consistency note

The scope paragraph of the LaTeX source refers to **twelve** research works, while its research catalogue contains **eleven numbered entries**. This README preserves all eleven catalogue entries and records the discrepancy rather than inventing a twelfth item or silently changing the source count.

---

# Part II — Documentation française

## Table des matières

- [1. Périmètre documentaire et guide de lecture](#1-périmètre-documentaire-et-guide-de-lecture)
- [2. Modèle de base eSonde v8.2.2](#2-modèle-de-base-esonde-v822)
- [3. Versions sources historiques v8.2.0 et v8.2.1](#3-versions-sources-historiques-v820-et-v821)
- [4. Huit variantes de population finalisées v8.2.3](#4-huit-variantes-de-population-finalisées-v823)
- [5. Catalogue des travaux de recherche](#5-catalogue-des-travaux-de-recherche)
- [6. Limites des preuves et réserves connues](#6-limites-des-preuves-et-réserves-connues)
- [7. Structure du paquet documentaire](#7-structure-du-paquet-documentaire)
- [8. Note de cohérence de la source](#8-note-de-cohérence-de-la-source)

## 1. Périmètre documentaire et guide de lecture

Ce document rassemble la documentation retrouvée de Dmodel v8.2.2, une sélection de pièces d’audit Amodel v8.2.2, les huit checkpoints finaux de populations v8.2.3 et les travaux de recherche consignés dans cette conversation ainsi que dans les preuves v8.2.3/v8.2.4. Il distingue le modèle de base d’un million d’Obsiss des populations expérimentales de 512 Obsiss et distingue les checkpoints des méthodes de coordination.

Le paquet documentaire associé sépare les langues dans deux arborescences : `EN/` et `FR/`. Chaque modèle, variante de population et travail de recherche possède son propre README et sa documentation technique dans les deux langues. Les documents sources originaux sont conservés sous `SOURCE_REFERENCES/`. Le document LaTeX maître contient la partie anglaise puis une partie française distincte ; ce fichier Markdown conserve la même séparation linguistique.

## 2. Modèle de base eSonde v8.2.2

Le modèle de base livré est un **candidat d’ingénierie CPU-only non neuronal** comprenant :

- **Population :** un million d’Obsiss.
- **Dimension :** 16.
- **Poids :** poids WH/WP int16, **64 000 000 octets**.
- **Composants de traitement :** prétraitement de langue/contexte ; proposition sparse n-gramme/beam ; activations de contexte P ; score R groupé response-only ; coordinateur/classeur A0–A4, Potts ou TFIM.

Le corpus OASST1 documenté contient **52 108 paires retenues** :

| Partition | Paires retenues |
|---|---:|
| TRAIN | 41 673 |
| VALIDATION | 5 290 |
| TEST | 5 145 |
| **Total** | **52 108** |

**SHA-256 du corpus :** `c412ae3aba06970bbbd5b03d6a94acfb23fc590eff24d9735d8c7a8439e00b01`.

Le checkpoint a été reconstruit à partir de statistiques TRAIN vérifiées avec de nouveaux poids WH/WP. Les anciens poids v8.2.1 étaient tronqués ; les tentatives de reconstruction complète depuis les statistiques brutes et d’ajustement contrastif ont été interrompues et non commises. Le checkpoint livré contient **un seul profil fonctionnel canonique** et **zéro arête du graphe des profils**.

Le prompt smoke `What is water?` a produit `I's a good.`. L’exécution logicielle a réussi, mais la qualité de réponse a échoué. La validation multi-tour, hors distribution (OOD) et humaine est absente. Ce checkpoint est donc un **candidat d’ingénierie**, et non un modèle conversationnel accepté.

## 3. Versions sources historiques v8.2.0 et v8.2.1

### eSonde v8.2.0

La source v8.2.0 est une spécification formelle de laboratoire datée du **22 novembre 2026**. Elle consigne :

- les identités Obsiss stables ;
- les caractéristiques entières/statistiques ;
- les transformations signées déterministes propres aux identités ;
- les opérateurs P/R ;
- les méthodes de coordination A0–A4 ;
- le traitement CPU-only borné ;
- la séparation TRAIN/VALIDATION/TEST.

Il s’agit d’un document de conception/formalisme. Les sources inspectées **n’établissent pas l’existence d’un checkpoint final v8.2.0 distinct et vérifié**.

### eSonde v8.2.1

L’archive v8.2.1 contient le formalisme, des guides runtime et des états, mais le rapport de récupération des sources indique que l’enregistrement historique des poids était tronqué et qu’aucun checkpoint complet correspondant n’a été retrouvé.

Le checkpoint v8.2.2 a réutilisé des statistiques linguistiques TRAIN vérifiées, mais initialisé de nouveaux poids WH/WP. Il ne constitue explicitement **pas une restauration bit à bit** de v8.2.1.

Voir les documents séparés `models/eSonde_v8_2_0/` et `models/eSonde_v8_2_1/` dans les deux arborescences linguistiques.

## 4. Huit variantes de population finalisées v8.2.3

Chaque checkpoint expérimental contient **512 Obsiss**, une dimension **16** et un fichier de poids de **32 768 octets**. Les profils sont des classes d’équivalence exacte des poids canoniques découvertes après apprentissage ; aucun rôle sémantique ne leur a été attribué.

| Variante | Exposition | Profils | VALIDATION A0 | TEST A0 | TEST TFIM |
|---|---|---:|---:|---:|---:|
| `shared` | Population partagée | 1 | 166/256 | 299/512 (58,40 %) | 58,40 % |
| `local256` | Cohortes de 256 | 2 | 174/256 | 314/512 (61,33 %) | 60,35 % |
| `local128` | Cohortes de 128 | 4 | 169/256 | 323/512 (63,09 %) | 64,45 % |
| `local64` | Cohortes de 64 | 8 | 170/256 | 338/512 (66,02 %) | 65,63 % |
| `local32` | Cohortes de 32 | 16 | 172/256 | 336/512 (65,63 %) | 65,43 % |
| `local16` | Cohortes de 16 | 32 | 171/256 | 334/512 (65,23 %) | 65,43 % |
| `random64` | 64 identités actives sur 512, choisies aléatoirement par exemple | 512 | 171/256 | 331/512 (64,65 %) | 64,65 % |
| `annealed16_to_all` | Exposition croissante de 1/16 à 100 % | 512 | 167/256 | 327/512 (63,87 %) | 64,06 % |

La comparaison confirmatoire appariée des cohortes locales fixes contre `shared`, corrigée par Holm, conserve un avantage pour `local128`, `local64`, `local32` et `local16` ; `local256` ne passe pas le seuil ajusté de 0,05. Il s’agit de résultats de récupération référence contre distracteur sur 512 exemples, **pas de scores de dialogue libre**.

Les décisions Potts correspondent à A0 pour les variantes à cohortes fixes. Aucun changement TFIM ne résiste à la correction des comparaisons multiples indiquée. Les deux variantes d’exposition naturelle (`random64` et `annealed16_to_all`) sont rapportées séparément et ne font pas partie de la famille Holm des cinq comparaisons à cohortes fixes.

## 5. Catalogue des travaux de recherche

1. **Spécialisation fonctionnelle.** L’exposition à des cohortes locales fixes a produit 1, 2, 4, 8, 16 et 32 profils exacts sans assignation de rôles sémantiques.
2. **Exposition naturelle.** `random64` change les 64 identités actives à chaque exemple ; `annealed16_to_all` fait croître l’exposition de 6,25 % à 100 %.
3. **Mesure de complémentarité.** Les marges TRAIN par profil et les bornes oracle rétrospectives mesurent le potentiel de désaccord/complémentarité. L’oracle choisit rétrospectivement et n’est pas déployable.
4. **Coordination.** A0–A4, Potts en champ moyen à température finie et TFIM classique en champ moyen ont été testés. Aucun gain robuste de coordination sur les données tenues à l’écart n’a été établi.
5. **Graphes résiduels signés.** La difficulté commune des exemples et la moyenne par profil sont retirées avant l’estimation des corrélations signées TRAIN. Les signes ne se sont pas traduits par des gains confirmés.
6. **Local→global et récursion.** Les méthodes local seul, global dès le départ, local→global par étapes et récursive ont modifié les marges de soutien mais pas l’exactitude dans les tests confirmatoires `random64`/`annealed16_to_all`.
7. **Renforcement de compétence.** La pondération de fiabilité issue de TRAIN a été comparée au vote égal et à un placebo par permutation d’identités. Les différences ne sont pas statistiquement étayées.
8. **Routage contextuel TF-IDF.** Le routeur lexical contextuel a égalé A0 à **335/512** et n’a apporté aucune amélioration confirmée.
9. **Contexte vivant v8.2.4.** Les vrais opérateurs P/R ont été utilisés sur `local64`, avec des activations relatives à la population et un retour persistant de la réponse. La VALIDATION est restée à **170/256** pour toutes les méthodes et les réponses du smoke test de dialogue étaient mauvaises.
10. **Dialogue/généralisation.** Aucun des benchmarks retrouvés n’établit une généralisation sémantique cohérente en dialogue libre multi-tour.
11. **Intégrité/provenance.** Les archives sources ont été récupérées, les huit checkpoints audités et les métadonnées périmées ainsi que les divergences des anciens manifestes conservées comme réserves explicites.

## 6. Limites des preuves et réserves connues

### Ce que les évaluations rapportées montrent et ne montrent pas

- Le TEST des cohortes fixes est une tâche de classification appariée réponse de référence/distracteur.
- Le nombre de profils et la complémentarité oracle ne sont **pas des preuves d’intelligence**.
- Les marges de consensus ne remplacent pas l’exactitude.
- La boucle à deux tours v8.2.4 ne prouve que le retour technique d’état.
- Les réponses du smoke test de dialogue v8.2.4 étaient `Here are some of the most popular.` et `The most popular and a few examples.` ; ce sont de mauvaises sorties de dialogue, pas des preuves de génération cohérente.
- La carte k-NN contexte→utilité a été rejetée parce que son erreur de validation croisée TRAIN était supérieure à celle d’un prédicteur utilisant uniquement la moyenne.
- Aucun benchmark retrouvé n’établit une généralisation sémantique cohérente en dialogue libre multi-tour.

### Métadonnées des checkpoints et divergences des anciennes sources

Dans les fichiers expérimentaux originaux `TRAIN_RESULT.json`, les champs de premier niveau `weights_bytes=64,000,000` et `weights_sha256` sont des valeurs héritées périmées. Les vrais fichiers de poids des variantes font **32 768 octets**, et leurs hashes concordent entre `model.json`, le sidecar et l’enregistrement imbriqué de fit.

Un ancien fichier de rapport est constitué de JSON concaténés et a été conservé tel quel. L’ancien manifeste de sommes de contrôle v8.2.1 à la racine ne décrit pas complètement l’arborescence actuelle v8.2.2. Ces réserves sont conservées dans l’audit source ; les fichiers originaux n’ont pas été réécrits.

## 7. Structure du paquet documentaire

Le paquet documentaire associé utilise la structure suivante :

| Répertoire | Contenu |
|---|---|
| `EN/` | README et documentation technique en anglais du modèle de base, des huit variantes et des travaux de recherche. |
| `FR/` | Documentation équivalente exclusivement en français, séparée de l’anglais. |
| `SOURCE_REFERENCES/` | Sélection de documents sources originaux, rapports, fichiers formels, manifestes et pièces d’audit. |
| `manifests/` | Manifeste SHA-256 de l’ensemble documentaire. |

## 8. Note de cohérence de la source

Le paragraphe de périmètre de la source LaTeX mentionne **douze** travaux de recherche, alors que son catalogue de recherche contient **onze entrées numérotées**. Ce README conserve les onze entrées du catalogue et signale la divergence au lieu d’inventer une douzième entrée ou de modifier silencieusement le décompte de la source.

---

## Source de référence

The source of record for this conversion is `docs_eSonde_v8.2.2_&_others_versions_&_variants.tex`. This README is intended as its complete Markdown counterpart; it does not replace the individual model-, variant- and research-specific documentation in `EN/` and `FR/`.
