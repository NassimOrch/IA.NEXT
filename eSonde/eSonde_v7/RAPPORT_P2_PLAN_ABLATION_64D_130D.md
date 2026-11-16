# Plan expérimental P2 — ablation 64D / 130D

**Date locale :** 2026-11-14T20:55:22.890670+01:00  
**Statut :** `PLANNED_NOT_EXECUTED` — aucun entraînement enregistré dans ce rapport.

## 1. Description
Tester si deux Obsiss sentinelles individualisées apportent au décodeur conditionnel une information utile en plus des statistiques collectives de la population active. L'objectif est de comparer la synthèse 64D à la représentation 130D, sans présumer du résultat.

## 2. Architecture
- Variante A : 64D = moyenne et écart-type des vues P/R de dix Obsiss actives.
- Variante B : 130D = mêmes 64D + deux slots P/R individualisés (indices originaux attendus `[2,4]`) + masques de présence.
- Les paramètres conditionnels sont un GRU entraînable. Les poids V6 restent immuables et servent uniquement de banque Obsiss.

## 3. Pipeline complet
1. Charger les sources via le chargeur canonique eGenBrain.
2. Employer les splits TRAIN/VALIDATION ; ne jamais lire TEST.
3. Utiliser les mêmes données, tokenizer, graines, dimensions du GRU, optimiseur, epochs et poids de loss pour les deux variantes.
4. Entraîner séparément les deux transducteurs.
5. Exporter les paramètres et leur provenance.
6. Charger chaque checkpoint dans l'inférence Python standard et faire un test de pas GRU, sans dialogue public.
7. Comparer les métriques par tâche et les coûts.

## 4. Commandes d'exécution
Les deux commandes exactes sont inscrites dans `experiments/P2_ABLATION_64D_VS_130D_PLAN_20261114.json`. La commande 64D ajoute `--no-sentinel-panel`; la commande 130D utilise `--panel-size 2`. Tous les autres paramètres sont identiques : seed 20261114, 4 epochs, batch 32, embedding 24, hidden 48, `chat_loss_weight=8`, `qa_loss_weight=1.5`, population 10.

## 5. Résultats
Aucun résultat à ce stade. La préparation 130D est documentée dans `RAPPORT_P2_PREPARATION_CHAT_MATHQA_PANEL130.md`. Les paramètres n'ont pas encore été entraînés dans le cadre de ce plan.

## 6. Interprétation prévue
La perplexité de validation est une métrique de prédiction de tokens, non une mesure exhaustive de cohérence. Le split chat ne compte qu'une paire de validation : la métrique chat sera descriptive, pas un estimateur fiable de généralisation créative. MathQA garde sa métrique distincte.

## 7. Conséquences
- **Théoriques :** comparer visibilité individuelle contre agrégation seule.
- **Conceptuelles :** les sentinelles restent des voix Obsiss originales, non des poids ordinaires ni des arbitres.
- **Opérationnelles :** 130D n'est retenu dans le runtime que si l'ablation donne un bénéfice mesurable justifiant son coût ; sinon le résultat 64D est conservé comme variante plus simple.

## 8. Conclusion
Plan préenregistré ; aucune préférence de variante n'est décidée avant les résultats.

## 9. Statut du modèle
`P2_ABLATION_PLANNED`; phase P2 `IN_PROGRESS`. La population de départ est dix ; un million n'est pas une cible obligatoire.
