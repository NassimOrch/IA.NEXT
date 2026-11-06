# REPLICA-U v003 — rapport de clôture exploratoire

**Statut : 65/65 runs terminés (13 datasets × 5 graines).** Tous sont `COMPLETED_VALIDATION_ONLY`. Cette campagne reste **exploratoire et non confirmatoire** : le code final v003 ne réentraîne pas le backbone/teacher sur tout le train extérieur après la sélection interne des durées. Le test scellé n’a pas été ouvert.

Audit : le script `src/evaluation/audit_replica_artifacts_v001.py` a réconcilié les rapports, logits, métriques recalculées, checkpoints, configurations, OOF, propriétaires des folds, hashes et GE4X. Tous les runs scientifiques passent. `src/evaluation/summarize_replica_v003.py` confirme 65 IDs uniques et aucune anomalie. Le run supplémentaire German Credit v002 est conservé séparément et n’entre pas dans les 65.

Les valeurs ci-dessous sont des **moyennes de validation** sur cinq graines, non des scores de test. L’écart-type inter-graines est fourni dans le CSV compagnon.

| Dataset | Backbone | Teacher | Student 64/32 | Student 32/16 | MLP apparié | MLP GE4X | Student64 gagne vs MLP apparié |
|---|---:|---:|---:|---:|---:|---:|---:|
| dataset_31_credit-g | 0.52576 | 0.55469 | 0.50926 | 0.51217 | 0.50990 | 0.51169 | 2/5 |
| dataset_44_spambase | 0.19215 | 0.19533 | 0.16825 | 0.17872 | 0.17863 | 0.18295 | 3/5 |
| dataset_50_tic-tac-toe | 0.08630 | 0.10631 | 0.07167 | 0.06937 | 0.05050 | 0.05162 | 1/5 |
| gina_agnostic | 0.26757 | 0.32882 | 0.26840 | 0.27513 | 0.24437 | 0.25830 | 0/5 |
| kc1 | 0.36184 | 0.36758 | 0.34547 | 0.34849 | 0.34876 | 0.34972 | 3/5 |
| kc2 | 0.38412 | 0.41633 | 0.36638 | 0.36359 | 0.36243 | 0.36242 | 2/5 |
| pc1 | 0.21609 | 0.22373 | 0.20389 | 0.20931 | 0.19787 | 0.19575 | 1/5 |
| pc3 | 0.27798 | 0.28812 | 0.26869 | 0.26937 | 0.26808 | 0.26539 | 3/5 |
| pc4 | 0.28648 | 0.31062 | 0.27418 | 0.25128 | 0.24876 | 0.25332 | 1/5 |
| php0FyS2T | 1.81219 | 1.76327 | 1.59346 | 1.72816 | 1.67007 | 1.53075 | 5/5 |
| php0iVrYT | 0.47164 | 0.47596 | 0.46373 | 0.46465 | 0.46389 | 0.46240 | 4/5 |
| php8Mz7BG | 0.31153 | 0.31274 | 0.30096 | 0.30709 | 0.30317 | 0.29421 | 4/5 |
| php9xWOpn | 0.02858 | 0.02234 | 0.00113 | 0.00323 | 0.00319 | 0.01054 | 4/5 |

## Interprétation

- Les performances du student sont très hétérogènes selon les domaines ; le résultat de Phoneme (php8Mz7BG) et de Steel Plates Fault (php9xWOpn) est nettement meilleur que sur One-Hundred-Plants-Shape (100 classes).
- Le student 64/32 ne dépasse le MLP apparié de façon systématique sur aucun domaine ; certains domaines le favorisent (Spambase, KC1, PC3, Phoneme) et d’autres favorisent fortement le MLP (Tic-Tac-Toe, GINA, PC1, PC4, One-Hundred-Plants).
- Le teacher n’est pas uniformément meilleur que le backbone. L’architecture teacher avec routeur ne doit donc pas être considérée comme gagnante par construction.
- Les métriques restent validation-only et l’écart de protocole de v003 interdit d’en faire une conclusion confirmatoire. REPLICA-U v004 est la campagne corrective prévue, avec refit final sur tout le train extérieur, C1, T0 et comparateurs appariés.

## Fichiers de résultats

- `results/metrics/replica_u_v003_summary.json`
- `results/metrics/replica_u_v003_summary.csv`
- `results/audits/replica_artifact_audit_v001.json`
- `logs/append_only/replica_u_campaign_v003.jsonl`
- `results/replica_u/`, `results/checkpoints/`, `results/predictions/`, `configs/replica/`
