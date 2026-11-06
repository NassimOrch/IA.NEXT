# Rapport final — EX8 v010 : PCA concaténée et récursion V004

Date : 1 novembre 2026. Workspace fixe : `/mnt/data/EX8/versions/sondes_ex8_v010__2026-11-01/`.

## Verdict exécutif

**Statut global : `DÉVELOPPEMENT UNIQUEMENT — VALIDATION EXTERNE NON ÉTABLIE`.** Les expériences A/B Wisconsin sont terminées sur cinq graines communes et toutes leurs comparaisons MLP appariées sont présentes. Les artefacts sont intègres et les métriques se recalculent. Mais le second domaine SMS, historiquement exposé, ne confirme aucun avantage des candidates face aux MLP ; le test confirmatoire est fermé. Les limites OOF non entièrement fold-isolées, l’absence de mesure énergétique/MAC complète et les ablations additionnelles du codebook empêchent un verdict de succès global.

## 1. Périmètre et reprise sans perte

Le prompt EX8 v1.0, les règles des projets antérieurs, le workspace v001 et le dossier v009 incomplet ont été récupérés et archivés sous `inputs/`. Le répertoire versionné est pointé par `/mnt/data/EX8/ACTIVE_VERSION.txt`. Aucun résultat v001 n’a été réentraîné : 60 runs de référence ont été vérifiés et réutilisés. Les expériences non retrouvées dans l’ancienne continuation n’ont pas été traitées comme des résultats : v010 possède ses propres IDs, configurations, historiques, checkpoints, prédictions, hashes et statut append-only.

## 2. Campagne commune

Wisconsin : 341 exemples train, 85 validation, même split, mêmes labels de validation, seeds `[1501,1607,1717,2029,3037]`. 18 bras × cinq seeds = 90 candidates. Les 160 MLP uniques constituent les références de capacité appariée ; chaque candidate se rattache à un MLP proche en `P_total` et à un MLP ≥4×. Les modèles réutilisent un même MLP lorsqu’ils ont exactement le même budget, pas un comparateur sélectionné après coup.

### Résumé A et B

| arm                         |   candidate_log_loss_mean |   candidate_log_loss_sd |   matched_MLP_log_loss_mean |   ge4x_MLP_log_loss_mean |   delta_vs_matched_mean |   wins_vs_matched |   latency_batch1_p50_ms_mean |   P_total_mean |   rbf_centre_evaluations_per_example |
|:----------------------------|--------------------------:|------------------------:|----------------------------:|-------------------------:|------------------------:|------------------:|-----------------------------:|---------------:|-------------------------------------:|
| A0_CORRECTED_PCA2           |                    0.0431 |                  0.0204 |                      0.0543 |                   0.0517 |                 -0.0112 |                 3 |                       0.2028 |       806.0000 |                              56.0000 |
| A1_RBF_LITE_PCA2            |                    0.0676 |                  0.0098 |                      0.0568 |                   0.0517 |                  0.0108 |                 1 |                       0.1692 |       395.0000 |                              16.0000 |
| A2_RBF_LITE_PCA4            |                    0.0831 |                  0.0148 |                      0.0573 |                   0.0519 |                  0.0258 |                 0 |                       0.1717 |       473.0000 |                              16.0000 |
| A3_RETRO_LITE_PCA2          |                    0.0625 |                  0.0098 |                      0.0568 |                   0.0521 |                  0.0057 |                 1 |                       0.1702 |       379.0000 |                              16.0000 |
| A4_RETRO_FULL_PCA2          |                    0.0592 |                  0.0029 |                      0.0540 |                   0.0513 |                  0.0052 |                 0 |                       0.2020 |       760.0000 |                              56.0000 |
| B10_ACTION_LANGUAGE_5P_SOFT |                    0.0414 |                  0.0049 |                      0.0547 |                   0.0508 |                 -0.0133 |                 5 |                       0.3318 |       884.0000 |                              20.0000 |
| B11_ACTION_GATE_5P_K4       |                    0.0444 |                  0.0034 |                      0.0543 |                   0.0522 |                 -0.0099 |                 5 |                       0.1163 |       835.0000 |                              20.0000 |
| B1_NO_OOF_GREEDY            |                    0.0814 |                  0.0051 |                      0.0491 |                   0.0474 |                  0.0323 |                 0 |                       0.7539 |      6742.0000 |                             280.0000 |
| B2_NO_OOF_JOINT             |                    0.0969 |                  0.0072 |                      0.0491 |                   0.0474 |                  0.0477 |                 0 |                       0.7531 |      6742.0000 |                             280.0000 |
| B3_COMPACT15_5L             |                    0.0630 |                  0.0174 |                      0.0525 |                   0.0490 |                  0.0105 |                 1 |                       0.7885 |      2928.0000 |                             120.0000 |
| B4_COMPACT15_3L             |                    0.0695 |                  0.0076 |                      0.0525 |                   0.0501 |                  0.0170 |                 0 |                       0.4760 |      2926.0000 |                             120.0000 |
| B5_COMPACT15_K4             |                    0.0586 |                  0.0180 |                      0.0524 |                   0.0492 |                  0.0062 |                 1 |                       0.6185 |      2508.0000 |                              60.0000 |
| B6_SELECTIVE_L2             |                    0.0699 |                  0.0080 |                      0.0500 |                   0.0465 |                  0.0199 |                 0 |                       0.8128 |      6748.0000 |                             280.0000 |
| B6_SELECTIVE_L2L4           |                    0.0687 |                  0.0061 |                      0.0500 |                   0.0465 |                  0.0187 |                 0 |                       0.8014 |      6754.0000 |                             280.0000 |
| B6_SELECTIVE_L4             |                    0.0687 |                  0.0058 |                      0.0500 |                   0.0465 |                  0.0188 |                 0 |                       0.7571 |      6748.0000 |                             280.0000 |
| B7_VARIANCE_WEIGHT          |                    0.0618 |                  0.0089 |                      0.0500 |                   0.0465 |                  0.0118 |                 0 |                       1.6129 |      6759.0000 |                             280.0000 |
| B8_ACTION_CODEBOOK          |                    0.0619 |                  0.0053 |                      0.0510 |                   0.0478 |                  0.0109 |                 0 |                       1.7241 |      6792.0000 |                             280.0000 |
| B9_RETRO_OUTER              |                    0.0713 |                  0.0112 |                      0.0500 |                   0.0465 |                  0.0213 |                 0 |                       0.8240 |      6755.0000 |                             280.0000 |

## 3. Piste A — PCA concaténée

Le défaut de repère a été réparé : une PCA commune est fit sur `Xtr` et appliquée aux deux partitions ; le contexte global RBF des lignes train est OOF. A0 obtient la meilleure moyenne PCA v010 (0,04307), mais la dispersion par seed est importante et le delta vs MLP apparié (-0,01122) a un IC 95 % qui traverse zéro ; elle ne gagne que 3/5 graines. Elle reste une candidate de développement, pas un modèle supérieur établi.

La réduction RBF d’A0 vers A1 passe de 56 à 16 centres par ligne et accélère batch1 p50 de 0,203 à 0,169 ms, mais la log-loss se dégrade de 0,0431 à 0,0676. A2 PCA4 est encore moins favorable (0,0831). A3 RETRO-lite gagne un peu sur A1 mais demeure derrière MLP ; A4 RETRO-full ne déclenche jamais.

Sur SMS, A0 donne 0,10682 contre 0,07268 pour MLP apparié (5/5 pertes). Son avantage de log-loss ne survit donc pas à cette réplication de second domaine historiquement exposée.

## 4. Piste B — V004 et réduction récursive

La récursion transmet seulement deux logits additionnels : largeur 30 pour la première couche, puis 32 pour les suivantes. Le coût est davantage lié au nombre de probes/centres et à la profondeur sérielle qu’à une explosion dimensionnelle.

- Sans OOF : B1 greedy (0,08140) et B2 joint (0,09686) sont nettement moins bons que les MLP ; le joint est plus rapide au fit (0,87 s) mais plus dégradé.
- Couches compactes : B3 (15 probes, 5 couches) 0,06299 ; B4 (15 probes, 3 couches) 0,06946. Trois couches sont ~40 % plus rapides en latence mais perdent en qualité.
- Réduction K : B5 (15 probes, 5 couches, K4) passe à 60 centres de 120 et p50 0,619 vs 0,789 ms ; log-loss 0,05862. C’est une réduction de calcul intéressante, sans battre MLP moyen.
- OOF sélectif : B6 couches 2/4/2+4 ne gagne pas ; corriger seulement la tête de quelques couches n’élimine pas le coût de création des OOF qui restent le contexte des couches suivantes.
- Variance : B7 ne démontre pas que le désaccord brut soit une mesure de fiabilité ; le coût de fusion augmente et la log-loss reste derrière les MLP.
- B8 : codebook sur récursion entière ; 280 centres toujours calculés et latence plus haute.
- RETRO B9 : aucune activation sélectionnée ; alpha=0 au meilleur checkpoint dans les cinq graines.

Sur SMS, B3 donne 0,10811 contre 0,07609 pour le MLP apparié (5/5 pertes). La récursion compacte ne confirme pas d’avantage sur ce second domaine.

## 5. Piste 5 — coordination codifiée

La formalisation utilise neuf états flous (marge × désaccord), construits depuis quantiles OOF train-only ; une table 9×5 produit des poids continus `softmax` sur cinq logits. Aucun état ne choisit une classe binaire. B10 est comparé à B11, gate standard sur le même backbone 5 probes/1 couche/K4. B10 mean LL 0,04139 contre 0,04443, 5/5 différences favorables, mais les intervalles 95 % et le test ajusté ne permettent pas de conclure à un effet robuste. B10 est 2,85× plus lent que B11. La réduction de calcul est surtout due au backbone léger (20 centres, 1 niveau vs B8 280 centres, 5 niveaux), pas au langage d’actions.

Sur SMS, B10 =0,10020 et B11=0,10349, mais tous deux perdent face aux MLP (0,07413 apparié). La table ajoute un signal de contrôle intéressant, pas un substitut démontré au calcul. Les ablations supplémentaires de seuils, taille d’état et suppression individuelle des signaux sont explicitement `NON EXÉCUTÉES`.

## 6. RETRO

A3 déclenche deux fois sur cinq, A4 zéro fois, B9 zéro fois. Le mécanisme protège donc le début local, mais il est souvent trop tardif ou le signal de maturation trop faible pour que le global contribue au checkpoint choisi. Le monitor B9 observe seulement le gate de la dernière couche, donc il n’est pas suffisant pour juger la maturation de toutes les couches. Aucun résultat RETRO ne valide un avantage général.

## 7. Intégrité, ressources et limites

L’audit indépendant `tests/test_v010_integrity.py` passe. Il vérifie 90 candidates, 160 MLP uniques, 60 runs SMS, cinq graines, les hashes checkpoint/prédiction/historique, les probabilités finies et normalisées, les mêmes labels de validation, les tables d’actions, RETRO, 10 archives ZIP CRC, 1 177 JSON stricts et 155 lignes JSONL. Les écarts de log-loss recalculée sont <1,34e-8 Wisconsin et <3,60e-9 SMS.

Les latences batch 1/16/64/256 sont profilées ; paramètres, bytes de checkpoints, temps de fit et évaluations des centres RBF sont documentés. Les FLOPs/MAC exacts, l’énergie et le RSS complet de chaque processus ne sont pas mesurés. Certaines initialisations K-means supérieures sont transductives sur features train non étiquetées, même si les labels restent OOF. Wisconsin est un split de développement exposé historiquement. SMS est aussi historiquement exposé. Le test reste fermé.

## 8. Décisions et prochaines expériences

1. Conserver A0 corrigée comme candidate exploratoire, sans revendiquer sa supériorité ; prochaine priorité : cross-fit strict de toute initialisation non supervisée et nouvelle validation confirmatoire vierge.
2. Conserver B5 comme piste de réduction K ; tester topologies 2/3/4/5 niveaux en gardant constant le nombre total de centres, puis profiling CPU/GPU robuste.
3. Ne pas remplacer V004 OOF par no-OOF pour l’instant ; les deux variantes testées échouent sur qualité.
4. Pour OOF sélectif, isoler la production des logits OOF (cache partagé) de l’apprentissage des correcteurs afin de mesurer les coûts réutilisables.
5. Garder B10 comme hypothèse de coordination codifiée mais pas comme optimisation prouvée ; faire les ablations signaux, seuils, taille de table et profiler la table optimisée/lookup vectorisé.
6. Pour RETRO, monitorer la maturation agrégée des niveaux (pas seulement la couche finale), et enregistrer alpha de chaque couche ; tester une rampe avec déclencheur train/OOF seulement.

## Conclusion

La campagne v010 A/B est terminée au niveau développement, les fichiers sont audités et ne montrent pas de corruption des sorties entraînées. Les résultats ne prouvent pas une supériorité externe. Le verdict demeure `DÉVELOPPEMENT UNIQUEMENT — VALIDATION EXTERNE NON ÉTABLIE`.
