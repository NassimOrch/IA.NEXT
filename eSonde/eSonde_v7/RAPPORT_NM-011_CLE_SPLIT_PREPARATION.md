# Rapport d'incident NM-011 — clé de réconciliation des partitions dans la préparation conditionnelle

## 1. Description
Lors d'une exécution `--prepare-only` du pipeline d'apprentissage conditionnel, la préparation des textes et des exemples conversationnels est arrivée à son terme, mais la construction du résumé final s'est interrompue sur un `KeyError: 'split_counts'`.

## 2. Architecture concernée
Le script `Amodel_eSonde_v7/tools/train_conditional_obsiss.py` appelle le chargeur canonique `egenbrain.train.load_records`, puis expose les tailles de partitions sous la clé `chat_split_counts`. Le résumé de préparation cherchait à tort `split_counts`.

## 3. Pipeline complet
1. Charger le jeu eGenBrain par le chargeur officiel.
2. Dédupliquer les paires par contenu et conserver le split canonique.
3. Séparer chat TRAIN/VALIDATION/TEST.
4. Charger exclusivement les textes MTEB TRAIN et dériver un holdout interne déterministe.
5. Construire tokenizer et caractéristiques causales.
6. Projeter les 16 observations via les lignes P/R v6 en lecture seule.
7. Construire exemples LM et chat conditionnel.
8. Composer le rapport de préparation.
9. L'erreur est survenue à l'étape 8, à cause du mauvais nom de clé.

## 4. Commandes d'exécution
Commande exécutée :

```bash
PYTHONPATH=Dmodel_eSonde_v7/src python -u Amodel_eSonde_v7/tools/train_conditional_obsiss.py \
  --source-root /mnt/data/work_esonde_v7 \
  --v6-model-dir Dmodel_eSonde_v7/models/eSonde_v6 \
  --output Dmodel_eSonde_v7/models/eSonde_v7/conditional_checkpoint.json \
  --initial-obsiss 10 --prepare-only --max-vocab 1024 --max-units 160
```

## 5. Résultats
Le journal confirme le traitement des 13 759 textes TRAIN retenus et des 13 paires de chat TRAIN. Le script s'est arrêté au rapport avec `KeyError: 'split_counts'`. Aucun fichier checkpoint conditionnel n'a été écrit ; le mode `--prepare-only` n'importe pas PyTorch, n'initialise aucun paramètre et n'entraîne aucun poids.

## 6. Interprétation des résultats
Il s'agit d'un défaut de contrat entre deux noms de champ dans l'instrumentation. Le chargeur source expose `chat_split_counts`, déjà vérifié comme 13/1/3. Les données et exemples préparés ne sont pas des résultats d'entraînement.

## 7. Conséquences
- **Théorique :** aucune conséquence sur la définition du modèle ou les données sources.
- **Conceptuelle :** aucune modification de l'objectif conditionnel.
- **Opérationnelle :** correction de la clé du résumé ; un test de réconciliation devra garantir que les partitions affichées correspondent aux partitions canoniques.

## 8. Conclusion
Incident d'instrumentation reproduit et corrigé dans le script. Aucun poids, résultat antérieur ou fichier source n'a été perdu ou modifié. La préparation doit être relancée pour obtenir un rapport complet.

## 9. Statut du modèle
**NON EXÉCUTÉ / NON ENTRAÎNÉ pendant cet incident.** P2 reste `IN_PROGRESS`. Aucun jugement sur la qualité ou le potentiel de eSonde v7 n'est tiré de cet incident.
