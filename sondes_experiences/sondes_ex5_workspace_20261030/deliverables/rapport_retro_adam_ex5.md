# RETRO, maturation et optimiseurs

## Protocole et résultats

Le bloc v001 comporte 12 familles de calendrier/contrôle sur cinq graines. Les checkpoints pré-activation, post-activation et sélectionnés sont distincts et conservés. Le rapport `ex4_retro_trace_audit.csv` dans v001 trace les dates de déclenchement, alpha/beta et les métriques ; `retro_factorial_summary.csv` fournit les agrégats.

| Contrôle | Accuracy validation moyenne | Log-loss validation moyenne | Alpha au checkpoint sélectionné | Beta local sélectionné |
|---|---:|---:|---:|---:|
| A0B1 / none | 96,71 % | 0,08199 | 0 | 1 |
| Maturation | 96,71 % | 0,08199 | 0 | 1 |
| RETRO inverse | 96,71 % | 0,08199 | 0 | 1 |
| Local seulement | 97,18 % | 0,10693 | 0 | ≈0,0333 |
| Coordination immédiate | 96,71 % | 0,08552 | 1 | 1 |
| Coordination linéaire | 96,94 % | 0,08518 | ≈0,74 | 1 |
| RETRO linéaire | 96,94 % | 0,09538 | ≈0,9467 | ≈0,0533 |
| RETRO delta | 96,94 % | 0,09538 | ≈0,9467 | ≈0,0533 |
| RETRO gradient | 96,71 % | 0,08513 | ≈0,7733 | ≈0,2267 |

Le point essentiel est que maturation et RETRO inverse ont déclenché le contrôleur sur les cinq graines, mais après le meilleur checkpoint de validation. Les checkpoints sélectionnés restent donc à `alpha=0, beta_local=1`. Ce résultat n'est pas un RETRO mature sélectionné ; les métriques post-activation sont conservées séparément et ne sont pas substituées au meilleur checkpoint.

Pour les snapshots post-activation, les variantes où `alpha=1` et `beta=0` (RETRO couplé) dégradent la log-loss moyenne, généralement vers 0,10–0,16. `retro_linear` et `retro_delta` ont une log-loss moyenne du meilleur snapshot strictement post-activation d’environ 0,09669. À distinguer de `linear` (sans préfixe `retro`), dont alpha moyen au checkpoint sélectionné est ≈0,74 avec beta=1 ; `retro_linear` et `retro_delta` sélectionnent tous deux alpha moyen ≈0,9467 et beta moyen ≈0,0533. Les variantes gamma/gradient ne démontrent pas de gain stable. Le protocole n'a pas choisi artificiellement un checkpoint post-activation défavorable ou favorable : les deux familles de checkpoints sont rapportées.

La campagne factorielle couvre les quatre cellules de base A0B0, A0B1, A1B0 et A1B1 ainsi que les contrôles immédiat, linéaire, gamma=1/2, gamma=2, gradient, delta, local-only et none. Les contrastes isolent l'effet de la coordination, la réduction locale et l'interaction ; l'analyse ne montre pas de bénéfice robuste du couplage dans la petite expérience Wisconsin.

## États Adam et gel

La v002 contient 25 essais sur cinq politiques et cinq graines : `adam_keep`, `adam_reset`, `adam_rebuild`, `adamw_keep`, `adam_nofreeze`. Les contrôles de gel strict passent pour les 20 cas applicables : hashes des paramètres, moments, compteurs de pas et état couvert inchangés. La définition stricte saute `optimizer.step()` durant le gel.

L'ablation sémantique illustre pourquoi `lr=0` n'est pas un gel d'état : paramètres constants mais moments/step modifiés. Un step avec gradient nul peut même modifier les poids par le momentum Adam. L'interpolation delta à zéro garde les poids constants mais modifie encore l'état de l'optimiseur. Seul le saut du step maintient simultanément paramètres et état inchangés parmi ces contrôles.

Les essais `best_thaw` sont généralement moins bons que le checkpoint global (exemple `adam_keep`, log-loss moyenne sélectionnée ≈0,085 contre ≈0,105 au meilleur checkpoint après dégel). Le gel/dégel n'a donc pas créé de gain mesuré dans ces conditions. La télémétrie des moments est suffisamment présente pour les checks de gel et certains snapshots, mais l'historique complet de tous les moments Adam à chaque époque n'est pas disponible pour chaque ancienne expérience ; cette partie demeure partielle.

## Addendum final — réconciliation des calendriers et doublon

La table dérivée `retro_post_activation_summary_ex5.csv` doit être privilégiée pour la lecture par famille et graine. Elle confirme que `maturation` et `retro_inverse` déclenchent 5/5, mais le checkpoint sélectionné garde alpha=0 et beta=1 ; les log-loss des meilleurs snapshots post-activation sont respectivement 0,16301 et 0,14945. La variante `linear` (sans préfixe `retro`) retient alpha moyen ≈0,74 et beta=1. `retro_linear` et `retro_delta` retiennent tous deux alpha moyen ≈0,9467 et beta moyen ≈0,0533 ; le déclenchement plateau est constaté 0/5 pour `retro_linear` et 3/5 pour `retro_delta`. Le meilleur snapshot post-activation de chacun est ≈0,09669. La ligne `retro_linear/1501` est dupliquée : même prédiction et même référence de checkpoint, temps incompatible ; les deux lignes brutes restent et le temps le plus élevé sert au coût conservateur. `retro_duplicate_timing_audit.csv` l'explicite.
