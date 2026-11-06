# A0/PCA — audit historique et réplication

## Définition historique EX8

A0 utilise une PCA2 unique ajustée sur X_train et appliquée dans la même base à train/validation. La PCA est concaténée aux probabilités globales OOF d'une AdaptiveRBF D4/K8 ; six sondes locales D4/K8 reçoivent cette représentation. Le global OOF compte cinq folds. Le modèle global plein prédit validation. Le nombre d'évaluations de centres RBF est 56/exemple. P_total historique 806. La première version partageait un artefact global ancien V001 ; le coût historique de formation complète n'était pas intégralement attribué à A0, ce qui doit être corrigé en EX9.

Sur Wisconsin EX8, LL moyenne 0,0430683 (sd 0,0204202), 3/5 gagnants vs MLP apparié ; IC de la différence inclut zéro. Sur SMS, la candidate perd vs MLP, et SMS est historiquement exposé. A1 RBF-lite PCA2 et A2 PCA4 réduisent les évaluations 56→16, mais leurs LL (0,067596 et 0,083119) sont moins bonnes. A3 RETRO-lite LL 0,062473 ; déclenchement seulement 2/5. A4 RETRO-full LL 0,059165 ; aucun déclenchement. Ces résultats ne justifient pas la supériorité.

## Réplication synthétique EX9

Sur xor8, A0 obtient LL 0,450060, contre 0,303134 MLP apparié et 0,304630 MLP_GE4X. A0 perd dans les 5 graines. P_total 608 ; MLP_GE4X 2 438 (ratio 4,0099). Temps de fit complet moyen 1,732 s ; p50 E2E batch1 0,411 ms contre environ 0,018 ms pour les MLP. Variance inter-graines élevée (sd LL 0,11415).

## Réserve technique

Les folds OOF Rev2 sont fixés à 100 époques sans accès aux labels held-out ; KMeans/encodeur sont ajustés fold-train uniquement. Le modèle final global utilise une sélection sur validation, ce qui est acceptable pour le modèle final, distinct de l'OOF. Les initialisations transductives d'autres pistes doivent être étiquetées explicitement et ablatées fold-pure lorsque possible.


## Extension multi-domaines synthétiques

A0 a été exécutée sur `concentric2` et `rotated_moons2`, chacune avec cinq seeds, un MLP apparié et un MLP_GE4X par seed. En validation, A0 donne 0,199706 sur concentric2 et 0,269514 sur rotated_moons2, contre 0,039272/0,042231 et 0,153671/0,153051 pour ses MLP. Sur les tests synthétiques scellés, A0 obtient 0,200912 (accuracy 0,9228) et 0,232610 (accuracy 0,9170), contre 0,059220/0,060707 et 0,121618/0,121019 pour les MLP. A0 perd 5/5 graines contre les deux comparateurs dans les deux domaines. Les IC bootstrap appariés des différences test sont entièrement positifs. A0 reste plus compacte que le MLP_GE4X, mais ne satisfait pas la qualité ni la vitesse (p50 batch1 autour de 0,29–0,35 ms contre ~0,017–0,018 ms MLP).
