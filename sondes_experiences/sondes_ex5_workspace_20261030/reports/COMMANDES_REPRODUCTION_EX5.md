# Reproduction EX5

Toutes les commandes s'exécutent depuis la version `sondes_ex5_v001__2026-10-30/`. Elles utilisent les journaux append-only et les checkpoints de reprise ; vérifier les hashes avant de relancer. Les campagnes terminées ne doivent pas être forcées en mode overwrite.

```bash
python src/run_retro_factorial.py
python src/run_retro_thaw_optimizer_v2.py
python src/run_mixa_proportions.py
python src/run_mixa_gate_refine.py
python src/run_mixa_geometry_sweep.py
python src/run_mixa_gate_geometry.py
python src/run_hierarchical_micro_mixa.py
python src/run_twolevel_oof_residual.py
python src/run_alternating_error_corrector.py
python src/run_alternating_error_corrector_strict_cycles.py
python src/run_external_label_blind_split.py
python src/rebuild_external_v3_validation_and_freeze.py
python scripts/build_ex5_reports.py
python tests/test_adam_freeze_semantics.py
python tests/test_ex5_final_integrity.py
```

Note : `run_external_label_blind_split.py` a déjà été exécuté et les v3 sont finalisées ; ne pas relancer en écrasement. Pour les données Banknote/MAGIC, le manifeste d'échec réseau est `results/processed/external_data_attempts.json`.
