# Dossier complet B10 — langage d’actions codifiées (EX8 v010)

Ce dossier complémentaire rassemble le code, les configurations, les données d’entraînement/validation autorisées, les checkpoints, les prédictions, les historiques et les comparateurs MLP pour B10 et son contrôle B11. Le paquet global EX8 v010 contient en plus toutes les autres variantes A0–A4 et B1–B9.

## Résultat B10 sur Wisconsin (5 graines)

| Graine | B10 log-loss | B11 gate standard | MLP apparié B10 | MLP ≥4× B10 |
|---:|---:|---:|---:|---:|
| 1501 | 0.04507602 | 0.04639599 | 0.05309571 | 0.05388297 |
| 1607 | 0.03892050 | 0.03918663 | 0.05443205 | 0.05022439 |
| 1717 | 0.03475841 | 0.04361378 | 0.05260622 | 0.05136449 |
| 2029 | 0.04704858 | 0.04824928 | 0.05549038 | 0.05049692 |
| 3037 | 0.04114467 | 0.04468064 | 0.05801149 | 0.04804699 |

Moyennes : B10 **0.04138964**, B11 **0.04442526**, MLP apparié B10 **0.05472717**, MLP ≥4× **0.05080315**. B10 bat son MLP apparié sur **5/5 graines** et le MLP ≥4× sur **5/5 graines**.

## Architecture B10

- Un seul niveau, cinq probes parallèles.
- Dimension latente D=4, K=4 centres par probe.
- 20 évaluations de centres RBF par observation.
- État flou 3×3 construit à partir de la marge OOF et du désaccord inter-probes.
- Une table 9×5 produit des poids continus softmax sur les cinq vecteurs de logits ; le codebook ne décide jamais la classe.
- 45 paramètres d’action ; total déclaré 884 paramètres.
- Les seuils sont estimés uniquement sur les signaux OOF du train.

## Comparaison statistique B10 vs B11

Delta moyen (B10 − B11) = **-0.00303563**. Les cinq différences par graine sont négatives, mais l’IC t apparié à 95 % [-0.00734137, 0.00127012] recouvre zéro ; le test exact de permutation des signes bilatéral donne p=0.0625. L’avantage observé doit donc rester qualifié d’encourageant mais exploratoire.

Latence p50 batch 1 moyenne : B10 0.331801 ms ; B11 0.116289 ms ; ratio B10/B11 **2.853×**. Le mécanisme d’actions est plus lent que le gate standard.

## Fichiers inclus

- `workspace/src/` : scripts d’exécution et moteur partagé.
- `workspace/configs/` : pré-enregistrement B10/B11 et configurations par graine.
- `workspace/inputs/` : code commun et Wisconsin train/validation only.
- `workspace/results/metrics/` : métriques candidates, MLP, comparatif direct et agrégats.
- `workspace/results/models/` : checkpoints B10, B11, backbone et MLP appariés/≥4×.
- `workspace/results/raw/` : prédictions et historiques B10/B11/backbone/MLP disponibles.
- `B10_B11_PAIRED_RESULTS.csv` : table condensée par graine.
- `SHA256SUMS.txt` : manifeste d’intégrité du dossier.

## Limites

Les chiffres sont des résultats de développement sur la partition Wisconsin, pas une validation externe confirmatoire. La réplication SMS est historiquement exposée et B10 n’y bat pas les MLP. Le test indépendant n’a pas été ouvert dans cette campagne. Les checkpoints et prédictions fournis permettent l’inspection et la vérification des métriques ; une reproduction exacte de l’environnement exige les versions de bibliothèques et le matériel documentés dans la configuration système du workspace complet.
