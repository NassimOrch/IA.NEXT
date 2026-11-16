# Rapport NM-009 — Réconciliation du lecteur de paires dialogiques

## 1. Description
Le premier préparateur d'entraînement conditionnel a tenté de rapprocher les identifiants bruts de `Screenplay_dataset.jsonl` avec le manifeste d'entraînement eSonde v6. La réconciliation a échoué avant la construction de paramètres : les occurrences brutes répétées et les identifiants qui ne font pas partie du sous-ensemble canonique v6 ont été comptés comme des paires d'entraînement supplémentaires.

## 2. Architecture
La source eGenBrain v4 est constituée de plusieurs fichiers et de répétitions. Son chargeur canonique `egenbrain.train.load_records` regroupe les paires par tâche et signature de contenu, conserve leur multiplicité et applique une séparation déterministe par groupe de prompt. Le lecteur expérimental initial ne reproduisait pas ce pipeline et utilisait à tort un seul fichier brut comme substitut du corpus canonique.

## 3. Pipeline complet
1. Lire le manifeste des sources eSonde v6 et le fichier brut de dialogues.
2. Comparer directement des identifiants bruts au manifeste v6.
3. Observer une réconciliation impossible : les occurrences comptées dépassent le nombre d'exemples canoniques.
4. Arrêter avant l'initialisation du réseau et avant tout entraînement.
5. Reprendre l'ingestion avec le chargeur eGenBrain v4 officiel.
6. Filtrer strictement `task == chat` après déduplication canonique.
7. Vérifier les comptes de split du chargeur lui-même.

## 4. Commandes d'exécution
Commande initiale ayant produit l'incident :

```bash
PYTHONPATH=src python ../Amodel_eSonde_v7/tools/train_conditional_obsiss.py \
  --source-root /mnt/data/work_esonde_v7 --prepare-only \
  --max-units 128 --initial-obsiss 10
```

La correction est vérifiée séparément par l'appel à `load_egb_chat_pairs` depuis le script d'entraînement, qui importe `egenbrain.train.load_records` sans créer ni entraîner de paramètres.

## 5. Résultats
- Lecteur brut initial : réconciliation refusée ; les lignes sources contiennent des répétitions et des IDs hors du sous-ensemble de 17 paires canoniques v6.
- Chargeur eGenBrain v4 : 4 783 occurrences brutes `chat`, 17 paires canoniques, réparties 13 TRAIN / 1 VALIDATION / 3 TEST.
- Une ligne JSONL malformée de `batch_dataset.jsonl` (ligne 784) reste exclue sans réparation par le chargeur officiel.
- Aucune initialisation de paramètres, aucun entraînement et aucune inférence n'ont eu lieu pendant l'incident.
- Les fichiers sources et le checkpoint original n'ont pas été modifiés.

## 6. Interprétation des résultats
La source brute ne peut pas être assimilée au jeu de paires canoniques. Les répétitions doivent conserver leur provenance et leur multiplicité, mais ne doivent pas devenir artificiellement des observations indépendantes lors de l'apprentissage. La séparation 13/1/3 de eGenBrain est l'autorité pour cette expérience v7 ; les comptes 10/3/4 du manifeste v6 restent une information historique distincte et ne sont pas mélangés.

## 7. Conséquences
- **Théorique :** l'objectif conditionnel repose sur une paire canonique question/réponse, non sur le nombre de lignes brutes.
- **Conceptuelle :** la provenance et la multiplicité sont conservées, mais elles ne remplacent pas la diversité des exemples.
- **Opérationnelle :** le script appelle désormais le chargeur eGenBrain v4 et vérifie `13/1/3` avant tout entraînement.

## 8. Conclusion
Incident de lecteur de données, détecté par une assertion de réconciliation et corrigé avant l'apprentissage. Aucune source ni donnée n'a été perdue ou altérée.

## 9. Statut du modèle
`RESOLVED_BEFORE_TRAINING`. Le chemin d'ingestion canonique est vérifié ; le prétraitement complet et l'entraînement conditionnel restent à exécuter et à auditer.
