# Index des livrables EX6 — v003

**Verdict : INCOMPLET.** Consultez d’abord le rapport final et la matrice de conformité.

## Documents de décision
- `../reports_v3/FINAL_REPORT_EX6_V003.md` — synthèse complète et verdict.
- `../reports_v3/CONFORMITE_PROMPT_EX6_V003.md` — contrôle des 19 sections, PASS/PARTIEL.
- `../reports_v3/ETAT_EXECUTION_EX6_V003.json` — état machine-readable.
- `../reports_v3/AUDIT_INDEPENDANT_V003.json` — audit automatisé indépendant (`PASS_WITH_LIMITATIONS`).
- `../reports_v3/AUDIT_INTEGRITE_FINALE_V003.md` — CRC, hashes et contrôles de lecture.
- `../prompt_ex6.json` — prompt base EX6, révision 1.0.1.

## Expériences et métriques
- `../results_v3/metrics/EX6_V003_PER_SEED_COMPARISONS.csv` — métriques par graine.
- `../results_v3/metrics/EX6_V003_AGGREGATES.csv` — agrégats principaux.
- `../results_v3/metrics/EX6_V003_LATENCY_BATCHES.csv` — profils batchés et quantiles.
- `../results_v3/metrics/EX6_V003_PAIRED_BOOTSTRAP_POSTHOC.csv` — IC exploratoires post-hoc.
- `../results_v3/metrics/EX6_V003_CASCADE_DIAGNOSTICS.csv` — préfixes et cascade.
- `../results_v3/metrics/EX6_V003_ANALYTICAL_OPERATION_COUNTS.csv` — estimations analytiques, pas de compteurs matériels.
- `../results_v3/metrics/EX6_V003_PARETO_EXPLORATORY.csv` et `../reports_v3/FRONT_PARETO_EXPLORATOIRE_V003.md` — front de Pareto exploratoire (non confirmatoire).
- `../results_v3/raw/` — sorties brutes, prédictions, contrôles Replica et RETRO.
- `../results_v3/models/` et `../results_v3/deployment/` — checkpoints et exports.

## Reproduction / provenance
- `../src/` — scripts et snapshots de code exécuté.
- `../configs/continuation_preregistration_v003.json` — protocole de continuation pré-enregistré.
- `../configs/variant_selection_v003.json` — candidats et décisions de sélection.
- `../inputs/` — dataset autorisé, prompts et sources de référence.
- `../checksums/MANIFEST_SHA256_V003.txt` — empreintes des fichiers de la version, calculées après fermeture des livrables.
