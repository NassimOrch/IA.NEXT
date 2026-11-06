# Audit indépendant de la campagne — version v6

## Résumé des contrôles

- Identifiant : `NG-ADAPT-INDEPENDENT-AUDIT-v6`.
- Contrôles instrumentés : **49**.
- Réussis : **49** ; échoués : **0**.
- Archive source SHA-256 : `8fcf82931988a96cdfb1ff5cbe5892142b4b1174385dc87cd9ed0f9e2d7069bb`.
- Archives imbriquées testées : **80/80**, aucune archive défaillante ni chemin dangereux détecté.
- Registre web : **40 URL uniques**, **28 requêtes** avec motif et disposition; la traçabilité d’anciennes recherches non récupérables est explicitement limitée.

## Ce que l’audit couvre

1. SHA-256 de l’archive racine et intégrité ZIP; extraction récursive, chemins et liens symboliques.
2. Manifeste de 14 970 entrées de fichiers à travers les deux vues d’extraction, contrôles syntaxiques Python et comptage des fichiers JSON/JSONL malformés.
3. Complétude des 165 runs A–K sur cinq tâches binaires et recalcul post-hoc des métriques sur **29 403 prédictions de test**.
4. Extension multiclasse digits10 : **33 runs**, **8 910 prédictions** et **2 700 événements d’empreinte**; contrôle des splits/scaler, recalcul des métriques, ordre prévision → révélation → adaptation, et agrégats.
5. Benchmark principal combiné : **198 runs sur six tâches**, soit **38 313 prédictions** et **11 610 événements d’empreinte** pour les tâches A–K. Les runs additionnels n’effacent pas le fait que digits10 est une extension nouvelle et non un rejeu strict du protocole historique.
6. Ablation de coordination : 60 runs; lorsque le coordinateur est gelé avec poids uniformes, les prédictions comparées aux sondes locales sont identiques pour 2 673 lignes (différence absolue maximale nulle).
7. Robustesse de boucle : 120 lignes métriques, 16 200 événements d’empreinte, contrôles de baseline et de mise à jour désactivée.
8. FBR-1 et RBF-R1 : vérifier que les décisions de gate/routage sont pilotées par le signal d’empreinte dans les protocoles ciblés, et non simplement journalisées. FBR-1 reste limité aux architectures A–E sur une tâche synthétique; RBF-R1 traite deux modèles de reconstruction.
9. Reconstruction : 148 lignes métriques et 2 880 empreintes pour l’expérience de base; identité directe identifiée comme contrôle trivial non appris et aucun accès direct de la seconde sonde à l’entrée n’est autorisé. RBF-R1 complète cette analyse par 162 lignes et 23 040 événements.
10. Validateurs des paquets d’origine : bundle observation, expérience v1.2, manifestes v2/v3.1 et suites de tests consignés.
11. Registre `sites_web_consulte.json` : URL uniques, requêtes, motifs d’utilisation, disposition des sources et caveat de traçabilité historique.

## Contrôle numérique digits10

Les prédictions brutes du CSV n’ont pas été modifiées. Le plus grand écart observé entre la somme d’une ligne de probabilités et 1 est `2.3991663589129075e-7`, compatible avec l’export de probabilités softmax en float32. Pour un recalcul stable, les vecteurs sont renormalisés uniquement dans la copie en mémoire utilisée pour les métriques. L’écart absolu maximal entre les métriques sauvegardées et recalculées après normalisation est `2.4422297517645575e-11`; aucune différence ne dépasse la tolérance d’audit. Aucun entraînement n’a été relancé pour ce contrôle.

## Anomalies et limites conservées

- `batch_dataset.jsonl` contient 783 objets valides sur 784 lignes; la dernière ligne est tronquée.
- `Screenplay_dataset.jsonl` contient 4 000 lignes JSON valides, mais 2 000 objets distincts chacun dupliqués une fois.
- Quatre fichiers JSON et un fichier JSONL source sont signalés malformés; les sources ne sont pas réparées silencieusement.
- `0000.parquet` n’a été vérifié qu’au niveau de sa signature de fichier, faute de décodeur Parquet disponible; aucun résultat scientifique n’est revendiqué à partir de ce contenu.
- Certains hash de checkpoints dans d’anciennes livraisons ne correspondent pas à l’archive racine actuelle; le présent audit est lié au SHA indiqué ci-dessus.
- Un seul split par tâche et trois graines d’optimisation ne constituent pas trois échantillons indépendants. Aucun benchmark FLOPs/RSS strictement égalisé ni protocole confirmatoire multi-split n’est fourni.

## Interprétation correcte

**49/49 signifie que les invariants techniques instrumentés passent sur les artefacts examinés.** Cela ne prouve ni la validité universelle d’une architecture, ni l’absence de toute fuite sémantique, ni la stabilité générale d’un algorithme adaptatif. Les phases 1, 4 et 8 restent partielles comme indiqué dans `ETAT_DES_PHASES.md`. Les résultats négatifs (dérive de boucle et dégradation RBF-R1) restent inclus.

### Contrôles passés par nom

- **PASS** — `source_archive_sha256` — {"entries": 26, "sha256": "8fcf82931988a96cdfb1ff5cbe5892142b4b1174385dc87cd9ed0f9e2d7069bb"}
- **PASS** — `source_archive_integrity` — {"first_bad_member": null}
- **PASS** — `recursive_zip_validation` — {"archives": 80, "failed": 0, "unsafe": 0}
- **PASS** — `recursive_source_file_manifest_complete` — {"recursive_extracted": {"bytes": 378456251, "file_count": 4132}, "rows": 14970, "source_tree": {"bytes": 869746379, "file_count": 10838}, "summary_count": 14970}
- **PASS** — `recursive_source_syntax_checks_accounted` — {"json_invalid": 4, "jsonl_invalid_files": 1, "pdf_magic_invalid": 0, "python_syntax_errors": 0}
- **PASS** — `two_moons_run_completeness` — {"errors": 0, "fingerprints": 2700, "predictions": 8910, "runs": 33, "status": "completed"}
- **PASS** — `two_moons_partition_disjointness` — {"cross_split_feature_hashes": 0}
- **PASS** — `circles_run_completeness` — {"errors": 0, "fingerprints": 2700, "predictions": 8910, "runs": 33, "status": "completed"}
- **PASS** — `circles_partition_disjointness` — {"cross_split_feature_hashes": 0}
- **PASS** — `xor_product_run_completeness` — {"errors": 0, "fingerprints": 2700, "predictions": 8910, "runs": 33, "status": "completed"}
- **PASS** — `xor_product_partition_disjointness` — {"cross_split_feature_hashes": 0}
- **PASS** — `wine_binary_run_completeness` — {"errors": 0, "fingerprints": 270, "predictions": 891, "runs": 33, "status": "completed"}
- **PASS** — `wine_binary_partition_disjointness` — {"cross_split_feature_hashes": 0}
- **PASS** — `digits_3_vs_8_run_completeness` — {"errors": 0, "fingerprints": 540, "predictions": 1782, "runs": 33, "status": "completed"}
- **PASS** — `digits_3_vs_8_partition_disjointness` — {"cross_split_feature_hashes": 0}
- **PASS** — `all_main_metrics_recomputed` — {"discrepancies": [], "models": 165, "predictions": 29403}
- **PASS** — `global_coordination_ablation_complete` — {"audit": {"compared_probability_rows": 2673, "exactly_equal_probability_rows": 2673, "max_abs_probability_diff_B_vs_C_frozen": 0.0}, "errors": 0, "runs": 60}
- **PASS** — `frozen_global_equals_local` — {"compared_probability_rows": 2673, "exactly_equal_probability_rows": 2673, "max_abs_probability_diff_B_vs_C_frozen": 0.0}
- **PASS** — `loop_robustness_complete` — {"conditions": ["clean_full_update", "covariate_shift_stream", "label_noise_20pct", "misleading_labels_50pct", "missing_30pct", "no_loop_baseline", "updates_disabled"], "errors": 0, "fingerprint_rows": 16200, "per_seed_rows": 120}
- **PASS** — `loop_disabled_is_controlled` — {"rows_baseline": 15, "rows_disabled": 15}
- **PASS** — `reconstruction_experiment_complete` — {"config": {"epochs_global": 300, "errors": [], "fingerprint_events": 2880, "identity_included": true, "loop_models": ["RBF2_free_global_loop", "RBF2_free_tanh_global_loop"], "lr": 0.01, "model_names": ["RBF2_free_untrained", "RBF2_free_local", "RBF2_free_global", "RBF2_free_tanh_global", "RBF3_free_global", "RBF2_bottleneck1_global", "MLP_AE_latent1", "MLP_AE_latent2"], "model_seeds": [101, 202, 303], "n_metrics_rows": 148, "no_input_skip_connection": true, "no_original_x_argument_to_second_probe": true, "noise_sigma": 0.1, "online_optimizer_state_for_loop": "fresh Adam state at loop start; reset is explicit in code, not reused silently from pretraining", "shift_vector": [0.75, 0.0], "sourc
- **PASS** — `identity_baseline_exact` — {"n_identity_rows": 1, "rmse": [0.0]}
- **PASS** — `composition_has_no_skip_connection` — {"no_skip": true, "no_x_to_g": true}
- **PASS** — `reconstruction_parameter_accounting` — {"requires_grad_after_fit": [122.0, 122.0, 122.0], "rows": 3, "stored": [244.0, 244.0, 244.0], "updated": [244.0, 244.0, 244.0]}
- **PASS** — `fingerprint_feedback_config_complete` — {"completed_pairs": 15, "errors": 0, "fingerprints": 54000, "metrics": 390, "requested_architectures": ["A", "B", "C", "D", "E"], "requested_seeds": [1501, 1607, 1717], "status": "completed"}
- **PASS** — `fingerprint_feedback_chunks_complete` — {"config_count": 15, "expected_count": 15, "extra_tags": [], "issues": [], "missing_tags": []}
- **PASS** — `fingerprint_feedback_events_unique_and_actions_match` — {"actions_match": true, "events": 54000, "unique_fingerprints": 54000}
- **PASS** — `fingerprint_feedback_seed_metadata_matches_data` — {"architectures": ["A", "B", "C", "D", "E"], "pairs": 15, "seeds": [1501, 1607, 1717]}
- **PASS** — `fingerprint_feedback_causal_order_and_no_test_update` — {"source_update_uses_observed_label": true, "test_evaluated_after_stream_freezes": true, "test_labels_passed_to_updates": false, "threshold_source": "q90 absolute probability residual measured on clean validation only, before adaptation; no test selection"}
- **PASS** — `RBF_R1_completeness_and_checkpoints` — {"chunk_count": 6, "chunk_issues": [], "errors": [], "event_rows": 23040, "metric_rows": 162, "missing_pairs": [], "pairs": 6, "status": "completed", "summary_groups": 54}
- **PASS** — `RBF_R1_unique_events_and_action_record` — {"actions_match_decisions": true, "rows": 23040, "unique_event_keys": 23040, "unique_fingerprint_hashes": 23040}
- **PASS** — `RBF_R1_policy_rules_and_missingness` — {"examples": [], "gate_updates": 46, "missing_events": 1608, "policy_mismatches_or_missing_updates": 0, "updates_on_missing": 0}
- **PASS** — `RBF_R1_causal_order_and_test_isolation` — {"test_isolation_flags_all_true": true, "threshold_from_clean_validation": true, "updates_use_adaptation_stream": true}
- **PASS** — `RBF_R1_summary_recomputed` — {"groups": 54, "mismatches": []}
- **PASS** — `reconstruction_feedback_gate_complete` — {"chunk_issues": [], "errors": [], "fingerprints": 23040, "metrics": 162, "pairs": 6, "status": "completed", "summary_rows": 54}
- **PASS** — `reconstruction_feedback_gate_event_integrity` — {"code_order_verified": true, "rows": 23040, "test_data_excluded": true, "unique_fingerprints": 23040, "updates_match_decisions": true}
- **PASS** — `reconstruction_feedback_no_update_reproduces_baseline` — {"comparisons": 30, "differences": [], "metrics_compared": ["rmse", "mae", "r2_scalar", "p90_vector_error", "max_vector_error"]}
- **PASS** — `digits10_completeness_and_checkpoints` — {"chunk_issues": [], "chunks": 33, "classes": 10, "errors": 0, "expected_runs": 33, "fingerprints": 2700, "missing_tags": [], "predictions": 8910, "retained_n": 1797, "runs": 33, "source_n": 1797, "status": "completed"}
- **PASS** — `digits10_split_integrity_and_train_only_scaler` — {"counts": {"adaptation": 180, "test": 270, "train": 1077, "validation": 270}, "cross_split_overlaps": {"adaptation:test": 0, "train:adaptation": 0, "train:test": 0, "train:validation": 0, "validation:adaptation": 0, "validation:test": 0}, "scaler_fit_n": 1077, "train_n": 1077}
- **PASS** — `digits10_predictions_and_metrics_recomputed` — {"argmax_matches_label": true, "difference_count": 0, "matches_test_ledger": true, "max_abs_metric_difference_after_normalization": 2.4422297517645575e-11, "max_abs_probability_row_mass_error_before_normalization": 2.3991663589129075e-07, "metric_or_confusion_differences": [], "metric_recomputation_row_normalization": "each saved probability row divided by its sum for stable metric recomputation; raw prediction file retained unchanged", "predictions": 8910, "probabilities_valid": true, "unique_keys": true}
- **PASS** — `digits10_fingerprint_order_stream_isolation_and_trigger` — {"adaptation_stream_only": true, "events": 2700, "static_order_checks": true, "test_hash_overlap": 0, "threshold_or_trigger_issues": [], "unique_keys": true}
- **PASS** — `digits10_summary_recomputed` — {"mismatch_count": 0, "mismatches": [], "summary_rows": 11}
- **PASS** — `website_consultation_ledger_complete_and_caveated` — {"all_items_have_purpose_and_disposition": true, "historical_url_caveat_present": true, "queries": 17, "unique_urls": 34, "websites": 34}
- **PASS** — `validator_observation_bundle` — {"exit_code": 0}
- **PASS** — `validator_v1_2_validator` — {"exit_code": 0}
- **PASS** — `validator_ngbrain_v2_manifest` — {"exit_code": 0}
- **PASS** — `validator_ngbrain_v3_1_clean_manifest` — {"exit_code": 0}
- **PASS** — `validator_ngbrain_v3_1_pytest` — {"exit_code": 0}
- **PASS** — `validator_ngbrain_v3_1_legacy` — {"exit_code": 0}
