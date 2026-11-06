# Index des livrables — EX7 V002

**Version de livraison complète : `sondes_ex7_v002__2026-10-31`**.

Commencer par :

1. `reports/FINAL_REPORT_EX7_V002.md` — résultats et verdict général.
2. `reports/CONFORMITE_PROMPT_EX7_V002.md` — audit de chaque section A–L et de l'héritage EX6.
3. `reports/AUDIT_RECURSIVE_ORG_V002.md` — confirmation de l'implémentation et de l'exécution de l'architecture récursive originale.
4. `reports/COMPARATEURS_MLP_VARIANTES_EX7_V002.md` — comparaisons détaillées par variantes et MLP appariés.
5. `reports/AUDIT_REPRISE_V002.md` — différence archive V001/workspace et contrôle de non-répétition.

## Fichiers statistiques principaux

- `deliverables/EX7_STRUCTURAL_COMPRESSION_MLP_COMPARISONS_PER_SEED.csv` et `_AGGREGATES.csv` : six variantes structurelles × deux familles × cinq graines.
- `deliverables/EX7_ORCHESTRA_ORG_CAPACITY_MLP_COMPARISONS_PER_SEED.csv` et `_AGGREGATES.csv` : cinq architectures × cinq graines, incluant `centers_k4`.
- `deliverables/EX7_ORCHESTRA_ORG_OOF_MLP_COMPARISONS_PER_SEED.csv` et `_AGGREGATES.csv` : correcteurs OOF Org.
- `deliverables/EX7_ORCHESTRA_ORG_ABLATIONS_MLP_COMPARISONS_PER_SEED.csv` et `_AGGREGATES.csv` : 30 ablations comparées MLP.
- `deliverables/EX7_ORCHESTRA_ORG_STAGE_OOF_MLP_COMPARISONS_PER_SEED.csv` et `_AGGREGATES.csv` : 10 correcteurs de sorties d'étage comparés MLP.
- `deliverables/EX7_ORCHESTRA_ORG_STAGE_OOF_EXTRACTION_TIMING.csv` : coût additionnel mesuré pour relire les trois checkpoints de folds et recalculer les sept sorties d'étage, parité exacte.
- `deliverables/EX7_ORCHESTRA_ORG_BASE_MLP_COMPARISONS_PER_SEED.csv` et `_AGGREGATES.csv` : modèles récursifs racine comparés MLP.
- `deliverables/EX7_ORCHESTRA_ORG_ROOT_SEEDS_ONLY.csv`, `...OOF_FOLD_MODELS_ONLY.csv` et `...STATUS_RECONCILED_V002.json` : séparation claire entre cinq modèles racine et quinze fits fold.
- `deliverables/EX7_RECURSIVE_VARIANTS_AUDIT.json` : audit machine de chargement, hash, OOF coverage et métriques.

## Code et données

- `src/run_orchestra_org_recursive.py`, `src/run_orchestra_org_oof.py`, `src/run_ex7_org_stage_oof.py` : code original/OOF/étages.
- `src/audit_ex7_recursive_and_variants_v002.py` et `src/build_additional_org_mlp_comparisons_v002.py` : scripts de contrôle et de consolidation sans réentraînement.
- `results/raw/`, `results/models/`, `results/metrics/`, `logs/`, `inputs/`, `configs/` : données brutes, checkpoints, mesures, configurations et logs.

## Statut scientifique

La branche Org récursive est complète en termes d'implémentation et des runs programmés. La campagne ne démontre pas de réussite globale : pas de non-infériorité robuste sur tous les bras, pas de gain de temps end-to-end, mémoire/énergie non mesurées de façon fiable, pas de validation externe vierge. Verdict : **DÉVELOPPEMENT UNIQUEMENT — VALIDATION EXTERNE NON ÉTABLIE**.
