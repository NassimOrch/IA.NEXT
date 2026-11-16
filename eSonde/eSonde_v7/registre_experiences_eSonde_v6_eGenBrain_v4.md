# Registre des expériences et artefacts de résultat — eSonde v6 / eGenBrain v4

Ce registre donne une ligne par résultat JSON, trace gzip, journal et tour de laboratoire. Les hashes sont conservés pour retourner à la source exacte. Les résultats absents ou incomplets ne sont pas extrapolés.

## eSonde v6 — résultats JSON

| Fichier | Statut | Parsing | Octets | SHA-256 |
|---|---|---|---:|---|
| `results/EXEC-0001-P2-TRAIN-1M-TIMEOUT.json` | `UNPARSEABLE` | `INVALID_JSON` | 1429 | `347591189a6c7687e86a975d697c64a4d8966760c37480c80e6691aefcbe2b82` |
| `results/bench_seed_vectorization_1m.json` | `None` | `VALID_JSON` | 842 | `85fa24fa2e724c6931d95729d5b494b753edaf9bf317da4343a9d1f58032ea50` |
| `results/cli_status_1m.json` | `PASS` | `VALID_JSON` | 799 | `c1772b25acadb5f2041b5f85458eeafd07fe0ce538e7bd6a69aa0d4f5dd71468` |
| `results/cli_status_1m.stdout.json` | `PASS` | `VALID_JSON` | 799 | `c1772b25acadb5f2041b5f85458eeafd07fe0ce538e7bd6a69aa0d4f5dd71468` |
| `results/cli_verify_1m.json` | `PASS` | `VALID_JSON` | 1104 | `9c6f629478f8c873ce655995e6871213868e441ba0d12aa520ebc8817f17487b` |
| `results/cli_verify_1m.stdout.json` | `PASS` | `VALID_JSON` | 1104 | `9c6f629478f8c873ce655995e6871213868e441ba0d12aa520ebc8817f17487b` |
| `results/dmodel_release_verify.json` | `PASS` | `VALID_JSON` | 1009 | `0da7193d40fe4279cbc0dba71b0f3f5715595927f4c226a781d82e586d9e98d6` |
| `results/fixedpoint_index_bench_100k_P.stdout.json` | `NO_RESULT` | `EMPTY_ZERO_BYTE` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/fixedpoint_tree_index_100k_P.json` | `PASS_TRACE_SHA_AND_INDEX_COMPLETED` | `VALID_JSON` | 971 | `23b04cf8c5d9a80895c1966058b97b85c613bd04e032a4c4e4d681c0bebe9a5b` |
| `results/fixedpoint_tree_index_100k_P.stdout.json` | `PASS_TRACE_SHA_AND_INDEX_COMPLETED` | `VALID_JSON` | 971 | `23b04cf8c5d9a80895c1966058b97b85c613bd04e032a4c4e4d681c0bebe9a5b` |
| `results/fixedpoint_tree_index_100k_P_vectorized.json` | `PASS_TRACE_SHA_AND_INDEX_COMPLETED` | `VALID_JSON` | 971 | `ab7a6a0595c3906825eae7600a274e557d4f8d55af1d629a05c63ea43d70a916` |
| `results/fixedpoint_tree_index_100k_P_vectorized.stdout.json` | `NO_RESULT` | `EMPTY_ZERO_BYTE` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/fixedpoint_tree_index_100k_R.json` | `PASS_TRACE_SHA_AND_INDEX_COMPLETED` | `VALID_JSON` | 971 | `66b561daaef15199602d4bbf36d65e7ac16b68bf7c4dbcebc9c4621c6675d097` |
| `results/fixedpoint_tree_index_100k_R.stdout.json` | `PASS_TRACE_SHA_AND_INDEX_COMPLETED` | `VALID_JSON` | 971 | `66b561daaef15199602d4bbf36d65e7ac16b68bf7c4dbcebc9c4621c6675d097` |
| `results/fixedpoint_tree_index_100k_R_vectorized.json` | `PASS_TRACE_SHA_AND_INDEX_COMPLETED` | `VALID_JSON` | 995 | `6c4de2b8925f885ebf79d00a3d19dff001e71f4777da2d7993311da6f5038066` |
| `results/generation_smoke_en.json` | `GENERATED` | `VALID_JSON` | 16856 | `af5dafb1e05037aae29e89f5c68d8f353d7fc8e849b98afde8145df1f1c6fc2e` |
| `results/generation_smoke_fr.json` | `GENERATED` | `VALID_JSON` | 13879 | `cb238ab1f8fd70886ea8d17e92870d8decb34affff00056e9d9be142068058de` |
| `results/generation_smoke_fr.stdout.json` | `GENERATED` | `VALID_JSON` | 13879 | `cb238ab1f8fd70886ea8d17e92870d8decb34affff00056e9d9be142068058de` |
| `results/generation_smoke_graph.json` | `GENERATED` | `VALID_JSON` | 16843 | `c9b5df73c4d759c0ba3c4c9c88580d5da3d25ac95c67d37173760c2d557d5274` |
| `results/generation_v3_ar.json` | `GENERATED` | `VALID_JSON` | 17811 | `b6fef4c6516ba378343ccafb348be7070be5b91d66c1297d708561e2a88b0e80` |
| `results/generation_v3_ar.stdout.json` | `GENERATED` | `VALID_JSON` | 17811 | `b6fef4c6516ba378343ccafb348be7070be5b91d66c1297d708561e2a88b0e80` |
| `results/generation_v3_en.json` | `GENERATED` | `VALID_JSON` | 18070 | `b987fe9c503f2f089bee759ab372543499d761078afc043e6eada30aab32a160` |
| `results/generation_v3_en.stdout.json` | `GENERATED` | `VALID_JSON` | 18070 | `b987fe9c503f2f089bee759ab372543499d761078afc043e6eada30aab32a160` |
| `results/generation_v3_fr.json` | `GENERATED` | `VALID_JSON` | 18399 | `b7bf363dd8e0a602cbc92307357c1561f2a79c4b2316792e71f840e204a3db5b` |
| `results/generation_v3_fr.stdout.json` | `GENERATED` | `VALID_JSON` | 18399 | `b7bf363dd8e0a602cbc92307357c1561f2a79c4b2316792e71f840e204a3db5b` |
| `results/generation_v3_zh.json` | `GENERATED` | `VALID_JSON` | 19930 | `add9568e8d74d8048d4b44aa5eccfc33e7f1c838e66b78da58d1dd36e87433a7` |
| `results/generation_v3_zh.stdout.json` | `GENERATED` | `VALID_JSON` | 19930 | `add9568e8d74d8048d4b44aa5eccfc33e7f1c838e66b78da58d1dd36e87433a7` |
| `results/generation_v3b_ar.json` | `GENERATED` | `VALID_JSON` | 17810 | `731020d6bfd8a4fcbc8991af8898b80c7d8e114afaf7f3e0f8ba02b3e27c808c` |
| `results/generation_v3b_ar.stdout.json` | `GENERATED` | `VALID_JSON` | 17810 | `731020d6bfd8a4fcbc8991af8898b80c7d8e114afaf7f3e0f8ba02b3e27c808c` |
| `results/generation_v3b_en.json` | `GENERATED` | `VALID_JSON` | 18126 | `9ead40d4834b34cbd8cf41658a7d6f3b23908e776c647bd7632e86bf0557e67c` |
| `results/generation_v3b_en.stdout.json` | `GENERATED` | `VALID_JSON` | 18126 | `9ead40d4834b34cbd8cf41658a7d6f3b23908e776c647bd7632e86bf0557e67c` |
| `results/generation_v3b_fr.json` | `GENERATED` | `VALID_JSON` | 18440 | `c33a2b3f0dcdec3b59ffbfdfe87937e3d055f0fa02fecd4d07e0178bdc7cf9e6` |
| `results/generation_v3b_fr.stdout.json` | `GENERATED` | `VALID_JSON` | 18440 | `c33a2b3f0dcdec3b59ffbfdfe87937e3d055f0fa02fecd4d07e0178bdc7cf9e6` |
| `results/generation_v3b_zh.json` | `GENERATED` | `VALID_JSON` | 19883 | `e62f6126e81a30ea438cfbf33844b9c9f7bba38ccb8bf4ec0b93bf84277903d9` |
| `results/generation_v3b_zh.stdout.json` | `GENERATED` | `VALID_JSON` | 19883 | `e62f6126e81a30ea438cfbf33844b9c9f7bba38ccb8bf4ec0b93bf84277903d9` |
| `results/generation_v4_ar.json` | `GENERATED` | `VALID_JSON` | 17550 | `8c9341ff6b00052bbf1d039ed62e21ae0fed69972c14a90084439390eb548245` |
| `results/generation_v4_ar.stdout.json` | `GENERATED` | `VALID_JSON` | 17550 | `8c9341ff6b00052bbf1d039ed62e21ae0fed69972c14a90084439390eb548245` |
| `results/generation_v4_en.json` | `GENERATED` | `VALID_JSON` | 18153 | `18e37e13043c7131ccbbd0e2abab396a0c03fe0d98e3649db8c090c82943485e` |
| `results/generation_v4_en.stdout.json` | `GENERATED` | `VALID_JSON` | 18153 | `18e37e13043c7131ccbbd0e2abab396a0c03fe0d98e3649db8c090c82943485e` |
| `results/generation_v4_fr.json` | `GENERATED` | `VALID_JSON` | 18339 | `18cf3394ef2b2d1bea90f244b021f859655c7fd0962edf196dcfa7ee5591e8f2` |
| `results/generation_v4_fr.stdout.json` | `GENERATED` | `VALID_JSON` | 18339 | `18cf3394ef2b2d1bea90f244b021f859655c7fd0962edf196dcfa7ee5591e8f2` |
| `results/generation_v4_zh.json` | `GENERATED` | `VALID_JSON` | 19870 | `4f15df2b929af1e78977a91cbeb86242ba21ba72a404ec41ed0778520a4bd62f` |
| `results/generation_v4_zh.stdout.json` | `GENERATED` | `VALID_JSON` | 19870 | `4f15df2b929af1e78977a91cbeb86242ba21ba72a404ec41ed0778520a4bd62f` |
| `results/gui_structure_smoke.json` | `PASS` | `VALID_JSON` | 496 | `2eb1ece34a511071bfc4113ac288c05839fbd25b22647e90d0d494d12aec85b2` |
| `results/model_verify_v4_before_1m.json` | `PASS` | `VALID_JSON` | 1009 | `0da7193d40fe4279cbc0dba71b0f3f5715595927f4c226a781d82e586d9e98d6` |
| `results/model_verify_v4_before_1m.stdout.json` | `PASS` | `VALID_JSON` | 1009 | `0da7193d40fe4279cbc0dba71b0f3f5715595927f4c226a781d82e586d9e98d6` |
| `results/model_verify_v4_before_1m_retry.json` | `PASS` | `VALID_JSON` | 1009 | `0da7193d40fe4279cbc0dba71b0f3f5715595927f4c226a781d82e586d9e98d6` |
| `results/model_verify_v4_before_1m_retry.stdout.json` | `PASS` | `VALID_JSON` | 1009 | `0da7193d40fe4279cbc0dba71b0f3f5715595927f4c226a781d82e586d9e98d6` |
| `results/native_query_pairs_100k_P.json` | `PASS_TRACE_SHA_AND_INDEX_COMPLETED` | `VALID_JSON` | 1312 | `186fe343011048812bcb1d3653308be821dde3f85be006efd71a4d986777444d` |
| `results/native_query_pairs_100k_P.stdout.json` | `PASS_TRACE_SHA_AND_INDEX_COMPLETED` | `VALID_JSON` | 1312 | `186fe343011048812bcb1d3653308be821dde3f85be006efd71a4d986777444d` |
| `results/native_query_pairs_100k_R.json` | `PASS_TRACE_SHA_AND_INDEX_COMPLETED` | `VALID_JSON` | 1312 | `9a3a155362b365a8086f4c0b0a7ffee9086696b82835e7ce734fa32e2d04a1f6` |
| `results/native_query_pairs_100k_R.stdout.json` | `PASS_TRACE_SHA_AND_INDEX_COMPLETED` | `VALID_JSON` | 1312 | `9a3a155362b365a8086f4c0b0a7ffee9086696b82835e7ce734fa32e2d04a1f6` |
| `results/observe_1m.stdout.json` | `NO_RESULT` | `EMPTY_ZERO_BYTE` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/observe_1m_encoding_abort.json` | `ABORTED_INPUT_ENCODING_INVALID` | `VALID_JSON` | 965 | `96da6bbb622649f52ea394000c0a515eca4af2e6b0398837f2793dbda910669e` |
| `results/observe_1m_interrupted.json` | `INTERRUPTED_FOR_IMPLEMENTATION_OPTIMIZATION` | `VALID_JSON` | 1359 | `65420340c53d10d990c696c276983e44ba1818fe724428da54821b812befb630` |
| `results/observe_full_1m.stdout.json` | `NO_RESULT` | `EMPTY_ZERO_BYTE` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/observe_pair_100k.json` | `OBSERVED` | `VALID_JSON` | 7497 | `ae5d4b8f7ab57c1409d4c7d0c47e7106d6503c79e5078bdbd6da922cab3c8c9a` |
| `results/observe_pair_100k.stdout.json` | `OBSERVED` | `VALID_JSON` | 7497 | `ae5d4b8f7ab57c1409d4c7d0c47e7106d6503c79e5078bdbd6da922cab3c8c9a` |
| `results/observe_pair_10k.json` | `OBSERVED` | `VALID_JSON` | 7324 | `f0bec0e717c92af6374989a48e1e130519491b7c9af15a9910035adadd1eeecc` |
| `results/observe_pair_10k.stdout.json` | `OBSERVED` | `VALID_JSON` | 7324 | `f0bec0e717c92af6374989a48e1e130519491b7c9af15a9910035adadd1eeecc` |
| `results/observe_pair_1k.json` | `OBSERVED` | `VALID_JSON` | 7224 | `a28c2de954bcdcfcf9950a9d58577e472da5e336e0d8079a02fdb376bb6ea3f5` |
| `results/observe_pair_1k.stdout.json` | `OBSERVED` | `VALID_JSON` | 7224 | `a28c2de954bcdcfcf9950a9d58577e472da5e336e0d8079a02fdb376bb6ea3f5` |
| `results/observe_pair_1m_exact128_interrupted.json` | `INCOMPLETE` | `VALID_JSON` | 1206 | `dd124a535195e1a8772f165accbe53a6e839710d83e4bcbe0660d7cfe1ff271f` |
| `results/observe_pair_1m_multidim_exact.stdout.json` | `NO_RESULT` | `EMPTY_ZERO_BYTE` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/observe_pair_1m_multidim_exact_incomplete.json` | `INCOMPLETE_STOPPED_FOR_VECTORIZED_FIXEDPOINT_QUANTIZATION` | `VALID_JSON` | 1851 | `26fd0d649958898fb5a72d4c5f1c5fed5f1fef15a9967822b179a503fb580ab3` |
| `results/observe_pair_1m_native_query_pairs.launch.json` | `RUNNING` | `VALID_JSON` | 289 | `984d771b50adbaed43eebc90e03dbd84ad2a70db882cd3fd70777bbe08a471f6` |
| `results/observe_pair_1m_native_query_pairs.stdout.json` | `NO_RESULT` | `EMPTY_ZERO_BYTE` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/observe_pair_1m_parallel_radius_interrupted.json` | `INCOMPLETE_STOPPED_FOR_INDEX_REDESIGN` | `VALID_JSON` | 1694 | `9d8e03e2ec04d34eed8707aad9a52cc16ff6bef3517bfed1104f65e7d2b3de5f` |
| `results/observe_pair_1m_roundeven.stdout.json` | `NO_RESULT` | `EMPTY_ZERO_BYTE` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/observe_pair_1m_roundeven_incomplete.json` | `INCOMPLETE` | `VALID_JSON` | 823 | `cf6a41613b995139172a4dea9f3008bbd379cce38dee5914c4b87e0070331284` |
| `results/observe_pair_1m_scalar_interrupted.json` | `INCOMPLETE` | `VALID_JSON` | 1306 | `02646aa0118e552c2ab25be68667dfbf44abffe73722d604941dc73055bcfab2` |
| `results/partition_benchmark_1m.json` | `PASS` | `VALID_JSON` | 588 | `e6c672ddb8dcd344e3a07f9485be7915e5e3deb356a44bd6f2714909b836623c` |
| `results/preflight_after_v3b_train.json` | `PASS` | `VALID_JSON` | 716 | `0c01b3eea1cf1d307a5a3acdcfc9d15d0b1ee7086e8478f43a1d6b76eb03a8be` |
| `results/preflight_after_v4_train.json` | `PASS` | `VALID_JSON` | 707 | `6c01e719bdf5cacfc3e94e52d631ccbf7cc711ab1662e8085ce37ec027648c2f` |
| `results/preflight_before_100k_index_bench.json` | `PASS` | `VALID_JSON` | 706 | `6c3cb184d479134b75a4ca247b22a0900f66e51783b5b84895404737608af1ef` |
| `results/preflight_before_exact_fixedpoint_tests.json` | `PASS` | `VALID_JSON` | 696 | `605bfb64d4c3c743677b5e4372be5d92b2845be3f13c0ef35e3335a47af3b0ef` |
| `results/preflight_before_exact_fixedpoint_tests_xvfb.json` | `PASS` | `VALID_JSON` | 696 | `dc430c801d0114d42d37ee5e8dc71a06a972b6ee670f085127675a32904a7dc4` |
| `results/preflight_before_final_savepoint.json` | `PASS` | `VALID_JSON` | 701 | `4b2ad65bdde5f54a63541076215ba2f56ab72af87febc1cff2ee6ad59cff71aa` |
| `results/preflight_before_fixedpoint_fulltests.json` | `PASS` | `VALID_JSON` | 696 | `dc430c801d0114d42d37ee5e8dc71a06a972b6ee670f085127675a32904a7dc4` |
| `results/preflight_before_generation_v3.json` | `PASS` | `VALID_JSON` | 718 | `abe8a27880ba0e9c81fbea505f51ee56bfb715461ff1b7a811a2c46321286962` |
| `results/preflight_before_generation_v3b.json` | `PASS` | `VALID_JSON` | 711 | `9017c35814eab03f8ab40a55d2363990c1bf250feef2333eebf1ca5239746589` |
| `results/preflight_before_native_query_pairs_1m.json` | `PASS` | `VALID_JSON` | 701 | `4b2ad65bdde5f54a63541076215ba2f56ab72af87febc1cff2ee6ad59cff71aa` |
| `results/preflight_before_observe_pair_1m_parallel.json` | `PASS` | `VALID_JSON` | 696 | `4041baeaaab74321981e0b6d830d8b296d34f0a4ba1237bd5df8d4f4668c9573` |
| `results/preflight_before_savepoint_029.json` | `PASS` | `VALID_JSON` | 696 | `dc430c801d0114d42d37ee5e8dc71a06a972b6ee670f085127675a32904a7dc4` |
| `results/preflight_before_savepoint_030.json` | `PASS` | `VALID_JSON` | 706 | `ede77bebd29441dc2ceac35b4f73a1cbefa1071907593404b4f0bfb0e602a536` |
| `results/preflight_before_savepoint_031.json` | `PASS` | `VALID_JSON` | 712 | `3ab561db4010cfe9347d4d685973834dd056fcfc2ab07e150bb357d95afbc00a` |
| `results/preflight_before_tex_fixedpoint.json` | `PASS` | `VALID_JSON` | 696 | `dc430c801d0114d42d37ee5e8dc71a06a972b6ee670f085127675a32904a7dc4` |
| `results/preflight_before_tex_fixedpoint_pass2.json` | `PASS` | `VALID_JSON` | 696 | `dc430c801d0114d42d37ee5e8dc71a06a972b6ee670f085127675a32904a7dc4` |
| `results/preflight_before_v3_train.json` | `PASS` | `VALID_JSON` | 714 | `e8d02a063a7a01b614d4fa967fde24f928684a85e89e930e0b4e119548feeaed` |
| `results/preflight_before_v3_train_retry.json` | `PASS` | `VALID_JSON` | 694 | `4792e76e91172b6c9769ea6b90f3e932231bc2d005fdf70e9a4672365b508c6d` |
| `results/preflight_before_v3b_train.json` | `PASS` | `VALID_JSON` | 706 | `bc209dfbaa70648aff73e14d2a6dcd2b128271c493ade5960c9b274684c321aa` |
| `results/preflight_before_v4_train.json` | `PASS` | `VALID_JSON` | 728 | `933321f8e324597c15cf38ea99f01843faea0c9e8a46d3ebfb864645b14b8f7d` |
| `results/preflight_pass1.json` | `PASS` | `VALID_JSON` | 695 | `18a143d141e7d0330d01d130367c366987cb46cfae39d2475fd818aca8651621` |
| `results/preflight_post_training.json` | `PASS` | `VALID_JSON` | 685 | `3bd152f5efef63110ae2578d791062620a4a77541c9a28bc8cf8f48e9141b8b9` |
| `results/preflight_pretraining.json` | `PASS` | `VALID_JSON` | 684 | `45e2175343056a1a9ac66396264f68dbc042ff9aa7f42ec98e2f3bfab6206e2d` |
| `results/savepoint_011.json` | `SAVEPOINT_CREATED` | `VALID_JSON` | 1172 | `1351df4b44615c2411176ac33fa1468dd5f3cb5eea4c5bea17b06eb4f9a21074` |
| `results/savepoint_012.json` | `NO_RESULT` | `EMPTY_ZERO_BYTE` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/savepoint_013.json` | `SAVEPOINT_CREATED` | `VALID_JSON` | 1176 | `a7cb4442c4d041ce685fe67d861ee1f16d49a4562b39cf7d7be63be2d2abfbad` |
| `results/savepoint_014.json` | `SAVEPOINT_CREATED` | `VALID_JSON` | 1162 | `30c731b738d0d9d9059fa358720fcfbdda605077197c360978ef358d6dbcde0f` |
| `results/savepoint_015.json` | `SAVEPOINT_CREATED` | `VALID_JSON` | 1166 | `06ddef599872b91de7e6fba54c37b596ca0abc1c63e6c206dc3d3833fc7460e8` |
| `results/savepoint_017.json` | `SAVEPOINT_CREATED` | `VALID_JSON` | 1221 | `1f67481a07c2fcd2027997f7e203cc07a1bd3723785601e861ffdd64abdb2e20` |
| `results/savepoint_018.json` | `SAVEPOINT_CREATED` | `VALID_JSON` | 1179 | `cbc99a446fd4f4a9d7155f1a6dc157610998fec81f586b5d7b7b4e06a41a4a8e` |
| `results/savepoint_019.json` | `SAVEPOINT_CREATED` | `VALID_JSON` | 1203 | `ccf6e794720628be34eb5562df3b7cb7ffee53645f2fccaff72b19f3ef3aae5a` |
| `results/savepoint_020.json` | `SAVEPOINT_CREATED` | `VALID_JSON` | 1223 | `5f2e2754879dd9ad996898cf7d0ead59f9572d98d79336bdee6511edb7201808` |
| `results/savepoint_021.json` | `SAVEPOINT_CREATED` | `VALID_JSON` | 1227 | `a687bee3015dd95962b8e7c95992bc824b4e6abb173d2fcbc88e45ed7639b3f8` |
| `results/savepoint_022.json` | `SAVEPOINT_CREATED` | `VALID_JSON` | 1213 | `262212ac377fd4f949a43b4f8157a7dff3727210826ee3c25b63f103de7ae44a` |
| `results/savepoint_023.json` | `SAVEPOINT_CREATED` | `VALID_JSON` | 1247 | `a7a2edb21e9858c9580541f8de654295ed404fd88f2f612488ffeb9b07541517` |
| `results/savepoint_024.json` | `SAVEPOINT_CREATED` | `VALID_JSON` | 1205 | `84951af4e422be7b3fd4cd65cc0247a805d4fa21b51d45aa70ccbff21c9c24f4` |
| `results/savepoint_027.stdout.json` | `SAVEPOINT_CREATED` | `VALID_JSON` | 1190 | `de0029442eef550e94e7b5b6ac04c6eeb0ff93e22c77e2be8a88b3d64d923e15` |
| `results/savepoint_029.json` | `SAVEPOINT_CREATED` | `VALID_JSON` | 1202 | `f53469ec718ab2a5ee617dd8fb3a680ca6ba871be46259cc92c2359b04416d53` |
| `results/savepoint_030.json` | `SAVEPOINT_CREATED` | `VALID_JSON` | 1214 | `4a3230ed42727da82e442e2dc1f1cf6e3181c8a5f1e5bf28d71abc3224fbb1f1` |
| `results/savepoint_031.json` | `SAVEPOINT_CREATED` | `VALID_JSON` | 1202 | `af649a67118d9fab599f909e92159c6fc950d7a9aadbe9fa8b31087eeee33336` |
| `results/savepoint_final_creation.json` | `NO_RESULT` | `EMPTY_ZERO_BYTE` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/savepoint_post_training.json` | `SAVEPOINT_CREATED` | `VALID_JSON` | 1138 | `896ac4f9a27994b603488e45b29069bf462843c376b1ca6132a77846867976fa` |
| `results/savepoint_pretraining.json` | `SAVEPOINT_CREATED` | `VALID_JSON` | 1137 | `117243e83983ec47089e59a01132de40e4fb7d0584eda9ff656ffc5a3baf6584` |
| `results/savepoint_verify_011.json` | `PASS` | `VALID_JSON` | 413 | `6c965a2c73d864156672d838d7f4a77dd7d4b4798b936f21eacaaffa08d553d0` |
| `results/savepoint_verify_013.json` | `PASS` | `VALID_JSON` | 413 | `b6ae5c0e6656f4641ab777f64e718146463ad5c5956b0094bfafeba6502c6afb` |
| `results/savepoint_verify_014.json` | `PASS` | `VALID_JSON` | 413 | `5f611bb1a15d80db9c7eae5b69a9e416125359a35d4a6270ca976fc481ce6fc7` |
| `results/savepoint_verify_015.json` | `PASS` | `VALID_JSON` | 413 | `9188acea8a429b3b8b274624a07f291da8361093098f38771a40bb9f23d1474e` |
| `results/savepoint_verify_029.json` | `PASS` | `VALID_JSON` | 413 | `dc5b5b1dbd8f93f53e8ed2feb25d80c4f1cc8908976c01e733f335df93c70521` |
| `results/savepoint_verify_030.json` | `PASS` | `VALID_JSON` | 413 | `f0fbd740b9ca948fda9d1acc431c0704747f4fc7dd930f79ecc8bcabd8d2928d` |
| `results/savepoint_verify_031.json` | `PASS` | `VALID_JSON` | 413 | `7a230b08e4ec2cf565da8942d6cc4120c0595d0828247bbc95a11f4a144b63c0` |
| `results/savepoint_verify_before_final_savepoint.json` | `PASS` | `VALID_JSON` | 413 | `62228775f26605fc2b7602dd613be5b19749fb7091f7167d0361a7217090c77e` |
| `results/savepoint_verify_before_observe_100k.json` | `PASS` | `VALID_JSON` | 413 | `9188acea8a429b3b8b274624a07f291da8361093098f38771a40bb9f23d1474e` |
| `results/savepoint_verify_before_observe_10k.json` | `PASS` | `VALID_JSON` | 413 | `5f611bb1a15d80db9c7eae5b69a9e416125359a35d4a6270ca976fc481ce6fc7` |
| `results/savepoint_verify_before_observe_1k.json` | `PASS` | `VALID_JSON` | 413 | `b6ae5c0e6656f4641ab777f64e718146463ad5c5956b0094bfafeba6502c6afb` |
| `results/savepoint_verify_before_tests.json` | `PASS` | `VALID_JSON` | 413 | `89b1c2a9953fa3b139ec76fabc60db5f932671784ba8c53c0f26b51538b99fe5` |
| `results/savepoint_verify_post_training.json` | `PASS` | `VALID_JSON` | 413 | `3583a6ffd81557f87ffcb4b03fcffa8f82c54d8bc5bf759de0619916525c130a` |
| `results/savepoint_verify_pre_fixedpoint.json` | `PASS` | `VALID_JSON` | 413 | `dd4151e29265ceaeaac099a1301b7d771cabc8ae2f7b1e0cbed6609875b2b75a` |
| `results/savepoint_verify_pretraining.json` | `PASS` | `VALID_JSON` | 413 | `a5add0c84ca15f134d8d3f58414eea4b2f0dcbe9d4a4c42331884baca3ba94dd` |
| `results/single_coordinate_index_candidate_explosion_100k.json` | `None` | `VALID_JSON` | 902 | `0faa1da718ac3988b8ee2332cae8d1c5150d168f7417c0f336b105e7b715ad1d` |
| `results/train_1m.json` | `TRAINED` | `VALID_JSON` | 7686 | `01aee9153928c1ffcf30f0a8e64e54030e699e81b0bff35119405d54a7b75c46` |
| `results/train_1m.stdout.json` | `TRAINED` | `VALID_JSON` | 7686 | `01aee9153928c1ffcf30f0a8e64e54030e699e81b0bff35119405d54a7b75c46` |
| `results/train_full_1m.stdout.json` | `NO_RESULT` | `EMPTY_ZERO_BYTE` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/train_repro_full_1m.json` | `TRAINED` | `VALID_JSON` | 7436 | `1d6c87287d425367cc63ec8c25e41362850390125539bbb42a1ebff9f1c553bb` |
| `results/train_reproducibility_check.json` | `None` | `VALID_JSON` | 870 | `3169fbe69a9ddc2d0154802b47fe55cbd83fb238e0057d7ab8a740d19be70b62` |
| `results/train_v3_1m.json` | `TRAINED` | `VALID_JSON` | 6535 | `b0864665d546162ef586de81870047d9f45fbc53fabcdd5213d12fca7cd341ba` |
| `results/train_v3_1m.stdout.json` | `TRAINED` | `VALID_JSON` | 6535 | `b0864665d546162ef586de81870047d9f45fbc53fabcdd5213d12fca7cd341ba` |
| `results/train_v3_1m_with_v5examples.json` | `TRAINED` | `VALID_JSON` | 7717 | `f943107cabc791f12060f0bdea3e80fb88b1e33b2936b96393f79cf8462a76eb` |
| `results/train_v3_1m_with_v5examples.stdout.json` | `TRAINED` | `VALID_JSON` | 7717 | `f943107cabc791f12060f0bdea3e80fb88b1e33b2936b96393f79cf8462a76eb` |
| `results/train_v4_1m_no_sms.json` | `TRAINED` | `VALID_JSON` | 8242 | `c6472ab5721b41f6adf3321d53c39a4910bdc4fab8679223009f5a3bab820ba4` |
| `results/train_v4_1m_no_sms.stdout.json` | `TRAINED` | `VALID_JSON` | 8242 | `c6472ab5721b41f6adf3321d53c39a4910bdc4fab8679223009f5a3bab820ba4` |
| `results/verify_1m.json` | `PASS` | `VALID_JSON` | 1101 | `8f0553046b22aa7c8e1f1a6420685d8378c2894a80066a7fd2e6e0b470538d21` |
| `results/verify_1m.stdout.json` | `PASS` | `VALID_JSON` | 1101 | `8f0553046b22aa7c8e1f1a6420685d8378c2894a80066a7fd2e6e0b470538d21` |
| `results/verify_v3_1m.json` | `PASS` | `VALID_JSON` | 1130 | `9caeaf0fb0535eec951f806db262edb5cd74107702071679f4dc5b45844284c7` |
| `results/verify_v3_1m.stdout.json` | `PASS` | `VALID_JSON` | 1130 | `9caeaf0fb0535eec951f806db262edb5cd74107702071679f4dc5b45844284c7` |
| `results/verify_v4_1m.json` | `PASS` | `VALID_JSON` | 1121 | `39020abb4284130766a106f67f5afa8a014e745f5bc8191b0aa8f1faedc69fa4` |
| `results/verify_v4_1m.stdout.json` | `PASS` | `VALID_JSON` | 1121 | `39020abb4284130766a106f67f5afa8a014e745f5bc8191b0aa8f1faedc69fa4` |
| `results/verify_v4_post_native_index.json` | `PASS` | `VALID_JSON` | 1009 | `0da7193d40fe4279cbc0dba71b0f3f5715595927f4c226a781d82e586d9e98d6` |
| `results/verify_v4_post_native_index.stdout.json` | `PASS` | `VALID_JSON` | 1009 | `0da7193d40fe4279cbc0dba71b0f3f5715595927f4c226a781d82e586d9e98d6` |
| `results/zero_neuron_audit.stdout.json` | `PASS` | `VALID_JSON` | 732 | `327c1e6a11442ed15d3a2411f361ede3e71285152e35630ca42e5e9f3e48388d` |
| `results/zero_neuron_audit_after_fixes.json` | `PASS` | `VALID_JSON` | 732 | `327c1e6a11442ed15d3a2411f361ede3e71285152e35630ca42e5e9f3e48388d` |
| `results/zero_neuron_audit_after_multidim.stdout.json` | `PASS` | `VALID_JSON` | 732 | `327c1e6a11442ed15d3a2411f361ede3e71285152e35630ca42e5e9f3e48388d` |
| `results/zero_neuron_audit_after_multidim_final.stdout.json` | `PASS` | `VALID_JSON` | 732 | `327c1e6a11442ed15d3a2411f361ede3e71285152e35630ca42e5e9f3e48388d` |
| `results/zero_neuron_audit_current.json` | `PASS` | `VALID_JSON` | 732 | `327c1e6a11442ed15d3a2411f361ede3e71285152e35630ca42e5e9f3e48388d` |
| `results/zero_neuron_audit_current_retest.json` | `PASS` | `VALID_JSON` | 732 | `327c1e6a11442ed15d3a2411f361ede3e71285152e35630ca42e5e9f3e48388d` |
| `results/zero_neuron_audit_final.json` | `PASS` | `VALID_JSON` | 732 | `327c1e6a11442ed15d3a2411f361ede3e71285152e35630ca42e5e9f3e48388d` |
| `results/zero_neuron_audit_final_candidate.json` | `PASS` | `VALID_JSON` | 732 | `327c1e6a11442ed15d3a2411f361ede3e71285152e35630ca42e5e9f3e48388d` |
| `results/zero_neuron_audit_pretrain.stdout.json` | `PASS` | `VALID_JSON` | 732 | `327c1e6a11442ed15d3a2411f361ede3e71285152e35630ca42e5e9f3e48388d` |

## eSonde v6 — traces de trajectoire gzip

| Trace | Statut gzip | Enregistrements JSONL | Octets | SHA-256 |
|---|---|---:|---:|---|
| `runs/generation_smoke_en/traces/P_bdbdd23fe90424780fbe.trajectory.jsonl.gz` | `PASS` | 16 | 41001 | `b42d496aa7bdbe8eda875675c1f721bd9f2102e3a769a92bf319b2c5c24cbba4` |
| `runs/generation_smoke_en/traces/R_2bc84d93e7179a56597b.trajectory.jsonl.gz` | `PASS` | 16 | 69306 | `b8fe67043df648e8f4b445dca23712a472ef17248fcd5e1060336f096e3772f5` |
| `runs/generation_smoke_en/traces/R_5ab554300592257e6259.trajectory.jsonl.gz` | `PASS` | 16 | 58553 | `27b3269808575e830921fae9ce4a6841e463f1f4e0d2f351841a581f21ea154f` |
| `runs/generation_smoke_en/traces/R_9310eeb061d8869dc413.trajectory.jsonl.gz` | `PASS` | 16 | 65381 | `5c18b1a6491a958867185f80ecd87d98a0819b4fad7f4cfafebda15b852cfa4b` |
| `runs/generation_smoke_fr/traces/P_d40dfa576786cc79d874.trajectory.jsonl.gz` | `PASS` | 16 | 64518 | `de77ac650ffa65241504a23f01332dd0a73cc7020b65e94c74ccc49d1a2fc4eb` |
| `runs/generation_smoke_fr/traces/R_328f633bb324781d57dd.trajectory.jsonl.gz` | `PASS` | 16 | 120286 | `4d9fc49eb5f9783100d55791499d5c8adf20b63217c2bc5ea4a3021a7708ff83` |
| `runs/generation_smoke_fr/traces/R_672da798833818e9ebe4.trajectory.jsonl.gz` | `PASS` | 16 | 119291 | `e9b0ce6eefa6f8285052ab381ba8c9329cd1f0bdad19b309f44925ab136b468f` |
| `runs/generation_smoke_graph/traces/P_d2dff11e47a1b6513742.trajectory.jsonl.gz` | `PASS` | 16 | 38810 | `8d42408a11e38950b1c6db1cd721e5899c91cc2648544fe7dbacbb74f2bfeaed` |
| `runs/generation_smoke_graph/traces/R_21eee1e303f9ea95f9b8.trajectory.jsonl.gz` | `PASS` | 16 | 60399 | `a9cbc6ae6e5015c8494af458a6c6a1fc56bf5d1ee4ce9f0c8dff56257ccb8f13` |
| `runs/generation_smoke_graph/traces/R_5955e802f77e737c00a1.trajectory.jsonl.gz` | `PASS` | 16 | 59693 | `b3f2cda58dcfd8a689875a9f847062a9944fb14ed61ce5aacbd5edd0fe116ef6` |
| `runs/generation_smoke_graph/traces/R_66d815697c0e79bfbc24.trajectory.jsonl.gz` | `PASS` | 16 | 59196 | `260a1a33e736bbefb609fd3039773634fd0093488bb08caca22b019fdaa2c274` |
| `runs/generation_v3_ar/traces/P_559058c48f68631295a6.trajectory.jsonl.gz` | `PASS` | 16 | 77622 | `17801b14903012f45e724799501d98fb8d1691d98c94367211f0c5500cc0703d` |
| `runs/generation_v3_ar/traces/R_095b20690e09e8a3410c.trajectory.jsonl.gz` | `PASS` | 16 | 127776 | `6215986e08e8b3baa2a80c5c54f8289cfc4d688d0bf44c2949288aad5ae11663` |
| `runs/generation_v3_ar/traces/R_4a6f5244b8c3ca091795.trajectory.jsonl.gz` | `PASS` | 16 | 126126 | `98da384208b46bed825b70524de7dc87f21ffafd2b43136813af912311229010` |
| `runs/generation_v3_ar/traces/R_85c12200119c2d6d08e2.trajectory.jsonl.gz` | `PASS` | 16 | 126341 | `af3e5619843c2e09460aa96e3d1b7cbaceebd3c5472879eff81b9327059fb549` |
| `runs/generation_v3_en/traces/P_641494b9421a58044230.trajectory.jsonl.gz` | `PASS` | 16 | 76816 | `24e3423c437f22813c3c4ce3c1b4e73c132b20bfd9863ceb43932cbd3dddee3b` |
| `runs/generation_v3_en/traces/R_2c1d12c86692c4a5506f.trajectory.jsonl.gz` | `PASS` | 16 | 121882 | `2d7f3ba61a1eca091e814323adf818d624a785dd24c46a807e85fbfbb62ef211` |
| `runs/generation_v3_en/traces/R_96eb986091f2c1534011.trajectory.jsonl.gz` | `PASS` | 16 | 121371 | `87768bffcb85d90b27f7e444e8f8014372a4081546d98e6bcc0db6fddba1d7a9` |
| `runs/generation_v3_en/traces/R_dc98f25184e1ac5ecdb8.trajectory.jsonl.gz` | `PASS` | 16 | 121021 | `8631749554a3079d30991d66be853ae98c2092e8a0510c54a7436de718fa1e0f` |
| `runs/generation_v3_fr/traces/P_57ddfdec31883585a865.trajectory.jsonl.gz` | `PASS` | 16 | 58920 | `20ca51a1f6b38505a10fdda94ac730c0af7dd34bbb48d641e5f291daaa8106f4` |
| `runs/generation_v3_fr/traces/R_643724af594cc98688bb.trajectory.jsonl.gz` | `PASS` | 16 | 111160 | `9027d63d376c592f9eff10a2373797bd262a64e05e00e7dacab7d30f88535ca0` |
| `runs/generation_v3_fr/traces/R_7678ba99fdb787f9ca00.trajectory.jsonl.gz` | `PASS` | 16 | 124841 | `a172c2b85038ec1dbd476441d3b5d1f9a6ab026ddf462b43265602183b390a24` |
| `runs/generation_v3_fr/traces/R_f0ea8a9457c7f7b6d8f8.trajectory.jsonl.gz` | `PASS` | 16 | 124376 | `f47ddb267cc9b960b9977f81af57ee65c230b736723b110dce0a657d9e472c06` |
| `runs/generation_v3_zh/traces/P_9fd765855ed8cc705a83.trajectory.jsonl.gz` | `PASS` | 16 | 71587 | `4d5983c52c68f9777dc8f017ca7bc2462f6ed5c638a19541342bd74c9c83d269` |
| `runs/generation_v3_zh/traces/R_b449fb8a05a61fcf32a6.trajectory.jsonl.gz` | `PASS` | 16 | 113438 | `5c6515e1e907768714478893147afa235d14c6f79ce0abc44569fe5f9f956a97` |
| `runs/generation_v3_zh/traces/R_ed2ddb8fd7e9243397f8.trajectory.jsonl.gz` | `PASS` | 16 | 110607 | `bcab92eea06a896657d027589594f404368fe037ed883b29b791668fc154ba21` |
| `runs/generation_v3_zh/traces/R_f777079f3cbd6d99eea5.trajectory.jsonl.gz` | `PASS` | 16 | 111206 | `db5d430416c312fdd46814694d42878efffea424901be18c2f24c9289fbfb33a` |
| `runs/generation_v3b_ar/traces/P_559058c48f68631295a6.trajectory.jsonl.gz` | `PASS` | 16 | 77622 | `35432f0d81c3ff88b36f0d5b017bc91e0625da2a273ab446b9e0b89df7da8b3f` |
| `runs/generation_v3b_ar/traces/R_4a6f5244b8c3ca091795.trajectory.jsonl.gz` | `PASS` | 16 | 126126 | `dc8709e0a8fad9e7245123ed8f691d55a241a56c14c861cdc6e5c7a368ce7f22` |
| `runs/generation_v3b_ar/traces/R_85c12200119c2d6d08e2.trajectory.jsonl.gz` | `PASS` | 16 | 126341 | `1f65c82d311e8cdcad9b2ad69e92506f38fbd8a5563738ea8e81810f34ca7049` |
| `runs/generation_v3b_ar/traces/R_93060cdb2f1802be897c.trajectory.jsonl.gz` | `PASS` | 16 | 121773 | `2a665338e3b977a497994e379519759939753da053aac37c61d678f20250a17d` |
| `runs/generation_v3b_en/traces/P_641494b9421a58044230.trajectory.jsonl.gz` | `PASS` | 16 | 76816 | `41b2198bde707e8a84b109c052ea2cfa53635d2db9b703887350179cb2d3d790` |
| `runs/generation_v3b_en/traces/R_c5b076d1cc94694b1030.trajectory.jsonl.gz` | `PASS` | 16 | 122948 | `1c49f1a2c9d8dc8d3e23a89ba8b8d57a44e45d06662d6f46b138d2d7d88d31fc` |
| `runs/generation_v3b_en/traces/R_e1a60e432ecd32d33245.trajectory.jsonl.gz` | `PASS` | 16 | 115002 | `fbb0e73f0543396f3b90a22cfe304b625dcd6b5df9776f34278d837f2b0b0189` |
| `runs/generation_v3b_en/traces/R_e67fe4e9dd2e5bf9a94a.trajectory.jsonl.gz` | `PASS` | 16 | 104454 | `e187a672a7554f86af445d4f16bc83544e5a0f760cb80244e33daa339615b7de` |
| `runs/generation_v3b_fr/traces/P_57ddfdec31883585a865.trajectory.jsonl.gz` | `PASS` | 16 | 58920 | `868931ae224fa2621f5c17e698978f99c3cb17be3bec85af70f5ccaa2a45500a` |
| `runs/generation_v3b_fr/traces/R_0b38c3a297b4f6a37be9.trajectory.jsonl.gz` | `PASS` | 16 | 120395 | `f658d701b3cbce1547b3797c39dc7cabdf968becfa901501bb5be448e556c394` |
| `runs/generation_v3b_fr/traces/R_7042232904e28de0dd58.trajectory.jsonl.gz` | `PASS` | 16 | 127433 | `c1bac0615462fb5bd3743fa68a0c8c61ff4546a8283c1c192b1208d1b74e8479` |
| `runs/generation_v3b_fr/traces/R_e037fb6f68e8e1d99ca0.trajectory.jsonl.gz` | `PASS` | 16 | 126499 | `85a5afe8b1967caf2926652b48a33c2be771329684ed6e14af71a895c77ff48b` |
| `runs/generation_v3b_zh/traces/P_9fd765855ed8cc705a83.trajectory.jsonl.gz` | `PASS` | 16 | 71587 | `ce8417a261a368704dd674aacaea8ac8d053b64b5fd69285d8b33e85e38d3d7a` |
| `runs/generation_v3b_zh/traces/R_86f0163d085ec96b2f35.trajectory.jsonl.gz` | `PASS` | 16 | 111206 | `be0b04ed3321a3def252ec6d7d893f6f2d080c1680fc74341457502042103144` |
| `runs/generation_v3b_zh/traces/R_baade54907802e043b10.trajectory.jsonl.gz` | `PASS` | 16 | 113438 | `a7c065cb366f78dff37e07536af0076bd1026001aa8eb66f66f678cd3304018c` |
| `runs/generation_v3b_zh/traces/R_cb4e2be9de98fe34f47e.trajectory.jsonl.gz` | `PASS` | 16 | 110607 | `256cc2ee817c158431729d506ad9191e33ad81a031dadb3dcec0df104259da2a` |
| `runs/generation_v4_ar/traces/P_559058c48f68631295a6.trajectory.jsonl.gz` | `PASS` | 16 | 79025 | `889ef4b2829eaf3bee186e1dc94b73fe11343d2daf46b425f2613cf64d2a4246` |
| `runs/generation_v4_ar/traces/R_65897079cacd6ea38a19.trajectory.jsonl.gz` | `PASS` | 16 | 119415 | `24e448f0d97d9ad98a2711acc2075e9867693a700b41a48314007dfaf4d6e9ae` |
| `runs/generation_v4_ar/traces/R_a7f7271058a247e9e52d.trajectory.jsonl.gz` | `PASS` | 16 | 123552 | `c4123a74764c01f1d2a5e4c96b1e2f6cb00db2b4a4c3b81a8154b490295e96a7` |
| `runs/generation_v4_ar/traces/R_e991ceae0826cb164951.trajectory.jsonl.gz` | `PASS` | 16 | 120939 | `09e6cbe4d085cf81b6a317a296f8a76e63623c03887ac1f95b19ed172e9ba670` |
| `runs/generation_v4_en/traces/P_641494b9421a58044230.trajectory.jsonl.gz` | `PASS` | 16 | 78411 | `c636df811f92aba9430e8ac595b2a5403996e3a3129633209977085cbb2edfa5` |
| `runs/generation_v4_en/traces/R_05e9f88e78eeb6f7767f.trajectory.jsonl.gz` | `PASS` | 16 | 119742 | `62a44a689db615a0cec55cf61ce4eecee4727922444b1aad9a58ec461f294737` |
| `runs/generation_v4_en/traces/R_6288e05d1c6b4bdaa989.trajectory.jsonl.gz` | `PASS` | 16 | 125374 | `9b2ef4693101e0f2c62d96b3b4862574ee99cc6c60c1edc58e45675ab0659721` |
| `runs/generation_v4_en/traces/R_c1d8a4fce828063eb19a.trajectory.jsonl.gz` | `PASS` | 16 | 123341 | `5e8c27fe26d055c87f0c837d445cd11ccaabbca03aaace3abf98ac03131ca07e` |
| `runs/generation_v4_fr/traces/P_57ddfdec31883585a865.trajectory.jsonl.gz` | `PASS` | 16 | 65104 | `c6da935e918d0b27593154ef5ebfc2dfeeb3b3c51b9e217b41e5d8632abb563d` |
| `runs/generation_v4_fr/traces/R_310eb08f4ac8e3ac9c70.trajectory.jsonl.gz` | `PASS` | 16 | 124721 | `80288107417d340d0ac2486692d2097eb287104e5e4eae3693cacb4cf97d37bd` |
| `runs/generation_v4_fr/traces/R_3b199d59705536b3a2dc.trajectory.jsonl.gz` | `PASS` | 16 | 120950 | `ec37d337ad8758bf9bc19b53468f2054bb14abaa31877126fb996e79e524de1b` |
| `runs/generation_v4_fr/traces/R_ed4a08d4df685fcdd36b.trajectory.jsonl.gz` | `PASS` | 16 | 124201 | `1b5647e737e20193cd745577c58e7b943f32d95e8dd1259089d8083af255cc20` |
| `runs/generation_v4_zh/traces/P_9fd765855ed8cc705a83.trajectory.jsonl.gz` | `PASS` | 16 | 70881 | `94bd166fc24f57e2d0111cd4a6047389019259d54d457e8ae0dfcd4653803547` |
| `runs/generation_v4_zh/traces/R_86f0163d085ec96b2f35.trajectory.jsonl.gz` | `PASS` | 16 | 109168 | `b459cb8bff63837aec7f7dc29f27799d3c50fb35d012ee6a0722a899af6f8124` |
| `runs/generation_v4_zh/traces/R_baade54907802e043b10.trajectory.jsonl.gz` | `PASS` | 16 | 108353 | `4358daf015ae721c9f17b8fbf4b01fcdac7bb9497e937133a5868a287287aa82` |
| `runs/generation_v4_zh/traces/R_cb4e2be9de98fe34f47e.trajectory.jsonl.gz` | `PASS` | 16 | 110140 | `239ec474888b8fe4d3e4507c13884d4f64fa98068e1e8bdb0cd91a7e0660f8e5` |
| `runs/observe_pair_100k/traces/P_f911548ccff4c877fc48.trajectory.jsonl.gz` | `PASS` | 16 | 24416422 | `a16e2b2d617b9ba81bbb4c70012244d0d37ffe21fde5c6efc46d0827d2ef684b` |
| `runs/observe_pair_100k/traces/R_39046ac71621ed530b6d.trajectory.jsonl.gz` | `PASS` | 16 | 33077052 | `d816fe2687b2b2acc9c3f9c0f7f18b6d7de7129614eb277a201fdb883cff67a0` |
| `runs/observe_pair_10k/traces/P_f911548ccff4c877fc48.trajectory.jsonl.gz` | `PASS` | 16 | 2284571 | `20a15e6320e164aeaf5ad396862485ee25d1e6ae1a138a113228c5e49e88edf5` |
| `runs/observe_pair_10k/traces/R_39046ac71621ed530b6d.trajectory.jsonl.gz` | `PASS` | 16 | 2560794 | `2b9e1e8a672fbabd47a818526450484b2bd18994689c305ca70505762da71d99` |
| `runs/observe_pair_1k/traces/P_f911548ccff4c877fc48.trajectory.jsonl.gz` | `PASS` | 16 | 81963 | `0ef9f84cd4e8aaa4ac06998ce62569492d0035306c31e2335677c3288cb1c658` |
| `runs/observe_pair_1k/traces/R_39046ac71621ed530b6d.trajectory.jsonl.gz` | `PASS` | 16 | 222305 | `3e51154c4497a53664ee47e4c7a2db49cec09cce4dd9da8598bbd4876472c9ef` |
| `runs/observe_pair_1m_exact128/traces/P_f911548ccff4c877fc48.trajectory.jsonl.gz.incomplete` | `FAIL_OR_INCOMPLETE` | None | 12547135 | `fd006dec627558cbcc17cf8c825f8b31c3157a28bf38b80f9bbaa9c6f882efc1` |
| `runs/observe_pair_1m_multidim_exact/traces/P_f911548ccff4c877fc48.trajectory.jsonl.gz.incomplete` | `FAIL_OR_INCOMPLETE` | None | 12547135 | `e326b3a1f984c3c7ea922abe4c09bd88f1341abd01d247833776b995cf1de285` |
| `runs/observe_pair_1m_parallel_radius/traces/P_f911548ccff4c877fc48.trajectory.jsonl.gz.incomplete` | `FAIL_OR_INCOMPLETE` | None | 12547135 | `6e62f130a6fb44fdb022dbb912fc04ebd059b8c5f2daa9ebd20a3f3e5a7eba30` |
| `runs/observe_pair_1m_roundeven/traces/P_f911548ccff4c877fc48.trajectory.jsonl.gz.incomplete` | `FAIL_OR_INCOMPLETE` | None | 12547135 | `96e482bbeb02cad32ce49844b44e857d37dd3662265ddbb8601a40afdffbb663` |
| `runs/observe_pair_1m_vectorized/traces/P_f911548ccff4c877fc48.trajectory.jsonl.gz.incomplete` | `FAIL_OR_INCOMPLETE` | None | 12547135 | `fec39d5591f53277b8f21bde1232d861ed4684f176ed26423aebc5024fa2d7b7` |
| `runs/traces/P_3682b594d36e50df4a1b.trajectory.jsonl.gz.incomplete` | `FAIL_OR_INCOMPLETE` | None | 12589383 | `9853d24a8a7b6c75a740719c1b808e39e676276f7c799598ded63fc1d1c79909` |
| `runs/traces/P_e8cecc7a0de52a2a6a47.trajectory.jsonl.gz` | `FAIL_OR_INCOMPLETE` | None | 12532962 | `8b32820f28e2acc00e332b4afdc461c0936d15226e36d5375286b5d7c9726812` |

## eSonde v6 — journaux d'exécution

| Journal | Marqueurs d'échec | Marqueurs PASS | Octets | SHA-256 |
|---|---|---|---:|---|
| `results/bench_seed_vectorization_1m.time.log` | aucun détecté | aucun | 746 | `ef50c1432bb9bd390c3efc5216d50f0c514d5d927271244745d1b723618d858a` |
| `results/dmodel_release_tests.log` | aucun détecté | aucun | 7343 | `309ad3b832a0158151b3c2968b40696f92b034860fdb1045ee8480ec81cabb2f` |
| `results/fixedpoint_tree_index_100k_P.stderr.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/fixedpoint_tree_index_100k_P_vectorized.stderr.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/fixedpoint_tree_index_100k_R.stderr.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/generation_v3_ar.stderr.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/generation_v3_en.stderr.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/generation_v3_fr.stderr.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/generation_v3_zh.stderr.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/generation_v3b_ar.stderr.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/generation_v3b_en.stderr.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/generation_v3b_fr.stderr.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/generation_v3b_zh.stderr.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/generation_v4_ar.stderr.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/generation_v4_en.stderr.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/generation_v4_fr.stderr.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/generation_v4_zh.stderr.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/latex_after_fixes_pass1.stdout.log` | aucun détecté | aucun | 8116 | `59e888d5176be3a6e284b522aaaea9b7397c241cbf68d836cb87a168b3df6a82` |
| `results/latex_after_fixes_pass2.stdout.log` | aucun détecté | aucun | 8116 | `59e888d5176be3a6e284b522aaaea9b7397c241cbf68d836cb87a168b3df6a82` |
| `results/latex_final_pass1.stdout.log` | aucun détecté | aucun | 8116 | `e8045d67337aa5ceb30346d7c92ffce140f920f06d9062b72d9e0c510a986dd4` |
| `results/latex_final_pass2.stdout.log` | aucun détecté | aucun | 8116 | `e8045d67337aa5ceb30346d7c92ffce140f920f06d9062b72d9e0c510a986dd4` |
| `results/latex_fixedpoint_index.log` | ERROR | aucun | 19136 | `a71486493e67f524849a27540d2afaedb732daa57fd7321fe0107e52e8cb8d4e` |
| `results/latex_fixedpoint_index_pass2.log` | ERROR | aucun | 8736 | `738014c4244fb0b563bb9ec00272c381c198cb95a8918f9742c80eeb7f9bdd5e` |
| `results/latex_multidim_index_pass1.stdout.log` | aucun détecté | aucun | 8008 | `018a3de47abdba2140967434ff67cb3f6d070f0e2126a51c48e2e6b7adedfb74` |
| `results/latex_multidim_index_pass2.stdout.log` | aucun détecté | aucun | 8008 | `b1d2eb2f2ffdb8595326edc292f5c508d71c84c461cb947adb33715529f1ca12` |
| `results/latex_multidim_vectorized_pass1.stdout.log` | aucun détecté | aucun | 8008 | `c7dc154ebcbe0e9f3743da1cdc42fcc112e73b849c4f3dcb4a2d56a0210e27a5` |
| `results/latex_multidim_vectorized_pass2.stdout.log` | aucun détecté | aucun | 8008 | `c7dc154ebcbe0e9f3743da1cdc42fcc112e73b849c4f3dcb4a2d56a0210e27a5` |
| `results/latex_pass1.stdout.log` | aucun détecté | aucun | 9191 | `e37dd8c611f00f9ee409efc8fca0f75834b4734f0a328277bfa3d4fc53fa7baa` |
| `results/latex_pass2.stdout.log` | aucun détecté | aucun | 8121 | `05e6a7d02ecef023e779aafe3041a7f5f39d6697dece8c59678ca11473db2d88` |
| `results/latex_reprise_pass1.stdout.log` | aucun détecté | aucun | 8116 | `8572b7357f5b7e64db07cd410cf06f68f53dd554b5b6064d6bc0090f744f6a7e` |
| `results/latex_reprise_pass2.stdout.log` | aucun détecté | aucun | 8116 | `e8045d67337aa5ceb30346d7c92ffce140f920f06d9062b72d9e0c510a986dd4` |
| `results/observe_1m.stderr.log` | aucun détecté | aucun | 1010 | `26e180bf8fc5d79fd7af34d780b730bd7b80425a28ab17345191c933b718d3da` |
| `results/observe_full_1m.stderr.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/observe_full_1m.time.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/observe_pair_100k.time.log` | aucun détecté | aucun | 1043 | `cb47e9d96a8c8b5137f20b05ccd248b731ac6055c5b492faa38ccc06cc0f4db4` |
| `results/observe_pair_1m_exact128.stderr.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/observe_pair_1m_exact128.stdout.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/observe_pair_1m_multidim_exact.stderr.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/observe_pair_1m_native_query_pairs.stderr.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/observe_pair_1m_parallel_radius.stderr.log` | aucun détecté | aucun | 1076 | `89edfcec674eb3ca412d72057e4ef7b37de17d8cae927b7eedc096c199126847` |
| `results/observe_pair_1m_parallel_radius.stdout.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/observe_pair_1m_roundeven.stderr.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/observe_pair_1m_vectorized.stderr.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/observe_pair_1m_vectorized.stdout.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/partition_benchmark_1m.time.log` | aucun détecté | aucun | 1438 | `3712ae3f399f766dcceda517891ad230170623dff5cc2ae4f38f9a2b22e08492` |
| `results/profile_ckdtree_native_100k_P.stderr.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/profile_ckdtree_query_pairs_100k_P.stderr.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/profile_ckdtree_query_pairs_100k_R.stderr.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/savepoint_027.stderr.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/savepoint_030.stderr.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/savepoint_031.stderr.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/train_1m.stderr.time.log` | aucun détecté | aucun | 1030 | `2cce07aa9d772bd95e2bf0d8c3b875292cc5848de6c0ecd69b1907acca1d42e8` |
| `results/train_full_1m.stderr.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/train_full_1m.time.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/train_repro_full_1m.stderr.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/train_v3_1m.time.log` | aucun détecté | aucun | 953 | `fd92374d635cd5d48fd1e919a210b388bec0da2cbfc85d9fad1647d3232cca94` |
| `results/train_v3_1m_with_v5examples.time.log` | aucun détecté | aucun | 997 | `355507cd5bd58f004ee4952b07cac4aa9999a40c6a1bd6f23d2facc45d39ca68` |
| `results/train_v4_1m_no_sms.time.log` | aucun détecté | aucun | 990 | `6e7cebd5ee35c7eaa9bf5bc3dcc64655a0b2eed654d443103186eb4f64543ef1` |
| `results/unit_tests.log` | Traceback, ERROR, FAILED, FAIL | aucun | 2625 | `7df6224e21e10977980812dc3d0648202d02491397fa6a711c61b686a3469601` |
| `results/unit_tests_after_beam_seed_score.log` | aucun détecté | aucun | 5253 | `3f64ae7dc5a044455bab4472d3c282e00ece597af31e1681d0a7d79eec3d9d7d` |
| `results/unit_tests_after_ckdtree_batching.log` | aucun détecté | aucun | 6432 | `d75966ba713e10d156ca299bb956995e13d19e4ea3da682d4d7bc385268b7a6a` |
| `results/unit_tests_after_cli_utf8.log` | aucun détecté | aucun | 4935 | `99b99fb7fae42c90774be5a206967c7edff54f48c9a81760d629b5da424c8a7d` |
| `results/unit_tests_after_csr.log` | aucun détecté | aucun | 3667 | `3f49937dfdbb5bd1ea65436b54438431dfc8f98dc182f01d51cf77b873e6dc74` |
| `results/unit_tests_after_exact_seed_vectorization.log` | aucun détecté | aucun | 3830 | `ab99b5ef8ac982a4c89b8c29a0b74612582387daf9a3b0a745e0a0cb8cb5eb2d` |
| `results/unit_tests_after_gui_fix.log` | aucun détecté | aucun | 6299 | `c0bac758f3537b922914ac0be8de5a54ca388b615744e01d70375dd5796eddc6` |
| `results/unit_tests_after_gui_thread_fix.log` | aucun détecté | aucun | 6299 | `7adf9794660a06728d407d044fa432008ff0d402bfde84f2e93de7148d0d524e` |
| `results/unit_tests_after_invariant_fixes.log` | aucun détecté | aucun | 3667 | `8727b8428f4a2d6102eb801534a1c65e92ef8928f5373ecddfd9c69f3267c9e2` |
| `results/unit_tests_after_semantic_opt.log` | aucun détecté | aucun | 3075 | `3deb68ae1160c06fef2bafb0129c0f4eda32044a41840a161f2131078d9bc865` |
| `results/unit_tests_after_sms_scope.log` | aucun détecté | aucun | 5253 | `263cf580049076f5e2a03b9d9f62c62775280131d593cccf3fcc334566218d19` |
| `results/unit_tests_after_social_normalization.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/unit_tests_after_transform_reuse.log` | aucun détecté | aucun | 3963 | `bfc5101175fade087066bb95927245cc6f7c40a5b26292e0a0643cb08245a1d0` |
| `results/unit_tests_csr_equivalence.log` | aucun détecté | aucun | 3830 | `79e44ae1acc2f1d4145218886296472e6da77b1956b6de6f7d34b2968e15fe70` |
| `results/unit_tests_current_retest.log` | aucun détecté | aucun | 4108 | `6684ae5cade895eecc86e8a4404a0b85c0c19ddd6f88973f8f68fe45af3491ee` |
| `results/unit_tests_exact_vector_filter.log` | aucun détecté | aucun | 6197 | `acff3af4189cbc36825ada9b00545508793029efe58e389af1b6a1c050ec18cf` |
| `results/unit_tests_final.log` | aucun détecté | aucun | 2953 | `05a8cd9a4ae468f2be0d7063ff47da81c406fa5825c675ec840a5c469b477730` |
| `results/unit_tests_final_candidate.log` | aucun détecté | aucun | 7342 | `08f1d13e662b8403de7e5f80033f3518bcb6f5afc945e3598751c18544ea0059` |
| `results/unit_tests_fixedpoint_full.log` | aucun détecté | aucun | 6704 | `43a334c8fa9e654ed77e4e4125753b65acdec63cdefcf8a6258be1bb5f073fc9` |
| `results/unit_tests_fixedpoint_index.log` | Traceback, ERROR, FAILED, FAIL | aucun | 7471 | `e7a0d0a65523e9b57c4f001d60768eb0f5fd1c0d9d983e677ed611f5d03c5924` |
| `results/unit_tests_fixedpoint_index_xvfb.log` | aucun détecté | aucun | 6704 | `3648649390072047980a482f038cb7ab923fbb6123de74ba5ab1a06de24ef1ad` |
| `results/unit_tests_multidim_tree.log` | aucun détecté | aucun | 7026 | `bbdf99cff8f28c537fc902ac3fdc37e4f55d2f83d29f52a52cdd820df48f776e` |
| `results/unit_tests_multidim_tree_final.log` | aucun détecté | aucun | 7026 | `5850d95b7bf07cbb28cc3523c1a719625e63e2912d7f0d1a9cf7c9bf8548ffe2` |
| `results/unit_tests_multidim_vectorized_q.log` | aucun détecté | aucun | 7199 | `ab39b236d8f2c712ba385be75f7a5bf5c47cd5f80e965d15d6083eda0dd24c7b` |
| `results/unit_tests_multidim_vectorized_q_final.log` | aucun détecté | aucun | 7199 | `da403413c798eba4c63ef963dd94196acf14fb7ad25a99594e2c6bcc9938a73b` |
| `results/unit_tests_native_query_pairs.log` | aucun détecté | aucun | 7342 | `da2ab4259108b1b5673e745781fa3665c188bf9dd1bc3fdda6f3ea181a57b5f3` |
| `results/unit_tests_native_query_pairs_final.log` | aucun détecté | aucun | 7342 | `883b5b06939eb7160fc034d53c8bf950a1b77369b4195ed30203c81f93576ada` |
| `results/unit_tests_native_query_pairs_integration.log` | Traceback, ERROR, FAILED, FAIL | aucun | 8109 | `344a337d018b17b57c38bb63d26861def44f3a4a491295dda8663e08d55e6816` |
| `results/unit_tests_native_query_pairs_integration_xvfb.log` | aucun détecté | aucun | 7342 | `49e2c579846c7f85861aeba74b276ae4c7fb365bd26af8ce478ef9c2369cd099` |
| `results/unit_tests_pass2.log` | aucun détecté | aucun | 1457 | `e6f6b1531324706b063ca2cdb2d9464c0c402efd83839af2437151e885eca50f` |
| `results/unit_tests_pretrain.log` | aucun détecté | aucun | 3075 | `0d03c348532490201d09356f90c7d19717c6ae08647eb3c528879f3f1f475982` |
| `results/unit_tests_transform_cache_fix.log` | aucun détecté | aucun | 4108 | `3dca6701ea51f0f3c6583942530d0841cb447a3aa07a694b38576f4fb325c1ee` |
| `results/unit_tests_vectorized_neighbors.log` | aucun détecté | aucun | 5738 | `0d82ae6688237d4a424732d40a4f6d7c11de83428bffea8cd60ef0f29e63db9b` |
| `results/verify_1m.stderr.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/zero_neuron_audit_after_multidim.stderr.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/zero_neuron_audit_after_multidim_final.stderr.log` | aucun détecté | aucun | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

## eSonde v6 — campagnes / dossiers de run

| Campagne | Fichiers | Traces | Incomplètes | Octets |
|---|---:|---:|---:|---:|
| `generation_smoke_en` | 4 | 4 | 0 | 234241 |
| `generation_smoke_fr` | 3 | 3 | 0 | 304095 |
| `generation_smoke_graph` | 4 | 4 | 0 | 218098 |
| `generation_v3_ar` | 4 | 4 | 0 | 457865 |
| `generation_v3_en` | 4 | 4 | 0 | 441090 |
| `generation_v3_fr` | 4 | 4 | 0 | 419297 |
| `generation_v3_zh` | 4 | 4 | 0 | 406838 |
| `generation_v3b_ar` | 4 | 4 | 0 | 451862 |
| `generation_v3b_en` | 4 | 4 | 0 | 419220 |
| `generation_v3b_fr` | 4 | 4 | 0 | 433247 |
| `generation_v3b_zh` | 4 | 4 | 0 | 406838 |
| `generation_v4_ar` | 4 | 4 | 0 | 442931 |
| `generation_v4_en` | 4 | 4 | 0 | 446868 |
| `generation_v4_fr` | 4 | 4 | 0 | 434976 |
| `generation_v4_zh` | 4 | 4 | 0 | 398542 |
| `observe_pair_100k` | 2 | 2 | 0 | 57493474 |
| `observe_pair_10k` | 2 | 2 | 0 | 4845365 |
| `observe_pair_1k` | 2 | 2 | 0 | 304268 |
| `observe_pair_1m_exact128` | 1 | 1 | 1 | 12547135 |
| `observe_pair_1m_multidim_exact` | 1 | 1 | 1 | 12547135 |
| `observe_pair_1m_parallel_radius` | 1 | 1 | 1 | 12547135 |
| `observe_pair_1m_roundeven` | 1 | 1 | 1 | 12547135 |
| `observe_pair_1m_vectorized` | 1 | 1 | 1 | 12547135 |
| `traces` | 2 | 2 | 1 | 25122345 |

## eGenBrain v4 — tours du laboratoire de maillage

| Tour | Statut | Description / observation |
|---|---|---|
| `?` | `PASS` | {"tour": "T01", "status": "PASS", "experiment_artifact": "experiments/tour_T01.json", "experiment_sha256": "59324e8ffb7d27b0e7d7a5f5c9671acddd135d31eadd6b232046dd979f2fcdf0", "integration_title": "Raffinement observationnel", "integrated_conclusion": "La monotonie des classes est intégrée comme proposition de quotient : une résolution plus fine ne fusionne pas des classes précédemment séparées. La définition doit toujours nommer le contexte et la |
| `?` | `PASS` | {"tour": "T02", "status": "PASS", "experiment_artifact": "experiments/tour_T02.json", "experiment_sha256": "7569d3a73c193e9395ac44dfc0a31fb0c4827f2875220a36e937bbb0399b609f", "integration_title": "Seuils hiérarchiques conditionnels", "integrated_conclusion": "La distance ultramétrique est conservée comme géométrie dérivée sous hypothèse explicite de seuils satisfaisant la loi du minimum double, jamais comme propriété automatique de tout maillage. |
| `?` | `PASS` | {"tour": "T03", "status": "PASS", "experiment_artifact": "experiments/tour_T03.json", "experiment_sha256": "3b02cc228f88dd2fcb0419ae6aac5a7ece678dfe67e4e44c69e0f6a011516150", "integration_title": "Superposition sans identité", "integrated_conclusion": "L’intersection de supports est distinguée de l’identité des structures. Le recouvrement doit être qualifié par type : token, occurrence, motif, relation ou règle.", "scope_limit": "contre-exemple f |
| `?` | `PASS` | {"tour": "T04", "status": "PASS", "experiment_artifact": "experiments/tour_T04.json", "experiment_sha256": "520a8ad8c3a1d4b30ad068f5d11cb8e4570fdf8f2fc41089b6b8222ff8dc2083", "integration_title": "Ordre observé distinct de causalité", "integrated_conclusion": "Les relations d’ordre observé et les annotations causales restent des types différents. Aucun passage de l’un à l’autre n’est autorisé sans règle ou annotation explicite.", "scope_limit": " |
| `?` | `PASS` | {"tour": "T05", "status": "PASS", "experiment_artifact": "experiments/tour_T05.json", "experiment_sha256": "416c970a1ead969f1d2681b09edc26ffaaf3c3f85620d366b12122066281a52a", "integration_title": "Sémantique des hyperrègles", "integrated_conclusion": "Les règles conjonctives demandent une représentation des prémisses comme ensemble lié, hyperarête ou mécanisme équivalent. Une projection vers des arêtes indépendantes peut ajouter de fausses conséq |
| `?` | `PASS` | {"tour": "T06", "status": "PASS", "experiment_artifact": "experiments/tour_T06.json", "experiment_sha256": "3ae8f983f2d48be9464b2f3ecc4bdc9a8eab4432fb3e160520150c27de560c11", "integration_title": "Arbitrage union/intersection", "integrated_conclusion": "L’union et l’intersection de candidats sont des opérateurs avec compromis mesurable, et non des stratégies universellement optimales. La précision, le rappel et le coût des faux positifs doivent ê |
| `?` | `PASS` | {"tour": "T07", "status": "PASS", "experiment_artifact": "experiments/tour_T07.json", "experiment_sha256": "bb095c1c59eb10d56cd3b916517f0d07299a864f48b775cf23a61a777d730d21", "integration_title": "Isolation du maillage transitoire", "integrated_conclusion": "Une construction MGR/MGR2 depuis zéro requiert un état vide réellement séparé et une provenance de chaque relation reconstruite. Le test jouet illustre le contrat, sans prétendre tester le ru |
| `?` | `PASS` | {"tour": "T08", "status": "PASS", "experiment_artifact": "experiments/tour_T08.json", "experiment_sha256": "dc5ac7d63950862df94c2a80489f3b1beddce4a5c89948b7736bafea0b305584", "integration_title": "Composition typée et unités", "integrated_conclusion": "La composition arithmétique exige des primitives, des unités compatibles et un opérateur déclaré. Le nombre final peut être dérivé sans être stocké, mais le maillage seul ne remplace pas l’opérateu |
| `?` | `PASS` | {"tour": "T09", "status": "PASS", "experiment_artifact": "experiments/tour_T09.json", "experiment_sha256": "417cc3aa665d827704b0cc790cdba89dec17921f8599612df89f18ce05c96bad", "integration_title": "Composition relationnelle certifiée", "integrated_conclusion": "Une relation nouvelle issue de plusieurs faits requiert une règle explicite, une substitution et une provenance multi-prémisses. Le chemin topologique et le prédicat dérivé demeurent distin |
| `?` | `PASS` | {"tour": "T10", "status": "PASS", "experiment_artifact": "experiments/tour_T10.json", "experiment_sha256": "20b1cb3d9f7e5ef16224351fee62d7194295932e40a19a8cd6a391303b284d88", "integration_title": "Ablation topologique", "integrated_conclusion": "L’ablation établit la dépendance d’un chemin à une arête dans le graphe testé ; elle ne transforme pas cette dépendance topologique en causalité du monde représenté.", "scope_limit": "dépendance topologiq |
| `?` | `PASS` | {"tour": "T11", "status": "PASS", "experiment_artifact": "experiments/tour_T11.json", "experiment_sha256": "f3ddd15f7085c5b5a660a4297c1a91daf58308c7935e6e00ca4915815ab9e69b", "integration_title": "Nouveauté compositionnelle et limites de preuve", "integrated_conclusion": "Une réponse produite pour une combinaison non préenregistrée ne prouve la composition que relativement aux primitives et opérateurs disponibles. Pour tester eGenBrain, l’opérate |

## Lecture des statuts

- `PASS` signifie que la procédure enregistrée a satisfait ses assertions définies ; cela ne généralise pas la validité à un dialogue libre.
- `INCOMPLETE`, `RUNNING`, `NO_RESULT`, `UNPARSEABLE` et `FAIL_OR_INCOMPLETE` restent des statuts distincts.
- Les marqueurs de succès extraits des logs sont des indices de journal ; leur portée exacte est donnée par le test ou la commande source.
- Les résultats micro-monde eGenBrain ne constituent pas un benchmark de génération conversationnelle.
