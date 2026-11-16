# Protocole d'évaluation de cohérence — eSonde v7

## 1. Principe

La qualité du chat doit être évaluée par rapport au prompt et au contexte réel, pas par le seul score interne des Obsiss. Les évaluations doivent être reproductibles et menées sans réponse cible dans la fonction de génération.

## 2. Dimensions à mesurer

| Dimension | Question évaluée | Mesure proposée |
|---|---|---|
| Pertinence locale | La réponse traite-t-elle la demande ? | annotation aveugle 1–5, couverture des sous-questions |
| Continuité multi-tours | Reprend-elle correctement les éléments antérieurs ? | résolution de références et continuité évaluées par annotateurs |
| Fidélité référentielle | Les entités et faits du dialogue sont-ils conservés ? | contradictions et erreurs référentielles comptées |
| Non-contradiction | La réponse contredit-elle les tours précédents ? | annotation, contradicteurs ciblés |
| Cohérence temporelle | Les ordres et dates restent-ils compatibles ? | jeux de dialogue temporels et annotation |
| Complétude | Les éléments demandés sont-ils traités ? | couverture par item de demande |
| Fluidité | La réponse est-elle lisible et grammaticale ? | évaluation humaine et métriques linguistiques auxiliaires |
| Généralisation lexicale | Le modèle traite-t-il des formes hors vocabulaire ? | taux OOV et qualité morphologique annotée |
| Calibration | Les signaux de désaccord correspondent-ils à l'incertitude humaine ? | corrélation, courbes de calibration après annotation |
| Efficacité | Quel coût de calcul est requis ? | latence p50/p95, tokens/s, RSS, coûts de chargement |

## 3. Préenregistrement

Avant toute campagne, figer : checkpoint et hash ; version du code ; corpus et splits ; prompts et historiques ; langues ; budgets de tokens, faisceau et Obsiss ; politique non-réponse ; nombre de répétitions ; critères d'exclusion ; comparateurs ; métriques et méthode d'agrégation. Les prompts utilisés pour le développement ne doivent pas être reclassés en test final.

## 4. Comparateurs

Au minimum : eSonde v6, un baseline n-gramme/PPMI sans Obsiss, eSonde v7 avec ablations ciblées, et un ou plusieurs LLM explicitement nommés et versions fixées. Tous reçoivent exactement les mêmes messages et consignes. Les budgets doivent être comparables et déclarés ; si le coût intrinsèque ne peut être égalisé, les deux axes coût/qualité sont publiés.

## 5. Aveugle et notation

Les sorties sont anonymisées et mélangées. Deux annotateurs indépendants évaluent chaque réponse ; les désaccords sont conservés et arbitrés selon une règle préenregistrée. Il faut publier les critères, exemples limites, cohérence inter-annotateurs, intervalles et distribution complète des notes.

## 6. Anti-fuite

Aucune réponse de référence ni étiquette de test n'est accessible au code de génération. Les partitions de test restent hors des statistiques TRAIN. Le registre de provenance doit préciser toutes les sources, déduplications, filtres, exclusions et hashes.

## 7. Rapport

Tout résultat suit les neuf rubriques dans `REPORT_TEMPLATE.md`. Les métriques internes `collective_rank_score`, `observer_disagreement` et `P_R_cosine_diagnostic_only` sont des diagnostics du système, jamais des scores de vérité ou de cohérence humaine.
