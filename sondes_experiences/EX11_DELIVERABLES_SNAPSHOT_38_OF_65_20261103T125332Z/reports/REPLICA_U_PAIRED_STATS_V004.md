# Statistiques appariées REPLICA-U v004

Paires par graine, métriques de validation uniquement. Les intervalles t bilatéraux à 95 % ne sont pas corrigés pour comparaisons multiples et restent descriptifs (n faible). Aucun holdout tabulaire scellé n’est consulté.

| Dataset | Comparaison | n | Moyenne Δ / ratio | IC 95 % | Victoires first<second |
|---|---|---:|---:|---:|---:|
| dataset_31_credit-g | student64_minus_matched64 | 5 | 0.00334 | [-0.01419; 0.02086] | 1/5 |
| dataset_31_credit-g | student64_minus_backbone | 5 | -0.01187 | [-0.04050; 0.01676] | 3/5 |
| dataset_31_credit-g | teacher_minus_backbone | 5 | 0.03566 | [-0.00150; 0.07283] | 0/5 |
| dataset_31_credit-g | student64_time_ratio | 5 | 1.62872 | [1.02908; 2.22836] | 0/5 |
| dataset_44_spambase | student64_minus_matched64 | 5 | -0.00500 | [-0.01667; 0.00667] | 3/5 |
| dataset_44_spambase | student64_minus_backbone | 5 | -0.02086 | [-0.03516; -0.00656] | 5/5 |
| dataset_44_spambase | teacher_minus_backbone | 5 | -0.00210 | [-0.01472; 0.01053] | 3/5 |
| dataset_44_spambase | student64_time_ratio | 5 | 3.63214 | [0.29589; 6.96840] | 0/5 |
| dataset_50_tic-tac-toe | student64_minus_matched64 | 5 | 0.01626 | [0.00437; 0.02815] | 0/5 |
| dataset_50_tic-tac-toe | student64_minus_backbone | 5 | -0.01870 | [-0.06022; 0.02283] | 4/5 |
| dataset_50_tic-tac-toe | teacher_minus_backbone | 5 | -0.00212 | [-0.02745; 0.02321] | 3/5 |
| dataset_50_tic-tac-toe | student64_time_ratio | 5 | 1.35766 | [0.87923; 1.83610] | 0/5 |
| gina_agnostic | student64_minus_matched64 | 5 | 0.01147 | [-0.01347; 0.03641] | 2/5 |
| gina_agnostic | student64_minus_backbone | 5 | 0.00193 | [-0.03412; 0.03798] | 3/5 |
| gina_agnostic | teacher_minus_backbone | 5 | 0.06915 | [0.04238; 0.09592] | 0/5 |
| gina_agnostic | student64_time_ratio | 5 | 4.65037 | [-0.32203; 9.62277] | 0/5 |
| kc1 | student64_minus_matched64 | 5 | 0.00231 | [-0.00565; 0.01026] | 2/5 |
| kc1 | student64_minus_backbone | 5 | -0.01898 | [-0.03878; 0.00082] | 4/5 |
| kc1 | teacher_minus_backbone | 5 | 0.00072 | [-0.01590; 0.01733] | 3/5 |
| kc1 | student64_time_ratio | 5 | 1.57300 | [0.33376; 2.81224] | 0/5 |
| kc2 | student64_minus_matched64 | 5 | 0.00221 | [-0.00488; 0.00929] | 2/5 |
| kc2 | student64_minus_backbone | 5 | -0.04493 | [-0.13613; 0.04626] | 4/5 |
| kc2 | teacher_minus_backbone | 5 | 0.00993 | [-0.01119; 0.03105] | 1/5 |
| kc2 | student64_time_ratio | 5 | 1.05591 | [0.71769; 1.39414] | 0/5 |
| pc1 | student64_minus_matched64 | 5 | 0.00612 | [-0.01088; 0.02312] | 2/5 |
| pc1 | student64_minus_backbone | 5 | 0.00379 | [-0.01292; 0.02050] | 1/5 |
| pc1 | teacher_minus_backbone | 5 | 0.01061 | [-0.01045; 0.03166] | 1/5 |
| pc1 | student64_time_ratio | 5 | 1.61041 | [-0.13357; 3.35439] | 0/5 |
| pc3 | student64_minus_matched64 | 2 | 0.02089 | [-0.17364; 0.21542] | 0/2 |
| pc3 | student64_minus_backbone | 2 | -0.02012 | [-0.10420; 0.06396] | 2/2 |
| pc3 | teacher_minus_backbone | 2 | 0.00433 | [-0.08894; 0.09760] | 1/2 |
| pc3 | student64_time_ratio | 2 | 0.94298 | [-1.96878; 3.85473] | 0/2 |

Pour les trois premières comparaisons, une différence négative favorise le premier modèle en log-loss. Pour `student64_time_ratio`, un ratio inférieur à 1 favorise le student en temps d’entraînement. Un IC qui contient 0 (ou un ratio qui contient 1) ne permet pas de conclure à un avantage stable.
