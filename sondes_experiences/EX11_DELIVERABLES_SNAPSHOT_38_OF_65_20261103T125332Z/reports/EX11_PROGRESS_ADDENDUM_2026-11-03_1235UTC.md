# Addendum de progression EX11 — 2026-11-03 12:35 UTC

Cet addendum actualise les instantanés antérieurs sans les réécrire. Il décrit l'état matériel observé sur disque au moment de sa création.

## REPLICA-U v004 confirmatoire

- Runner actif : `src/training/train_replica_campaign_v004.py`, PID observé 11597.
- Plan : 13 jeux × 5 graines = 65 blocs ; 5 folds OOF par bloc ; entraînement final sur tout le train extérieur après sélection des durées internes.
- Registre append-only : `logs/append_only/replica_u_campaign_v004.jsonl`.
- Blocs terminés et inscrits à cet instant : 17/65, tous `COMPLETED_VALIDATION_ONLY`.
- Couverture : German Credit 5/5 ; Spambase 5/5 ; Tic-Tac-Toe 5/5 ; GINA 2/5 ; 9 autres jeux 0/5.
- Audit indépendant `src/evaluation/audit_replica_artifacts_v002.py` : 17/17 rapports scientifiques passent les contrôles de checkpoints, prédictions, OOF, configuration, ratios de paramètres et métriques recalculées.
- Pas de score de test tabulaire : les holdouts restent fermés.

### Log-loss moyenne de validation par dataset, sur les graines terminées

| Jeu | n seeds | Backbone | Teacher | Student 64/32 | Student 32/16 | MLP apparié 64/32 | MLP GE4X |
|---|---:|---:|---:|---:|---:|---:|---:|
| German Credit | 5 | 0.52306 | 0.55872 | 0.51119 | 0.51387 | 0.50785 | 0.50998 |
| Spambase | 5 | 0.19504 | 0.19294 | 0.17418 | 0.17881 | 0.17918 | 0.18193 |
| Tic-Tac-Toe | 5 | 0.08390 | 0.08178 | 0.06520 | 0.06486 | 0.04894 | 0.04853 |
| GINA | 2 | 0.25662 | 0.32053 | 0.25750 | 0.26601 | 0.23355 | 0.25869 |

Ces résultats sont des moyennes de validation uniquement. Les datasets GINA, German Credit, Spambase et Tic-Tac-Toe sont des domaines distincts, pas des réplications d'un unique problème. Aucune inférence statistique inter-dataset n'est faite ici. Une meilleure log-loss sur un jeu ne prouve pas une supériorité générale.

## Autres branches

- REPLICA-U v003 : 65/65 blocs complets, audités, mais classés exploratoires en raison de la déviation de refit final (modèles finaux ajustés sur `i_fit` au lieu du train extérieur complet).
- CNG v001 : 18 runs réels audités mais exploratoires (initialisation de centres non conforme KMeans).
- CNG v004 et LOO v004 : scripts préparés/testés, aucune campagne confirmatoire inscrite à ce snapshot.
- CNC v003 : un seed ; exploratoire.
- CNC v004 : un seed ; KMeans train-only mais ordre de mini-batches C3/C4 non apparié.
- CNC v005 : script/runner appariés préparés, aucun seed terminé à ce snapshot.
- D3Q v001 : 160/160 runs réconciliés mais exploratoires (initialisation et comparateur GE4X non conformes, chronométrie sous contention).
- D3Q v004 : script préparé, aucun run confirmé à ce snapshot.
- D1/D2 : équivalence numérique vérifiée sur 40 cas (10 graines × 4 batchs), avec erreurs maximales sous 1e-6 ; microbenchmark mono-thread pré-campagne en faveur de D2 pour forward et train-step.

## Intégrité et statut des phases

- 13/13 ARFF identiques aux membres de l'archive fournie ; archives ZIP CRC valides.
- 65 splits / 195 CSV audités indépendamment ; holdouts 0440.
- Prompt v2.3.1-reconstructed / préinscription synchronisés octet pour octet ; audit du prompt 13/13.
- Tests logiciels : 24/24 PASS.
- P0/P1/P2 fermées. P3 reste IN_PROGRESS. P4 (test tabulaire scellé) reste NOT_STARTED et interdite avant gel. P5 (pack final stable) reste à finaliser après stabilisation des registres.
- Énergie matérielle : NOT MEASURED. RSS : pic du processus partagé, non attribuable proprement à un modèle.

Cet addendum n'altère aucun run, aucune donnée, ni aucun checkpoint. Il ne transforme pas le processus actif en campagne terminée.
