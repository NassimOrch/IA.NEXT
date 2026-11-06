# EX12_NEXT_0 — Rapport de clôture P1

**Porte P1 : PASS avec limites de plateforme déclarées.**

## 1. Objet et périmètre

P1 vérifie la correction numérique des noyaux de distance/activation/lecture HC-RBF, valide le banc de mesure et compare certaines réalisations informatiques avant tout entraînement. Aucun modèle n'a été entraîné dans cette phase. Le résultat P1 ne démontre aucune supériorité prédictive.

Plateforme observée : AMD EPYC 9V74, 3 CPU logiques visibles, PyTorch 2.10.0+cpu, Python 3.13.5, un seul thread PyTorch par benchmark. CUDA, VRAM et compteur énergétique calibré indisponibles. La RSS est au niveau du processus et les bytes structurels sont des estimations de tenseurs, pas des mesures d'accès mémoire matériel.

## 2. Historique intégral des tentatives conservées

| Run | Statut | Données | Tests | Usage dans les conclusions |
|---|---|---:|---:|---|
| P1_RUN_001_FAILED | Échec | 384 lignes, 15 360 mesures | 54, dont 35 échecs | Conservé, exclu des comparaisons finales. Le calcul d'identité float32 des distances a divergé jusqu'à 2,2888e-5; un test pytest de gradient échouait marginalement. |
| P1_RUN_002 | Provisoire | 420 lignes, 16 800 mesures | 54, 0 échec | Conservé, mais non utilisé pour conclure sur top-q : la mesure top-q excluait distance/activation tandis que le dense les incluait. |
| P1_RUN_003 | PASS | 600 lignes, 24 000 mesures | 126, 0 échec | Benchmark end-to-end apparié de référence. |
| P1_RUN_004 | PASS | 600 lignes, 24 000 mesures | 126, 0 échec | Réplication indépendante, graine différente. |

Le script exact des deux prototypes initiaux RUN_001/RUN_002 n'a pas été retrouvé dans le workspace. Cette lacune est signalée dans `P1_RUN_REGISTRY.jsonl` et ne doit pas être masquée. Leurs fichiers de résultats restent conservés sans modification. Les scripts exacts utilisés pour RUN_003/RUN_004, leur code noyau et l'analyse de résultats sont fournis avec SHA-256. Les copies du RUN_001 à la racine de P1 ont été vérifiées identiques à celles du répertoire `attempts/P1_RUN_001_FAILED`.

## 3. Validation numérique

RUN_003 et RUN_004 ont chacun 126 contrôles numériques et aucun échec. L'erreur maximale de sortie du chemin HC complet est 0; l'erreur maximale des gradients entrée/paramètres est 2,9802322387695312e-8, sous la tolérance 1e-6. Le test pytest indépendant donne 19 tests réussis (`P1_RUN_003/P1_PYTEST_FINAL.log`). Les distances calculées par broadcasting direct coïncident avec la référence explicite dans les 36 formes testées. L'implémentation identité avec accumulation float64 respecte la tolérance, mais reste plus lente que le broadcasting sur les deux runs.

## 4. Validation du banc et intégrité statistique des mesures

Chaque run canonique contient 600 groupes kernel/forme, 40 mesures par groupe et donc 24 000 mesures brutes. L'analyse indépendante a recomposé p50, p95, p99, moyenne et écart-type depuis les CSV bruts. Les 1 200 groupes (600 x 2 runs) concordent avec les synthèses à 1e-9 près; aucun groupe ne manque et aucun agrégat n'a été modifié. Chaque essai est exécuté avec 5 warmups, 40 observations chronométrées, un thread et un ordre de kernels mélangé. La seconde graine vérifie la stabilité des rapports de latence.

## 5. Comparaisons informatiques appariées

Ratios calculés forme par forme sur le même batch, nombre de centres et dimension latente; ratio inférieur à 1 signifie que le premier kernel est plus rapide.

| Comparaison p50 | RUN 003 médiane (Q1–Q3) | RUN 004 médiane (Q1–Q3) | configurations plus rapides |
|---|---:|---:|---:|
| Distance broadcasting / boucle | 0,118 (0,069–0,174) | 0,113 (0,070–0,178) | 36/36 dans les deux runs |
| Distance identité-float64 / boucle | 0,186 (0,106–0,350) | 0,181 (0,109–0,331) | 36/36 dans les deux runs |
| Forward HC broadcasting / référence | 0,240 (0,168–0,324) | 0,235 (0,168–0,318) | 36/36 dans les deux runs |
| Forward HC identité-float64 / référence | 0,291 (0,186–0,497) | 0,295 (0,180–0,479) | 36/36 dans les deux runs |

Le broadcasting direct réduit donc la p50 d'un facteur médian de 8,46x puis 8,89x sur le noyau de distance, et de 4,16x puis 4,25x sur le forward HC complet. La vectorisation est une équivalence d'implémentation, pas une nouvelle capacité d'apprentissage.

## 6. Décision sur la parcimonie top-q

La comparaison corrigée est end-to-end : dense = distance + activation + lecture dense; sparse = distance + activation + top-k + gather de poids + lecture sparse.

| q | ratio p50 top-q / dense RUN003 | RUN004 | configurations top-q plus rapides |
|---:|---:|---:|---:|
| 2 | 1,280 | 1,271 | 0/36, 0/36 |
| 4 | 1,307 | 1,286 | 0/36, 0/36 |
| 8 | 1,337 | 1,324 | 0/36, 0/36 |
| 16 | 1,396 | 1,375 | 0/12, 0/12 |

La sélection top-q est donc **rejetée de l'architecture de base P1** sur la plateforme mesurée : le tri et le gather coûtent davantage que le calcul dense. Elle ne pourra être réintroduite qu'avec une nouvelle implémentation pré-enregistrée dont le coût complet est mesuré et plus faible.

## 7. Modules supplémentaires et initialisation des centres

Le module de modulation faible-rang, isolément, présente une p50 environ 7,36x (RUN003) et 7,55x (RUN004) celle du readout affine-RBF. Cette comparaison de modules est un signal de coût, non une comparaison de modèles complets; C5 est différé et ne sera activé qu'en ablation justifiée. Le bloc message-passing à trois tours est environ 13,28x/13,45x la latence du forward HC complet vectorisé; il est exclu du chemin critique de base.

Les médianes p50 d'initialisation (9 configurations, 7 répétitions chacune) sont : Sobol sur bornes train 0,050/0,061 ms; farthest-point train-only 0,302/0,292 ms; KMeans train-only 10,902/11,908 ms. Ces mesures appuient le maintien de Sobol pour les centres globaux et de farthest-point comme alternative locale peu coûteuse. KMeans est conservé comme option de contrôle, pas éliminé ni considéré scientifiquement inférieur par la seule durée d'initialisation.

## 8. Décisions P1 qui contraignent P2

1. Utiliser `squared_distances_vectorized` (broadcast direct) comme noyau primaire, avec test d'équivalence contre la référence.
2. Ne pas activer le top-q dans la base.
3. Différer la modulation faible-rang et le message-passing dynamique du chemin critique; les variantes restent identifiées comme non retenues/deferred, pas présentées comme testées prédictivement.
4. Garder les centres déterministes Sobol/farthest et KMeans train-only comme comparateurs d'initialisation.
5. Tous les entraînements restent interdits jusqu'à PASS de P1; ce gate est maintenant satisfait.

## 9. Limites

P1 est CPU-only, un thread. Les mesures n'établissent pas les temps sur GPU, consommation électrique, mémoire de pic par modèle ou latence dans un environnement de déploiement différent. Elles n'incluent pas le coût d'apprentissage et ne renseignent pas sur précision, log-loss, calibration, extrapolation ou stabilité entre graines de modèles. Ces dimensions appartiennent aux phases d'entraînement et de validation ultérieures.

## 10. Artefacts et reproductibilité

- `04_code/hc_kernels.py`, `p1_microbench.py`, `p1_microbench_repeat.py`, `test_p1_kernels.py`, `analyze_p1.py` : code utilisé avec SHA-256 dans `08_benchmarks/P1/P1_SOURCE_HASHES.json`.
- `08_benchmarks/P1/P1_RUN_003/` et `P1_RUN_004/` : mesures brutes, synthèses, tests, métadonnées et logs.
- `08_benchmarks/P1/P1_RAW_TO_SUMMARY_AUDIT.csv` : audit des 1 200 groupes.
- `08_benchmarks/P1/P1_PAIRED_KERNEL_COMPARISONS.csv` : ratios appariés.
- `08_benchmarks/P1/P1_CENTER_INIT_COMPARISON.csv` et `P1_CROSS_RUN_REPEATABILITY.csv`.
- `00_governance/P1_RUN_REGISTRY.jsonl` : registre append-only des quatre tentatives.
- `00_governance/P1_DECISIONS.json` et `P1_phase_gate.json` : décisions et porte de phase.

**Conclusion : P1 PASS.** Cela autorise P2 (criblage architectural), pas le test final ni une revendication de performance prédictive.
