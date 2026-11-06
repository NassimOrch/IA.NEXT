# EX12 — Erratum de comptage du benchmark P5

Date : 2026-11-04

## Objet

Un message d'avancement a indiqué par erreur que P5 avait profilé 640 modèles et 256 000 mesures de latence. Ce comptage ne correspond pas au benchmark P5 canonique et ne doit pas être repris dans les rapports scientifiques.

## Source faisant autorité

Le contrôle de phase `00_governance/P5_phase_gate.json` est PASS (15/15) et consigne :

- 560 modèles et 560 enregistrements de mémoire ;
- 13 440 cellules de timing uniques ;
- 1 075 200 échantillons de latence positifs (80 par cellule) ;
- 2 560 lignes de latence candidate–MLP appariées ;
- 320 paires mémoire ;
- 320 paires de temps de pipeline ;
- aucune donnée test ou holdout consultée.

La reproduction canonique V3 et ses fichiers sont :

- `08_benchmarks/P5/P5_TIMING_REPRO_V3.jsonl` ;
- `08_benchmarks/P5/P5_TIMING_REPRO_V3_MODEL_MEMORY.jsonl` ;
- `09_analysis/P5_V3_LATENCY_OVERALL.csv` ;
- `09_analysis/P5_V3_LATENCY_AGGREGATES.csv` ;
- `09_analysis/P5_V3_MEMORY_PAIRED.csv` ;
- `09_analysis/P5_V3_TRAINING_TIME_PAIRED.csv` ;
- `09_analysis/P5_V3_PARETO_SCORECARD.csv` ;
- `09_analysis/P5_REPRO_V3_AUDIT.json`.

Le benchmark P5 V3 couvre 8 tâches × 10 graines × 7 slots de modèles × 4 tailles de batch × 2 chemins × 3 blocs, soit 13 440 cellules. Les 560 modèles correspondent à 8 tâches × 10 graines × 7 slots. Le nombre 640 et les 2 560 scores modèle×régime appartiennent à P7, pas à P5.

## Correction scientifique

Les tableaux finaux doivent utiliser les agrégats P5 V3, et distinguer les temps d'entraînement P3/P4 (pipeline complet descriptif) du temps passé dans l'optimiseur. Aucune mesure énergétique ou GPU n'est revendiquée ; le RSS est process-level et ne doit pas être présenté comme un pic attribuable à chaque modèle.

## Signature et portée

Rédigé par l'assistant OpenAI à partir des fichiers locaux et des registres EX12. Cette signature identifie le rédacteur du rapport ; ce n'est pas une signature numérique certifiée ni une expertise judiciaire. Le présent erratum rectifie une erreur de synthèse de l'assistant. Il n'indique ni suppression de données ni altération des résultats.
