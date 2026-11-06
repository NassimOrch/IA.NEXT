# EX7 — Livraison complète ciblée V005

## Périmètre

Cette livraison contient uniquement les deux snapshots EX7 V001 et V002 (complets depuis les répertoires de travail), les suppléments produits après V002, les outils propres à EX7 et les rapports/audits EX7. Aucun ZIP source complet EX4, EX5 ou EX6, aucun workspace EX4–EX6 et aucun prompt parent EX6 n'est inclus.

Le petit bundle `inputs/ex6_reference/` contenu dans chaque snapshot a été limité aux 34 dépendances de runtime/référence explicitement utilisées par les scripts EX7 : `ex6_common.py`, `ex6_mixa_engine.py`, l'entrée Wisconsin développement-only, les 10 checkpoints de référence Emplica/Orchestra OOF et leurs résumés/prédictions. Les anciens scripts EX6 sans usage EX7 ont été exclus. Il s'agit d'entrées figées de l'expérience EX7, pas d'une archive historique générale.

Le libellé « v100 » de la demande a été interprété comme **V001** : aucun artefact distinct nommé V100 n'existe dans les fichiers disponibles.

## Snapshots présents

| Snapshot | Fichiers dans la copie V005 | Taille décompressée |
|---|---:|---:|
| V001 | 1269 | 97,013,607 octets |
| V002 | 1312 | 97,279,427 octets |

Les snapshots sont sous `01_SNAPSHOTS/V001/` et `01_SNAPSHOTS/V002/`. Les fichiers d'expérience n'ont pas été dédupliqués entre snapshots : ils sont conservés séparément pour préserver la comparaison historique des versions.

**Important sur V001 :** le ZIP anciennement émis sous le nom `sondes_ex7_livrables_complets_v001.zip` ne contenait que 979 entrées et omettait 312 fichiers par rapport au snapshot V001 complet du workspace. Pour éviter cette omission, V005 reprend le répertoire source V001 complet (1 290 fichiers avant le filtrage des sources EX6 hors périmètre), et non cet ancien ZIP incomplet.

## Suppléments postérieurs à V002

Le dossier `02_SUPPLEMENTS_POST_V002/EX7_V002_SUPPLEMENT/` conserve les fichiers du supplément d'origine, notamment les agrégats et résultats par graine des comparateurs MLP, les tables de folds OOF seuls, le timing d'extraction OOF des étages, l'audit des variantes récursives, le script d'agrégation et son journal.

## Récursion Orchestra Org — expérience de bout en bout

Les scripts, sorties brutes, métriques, livrables, journaux et checkpoints sont dans chacun des snapshots ; les comparaisons et compléments post-V002 sont dans le supplément.

### Scripts d'expérience (snapshot V002)
- `01_SNAPSHOTS/V002/sondes_ex7_v002__2026-10-31/src/run_orchestra_org_recursive.py`
- `01_SNAPSHOTS/V002/sondes_ex7_v002__2026-10-31/src/run_orchestra_org_oof.py`
- `01_SNAPSHOTS/V002/sondes_ex7_v002__2026-10-31/src/run_ex7_org_stage_oof.py`
- `01_SNAPSHOTS/V002/sondes_ex7_v002__2026-10-31/src/run_orchestra_org_ablations.py`
- `01_SNAPSHOTS/V002/sondes_ex7_v002__2026-10-31/src/run_orchestra_org_capacity_variants.py`
- `01_SNAPSHOTS/V002/sondes_ex7_v002__2026-10-31/src/run_orchestra_org_mlp_ge4x.py`
- `01_SNAPSHOTS/V002/sondes_ex7_v002__2026-10-31/src/run_orchestra_org_parallel_layers.py`
- `01_SNAPSHOTS/V002/sondes_ex7_v002__2026-10-31/src/profile_orchestra_org_parallel_layers.py`
- `01_SNAPSHOTS/V002/sondes_ex7_v002__2026-10-31/src/profile_orchestra_org_vectorization.py`
- `01_SNAPSHOTS/V002/sondes_ex7_v002__2026-10-31/src/org_oof_parallel_fold_worker.py`
- `01_SNAPSHOTS/V002/sondes_ex7_v002__2026-10-31/src/run_ex7_oof_2fold.py`
- `01_SNAPSHOTS/V002/sondes_ex7_v002__2026-10-31/src/run_ex7_oof_5fold.py`
- `01_SNAPSHOTS/V002/sondes_ex7_v002__2026-10-31/src/run_ex7_structural_compression_variants.py`
- `01_SNAPSHOTS/V002/sondes_ex7_v002__2026-10-31/src/run_ex7_light_correctors.py`
- `01_SNAPSHOTS/V002/sondes_ex7_v002__2026-10-31/src/run_ex7_distilled_and_base_only.py`
- `01_SNAPSHOTS/V002/sondes_ex7_v002__2026-10-31/src/export_and_profile_ex7.py`
- `01_SNAPSHOTS/V002/sondes_ex7_v002__2026-10-31/src/audit_ex7_recursive_and_variants_v002.py`
- `01_SNAPSHOTS/V002/sondes_ex7_v002__2026-10-31/src/build_additional_org_mlp_comparisons_v002.py`

### Comptage des artefacts dans V002

| Répertoire | Fichiers |
|---|---:|
| `src/` | 23 |
| `results/raw/` | 642 |
| `results/metrics/` | 61 |
| `results/models/` | 458 |
| `deliverables/` | 62 |
| `logs/` | 4 |
| `reports/` | 18 |
| Checkpoints PyTorch `.pt/.pth` | 458 |

### Fichiers d'agrégation / preuve à ouvrir

- `deliverables/EX7_ORCHESTRA_ORG_STATUS.json`
- `deliverables/EX7_ORCHESTRA_ORG_OOF_STATUS.json`
- `deliverables/EX7_ORCHESTRA_ORG_STAGE_OOF_STATUS.json`
- `deliverables/EX7_ORCHESTRA_ORG_CAPACITY_STATUS.json`
- `deliverables/EX7_RECURSIVE_ORG_AUDIT.json`
- `deliverables/EX7_RECURSIVE_VARIANTS_AUDIT.json`
- `deliverables/EX7_ORCHESTRA_ORG_OOF_MLP_COMPARISONS_AGGREGATES.csv`
- `deliverables/EX7_ORCHESTRA_ORG_STAGE_OOF_MLP_COMPARISONS_AGGREGATES.csv`
- `deliverables/EX7_ORCHESTRA_ORG_ABLATIONS_MLP_COMPARISONS_AGGREGATES.csv`
- `deliverables/EX7_ORCHESTRA_ORG_CAPACITY_MLP_COMPARISONS_AGGREGATES.csv`
- `deliverables/EX7_STRUCTURAL_COMPRESSION_MLP_COMPARISONS_AGGREGATES.csv`
- `results/raw/` : prédictions, résultats et diagnostics par exécution/graine/fold
- `results/models/` : checkpoints racine, folds OOF, correcteurs, variantes et MLP appariés


## Campagnes EX7 : décompte vérifié dans les fichiers de statut V002

| Campagne | Attendu | Achevé |
|---|---:|---:|
| Récursion Orchestra Org racine (7×5) | 5 | 5 |
| OOF récursif 3-fold (avec 15 fits de fold) | 5 graines | 5 graines |
| Correcteurs OOF de sorties d'étages | 10 | 10 |
| Ablations causales | 30 | 30 |
| Capacité/profondeur (incluant `centers_k4`) | 25 | 25 |
| Compression structurelle | 60 | 60 |
| Couches indépendantes/parallèles | 5 | 5 |
| Correcteurs légers | 50 | 50 |
| Distillation et base-only | 20 | 20 |
| Cross-fitting 2-fold | 10 | 10 |
| Cross-fitting 5-fold | 10 | 10 |

Les fichiers de statut confirment que ces campagnes sont achevées et que le test externe n'a pas été ouvert (`test_opened: false`). Pour le détail de la récursion, voir `04_REPORTS_AND_AUDITS/RECURSION_ORCHESTRA_ORG_END_TO_END_V005.md`.

## Delta V001 → V002

Voir `05_PROVENANCE/V001_V002_DELTA.json` pour les chemins ajoutés/supprimés/modifiés. V002 ajoute notamment les comparateurs MLP par graine et agrégés, l'audit récursif révisé et les rapports de reprise. V001 est conservé comme snapshot distinct, pas remplacé par V002.

## Outils

`03_REPRODUCTION_AND_AUDIT_TOOLS/` contient les scripts d'audit et d'agrégation ajoutés hors snapshots, ainsi que le script de reconstruction des comparateurs MLP post-V002 et le journal d'exécution.

## Intégrité

Les sommes SHA-256 de tous les fichiers du paquet (hors manifeste lui-même) sont dans `SHA256SUMS_V005.txt` à la racine et dans `05_PROVENANCE/FILE_MANIFEST_V005.csv`. Les manifestes internes de chaque snapshot filtré se trouvent sous son `checksums/`.
