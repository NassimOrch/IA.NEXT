# EX11 — addendum de progression (2026-11-03 13:16 UTC)

## Statut de la campagne REPLICA-U v004

- Registre canonique : `logs/append_only/replica_u_campaign_v004.jsonl`.
- Processus actif au contrôle : PID 11597 (`train_replica_campaign_v004.py`).
- Runs de validation terminés inscrits : 37/65.
- Audit indépendant `audit_replica_artifacts_v002.py` : 37 rapports, 37 runs scientifiques, `all_science_runs_pass=true`.
- Couverture complète à ce snapshot : German Credit, Spambase, Tic-Tac-Toe, GINA, KC1, KC2, PC1 (5 graines chacun) ; PC3 (2 graines). Les autres jeux sont en attente.
- Aucun test tabulaire scellé consulté.

## Résumé validation v004 à ce snapshot

Les moyennes et intervalles appariés les plus récents sont ceux produits par `summarize_ex11_v002.py` et `paired_replica_stats_v001.py`. Ils sont descriptifs, non corrigés pour multiplicité, et restent sur données de validation :

- Le student64 améliore nettement le backbone sur Spambase (différence moyenne appariée de log-loss -0,02086, IC t 95 % [-0,03516 ; -0,00656], 5/5 graines).
- L'avantage du student64 sur le MLP apparié Spambase n'est pas démontré (différence -0,00500, IC [-0,01667 ; 0,00667], 3/5).
- Tic-Tac-Toe favorise le MLP apparié sur les cinq graines (différence student64 - MLP +0,01626, IC [0,00437 ; 0,02815]).
- Sur GINA, le teacher est nettement inférieur au backbone (différence +0,06915, IC [0,04238 ; 0,09592]).
- Les student64 sont plus lents à entraîner que le MLP apparié sur les sept datasets alors complets (ratios moyens appariés entre 1,06× et 4,65×). Ce ratio concerne le temps d'entraînement du student vs MLP apparié, pas la latence d'inférence.

## Statut des autres branches

- D1/D2 : équivalence confirmée 40/40 (10 graines × 4 batches), erreurs max sorties 1,788e-7, gradients d'entrée 3,725e-9, gradients paramètres 2,980e-8, tolérance 1e-6. Microbenchmark isolé mono-thread pré-campagnes : D2 est plus rapide que D1 en forward et train-step pour les quatre batches.
- D3 : architecture distincte, donc pas d'affirmation d'équivalence ; qualité à mesurer par campagne confirmatoire.
- REPLICA-U v003 : 65/65 terminés et audités, mais exploratoires en raison du refit final sur i_fit plutôt que tout le train extérieur.
- D3Q v001 : 160/160 terminés et réconciliés, mais exploratoires (initialisation non-KMeans, GE4X insuffisant pour D1/D2, mesures de durée sous contention).
- CNG v001 : 18 runs réconciliés, exploratoires (initialisation de centres non conforme).
- CNC v003/v004 : un run par version, archivés ; v004 KMeans train-only, mais le couplage C3/C4 de l'ordre des minibatches n'est pas identique. CNC v005 préparé, non lancé.
- Les versions confirmatoires CNG v004, CNG-LOO v004, CNC v005 et D3Q v004 ne sont pas encore exécutées à ce snapshot.

## Décision de protocole

P3 reste ouverte. P4 (ouverture du holdout final) reste interdite. Ne pas réduire les budgets ni supprimer des runs pour annoncer artificiellement la complétude. Les campagnes antérieures présentant une déviation restent identifiables et ne sont pas requalifiées rétroactivement.
