# Rapport M-030 — tentative 2 interrompue après deux époques

**Date :** 15 novembre 2026  
**Statut :** `INCOMPLETE_SIGKILL_AFTER_EPOCH_2_OF_4_NO_CHECKPOINT`  
**Périmètre :** ablation d'entraînement 64D, vocabulaire lexical 16 384, comparaison au témoin M-024 64D/vocabulaire 1 024.

## 1. Description

M-030 teste une seule intervention : augmenter le plafond lexical de 1 024 à 16 384, en conservant le jeu de données TRAIN/VALIDATION, la graine, la structure 64D, les dix Obsiss initiales, les pertes, les quatre époques et les autres hyperparamètres préenregistrés. La deuxième tentative supervisée a été interrompue avant la fin des quatre époques.

## 2. Architecture

La variante réutilise le transducteur GRU avec attention par occurrence M-024 64D. La taille lexicale est de 16 384 ; avec les ID réservés, l'espace de sortie attendu est de 16 651 classes. Le panneau sentinelle est désactivé. Le modèle témoin M-024 64D reste gelé et distinct. Le checkpoint V6 de 64 000 000 octets n'est pas modifié.

## 3. Pipeline complet

1. Lecture des chemins, checklists, incidents et référence de sauvegarde.
2. Préflight P2 `PASS` et snapshot vérifié avant exécution.
3. Chargement des données TRAIN/VALIDATION ; les splits TEST restent exclus.
4. Entraînement de quatre époques demandé avec graine `20261114`.
5. Validation à la fin de chaque époque et journalisation JSONL.
6. Export prévu du meilleur checkpoint uniquement après la fin de l'entraînement.
7. L'exécution s'est terminée par SIGKILL après l'époque 2 : l'export final n'a pas eu lieu.

## 4. Commandes d'exécution

Commande exacte conservée dans `experiments/P2_M030_ATTEMPT2_COMMAND_20261115.json`. Elle utilise notamment `--max-vocab 16384 --min-frequency 2 --epochs 4 --batch-size 32 --embedding-size 24 --hidden-size 48 --max-units 256 --learning-rate 0.001 --weight-decay 0.0001 --threads 2 --max-train-examples 0`.

Préflight : `experiments/P2_M030_ATTEMPT2_PREFLIGHT_20261115.json`, statut `PASS`.  
Superviseur : PID 13430 ; processus d'entraînement : PID 13437.  
Sortie finale : `experiments/checkpoints/P2_M030_occurrence_attention_64d_vocab16k.json` (absente).

## 5. Résultats

Le journal durable `experiments/logs/P2_M030_ATTEMPT2_20261115.log` contient deux époques complètes. Son SHA-256 est `7f70f356f13869ae61aa5f5ecaa3723a839556bc7422e16a3f4e67f7ce6d83d0`.

| Mesure | Époque 1 | Époque 2 |
|---|---:|---:|
| Perplexité pondérée TRAIN | 85,0283 | 21,9935 |
| Perplexité validation mixte pondérée | 26,4778 | 16,6326 |
| Perplexité validation mixte non pondérée | 25,6871 | 16,2735 |
| Perplexité validation chat | 71,3209 | 50,1833 |
| Perplexité validation MathQA | 24,2779 | 14,5854 |

Le statut du superviseur est `FAILED`, code de sortie `-9` (SIGKILL), durée enregistrée 3 708,087 secondes. Aucun checkpoint final ou état optimiseur n'a été écrit. Le TEST n'a pas été utilisé ; aucune génération libre n'a été exécutée. Les poids V6 restent à 64 000 000 octets et SHA-256 `8526943d1528418fa8bbbf9128b61b5e1acd90a16eeb7cc062e18864b083dff4`.

## 6. Interprétation des résultats

Les métriques des deux époques montrent une baisse de la perplexité de validation au cours de cette tentative. Elles ne constituent pas le résultat final de l'ablation : il manque deux époques, la sélection du checkpoint, l'évaluation TEST après gel et les générations prompt-only. Elles ne peuvent pas être comparées comme performance finale à M-024.

Le SIGKILL a perdu l'état modèle/optimiseur qui existait seulement en mémoire. Les métriques numériques sont, elles, conservées dans le journal. La cause exacte du signal n'est pas déterminée ; elle n'est pas attribuée à une commande concomitante sans preuve causale.

## 7. Conséquences théoriques, conceptuelles et opérationnelles

- **Théoriques :** aucune conclusion sur l'effet causal de la capacité lexicale ne peut être tirée d'un entraînement incomplet.
- **Conceptuelles :** la réduction attendue du byte-fallback reste une hypothèse de représentation, distincte de la cohérence sémantique.
- **Opérationnelles :** le trainer doit persister à chaque frontière d'époque l'état du modèle, l'état de l'optimiseur, les états RNG et le numéro d'époque, puis valider la reprise sur une fixture déterministe avant une nouvelle tentative longue.

## 8. Conclusions

La tentative 2 de M-030 est conservée comme exécution interrompue, pas comme modèle entraîné validé. Les données source, les fichiers persistés, le checkpoint témoin M-024 et les poids V6 n'ont pas été perdus ni altérés. La reprise doit d'abord améliorer la persistance/reprise, créer une nouvelle sauvegarde vérifiée et repasser le préflight. Aucune valeur TEST ne doit être consultée avant la finalisation et le hash du checkpoint.

## 9. Statut du modèle/expérience

`INCOMPLETE` — deux époques sur quatre enregistrées ; sortie `-9` ; checkpoint absent ; état modèle/optimiseur non récupérable ; TEST scellé ; génération non exécutée. P2 reste `IN_PROGRESS` ; aucune phase suivante n'est ouverte.
