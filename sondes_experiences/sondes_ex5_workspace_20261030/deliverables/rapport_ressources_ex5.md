# Ressources, Pareto et règle rouge

## Résultat global

Les paramètres sont tous conformes au ratio MLP ge4x : 437 liens audités, zéro ratio sous 4, minimum global `4,000735×`. Cela ne suffit pas à la réussite. La règle rouge demande la performance et chaque ressource mesurable au plus égale au MLP correspondant.

| Campagne | Dimension | Liens | Sonde ≤ MLP |
|---|---|---:|---:|
| V1/V2 Wisconsin | training wall | 235 | 16/235 (6.8%) |
| V1/V2 Wisconsin | forward MACs | 235 | 235/235 (100.0%) |
| V1/V2 Wisconsin | latency p50 batch 1 | 235 | 0/235 (0.0%) |
| V1/V2 Wisconsin | latency p95 batch 1 | 235 | 0/235 (0.0%) |
| V1/V2 Wisconsin | deployment bytes | 235 | 145/235 (61.7%) |
| V1/V2 Wisconsin | RSS delta | 235 | 153/235 (65.1%) |
| V3 external | training wall | 30 | 4/30 (13.3%) |
| V3 external | forward MACs | 30 | 30/30 (100.0%) |
| V3 external | latency p50 batch 1 | 30 | 0/30 (0.0%) |
| V3 external | latency p95 batch 1 | 30 | 0/30 (0.0%) |
| V3 external | deployment bytes | 30 | 30/30 (100.0%) |
| V3 external | RSS delta | 30 | 22/30 (73.3%) |
| v004 | training wall | 35 | 7/35 (20.0%) |
| v004 | forward MACs | 35 | 35/35 (100.0%) |
| v004 | latency p50 batch 1 | 35 | 5/35 (14.3%) |
| v004 | latency p95 batch 1 | 35 | 3/35 (8.6%) |
| v004 | deployment bytes | 35 | 35/35 (100.0%) |
| v004 | RSS delta | 35 | 29/35 (82.9%) |
| v005 | training wall | 20 | 0/20 (0.0%) |
| v005 | forward MACs | 20 | 20/20 (100.0%) |
| v005 | latency p50 batch 1 | 20 | 0/20 (0.0%) |
| v005 | latency p95 batch 1 | 20 | 0/20 (0.0%) |
| v005 | deployment bytes | 20 | 20/20 (100.0%) |
| v005 | RSS delta | 20 | 17/20 (85.0%) |
| v006 PCA-Q micro-MIXA | training wall | 30 | 1/30 (3.3%) |
| v006 PCA-Q micro-MIXA | forward MACs | 30 | 30/30 (100.0%) |
| v006 PCA-Q micro-MIXA | latency p50 batch 1 | 30 | 0/30 (0.0%) |
| v006 PCA-Q micro-MIXA | latency p95 batch 1 | 30 | 0/30 (0.0%) |
| v006 PCA-Q micro-MIXA | deployment bytes | 30 | 30/30 (100.0%) |
| v006 PCA-Q micro-MIXA | RSS peak delta | 30 | 9/30 (30.0%) |


## Interprétation

- Les MACs de forward sont inférieurs au MLP dans tous les ensembles comparés (tous les liens mesurés de V1/V2, v003, v004, v005 et v006). C'est le point de ressource favorable le plus robuste.
- La latence p50 et p95 batch=1 n'est jamais inférieure sur les campagnes principales, sauf quelques cas isolés dans v004 ; elle est généralement nettement plus élevée. La vectorisation v006 conserve une parité exacte des logits mais TorchScript demeure environ 6,45–8,42× plus lent que le MLP (selon la variante et le comparateur eager/TorchScript) selon les candidats.
- Le temps d'entraînement ne passe que sur une fraction des comparaisons. Les pipelines Q-only/alternés sont particulièrement coûteux parce que l'entraînement de toutes les branches et le pré-entraînement sont imputés au modèle complet.
- Les bytes de déploiement sont souvent inférieurs ; les snapshots RAM/RSS sont variables. Ces avantages ne compensent pas une latence ou un temps d'entraînement supérieurs.
- Les MACs d'entraînement complets ne sont pas mesurés de façon instrumentée ; FLOPs des opérations non linéaires ne sont pas exhaustivement capturés par le décompte analytique MAC. VRAM est indisponible (CPU-only), énergie non instrumentée. Ces champs sont `NON_MESURÉ`, jamais estimés comme des passes.

**Conclusion de la règle rouge : aucun candidat EX5 ne satisfait l'ensemble des dimensions ressources obligatoires mesurables et la non-infériorité prédictive.** Il n'existe pas de réussite rouge à déclarer. Les points Pareto (MAC/bytes contre qualité/latence) sont conservés pour recherche ultérieure, mais aucune candidate n'est promue en solution déployable.

## Addendum — correcteur OOF et profilage v007

Pour le système OOF à correcteur adaptatif, 10 comparaisons sur cinq graines (deux candidats OOF × cinq MLP réutilisés) donnent : entraînement pipeline 0/10 au plus égal au MLP, forward MACs 10/10 inférieurs, latence p50 et p95 batch 1 0/10 au plus égales, taille déployée 10/10 inférieure. L'économie MAC/stockage ne compense donc pas le coût de cross-fitting et la latence.

Pour v007, TorchScript trace passe la parité stricte 5/5 mais aucune des cinq latences p50/p95 batch1 ne devient inférieure au MLP. Les exports optimized-for-inference et Numba v2 ne sont pas admissibles comme résultats primaires quand la parité échoue. Numba v1 a été invalidé avant toute conclusion car son wrapper MLP ne reproduisait pas la primitive de référence.
