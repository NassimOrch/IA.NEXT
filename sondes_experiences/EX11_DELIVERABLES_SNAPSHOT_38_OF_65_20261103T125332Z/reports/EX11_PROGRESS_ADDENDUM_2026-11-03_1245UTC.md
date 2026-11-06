# Addendum de progression EX11 — 2026-11-03 12:45 UTC

Instantané issu des fichiers persistés. Il complète les addenda antérieurs sans les remplacer.

## REPLICA-U v004 confirmatoire

- Runner actif : PID 11597 ; script `src/training/train_replica_campaign_v004.py` ; un seul processus d'entraînement, 1 thread Torch.
- Pré-enregistrement : 13 datasets × 5 graines = 65 blocs ; cinq folds OOF ; choix des durées interne puis réentraînement final sur tout le train extérieur.
- Registre append-only : `logs/append_only/replica_u_campaign_v004.jsonl`.
- 27/65 blocs terminés `COMPLETED_VALIDATION_ONLY`, aucun échec explicite.
- Répartition : German Credit 5/5 ; Spambase 5/5 ; Tic-Tac-Toe 5/5 ; GINA 5/5 ; KC1 5/5 ; KC2 2/5 ; sept datasets restent à démarrer.
- Audit indépendant v002 : 27/27 PASS : checkpoints, prédictions, logits OOF, owner map, hashes, configuration, paramètres/ratio GE4X et métriques recalculées.
- Holdouts tabulaires toujours fermés.

### Log-loss moyenne de validation

| Dataset | n seeds | Backbone | Teacher | Student 64/32 | Student 32/16 | MLP matched 64/32 | MLP GE4X |
|---|---:|---:|---:|---:|---:|---:|---:|
| German Credit | 5 | 0.52306 | 0.55872 | 0.51119 | 0.51387 | 0.50785 | 0.50998 |
| Spambase | 5 | 0.19504 | 0.19294 | 0.17418 | 0.17881 | 0.17918 | 0.18193 |
| Tic-Tac-Toe | 5 | 0.08390 | 0.08178 | 0.06520 | 0.06486 | 0.04894 | 0.04853 |
| GINA | 5 | 0.25878 | 0.32793 | 0.26072 | 0.26681 | 0.24925 | 0.25246 |
| KC1 | 5 | 0.36716 | 0.36788 | 0.34818 | 0.34726 | 0.34588 | 0.34954 |
| KC2 | 2 | 0.44925 | 0.46488 | 0.34221 | 0.34093 | 0.34208 | 0.35094 |

### Temps d'entraînement student 64/32 vs MLP apparié 64/32

| Dataset | Student (s, moyenne) | MLP matched (s, moyenne) | Student/MLP |
|---|---:|---:|---:|
| German Credit | 0.27 | 0.16 | 1.69× |
| Spambase | 2.21 | 0.68 | 3.25× |
| Tic-Tac-Toe | 0.71 | 0.55 | 1.29× |
| GINA | 4.57 | 1.06 | 4.31× |

La mesure d'entraînement de l'étudiant inclut la phase de distillation mais pas le coût de génération OOF/teacher complet ; le coût total de REPLICA est bien supérieur et est rapporté séparément. Dans les données terminées, le student est plus lent que son MLP apparié sur chaque dataset. Le student obtient une meilleure log-loss que le MLP matched uniquement sur Spambase parmi les cinq domaines complets ; German Credit, Tic-Tac-Toe, GINA et KC1 ne le confirment pas. KC2 n'a que deux graines. Le teacher n'améliore pas la log-loss du backbone sur les six jeux affichés.

## Historique et branches restantes

- REPLICA-U v003 : 65/65 terminé et audité ; exploratoire en raison du refit final non exécuté sur tout le train externe.
- CNG v001 : 18 runs audités mais exploratoires (centres non-KMeans). CNG v004 et LOO v004 : 0 run confirmatoire.
- CNC v003 : 1 graine exploratoire ; CNC v004 : 1 graine KMeans train-only mais ordre de batch non apparié ; CNC v005 : 0 seed, script apparié préparé.
- D3Q v001 : 160/160 runs réconciliés, exploratoires (centres, GE4X et contention). D3Q v004 : 0 runs.
- D1/D2 : 40/40 cas équivalence sorties/gradients (10 seeds × 4 batchs), erreur sous `1e-6`. Le microbenchmark CPU mono-thread pré-campagne donne un gain D2 de 1.75–4.04× en forward et 1.97–3.21× en train-step selon batch.

## Intégrité / portes

- 13/13 ARFF identiques à l'archive jointe ; ZIP source CRC valides.
- 130 fichiers train/validation + 65 holdouts = 195 CSV ; vérification indépendante passée ; holdouts en `0440`.
- Prompt v2.3.1-reconstructed et préinscription identiques ; audit prompt 13/13 ; tests logiciels 24/24.
- P0/P1/P2 fermées ; P3 en cours ; P4 non commencée ; P5 archive snapshot disponible mais archive finale à réactualiser après fin/stabilisation des campagnes.
- Énergie `NOT MEASURED` ; RSS high-water partagé non attribuable par modèle.
