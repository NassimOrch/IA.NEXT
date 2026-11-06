# Orchestra Org récursif — index de bout en bout (EX7 V005)

Ce dossier ne décrit pas une simple proposition d'architecture : il référence le code d'entraînement, les checkpoints, les logits/prédictions, les folds OOF, les correcteurs, les ablations, les comparateurs MLP et les diagnostics réellement produits.

## Modèle récursif original

- Architecture racine : 7 couches × 5 probes par couche.
- `pi` : coordination globale interne des probes de chaque couche.
- `rho` : coordination globale externe entre les couches.
- Cascade et modulation des taux d'apprentissage : activées dans la variante originale.
- Entraînements racine terminés : **5/5 graines** (`1501, 1607, 1717, 2029, 3037`).
- Fits OOF récursifs : **5/5 graines**, trois folds par graine (**15 fits de folds**).
- Correcteurs OOF racine : **5/5** exécutions.
- Correcteurs OOF de sorties d'étages : **10/10** (2 variantes × 5 graines).

## Matrice des expériences associées

| Campagne | Résultats attendus | Résultats achevés | Emplacement principal |
|---|---:|---:|---|
| Orchestra Org racine 7×5 | 5 | 5 | `deliverables/EX7_ORCHESTRA_ORG_STATUS.json` |
| OOF récursif 3-fold | 5 | 5 (15 fits de fold) | `deliverables/EX7_ORCHESTRA_ORG_OOF_STATUS.json` |
| OOF correcteurs par étage | 10 | 10 | `deliverables/EX7_ORCHESTRA_ORG_STAGE_OOF_STATUS.json` |
| Ablations causales | 30 | 30 (6 × 5 graines) | `deliverables/EX7_ORCHESTRA_ORG_ABLATIONS_STATUS.json` |
| Profondeur/capacité | 25 | 25 (5 × 5 graines) | `deliverables/EX7_ORCHESTRA_ORG_CAPACITY_STATUS.json` |
| Compression structurelle | 60 | 60 (6 variantes × 2 familles × 5 graines) | `deliverables/EX7_STRUCTURAL_COMPRESSION_STATUS.json` |
| Couches parallèles/indépendantes | 5 | 5 | `deliverables/EX7_ORCHESTRA_ORG_PARALLEL_LAYERS_STATUS.json` |
| Correcteurs légers | 50 | 50 (5 variantes × 2 familles × 5 graines) | `deliverables/EX7_LIGHT_CORRECTORS_STATUS.json` |
| Distillation + base-only | 20 | 20 (2 variantes × 2 familles × 5 graines) | `deliverables/EX7_DISTILLED_AND_BASE_ONLY_STATUS.json` |
| OOF 2-fold | 10 | 10 | `deliverables/EX7_OOF_2FOLD_STATUS.json` |
| OOF 5-fold | 10 | 10 | `deliverables/EX7_OOF_5FOLD_STATUS.json` |

Tous les fichiers de statut de ces campagnes indiquent `test_opened: false`.

## Scripts d'exécution

- `src/run_orchestra_org_recursive.py` — architecture récursive racine.
- `src/run_orchestra_org_oof.py` — cross-fitting OOF strict de l'architecture récursive.
- `src/run_ex7_org_stage_oof.py` — correcteurs OOF de sorties d'étages.
- `src/run_orchestra_org_ablations.py` — matrice des ablations causales.
- `src/run_orchestra_org_capacity_variants.py` — profondeurs et capacités.
- `src/run_orchestra_org_parallel_layers.py` et `src/profile_orchestra_org_parallel_layers.py` — essais de parallélisation des couches.
- `src/profile_orchestra_org_vectorization.py` — profilage/parité vectorisée.
- `src/org_oof_parallel_fold_worker.py` et `src/benchmark_parallel_oof_folds.py` — essai de parallélisation des folds OOF.
- `src/run_orchestra_org_mlp_ge4x.py` — comparateur MLP adapté au budget.
- `src/run_ex7_structural_compression_variants.py` — 60 essais structurels.
- `src/run_ex7_oof_2fold.py` et `src/run_ex7_oof_5fold.py` — contrôles de nombre de folds.
- `src/run_ex7_light_correctors.py`, `src/run_ex7_distilled_and_base_only.py`, `src/export_and_profile_ex7.py` — familles de correcteurs/export.
- `src/audit_ex7_recursive_and_variants_v002.py` et `src/build_additional_org_mlp_comparisons_v002.py` — audit et comparaisons additionnelles.

## Sorties et checkpoints

- `results/raw/` : **642 éléments de système de fichiers** (prédictions, résumés, logits/folds et traces brutes).
- `results/metrics/` : tables agrégées et par graine/fold.
- `results/models/` : **458 checkpoints `.pt/.pth`** dans le snapshot V002, incluant les modèles racine, folds, correcteurs, variantes et comparateurs.
- `deliverables/` : statuts, audits, comparaisons par graine et agrégats finaux.
- `logs/` et `reports/` : journaux des interruptions/reprises et rapports d'exécution.

## Comparateurs supplémentaires post-V002

Le dossier `02_SUPPLEMENTS_POST_V002/EX7_V002_SUPPLEMENT/` comprend notamment les comparaisons MLP par graine et agrégées des bases récursives, des folds OOF, des correcteurs d'étages, des ablations et des variantes structurelles ; il comprend aussi `EX7_ORCHESTRA_ORG_STAGE_OOF_EXTRACTION_TIMING.csv`, les audits et le script de consolidation.

## Points d'entrée pour vérifier

1. `deliverables/EX7_RECURSIVE_ORG_AUDIT.json`
2. `deliverables/EX7_RECURSIVE_VARIANTS_AUDIT.json`
3. Les fichiers `*_STATUS.json` listés dans la matrice.
4. `results/metrics/EX7_ORCHESTRA_ORG_*_PER_SEED.csv` et `*_AGGREGATES.csv`.
5. `results/models/` et `results/raw/` pour les checkpoints et les prédictions brutes.

L'architecture récursive et ses expérimentations sont incluses dans le paquet ; cela ne signifie pas que l'objectif final de gain de vitesse/ressources a été atteint. Les métriques et rapports gardent les résultats négatifs et les limites tels qu'observés.
