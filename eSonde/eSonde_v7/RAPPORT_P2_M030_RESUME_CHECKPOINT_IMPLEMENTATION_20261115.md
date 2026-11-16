# Rapport P2 — persistance et reprise M-030 aux frontières d’époque

## 1. Description

Après SIGKILL de la tentative M-030 2/4, les métriques déjà écrites étaient conservées, mais les paramètres courants, l’optimiseur et les états aléatoires restés uniquement en mémoire n’étaient pas récupérables. Le présent travail ajoute un mécanisme de persistance pour les prochains entraînements ; il ne prétend pas récupérer l’état perdu de cette tentative.

## 2. Architecture

Le module `tools/training_resume.py` capture à la frontière de chaque époque : `model_state_dict`, `optimizer_state_dict`, meilleur état jusqu’à l’époque, historique, numéro d’époque, RNG Python, RNG CPU PyTorch, RNG NumPy et états CUDA lorsque disponibles. Un fingerprint SHA-256 lie la sauvegarde aux sources TRAIN/VALIDATION, aux splits, au tokenizer, aux hyperparamètres, aux poids V6 parents, aux scripts de training/reprise, à la version Python et à PyTorch. Une différence de fingerprint bloque la reprise.

L’écriture est atomique : sérialisation dans un fichier temporaire frère, flush/fsync, remplacement atomique, puis calcul SHA-256. Le modèle exporté pour l’inférence reste le JSON courant ; le fichier `.training_state.pt` est un état de reprise interne au laboratoire.

## 3. Pipeline

1. Préparer les données TRAIN/VALIDATION comme auparavant, sans accès au TEST.
2. Construire le fingerprint exact de l’expérience.
3. En entraînement neuf, sauvegarder l’état complet à la fin de chaque époque.
4. En reprise, charger l’état, contrôler le fingerprint, restaurer modèle/optimiseur/historique et tous les RNG, puis commencer à l’époque suivante.
5. Après la dernière époque, sélectionner le meilleur état de validation et exporter le checkpoint d’inférence ainsi que le rapport.

## 4. Commandes

Nouveau run (les options expérimentales exactes M-030 restent celles du plan préenregistré) :

```bash
python Amodel_eSonde_v7/tools/train_occurrence_attention.py \
  --source-root /mnt/data/work_esonde_v7 \
  --workspace /mnt/data/eSonde_v7_work \
  --output Amodel_eSonde_v7/experiments/checkpoints/M030_vocab16k.json \
  --state-checkpoint Amodel_eSonde_v7/experiments/checkpoints/M030_vocab16k.state.pt \
  --max-vocab 16384 --epochs 4 --seed 20261114
```

Reprise après interruption à une frontière d’époque, avec toutes les autres options identiques :

```bash
python Amodel_eSonde_v7/tools/train_occurrence_attention.py \
  --source-root /mnt/data/work_esonde_v7 \
  --workspace /mnt/data/eSonde_v7_work \
  --output Amodel_eSonde_v7/experiments/checkpoints/M030_vocab16k.json \
  --state-checkpoint Amodel_eSonde_v7/experiments/checkpoints/M030_vocab16k.state.pt \
  --resume-from Amodel_eSonde_v7/experiments/checkpoints/M030_vocab16k.state.pt \
  --max-vocab 16384 --epochs 4 --seed 20261114
```

Toute la commande préenregistrée doit être conservée ; les paramètres abrégés ci-dessus illustrent seulement l’interface de reprise. Le fingerprint refuse une configuration ou un jeu de données différent. Utiliser uniquement des fichiers d’état créés localement et conservés sous contrôle d’intégrité.

## 5. Résultats des validations logicielles

La suite spécifique `Amodel_eSonde_v7/tools/tests/test_training_resume.py` passe 3/3 tests : (1) sauvegarde/lecture atomique, (2) reprise déterministe exactement égale à une exécution continue sur une fixture PyTorch à deux époques (modèle, optimiseur, RNG Python/NumPy/PyTorch), (3) rejet d’un fingerprint différent et d’un fichier corrompu. Le script et le module passent `py_compile`, et l’aide CLI expose `--state-checkpoint` et `--resume-from`.

## 6. Interprétation

Le mécanisme teste la continuité exacte d’une fixture synthétique et sécurise les prochains runs. Il ne prouve pas encore la reprise d’un long entraînement M-030 réel, ni une amélioration de la qualité des réponses. L’état des deux époques de la tentative SIGKILL demeure perdu en mémoire et n’est pas reconstruit à partir des seules métriques.

## 7. Conséquences théoriques, conceptuelles et opérationnelles

- Théoriques : aucune modification de la fonction objectif ou de l’architecture M-030.
- Conceptuelles : une expérience longue doit être reprise depuis un état complet vérifiable, pas depuis une courbe de métriques.
- Opérationnelles : chaque fin d’époque devient un point de reprise durable ; les frontières, fingerprints et RNG sont audités. Le TEST reste scellé jusqu’au gel final.

## 8. Conclusions

Le mécanisme epoch-boundary resume est implémenté et ses invariants sont testés sur fixture déterministe. La tentative M-030 précédente reste `INCOMPLETE`, 2/4 époques, exit -9, sans checkpoint final. Aucune nouvelle tentative réelle n’a été lancée pendant cette intégration.

## 9. Statut du modèle

`RESUME_MECHANISM_IMPLEMENTED_AND_UNIT_TESTED`; `M030_TRAINING_EXPERIMENT_INCOMPLETE`; P2 `IN_PROGRESS`; P3–P6 restent bloquées.
