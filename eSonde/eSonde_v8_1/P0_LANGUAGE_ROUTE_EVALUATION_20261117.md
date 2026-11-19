# Évaluation du routage linguistique OASST1 — 17 novembre 2026

## Description
Deux évaluations non neuronales du routage de langue du dernier tour USER ont été exécutées. Elles évaluent l'attribution d'une route linguistique, pas la génération de texte ni la cohérence d'une réponse.

## Architecture
Les priors linguistiques sont calculés sur le TRAIN uniquement. Le routage lit le dernier tour USER, combine des fréquences unigrammes relatives aux priors globaux et des indices Unicode explicites de script pour les alphabets non ambigus. Les seuils et fenêtre sont choisis sur VALIDATION uniquement ; TEST est réservé. Le fichier de priors livré au runtime a SHA-256 `8b769436d13b31ce9b8639720bf97a902b35bed82a17c7b4f713ad0739d15e91`.

## Pipeline
1. Construire les priors de dernier tour USER avec OASST1 TRAIN.
2. Dédupliquer les contextes de validation par hash et sélectionner la fenêtre/seuils sur VALIDATION.
3. Geler la politique.
4. Évaluer sur TEST dédupliqué, sans réajuster les seuils.

## Résultats — politique latest-user retenue
- Fenêtre : 24 tokens ; indice de script direct activé.
- Seuils gelés : min_tokens=1, min_coverage=0,05, min_margin=0,03.
- VALIDATION : 1 004 contextes uniques, 996 routés, couverture 99,20 %, exactitude sélective 99,10 %, part correcte sur tous les contextes 98,31 %.
- TEST : 1 080 contextes uniques, 1 068 routés, couverture 98,89 %, exactitude sélective 99,25 %, part correcte sur tous les contextes 98,15 %.
- Aucun conflit de labels entre doublons de contexte sur VALIDATION ou TEST.
- TEST non utilisé pour choisir les seuils.
- Résultat TEST SHA-256 : `c7f6e58c9004fafcf8c6700fb3a891fe78302a6654cce82d9b7c6e9445f0d197`.

## Évaluation de route v1
Une évaluation distincte sur les lignes complètes a comparé la route de base et 120 variantes admissibles. La sélection était basée sur VALIDATION avec couverture minimale de 30 % ; TEST n'a pas servi à choisir les seuils. Les métriques détaillées et matrices de confusion sont dans `oasst1_language_route_eval_20261117.json` et `oasst1_language_route_test_20261117.json`.

## Interprétation
Les résultats établissent une bonne attribution de route sur les contextes OASST1 tree-isolated évalués. Ils n'établissent pas que la route améliore les continuations, la pertinence, la cohérence ou la généralisation du dialogue. Les groupes de faible effectif et les scripts/alphabets proches doivent rester inspectés par langue. Le routage est un sous-système du runtime, pas une preuve d'intelligence dialogique.

## Conséquences
- Théoriques : distinguer classification de route et génération de réponse.
- Conceptuelles : ne pas présenter un taux de bonne langue comme une mesure de compréhension.
- Opérationnelles : l'intégration utilise le dernier tour USER et les priors validés par hash ; des ablations de génération restent nécessaires.

## Statut
`LANGUAGE_ROUTE_COMPONENT_EVALUATED`; free-running coherence remains `NON_EVALUE`.
