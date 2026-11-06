# Ressources et vitesse — EX9 v011

## Environnement

Exécution sur CPU seulement (`torch 2.10.0+cpu`, Python 3.13, NumPy/scikit-learn ; 3 CPU logiques rapportés dans la session, RAM disponible environ 5,8 GiB). Aucun GPU ni wattmètre disponible. Le profil de classification utilise 20 warmups et 40 répétitions par batch, synchronisation CPU ; p95/p99 sont descriptifs et sous-échantillonnés.

## `xor8` — candidats versus comparateurs

| Modèle | P_total | Fit E2E moyen (s) | Latence batch1 p50 E2E (ms) |
|---|---:|---:|---:|
| B10 | 400 | 1,2511 | 0,4076 |
| MLP B10 matched | 403 | 0,7273 | 0,0170 |
| MLP B10 ≥4× | 1 602 | 0,6343 | 0,0179 |
| B11 | 351 | 0,7123 | 0,2326 |
| MLP B11 matched | 348 | 0,7461 | 0,0171 |
| MLP B11 ≥4× | 1 404 | 0,6149 | 0,0176 |
| A0 | 608 | 1,7319 | 0,4105 |
| MLP A0 matched | 612 | 0,6953 | 0,0172 |
| MLP A0 ≥4× | 2 438 | 0,5773 | 0,0180 |

La latence du modèle seul est aussi conservée dans les JSON. L'end-to-end comprend StandardScaler+modèle. Le coût du KMeans, OOF/PCA et entraînement global A0 est inclus dans le temps E2E du candidat. Les comparateurs ont chacun leur scaler compté et profilé symétriquement.

## Mesures absentes ou non comparables

MAC/FLOPs complet : ND ; seuls les proxies structuraux déclarés par script existent. Mémoire RSS peak : ND (pas de capture homogène par run). Énergie : ND. Optimizer-state bytes complets : ND. Latence GPU : ND. Les tailles checkpoints sont conservées dans le système de fichiers mais ne sont pas un substitut à RSS ni à la mémoire de travail.

## Verdict

Sur ce petit dataset synthétique, le coût runtime des sondes en PyTorch CPU est plus élevé que celui des MLP. Le coût RBF, la construction des centres et la coordination dominent sur petit batch. Le profil est un diagnostic matériel/implémentation, pas une conclusion générale sur une implémentation optimisée C++/GPU ou une autre taille de charge.

## Extension multi-domaines concentric2 / rotated_moons2

Les 90 runs additionnels (45 par domaine) ont été profilés avec le même protocole CPU (StandardScaler + modèle, warm-up 20, 40 mesures). Moyennes sur cinq seeds :

| Domaine | Modèle | P_total | Fit E2E (s) | p50 batch 1 E2E (ms) |
|---|---|---:|---:|---:|
| concentric2 | B10 | 268 | 2.623 | 0.3847 |
| concentric2 | MLP B10 apparié | 266 | 2.308 | 0.0171 |
| concentric2 | B11 | 219 | 2.011 | 0.2228 |
| concentric2 | MLP B11 apparié | 221 | 2.284 | 0.0170 |
| concentric2 | A0 | 554 | 3.178 | 0.3456 |
| concentric2 | MLP A0 apparié | 556 | 2.290 | 0.0171 |
| rotated_moons2 | B10 | 268 | 1.243 | 0.3669 |
| rotated_moons2 | MLP B10 apparié | 266 | 1.567 | 0.0170 |
| rotated_moons2 | B11 | 219 | 1.005 | 0.2048 |
| rotated_moons2 | MLP B11 apparié | 221 | 1.478 | 0.0169 |
| rotated_moons2 | A0 | 554 | 1.848 | 0.2911 |
| rotated_moons2 | MLP A0 apparié | 556 | 1.428 | 0.0174 |

L'inférence des candidates est ici environ 12–22× plus lente que celle des MLP appariés en p50 batch 1. Les temps de fit sont variables selon la tâche : B11 est parfois plus rapide, A0 parfois plus lent, B10 sans avantage stable. Le MLP_GE4X conserve le ratio `P_total≥4`. Ces mesures décrivent l'implémentation PyTorch CPU actuelle et n'excluent pas des optimisations de kernels, mais aucun gain de ressources/latence n'est démontré par l'implémentation évaluée.

Les mesures complètes FLOPs/MAC, RSS peak isolé par run, énergie et GPU restent `ND`. Les proxies MAC structurels présents dans les JSON sont des bornes partielles et n'incluent pas toute la coordination et les opérations non-linéaires.
