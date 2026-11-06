# Rapport micro-MIXA EX5 — proportions, portes et géométries

## Balayage de proportion à capacité constante

Le nombre total d'unités est fixé à quatre ; chaque unité fixe/adaptative a une capacité comptée identique dans ce design. Chaque candidate a `P_total=788` (scaler inclus), cinq graines.

| Composition | Accuracy moyenne | Log-loss moyenne | Temps d'entraînement moyen (s) |
|---|---:|---:|---:|
| A4_F0 | 0.97647 | 0.08239 | 0.477 |
| A3_F1 | 0.97412 | 0.07848 | 0.433 |
| A2_F2 | 0.97176 | 0.08647 | 0.448 |
| A1_F3 | 0.96706 | 0.09600 | 0.505 |
| A0_F4 | 0.96706 | 0.10060 | 13.627 |

Le mélange égal A3/F1 (75 % adaptatif/25 % fixe) est le meilleur en log-loss parmi les cinq ratios à gate égal (0,07848). A4/F0 a la meilleure accuracy de ce balayage (0,97647) et log-loss 0,08239. A0/F4 demande beaucoup plus d'entraînement (≈13,63 s moyenne) à cause de sa convergence lente. Le MLP ge4x au budget sonde 788 a 3164 paramètres (4,0152×), accuracy 0,98353 et log-loss 0,05093.

## Portes de mélange

Le gate conditionnel conjoint améliore le mélange A3/F1 à log-loss 0,06407 pour `P_total=912`, mais son MLP ge4x (3659 paramètres, 4,0121×) atteint 0,05149. Le gate-only après gel des branches a log-loss 0,07045. Le gate global ne fournit pas le gain de probabilité attendu.

## Géométrie et interaction gate×géométrie

Pour gate égal, les cinq géométries donnent des log-loss comprises entre 0,06913 (d4/k16) et 0,09430 (d4/k4). En gate conditionnel 75/25, la géométrie d4/k4 obtient le meilleur résultat de ce bras : accuracy 0,97412, log-loss 0,06187, `P_total=800`. Son MLP ge4x compte 3230 paramètres (4,0375×), accuracy 0,98588, log-loss 0,05076. Temps d'entraînement moyen : 0,583 s contre 0,297 s ; latence médiane batch 1 : 0,168 ms contre 0,01386 ms ; taille de déploiement : 11 989 contre 15 965 octets. La sonde est plus petite à déployer, mais n'égale ni les métriques, ni la latence, ni le temps.

`A3/F1 d4/k4 gate input` est donc la meilleure micro-MIXA simple selon la log-loss validation de cette exploration, pas une solution finale ni une candidate non inférieure. La recherche de géométrie est bornée aux cinq variantes pré-enregistrées/addendum, pas un optimum global.
