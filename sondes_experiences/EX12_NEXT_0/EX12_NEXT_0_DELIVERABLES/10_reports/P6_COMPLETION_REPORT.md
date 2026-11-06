# EX12 — Rapport de clôture P6

Date de génération UTC : 2026-11-04T13:30:29.753286+00:00

## Décision

P6 : **PASS** — 24/24 contrôles passés. Le PASS concerne la complétude de la campagne et l’intégrité des artefacts ; il ne signifie pas que l’hypothèse de spécialisation générale est confirmée.

## Résumé vérifié

- 320/320 modèles candidats analysés.
- 10 240 unités modèle-centre et 34 560 lignes d’ablation développées sur les régimes de validation.
- 1 600/1 600 permutations group-preserving conformes. Maximum observé : output abs diff 9.54e-07, input-gradient abs diff 1.91e-06; chaque test a passé `torch.allclose(atol=rtol=1e-6)`.
- 1 440 paires de modèles uniques entre graines, 2 160 opérations de matching par groupe et 46 080 appariements centre-centre.
- 1 024 hypothèses de rôle : 549 stables, 9 utiles après Holm, 7 satisfont les deux.
- SHA-256 des checkpoints/données/prédictions/configurations/historiques/métriques et outputs P6 vérifiés : aucune divergence.
- Test et holdout non accédés.

## Livrables principaux

- `03_design/P6/P6_PREREGISTRATION.json` — protocole figé.
- `08_benchmarks/P6/P6_RUN_REGISTRY.jsonl` — registre append-only incluant l’interruption.
- `08_benchmarks/P6/P6_PERMUTATION_REGISTRY.jsonl` — registre de permutations.
- `08_benchmarks/P6/P6_ERROR_SIMILARITY_REANALYSIS.jsonl` — réanalyse et flags de variance nulle.
- `09_analysis/P6/P6_LOO_ABLATIONS.csv` — 34560 lignes LOO consolidées.
- `09_analysis/P6/P6_PERMUTATIONS.csv` — 1 600 permutations consolidées.
- `09_analysis/P6/P6_ERROR_SIMILARITY.csv` — 320 analyses consolidées.
- `09_analysis/P6/P6_CROSS_SEED_MATCHES.csv` — 46 080 appariements.
- `09_analysis/P6/P6_ROLE_STABILITY.csv` — 1 024 hypothèses.
- `09_analysis/P6/P6_SOURCE_ARTIFACT_INTEGRITY.csv` — 320 lignes de vérification par source P3.
- `09_analysis/P6/P6_INTEGRITY_AUDIT.json` — contrôle machine-readable.
- `10_reports/P6_FALSIFICATION_REPORT.md` — résultat scientifique détaillé.
- `10_reports/P6_SCRIPT_PROVENANCE_CAVEAT.md` — réserve de traçabilité v1.

## Limites

La spécialisation est rare et limitée à la tâche `g5_sin_mul_plus_square`. Les résultats ne démontrent pas une spécialisation générale ou sémantique. Le registre v1 a une réserve de liaison hash/script pour 123 runs, décrite séparément. Une tentative A01 interrompue est conservée comme telle et remplacée sans écrasement par A02. Aucun holdout n’a été consulté.

Signature d’exécution : assistant OpenAI — rapport généré automatiquement à partir des registres et artefacts EX12 présents. Cette signature identifie l’agent rédacteur, elle ne constitue pas une signature cryptographique d’une personne physique.
