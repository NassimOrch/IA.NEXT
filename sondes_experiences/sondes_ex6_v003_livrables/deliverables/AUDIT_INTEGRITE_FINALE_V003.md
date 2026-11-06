# Audit final d’intégrité — EX6 v003

Date : 31 octobre 2026  
Statut : **PASS_WITH_LIMITATIONS**

## Sources
- `last_sources.zip` : 457,109,554 octets ; SHA-256 `5f7a86cb3875f97324f75c46e379b6639673dfe9cc265a173fa8749f1be0f8eb`. Contrôle `unzip -tq` passé.
- Les 5 ZIP imbriqués principaux et 12 ZIP internes du corpus sont PASS selon le manifeste source.
- Les archives originales et les versions v001/v002 sont conservées sans écrasement.

## Prompt et données
- Prompt EX6 JSON valide, 19 sections ; SHA-256 `72744213da2626174e63c45256a6e7a69c6de84c2b810d7a4a94e931c885237c`. Copies racine/version/inputs identiques.
- NPZ : SHA-256 `93f7a5f6ef8a5daa090bf83f4a2169a9857893f4aca4b700f7b74566b14be1da` ; lecture `allow_pickle=False` réussie ; train 341×30, validation 85×30, adaptation 57×30 ; aucune matrice ni label test dans ce NPZ.
- Limite : le loader sklearn source matérialise le dataset complet en mémoire. Domaine de développement historique uniquement.

## Parsing des fichiers
- JSON : 335 fichiers, zéro erreur de parsing.
- JSONL : 6 fichiers, 55 lignes, zéro erreur de parsing par ligne.
- CSV : 29 fichiers, tous lisibles ; 1600 lignes de données au total.

| CSV | Lignes |
|---|---:|
| `deliverables/DECISION_MATRIX_EX6.csv` | 4 |
| `deliverables/EX6_V003_AGGREGATES.csv` | 9 |
| `deliverables/EX6_V003_LATENCY_BATCHES.csv` | 240 |
| `deliverables/EX6_V003_PAIRED_BOOTSTRAP_POSTHOC.csv` | 9 |
| `deliverables/EX6_V003_PARETO_EXPLORATORY.csv` | 12 |
| `deliverables/EX6_V003_PER_SEED_COMPARISONS.csv` | 45 |
| `deliverables/audit_metrics_recalculated.csv` | 62 |
| `deliverables/audit_parameter_counts.csv` | 20 |
| `deliverables/deployment_export_sizes.csv` | 20 |
| `deliverables/parameter_decomposition.csv` | 4 |
| `deliverables/pareto_frontier_pilot.csv` | 8 |
| `deliverables/per_seed_comparison.csv` | 20 |
| `inputs/data_manifest/ex4_reference_partition_ledger_v009.csv` | 569 |
| `reports/DECISION_MATRIX_EX6.csv` | 4 |
| `results/metrics/audit_metrics_recalculated.csv` | 62 |
| `results/metrics/audit_parameter_counts.csv` | 20 |
| `results/metrics/deployment_export_sizes.csv` | 20 |
| `results/metrics/parameter_decomposition.csv` | 4 |
| `results/metrics/pareto_frontier_pilot.csv` | 8 |
| `results/metrics/per_seed_comparison.csv` | 20 |
| `results_v3/metrics/EX6_V003_AGGREGATES.csv` | 9 |
| `results_v3/metrics/EX6_V003_ANALYTICAL_OPERATION_COUNTS.csv` | 35 |
| `results_v3/metrics/EX6_V003_CASCADE_DIAGNOSTICS.csv` | 60 |
| `results_v3/metrics/EX6_V003_DEPLOYMENT_EXPORTS.csv` | 14 |
| `results_v3/metrics/EX6_V003_LATENCY_BATCHES.csv` | 240 |
| `results_v3/metrics/EX6_V003_PAIRED_BOOTSTRAP_POSTHOC.csv` | 9 |
| `results_v3/metrics/EX6_V003_PARETO_EXPLORATORY.csv` | 12 |
| `results_v3/metrics/EX6_V003_PER_SEED_COMPARISONS.csv` | 45 |
| `results_v3/metrics/EX6_V003_REPLICA_KERNEL_LATENCY.csv` | 16 |

## Modèles et métriques
- Audit indépendant automatisé : `PASS_WITH_LIMITATIONS`, aucune erreur déclarée.
- 20 runs stack, 10 runs OOF, 5 runs Replica train-shard achevés selon registres.
- 35 comptes de paramètres reconstruits depuis checkpoints ; aucun écart ; ratio MLP-ge4x/candidate minimal `4.0004699248`.
- 105 prédictions recalculées ; écart maximal des métriques `0.0`. Aucun checkpoint temporaire `*.pt.tmp` résiduel.

## Limites
Ces contrôles détectent les corruptions ZIP, erreurs de parsing, incohérences de hashes et divergences métriques ciblées. Ils ne prouvent pas l’absence absolue de toute altération, ni une isolation parfaite du test. Le statut scientifique reste **INCOMPLET**.
