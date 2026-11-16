# Rapport P2-M030 — progression de l’entraînement vocabulaire 16K

## 1. Description

M-030 compare le transducteur M-024 64D, vocabulaire lexical 1 024, à une nouvelle variante 64D avec vocabulaire lexical maximal 16 384. L’hypothèse est que la réduction du byte-fallback peut modifier la prédiction conditionnelle et la génération. Cette fiche décrit un jalon intermédiaire de la deuxième tentative, non le résultat final.

## 2. Architecture

Même architecture GRU avec attention par occurrence du prompt et observations Obsiss 16D que M-024 64D ; dix Obsiss initiales, sans panneau sentinelle. Les seules différences planifiées sont la capacité du vocabulaire et les tailles d’embedding/sortie qui en découlent. Données, seed, batch, optimisation, objectifs et nombre d’époques sont préenregistrés et conservés. Le checkpoint V6 reste en lecture seule.

## 3. Pipeline complet

1. Préflight P2 et vérification du savepoint complet.
2. Chargement des sources TRAIN et VALIDATION, sans accès TEST.
3. Construction du vocabulaire à partir de TRAIN seulement.
4. Préparation du texte autonome, des paires chat et MathQA.
5. Entraînement de quatre époques, sélection du meilleur état sur validation mixte pondérée.
6. Export atomique du checkpoint après la fin des époques.
7. Évaluation TEST gelée et générations prompt-only seulement après vérification du checkpoint.

## 4. Commandes d’exécution

Commande exacte, exécutée sous superviseur persistant :

```bash
python Amodel_eSonde_v7/tools/train_occurrence_attention.py --source-root /mnt/data/work_esonde_v7 --workspace /mnt/data/eSonde_v7_work --output Amodel_eSonde_v7/experiments/checkpoints/P2_M030_occurrence_attention_64d_vocab16k.json --initial-obsiss 10 --no-sentinel-panel --max-vocab 16384 --min-frequency 2 --qa-loss-weight 1.5 --chat-loss-weight 8 --seed 20261114 --epochs 4 --batch-size 32 --embedding-size 24 --hidden-size 48 --max-units 256 --learning-rate 0.001 --weight-decay 0.0001 --threads 2 --max-train-examples 0
```

Préflight `P2_M030_ATTEMPT2_PREFLIGHT_20261115.json` : PASS. Savepoint pré-entraînement : `pre_P2_M030_VOCAB16K_ATTEMPT2_20261115`, manifeste SHA-256 `a64683e58856700274ac2b6e159e5e57f2a7b791ae03dd36150010b433742af7`.

## 5. Résultats

Tentative 2 toujours active à l’observation de ce rapport. Une époque sur quatre est terminée. Résultats de validation de l’époque 1 :

| Mesure | Valeur |
|---|---:|
| Perplexité mixte pondérée | 26,4777619 |
| Perplexité mixte non pondérée | 25,6870883 |
| Perplexité chat | 71,3208700 |
| Perplexité MathQA | 24,2778785 |
| Tokens pondérés TRAIN observés | 2 486 860,5 |

Journal : `/mnt/data/eSonde_v7_work/Amodel_eSonde_v7/experiments/logs/P2_M030_ATTEMPT2_20261115.log`  
SHA-256 du journal à ce jalon : `199b689c8550aed37e5aac17335d7e9d9162b508024329fd20fd1cb39050fc0f`  
Taille : 6527 octets ; 78 lignes.  
Statut superviseur : `RUNNING` ; PID enfant : 13437.  
Aucun checkpoint final n’est encore publié. Le split TEST n’a pas été utilisé. Poids V6 attendus : `8526943d1528418fa8bbbf9128b61b5e1acd90a16eeb7cc062e18864b083dff4`.

## 6. Interprétation des résultats

La perplexité de l’époque 1 est nettement supérieure aux meilleures validations M-024 64D (PPL mixte 8,1486 ; chat 11,1392 ; MathQA 7,8373). Cette comparaison est provisoire : une seule époque est achevée, la sélection finale du meilleur état n’a pas eu lieu et le vocabulaire plus large répartit la probabilité sur davantage de classes. Il serait incorrect de conclure à l’échec du vocabulaire 16K avant les quatre époques, ni d’interpréter la perplexité comme une mesure de cohérence humaine.

## 7. Conséquences théoriques, conceptuelles et opérationnelles

- **Théoriques :** l’augmentation de couverture lexicale change l’espace de prédiction ; le coût en classes de sortie et l’apprentissage de classes rares doivent être considérés conjointement.
- **Conceptuelles :** la couverture de lexèmes OOV mesurée par M-029 n’implique pas que les relations contextuelles ou l’intention dialogique soient mieux représentées.
- **Opérationnelles :** la tête 16K coûte beaucoup plus de calcul et de mémoire que 1K dans cet environnement CPU. La tentative supervisée est suivie par journaux persistants ; aucune réduction silencieuse du corpus ou du budget n’est autorisée.

## 8. Conclusions

Aucune conclusion finale sur M-030 n’est permise à ce stade. Il faut achever quatre époques, vérifier code de sortie et hash du checkpoint, contrôler à nouveau les poids V6, puis seulement évaluer les partitions TEST et les trois générations prompt-only selon le protocole.

## 9. Statut du modèle/expérience

**`INCOMPLET` — RUNNING, 1/4 époque.** Critères de sortie non atteints : processus non terminé, checkpoint final absent, évaluation TEST et générations libres non exécutées. P2 reste `IN_PROGRESS`.


## Mise à jour — époque 2/4 (2026-11-15T12:16:18+01:00)

Le journal durable contient maintenant les époques 1 et 2 (dans l’ordre). L’époque 2 a terminé avec code de processus non encore publié (l’entraînement global continue).

- Perplexité validation mixte pondérée : 16.632559
- Perplexité validation chat : 50.183341
- Perplexité validation MathQA : 14.585446
- Époques confirmées : 2/4
- Checkpoint final : absent à cette mise à jour
- TEST : non consulté ; génération libre : non exécutée

Ces valeurs restent internes au vocabulaire M-030 de 16 384 lexèmes. Elles ne sont pas directement comparables aux perplexités M-024, dont l’espace de sortie était différent.
