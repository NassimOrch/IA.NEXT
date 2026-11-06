# Rapport ressources et généralisation EX5

## Ressources mesurées et non mesurées

L'environnement est CPU-only : Python 3.13.5, PyTorch 2.10.0+cpu, NumPy 2.3.5, scikit-learn 1.8.0, trois threads CPU autorisés, RAM hôte ≈6,24 Go. Pas de CUDA, VRAM indisponible, pas de wattmètre énergétique.

Mesures présentes dans les registres : `P_total/P_train`, MACs analytiques du forward (approximation et non FLOPs instrumentés), temps d'entraînement, latences batch 1/16/64 après warm-up, p95 et débit, RSS delta par processus pendant certaines campagnes, taille sérialisée de déploiement et taille de checkpoint.

Dimensions incomplètes : MACs/FLOPs du backward+step non mesurés ; coût total de tuning et profils séparés chargement/fit/évaluation pas complet pour tous les bras ; RSS non isolé/mesuré de manière uniforme à chaque stade ; énergie non mesurée (instrument absent) ; VRAM impossible (CPU seul). Ces champs restent explicitement indisponibles.

La règle rouge ne se réduit pas au nombre de paramètres. Plusieurs sondes sont plus petites sur disque, mais leur latence batch 1 est typiquement 4× à 45× supérieure aux MLP comparés ; l'entraînement peut également être beaucoup plus long. Pour la micro-MIXA 75/25 d4/k4 à gate conditionnel, la sonde est plus petite en fichier (11 989 vs 15 965 octets) mais 12,1× plus lente en latence et plus lente à entraîner. Pour l'OOF adaptatif, la sonde a 16 311 octets vs 21 725, mais environ 38,7× la latence batch 1.

## Généralisation indépendante et partitions

Wisconsin est un jeu développemental historiquement exposé dans EX2/EX4 ; il ne constitue pas une confirmation vierge. Les évaluations externes v3 sont Wine et Digits. Pour les deux, les indices du test ont été tirés par permutation sans consulter ni les caractéristiques ni les labels test ; les ensembles non-test ont ensuite été séparés train/adaptation/validation ; scaler train-only. Checkpoints, codes, hyperparamètres et prédictions validation ont été hashés et gelés avant tout indexage des valeurs test. Le manifeste porte le statut `FROZEN_BEFORE_TEST_FEATURE_OR_LABEL_ACCESS`.

| Dataset / gate | Test n | Accuracy sonde | Log-loss sonde | Accuracy MLP ge4x | Log-loss MLP ge4x |
|---|---:|---:|---:|---:|---:|
| wine / equal | 36 | 0.97222 | 0.07410 | 1.00000 | 0.02927 |
| wine / input | 36 | 0.99444 | 0.02373 | 1.00000 | 0.02523 |
| digits / equal | 360 | 0.87722 | 0.44408 | 0.95667 | 0.18242 |
| digits / input | 360 | 0.86444 | 0.54129 | 0.95389 | 0.17923 |

Chaque test a été appliqué au même modèle de données cinq fois via cinq seeds modèle ; les cinq graines ne représentent pas cinq tests indépendants. Wine n'a que 36 exemples test : la log-loss moyenne du gate input (0,02373) est légèrement inférieure à celle de son MLP ge4x (0,02523), mais accuracy moyenne 0,99444 vs 1,0, et latence ≈0,172 ms vs 0,0194 ms. Ce résultat descriptif sur 36 observations ne permet pas une conclusion de non-infériorité. Sur Digits, les MLP sont nettement meilleurs en accuracy et log-loss. `load_digits` correspond à 1 797 observations et 64 pixels 8×8, documenté comme la copie de la partition de test UCI ; ce n'est pas l'ensemble UCI complet.

Banknote Authentication et MAGIC Gamma Telescope ont été recherchés sur UCI et sur la collection miroir OpenML/DataHub. Les pages et fichiers CSV sont vérifiables dans le navigateur, mais les téléchargements n'ont pas abouti dans le conteneur : `curl` échoue avec `Could not resolve host: datahub.io`, et le service web ne rend pas `text/csv` (unsupported content-type). Aucun jeu local n'a été fabriqué et aucun résultat n'est rapporté pour ces deux domaines. Wine/Digits complètent une partie du transfert, mais la généralisation multi-domaines exigée reste partielle.
