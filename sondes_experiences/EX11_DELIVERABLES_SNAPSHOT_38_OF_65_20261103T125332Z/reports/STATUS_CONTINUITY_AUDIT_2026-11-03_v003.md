# Audit de continuité EX11 — instantané v003

Instantané de lecture : 2026-11-03, environ 13:00 Africa/Algiers. L'état d'un processus peut avancer immédiatement après la lecture ; les registres sont la source de vérité.

## État observé

- `replica_u_campaign_v003.jsonl` : 60 lignes `COMPLETED_VALIDATION_ONLY` à la dernière lecture ; les datasets German Credit, Spambase, Tic-Tac-Toe, GINA, KC1, KC2, PC1, PC3, PC4, One-Hundred-Plants et Blood Transfusion avaient cinq graines ; Phoneme avait quatre graines ; Steel Plates avait commencé (seed 1501 en cours, non encore inscrit).
- PID 6129 exécutait encore `train_replica_campaign_v003.py`, avec consommation CPU active. Ce processus était donc laissé seul ; aucune campagne parallèle n'a été lancée.
- Audit des fichiers REPLICA v001 : 59 runs scientifiques complets présents (le compteur inclut un v002 et 58 lignes v003 à la lecture antérieure), tous prédictions/checkpoints/configurations/OOF réconciliés. Le décompte a progressé ensuite ; consulter le registre courant.
- D3Q v001 : 160 runs ; audit des artefacts `all_artifacts_reconciled=true`. Statut exploratoire/non confirmatoire en raison de l'initialisation et du comparateur GE4X historiques.
- CNG v001 : 18/18 runs réconciliés ; statut exploratoire (initialisation de centres aléatoire).
- CNC : v003 seed1501 et v004 seed1501 persistés ; v002 est conservé comme échec de persistance. v004 a KMeans ; v005 introduit l'ordre de mini-batches apparié C3/C4.
- D1/D2 : 40/40 cas d'équivalence, dix seeds × quatre tailles de batch ; erreur max sortie `1.7881393432617188e-07`, gradient d'entrée `3.725290298461914e-09`, gradient paramètres `2.9802322387695312e-08`.
- Splits : audit indépendant repassé, 13 datasets/65 splits, `all_pass=true`; aucun CSV test n'a de mode différent de `0440`.
- Tests : 24/24 PASS.

## Limites explicites

Les campagnes confirmatoires REPLICA v004, CNG v004, CNC v005 et D3Q v004 ne sont pas déclarées exécutées. Le test scellé reste fermé. Les mesures d'énergie ne sont pas disponibles, et le high-water RSS du microbenchmark n'est pas une mesure mémoire attribuable à chaque modèle. Les mesures d'entraînement pendant les campagnes concurrentes ne valent pas comme mesure confirmatoire de vitesse.

## Fichiers de code confirmatoire préparés

- `src/training/train_replica_u_v004.py`, `src/training/train_replica_campaign_v004.py`
- `src/training/train_cng_suite_v004.py`, `src/training/run_cng_loo_ablation_v004.py`
- `src/training/train_cnc_composition_v005.py`, `src/training/run_cnc_campaign_v005.py`
- `src/training/train_efficiency_quality_v004.py`

Ils sont inclus comme scripts réels, testés/compilés, mais leur présence ne vaut pas preuve d'exécution.
