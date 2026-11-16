# Rapport P2 — préparation du transducteur conditionnel Obsiss

## 1. Description
Préparer de manière reproductible un modèle paramétrique prompt/contexte → réponse. Cette expérience est strictement `--prepare-only` : elle construit les exemples et les caractéristiques, mais n'importe pas PyTorch, n'initialise aucun paramètre et n'entraîne aucun poids.

## 2. Architecture
Le prototype comprend un tokenizer mot/octet appris sur TRAIN, 16 observations causales, une projection Obsiss P/R (moyenne et dispersion des observations de l'ensemble actif, soit 64 caractéristiques), puis un GRU conditionnel prévu pour l'entraînement ultérieur. Le runtime d'inférence visé reste Python standard et ne possède aucune table de réponses.

## 3. Pipeline complet
1. Appel du chargeur canonique `egenbrain.train.load_records`.
2. Filtrage des exemples `task=chat` après déduplication, en conservant le split canonique.
3. Séparation de 13 paires TRAIN, 1 validation et 3 test.
4. Chargement du seul fichier MTEB `train/train.json` et création d'un holdout déterministe interne : 13 759 textes TRAIN, 764 textes de validation.
5. Construction du vocabulaire sur TRAIN uniquement ; les mots inconnus sont codés en UTF-8 par octets.
6. Construction des 16 observations causales, sans lire les tokens futurs.
7. Projection à travers les lignes P/R originales des dix premières Obsiss ; poids V6 ouverts en lecture seule.
8. Découpage des longues réponses en segments de continuation, avec loss masquée sur la seule sortie assistant.
9. Comptage des tokens supervisés séparément par tâche.
10. Arrêt `PREPARATION_ONLY`, sans initialisation de paramètres.

## 4. Commandes d'exécution

```bash
PYTHONPATH=Dmodel_eSonde_v7/src python -u Amodel_eSonde_v7/tools/train_conditional_obsiss.py \
  --source-root /mnt/data/work_esonde_v7 \
  --v6-model-dir Dmodel_eSonde_v7/models/eSonde_v6 \
  --output Dmodel_eSonde_v7/models/eSonde_v7/conditional_checkpoint.json \
  --initial-obsiss 10 --prepare-only --max-vocab 1024 --max-units 160 \
  --chat-loss-weight 8.0
```

## 5. Résultats
- Textes autonomes : 13 759 TRAIN, 764 validation interne.
- Paires chat : 13 TRAIN, 1 validation, 3 TEST gardées à l'écart.
- Séquences : 14 488 TRAIN (13 759 LM + 729 segments chat), 801 validation (764 LM + 37 segments chat).
- Tokens supervisés TRAIN : 1 249 157 LM et 43 395 chat.
- Tokens supervisés VALIDATION : 69 388 LM et 2 200 chat.
- Taille du vocabulaire : 1 291 identifiants, dont 1 024 entrées lexicales au maximum et les identifiants réservés.
- Les données `math_qa` et `sms_classification` sont exclues de l'objectif chat.
- Aucun paramètre conditionnel n'a été initialisé ; aucun entraînement n'a été effectué.
- SHA-256 des poids V6 : `8526943d1528418fa8bbbf9128b61b5e1acd90a16eeb7cc062e18864b083dff4`.

## 6. Interprétation des résultats
Le texte seul domine le volume de cibles (environ 96,6 %). Le poids de tâche chat fixé à 8 donne un objectif différencié et mesurable ; sa valeur reste un hyperparamètre expérimental. Les 17 paires eGenBrain `chat` sont en anglais et majoritairement des consignes de création, de réécriture et de structuration de contenus créatifs. Elles ne représentent pas une couverture suffisante pour affirmer une compétence générale de dialogue multi-tours ou une capacité française conditionnelle. Ce constat délimite les données présentes, pas le potentiel du modèle.

## 7. Conséquences
- **Théorique :** le modèle paramétrique peut apprendre une transformation conditionnelle différente d'un simple co-comptage lexical ; cette expérience de préparation ne démontre pas encore qu'il l'apprend.
- **Conceptuelle :** les Obsiss conservent des voix P/R distinctes ; leur projection agrégée transporte moyenne et dispersion sans stocker les réponses.
- **Opérationnelle :** l'apprentissage utilise PyTorch hors ligne ; l'inférence exportée est prévue sans PyTorch. Les poids originaux ne sont ni modifiés ni réécrits.

## 8. Conclusions
La préparation des exemples et la réconciliation des partitions sont validées. Le déséquilibre des tâches est désormais visible et contrôlé par un poids de chat documenté. La préparation ne doit pas être confondue avec un entraînement ou avec une validation de réponses.

## 9. Statut du modèle
**Architecture conditionnelle : implémentation prototype. Préparation des données : PASS. Paramètres conditionnels : NON ENTRAÎNÉS. P2 : IN_PROGRESS.** Aucune conclusion anticipée de réussite ou d'échec n'est formulée.
