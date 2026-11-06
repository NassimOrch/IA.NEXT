# Micro-MIXA : proportions, sélection, optimisation et PCA-Q

## Proportions fixe/adaptative à budget constant

L'unité fixe et l'unité adaptative de la première étude ont 182 coefficients de branche chacune. Les compositions 0/4, 1/3, 2/2, 3/1 et 4/0 conservent donc 788 paramètres totaux (avec 60 coefficients de prétraitement commun) à budget égal, cinq graines chacune. Les ratios coefficient-level sont issus du champ brut `rho_A=P_adaptive_branch_total/(P_adaptive_branch_total+P_fixed_branch_total)` ; `rho_F=1-rho_A`.

| Adaptatif/Fixe | rho_A exact (coefficients de branche) | Accuracy | Log-loss |
|---|---:|---:|---:|
| 0/4 | 0,00 | 96,71 % | 0,10060 |
| 1/3 | 0,25 | 96,71 % | 0,09600 |
| 2/2 | 0,50 | 97,18 % | 0,08647 |
| 3/1 | 0,75 | 97,41 % | 0,07848 |
| 4/0 | 1,00 | 97,65 % | 0,08239 |

Le 3/1 a la log-loss moyenne la plus basse de ce balayage, tandis que 4/0 obtient l'accuracy moyenne la plus élevée. Les valeurs exactes par graine sont dans `mixa_proportion_rho_exact.csv`. Gate global/conditionnel et ablations de gates ont ensuite été comparés ; le gate d'entrée améliore parfois la log-loss mais ajoute des paramètres et du calcul. Les MLP matched/ge4x sont appariés sur le P_total exact par candidate/graine.

## Optimisation et partage

Les branches partagent ensuite encodeurs/projections ou centres (v005), puis les bases PCA question-only (v006). Les résultats de validation n'atteignent pas les MLP ge4x :

| Candidate v005 | P_total sonde | Accuracy | Log-loss | Log-loss MLP ge4x | Latence p50 sonde / MLP (ms) |
|---|---:|---:|---:|---:|---:|
| Encodeur partagé d4/k8 égal | 540 | 96,94 % | 0,08377 | 0,05125 | 0,1607 / 0,01424 |
| Centres partagés d4/k8 égal | 476 | 97,41 % | 0,07542 | 0,05364 | 0,1618 / 0,01400 |
| Centres partagés d4/k8 gate entrée | 600 | 97,41 % | 0,07180 | 0,05146 | 0,1633 / 0,02221 |
| Centres partagés d4/k16 égal | 636 | 97,65 % | 0,07109 | 0,05031 | 0,1930 / 0,01390 |

## Nouveau bras PCA question-only v006

Six candidates, cinq graines (30 sondes), 30 comparaisons matched et 30 ge4x. Les MLP sont mutualisés entre candidates quand le P_total et la graine sont identiques : 40 MLP physiques distincts pour 60 liens de comparaison, sans perte d'appariement.

| Candidate | P_total | Accuracy | Log-loss | MLP ge4x log-loss | Temps pipeline sonde / MLP (s) | Latence p50 sonde / MLP (ms) |
|---|---:|---:|---:|---:|---:|---:|
| PCA_Q_A0F1_FIXED | 268 | 0.9529 | 0.12285 | 0.05509 | 14.126 / 0.332 | 0.0777 / 0.0140 |
| PCA_Q_A1F0_ADAPTIVE | 268 | 0.9529 | 0.13718 | 0.05509 | 0.919 / 0.332 | 0.0951 / 0.0140 |
| PCA_Q_A2F2_GLOBAL | 446 | 0.9529 | 0.13424 | 0.05131 | 0.762 / 0.263 | 0.1210 / 0.0141 |
| PCA_Q_A3F1_EQUAL | 442 | 0.9482 | 0.13986 | 0.05253 | 1.160 / 0.285 | 0.1844 / 0.0164 |
| PCA_Q_A3F1_GLOBAL | 446 | 0.9529 | 0.13494 | 0.05131 | 0.762 / 0.263 | 0.1266 / 0.0141 |
| PCA_Q_A3F1_INPUT | 462 | 0.9576 | 0.12796 | 0.05200 | 0.871 / 0.323 | 0.1562 / 0.0164 |


Le bras fixe-only prend environ 1 900 à 2 300 époques selon la graine ; il a été poursuivi avec patience et sauvegardes d'état, sans plafond artificiel. Il demeure moins performant en qualité probabiliste et plus coûteux en pipeline. Le PCA a été ajusté sur X_train uniquement ; les hashes PCA ont été recalculés indépendamment pour les cinq graines et correspondent aux manifestes, et les 30 checkpoints reprennent le même hash PCA dans leur métadonnée.

**Interprétation :** le partage et les projections PCA diminuent les MACs d'inférence et les bytes de déploiement, mais ne préservent pas la log-loss du MLP. Les coûts CPU du prétraitement et de l'apprentissage non supervisé annulent en partie les économies du réseau final.

## Addendum — v007, déploiement de la hiérarchie Q-only

Le candidat `QONLY_HYBRID_GLOBAL_GATE` déjà entraîné en v004 a été profilé en v007 sans réentraînement. TorchScript `trace` reproduit les logits exactement sur les cinq graines, mais la latence batch1 moyenne de la sonde tracée est 0,09597 ms contre 0,01239 ms pour le MLP tracé. `optimize_for_inference` dépasse la tolérance stricte 1e-6 et est écarté. Le noyau Numba v2 n'est paritaire pour la sonde que sur une graine sur cinq ; il est donc également rejeté comme backend admissible. Le code source, les cinq graines et hashes d'exports sont dans le dossier v007.
