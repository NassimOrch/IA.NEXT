# Audit final d’intégrité EX5

- JSON : 1 151 fichiers analysés, tous parsés.
- JSONL : 32 fichiers, 829 lignes analysées, toutes parsées.
- Hashes checkpoints : 532 références, 0 échec.
- Hashes prédictions canoniques : 495 références, 0 échec.
- Prédictions externes validation v3 reconstruites par graine : 20 fichiers uniques, métriques concordantes.
- Métriques recalculées sur les prédictions brutes et les deux résultats test v3 : 0 divergence.
- MLP ge4x : toutes les comparaisons du registre atteignent le ratio `P_MLP_total/P_sonde_total ≥ 4`; minimum observé 4,000735×.
- Gels Adam : 20/20 gels stricts PASS.
- Alternance A↔B stricte : 5/5 runs, cycles complets, 2 cycles sans progrès, hashes de gel PASS.
- Test externe : manifeste `FROZEN_BEFORE_TEST_FEATURE_OR_LABEL_ACCESS`, deux domaines.
- Checkpoints modèles : 1 190 fichiers `.pt`, tous non vides ; inventaire SHA prévu dans checksums.

## Exceptions conservées

Les registres bruts `external_v3_*_probe_runs.jsonl` contiennent des pointeurs de prédictions historiques dont le nom omettait la graine. Ces fichiers bruts n’ont pas été modifiés ; 16 pointeurs y sont effectivement périmés. Les sidecars `external_v3_*_probe_runs_corrected.jsonl` conservent les anciennes colonnes pour provenance, mais `prediction_file_corrected`/`prediction_sha256_corrected` est la référence canonique : 20 prédictions uniques, hashes et métriques revérifiés. Le nombre total de références obsolètes documentées (pointeurs source et colonnes héritées) est consigné dans le JSON d’audit.

Le registre RETRO conserve une ligne dupliquée (`retro_linear`, seed 1501), sans suppression ; les agrégats utilisent le couple candidat/graine unique. Le registre global v007 EX4 et les tests externes v2 restent historiques/non canoniques.

**Verdict d’intégrité : PASS pour les artefacts canoniques ; exceptions historiques explicites et isolées.** L’intégrité ne signifie pas que les critères scientifiques de performance, ressources ou statistiques sont satisfaits.
