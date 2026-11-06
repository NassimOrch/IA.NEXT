# Reproduction et commandes EX5 — clôture v001–v007

Racine canonique : `/mnt/data/sondes_research_workspace_ex5/`. Environnement de référence : CPU-only, 3 cœurs, PyTorch CPU. Pour comparer les temps, fixer `OMP_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`.

## Règle de reprise

Les expériences complètes ne doivent pas être relancées pour produire de nouveaux fichiers. Les registres `results/raw/`, checkpoints, prédictions et marqueurs `*_complete.json` sont les sources d'autorité. Toute reprise doit utiliser le mécanisme idempotent propre à la version et ne traiter que les clés absentes. Ne jamais écraser les sources EX2/EX3/EX4, les JSONL historiques ou les snapshots test scellés.

## Tests versionnés

- v001 : depuis `versions/sondes_ex5_v001__2026-10-30/` : `python tests/test_ex5_final_integrity.py` et `python tests/test_adam_freeze_semantics.py`.
- v002 : `python tests/test_alternating_freeze.py` et `python tests/test_adam_freeze_semantics.py`.
- v003 : `python tests/test_external_split.py`.
- v004 : `pytest -q tests` (2 tests).
- v005 : `pytest -q tests` (1 test).
- v006 : `pytest -q tests` (3 tests). Le profilage `src/run_vectorized_inference.py` est un audit, pas un réentraînement ; `src/run_pca_q_mixa.py` ne doit être repris que si les marqueurs montrent une clé manquante.
- v007 : les trois fonctions de `versions/sondes_ex5_v007__2026-10-30/tests/test_profile_integrity.py` ont été invoquées individuellement et passent. Une collecte pytest globale a dépassé la fenêtre de commande ; ne pas écrire « suite pytest globale PASS ».

## Tests OOF / hiérarchie

Depuis la racine du workspace :

```bash
pytest -q tests/test_oof_mlp_pairing.py tests/test_oof_artifacts_complete.py
python scripts/audit_oof_artifacts_ex5.py
```

L'audit OOF contrôle les 5 folds × 5 graines, les états de reprise Adam, les prédictions OOF, la réinférence du composite, les métriques et les 20 liens MLP (matched/ge4x). L'audit a produit 162 lignes dans `deliverables/oof_artifact_manifest_ex5.csv` et aucune référence requise manquante.

## Audits globaux / catalogue

```bash
python scripts/audit_integrite_global_ex5.py
python scripts/build_variant_catalogue_ex5.py
python scripts/final_workspace_integrity_audit.py
```

`audit_integrite_global_ex5.py` vérifie les registres versionnés, hashes checkpoint/prédiction, recalcul des métriques et ratios MLP ge4x. `build_variant_catalogue_ex5.py` reconstruit le catalogue des candidats et campagnes. `final_workspace_integrity_audit.py` vérifie le parsing JSON/JSONL/CSV, les hashes du prompt et le confinement des chemins.

## Profilage v007 : méthode de test stable

Les tests v007 s'exécutent de façon isolée pour éviter de re-déclencher les compilations et le profilage complet :

```bash
python - <<'PY'
import importlib.util
p='versions/sondes_ex5_v007__2026-10-30/tests/test_profile_integrity.py'
s=importlib.util.spec_from_file_location('ex5_v007_tests', p)
m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
for name in ('test_all_exported_model_hashes',
             'test_optimized_and_numba_v2_not_misclassified_as_pass',
             'test_torchscript_trace_strict_parity_and_ge4x'):
    getattr(m, name)()
    print('PASS', name)
PY
```

## Limites non contournées

Wine et Digits ont été ouverts uniquement après le manifeste de gel v003 ; leurs graines sont des initialisations sur les mêmes sujets, pas des échantillons indépendants supplémentaires. Banknote/MAGIC n'ont pas été fabriqués ni remplacés lorsque DNS a échoué. L'énergie, la VRAM (CPU-only) et les MACs complets d'entraînement restent non mesurés. Un résultat de test ne doit jamais être réutilisé pour sélectionner ou retuner une candidate.
