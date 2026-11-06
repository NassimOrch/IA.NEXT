# Comparaison des variantes et MLP — EX7 V002

Ce rapport consolide uniquement des exécutions déjà réalisées. **Aucun modèle n'a été réentraîné pour cette réconciliation** : les tableaux appariés sont calculés à partir des sorties par graine existantes, avec le MLP de la même graine et le ratio de paramètres contrôlé.

## 1. Réduction dimensionnelle / centres / partage / low-rank des correcteurs OOF

Moyennes sur 5 graines. Les temps candidats sont des pipelines complets reconstruits depuis les champs OOF/base/correcteur des runs ; les temps MLP sont le fit comparateur associé.

| Famille | Variante | Paramètres sonde / MLP | Ratio | Accuracy sonde / MLP | Log-loss sonde / MLP | Pipeline sonde / fit MLP (s) | Ralentissement |
|---|---|---:|---:|---:|---:|---:|---:|
| emp_oof_corrector | rbf_d1_k4 | 7391 / 33194 | 4.491× | 98.35% / 98.82% | 0.03884 / 0.04675 | 11.47 / 0.263 | 44.4× |
| emp_oof_corrector | rbf_d2_k2 | 7418 / 33194 | 4.475× | 98.59% / 98.82% | 0.04136 / 0.04675 | 11.35 / 0.263 | 43.9× |
| emp_oof_corrector | rbf_d1_k2 | 7383 / 33194 | 4.496× | 98.35% / 98.82% | 0.04448 / 0.04675 | 11.51 / 0.263 | 44.3× |
| emp_oof_corrector | shared_centers_2heads | 7440 / 33194 | 4.462× | 98.59% / 98.82% | 0.03970 / 0.04675 | 12.31 / 0.263 | 48.0× |
| emp_oof_corrector | lowrank_context_r1 | 7376 / 33194 | 4.500× | 98.59% / 98.82% | 0.04485 / 0.04675 | 11.30 / 0.263 | 43.7× |
| emp_oof_corrector | lowrank_context_r2 | 7410 / 33194 | 4.480× | 98.59% / 98.82% | 0.04388 / 0.04675 | 11.28 / 0.263 | 43.6× |
| orch_input_oof_corrector | rbf_d1_k4 | 7608 / 34052 | 4.476× | 97.88% / 98.82% | 0.05603 / 0.04733 | 10.25 / 0.260 | 39.7× |
| orch_input_oof_corrector | rbf_d2_k2 | 7635 / 34052 | 4.460× | 97.41% / 98.82% | 0.05639 / 0.04733 | 10.36 / 0.260 | 40.1× |
| orch_input_oof_corrector | rbf_d1_k2 | 7600 / 34052 | 4.481× | 97.65% / 98.82% | 0.04847 / 0.04733 | 10.45 / 0.260 | 40.5× |
| orch_input_oof_corrector | shared_centers_2heads | 7657 / 34052 | 4.447× | 97.18% / 98.82% | 0.05250 / 0.04733 | 10.37 / 0.260 | 40.2× |
| orch_input_oof_corrector | lowrank_context_r1 | 7593 / 34052 | 4.485× | 97.18% / 98.82% | 0.05709 / 0.04733 | 10.23 / 0.260 | 39.6× |
| orch_input_oof_corrector | lowrank_context_r2 | 7627 / 34052 | 4.465× | 97.41% / 98.82% | 0.05708 / 0.04733 | 10.17 / 0.260 | 39.4× |

**Lecture :** les 12 bras (6 variantes × 2 familles) restent au moins à 4× moins de paramètres. Côté Emplica, plusieurs correcteurs réduits conservent une log-loss meilleure que le MLP, mais l'accuracy baisse de 0.24 à 0.47 point et le pipeline reste environ 44–48× plus long. Côté Orchestra, seule `rbf_d1_k2` approche le MLP en log-loss (écart relatif +2.44 %), mais son accuracy est inférieure d'environ 1.18 point et le pipeline reste environ 40× plus long. Aucun bras ne remplit simultanément les critères de qualité et de vitesse.

## 2. Profondeur et capacité de l'Orchestra Org

| Variante | Paramètres sonde / MLP | Ratio | Accuracy sonde / MLP | Log-loss sonde / MLP | Fit sonde / MLP (s) | Ralentissement |
|---|---:|---:|---:|---:|---:|---:|
| shallow_5x5 | 4800 / 27221 | 5.671× | 98.12% / 98.59% | 0.06008 / 0.04791 | 5.89 / 0.401 | 17.8× |
| deep_9x5 | 8624 / 34514 | 4.002× | 98.35% / 98.82% | 0.06447 / 0.04719 | 9.02 / 0.278 | 33.4× |
| latent_d2 | 3862 / 27221 | 7.048× | 98.35% / 98.59% | 0.06778 / 0.04791 | 4.92 / 0.401 | 14.3× |
| centers_k4 | 5732 / 27221 | 4.749× | 97.65% / 98.59% | 0.07208 / 0.04791 | 6.48 / 0.401 | 18.7× |
| latent_d2_centers_k4 | 3162 / 27221 | 8.609× | 97.65% / 98.59% | 0.07088 / 0.04791 | 6.37 / 0.401 | 19.0× |

`centers_k4` est bien achevée sur cinq graines : 5 732 paramètres moyens, ratio 4.749×, accuracy 97.65 % vs 98.59 % MLP, log-loss 0.07208 vs 0.04791, temps fit 6.48 s vs 0.401 s (18.7× plus lent). La combinaison `latent_d2_centers_k4` réduit davantage les paramètres mais conserve la dégradation de qualité. La variante profonde `deep_9x5` utilise un MLP frais à 34 514 paramètres (ratio 4.002×), et non un comparateur trop petit.

**Conclusion capacité :** les réductions de centres/dimension ne se traduisent pas par un gain de ressources ; elles dégradent la log-loss et le fit reste 14–33× plus long que le MLP apparié.

## 3. Correcteurs OOF de l'Org récursive

| Correcteur | Paramètres sonde / MLP | Ratio | Accuracy sonde / MLP | Log-loss sonde / MLP | Pipeline OOF complet / fit MLP (s) | Ralentissement |
|---|---:|---:|---:|---:|---:|---:|
| temp_bias | 6715 / 27221 | 4.054× | 98.35% / 98.59% | 0.06195 / 0.04791 | 21.86 / 0.401 | 62.0× |
| linear_context | 6778 / 27221 | 4.016× | 98.12% / 98.59% | 0.05765 / 0.04791 | 21.92 / 0.401 | 62.2× |
| rbf_lite_1probe | 6800 / 27221 | 4.003× | 97.88% / 98.59% | 0.05535 / 0.04791 | 21.99 / 0.401 | 62.4× |

Les trois correcteurs conservent le ratio ≥4, mais la log-loss reste 14.7–28.4 % supérieure à celle du MLP dans les comparaisons appariées ; le pipeline reconstruit est autour de 62× plus long. Le RBF-Lite est le meilleur des trois correcteurs Org testés, mais demeure inférieur aux références EX6.

## 4. Ablations causales de l'Org

Le temps ici est le fit direct de l'architecture (pas de génération OOF), comparé au fit MLP de même graine.

| Ablation | Accuracy moyenne | Log-loss moyenne | Fit sonde / MLP (s) | Ralentissement |
|---|---:|---:|---:|---:|
| global_gates_no_lr_mod | 97.65% | 0.07271 | 3.89 / 0.401 | 11.4× |
| inner_coord_only | 98.35% | 0.06360 | 3.23 / 0.401 | 9.3× |
| local_only | 97.65% | 0.07168 | 5.01 / 0.401 | 14.1× |
| outer_coord_only | 98.59% | 0.06013 | 3.43 / 0.401 | 10.0× |
| static_global_coord | 98.35% | 0.05991 | 4.55 / 0.401 | 13.6× |
| uniform_gates_with_lr_mod | 98.35% | 0.06233 | 3.79 / 0.401 | 11.0× |

L'ablation `outer_coord_only` est la meilleure de ces six en log-loss (0.06013), mais reste moins bonne que le MLP (0.04791). `local_only` et `global_gates_no_lr_mod` sont les plus faibles. Aucun bras d'ablation n'est une amélioration qualité-ressources.

## 5. Correction sur sorties d'étages

| Variante | Accuracy moyenne | Log-loss moyenne | Pipeline OOF complet / MLP (s) | Ralentissement |
|---|---:|---:|---:|---:|
| stage_affine_gate | 98.35% | 0.05996 | 22.91 / 0.401 | 65.0× |
| stage_gate_only | 98.35% | 0.06018 | 22.90 / 0.401 | 65.0× |

Le coût du pipeline inclut les trois fits OOF, le fit de la base, le passage supplémentaire d'extraction des logits d'étage (moyenne 1,012 s, parité exacte avec les logits sauvegardés) et l'ajustement du correcteur. Les correcteurs d'étages sont plus légers à ajuster, mais leur chaîne complète est d'environ 22,9 s contre 0,401 s pour le MLP (≈65×), et leur log-loss est dégradée.

## 6. Optimisation du calcul — verdict expérimental

- Vectorisation : parité maximale observée `4.77e-7` ; gain de temps non uniforme selon la taille du batch.
- Processus OOF en parallèle : 27.34 s pour la voie concurrente vs 16.11 s pour la somme séquentielle, sur le CPU testé ; paralléliser les folds est donc négatif ici.
- Threads inter-couches : moins performants que la voie séquentielle vectorisée sur le CPU testé.
- TorchScript : logits identiques sur batch 1/16/64/256 et p50 plus faible qu'en eager ; toujours plus lent que le MLP apparié.
- Quantification dynamique qint8 : métriques presque identiques, mais latence plus lente ; non retenue.
- ONNX, GPU/CUDA : indisponibles dans l'environnement ; `torch.compile` non exécuté.
- FLOPs : comptage incomplet des opérateurs non élémentaires ; ne pas le présenter comme total FLOPs exact.
- RSS, mémoire d'activation, DRAM et énergie : aucune comparaison fiable/mesurée.

## Verdict de ce rapport

Le nombre de paramètres est bien réduit (ratio ≥4 dans les comparaisons présentées), mais cette compacité ne s'est pas convertie en accélération globale. La principale dépense reste la génération OOF, puis l'entraînement des bases récursives. Les correcteurs structurels peuvent préserver une partie de la log-loss pour Emplica, mais ne réduisent pas suffisamment le temps complet. Sur l'expérience Wisconsin de développement seulement, **aucun succès global EX7 n'est établi**.
