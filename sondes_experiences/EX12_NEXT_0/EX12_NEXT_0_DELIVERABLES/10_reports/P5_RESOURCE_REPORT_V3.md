# P5 — Qualité, coût, stabilité et benchmark des ressources

Statut : **PASS**

Modèles profilés : 560/560.
Cellules brutes : 13440/13 440.
Latences élémentaires conservées : 1,075,200.
Paires candidates–MLP profilées : 2560.

## Protocole

CPU mono-thread, float32, batch sizes 1/16/64/256, 12 warm-ups, 3 blocs indépendants de 80 mesures. Deux chemins séparés : modèle seul sur entrées normalisées et normalisation + modèle. Les quantiles sont recalculés depuis les temps bruts.

## Latence p50 relative au MLP apparié

| Variante | Batch | Chemin | Paires | Ratio médian | Fraction plus rapide |
|---|---:|---|---:|---:|---:|
| R0 | 1 | model_only | 80 | 1.894× | 0.0% |
| R0 | 1 | normalization_plus_model | 80 | 1.825× | 0.0% |
| R0 | 16 | model_only | 80 | 1.945× | 0.0% |
| R0 | 16 | normalization_plus_model | 80 | 1.879× | 0.0% |
| R0 | 64 | model_only | 80 | 2.185× | 0.0% |
| R0 | 64 | normalization_plus_model | 80 | 2.112× | 0.0% |
| R0 | 256 | model_only | 80 | 2.661× | 0.0% |
| R0 | 256 | normalization_plus_model | 80 | 2.586× | 0.0% |
| C2 | 1 | model_only | 80 | 1.903× | 0.0% |
| C2 | 1 | normalization_plus_model | 80 | 1.824× | 0.0% |
| C2 | 16 | model_only | 80 | 1.956× | 0.0% |
| C2 | 16 | normalization_plus_model | 80 | 1.894× | 0.0% |
| C2 | 64 | model_only | 80 | 2.207× | 0.0% |
| C2 | 64 | normalization_plus_model | 80 | 2.127× | 0.0% |
| C2 | 256 | model_only | 80 | 2.699× | 0.0% |
| C2 | 256 | normalization_plus_model | 80 | 2.609× | 0.0% |
| C3 | 1 | model_only | 80 | 2.048× | 0.0% |
| C3 | 1 | normalization_plus_model | 80 | 1.955× | 0.0% |
| C3 | 16 | model_only | 80 | 2.120× | 0.0% |
| C3 | 16 | normalization_plus_model | 80 | 2.019× | 0.0% |
| C3 | 64 | model_only | 80 | 2.406× | 0.0% |
| C3 | 64 | normalization_plus_model | 80 | 2.291× | 0.0% |
| C3 | 256 | model_only | 80 | 3.130× | 0.0% |
| C3 | 256 | normalization_plus_model | 80 | 2.922× | 0.0% |
| C4 | 1 | model_only | 80 | 2.386× | 0.0% |
| C4 | 1 | normalization_plus_model | 80 | 2.254× | 0.0% |
| C4 | 16 | model_only | 80 | 2.413× | 0.0% |
| C4 | 16 | normalization_plus_model | 80 | 2.280× | 0.0% |
| C4 | 64 | model_only | 80 | 2.650× | 0.0% |
| C4 | 64 | normalization_plus_model | 80 | 2.525× | 0.0% |
| C4 | 256 | model_only | 80 | 3.265× | 0.0% |
| C4 | 256 | normalization_plus_model | 80 | 3.104× | 0.0% |

## Temps d’entraînement enregistré

Les ratios de temps sont des mesures end-to-end issues des registres d'entraînement P3/P4. Ils incluent initialisation, évaluation, diagnostics de couverture et écriture d'artefacts pour P3 ; ils ne constituent donc pas une mesure pure du temps passé dans l'optimiseur. Ils sont publiés à titre descriptif, sans conclusion de vitesse causale.

## Mémoire

La mémoire exacte des paramètres, buffers, normaliseurs et checkpoints est publiée par modèle dans `P5_V3_MEMORY_PAIRED.csv`. Le RSS est une observation du processus séquentiel, et non un pic isolé par modèle. Aucun GPU ni instrument énergétique validé n'était disponible ; ces dimensions sont explicitement non mesurées.

## Stabilité de validation

`P5_V3_VALIDATION_STABILITY.csv` fournit les deltas appariés par tâche, graine et régime, avec IC descriptifs à 95 %. Ces dix graines sont pilotes ; les IC ne sont pas des résultats confirmatoires et aucun test/holdout n'a été consulté.

## Pareto

La frontière de Pareto est calculée séparément sur NMAE d'interpolation des quatre fonctions principales, latence p50 batch 1, temps de pipeline enregistré et taille mémoire exacte. La log-loss de classification et la validation Diabetes sont rapportées séparément car elles ne doivent pas être amalgamées à la NMAE de régression.

## Limites et anomalies conservées

- CPU-only benchmark; no GPU measurements available in this runtime.
- Energy was not measured because no validated physical energy instrument is available.
- Per-model isolated peak RSS was not measurable in the sequential process; exact tensor/buffer/normalizer bytes and checkpoint sizes are reported, with process RSS observations clearly labeled.
- Training times are immutable P3/P4 full-run elapsed times, not pure optimizer-loop durations; P3 includes model initialization, validation, coverage diagnostics and artifact writing. They are descriptive only and not used as definitive training-speed superiority evidence.
- The canonical V3 reproduction uses two immutable scripts: benchmark_p5_timing_repro_v3.py for the initial complete batches and benchmark_p5_timing_repro_v3_resume.py for resume-safe continuation. Each raw cell and memory row contains its exact script path and SHA-256, independently checked by this audit.

## Erreurs de complétude

Aucune erreur de complétude détectée.

## Provenance historique et reproduction indépendante

Le jeu antérieur `P5_TIMING_RAW.jsonl` est conservé sans modification. Ses 24 cellules initiales sont reliées au script v1 présent ; les 13 416 autres cellules déclarent le hash v2 `2fc228bbc66b919c30dbbcc7d3aaaa76b0f0a3770cb7785d58e3b292ec31df53`, mais le fichier source exact n'a pas été retrouvé. Cette lacune est décrite et signée dans `10_reports/RAPPORT_LACUNE_REPRODUCTIBILITE_P5_V2.md` et `.tex`.

La campagne V3 a été exécutée indépendamment avec les scripts livrés et hashés. Les 13 440 cellules anciennes sont appariables par identifiant aux 13 440 cellules V3. Le ratio médian `p50_V3 / p50_historique` est 0,99747 (IQR 0,98375–1,01255) ; 90,45 % des cellules sont à moins de 10 % d'écart. Cela confirme la cohérence des conclusions agrégées, sans restaurer le source v2 absent ni prétendre que les temps individuels sont identiques. Le CSV complet est `09_analysis/P5_V2_V3_CELL_REPLICATION.csv`.
