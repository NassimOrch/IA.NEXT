# Rapport final EX7 V003 — OuterCoord-Lite-7x1

**Date : 31 octobre 2026**  
**Statut : DÉVELOPPEMENT UNIQUEMENT — VALIDATION EXTERNE NON ÉTABLIE**  
**Verdict global : NON.** La candidate simplifie réellement Orchestra et réduit le coût de la lignée récursive, mais ne respecte pas la marge de log-loss et n'est pas plus rapide que le MLP aux latences mesurées.

## 1. Résumé exécutif

V003 a entraîné 5 graines de la nouvelle architecture, 5 MLP appariés en paramètres et 5 MLP-ge4x. Elle a aussi réutilisé, après vérification de hashes et de prédictions, cinq références historiques `OuterCoord-only-7x5` et cinq `Recursive-Org-7x5`. Le split Wisconsin de développement historique est inchangé (341 train, 85 validation). Aucun test externe n'a été ouvert.

La candidate ramène la capacité persistante à **1 341 paramètres** contre **6 712** pour les deux Orchestra historiques (−80,0 %, environ 5,00× moins). Elle obtient **97,88 % d'accuracy**, **97,34 % de précision macro** et **0,06806 de log-loss**. Elle réduit le temps d'optimisation rapporté par le script à 0,889 s, contre 3,431 s pour OuterCoord-only et 5,921 s pour l'Org récursive. Mais elle est dominée par les MLP sur les métriques principales et reste beaucoup plus lente que les MLP à l'inférence.

**Décision : simplification utile comme ablation de recherche ; pas de promotion comme architecture gagnante.**

## 2. Résultats moyens sur les cinq graines

Les temps `fit_seconds` mesurent le temps dans la boucle d'entraînement et de validation, après construction du modèle, initialisation KMeans, construction des tenseurs et des optimiseurs. Ils ne sont donc pas le temps complet de bout en bout ; les temps d'initialisation ne sont pas mesurés ici.

| Modèle | Accuracy | Précision macro | F1 macro | Log-loss | `fit_seconds` | `P_total` |
|---|---:|---:|---:|---:|---:|---:|
| V003 OuterCoord-Lite 7×1 | 97.88 % | 97.34 % | 97.77 % | 0.06806 | 0.889 | 1 341 |
| OuterCoord-only historique 7×5 | 98.59 % | 98.20 % | 98.51 % | 0.06013 | 3.431 | 6 712 |
| Orchestra Org récursive historique 7×5 | 98.35 % | 97.91 % | 98.26 % | 0.06187 | 5.921 | 6 712 |
| MLP apparié en P_total | 98.12 % | 97.63 % | 98.02 % | 0.05136 | 0.342 | 1 349 |
| MLP au moins 4× les paramètres | 98.59 % | 98.29 % | 98.50 % | 0.05222 | 0.269 | 5 375 |

Les métriques prioritaires restent accuracy et log-loss. ROC-AUC moyen de V003 : 0.998349 ; Brier : 0.01761 ; ECE10 : 0.02093. Les moyennes et écarts-types complets, ainsi que les résultats par graine, sont dans `results/metrics/AGGREGATES_V003.csv` et `PER_SEED_COMPARISON_V003.csv`.

## 3. Qualité : contrôle des marges EX7

Le repère de développement hérité est une baisse d'accuracy maximale de 0,5 point et une hausse relative maximale de log-loss de 5 %. Il s'agit d'un repère descriptif, pas d'une preuve statistique de non-infériorité. Les différences sont calculées sur cinq graines appariées, sur le même split historique.

| Référence | Baisse accuracy candidate | Hausse log-loss candidate | Marge accuracy | Marge log-loss |
|---|---:|---:|---|---|
| OuterCoord-only historique 7×5 | +0.706 pp | +13.19 % | ÉCHEC | ÉCHEC |
| Orchestra Org récursive historique 7×5 | +0.471 pp | +10.01 % | PASS | ÉCHEC |
| MLP apparié en P_total | +0.235 pp | +32.52 % | PASS | ÉCHEC |
| MLP au moins 4× les paramètres | +0.706 pp | +30.35 % | ÉCHEC | ÉCHEC |

La candidate échoue donc la marge de log-loss face aux quatre références. Elle dépasse aussi la marge accuracy face à OuterCoord-only et au MLP-ge4x. Face au MLP apparié et à la récursion complète, l'accuracy reste dans la marge descriptive, mais la log-loss ne la respecte pas.

### Résultats par graine de la candidate

| Graine | Accuracy % | Précision macro | Log-loss | MLP apparié accuracy / LL | MLP-ge4x accuracy / LL |
|---:|---:|---:|---:|---:|---:|
| 1501 | 97.65 | 0.9706 | 0.07414 | 97.65 / 0.05469 | 97.65 / 0.05471 |
| 1607 | 98.82 | 0.9848 | 0.04876 | 97.65 / 0.05215 | 98.82 / 0.04941 |
| 1717 | 97.65 | 0.9706 | 0.07849 | 97.65 / 0.05014 | 98.82 / 0.05412 |
| 2029 | 97.65 | 0.9706 | 0.08204 | 98.82 / 0.04737 | 98.82 / 0.05451 |
| 3037 | 97.65 | 0.9706 | 0.05689 | 98.82 / 0.05246 | 98.82 / 0.04833 |

Les cinq graines partagent le même split et ne sont pas cinq domaines indépendants. Les intervalles t appariés publiés dans `PAIRED_DIFFERENCES_V003.json` sont uniquement descriptifs.

## 4. Paramètres et comparaison MLP

- V003 : 1 281 paramètres entraînables + 60 coefficients du scaler = **1 341**.
- MLP apparié : 1 289 paramètres entraînables + 60 scaler = **1 349** (écart de 8 paramètres).
- MLP-ge4x : 5 315 paramètres entraînables + 60 scaler = **5 375**, soit **4,008×** V003 ; ratio vérifié graine par graine.
- Orchestra Org historique et OuterCoord-only : 6 712 `P_total` chacun.

Le correcteur/gate global de V003 représente 7 logits `rho`, déjà compris dans `P_train`. Les 60 paramètres du préprocesseur sont inclus pour tous les modèles, avec la même transformation de données. Les dimensions d'états Adam, checkpoint et export sont détaillées dans les JSON de chaque run.

Le MLP apparié est plus performant que V003 : 98,12 % vs 97,88 % d'accuracy et 0,05136 vs 0,06806 de log-loss. Le MLP-ge4x atteint 98,59 % d'accuracy et 0,05222 de log-loss. V003 n'atteint donc pas le critère combiné de qualité face au MLP-ge4x, même si le rapport de paramètres est supérieur à 4.

## 5. Latence d'inférence

### Mesure brute end-to-end

Mesure sur CPU, un thread, float32, 30 warmups, 200 répétitions par graine/modèle/batch, ordre intercalé. Cette table inclut l'application Torch du StandardScaler à des entrées brutes reconstruites à partir de la validation standardisée ; elle exclut chargement de fichiers et transferts/IO hôte. Les batchs 256 sont formés par répétition déterministe des premières lignes de validation (85 lignes disponibles).

Chaque cellule donne **p50 / p95 en millisecondes**, moyenne des cinq profils de graines.

| Batch | V003 | OuterCoord-only | Org récursive | MLP apparié | MLP-ge4x |
|---:|---:|---:|---:|---:|---:|
| 1 | 0.2902 / 0.4531 | 1.4903 / 1.9550 | 1.4941 / 1.9382 | 0.0251 / 0.0466 | 0.0262 / 0.0421 |
| 16 | 0.3218 / 0.4712 | 1.6252 / 2.0417 | 1.6412 / 2.0367 | 0.0316 / 0.0535 | 0.0394 / 0.0651 |
| 64 | 0.3932 / 0.5653 | 1.9801 / 2.4757 | 1.9935 / 2.4391 | 0.0422 / 0.0801 | 0.0704 / 0.1223 |
| 256 | 0.6181 / 0.9377 | 3.2097 / 4.1868 | 3.1957 / 3.9829 | 0.0821 / 0.1408 | 0.1904 / 0.2925 |

Batch 1 : V003 p50 **0,290 ms**, contre 1,490 ms pour OuterCoord-only (≈5,13× plus rapide) et 1,494 ms pour Org récursive (≈5,15×). Mais elle reste ≈11,6× plus lente que le MLP apparié (0,0251 ms) et ≈11,1× plus lente que le MLP-ge4x (0,0262 ms).

Batch 256 : V003 p50 **0,618 ms**, contre 3,210 ms et 3,196 ms pour les Orchestra ; elle reste ≈7,5× plus lente que le MLP apparié et ≈3,25× plus lente que le MLP-ge4x. Les débits et les p99 complets se trouvent dans `LATENCY_AGGREGATES_RAW_END2END_V003.csv`.

Le profil modèle seul (déjà standardisé) est conservé séparément dans `LATENCY_AGGREGATES_V003.csv`. Ne pas mélanger les deux scopes.

## 6. Temps d'entraînement et limites du chronométrage

Le temps moyen dans la boucle d'optimisation/validation est 0,889 s pour V003, 3,431 s pour OuterCoord-only et 5,921 s pour la récursion complète. Cela indique une accélération de la phase mesurée de 3,86× et 6,66× respectivement.

Cette mesure **n'est pas un temps complet de bout en bout** : le chronomètre démarre après la construction des modèles, l'initialisation des centres RBF par KMeans, les tenseurs et les optimiseurs. Le coût d'initialisation n'a pas été mesuré séparément. Le gain annoncé ne doit donc être interprété que pour la boucle entraînement/validation. Le temps de sérialisation n'est pas inclus dans `fit_seconds`.

V003 est également 2,60× plus lente que le MLP apparié (0,342 s) et 3,31× plus lente que le MLP-ge4x (0,269 s) dans cette même convention `fit_seconds`.

## 7. Coordination globale : elle ne rend pas encore le calcul sparse

Moyenne des poids `rho` finaux sur les cinq graines :

`[0,1265 ; 0,1607 ; 0,1429 ; 0,1260 ; 0,1554 ; 0,1447 ; 0,1438]`

L'entropie relative de la distribution moyenne vaut environ 99,81 % du maximum ; son nombre effectif de branches est 6,975 sur 7. Les poids sont légèrement différenciés, mais le gate reste presque uniforme. À l'inférence, les sept experts sont toujours tous exécutés ; aucune économie conditionnelle n'est donc obtenue par sélection de branche. L'amélioration de latence par rapport à Orchestra vient de la réduction 35→7 experts et de la suppression de la cascade/coordination interne.

## 8. Coûts et mesures non concluants

- `P_total` et tailles checkpoint/deploy : mesurés et enregistrés.
- Proxy MAC linéaire : fourni dans les JSON, mais il exclut tanh, distances RBF, exponentielles et softmax. Ce n'est pas un FLOP count complet ni une mesure de latence ; **coût opérationnel complet NON MESURÉ**.
- RAM peak isolée et comparable entre modèles : **NON MESURÉ / NON COMPARABLE**. Des échantillons RSS sont archivés, mais l'allocateur et le cache du processus partagé empêchent une attribution fiable par modèle.
- Énergie : **NON MESURÉ**.
- Temps d'initialisation/KMeans et temps complet total d'entraînement : **NON MESURÉ**.
- Validation externe vierge : **NON EXÉCUTÉE** ; les datasets de lignée et le split Wisconsin sont historiquement exposés.

L'absence de mesure sur une dimension obligatoire empêche le succès global selon la règle EX7.

## 9. Conclusion et prochaine hypothèse

V003 répond à la question structurale : on peut simplifier l'Org en sept probes indépendantes et un seul coordinateur externe, avec cinq fois moins de paramètres et une latence environ cinq fois plus faible que la lignée Orchestra 7×5. Mais le résultat ne valide pas l'idée d'une architecture globalement plus efficiente : le MLP reste nettement meilleur en log-loss et beaucoup plus rapide à l'inférence, tandis que le gate `rho` ne sélectionne pratiquement pas les branches.

La piste suivante ne devrait pas être simplement de réduire encore `k` ou `d`. Il faudrait comparer une stratégie de routage réellement conditionnelle (avec calcul des branches évitées) à un calcul dense, et mesurer le coût du routeur lui-même. Il faut aussi tester si l'entraînement sur shards stratifiés trop petits dégrade la qualité des experts, sans rompre le protocole de prévention du leakage.

**Verdict EX7 V003 : succès structural partiel contre Orchestra ; échec du critère qualité/efficacité combiné ; aucune généralisation externe établie.**
