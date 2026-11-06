# Résultats complets — campagne NG-ADAPT-2026-10-29-v1

## Résumé reproductible

- Benchmark binaire principal : 5 tâches × 11 conditions (A–J + K) × 3 graines = **165 entraînements évalués**, 0 échec, **29 403 prédictions de test archivées**. Extension multiclasse distincte digits 8×8 : 11 conditions × 3 graines = **33 entraînements supplémentaires**, 8 910 prédictions et 2 700 événements d’empreinte. Total descriptif architecture : 198 entraînements sur six tâches (cinq binaires + une à dix classes).
- 90 epochs dans le run principal; les quick smoke tests à 8 epochs sont exclus des conclusions.
- 60 entraînements supplémentaires de l'ablation de coordination globale; 0 échec.
- Tests de robustesse de boucle : 120 lignes de résultats sur cinq architectures et 16 200 fingerprints.
- Reconstruction : 3 seeds pour les architectures apprises; identité directe en contrôle; erreurs et checkpoints d'audit conservés.

Les métriques sont calculées sur les labels d'évaluation seulement après l'entraînement et le flux d'adaptation. Les fichiers `predictions_test_evaluation_only.csv` et `partition_ledger.csv` exposent des labels à des fins d'audit post-hoc; aucun API `fit` ou update ne les reçoit. L'audit automatisé vérifie à nouveau chaque métrique calculée à partir des probabilités archivées.

## 1. Replay strict de l'expérience de référence du bundle sonde

Le script source de référence a été exécuté sans modification dans le workspace de reprise. Résultats CSV/JSON identiques octet pour octet aux fichiers de référence archivés (les figures ont aussi été recalculées). Résultats archivés :

| Modèle | Accuracy moyenne ± SD | ROC-AUC moyenne ± SD | Log-loss moyenne ± SD | Paramètres entraînables |
|---|---:|---:|---:|---:|
| MLP de référence | 0.958700 ± 0.000671 | 0.991892 ± 0.000490 | 0.110863 ± 0.002955 | 49 |
| Sondes adaptatives RBF | 0.960050 ± 0.000542 | 0.990641 ± 0.000115 | 0.117404 ± 0.000813 | 49 |
| Sondes fixes ablation | 0.862300 ± 0.007364 | 0.919910 ± 0.008314 | 0.354977 ± 0.018486 | 13 |

Les cinq seeds de la référence utilisent un unique dataset généré et une partition commune; les cinq résultats ne sont pas cinq échantillons indépendants de données. Les valeurs au-dessus sont une reproduction de l'archive, non une nouvelle campagne multi-splits.

## 2. Comparaison A–J + K à 90 epochs

A = MLP; B = probes locales; C = probes avec coordinateur; D/E = mêmes variantes avec tanh sur la sortie; F–J = variantes avec adaptation en ligne; K = contrôle RBF fixe 16 centres/largeurs. Accuracy et log-loss sont rapportés séparément; une baisse d'accuracy ne peut pas être compensée silencieusement par la seule accuracy.

### Extension multiclasse : `digits_10class` (10 classes)

Cette extension répond au point manquant concernant les chiffres manuscrits à dix classes. Il s'agit d'une expérience nouvelle, préenregistrée et explicitement distincte du rejeu historique : elle ne doit pas être présentée comme la reproduction d'un éventuel protocole digits antérieur. Source : `sklearn.datasets.load_digits` (1 797 images 8×8, 64 caractéristiques, labels 0–9). Le ledger indique 1 797 lignes retenues, aucun doublon exact de vecteur de pixels retiré et aucun conflit de labels. Partition stratifiée fixe : train 1 077, validation 270, adaptation 180, test 270. Le scaler est ajusté sur train uniquement. L'audit confirme zéro chevauchement de hashes de caractéristiques entre les six paires de partitions; les labels de test ne sont utilisés ni pour le fit ni pour l'adaptation.

Le protocole `docs/PROTOCOLE_DIGITS_10CLASSES.md` fixe A–K, 90 epochs et trois graines d'optimisation (1501, 1607, 1717). Les moyennes/écarts-types ci-dessous sont descriptifs sur trois graines d'optimisation d'un unique split fixe; ils ne fournissent pas une estimation générale de performance.
Les prédictions brutes sont préservées telles qu’exportées. La somme par ligne s’écarte au maximum de 2,40×10⁻⁷ de 1 (précision softmax float32); l’audit renormalise chaque copie de ligne en mémoire uniquement pour le recalcul indépendant des métriques. L’écart maximal entre métriques stockées et recalculées après normalisation est de 2,45×10⁻¹¹.

| Architecture | Accuracy moyenne ± SD | Macro-F1 moyenne ± SD | Log-loss moyenne ± SD | Paramètres entraînables |
|---|---:|---:|---:|---:|
| A — MLP | 0,9481 ± 0,0064 | 0,9482 ± 0,0065 | 0,1726 ± 0,0255 | 1 210 |
| B — Sondes locales | 0,7185 ± 0,0464 | 0,7151 ± 0,0463 | 1,8418 ± 0,0084 | 1 240 |
| C — Locales + coordination globale | 0,7012 ± 0,0687 | 0,6977 ± 0,0696 | 1,8107 ± 0,0130 | 1 244 |
| D — Locales + activation tanh | 0,7469 ± 0,0371 | 0,7453 ± 0,0377 | 1,8951 ± 0,0048 | 1 240 |
| E — Globales + activation tanh | 0,7099 ± 0,0577 | 0,7085 ± 0,0597 | 1,8728 ± 0,0094 | 1 244 |
| F — MLP avec boucle en ligne | 0,8605 ± 0,0167 | 0,8607 ± 0,0146 | 0,4113 ± 0,0332 | 1 210 |
| G — Sondes locales avec boucle | 0,6198 ± 0,0878 | 0,6042 ± 0,1079 | 1,8047 ± 0,0078 | 1 240 |
| H — Globales avec boucle | 0,5679 ± 0,1215 | 0,5239 ± 0,1582 | 1,7894 ± 0,0184 | 1 244 |
| I — Locales + tanh avec boucle | 0,6210 ± 0,0557 | 0,6061 ± 0,0749 | 1,9002 ± 0,0045 | 1 240 |
| J — Globales + tanh avec boucle | 0,6062 ± 0,0594 | 0,5786 ± 0,0869 | 1,9045 ± 0,0185 | 1 244 |
| K — RBF fixe | 0,7481 ± 0,0064 | 0,7439 ± 0,0047 | 1,7898 ± 0,0230 | 170 |

![Accuracy à dix classes par architecture](figures/digits10_accuracy.png)

![Log-loss à dix classes par architecture](figures/digits10_logloss.png)

**Interprétation limitée au protocole.** A (MLP) est nettement meilleur que les ensembles de sondes sur ce split de dix classes. La boucle en ligne F dégrade aussi l'accuracy du MLP, de 0,9481 à 0,8605; G–J sont plus faibles encore. La coordination globale C ne bat pas B, et l'activation tanh (D/E) ne produit pas de bénéfice uniforme. Ces chiffres réfutent une revendication de gain universel sur cette instanciation, pas toute possibilité de coordination ou d'adaptation sous un autre modèle, budget ou jeu de données. Les intervalles t sur trois seeds d'optimisation ne corrigent pas l'incertitude liée à l'unique partition.

### Tâche : `two_moons`

| Architecture | Accuracy moyenne (SD) | Log-loss moyenne (SD) | Paramètres | Train (s) | Adaptation (s) |
|---|---:|---:|---:|---:|---:|
| A — MLP classic sans boucle | 0.9185 (0.0098) | 0.2237 (0.0117) | 65 | 0.328 | 0.000 |
| B — Sondes locales sans coordination | 0.9074 (0.0000) | 0.3390 (0.0027) | 68 | 0.227 | 0.000 |
| C — Sondes locales + coordination globale | 0.9086 (0.0043) | 0.3199 (0.0078) | 72 | 0.232 | 0.000 |
| D — Sondes locales + tanh | 0.9074 (0.0000) | 0.4486 (0.0011) | 68 | 0.236 | 0.000 |
| E — Sondes globales + tanh | 0.9099 (0.0021) | 0.4425 (0.0029) | 72 | 0.247 | 0.000 |
| F — MLP avec boucle | 0.9309 (0.0113) | 0.1947 (0.0161) | 65 | 0.044 | 0.100 |
| G — Sondes locales avec boucle | 0.9049 (0.0021) | 0.3248 (0.0016) | 68 | 0.222 | 0.216 |
| H — Sondes globales avec boucle | 0.9012 (0.0021) | 0.3233 (0.0059) | 72 | 0.233 | 0.265 |
| I — Sondes locales + tanh avec boucle | 0.9037 (0.0000) | 0.4417 (0.0008) | 68 | 0.241 | 0.227 |
| J — Sondes globales + tanh avec boucle | 0.9012 (0.0077) | 0.4464 (0.0109) | 72 | 0.251 | 0.285 |
| K — Contrôle RBF fixes (centres/largeurs non adaptatifs) | 0.9111 (0.0064) | 0.2739 (0.0041) | 17 | 0.068 | 0.000 |

### Tâche : `circles`

| Architecture | Accuracy moyenne (SD) | Log-loss moyenne (SD) | Paramètres | Train (s) | Adaptation (s) |
|---|---:|---:|---:|---:|---:|
| A — MLP classic sans boucle | 0.9210 (0.0021) | 0.2588 (0.0120) | 65 | 0.390 | 0.000 |
| B — Sondes locales sans coordination | 0.9222 (0.0000) | 0.3572 (0.0096) | 68 | 0.273 | 0.000 |
| C — Sondes locales + coordination globale | 0.9210 (0.0021) | 0.3352 (0.0084) | 72 | 0.279 | 0.000 |
| D — Sondes locales + tanh | 0.9222 (0.0000) | 0.4489 (0.0037) | 68 | 0.257 | 0.000 |
| E — Sondes globales + tanh | 0.9222 (0.0000) | 0.4410 (0.0010) | 72 | 0.270 | 0.000 |
| F — MLP avec boucle | 0.8765 (0.0077) | 0.2924 (0.0072) | 65 | 0.049 | 0.112 |
| G — Sondes locales avec boucle | 0.9000 (0.0037) | 0.3317 (0.0090) | 68 | 0.225 | 0.214 |
| H — Sondes globales avec boucle | 0.8815 (0.0074) | 0.3251 (0.0159) | 72 | 0.279 | 0.339 |
| I — Sondes locales + tanh avec boucle | 0.8988 (0.0021) | 0.4478 (0.0022) | 68 | 0.276 | 0.280 |
| J — Sondes globales + tanh avec boucle | 0.8852 (0.0064) | 0.4482 (0.0084) | 72 | 0.310 | 0.341 |
| K — Contrôle RBF fixes (centres/largeurs non adaptatifs) | 0.7938 (0.0273) | 0.5902 (0.0148) | 17 | 0.068 | 0.000 |

### Tâche : `xor_product`

| Architecture | Accuracy moyenne (SD) | Log-loss moyenne (SD) | Paramètres | Train (s) | Adaptation (s) |
|---|---:|---:|---:|---:|---:|
| A — MLP classic sans boucle | 0.9185 (0.0064) | 0.3106 (0.0050) | 65 | 0.316 | 0.000 |
| B — Sondes locales sans coordination | 0.9173 (0.0057) | 0.4753 (0.0087) | 68 | 0.229 | 0.000 |
| C — Sondes locales + coordination globale | 0.9198 (0.0113) | 0.4389 (0.0024) | 72 | 0.238 | 0.000 |
| D — Sondes locales + tanh | 0.9235 (0.0057) | 0.5121 (0.0076) | 68 | 0.234 | 0.000 |
| E — Sondes globales + tanh | 0.9284 (0.0119) | 0.4952 (0.0014) | 72 | 0.247 | 0.000 |
| F — MLP avec boucle | 0.8383 (0.0043) | 0.3790 (0.0188) | 65 | 0.042 | 0.098 |
| G — Sondes locales avec boucle | 0.8914 (0.0140) | 0.4464 (0.0085) | 68 | 0.215 | 0.201 |
| H — Sondes globales avec boucle | 0.7951 (0.0396) | 0.4721 (0.0309) | 72 | 0.230 | 0.240 |
| I — Sondes locales + tanh avec boucle | 0.8988 (0.0150) | 0.4998 (0.0062) | 68 | 0.210 | 0.192 |
| J — Sondes globales + tanh avec boucle | 0.8173 (0.0107) | 0.5108 (0.0069) | 72 | 0.227 | 0.246 |
| K — Contrôle RBF fixes (centres/largeurs non adaptatifs) | 0.8914 (0.0043) | 0.5473 (0.0181) | 17 | 0.059 | 0.000 |

### Tâche : `wine_binary`

| Architecture | Accuracy moyenne (SD) | Log-loss moyenne (SD) | Paramètres | Train (s) | Adaptation (s) |
|---|---:|---:|---:|---:|---:|
| A — MLP classic sans boucle | 1.0000 (0.0000) | 0.0122 (0.0061) | 241 | 0.295 | 0.000 |
| B — Sondes locales sans coordination | 0.9259 (0.0000) | 0.3747 (0.0031) | 244 | 0.195 | 0.000 |
| C — Sondes locales + coordination globale | 0.9383 (0.0214) | 0.3440 (0.0084) | 248 | 0.200 | 0.000 |
| D — Sondes locales + tanh | 0.9630 (0.0000) | 0.4589 (0.0015) | 244 | 0.199 | 0.000 |
| E — Sondes globales + tanh | 0.9630 (0.0000) | 0.4458 (0.0052) | 248 | 0.218 | 0.000 |
| F — MLP avec boucle | 1.0000 (0.0000) | 0.0057 (0.0019) | 241 | 0.034 | 0.009 |
| G — Sondes locales avec boucle | 0.9259 (0.0000) | 0.3657 (0.0031) | 244 | 0.191 | 0.020 |
| H — Sondes globales avec boucle | 0.9506 (0.0214) | 0.3227 (0.0172) | 248 | 0.200 | 0.023 |
| I — Sondes locales + tanh avec boucle | 0.9630 (0.0000) | 0.4551 (0.0016) | 244 | 0.190 | 0.020 |
| J — Sondes globales + tanh avec boucle | 0.9630 (0.0000) | 0.4363 (0.0112) | 248 | 0.207 | 0.028 |
| K — Contrôle RBF fixes (centres/largeurs non adaptatifs) | 0.9506 (0.0214) | 0.2444 (0.0103) | 17 | 0.043 | 0.000 |

### Tâche : `digits_3_vs_8`

| Architecture | Accuracy moyenne (SD) | Log-loss moyenne (SD) | Paramètres | Train (s) | Adaptation (s) |
|---|---:|---:|---:|---:|---:|
| A — MLP classic sans boucle | 1.0000 (0.0000) | 0.0086 (0.0008) | 1057 | 0.340 | 0.000 |
| B — Sondes locales sans coordination | 0.9383 (0.0283) | 0.4344 (0.0038) | 1060 | 0.220 | 0.000 |
| C — Sondes locales + coordination globale | 0.9506 (0.0214) | 0.3896 (0.0061) | 1064 | 0.224 | 0.000 |
| D — Sondes locales + tanh | 0.9383 (0.0283) | 0.4849 (0.0016) | 1060 | 0.208 | 0.000 |
| E — Sondes globales + tanh | 0.9506 (0.0214) | 0.4622 (0.0026) | 1064 | 0.227 | 0.000 |
| F — MLP avec boucle | 0.8827 (0.0107) | 0.3131 (0.0617) | 1057 | 0.036 | 0.019 |
| G — Sondes locales avec boucle | 0.9568 (0.0107) | 0.4249 (0.0018) | 1060 | 0.200 | 0.040 |
| H — Sondes globales avec boucle | 0.9506 (0.0214) | 0.3507 (0.0135) | 1064 | 0.227 | 0.055 |
| I — Sondes locales + tanh avec boucle | 0.9568 (0.0214) | 0.4861 (0.0014) | 1060 | 0.233 | 0.047 |
| J — Sondes globales + tanh avec boucle | 0.9259 (0.0370) | 0.4574 (0.0026) | 1064 | 0.235 | 0.052 |
| K — Contrôle RBF fixes (centres/largeurs non adaptatifs) | 0.8951 (0.0107) | 0.5065 (0.0106) | 17 | 0.050 | 0.000 |


### Interprétation de la campagne principale

- **Pas de gagnant universel.** Sur la moyenne descriptive non pondérée des cinq tâches binaires, A (MLP) atteint environ 0,9516 en accuracy et 0,1628 en log-loss; B atteint environ 0,9222 et 0,3961; C environ 0,9277 et 0,3655. Ce résumé est descriptif; il mélange tâches de tailles et difficultés différentes, donc les tableaux par tâche restent les résultats principaux.
- **Coordination globale : effet modeste, dépendant de la tâche.** C améliore la log-loss par rapport à B dans les cinq tâches binaires utilisées, mais le gain varie et la validation sur trois seeds/une partition fixe reste faible. L'ablation C gelée est identique à B dans le contrôle dédié, ce qui vérifie la propriété de réduction annoncée.
- **Activation tanh à la sortie de chaque probe : pas d'avantage automatique.** D/E ont, dans cette implémentation où BCE-with-logits reçoit des sorties bornées par tanh, des log-loss plus élevées que B/C dans la plupart des tâches. Cette conclusion est spécifique au placement de l'activation et à la perte choisie, pas à toutes les activations des réseaux.
- **Boucle online : risque de dérive.** Le résultat F–J diffère selon la tâche. Aucune revendication de gain général : l'adaptation peut améliorer la log-loss sur certains streams et détériorer l'accuracy ou la calibration sur d'autres. Un flux d'adaptation ajoute également des données et du calcul; la comparaison à un système entièrement sans flux n'est pas à elle seule une comparaison de calcul égalisé.
- **K n'est pas une baseline de capacité équivalente.** Elle utilise 17 paramètres dans ce protocole (contre 65–72 pour A–E en deux dimensions) et sert de contrôle de centre/largeur fixes.

## 3. Ablation de coordination globale

Conditions : B (local uniforme); C gelée (phi=0, aucune mise à jour globale); C globale entraînée normalement; C globale entraînée sur labels `y_train` permutés par seed. Le contrôle shuffle affecte seulement l'objectif du coordinateur; les pertes des probes locaux restent sur leurs labels train réels.

| Tâche | Condition | Accuracy (moy.) | SD | Log-loss (moy.) | SD | Updates globales |
|---|---|---:|---:|---:|---:|---:|
| circles | B_local | 0.9222 | 0.0000 | 0.3572 | 0.0096 | 0 |
| circles | C_global_frozen | 0.9222 | 0.0000 | 0.3572 | 0.0096 | 0 |
| circles | C_global_full | 0.9210 | 0.0021 | 0.3352 | 0.0084 | 18 |
| circles | C_global_shuffled_labels | 0.9235 | 0.0021 | 0.3524 | 0.0082 | 18 |
| digits_3_vs_8 | B_local | 0.9383 | 0.0283 | 0.4344 | 0.0038 | 0 |
| digits_3_vs_8 | C_global_frozen | 0.9383 | 0.0283 | 0.4344 | 0.0038 | 0 |
| digits_3_vs_8 | C_global_full | 0.9506 | 0.0214 | 0.3896 | 0.0061 | 18 |
| digits_3_vs_8 | C_global_shuffled_labels | 0.9074 | 0.0000 | 0.4385 | 0.0012 | 18 |
| two_moons | B_local | 0.9074 | 0.0000 | 0.3390 | 0.0027 | 0 |
| two_moons | C_global_frozen | 0.9074 | 0.0000 | 0.3390 | 0.0027 | 0 |
| two_moons | C_global_full | 0.9086 | 0.0043 | 0.3199 | 0.0078 | 18 |
| two_moons | C_global_shuffled_labels | 0.9074 | 0.0000 | 0.3380 | 0.0036 | 18 |
| wine_binary | B_local | 0.9259 | 0.0000 | 0.3747 | 0.0031 | 0 |
| wine_binary | C_global_frozen | 0.9259 | 0.0000 | 0.3747 | 0.0031 | 0 |
| wine_binary | C_global_full | 0.9383 | 0.0214 | 0.3440 | 0.0084 | 18 |
| wine_binary | C_global_shuffled_labels | 0.9259 | 0.0000 | 0.3728 | 0.0024 | 18 |
| xor_product | B_local | 0.9173 | 0.0057 | 0.4753 | 0.0087 | 0 |
| xor_product | C_global_frozen | 0.9173 | 0.0057 | 0.4753 | 0.0087 | 0 |
| xor_product | C_global_full | 0.9198 | 0.0113 | 0.4389 | 0.0024 | 18 |
| xor_product | C_global_shuffled_labels | 0.9099 | 0.0150 | 0.4780 | 0.0194 | 18 |

Résultat exact du contrôle d'ablation : maximum d'écart absolu de probabilité B vs C gelé = 0.0; 2 673/2 673 lignes appariées sont égales bit à bit au niveau des valeurs CSV float décodées. C active est légèrement meilleur en log-loss sur plusieurs tâches, mais le contrôle labels permutés montre que le coordinateur n'est pas un gain magique et que son effet dépend des données. La campagne est trop petite pour conclure sur des différences pratiques stables.

## 4. Boucle observation → fingerprint → update : stress-tests

Sur `two_moons`, architectures A–E, seeds 1501/1607/1717; flux d'adaptation de 180 observations. Condition d'évaluation primaire : test source. Shift condition : évaluation aussi sur un test décalé. Le seuil de détection est le quantile 95% de `abs(y-p)` sur la validation propre, décidé avant la boucle.

Exemple de comparaison du MLP A :

| Condition | Accuracy moyenne sur test source | Log-loss moyenne (résultat par fichier source) | Interprétation |
|---|---:|---:|---|
| Sans boucle | 0.9185 | ≈0.2237 | Référence sans update |
| Boucle propre, updates actifs | 0.9309 | ≈0.1947 | Gain observé sur ce dataset/seed/split |
| Updates désactivés | 0.9185 | ≈0.2237 | Contrôle qui recouvre la baseline |
| 30% d'observations manquantes | 0.9173 | 0.2148 | Pas d'avantage d'accuracy, log-loss un peu meilleure dans ce pilote |
| 20% labels inversés | 0.8531 | 0.4043 | Dégradation importante |
| 50% labels trompeurs | 0.4012 | 0.7633 | Dérive grave |
| Flux covariablement décalé, test source | 0.8543 | 0.2938 | Dégradation sur la distribution source |

Pour les probes, la qualité n'est pas monotone non plus : par exemple B obtient 0.9049 / 0.3248 (accuracy/log-loss) avec boucle propre contre 0.9074 / 0.3390 sans boucle; C passe à 0.9012 / 0.3233 contre 0.9086 / 0.3199. C'est un compromis, pas une amélioration globale.

Les fingerprints ne détectent pas parfaitement les observations défectueuses. À 20% de corruption, la précision/rappel de détection varie suivant le modèle (précision ≈0,77–0,93 et rappel ≈0,38–0,67). Sous 50% de labels trompeurs, le rappel de A est seulement ≈0,07 alors que d'autres probes se situent autour de 0,49–0,59. Un seuil de résidu seul n'est donc pas un détecteur universel, et une observation trompeuse peut être absorbée par la mise à jour.

## 5. Reconstruction `x → f(x) → g(f(x)) ≈ x`

Jeu synthétique séparé de deux lunes, 2 400 points, bruit de génération 0,22, seeds d'optimisation 101/202/303, split train/validation/adaptation/test, standardisation sur train uniquement. La seconde sonde n'a pas accès au `x` d'origine et aucune connexion de saut n'est présente. Les résultats au niveau du test source :

| Modèle | RMSE moyenne | R² scalaire moyen | Paramètres stockés | Lecture correcte |
|---|---:|---:|---:|---|
| Identité directe | 0.0000 | 1.0000 | 0 | Baseline triviale exacte puisque cible = entrée; pas une solution apprise |
| Autoencodeur MLP latent 2 | ≈0.0349 | ≈0.9988 | 164 | Meilleure composition apprise sur ce problème |
| RBF libre, deux maps, global | ≈0.0982 | ≈0.9906 | 244 | Approximation non triviale, mais moins précise que le MLP AE |
| RBF deux maps, local-then-freeze | ≈0.1635 | ≈0.9745 | 244 stockés/actualisés; 122 restent `requires_grad` après gel | Le premier module est appris puis gelé; le compte de paramètres initial avait été sous-estimé dans le premier passage et a été corrigé dans les livrables finaux |
| RBF goulot latent 1 | ≈0.5165 | ≈0.76 | 147 | Démonstration descriptive de perte d'information due au goulot dans cette instance |
| RBF libre + boucle online | ≈0.4804 | ≈0.6374 | 244 | La mise à jour en ligne détériore fortement la reconstruction; SD élevée reflète une graine catastrophique conservée |
| RBF tanh + boucle online | ≈0.7521 | ≈0.3152 | 244 | Dérive encore plus forte; activation ne garantit pas la stabilité |

La boucle désactivée enregistre les mêmes observations/fingerprints mais n'actualise pas les paramètres; ses métriques de test sont identiques à la version pré-boucle, comme attendu. L'évaluation sous bruit, décalage (+0,75 sur la première coordonnée) et reconstruction vers le parent propre est dans `reconstruction_summary.csv`. Le MLP AE latent 2 ne montre pas de capacité de débruitage supérieure à l'identité dans la condition explicitement évaluée : le but d'entraînement est la reconstruction exacte X → X, pas le débruitage supervisé.

## 6. Boucle causale dédiée : décision de mise à jour pilotée par l'empreinte

Un second protocole isolé (ID `NG-ADAPT-2026-10-29-FBR-1`) teste non seulement l'existence des empreintes, mais aussi si leur résidu change la décision d'update. La campagne a été relancée dans un répertoire neuf après qu'un ancien manifeste a révélé une discordance entre graines demandées et fragments de résultats mis en cache. L'ancienne version est quarantinée par hashes sous `logs/fingerprint_feedback_loop_prior_quarantined/`; elle n'est pas utilisée pour les résultats finaux.

Le run propre demande explicitement les graines 1501/1607/1717 et les architectures A–E. Résultats : **15/15 couples graine–architecture**, 390 lignes métriques, 54 000 fingerprints, 0 erreur. Chaque fragment comporte 26 lignes métriques et 3 600 événements. L'audit vérifie les trois graines présentes, l'absence de fragments supplémentaires, l'unicité des hashes d'empreinte et la concordance entre décision d'update et action effectivement exécutée.

L'ordre est causal : prédire avant l'observation, révéler la mesure de la partition d'adaptation si disponible, calculer l'empreinte avec seuil q90 calibré sur la validation propre, puis choisir l'update. Le gate résiduel saute l'update si le résidu dépasse le seuil. Le contrôle aléatoire saute 10 % des updates sans regarder l'erreur. La politique ciblée sélectionne pour les ensembles RBF la sonde ayant le résidu local le plus élevé (sous condition de gate); elle ne donne pas de preuve d'optimalité.

La figure `figures/fbr1_archC_clean_vs_misleading.png` visualise l'accuracy de C sur flux propre et labels trompeurs; elle est descriptive (3 graines), sans prétention confirmatoire.

### Moyennes accuracy / log-loss sur les 3 graines, test source

Les cellules donnent `accuracy / log-loss`. Les résultats complets pour les cinq conditions, les cinq architectures, les deux distributions d'évaluation, toutes les métriques et les intervalles sont dans `results/fingerprint_feedback_loop/feedback_summary.csv` et `feedback_metrics_per_seed.csv`.

| Condition | Arch. | Update inconditionnel | Gate fingerprint, round-robin | Gate fingerprint ciblé | Contrôle aléatoire 10 % |
|---|:---:|---:|---:|---:|---:|
| Propre | A | 0,9309 / 0,1947 | 0,8901 / 0,4579 | 0,8901 / 0,4579 | 0,9321 / 0,2026 |
| Propre | B | 0,9049 / 0,3248 | 0,9037 / 0,3152 | 0,9025 / 0,3108 | 0,9099 / 0,3210 |
| Propre | C | 0,9012 / 0,3233 | 0,7259 / 0,6634 | 0,9025 / 0,3086 | 0,8864 / 0,3370 |
| Propre | D | 0,9037 / 0,4417 | 0,9037 / 0,4422 | 0,9037 / 0,4393 | 0,9074 / 0,4428 |
| Propre | E | 0,9012 / 0,4464 | 0,7926 / 0,5070 | 0,9111 / 0,4357 | 0,9025 / 0,4476 |
| Labels trompeurs 50 % | A | 0,4901 / 0,6701 | 0,8815 / 0,4903 | 0,8815 / 0,4903 | 0,5321 / 0,6519 |
| Labels trompeurs 50 % | B | 0,8914 / 0,3887 | 0,9012 / 0,3234 | 0,9074 / 0,3154 | 0,8815 / 0,3829 |
| Labels trompeurs 50 % | C | 0,8222 / 0,4685 | 0,8346 / 0,3514 | 0,8988 / 0,3045 | 0,8123 / 0,4708 |
| Labels trompeurs 50 % | D | 0,8654 / 0,4905 | 0,9012 / 0,4529 | 0,9000 / 0,4433 | 0,8617 / 0,4886 |
| Labels trompeurs 50 % | E | 0,8012 / 0,5180 | 0,8580 / 0,4618 | 0,9000 / 0,4382 | 0,8086 / 0,5210 |

### Lecture

- Le gate d'empreinte **aide nettement** lorsque les labels sont trompeurs à 50 % sur plusieurs architectures, notamment MLP A (accuracy 0,4901 → 0,8815). Il ne suffit pas à prévenir toutes les dérives et reste un seuil heuristique.
- Sur données propres, le gate round-robin nuit fortement à A, C et E sur ce split; le gate ciblé conserve mieux la performance pour les ensembles RBF, mais n'est pas meilleur partout. Un résidu élevé peut signaler une erreur potentiellement informative, et l'éliminer systématiquement peut nuire à l'apprentissage.
- Le contrôle aléatoire n'est pas équivalent à un gate résiduel : les politiques choisissent des mises à jour différentes. Aucune de ces variantes ne peut être déclarée optimale par ce seul pilote.
- Les observations de flux sont des labels simulés contrôlés. Le protocole prouve une conséquence de la règle implémentée, pas la validité d'une « empreinte » ontologique ou d'une théorie d'observation générale.

### Supplément de boucle causale pour la reconstruction (RBF-R1)

Le protocole séparé `NG-ADAPT-2026-10-29-RBF-R1` vérifie que l'empreinte résiduelle pilote effectivement la décision d'update pendant la composition `x → f(x) → g(f(x))`. Il ne remplace pas la campagne de reconstruction précédente. Deux variantes sont testées (`RBF2_free_global` et `RBF2_free_tanh_global`), avec les graines 101, 202 et 303, quatre conditions de flux (propre, 30 % de mesures absentes, bruit de mesure σ=0,10, décalage de la première coordonnée +0,75) et quatre politiques (mise à jour inconditionnelle, gate q90, gate aléatoire 10 %, aucune mise à jour). Le seuil q90 est calculé sur les résidus de validation propre avant adaptation. Les observations du flux d'adaptation servent aux updates; les tests sont évalués après le gel du flux.

La figure `figures/rbf_r1_reconstruction_policy_rmse.png` compare le RMSE test source par politique avec l'écart-type inter-graines.

**Bilan d'exécution :** 6/6 paires modèle–graine terminées, 162 lignes métriques et 23 040 événements d'empreinte, aucune erreur inscrite. L'audit indépendant recalcule les agrégats, vérifie les règles de décision, l'absence d'update sur une mesure manquante et le fait que le test n'est pas passé à l'update. Les métriques détaillées sont dans `results/reconstruction_feedback_gate/reconstruction_feedback_metrics_per_seed.csv` et les événements dans `reconstruction_feedback_fingerprints.csv`.

| Modèle | Politique | RMSE moyen, test source | Écart-type inter-graines | Updates moyens sur 240 observations |
|---|---|---:|---:|---:|
| RBF2 libre, globale | aucune mise à jour | 0,0982 | 0,0188 | 0 |
| RBF2 libre, globale | mise à jour inconditionnelle | 0,4804 | 0,4737 | 240,0 |
| RBF2 libre, globale | gate empreinte q90 | 1,4298 | 0,2076 | 2,33 |
| RBF2 libre, globale | gate aléatoire 10 % | 0,7519 | 0,4736 | 215,67 |
| RBF2 tanh, globale | aucune mise à jour | 0,0864 | 0,0017 | 0 |
| RBF2 tanh, globale | mise à jour inconditionnelle | 0,7521 | 0,4786 | 240,0 |
| RBF2 tanh, globale | gate empreinte q90 | 1,3659 | 0,2323 | 2,67 |
| RBF2 tanh, globale | gate aléatoire 10 % | 0,7750 | 0,4396 | 221,33 |

Le résultat est **défavorable à cette règle de gate en reconstruction** : le seuil résiduel q90 autorise très peu d'updates, mais les rares updates autorisées peuvent déstabiliser l'optimiseur et dégrader la fonction composée. Sur la tâche propre, l'absence d'update est nettement meilleure pour ces modèles pré-entraînés. Le résultat se répète sur le flux bruité et décalé; la boucle n'est donc ni intrinsèquement stable ni automatiquement bénéfique. Il s'agit d'un résultat négatif valable pour ces deux instanciations, ce n'est pas une preuve que toute adaptation de reconstruction échoue. Un protocole ultérieur doit préenregistrer des pas bornés, clipping, redémarrage d'optimiseur ou mise à jour amortie, avec contrôle et comparaison séparés; ces améliorations ne sont pas rétroactivement introduites dans RBF-R1.

## 7. Audit de paquets et qualité des données

- Archive du bundle de formalisation observationnelle : validateur interne code 0; PDF source 109 pages, hashes/structure valides selon son propre vérificateur.
- Expérience adaptive v1.2 : `PASS_WITH_LIMITATIONS`, 16/16 checks.
- NGeGenBrain v2 : manifeste valide sur 417 fichiers; NGeGenBrain v3.1 : manifeste valide sur extraction propre 794/794, 66 tests courants réussis, 65 tests de non-régression V1 réussis.
- `Screenplay_dataset.jsonl` : 4 000 lignes JSON valides, 2 000 objets uniques et 2 000 duplications supplémentaires.
- `batch_dataset.jsonl` : 783/784 objets valides; ligne 784 tronquée et conservée dans l'audit.
- `0000.parquet` : signature Parquet valide mais contenu non lu faute de librairie de décodage. Aucun résultat scientifique de ce fichier n'est revendiqué.

## 8. Limites d’interprétation

Les résultats sont descriptifs, sur un seul split par tâche, trois graines d'optimisation et six tâches spécifiques (cinq binaires, une multiclasse). Les intervalles t se rapportent aux seeds, pas à une population d'échantillons. Les coûts d'entraînement/latence ont été mesurés; le nombre de FLOPs et l'utilisation mémoire de pointe n'ont pas été contrôlés strictement. L'architecture centrale de coordination accède à tout le train; elle ne prouve pas une confidentialité distribuée. Pas de revendication d'équivalence mécanistique, d'identifiabilité générale, de convergence des mises à jour Adam/online ni de supériorité universelle.
