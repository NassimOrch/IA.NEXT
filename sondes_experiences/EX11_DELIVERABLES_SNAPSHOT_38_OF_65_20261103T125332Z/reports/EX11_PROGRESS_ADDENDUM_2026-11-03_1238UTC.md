# Addendum de progression EX11 — 2026-11-03 12:38 UTC

Instantané complémentaire ; les addenda précédents restent dans l'historique et ne sont pas réécrits.

## REPLICA-U v004 — campagne confirmatoire en cours

- Runner séquentiel : PID 11597, `src/training/train_replica_campaign_v004.py`.
- Plan préenregistré : 13 datasets × 5 graines = 65 blocs ; 5 folds OOF ; refit final sur tout le train externe.
- Registre : `logs/append_only/replica_u_campaign_v004.jsonl`.
- À cet instant : 20/65 blocs `COMPLETED_VALIDATION_ONLY`, 0 statut FAILED ; KC1 est en cours.
- Répartition : German Credit 5/5, Spambase 5/5, Tic-Tac-Toe 5/5, GINA 5/5, KC1 0/5, autres 0/5.
- Audit indépendant v002 : 20/20 rapports scientifiques PASS. Les métriques du JSON sont recalculées à partir des logits/predictions ; checkpoints, OOF, owners, config et GE4X sont vérifiés.
- Aucun holdout tabulaire scellé n'a été ouvert.

### Log-loss validation moyenne (moyenne de graines terminées)

| Dataset | Seeds | Backbone | Teacher | Student 64/32 | Student 32/16 | MLP matched 64/32 | MLP GE4X |
|---|---:|---:|---:|---:|---:|---:|---:|
| German Credit | 5 | 0.52306 | 0.55872 | 0.51119 | 0.51387 | 0.50785 | 0.50998 |
| Spambase | 5 | 0.19504 | 0.19294 | 0.17418 | 0.17881 | 0.17918 | 0.18193 |
| Tic-Tac-Toe | 5 | 0.08390 | 0.08178 | 0.06520 | 0.06486 | 0.04894 | 0.04853 |
| GINA | 5 | 0.25878 | 0.32793 | 0.26072 | 0.26681 | 0.24925 | 0.25246 |

Les valeurs sont des métriques de validation, jamais de test. Les quatre domaines démontrent un résultat dépendant du dataset : le student bat la log-loss du MLP apparié sur Spambase, mais pas sur German Credit, Tic-Tac-Toe ni GINA. Le teacher ne bat pas le backbone en moyenne sur ces quatre domaines. Aucune supériorité générale ne peut être conclue.

## Autres branches confirmatoires et exploratoires

- REPLICA-U v003 : 65/65 blocs terminés et audités ; exploratoire en raison de la déviation du refit final.
- CNG v001 : 18 runs audités ; exploratoire (centres non initialisés KMeans).
- CNG v004 / LOO v004 : scripts prêts, 0 exécution confirmatoire enregistrée.
- CNC v003 : un seed, exploratoire.
- CNC v004 : un seed KMeans train-only, mais ordre de mini-batches C3/C4 non apparié.
- CNC v005 : code/runner apparié préparés, 0 seed exécuté.
- D3Q v001 : 160/160 runs réconciliés mais exploratoires (KMeans et comparateur GE4X non conformes, temps sous contention).
- D3Q v004 : script corrigé prêt, 0 run enregistré.
- D1/D2 : équivalence sortie/gradient 40/40 (10 graines × 4 batchs) sous tolérance `1e-6`. Le microbenchmark CPU mono-thread pré-campagne donne D2 plus rapide que D1 de 1,75× à 4,04× en forward, et de 1,97× à 3,21× sur train-step, selon batch.

## Intégrité et phases

- 13/13 ARFF identiques aux fichiers de l'archive jointe ; les archives ZIP sources passent CRC.
- 65 splits / 195 CSV audités indépendamment ; 65 holdouts en `0440`.
- Prompt v2.3.1-reconstructed et préinscription identiques octet pour octet ; audit prompt 13/13.
- Tests logiciels : 24/24 PASS.
- P0/P1/P2 fermées ; P3 en cours ; P4 (test scellé) NOT_STARTED ; P5 en attente de stabilisation de campagne et de manifeste/ZIP final.
- Énergie : NOT MEASURED ; RSS disponible uniquement sous forme de high-water mark partagé, donc non attribuable à une variante.
