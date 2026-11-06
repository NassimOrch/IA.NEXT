# Addendum de progression EX11 — 2026-11-03 12:42 UTC

Instantané matériel à 12:42 UTC. Les addenda précédents restent conservés.

## REPLICA-U v004

- Runner actif : PID 11597 (`src/training/train_replica_campaign_v004.py`), un seul processus d'entraînement, 1 thread Torch.
- Plan : 13 jeux × 5 graines = 65 blocs, chaque bloc comprend 5 folds OOF et les variantes préenregistrées ; refit final sur tout le train externe.
- Registre : `logs/append_only/replica_u_campaign_v004.jsonl`.
- 23/65 blocs terminés `COMPLETED_VALIDATION_ONLY`, aucun échec enregistré.
- Répartition : German Credit 5/5 ; Spambase 5/5 ; Tic-Tac-Toe 5/5 ; GINA 5/5 ; KC1 3/5 ; KC2, PC1, PC3, PC4, Phoneme, Steel Plates, Plants et Blood Transfusion 0/5.
- Auditeur indépendant v002 : 23/23 PASS, recalcul des métriques depuis logits/predictions et vérification checkpoints, OOF/owners, configuration, code et GE4X.
- Test tabulaire scellé non ouvert.

### Log-loss moyenne de validation

| Dataset | n seeds | Backbone | Teacher | Student 64/32 | Student 32/16 | MLP matched 64/32 | MLP GE4X |
|---|---:|---:|---:|---:|---:|---:|---:|
| German Credit | 5 | 0.52306 | 0.55872 | 0.51119 | 0.51387 | 0.50785 | 0.50998 |
| Spambase | 5 | 0.19504 | 0.19294 | 0.17418 | 0.17881 | 0.17918 | 0.18193 |
| Tic-Tac-Toe | 5 | 0.08390 | 0.08178 | 0.06520 | 0.06486 | 0.04894 | 0.04853 |
| GINA | 5 | 0.25878 | 0.32793 | 0.26072 | 0.26681 | 0.24925 | 0.25246 |

### Temps d'entraînement mesurés (moyenne des graines terminées)

| Dataset | Student64 (s) | MLP matched64 (s) | Ratio Student/MLP |
|---|---:|---:|---:|
| German Credit | 0.27 | 0.16 | 1.69× |
| Spambase | 2.21 | 0.68 | 3.25× |
| Tic-Tac-Toe | 0.71 | 0.55 | 1.29× |
| GINA | 4.57 | 1.06 | 4.31× |

Ces temps concernent la phase d'entraînement du student / MLP apparié dans les mêmes runs, non la totalité du pipeline OOF. Ils montrent que le student REPLICA-U ne procure pas à ce stade de gain d'entraînement : il est plus lent que le MLP de même taille sur tous les domaines terminés. Les durées dépendent fortement de la taille/dimension des données et de l'architecture. Les temps globaux incluent les cinq folds OOF.

### Interprétation

La moyenne de log-loss du student64 est meilleure que le MLP matched sur Spambase, mais elle est moins bonne sur German Credit, Tic-Tac-Toe et GINA. Le teacher est moins bon que le backbone sur les quatre moyennes reportées. La compression en paramètres du student ne se convertit donc pas en supériorité prédictive générale ni en entraînement plus rapide. Les mesures d'inférence par variante ne sont pas encore réalisées dans la campagne confirmatoire ; aucun avantage de latence d'inférence ne doit être revendiqué.

## Branches CNG/CNC/D

- CNG v001 : 18 runs audités, exploratoires (initialisation aléatoire des centres).
- CNG v004 et LOO v004 : scripts confirmatoires préparés/tests passés, 0 run confirmé.
- CNC v003 : 1 seed exploratoire ; CNC v004 : 1 seed KMeans train-only, mais non apparié sur l'ordre mini-batches ; CNC v005 : code batch-order apparié prêt, 0 seed confirmé.
- D3Q v001 : 160/160 runs réconciliés mais exploratoires (centres aléatoires, GE4X inadéquat pour D1/D2, timings sous contention).
- D3Q v004 : code corrigé prêt, 0 run confirmé.
- D1/D2 : équivalence sortie/gradient 40/40, erreur max sous tolérance 1e-6 ; microbenchmark isolé mono-thread en faveur de D2, forward 1.75–4.04× et train-step 1.97–3.21× selon batch.

## Intégrité et phases

- 13/13 ARFF extraits identiques aux originaux de l'archive ; CRC ZIP valides.
- 65 splits : 130 fichiers train/validation + 65 holdouts = 195 CSV de partition ; tous vérifiés indépendamment. 65 holdouts en `0440`.
- Prompt v2.3.1-reconstructed synchronisé au préenregistrement, audit prompt 13/13.
- Tests logiciels 24/24 PASS.
- P0/P1/P2 fermées ; P3 en cours ; P4 non ouverte ; P5 archive snapshot créée mais package final à re-générer après campagne stable.
- Énergie : NOT MEASURED ; RSS high-water partagé, non attribuable par modèle.
