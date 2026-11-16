# Rapport P2 — préparation conditionnelle chat/Q-R avec panel Obsiss 130D

**Identifiant :** `P2_PREPARATION_CHAT_MATHQA_PANEL130_20261114`  
**Statut :** `PREPARATION_ONLY_PASS` — aucun paramètre conditionnel initialisé, aucun entraînement exécuté.  
**Log :** `experiments/logs/P2_PREPARE_CHAT_MATHQA_PANEL130_OPT_20261114.log`

## 1. Description
Préparer un transducteur paramétrique qui apprend à prolonger un échange utilisateur→assistant. La préparation inclut les exemples créatifs `chat` et les problèmes `math_qa` comme tours Q/R dans la même interface chat. Les objectifs et les partitions restent distingués. Elle étudie aussi deux voix Obsiss individualisées dans le vecteur de conditionnement.

## 2. Architecture
- 16 observations causales par position ; aucune cible future consultée.
- Projection 130D : 64D (moyennes et dispersions P/R de toutes les Obsiss actives), 32D pour chaque sentinelle, 2 masques de présence.
- Sentinelles sélectionnées par sondage borné sur les 10 Obsiss actives : indices originaux `[2, 4]` ; sonde `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]`.
- GRU conditionnel partagé prévu pour l’apprentissage. L’interface utilisateur reste seulement le chat.
- Poids de perte déclarés : LM=1, chat créatif=8, math Q/R=1,5. SMS classification exclue.
- Aucune table de réponses à l’inférence ; les poids v6 sont en lecture seule.

## 3. Pipeline complet
1. Lecture des chemins, checklists et registre de sauvegarde.
2. Chargeur canonique `egenbrain.train.load_records`, déduplication et réconciliation par tâche.
3. Préservation des splits `chat` 13/1/3 et `math_qa` 5 978/747/748.
4. Exclusion des 105 502 paires canoniques `sms_classification`.
5. Chargement MTEB TRAIN uniquement, validation interne déterministe.
6. Tokenizer TRAIN-only et repli UTF-8 octet.
7. Construction des séquences Q/R et du masque de loss portant seulement sur la réponse assistant.
8. Projection 130D et cache LRU 50 000 observations.
9. Contrôle des volumes, hashes et partitions.
10. Arrêt `PREPARATION_ONLY`, sans importer PyTorch et sans initialiser de paramètres.

## 4. Commandes d'exécution

```bash
PYTHONPATH=Dmodel_eSonde_v7/src python -u Amodel_eSonde_v7/tools/train_conditional_obsiss.py \
  --source-root /mnt/data/work_esonde_v7 \
  --v6-model-dir Dmodel_eSonde_v7/models/eSonde_v6 \
  --output /tmp/preparation.json --initial-obsiss 10 --prepare-only \
  --max-vocab 1024 --max-units 256 --chat-loss-weight 8.0 \
  --qa-loss-weight 1.5 --panel-size 2 --projection-cache-entries 50000
```

## 5. Résultats

| Indicateur | Résultat observé |
|---|---:|
| Séquences TRAIN | 24,777 |
| Séquences VALIDATION | 2,136 |
| LM TRAIN | 13,759 exemples ; 1,419,711 tokens |
| Chat TRAIN | 289 segments ; 43,874 tokens |
| Math Q/R TRAIN | 10,729 segments ; 1,238,448 tokens |
| LM VALIDATION | 764 exemples ; 78,428 tokens |
| Chat VALIDATION | 15 segments ; 2,247 tokens |
| Math Q/R VALIDATION | 1,357 segments ; 156,548 tokens |
| Vocabulaire | 1,291 identifiants |
| Projection | 130D |
| Cache | 3,913,962 hits ; 48,962 misses ; 48,962 entrées |
| Split chat | 13 / 1 / 3 |
| Split math_qa | 5 978 / 747 / 748 |

Le hash des poids v6 est `8526943d1528418fa8bbbf9128b61b5e1acd90a16eeb7cc062e18864b083dff4` ; le champ `model_parameters_initialized` vaut `false` et `training_executed` vaut `false`.

## 6. Interprétation des résultats
La préparation technique est achevée et les partitions sont réconciliées. Les 5 978 paires mathématiques apportent un volume conditionnel nettement plus grand, mais leur domaine est spécialisé ; elles ne doivent pas être interprétées comme une preuve de dialogue général. Les 13 exemples `chat` TRAIN sont anglais et créatifs ; les trois exemples test restent hors apprentissage. Le panel individualisé préserve deux voix dans le vecteur, mais son apport génératif ou correctif n’a pas encore été mesuré. Le cache réduit les projections répétées sans changer les observations logiques.

## 7. Conséquences
- **Théoriques :** la combinaison des statistiques collectives et de deux vues individuelles devient accessible au transducteur ; l’utilité de ces composantes reste une hypothèse testable.
- **Conceptuelles :** les sources mathématiques sont traitées comme des tours chat Q/R ; elles ne créent pas un second produit ou une option d’interface.
- **Opérationnelles :** les poids originaux restent immuables ; la préparation est reproductible ; les pertes et métriques devront être rapportées séparément par source. Le split TEST n’est pas utilisé.

## 8. Conclusions
La préparation 130D sur l’ensemble des données Q/R retenues passe. Le premier essai sans cache s’était arrêté pendant la préparation étendue ; l’optimisation bornée (256 unités, cache 50 000) a permis de terminer le traitement complet. Aucun paramètre conditionnel n’a été entraîné dans cette expérience.

## 9. Statut du modèle
**`CONDITIONAL_DATA_PREPARED_130D_NOT_TRAINED` — P2 `IN_PROGRESS`.** Le prochain jalon est l’entraînement sauvegardé, l’évaluation de validation distincte, l’ablation agrégat64/panel130 et la génération sur TEST sans consulter les réponses cibles.
