# Architecture et lignée — PCA concaténée, V004, RETRO, langage d’actions

## A — PCA concaténée

La faille de la construction précédente était la concaténation de composantes PCA apprises dans des sous-espaces de folds distincts. Le signe d’une composante ne résout pas la rotation/mélange au sein d’un sous-espace. En v010, une seule PCA est ajustée sur les 341 vecteurs `Xtr` ; cette base est ensuite appliquée sans réajustement à `Xtr` et `Xva`. Le global RBF fabrique des sorties OOF pour le train et une sortie issue du modèle complet pour validation. Le local voit `[PCA(X), global(X)]` et concatène le contexte global avec les features locales.

A0 : PCA2, global D4/K8, six sondes locales D4/K8, 56 évaluations de centres RBF environ par observation. A1 : RBF-lite D3/K4, trois sondes locales, PCA2, 16 évaluations. A2 : même RBF-lite mais PCA4. A3 : A1 avec alpha RETRO. A4 : A0 avec alpha RETRO.

## B — récursion V004

La couche 1 consomme 30 dimensions. Chaque couche suivante reçoit les 30 features d’origine et exactement deux logits transmis par la précédente, soit 32 dimensions ; la dimension ne croît plus ensuite. Pour chaque couche `l`, les probes produisent des logits `q_lj`, un gate interne `softmax(a_l)` forme `h_l = sum_j gate_lj q_lj`, et l’état récursif s’accumule par `r_l = r_(l-1) + h_l`. Le readout final forme un mélange pondéré des `h_l`. La topologie V004 `[1,3,6,10,15]` compte 35 probes, 5 couches et 280 évaluations de centres avec K=8.

- B1 : empilement greedy sans OOF ; les sorties in-sample nourrissent la couche suivante.
- B2 : entraînement conjoint sans OOF.
- B3 : 15 probes `[1,2,3,4,5]`, cinq couches, K=8.
- B4 : 15 probes `[1,4,10]`, trois couches, même nombre de probes/centres que B3.
- B5 : 15 probes/five layers, K=4, moitié du nombre de centres de B3.
- B6 : correcteurs uniquement sur les couches 2, 4, ou 2+4 ; les features OOF des couches non corrigées restent nécessaires au chaînage.
- B7 : poids continus de couche pénalisés par le désaccord OOF.
- B8 : table d’actions 3×3 sur la récursion complète.
- B9 : readout global RETRO, alpha démarre à zéro.
- B10/B11 : test isolant de coordination à cinq probes parallèles et un seul étage ; B10 table d’actions floue 9×5, B11 gate softmax standard. Ce n’est pas une reconstruction récursive V004 complète.

## Piste 5 — action language

L’état est défini par deux signaux continus calculés sur les sorties OOF train : marge de confiance et dispersion inter-probes. Les quantiles tiers forment trois appartenances floues pour chaque axe ; leur produit donne neuf états flous. Une table 9×5 retourne des poids `softmax` continus sur les cinq vecteurs de logits. Le code ne choisit pas la classe et ne transforme pas le problème en action binaire. La table est optimisée sur le train OOF par cross-entropy et régularisation vers le gate uniforme. Tous les paramètres/lookup/table et calculs de membership sont comptés.

Limitation : dans v010, l’architecture B10/B11 porte déjà la majeure partie de la réduction du coût ; la table d’actions est plus lente que le gate standard à backbone identique. Les contrôles de seuils et de cardinalité supplémentaires restent à mener.
