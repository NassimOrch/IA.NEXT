# Amodel_NGeGenBrain_v1 — dossier d’audit et de reproduction

Ce dossier contient les rapports, les entrées et sorties brutes du banc indépendant, les journaux de lancement, les reçus du paquet V1 extrait proprement, les formalismes comparés, le registre d’implémentation, le registre de preuves, les incidents historiques et l’archive source V0 utilisée comme baseline.

## Résumé des preuves

- Source V0 testée : `source_Dmodel_NGeGenBrain_v0.zip` ; SHA-256 : `6ffcc921732a9c58bda5d2aa1461bfa5d9dfad99cc5ef6e3b9331d85b078fe8d`.
- Archive V1 finale testée : `Dmodel_NGeGenBrain_v1.zip` est livrée à part; SHA-256 : `71534f98ff590e5c1a103888f0e553e9e8966d34d7f0364429eac8eae238b5c8`.
- Banc commun : `independent_hard_bench_v1.py`, SHA-256 `9325f55cf7e8694fd88c6f6df928e5b4a9f568f447fd41e6b80014659749b816`.
- Graine : `20261027`; même 15 ID de cas; V0 `8 PASS / 7 FAIL`, V1 final `15 PASS / 0 FAIL`.
- Suite V1 : 65/65 tests; validateur : 31/31; CLI smoke : 6/6; HTTP smoke : 6/6. SQLite `integrity_check=ok`, aucune violation de clé étrangère.

## Contenu

- `REPORT_AUDIT_NGeGenBrain_v1_FINAL.md` : rapport complet (description, architecture, pipeline, commandes, résultats détaillés, interprétations, conséquences et statut).
- `baseline_hard_benchmark_v0_replayed.json` et `hard_benchmark_v1_final.json` : sorties brutes des 15 cas, dont chaque observation attendue/observée et verdict.
- `comparison_v0_v1_final.json` : comparaison appariée et hash/identifiants/graine.
- `final_*`, `cli_*`, `web_*` : journaux et reçus d’exécution clean-room du paquet V1 exact.
- `NGeGenBrain_v1_mise_en_oevre.json` et `preuves_NGeGenBrain_v1.json` : lien exigences → formalisme → symboles de code → tests.
- `v0_historical/` : rapport, reçus et journaux de l’ancienne version conservés pour l’audit historique.
- `formalism_sources/` : sources LaTeX utilisées et théorie 3 enrichie.
- `source_Dmodel_NGeGenBrain_v0.zip` : archive V0 immuable à l’origine des cas baseline.

## Reproduire

Extraire le paquet V1 Dmodel, puis utiliser son répertoire racine comme `--model-root` :

```sh
python3 independent_hard_bench_v1.py \
  --model-root /path/to/extracted/Dmodel_NGeGenBrain_v1 \
  --source-archive /path/to/Dmodel_NGeGenBrain_v1.zip \
  --output hard_benchmark_v1_replay.json \
  --seed 20261027
```

Pour le baseline, utiliser le zip V0 exact et la même commande/le même script/la même graine. Les résultats de cette archive sont conservés, et aucune valeur de sortie attendue n’est injectée dans le runtime.

## Limites explicites

Le benchmark est fini et cible 15 propriétés; il ne prouve pas l’absence de tous défauts. La validation native Windows n’a pas été faite. L’équivalence historique avec des exécutables ASCR/AAM absents n’est pas démontrée; ASCR-NG est une reconstruction documentée.
