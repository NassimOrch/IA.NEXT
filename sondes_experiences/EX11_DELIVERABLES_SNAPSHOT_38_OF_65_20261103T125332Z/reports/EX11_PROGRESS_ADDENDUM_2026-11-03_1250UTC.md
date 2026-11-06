# Addendum de progression EX11 — 2026-11-03 12:50 UTC

État fondé sur les registres et artefacts persistés ; aucun holdout tabulaire scellé chargé.

## REPLICA-U v004

- 33/65 blocs terminés `COMPLETED_VALIDATION_ONLY`, 0 échec explicite.
- Répartition : German Credit 5/5 ; Spambase 5/5 ; Tic-Tac-Toe 5/5 ; GINA 5/5 ; KC1 5/5 ; KC2 5/5 ; PC1 3/5 ; six autres jeux 0/5.
- Processus runner actif : PID 11597, script `src/training/train_replica_campaign_v004.py`, 1 thread Torch.
- Audit indépendant v002 : 33/33 rapports complets PASS (métriques recalculées depuis les logits, checkpoints, prédictions, OOF owners/logits, config/code hash, compte de paramètres/GE4X).
- v003 historique : 65/65 complet, mais exploratoire (refit final non réalisé sur tout le train extérieur).

### Moyennes de log-loss validation (graine/tâche)

| Dataset | n | Backbone | Teacher | Student64/32 | Student32/16 | MLP matched64/32 | MLP GE4X |
|---|---:|---:|---:|---:|---:|---:|---:|
| German Credit | 5 | 0.52306 | 0.55872 | 0.51119 | 0.51387 | 0.50785 | 0.50998 |
| Spambase | 5 | 0.19504 | 0.19294 | 0.17418 | 0.17881 | 0.17918 | 0.18193 |
| Tic-Tac-Toe | 5 | 0.08390 | 0.08178 | 0.06520 | 0.06486 | 0.04894 | 0.04853 |
| GINA | 5 | 0.25878 | 0.32793 | 0.26072 | 0.26681 | 0.24925 | 0.25246 |
| KC1 | 5 | 0.36716 | 0.36788 | 0.34818 | 0.34726 | 0.34588 | 0.34954 |
| KC2 | 5 | 0.41140 | 0.42133 | 0.36646 | 0.36428 | 0.36426 | 0.36456 |
| PC1 | 3 | 0.19277 | 0.20323 | 0.20040 | 0.20041 | 0.19248 | 0.18837 |

### Contrastes appariés par graines

Le rapport complet est `REPLICA_U_PAIRED_STATS_V004.md` avec écart moyen, écart-type, IC t bilatéral 95 % non ajusté et nombre de graines gagnées.

- Spambase : Student64 vs backbone, Δ log-loss −0.02086, IC95% [−0.03516 ; −0.00656], 5/5 graines ; contre MLP matched, Δ −0.00500, IC [−0.01667 ; 0.00667], 3/5, donc pas de supériorité démontrée.
- Tic-Tac-Toe : Student64 moins bon que MLP matched, Δ +0.01626, IC [0.00437 ; 0.02815], 0/5 victoires.
- GINA : teacher moins bon que backbone, Δ +0.06915, IC [0.04238 ; 0.09592], 0/5 victoires.
- German Credit et KC1 : IC Student64−MLP inclut zéro ; pas de vainqueur statistique stable.
- KC2 : cinq graines, IC Student64−MLP inclut zéro.
- PC1 : trois graines, Student64 moins bon que MLP en moyenne (Δ +0.00792 ; IC [−0.01412 ; 0.02996]) ; résultats trop partiels pour conclure.

IC non corrigés pour multiplicité et calculés sur n=3–5 seeds seulement : ils sont descriptifs, pas une preuve de généralisation entre domaines.

### Temps d'entraînement et ressources

Le ratio moyen apparié (student64 / MLP matched64) est supérieur à 1 sur tous les jeux terminés : German Credit 1.63×, Spambase 3.63×, Tic-Tac-Toe 1.36×, GINA 4.65×, KC1 1.57×, KC2 1.06×. La distillation n'a donc pas transformé la compacité en entraînement plus rapide. Les temps sont ceux de la seule phase d'entraînement du student et du MLP apparié ; l'OOF/teacher est rapporté séparément. Latence d'inférence REPLICA par variante : pas encore mesurée.

## Autres branches

- CNG v001 : 18 runs audités mais exploratoires (centres non-KMeans). CNG v004 et LOO v004 : zéro run confirmatoire.
- CNC v003 : une graine exploratoire ; CNC v004 : une graine KMeans train-only, non appariée en ordre de batch ; CNC v005 : zéro run, code pairé prêt.
- D3Q v001 : 160/160 runs réconciliés mais exploratoires (KMeans, GE4X et contention). D3Q v004 : zéro run.
- D1/D2 : 40/40 équivalences sorties/gradients sous `1e-6`. Microbenchmark mono-thread pré-campagne : D2 est 1.75–4.04× plus rapide en forward et 1.97–3.21× en train-step selon le batch.

## Intégrité et phases

- 13 ARFF identiques à l'archive ; 130 train/validation + 65 holdouts = 195 CSV, vérification indépendante ; holdouts `0440`.
- Prompt v2.3.1-reconstructed / préinscription synchronisés ; audit 13/13 ; tests logiciels 24/24 PASS.
- P0/P1/P2 closes ; P3 en cours ; P4 NOT_STARTED ; P5 snapshot courant, final à réactualiser.
- Énergie `NOT_MEASURED` ; RSS high-water partagé, non attribuable par variante.
