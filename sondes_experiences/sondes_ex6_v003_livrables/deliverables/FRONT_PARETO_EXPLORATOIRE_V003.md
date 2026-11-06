# Front de Pareto exploratoire — EX6 v003

Objectifs : minimiser P_total, log-loss, temps de fit et latence p50 batch-1 ; maximiser accuracy. Comparaison des six familles v003 et de leurs MLP-ge4x, moyennes sur cinq graines. Cette analyse est descriptive et non confirmatoire. Replica train-shard exclu faute de mesure d’inférence comparable dans ce bras.

| Modèle | P_total | Accuracy | Log-loss | Fit (s) | p50 batch-1 (ms) | Non dominé |
|---|---:|---:|---:|---:|---:|---|
| Emplica homogène | 6705 | 98.12% | 0.05968 | 2.428 | 1.632 | Oui |
| Emplica homogène / MLP-ge4x | 26825 | 98.82% | 0.04566 | 0.212 | 0.030 | Oui |
| Emplica spécialiste | 7340 | 97.88% | 0.04944 | 2.239 | 1.634 | Oui |
| Emplica spécialiste / MLP-ge4x | 29366 | 98.82% | 0.04891 | 0.226 | 0.030 | Oui |
| Orchestra gate externe | 7227 | 97.65% | 0.06299 | 2.379 | 1.713 | Non |
| Orchestra gate externe / MLP-ge4x | 28937 | 98.82% | 0.04691 | 0.231 | 0.029 | Oui |
| Orchestra sans communication | 6967 | 97.88% | 0.05995 | 2.180 | 1.690 | Oui |
| Orchestra sans communication / MLP-ge4x | 27881 | 98.82% | 0.04563 | 0.241 | 0.030 | Oui |
| Emplica OOF | 8295 | 98.59% | 0.03637 | 11.818 | 1.856 | Oui |
| Emplica OOF / MLP-ge4x | 33194 | 98.82% | 0.04675 | 0.263 | 0.031 | Non |
| Orchestra OOF | 8512 | 98.12% | 0.03982 | 10.677 | 1.871 | Oui |
| Orchestra OOF / MLP-ge4x | 34052 | 98.82% | 0.04733 | 0.260 | 0.027 | Oui |

## Interprétation

La non-domination ne signifie pas succès : plusieurs modèles restent sur le front parce qu’ils échangent la compacité ou la log-loss contre un coût de calcul supérieur. Les MLP-ge4x restent plus rapides, et les candidates restent plus compactes. Le front devra être recalculé sur des domaines indépendants et sous marges de qualité pré-enregistrées avant toute décision de déploiement.
