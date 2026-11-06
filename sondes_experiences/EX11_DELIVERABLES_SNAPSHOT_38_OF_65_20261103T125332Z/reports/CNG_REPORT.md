# Rapport CNG — EX11

## Formalisme
AdaptiveRBF avec représentation `tanh(Wx+b)` de dimension latente 4, K=8 centres RBF, initialisation KMeans sur les seules représentations train. A1 (M=1), A2 (M=2/4/7, moyenne fixe), A3 (M=2/4/7, composeur linéaire appris). LOO doit comparer F (sondes gelées, composeur réappris) et R (système réduit réentraîné).

## Résultats effectivement disponibles

- v001 : 18 runs terminés (f1/f2, seed 1501), tous audités ; classés exploratoires car centres initiaux aléatoires.
- v004 : 0 lignes au registre v004 à ce snapshot ; code confirmatoire dimensionne un MLP matched et un GE4X propre à chaque candidate, impose GE4X≥4× et partage l’ordre de mini-batches pour une comparaison appariée. Vérifier le registre avant qualification.
- Les campagnes confirmatoires CNG v004 et LOO v004 ne sont pas considérées terminées tant que toutes les tâches, graines et artefacts n’ont pas été audités.

### v001 — MAE validation (exploratoire)

| Tâche | Variante | MAE | Paramètres | Temps train (s) |
|---|---|---:|---:|---:|
| f1 | A1_M1 | 0.001716 | 57 | 17.46 |
| f1 | A2_M2 | 0.001941 | 114 | 34.28 |
| f1 | A2_M4 | 0.001408 | 228 | 41.76 |
| f1 | A2_M7 | 0.002097 | 399 | 26.78 |
| f1 | A3_M2 | 0.001231 | 117 | 29.46 |
| f1 | A3_M4 | 0.001008 | 233 | 22.79 |
| f1 | A3_M7 | 0.001450 | 407 | 37.01 |
| f1 | MLP_MATCHED | 0.000685 | 397 | 3.46 |
| f1 | MLP_GE4X | 0.000753 | 1678 | 4.62 |
| f2 | A1_M1 | 0.536823 | 61 | 11.83 |
| f2 | A2_M2 | 0.008153 | 122 | 27.78 |
| f2 | A2_M4 | 0.004152 | 244 | 42.11 |
| f2 | A2_M7 | 0.005049 | 427 | 78.14 |
| f2 | A3_M2 | 0.005331 | 125 | 36.13 |
| f2 | A3_M4 | 0.003482 | 249 | 70.56 |
| f2 | A3_M7 | 0.002367 | 435 | 79.40 |
| f2 | MLP_MATCHED | 0.001730 | 415 | 24.66 |
| f2 | MLP_GE4X | 0.002826 | 1801 | 10.30 |

## Verdict provisoire

Les 18 runs exploratoires montrent une qualité très dépendante de la fonction : par exemple A1-M1 sur f1 atteint une faible MAE, tandis que la même famille sur f2 est nettement plus difficile. Les MLP appariés restent généralement plus précis sur les deux tâches historiques, malgré leur nombre de paramètres plus élevé. Aucune conclusion confirmatoire n’est permise sans la campagne v004 et les deux conditions LOO.

## Artefacts

- `logs/append_only/cng_runs.jsonl` ; `logs/append_only/cng_runs_v004.jsonl` (si présent).
- `results/checkpoints/cng/`, `results/predictions/cng/`, `configs/cng/`.
- `results/audits/cng_artifact_audit_v001.json`.
