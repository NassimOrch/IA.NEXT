# Matrice de conformité — prompt EX11 v2.2.0-reconstructed

Date : 2026-11-03. Cette matrice distingue les exigences vérifiées, les exécutions en cours et les exigences non encore exécutées. Une exigence présente dans le prompt n'est pas considérée satisfaite simplement parce que le code correspondant existe.

| Exigence | Preuve/artefact | État réel |
|---|---|---|
| Ne présumer ni réussite ni échec ; interdiction de tricher/saboter directement ou indirectement | `prompt_ex11.json`, `PRE_REGISTRATION_EX11.md` | PASS documentaire |
| Workspace exclusivement EX11 ; archives historiques laissées hors livraison | inventaire `/mnt/data/EX11`, `AUDIT_SOURCES_EX11.md` | PASS ; aucun ZIP historique copié dans EX11 |
| Provenance de `last_sources_3.zip` | SHA-256 attendu et mesuré identiques | PASS |
| Intégrité de `datasets_arff.zip` et extraction | CRC ZIP, SHA-256, comparaison binaire des 13 ARFF | PASS |
| Audit des 13 datasets, doublons et conflits | `data/metadata/dataset_audit_v002.json` | PASS |
| 65 splits train/validation/test group-stratifiés | manifestes + vérification indépendante | PASS ; tous les CSV test `0440` |
| Pas d'accès test par entraînement | contrôle des scripts et configs ; `test_access=false` | PASS pour les campagnes exécutées ; test scellé non ouvert |
| Tests logiciels et compilation | `PYTHONPATH=$PWD pytest -q`, `compileall` | PASS : 17/17 tests |
| REPLICA-U principal, 13 datasets × 5 seeds | `train_replica_campaign_v003.py`, JSON/NPZ/checkpoints/OOF | IN_PROGRESS ; les runs terminés passent l'audit indépendant |
| REPLICA C1 spécialistes gelés, T0, routeur sans désaccord, top-1/top-2 | campagne principale + `evaluate_replica_inference_ablations_v001.py` | PARTIEL ; top-1/top-2 et zéro-désaccord post-hoc testés sur 24 runs ; T0 et C1 gelé non exécutés ; top-k actuel calcule les 7 spécialistes avant le masque |
| MLP matched et GE4X pour étudiants | rapports/checkpoints REPLICA | PARTIEL ; matched/GE4X existent pour student 64/32 ; matched propre au 32/16 non exécuté |
| CNG A1/A2/A3 et MLP, dix seeds, six fonctions, KMeans train-only | `train_cng_suite_v002.py` | NOT STARTED ; les 18 runs v001 f1/f2 seed1501 restent exploratoires car initialisation antérieure non-KMeans |
| CNG LOO M=4/M=7, régimes F/R | `run_cng_loo_ablation.py` | NOT STARTED |
| CNC C1–C5, six opérations, g1–g5, dix seeds | v003 et v004 | PARTIEL ; v004 KMeans seed1501 terminé ; neuf seeds restantes |
| D1/D2 équivalence sorties et gradients | `d1d2d3_microbenchmark.json` | PASS ; erreurs max sous tolérance `1e-6` |
| D1/D2/D3 profiling pré-campagne | `d1d2d3_microbenchmark.csv` | PASS descriptif ; un thread, 30 warmups, 200 répétitions, 4 batchs |
| D3 qualité sur f1/f2/f5/f6, dix seeds, GE4X contre la plus grande sonde | `train_efficiency_quality.py` v001 | IN PROGRESS et exploratoire ; MLP_GE4X v001 n'est pas ≥4× D1/D2 ; timings de campagne contaminés par contention |
| D3 comparateur MLP réellement ≥4× max(D1,D2,D3) | `train_d3_ge4x_corrected.py`, `train_efficiency_quality_v003.py` | NOT STARTED |
| Timing d'entraînement/inférence isolé | microbenchmark pré-campagne uniquement | PARTIEL ; training times D3Q/REPLICA/CNC en contention et non confirmatoires |
| Test scellé uniquement après gel P3 | répertoire `data/sealed_test`, scripts | PASS d'abstention ; aucune évaluation scellée lancée car P3 non terminée |
| Rapport et archive finale CRC | à créer après consolidation | NOT STARTED |

## Décision globale

**Le prompt est respecté sur les règles de vérité, de provenance, d'intégrité, de séparation des données et de non-ouverture du test. L'exécution scientifique EX11 n'est PAS terminée.** P0/P1 et les contrôles logiciels P2 sont satisfaits. P3 reste incomplet (REPLICA, CNG/CNC et D3). P4 (test scellé) et P5 (livraison finale) ne doivent donc pas être déclarées terminées. Aucun chiffre manquant n'est interpolé et aucun run incomplet n'est transformé en run réussi.

## Audit addendum — 2026-11-03, strict byte-level prompt synchronization

A byte-level check found that the JSON `prompt` field lacked the terminal newline present in `PRE_REGISTRATION_EX11.md`; the previous matrix entry describing an exact byte match was premature. The JSON body has now been resynchronized to the full Markdown body. `revision.prompt_body_sha256` stores the Markdown body hash and `checksums/prompt_ex11_v2.2.0.sha256` stores hashes of both files. A post-write parse/hash check confirms exact byte equality.

New confirmatory code prepared after inspection:
- `src/training/train_efficiency_quality_v004.py`: resumable D3 campaign, train-only KMeans, exact D1→D2 weight copy, MLP GE4X against the largest of D1/D2/D3. Status: **implemented and compiled; not yet run**.
- `src/training/train_cng_suite_v003.py`: resumable CNG campaign, train-only KMeans, shared mini-batch order seed across paired variants, no test generation. Status: **implemented and compiled; not yet run**.
- Tests expanded to cover confirmatory D1/D2 construction and true GE4X sizing. Current suite: **21/21 PASS**.

Campaign state must be read from live registries, not this addendum: the old D3Q v001 has 160/160 exploratory runs with a clean exit and an artifact audit; REPLICA-U v003 is still running and all its runs are classified exploratory due the verified final-refit scope deviation. CNC v004 has one completed seed out of ten. CNG confirmatory, D3 quality confirmatory, REPLICA v004, CNC remaining seeds, LOO, sealed-test scoring and final profiling remain unfinished unless later registries establish otherwise.
