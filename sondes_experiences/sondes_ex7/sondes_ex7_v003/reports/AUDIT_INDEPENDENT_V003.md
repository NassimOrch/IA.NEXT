# Audit indépendant V003

**Statut : PASS** — 91/91 contrôles réussis.

Les contrôles portent sur la provenance des entrées, les empreintes, la cohérence des prédictions, le recalcul indépendant des métriques, l’intégrité des références historiques, la couverture des profils de latence et la syntaxe des sources/JSON.

| Contrôle | Statut | Détail |
|---|---|---|
| prompt_sha256 | PASS | `"3faf35349da74b62db043e81a8889189132cc0ce6ad5e0bdc75eb068e8b066ea"` |
| development_data_sha256 | PASS | `"93f7a5f6ef8a5daa090bf83f4a2169a9857893f4aca4b700f7b74566b14be1da"` |
| dataset_required_keys | PASS | `["Xad", "Xtr", "Xva", "adaptation_row_ids", "scaler_mean", "scaler_scale", "train_row_ids", "validation_row_ids", "yad", "ytr", "yva"]` |
| dataset_contains_no_test_arrays | PASS | `[]` |
| dataset_shapes | PASS | `{"Xtr": [341, 30], "ytr": [341], "Xva": [85, 30], "yva": [85], "Xad": [57, 30], "yad": [57]}` |
| parent_archive_present_and_hashed | PASS | `"0286ff0da64e49dfdcbcf4cda7a30cbc16870bc1876c0cc977a05512c89f2b6b"` |
| outercoord_lite_7x1_seed1501_files | PASS | `"result, predictions and checkpoint exist"` |
| outercoord_lite_7x1_seed1501_prediction_integrity | PASS | `"85 validation probabilities, class sums 1, labels match validation"` |
| outercoord_lite_7x1_seed1501_hashes | PASS | `{"checkpoint_sha256": "466b091fe0140f20bc0078174c37ff2ba62184c0ba52a6822836e6f68be137b6", "predictions_sha256": "86cab10ef71b5a152ca5ecca446fdfa2490da5d6b16220de0a198ba1beaa7f75"}` |
| outercoord_lite_7x1_seed1501_no_test_flag | PASS | `"both result and predictions mark test_opened=false"` |
| outercoord_lite_7x1_seed1501_metrics_recomputed | PASS | `{"accuracy": 0.9764705882352941, "macro_precision": 0.9705882352941176, "macro_recall": 0.9811320754716981, "macro_f1": 0.9752331002331003, "balanced_accuracy": 0.98113207547169...` |
| outercoord_lite_7x1_seed1607_files | PASS | `"result, predictions and checkpoint exist"` |
| outercoord_lite_7x1_seed1607_prediction_integrity | PASS | `"85 validation probabilities, class sums 1, labels match validation"` |
| outercoord_lite_7x1_seed1607_hashes | PASS | `{"checkpoint_sha256": "9ed063a43909134d8edda46401e5cbae2b9779e6666b4c99f5aef99344589627", "predictions_sha256": "ac81aa96ea091d69126e10286827c9f353a1bd3a2d1803a3be1882536082b7a2"}` |
| outercoord_lite_7x1_seed1607_no_test_flag | PASS | `"both result and predictions mark test_opened=false"` |
| outercoord_lite_7x1_seed1607_metrics_recomputed | PASS | `{"accuracy": 0.9882352941176471, "macro_precision": 0.9848484848484849, "macro_recall": 0.9905660377358491, "macro_f1": 0.9875457875457876, "balanced_accuracy": 0.99056603773584...` |
| outercoord_lite_7x1_seed1717_files | PASS | `"result, predictions and checkpoint exist"` |
| outercoord_lite_7x1_seed1717_prediction_integrity | PASS | `"85 validation probabilities, class sums 1, labels match validation"` |
| outercoord_lite_7x1_seed1717_hashes | PASS | `{"checkpoint_sha256": "e5356d43b504a90bcfe7bf696e2dddeea0398f6a84eb3c84f160f18c8ade9f2c", "predictions_sha256": "d5ab11da8c2eb6b6f2c2aabaee65f47c7a7ff1c0c6b054d379bb06baf9055ea3"}` |
| outercoord_lite_7x1_seed1717_no_test_flag | PASS | `"both result and predictions mark test_opened=false"` |
| outercoord_lite_7x1_seed1717_metrics_recomputed | PASS | `{"accuracy": 0.9764705882352941, "macro_precision": 0.9705882352941176, "macro_recall": 0.9811320754716981, "macro_f1": 0.9752331002331003, "balanced_accuracy": 0.98113207547169...` |
| outercoord_lite_7x1_seed2029_files | PASS | `"result, predictions and checkpoint exist"` |
| outercoord_lite_7x1_seed2029_prediction_integrity | PASS | `"85 validation probabilities, class sums 1, labels match validation"` |
| outercoord_lite_7x1_seed2029_hashes | PASS | `{"checkpoint_sha256": "cf66187955a5aa0fcd3aebeaf676c05b00fb3b4add3c8102755b6859445f9515", "predictions_sha256": "c0b73bc5b4f7703357647eaa1d6fa7c2226a9136b5da4309d5af85b45dcf5711"}` |
| outercoord_lite_7x1_seed2029_no_test_flag | PASS | `"both result and predictions mark test_opened=false"` |
| outercoord_lite_7x1_seed2029_metrics_recomputed | PASS | `{"accuracy": 0.9764705882352941, "macro_precision": 0.9705882352941176, "macro_recall": 0.9811320754716981, "macro_f1": 0.9752331002331003, "balanced_accuracy": 0.98113207547169...` |
| outercoord_lite_7x1_seed3037_files | PASS | `"result, predictions and checkpoint exist"` |
| outercoord_lite_7x1_seed3037_prediction_integrity | PASS | `"85 validation probabilities, class sums 1, labels match validation"` |
| outercoord_lite_7x1_seed3037_hashes | PASS | `{"checkpoint_sha256": "9106041f1951c75d970222679bbcb5ea848632ef66546d9a699fbd6b0bd8e95e", "predictions_sha256": "9b336c001d7472d753bed7fc48b60d03d1fe876be1e3ffa059b04d94eaf4a6b4"}` |
| outercoord_lite_7x1_seed3037_no_test_flag | PASS | `"both result and predictions mark test_opened=false"` |
| outercoord_lite_7x1_seed3037_metrics_recomputed | PASS | `{"accuracy": 0.9764705882352941, "macro_precision": 0.9705882352941176, "macro_recall": 0.9811320754716981, "macro_f1": 0.9752331002331003, "balanced_accuracy": 0.98113207547169...` |
| outercoord_lite_mlp_matched_seed1501_files | PASS | `"result, predictions and checkpoint exist"` |
| outercoord_lite_mlp_matched_seed1501_prediction_integrity | PASS | `"85 validation probabilities, class sums 1, labels match validation"` |
| outercoord_lite_mlp_matched_seed1501_hashes | PASS | `{"checkpoint_sha256": "1de8ee3dee2a6428837efbcd2e3de0cfe130fd5451180eb9ddd5a857c3c938a3", "predictions_sha256": "4f0d0b1b609535cece507f385c5de594f779fac64962e975c81e81a4d3508a2a"}` |
| outercoord_lite_mlp_matched_seed1501_no_test_flag | PASS | `"both result and predictions mark test_opened=false"` |
| outercoord_lite_mlp_matched_seed1501_metrics_recomputed | PASS | `{"accuracy": 0.9764705882352941, "macro_precision": 0.9705882352941176, "macro_recall": 0.9811320754716981, "macro_f1": 0.9752331002331003, "balanced_accuracy": 0.98113207547169...` |
| outercoord_lite_mlp_matched_seed1607_files | PASS | `"result, predictions and checkpoint exist"` |
| outercoord_lite_mlp_matched_seed1607_prediction_integrity | PASS | `"85 validation probabilities, class sums 1, labels match validation"` |
| outercoord_lite_mlp_matched_seed1607_hashes | PASS | `{"checkpoint_sha256": "f17f5b0d87ca23848e509723a27c3d6fc2e1380fd33d6734f502a3992f659c65", "predictions_sha256": "abda2964f5e1a7876d340bcd4592b941c07cff133ebee2826cc6431129c12454"}` |
| outercoord_lite_mlp_matched_seed1607_no_test_flag | PASS | `"both result and predictions mark test_opened=false"` |
| outercoord_lite_mlp_matched_seed1607_metrics_recomputed | PASS | `{"accuracy": 0.9764705882352941, "macro_precision": 0.9705882352941176, "macro_recall": 0.9811320754716981, "macro_f1": 0.9752331002331003, "balanced_accuracy": 0.98113207547169...` |
| outercoord_lite_mlp_matched_seed1717_files | PASS | `"result, predictions and checkpoint exist"` |
| outercoord_lite_mlp_matched_seed1717_prediction_integrity | PASS | `"85 validation probabilities, class sums 1, labels match validation"` |
| outercoord_lite_mlp_matched_seed1717_hashes | PASS | `{"checkpoint_sha256": "1329c92ebf9d515b3b0aa22b287a88b5ecb2d49b429d848b5b4ff024b0f3da44", "predictions_sha256": "f3754c709570d59a22eae8ace22b817a6cc34bdf935a8a19eb1b48f977618525"}` |
| outercoord_lite_mlp_matched_seed1717_no_test_flag | PASS | `"both result and predictions mark test_opened=false"` |
| outercoord_lite_mlp_matched_seed1717_metrics_recomputed | PASS | `{"accuracy": 0.9764705882352941, "macro_precision": 0.9705882352941176, "macro_recall": 0.9811320754716981, "macro_f1": 0.9752331002331003, "balanced_accuracy": 0.98113207547169...` |
| outercoord_lite_mlp_matched_seed2029_files | PASS | `"result, predictions and checkpoint exist"` |
| outercoord_lite_mlp_matched_seed2029_prediction_integrity | PASS | `"85 validation probabilities, class sums 1, labels match validation"` |
| outercoord_lite_mlp_matched_seed2029_hashes | PASS | `{"checkpoint_sha256": "b92fd56aa8070b1b9ea3bd14eafb3965ffba604e5c69a3f4396f455f4317a359", "predictions_sha256": "84eda2ccc0b8c2c12eed8b7f5fc1c4dfc777fc19ee13c6bbd9e2cd3fe84d86ab"}` |
| outercoord_lite_mlp_matched_seed2029_no_test_flag | PASS | `"both result and predictions mark test_opened=false"` |
| outercoord_lite_mlp_matched_seed2029_metrics_recomputed | PASS | `{"accuracy": 0.9882352941176471, "macro_precision": 0.9848484848484849, "macro_recall": 0.9905660377358491, "macro_f1": 0.9875457875457876, "balanced_accuracy": 0.99056603773584...` |
| outercoord_lite_mlp_matched_seed3037_files | PASS | `"result, predictions and checkpoint exist"` |
| outercoord_lite_mlp_matched_seed3037_prediction_integrity | PASS | `"85 validation probabilities, class sums 1, labels match validation"` |
| outercoord_lite_mlp_matched_seed3037_hashes | PASS | `{"checkpoint_sha256": "92feec83214f41286845ec8012d237768d3e3518501af243ba12cdf948d1670c", "predictions_sha256": "293a2773c3437652e3cceec334cf8f5c44e89019d5a569376f4a3d5afef5973c"}` |
| outercoord_lite_mlp_matched_seed3037_no_test_flag | PASS | `"both result and predictions mark test_opened=false"` |
| outercoord_lite_mlp_matched_seed3037_metrics_recomputed | PASS | `{"accuracy": 0.9882352941176471, "macro_precision": 0.9848484848484849, "macro_recall": 0.9905660377358491, "macro_f1": 0.9875457875457876, "balanced_accuracy": 0.99056603773584...` |
| outercoord_lite_mlp_ge4x_seed1501_files | PASS | `"result, predictions and checkpoint exist"` |
| outercoord_lite_mlp_ge4x_seed1501_prediction_integrity | PASS | `"85 validation probabilities, class sums 1, labels match validation"` |
| outercoord_lite_mlp_ge4x_seed1501_hashes | PASS | `{"checkpoint_sha256": "bdf3966b645c76a51a584b93d49f5edbf5e4b92502dff8a7738f64c7e3286db1", "predictions_sha256": "b1e058328f450f9c503494408a1d07e53d249f2d376be6300179661ed9006075"}` |
| outercoord_lite_mlp_ge4x_seed1501_no_test_flag | PASS | `"both result and predictions mark test_opened=false"` |
| outercoord_lite_mlp_ge4x_seed1501_metrics_recomputed | PASS | `{"accuracy": 0.9764705882352941, "macro_precision": 0.9749410377358491, "macro_recall": 0.9749410377358491, "macro_f1": 0.9749410377358491, "balanced_accuracy": 0.97494103773584...` |
| outercoord_lite_mlp_ge4x_seed1607_files | PASS | `"result, predictions and checkpoint exist"` |
| outercoord_lite_mlp_ge4x_seed1607_prediction_integrity | PASS | `"85 validation probabilities, class sums 1, labels match validation"` |
| outercoord_lite_mlp_ge4x_seed1607_hashes | PASS | `{"checkpoint_sha256": "4d29d1a050a8594ecf966039997a3f7614e4b852db83f83374449704bb6b79d2", "predictions_sha256": "a1faad964702ad509b38d14cc5d1ad23e4068995d0df184668ef70048d3e3cb7"}` |
| outercoord_lite_mlp_ge4x_seed1607_no_test_flag | PASS | `"both result and predictions mark test_opened=false"` |
| outercoord_lite_mlp_ge4x_seed1607_metrics_recomputed | PASS | `{"accuracy": 0.9882352941176471, "macro_precision": 0.9848484848484849, "macro_recall": 0.9905660377358491, "macro_f1": 0.9875457875457876, "balanced_accuracy": 0.99056603773584...` |
| outercoord_lite_mlp_ge4x_seed1717_files | PASS | `"result, predictions and checkpoint exist"` |
| outercoord_lite_mlp_ge4x_seed1717_prediction_integrity | PASS | `"85 validation probabilities, class sums 1, labels match validation"` |
| outercoord_lite_mlp_ge4x_seed1717_hashes | PASS | `{"checkpoint_sha256": "88c5b9a3c2910a6ffc669bd2655907cf8cb5ba4d1d6ee0600d79f20ee5b65614", "predictions_sha256": "34461bdfe4072c5725cbf169ec06062e8b71aa27fbd3f8f9832fecec53e38bc6"}` |
| outercoord_lite_mlp_ge4x_seed1717_no_test_flag | PASS | `"both result and predictions mark test_opened=false"` |
| outercoord_lite_mlp_ge4x_seed1717_metrics_recomputed | PASS | `{"accuracy": 0.9882352941176471, "macro_precision": 0.9848484848484849, "macro_recall": 0.9905660377358491, "macro_f1": 0.9875457875457876, "balanced_accuracy": 0.99056603773584...` |
| outercoord_lite_mlp_ge4x_seed2029_files | PASS | `"result, predictions and checkpoint exist"` |
| outercoord_lite_mlp_ge4x_seed2029_prediction_integrity | PASS | `"85 validation probabilities, class sums 1, labels match validation"` |
| outercoord_lite_mlp_ge4x_seed2029_hashes | PASS | `{"checkpoint_sha256": "2e6f31e515f96ef35d9724149e2ab5daa9516a16897b14fdcf7b73a161c222f7", "predictions_sha256": "16aa48a869b6c9d010efe6a76fd89656785a32aa00832447683006aa3cc3beb5"}` |
| outercoord_lite_mlp_ge4x_seed2029_no_test_flag | PASS | `"both result and predictions mark test_opened=false"` |
| outercoord_lite_mlp_ge4x_seed2029_metrics_recomputed | PASS | `{"accuracy": 0.9882352941176471, "macro_precision": 0.9848484848484849, "macro_recall": 0.9905660377358491, "macro_f1": 0.9875457875457876, "balanced_accuracy": 0.99056603773584...` |
| outercoord_lite_mlp_ge4x_seed3037_files | PASS | `"result, predictions and checkpoint exist"` |
| outercoord_lite_mlp_ge4x_seed3037_prediction_integrity | PASS | `"85 validation probabilities, class sums 1, labels match validation"` |
| outercoord_lite_mlp_ge4x_seed3037_hashes | PASS | `{"checkpoint_sha256": "22c9081fd98c49d9d45ce752ab348d958a605dc8acd5a845c73021790024a179", "predictions_sha256": "123ff0ea131fa223d0aadc9ce2b5fae6587d8fb0486bf1a86dd48b4d8cd42442"}` |
| outercoord_lite_mlp_ge4x_seed3037_no_test_flag | PASS | `"both result and predictions mark test_opened=false"` |
| outercoord_lite_mlp_ge4x_seed3037_metrics_recomputed | PASS | `{"accuracy": 0.9882352941176471, "macro_precision": 0.9848484848484849, "macro_recall": 0.9905660377358491, "macro_f1": 0.9875457875457876, "balanced_accuracy": 0.99056603773584...` |
| deployment_parity | PASS | `{"status": "PASS", "candidate_checks": [{"seed": 1501, "model": "outercoord_lite_7x1_seed1501", "max_abs_probability_difference": 0.0, "parity_atol_1e-6": true}, {"seed": 1607, ...` |
| historical_reference_hashes | PASS | `{"reference_rows": 10, "issues": []}` |
| LATENCY_PROFILE_DETAILS_V003.json | PASS | `{"profiles": 100, "unique_profiles": 100, "expected": 100, "warmup": 30, "repeats": 200}` |
| LATENCY_PROFILE_RAW_END2END_V003.json | PASS | `{"profiles": 100, "unique_profiles": 100, "expected": 100, "warmup": 30, "repeats": 200}` |
| LATENCY_SAMPLES_V003.csv | PASS | `{"sample_rows": 20000, "expected_rows": 20000}` |
| LATENCY_SAMPLES_RAW_END2END_V003.csv | PASS | `{"sample_rows": 20000, "expected_rows": 20000}` |
| python_sources_compile | PASS | `{"files": 5, "errors": []}` |
| strict_json_files | PASS | `{"files": 77, "errors": []}` |
| parameter_totals | PASS | `{"OuterCoord-Lite-7x1": "1341.0", "MLP-matched": "1349.0", "MLP-ge4x": "5375.0", "OuterCoord-only-7x5": "6712.0", "Recursive-Org-7x5": "6712.0"}` |
| mlp_ge4x_parameter_ratio | PASS | `4.008202833706189` |

## Limites
- No external test data included or opened.
- The 57-row adaptation partition is retained as protocol metadata but unused in V003.
- Five seeds share one historically exposed fixed development split; inferential results are descriptive only.
- Energy was not measured. Isolated cross-model peak memory was not reliably measured.
