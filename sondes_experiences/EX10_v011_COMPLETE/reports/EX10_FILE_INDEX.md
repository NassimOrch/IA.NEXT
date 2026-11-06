# EX10_v011 — index exhaustif des fichiers

Cet index décrit le contenu expérimental EX10_v011 uniquement. Chaque entrée du CSV comporte le chemin relatif, la taille, le SHA-256 et la catégorie.

- Fichiers de contenu indexés : **8104**
- Taille cumulée non compressée : **100,383,310 octets (95.73 MiB)**
- Les modèles, prédictions, métriques, historiques, configurations, scripts, journaux, rapports, données nécessaires et quarantaines sont inclus.
- Les holdouts déjà ouverts une seule fois sont livrés avec prédictions persistées, métriques et manifestes ; ne pas relancer les scripts de scoring.
- Les sources originales EX8 v010 et les cinq dépendances globales V009 ne sont incluses que sous forme de références minimales nécessaires à la traçabilité et à la réplication A0/B10/B11.
- Les tentatives abandonnées ou dont la provenance est insuffisante sont conservées sous les répertoires `quarantine`/`attempts` et ne sont pas mélangées aux agrégats principaux.
- Sont exclus uniquement les caches régénérables `.pytest_cache/`, `__pycache__/`, les fichiers `.pyc` et `.pyo`.
- `EX10_FILE_INDEX.csv`, ce document, `EX10_PACKAGE_MANIFEST.json` et `EX10_SHA256SUMS.txt` sont des métadonnées d’inventaire et sont gérés par leurs propres règles de checksum.

## Fichiers par catégorie

| Catégorie | Fichiers | Taille (MiB) |
|---|---:|---:|
| CNG_CNC_validation_and_training_artifacts | 2319 | 36.89 |
| classification_metrics | 97 | 0.48 |
| classification_predictions_and_histories | 160 | 6.58 |
| dataset_source_sms | 6 | 10.30 |
| datasets_cng_cnc | 262 | 1.54 |
| executed_and_audit_scripts | 44 | 0.35 |
| execution_logs | 29 | 0.20 |
| integrity_manifests_and_model_lock | 3 | 0.69 |
| invariant_tests | 1 | 0.00 |
| minimal_A0_reference_dependencies | 18 | 0.76 |
| model_checkpoints | 650 | 6.12 |
| one_shot_test_predictions_and_metrics | 3481 | 12.57 |
| pristine_EX8_protocol_reference | 37 | 0.19 |
| processed_tables_and_audits | 38 | 8.20 |
| protocol_and_input_data | 11 | 1.05 |
| quarantined_attempts | 893 | 8.27 |
| reports_and_theory_pdfs | 21 | 1.42 |
| run_configurations | 31 | 0.01 |
| theory_sources | 2 | 0.10 |
| workspace_documentation_and_other | 1 | 0.00 |

## Répertoires principaux

- `inputs/` : données CNG/CNC, domaine SMS, split Wisconsin de réplication, théorie et dépendances minimales documentées.
- `configs/` : configurations par run et essais mis en quarantaine.
- `src/` : scripts d’entraînement, reprise, scoring, audit, profiling et scripts historiques EX10 conservés.
- `results/models/` : checkpoints de classification ; `results/core/models/` : 550 checkpoints CNG/CNC.
- `results/raw/` et `results/core/raw/` : prédictions et historiques.
- `results/metrics/` et `results/core/metrics/` : métriques par run et summaries.
- `results/core_test/` : artefacts du scoring one-shot, sans réentraînement.
- `results/attempts/` et `results/core/quarantine*/` : tentatives et runners non autoritatifs archivés séparément.
- `reports/` : rapports complets, index, sources TeX et PDFs compilés.
- `checksums/` : lock pré-test, marqueur one-shot, manifestes et hashes.
