# Rapport NM-010 — Interruption temporelle du prétraitement conditionnel

## 1. Description
Une commande de préparation seule (`--prepare-only`) s'est interrompue à la limite de 120 secondes de l'environnement. Elle était destinée à charger, tokeniser et featuriser les données ; elle ne devait ni initialiser le réseau ni mettre à jour des paramètres.

## 2. Architecture
Le préparateur construit, pour chaque unité, un vecteur causal de 16 observations puis le projette à travers les lignes P/R originales des Obsiss pour obtenir 64 caractéristiques (moyennes et dispersions P/R). La première implémentation invoquait la projection Obsiss séparément pour chaque unité, ce qui répétait des opérations de tableau sur de très petits lots.

## 3. Pipeline complet
1. Charger les paires canoniques de chat et les textes TRAIN multilingues.
2. Construire les unités du tokenizer mots/octets.
3. Construire les observations causales sans lire les tokens cibles futurs.
4. Projeter les observations à travers les lignes Obsiss originales en lecture seule.
5. Accumuler les exemples préparés.
6. L'environnement interrompt le processus à 120 secondes avant la fin de la préparation.
7. Remplacer les projections unitaires par `project_many`, qui vectorise la projection pour une séquence entière et conserve le repli standard-library.

## 4. Commandes d'exécution
Commande interrompue :

```bash
PYTHONPATH=src python ../Amodel_eSonde_v7/tools/train_conditional_obsiss.py \
  --source-root /mnt/data/work_esonde_v7 --prepare-only \
  --max-units 128 --initial-obsiss 10
```

L'optimisation `project_many` est maintenant intégrée dans `src/esonde_v7/learned/obsiss_adapter.py`. Une nouvelle mesure complète est encore nécessaire.

## 5. Résultats
- La commande s'est terminée par le timeout de 120 secondes.
- Aucun statut `PREPARATION_ONLY` final n'a été écrit.
- Aucun checkpoint conditionnel n'a été créé par cette commande.
- Aucun paramètre du GRU n'a été initialisé ni entraîné.
- Le fichier de poids v6 est ouvert en lecture seule et son SHA-256 attendu reste `8526943d1528418fa8bbbf9128b61b5e1acd90a16eeb7cc062e18864b083dff4`.
- L'optimisation vectorisée a été écrite après l'interruption ; elle n'est pas encore validée par une nouvelle préparation complète.

## 6. Interprétation des résultats
Le délai observé est un incident opérationnel du prétraitement, pas un résultat de qualité du modèle. Le goulot le plus probable est la répétition d'opérations NumPy pour chaque unité, mais la cause ne sera tenue pour confirmée qu'après la nouvelle mesure instrumentée.

## 7. Conséquences
- **Théorique :** aucun effet sur le formalisme ou les paramètres du modèle.
- **Conceptuelle :** le mécanisme d'observation reste identique ; seule son exécution est vectorisée.
- **Opérationnelle :** `project_many` réduit le nombre d'appels de projection et convertit le résultat vers un tableau compact `float16`. Le résultat doit être comparé numériquement à `project`.

## 8. Conclusion
Préparation interrompue sans entraînement ni modification du modèle. Une optimisation a été ajoutée, mais son gain n'est pas déclaré acquis avant retest.

## 9. Statut du modèle
`PREPROCESSING_TIMEOUT_OPTIMIZATION_ADDED_RETEST_PENDING`. Aucun fichier, poids ou résultat antérieur n'a été perdu.
