# Parcours récursif Emplica Orchestra Org — de bout en bout

## Code source et exécution

Dans `workspace/sondes_ex7_v002__2026-10-31/src/` :

- `run_orchestra_org_recursive.py` : modèle récursif original (7 couches × 5 probes), coordination interne `pi`, coordination externe `rho`, cascade et modulation des LR.
- `run_orchestra_org_oof.py` : cross-fitting strict 3-fold ; fits fold et logits OOF.
- `run_ex7_org_stage_oof.py` : extraction des logits d'étages et correcteurs OOF d'étages.
- `run_orchestra_org_ablations.py` : six ablations causales × cinq graines.
- `run_orchestra_org_capacity_variants.py` : variantes profondeur/capacité, dont `centers_k4`.
- `run_orchestra_org_mlp_ge4x.py` : comparateurs MLP appariés ≥4×.
- `run_orchestra_org_parallel_layers.py`, `profile_orchestra_org_parallel_layers.py`, `profile_orchestra_org_vectorization.py`, `benchmark_parallel_oof_folds.py`, `org_oof_parallel_fold_worker.py` : parité, vectorisation et parallélisme.
- `audit_ex7_recursive_and_variants_v002.py`, `build_additional_org_mlp_comparisons_v002.py`, `validate_ex7_delivery.py` : audits, consolidation et vérification.

## Résultats

- `results/raw/` : journaux JSON bruts, prédictions, logits OOF par seed/étage, résultats d'ablation, mesures de profilage.
- `results/models/` : checkpoints racine, checkpoints de folds, états de reprise, correcteurs, MLP-ge4x et variantes de capacité/compression.
- `results/metrics/` et `deliverables/` : résultats par graine, agrégats, timings, ratios de paramètres, mesures batch/p99, comparaisons MLP et audits machine.
- `reports/AUDIT_COMPLETUDE_ORCHESTRA_ORG_EX7.md` et `reports/AUDIT_RECURSIVE_ORG_V002.md` : conclusion et preuves de complétude de la branche.

## Comptage séparé à utiliser

- Entraînements racine : 5 graines.
- Fits OOF : 15 (3 folds × 5 graines), distincts des 5 modèles racine.
- Correcteurs OOF racine : 3 variantes × 5 graines.
- Correcteurs OOF d'étages : 2 variantes × 5 graines.
- Ablations causales : 30 (6 × 5).
- Variantes profondeur/capacité : 25 (5 × 5).
- Variantes structurelles des correcteurs : 60 (6 × 2 familles × 5 graines).
- Contrôle couches indépendantes : 5 runs uniques.

Ne pas additionner les 15 fits de folds aux cinq graines racine comme s'il s'agissait de vingt graines indépendantes.
