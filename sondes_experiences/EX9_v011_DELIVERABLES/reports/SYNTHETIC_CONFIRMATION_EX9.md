# EX9 v011 — résultats confirmatoires synthétiques (cohortes concentric2 et rotated_moons2)

## Statut et protocole

Les deux holdouts synthétiques ont été ouverts une seule fois le 2 novembre 2026 après gel de `MODEL_LOCK_MULTI_DOMAIN.json` (295 entrées SHA-256) et préflight réussi des 90 checkpoints. Le préflight a chargé tous les modèles avant que le générateur de test soit appelé. Les 90 modèles ont été scorés sur 1 200 observations par domaine : 45 runs par domaine, 90 runs au total. Aucun modèle, hyperparamètre ou architecture n’a été modifié après ouverture.

Le holdout `xor8` reste séparément compromis/non scoré à cause de l’échec de désérialisation antérieur ; il n’a pas été relancé. Les résultats ci-dessous sont une **confirmation synthétique**, pas une confirmation externe réelle.

## Résultats test

Les valeurs présentées sont les moyennes sur cinq seeds de modèle ; l’écart-type reflète la variabilité entre ces entraînements, pas entre cinq jeux de données.

| Domaine | Variante | Log-loss test | SD entre seeds | Accuracy | MLP apparié | MLP ≥4× | Candidate wins vs MLP / MLP ≥4× |
|---|---|---:|---:|---:|---:|---:|---:|
| concentric2 | B10 | 0.255830 | 0.032037 | 0.8433 | 0.063186 | 0.059463 | 0/5 ; 0/5 |
| concentric2 | B11 | 0.255024 | 0.029714 | 0.8433 | 0.064854 | 0.058597 | 0/5 ; 0/5 |
| concentric2 | A0 | 0.200912 | 0.059369 | 0.9228 | 0.059220 | 0.060707 | 0/5 ; 0/5 |
| rotated_moons2 | B10 | 0.256111 | 0.047964 | 0.8963 | 0.122245 | 0.121291 | 0/5 ; 0/5 |
| rotated_moons2 | B11 | 0.255320 | 0.054813 | 0.8940 | 0.122342 | 0.121378 | 0/5 ; 0/5 |
| rotated_moons2 | A0 | 0.232610 | 0.070749 | 0.9170 | 0.121618 | 0.121019 | 0/5 ; 0/5 |

## Différences appariées et bootstrap

Le delta est défini comme `log-loss(candidate) − log-loss(MLP)` ; une valeur positive favorise le MLP. L’intervalle est un bootstrap imbriqué (10 000 réplications) sur seeds de modèle et observations test, calculé à partir des prédictions sauvegardées. Il décrit cette partition test unique et ne mesure pas l’incertitude entre domaines.

| Domaine | Candidate vs | Delta moyen | IC bootstrap 95 % | Victoires candidate |
|---|---|---:|---:|---:|
| concentric2 | B10 vs MLP_MATCHED | 0.192644 | [0.159530 ; 0.228564] | 0/5 |
| concentric2 | B10 vs MLP_GE4X | 0.196368 | [0.162622 ; 0.233270] | 0/5 |
| concentric2 | B11 vs MLP_MATCHED | 0.190169 | [0.158599 ; 0.224615] | 0/5 |
| concentric2 | B11 vs MLP_GE4X | 0.196427 | [0.165213 ; 0.229867] | 0/5 |
| concentric2 | A0 vs MLP_MATCHED | 0.141692 | [0.096674 ; 0.193854] | 0/5 |
| concentric2 | A0 vs MLP_GE4X | 0.140205 | [0.095734 ; 0.191300] | 0/5 |
| rotated_moons2 | B10 vs MLP_MATCHED | 0.133866 | [0.090520 ; 0.173427] | 0/5 |
| rotated_moons2 | B10 vs MLP_GE4X | 0.134820 | [0.091715 ; 0.174542] | 0/5 |
| rotated_moons2 | B11 vs MLP_MATCHED | 0.132977 | [0.085133 ; 0.176441] | 0/5 |
| rotated_moons2 | B11 vs MLP_GE4X | 0.133942 | [0.085459 ; 0.177648] | 0/5 |
| rotated_moons2 | A0 vs MLP_MATCHED | 0.110992 | [0.053163 ; 0.169131] | 0/5 |
| rotated_moons2 | A0 vs MLP_GE4X | 0.111591 | [0.053700 ; 0.169174] | 0/5 |

Les douze intervalles sont entièrement positifs et les candidates gagnent 0/5 dans toutes les comparaisons. Le test exact bilatéral des signes sur cinq différences par seed a un plancher de p=0,0625 ; il ne constitue pas une preuve statistique forte à lui seul. L’évidence est surtout le grand écart descriptif et la cohérence sur deux générations synthétiques différentes.

## Paramètres et ressources

Le nombre de paramètres `P_total` est resté celui du pré-test et le ratio des MLP ≥4× est garanti run par run. Les profils de latence et de temps d’entraînement sont consignés dans `MULTI_DOMAIN_SYNTH_DEV_REPORT.md` ; les sondes y étaient généralement 12–22× plus lentes que leurs MLP appariés en p50 batch 1 CPU. Les mesures de latence sont des mesures d’inférence de développement, pas des nouveaux réglages test.

FLOPs/MAC complets, mémoire RSS peak isolée par modèle, énergie et consommation GPU n’ont pas été mesurés. Les seuls proxies MAC sont des bornes structurelles incomplètes (exponentielles RBF, noyaux distance et coordination partiellement omis) et ne justifient aucun verdict d’économie de calcul.

## Audit des artefacts test

- `results/processed/MULTI_DOMAIN_TEST_METRIC_AUDIT.json` : PASS 90/90 ; les métriques recalculées depuis les labels et prédictions persistés correspondent exactement aux métriques enregistrées.
- Aucun générateur de données test n’a été rappelé lors de cet audit ; aucun modèle n’a été réexécuté.
- `SEALED_TEST_OPENED_MULTI_DOMAIN.json` : `SCORED`, 90 modèles ; hashes des fichiers de prédictions enregistrés.
- `results/raw/concentric2_MULTI_DOMAIN_TEST_PREDICTIONS.npz` et `rotated_moons2_MULTI_DOMAIN_TEST_PREDICTIONS.npz` conservent les probabilités et labels utilisés.
- Les résultats sont rapportés sans modification post-test des modèles.

## Verdict

**B10, B11 et A0 ne battent pas les MLP sur ces deux holdouts synthétiques.** Les MLP sont meilleurs en log-loss et en exactitude, malgré des tailles proches (MLP apparié) ou ≥4× supérieures (MLP_GE4X). Les sondes conservent donc une compression de paramètres face au grand MLP, mais sans qualité équivalente et avec une forte pénalité de latence CPU.

Ce résultat ne contredit pas arithmétiquement les résultats EX8 Wisconsin ; il montre qu’ils ne se généralisent pas aux deux familles synthétiques testées. Il ne permet pas d’exclure une spécialisation utile dans d’autres domaines, mais interdit toute revendication de supériorité générale. Une validation réelle, extérieure et vierge reste nécessaire.

## Fichiers

- Lock : `MODEL_LOCK_MULTI_DOMAIN.json`.
- Evaluateur one-shot : `src/open_score_multi_synth.py`.
- Audit métrique post-score : `src/audit_multi_domain_test_metrics.py`.
- Résumé numérique : `results/processed/MULTI_DOMAIN_TEST_AGGREGATES.json`.
- Audit : `results/processed/MULTI_DOMAIN_TEST_METRIC_AUDIT.json`.
- JSON détaillés : `results/processed/CONCENTRIC2_TEST_METRICS.json`, `ROTATED_MOONS2_TEST_METRICS.json`.
