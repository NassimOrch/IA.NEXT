# Index du workspace EX9 v011

| Répertoire/fichier | Contenu |
|---|---|
| `prompt_ex9.json` | Prompt EX9 final, règle rouge et protocole complet |
| `MODEL_LOCK.json` | Photographie hashée des 45 modèles classification Rev2 avant tentative d'ouverture du test xor8 |
| `MODEL_LOCK_MULTI_DOMAIN.json` | Snapshot pré-test de 295 hashes pour 90 modèles sur deux domaines synthétiques ; 294/295 correspondent en post-test, exception rapport documentée |
| `reports/PROMPT_EX9_AUDIT_LOCK_EXCEPTION.md` et `results/processed/MULTI_DOMAIN_LOCK_POSTTEST_AUDIT.json` | Justification et contrôle machine-readable de l'unique divergence documentaire post-gel |
| `SEALED_TEST_OPENED_MULTI_DOMAIN.json` | Trace de scoring unique des tests synthétiques concentric2/rotated_moons2 |
| `SEALED_TEST_OPENED.json`, `SEALED_TEST_FAILURE.json` | Trace de l'ouverture avortée ; test consommé/non scoré |
| `inputs/PRE_REGISTRATION_EX9.md`, `inputs/PRE_REGISTRATION_EX9_REV2.md` | Pré-enregistrements et correctifs normatifs |
| `inputs/PRE_REGISTRATION_MULTI_DOMAIN_DEV.md`, `inputs/MULTI_DOMAIN_DEV_LOCK.json` | Pré-enregistrement additionnel et lock de génération/validation de développement |
| `inputs/AUDIT_SOURCES_EX9.md` | Audit des sources historiques et prompts antérieurs |
| `inputs/source_provenance_manifest.json` | Provenance, tailles et hashes de fichiers source (aucune copie des sources) |
| `inputs/source_tree_inventory_addendum.json` | Hash des arbres EX3–EX8/source et hash de l'archive principale |
| `inputs/th_sondes_core_test_1.tex` | Théorie source enrichie par les corrections d'expérience CNG/CNC |
| `configs/` | Configurations des 45 runs principaux, 35 ablations B10 et 9 pilotes CNG/CNC |
| `src/classification_models.py` | Implémentation Rev2 B10/B11/A0 et MLP comparateurs |
| `src/core_pilot.py` | Implémentation des pilotes CNG/CNC |
| `src/b10_ablation_study.py` | Script exact des 35 ablations B10 table-only |
| `src/audit_classification.py` | Recalcul des métriques validation des 45 runs principaux |
| `src/audit_checkpoint_deserialization.py` | Audit de chargement des 45 checkpoints principaux |
| `src/audit_b10_ablations.py` | Recalcul indépendant des checkpoints et prédictions des 35 ablations |
| `src/audit_core_pilot.py` | Recalcul indépendant des neuf pilotes CNG/CNC |
| `src/multi_domain_dev.py` | Driver pour les deux cohortes synthétiques additionnelles ; sans génération test |
| `src/audit_multi_domain.py` | Audit indépendant validation des 90 runs multi-domaines |
| `src/open_score_multi_synth.py` | Evaluateur one-shot des deux tests synthétiques ; déjà exécuté, ne pas relancer |
| `src/audit_multi_domain_test_metrics.py` | Audit post-score des métriques depuis predictions persistées, sans nouvel appel modèle/générateur |
| `src/freeze_classification.py` | Script de gel et contrôle des hashes pré-test |
| `src/score_sealed_test.py` | Tentative d'ouverture unique, échouée avant prédiction ; à ne plus exécuter |
| `src/score_sealed_test_v2_UNEXECUTED.py` | Correctif de désérialisation non exécuté ; refuse l'ancien holdout consommé |
| `results/models/` | 45 checkpoints et JSON Rev2, plus quarantaine Rev1 |
| `results/raw/` | Artefacts intermédiaires/quarantaines ; aucun score test |
| `results/ablations/b10_table/` | 35 JSON et checkpoints de tables B10 ablatées |
| `results/multi_domain/` | 90 runs B10/B11/A0 + MLP apparié/GE4X sur concentric2/rotated_moons2, JSON/checkpoints |
| `results/core_pilot/` | 9 JSON/checkpoints pilotes CNG/CNC et deux synthèses |
| `results/processed/` | Agrégats et audits recalculables, y compris B10, CNG/CNC, multi-domaines et métriques test |
| `VARIANT_REGISTRY.csv` | Registre initial gelé des runs principaux et tentatives Rev1 |
| `VARIANT_REGISTRY_APPENDIX.csv` | Reclassification/quarantaine des premières tentatives |
| `VARIANT_REGISTRY_B10_ABLATIONS.csv` | Registre complémentaire des 35 ablations B10, sans modifier le registre gelé initial |
| `VARIANT_REGISTRY_MULTI_DOMAIN.csv` | Registre consolidé de 90 runs, deux domaines, candidats et comparateurs |
| `reports/` | Audit prompt, catalogue EX8, matrice de preuves, résultats, limitations et rapport TeX/PDF |
| `logs/` | Environnement, journal JSONL append-only et journal de compilation TeX |
| `tests/` | Tests de cohérence et d'intégrité de livraison |
| `checksums/SHA256SUMS.txt` | SHA-256 de tous les fichiers livrés, sauf ce manifeste lui-même |
| `deliverables/` | Synthèses par branche et synthèse générale EX9 |

Les archives EX3–EX8 et les données historiques ne sont pas copiées dans EX9. Le holdout xor8 reste consommé/compromis et non scoré ; les deux autres holdouts synthétiques sont scorés une seule fois sous `MODEL_LOCK_MULTI_DOMAIN.json`. Le statut des expériences non exécutées et des branches bloquées figure dans `reports/EVIDENCE_MATRIX_EX9.md`.
