# CNG/CNC — statut et résultats du pilote EX9

## Base théorique auditée

`th_sondes_core_test_0.tex` définit AdaptiveRBF (`z=tanh(Wx+b)`, centres KMeans train-only, RBF gaussiennes à largeur positive bornée, lecture linéaire), CNG multi-sondes et CNC en graphe opérationnel. L'audit a détecté les domaines réels d'entrée de noeuds mal spécifiés dans plusieurs tableaux, un risque de mélange interpolation/extrapolation, une normalisation cible non définie, et des ambiguïtés sur la contribution d'une sonde et les deux régimes d'ablation.

`inputs/th_sondes_core_test_1.tex` conserve le texte d'origine et ajoute des règles normatives : extrapolation en shell strict, cibles normalisées train-only, ablations gelées/re-entraînées séparées, CNC généré depuis les entrées primaires indépendantes, domaines exacts ADD/DIV/LOG, séparation C1/C2, aucune dépendance entre succès CNG et exécution CNC. Le document compile via `pdflatex` après ajout de `ragged2e` pour `\\RaggedRight`.

## Pilote effectué (validation seulement)

CNG : `sin(x)` sur [-π,π], 512 train et 192 validation, un seul modèle seed 1501 et une paire de graines données distinctes. Résultats :

| Configuration | M | P_total | MAE validation originale | RMSE validation originale | fit (s) |
|---|---:|---:|---:|---:|---:|
| Single | 1 | 50 | 0,4674 | 0,5412 | 0,119 |
| Mean | 2 | 102 | 0,4574 | 0,5305 | 0,183 |
| Linear composer | 2 | 103 | 0,5129 | 0,6000 | 0,189 |

Le mean-M2 améliore légèrement l'erreur sur ce pilote par rapport à M1, au prix d'environ 2× le nombre de paramètres. Un seul modèle seed et une seule génération n'autorisent aucune conclusion de coopération. Pas de MLP ni d'ablation dans ce pilote.

CNC : six spécialistes RBF M1, un seed chacun, chacun entraîné sur 512 exemples et validé sur 192, avec normalisation cible train-only. ADD est issu du noeud final `u=ab`, `v=exp(c)` du graphe `ab+exp(c)` ; DIV utilise numérateur `[-4,4]` et dénominateur `[-1,-0,25]∪[0,25,3]`; LOG sur [1,9]; EXP sur [-2,2]; MUL/SUB sur domaines primaires [-2,2]^2. MAE/RMSE obtenues :

| Opération | MAE | RMSE | P_total |
|---|---:|---:|---:|
| ADD (graphe 1) | 1,6308 | 2,0588 | 54 |
| SUB | 1,2124 | 1,4621 | 54 |
| MUL | 0,8846 | 1,1997 | 54 |
| DIV | 2,7193 | 3,9728 | 54 |
| EXP | 0,6859 | 1,0577 | 50 |
| LOG | 0,3192 | 0,4295 | 50 |

Ces erreurs reflètent un petit modèle et une seule graine sur les nœuds seuls. La validation du spécialiste DIV est notamment difficile et l'erreur relative serait instable près de zéro. Sa densité n'est pas fidèle à la distribution du graphe malgré les supports corrects ; ce n'est pas un échec ou succès définitif du CNC.

## Ce qui n'a pas été exécuté

- CNG complet sur les quatre fonctions avec M=1/2/4/7, 5 graines et les trois composeurs, ablations gelées et ré-entraînées.
- MLP apparié et ≥4×, AdaptiveRBF direct complet, coût end-to-end homogène.
- CNC graphes finaux C1 spécialistes gelés, C2 fine-tuning conjoint et C3 MLP direct ; métriques de propagation d'erreur par noeud.
- Seeds multiples, test scellé, validation/extrapolation confirmatoire.

Le pilote n'est pas présenté comme confirmation. L'exécution complète reste une priorité ouverte.
