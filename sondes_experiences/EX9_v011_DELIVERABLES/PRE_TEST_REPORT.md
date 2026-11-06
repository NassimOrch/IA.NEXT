# EX9 v011 — rapport avant ouverture du holdout synthétique

Date de gel : 2026-11-02 (Africa/Algiers). Le holdout ci-dessous n'a pas encore été généré ni consulté à l'heure de rédaction de ce rapport.

## Périmètre gelé

- Domaine unique : `xor8`, généré synthétiquement ; 600 train, 240 validation, test prévu 1 200.
- Générateurs indépendants : train seed 60101, validation seed 60201, holdout seed 60301.
- Graines modèles : 1501, 1607, 1717, 2029, 3037.
- Candidates : B10, B11, A0.
- Bras de comparaison par candidate et graine : MLP apparié en P_total et MLP_GE4X avec ratio vérifié `P_total_MLP/P_total_candidate >= 4`.
- Total attendu : 45 paires JSON/checkpoint (15 candidates + 30 MLP), avec 45 configurations.
- Le modèle, le script d'entraînement, le script d'évaluation du holdout, l'audit, les manifests de split, les configurations, les résultats de validation et les empreintes sont inclus dans le verrou.

## Construction des données

`xor8` utilise X~N(0,I) à 8 dimensions et une frontière générée à partir de `x0*x1 + 0.25*x2 - 0.15*x3 + 0.25*noise > 0`. Le scaler est ajusté exclusivement sur les 600 exemples train. La validation est générée avec une graine distincte. Le test est synthétique et ne permet en aucun cas de conclure à une généralisation sur des données réelles.

## Résultats validation gelés

| Candidate | LL candidate | LL MLP apparié | LL MLP ≥4× | P candidate | P MLP ≥4× | Fit candidate (s) | p50 batch 1 E2E (ms) |
|---|---:|---:|---:|---:|---:|---:|---:|
| B10 | 0.549981 | 0.314458 | 0.300874 | 400 | 1602 | 1.2511 | 0.4076 |
| B11 | 0.554089 | 0.306784 | 0.301720 | 351 | 1404 | 0.7123 | 0.2326 |
| A0 | 0.450060 | 0.303134 | 0.304630 | 608 | 2438 | 1.7319 | 0.4105 |

Chaque candidate a une log-loss supérieure aux deux MLP comparateurs sur les cinq graines de cette validation synthétique. Ce constat est limité à `xor8`, au générateur, aux splits et à l'implémentation décrits. Il ne réfute pas les résultats historiques Wisconsin EX8 ni ne les confirme.

Les ratios de paramètres MLP_GE4X/candidate sont respectivement 4.005 (B10), 4.000 (B11) et 4.0099 (A0). L'avantage de taille est donc correctement mis en place, mais il n'est pas accompagné ici d'une qualité équivalente. Les MLP sont aussi nettement plus rapides en inférence batch 1 sur cette implémentation CPU ; le coût PyTorch/KMeans des sondes est élevé relativement à ce petit modèle.

## Statut statistique

Les cinq initialisations modèle partagent les mêmes splits train/validation. Elles ne sont pas cinq datasets indépendants. Les résultats sont développement/sélection. Le test synthétique est réservé à une unique notation après gel ; il ne sert pas à choisir ou modifier des modèles. Aucun domaine réel externe neuf n'a été disponible hors-ligne.

## Contrôles préalables

- 45 fichiers résultats JSON et 45 checkpoints complets.
- 45 fichiers de configuration dérivés des métadonnées effectivement persistées et de la source d'entraînement.
- MLP_GE4X vérifié arithmétiquement à au moins 4× pour chaque candidate/graine.
- Recalcul indépendant des 45 log-loss validation : PASS, écart maximal 0 après calcul stable sur les prédictions enregistrées.
- Aucun fichier ne marque `test_opened=true`.

## Limites / déviations restantes

- Un seul domaine synthétique de classification, aucun benchmark réel confirmatoire.
- Le profil de latence utilise 20 warmups/40 mesures ; p95/p99 sur 40 mesures restent peu précis.
- L'audit CPU est sur cet environnement seulement ; pas de GPU, d'énergie ni de profilage matériel indépendant.
- CNG/CNC sont pilotes séparés sur validation uniquement et ne font pas partie du holdout classification.
