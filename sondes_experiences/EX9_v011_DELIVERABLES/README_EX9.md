# EX9 v011 — Sondes adaptatives

Workspace autonome. Les sources EX3–EX8 sont restées à l'extérieur ; aucun ZIP historique, ancien checkpoint ni backup EX3–EX8 n'est livré dans ce dossier.

## Livrables prioritaires

- `prompt_ex9.json` : prompt EX9 final validé ; copie exacte dans `deliverables/prompt_ex9.json`.
- `deliverables/SYNTHESE_EX9_v011.md` : verdict global et état d'achèvement.
- `deliverables/SYNTHETIC_CONFIRMATION_EX9.md` : résultats des deux tests synthétiques gelés.
- `deliverables/th_sondes_core_test_1.tex` et `.pdf` : théorie corrigée CNG/CNC.
- `MODEL_LOCK.json` : verrou historique 45 runs XOR8 avant tentative d'ouverture ; XOR8 est ensuite déclaré compromis/non scoré.
- `MODEL_LOCK_MULTI_DOMAIN.json` : snapshot pré-test de 295 hashes pour concentric2/rotated_moons2, tests synthétiques scorés une fois ; contrôle post-test 294/295, avec une exception de rapport uniquement (voir `reports/PROMPT_EX9_AUDIT_LOCK_EXCEPTION.md`).

## Exécution réellement présente

- Historique EX8 : catalogue A0–A4, B1–B11 ; récupération intégrale B10/B11, checkpoints, traces, prédictions, configurations et contrôles d'intégrité. Voir `reports/EX8_VARIANT_CATALOG.md` et `inputs/AUDIT_SOURCES_EX9.md`.
- Classification XOR8 développement : 45 runs Rev2 B10/B11/A0 + deux MLP par candidate/seed ; audit validation PASS 45/45 ; les candidates perdent contre MLP.
- Ablations B10 : 7 familles × 5 seeds = 35 runs table-only ; audit PASS 35/35 ; exploratoires sur validation réutilisée.
- Deux domaines synthétiques supplémentaires : concentric2 et rotated_moons2, 45 runs par domaine ; audit validation PASS 90/90, historiques MLP conservés.
- Holdouts synthétiques concentric2/rotated_moons2 : 90 scores ; audit post-score PASS 90/90 ; les trois sondes perdent 5/5 face aux deux MLP dans chacun des deux domaines.
- Coeur neuronal : 3 pilotes CNG et 6 spécialistes CNC, audit PASS 9/9 ; pas de graphes CNC complets C1/C2.
- `th_sondes_core_test_1.tex` compile en PDF après correction du prérequis LaTeX.

## Verdict scientifique

Les performances positives EX8 de B10/B11 sur Wisconsin sont historiques et spécifiques au domaine de développement. Elles ne se reproduisent ni sur XOR8 ni sur les deux domaines synthétiques additionnels. Sur concentric2/rotated_moons2, les log-loss test des sondes sont de 0,2009–0,2561 contre 0,0586–0,0649 et 0,1210–0,1223 pour les MLP ; les p50 batch1 CPU des sondes sont environ 12–22× plus élevés. Le ratio de paramètres face au MLP_GE4X est bien ≥4× mais ne compense ni la perte de qualité ni la latence.

Aucune donnée réelle externe vierge n'a été obtenue ; la conclusion n'est donc pas une confirmation générale sur données du monde réel. FLOPs/MAC complets, RSS peak par run et énergie restent non mesurés. Les extensions A0, les ablations de partage/distillation/kernels B10/B11 et la campagne complète CNG/CNC restent partielles.

## Audits

```bash
python -m pytest -q tests
python src/audit_classification.py
python src/audit_checkpoint_deserialization.py
python src/audit_b10_ablations.py
python src/audit_core_pilot.py
python src/audit_multi_domain.py
python src/audit_multi_domain_test_metrics.py
```

Ne pas exécuter `src/score_sealed_test.py` (XOR8 compromis) ni `src/open_score_multi_synth.py --open-test` (les deux tests synthétiques additionnels sont déjà ouverts/scorés). Les scripts d'audit lisent uniquement des artefacts déjà sauvegardés et ne réentraînent pas de modèles.

Voir `reports/EVIDENCE_MATRIX_EX9.md`, `reports/REPORT_EX9_FINAL.md`, `reports/TRACE_CAPTURE_GAP.md` et `FAILURES_AND_DEVIATIONS.md` avant toute reprise.
