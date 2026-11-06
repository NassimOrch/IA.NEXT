# Rapport RETRO et optimiseurs EX5

## Calendriers et contrôles

La campagne v001 contient 12 bras × cinq graines (60 couples uniques). Le journal contient 61 lignes : le couple `retro_linear/1501` apparaît deux fois. Les deux entrées sont conservées ; les agrégats utilisent la version unique documentée. Les sondes ont `P_total=794`, et le comparateur MLP ge4x `P_total=3197`, ratio 4,02645×.

| Bras | Accuracy | Log-loss | Alpha retenu moyen | Beta local retenu moyen | Détail
|---|---:|---:|---:|---:|
| none | 0.96706 | 0.08199 | 0.000 | 1.000 | déclenchement 0/5 ; postactivation LL — |
| maturation | 0.96706 | 0.08199 | 0.000 | 1.000 | déclenchement 5/5 ; postactivation LL 0.16301 |
| retro_inverse | 0.96706 | 0.08199 | 0.000 | 1.000 | déclenchement 5/5 ; postactivation LL 0.14945 |
| retro_gamma_half | 0.96706 | 0.08199 | 0.000 | 1.000 | déclenchement 5/5 ; postactivation LL 0.15579 |
| retro_gamma_two | 0.96706 | 0.08199 | 0.000 | 1.000 | déclenchement 5/5 ; postactivation LL 0.14087 |
| immediate | 0.96706 | 0.08552 | 1.000 | 1.000 | déclenchement 0/5 ; postactivation LL 0.08552 |
| linear | 0.96941 | 0.08518 | 0.740 | 1.000 | déclenchement 0/5 ; postactivation LL 0.10522 |
| retro_linear | 0.96941 | 0.09538 | 0.947 | 0.053 | déclenchement 0/5 ; postactivation LL 0.09669 |
| retro_delta | 0.96941 | 0.09538 | 0.947 | 0.053 | déclenchement 3/5 ; postactivation LL 0.09669 |
| retro_grad | 0.96706 | 0.08513 | 0.773 | 0.227 | déclenchement 3/5 ; postactivation LL 0.09764 |
| local_only | 0.97176 | 0.10693 | 0.000 | 0.033 | déclenchement 0/5 ; postactivation LL — |
| factorial_A0B0 | 0.48000 | 0.69969 | 0.000 | 0.000 | déclenchement 0/5 ; postactivation LL — |

Le MLP ge4x de référence atteint accuracy moyenne 0,98118 et log-loss 0,05101. Le meilleur checkpoint `maturation`, `retro_inverse`, `retro_gamma_half` ou `retro_gamma_two` est pré-activation (`alpha=0`, `beta_local=1`) sur les cinq graines, bien que les déclencheurs soient atteints 5/5. Les meilleurs checkpoints strictement post-activation ont des log-loss moyennes respectives 0,16301, 0,14945, 0,15579 et 0,14087 : le calendrier a été exécuté, mais l'état post-activation n'a pas amélioré le minimum validation global. Il est faux de dire que ces quatre bras ne se sont pas déclenchés ; il faut dire qu'aucun checkpoint post-déclenchement ne les a rendus gagnants.

`retro_linear` et `retro_delta` sont des ramps dont le meilleur checkpoint conserve alpha≈0,9467 et beta_local≈0,0533 ; `retro_delta` ne déclenche son contrôleur sur plateau que sur 3/5 graines. `retro_grad` déclenche 3/5 et retient alpha≈0,7733/beta≈0,2267. La coordination immédiate/linéaire ne bat pas le contrôle en log-loss. La variante local-only monte l'accuracy à 0,97176 mais la log-loss se dégrade à 0,10693. Le contrôle `A0B0` est dégénéré et reste clairement identifié comme contrôle négatif, non comme candidat.

## Adam, gel et dégel

25 essais comparant `adam_keep`, `adam_nofreeze`, `adam_rebuild`, `adam_reset`, `adamw_keep`. Les 20 runs gelés passent les contrôles bitwise des paramètres, états optimiser et compteurs de pas. Le test unitaire contrôle que `optimizer.step()` à lr=0 ou gradients nuls modifie les moments/compteurs : le vrai gel doit sauter l'appel `step`, pas seulement mettre lr à zéro. Le meilleur checkpoint après dégel présente des log-loss environ 0,1046–0,1098 selon politique, contre ≈0,0852 pour l'état global sélectionné. Aucun reset/rebuild Adam ne renverse le résultat.

## Conclusion

Le bloc RETRO et Adam a été exécuté et audité ; son résultat est négatif au regard de l'objectif MLP. Les checkpoints pré- et post-activation restent disponibles. Les mesures énergie et VRAM portent les valeurs explicites `non_mesuree_instrument_absent` et `indisponible_CPU_only`.
