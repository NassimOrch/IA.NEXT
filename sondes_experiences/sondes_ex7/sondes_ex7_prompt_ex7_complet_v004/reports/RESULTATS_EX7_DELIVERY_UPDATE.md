# Résultats EX7 — rapport consolidé

Tous les résultats ci-dessous sont sur le split historique Wisconsin de développement. Cinq graines appariées ; ils sont descriptifs, non confirmatoires.

## 1. Correcteurs allégés sur les logits OOF 3-fold existants

| Famille | Variante | P_total moyen | Accuracy | Log-loss | Fit correcteur (s) | Pipeline (s) |
|---|---|---:|---:|---:|---:|---:|
| emp_oof_corrector | affine_logit | 7,346 | 98.12% | 0.04647 | 0.182 | 10.97 |
| emp_oof_corrector | linear_context | 7,406 | 98.59% | 0.04631 | 0.222 | 11.01 |
| emp_oof_corrector | rbf_lite_1probe | 7,428 | 98.59% | 0.04303 | 0.211 | 11.01 |
| emp_oof_corrector | rbf_lite_2probe | 7,518 | 98.35% | 0.04249 | 0.265 | 11.07 |
| emp_oof_corrector | temp_bias | 7,343 | 98.35% | 0.04606 | 0.170 | 10.96 |
| orch_input_oof_corrector | affine_logit | 7,563 | 97.41% | 0.06613 | 0.179 | 9.91 |
| orch_input_oof_corrector | linear_context | 7,623 | 97.65% | 0.05177 | 0.263 | 10.00 |
| orch_input_oof_corrector | rbf_lite_1probe | 7,645 | 98.12% | 0.04843 | 0.397 | 10.14 |
| orch_input_oof_corrector | rbf_lite_2probe | 7,735 | 97.65% | 0.04999 | 0.407 | 10.15 |
| orch_input_oof_corrector | temp_bias | 7,560 | 97.41% | 0.06418 | 0.190 | 9.92 |

Référence Emplica OOF : accuracy 98,59 %, log-loss 0,03637. Référence Orchestra OOF : 98,12 %, log-loss 0,03982. Les correcteurs de substitution sont plus légers (3 à 178 paramètres entraînables), mais tous détériorent la log-loss par rapport au correcteur OOF original. Le RBF-Lite 1 probe est le meilleur compromis des variantes 3-fold, mais ne rejoint pas la référence. Le gain d'entraînement complet est faible car le temps OOF et le fit base dominent le pipeline.

## 2. Réduction OOF 3-fold → 2-fold avec correcteur RBF-Lite 1 probe

| Famille | OOF moyen 3f → 2f (s) | Réduction OOF | Pipeline complet 3f → 2f (s) | Réduction pipeline | Accuracy 2f | Log-loss 2f | Δ log-loss vs réf. | Δ accuracy vs réf. |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| emp_oof_corrector | 8.69 → 3.99 | 54.1% | 11.82 → 6.75 | 42.9% | 98.35% | 0.03801 | +0.00165 | -0.235 pp |
| orch_input_oof_corrector | 7.68 → 3.44 | 55.3% | 10.68 → 6.15 | 42.4% | 97.88% | 0.04344 | +0.00362 | -0.235 pp |

Le temps du pipeline 2-fold ci-dessus est reconstruit : initialisation base + génération OOF + fit base complet + initialisation correcteur + fit correcteur. Le champ `candidate_training_total_seconds` du JSON brut 2-fold est une somme intermédiaire qui n'inclut pas toutes ces initialisations ; ne pas l'utiliser comme total final. Les formules complètes sont dans `EX7_OOF_2FOLD_RESOURCE_AUDIT.csv`.

### Contrôle par graine — RBF-Lite 2-fold

**emp_oof_corrector** : Δ log-loss appariés = -0.00222, +0.00472, -0.00020, +0.01180, -0.00586 ; variation relative = -6.6%, +13.6%, -0.5%, +33.9%, -14.4% ; Δ accuracy = +0.000 pp, -1.176 pp, +0.000 pp, +0.000 pp, +0.000 pp.
**orch_input_oof_corrector** : Δ log-loss appariés = +0.02280, -0.01334, +0.00901, +0.02124, -0.02162 ; variation relative = +61.4%, -31.1%, +28.0%, +46.4%, -52.7% ; Δ accuracy = -1.176 pp, +2.353 pp, -1.176 pp, -2.353 pp, +1.176 pp.

Interprétation : Emplica 2-fold RBF-Lite a une moyenne de log-loss à +4,5 % de la référence, mais une graine dépasse largement cette dégradation et une graine dépasse la limite descriptive accuracy de −0,5 pp ; la non-infériorité par graine n'est donc **pas établie**. Orchestra 2-fold est à environ +9,1 % de log-loss en moyenne et échoue la marge descriptive de 5 %.

## 3. Original Emplica Orchestra Org récursive

| Variante | P_total | Accuracy moyenne | Log-loss moyenne | OOF génération moyenne (s) | Fit correcteur (s) |
|---|---:|---:|---:|---:|---:|
| Org base cascade (sans correcteur) | 6 712 | 98.35% | 0.06187 | — | — |
| Org OOF + temp_bias | 6715 | 98.35% | 0.06195 | 15.77 | 0.172 |
| Org OOF + linear_context | 6778 | 98.12% | 0.05765 | 15.77 | 0.231 |
| Org OOF + rbf_lite_1probe | 6800 | 97.88% | 0.05535 | 15.77 | 0.292 |

Ablation couches indépendantes : 97.65% accuracy, 0.05258 log-loss, 7.60 s. Elle retire la dépendance en cascade mais ne donne pas de gain CPU démontré ; l'ablation améliore la log-loss contre la cascade Org base, mais baisse l'accuracy.

### Ablations causales des deux niveaux de coordination (30/30 exécutions)

| Configuration Org | Accuracy moyenne | Log-loss moyenne | Fit moyen (s) |
|---|---:|---:|---:|
| inner_coord_only | 98.35% | 0.06360 | 3.23 |
| outer_coord_only | **98.59%** | 0.06013 | 3.43 |
| static_global_coord | 98.35% | 0.05991 | 4.55 |
| local_only | 97.65% | 0.07168 | 5.01 |
| global_gates_no_lr_mod | 97.65% | 0.07271 | 3.89 |
| uniform_gates_with_lr_mod | 98.35% | 0.06233 | 3.79 |

L'adaptation externe seule est le meilleur bras de cette ablation en accuracy, mais sa log-loss reste nettement supérieure aux références Emplica/Orchestra OOF EX6. L'activation simultanée de toutes les coordinations n'est donc pas démontrée optimale ; les ablations isolent des effets, pas encore une combinaison gagnante. Détails par graine : `EX7_ORCHESTRA_ORG_ABLATIONS_PER_SEED.csv`.


## 4. Parallélisation et vectorisation

- Parité boucle vs vectorisation : écart absolu maximal de sortie mesuré `4,768e-7`, inférieur à la tolérance `1e-6`.
- Vectorisation CPU : résultat dépendant du batch ; un seul cas favorable clair (batch 16, 1 thread), batch 1 et 256 plus lents, batch 64 similaire ou légèrement plus lent. Aucun gain universel.
- Parallélisme folds OOF : même poids/checkpoints bit-identiques (écart d'état 0), mais 3 processus simultanés `27,34 s` vs `16,11 s` séquentiel cumulé, soit 1,70× plus lent.
- Parallélisme des couches avec 3 threads : p50 plus lent que séquentiel vectorisé à chacun des batchs testés (batch 1 `7,67 ms` vs `1,92 ms`; 16 `8,09` vs `2,37`; 64 `9,00` vs `2,95`; 256 `9,18` vs `4,22`).

## 5. Latence batch et p99

Les mesures EX7 p50/p95/p99 des variantes 3-fold se trouvent dans `EX7_LIGHT_CORRECTORS_LONG.csv`. Pour le 2-fold RBF-Lite, `EX7_OOF_2FOLD_LATENCY_BY_SEED.csv` et `EX7_OOF_2FOLD_LATENCY_AGGREGATES.csv` fournissent les comparaisons par batch. Attention : références historiques = 200 répétitions, candidats 2-fold = 40 répétitions ; ces agrégats sont descriptifs, pas une comparaison instrumentale strictement homogène. Ils ne montrent pas d'amélioration stable de l'inférence : la moyenne p50 du candidat est plus lente pour chaque batch et chaque famille (dégradation allant d'environ +1,9 % à +19,4 %). Les p99 sont bruités et varient selon le batch ; ils ne permettent pas de réclamer une réduction fiable de latence de queue.

## 6. Paramètres et ressources

Le ratio 4× reste atteint dans les comparaisons de référence pour les variantes OOF d'origine. Les candidats 2-fold RBF-Lite restent également au-dessus de 4× avec le MLP-ge4x historique : les comptes détaillés et ratios sont dans `EX7_OOF_2FOLD_LATENCY_BY_SEED.csv`. Cela ne signifie pas une économie de calcul contre le MLP : les pipelines de probes restent environ 6–7 secondes, soit environ 25,7× (Emplica) et 23,7× (Orchestra) les temps MLP-ge4x historiques autour de 0,26 s. Énergie, mémoire activations, consommation DRAM et peak RSS isolé : NON MESURÉS / NON FIABLES.

## 7. Verdict scientifique

**Aucun succès global.** Le passage 3→2 folds donne un vrai gain partiel de coût de formation OOF, avec qualité proche pour Emplica mais non-infériorité stricte non établie ; Orchestra ne préserve pas la marge de log-loss. Les correcteurs allégés seuls réduisent le coût marginal du correcteur mais abaissent la qualité. Orchestra Org originale est implémentée et exécutée mais n'atteint pas la qualité OOF de référence et sa production OOF est coûteuse. Le parallélisme CPU naïf détériore les temps. Pas de preuve de baisse mémoire/énergie ni de généralisation externe.


## 8. Distillation et suppression du correcteur (20/20 exécutions)

| Famille | Variante | Paramètres totaux | Accuracy | Log-loss | Pipeline (s) |
|---|---|---:|---:|---:|---:|
| Emplica | sans correcteur | 7 340 | 97.88% | 0.04860 | 10.787 |
| Emplica | RBF-Lite distillé (88 paramètres correcteur) | 7 428 | 97.88% | 0.03983 | 10.865 |
| Orchestra | sans correcteur | 7 557 | 97.41% | 0.06091 | 9.732 |
| Orchestra | RBF-Lite distillé (88 paramètres correcteur) | 7 645 | 98.12% | 0.04701 | 9.799 |

La distillation rapproche la log-loss de la référence sans ajouter un ajustement correcteur coûteux, mais ne réduit pas le coût total du pipeline : le pipeline reste pratiquement inchangé et l'ajustement distillé ne remplace pas le coût OOF. Les logits enseignants sont ceux du correcteur EX6 gelé ; les soft targets de distillation proviennent uniquement des lignes d'entraînement. Cette piste conserve donc un bénéfice qualité intéressant, pas un gain de vitesse mesuré.

## 9. Variante OOF 5-fold — campagne complète (10/10)

La campagne strictement imbriquée 5-fold est maintenant terminée sur les cinq graines pour les deux familles. Les résultats agrégés sont :

| Famille | Correcteur 5-fold | Accuracy | Log-loss | Référence 3-fold log-loss |
|---|---|---:|---:|---:|
| Emplica OOF | RBF-Lite 1 probe | 98.12% | 0.04512 | 0.03637 |
| Emplica OOF | Linear context | 97.65% | 0.04712 | 0.03637 |
| Orchestra OOF | RBF-Lite 1 probe | 98.12% | 0.05964 | 0.03982 |
| Orchestra OOF | Linear context | 98.12% | 0.05113 | 0.03982 |

Les 5-fold sont inférieurs en log-loss aux références 3-fold, même lorsque l'accuracy reste proche. Ils ne remplacent donc pas les correcteurs OOF EX6. Les temps muraux ne sont pas utilisés pour conclure : la campagne a été reprise depuis des checkpoints partiels, ce qui rend les mesures end-to-end non homogènes. Le fichier d'agrégats et les JSON par graine restent fournis, sans mélanger les 5-fold aux résultats de référence 3-fold. Voir `EX7_OOF_5FOLD_STATUS.json` et `EX7_OOF_5FOLD_AGGREGATES.csv`.
