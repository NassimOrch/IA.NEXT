# Écart de capture des traces — EX9 v011

Les 45 runs de classification possèdent un JSON, un checkpoint, une configuration, les prédictions validation et les métriques. Les candidates B10/B11/A0 conservent leurs objets de trace dans `fit_record` (OOF owner maps, historiques de sondes, seuils/actions, folds PCA/OOF et sélection). Les neuf pilotes CNG/CNC conservent les historiques de loss par époque.

**Limite identifiée après audit du code :** `fit_mlp()` construit et retourne un historique MLP par époque, mais `run_all()` n'écrit pas ce champ dans les JSON des runs `MLP_MATCHED` et `MLP_GE4X`. Les prédictions finales, métriques, compte de paramètres, hidden size, ratio et checkpoints sont persistés, mais les courbes/historiques MLP complets ne le sont pas. Les états des optimiseurs n'ont pas non plus été sauvegardés. Aucune trace absente n'est inventée ou reconstituée en la présentant comme originale.

Ce défaut rend le livrable partiellement non conforme à l'exigence d'exhaustivité du prompt. Une future campagne doit écrire `history`, l'état optimal et les états d'optimiseur/étapes dès le run. Une relecture/ré-exécution MLP après ouverture du holdout actuel n'a pas été faite : le verrou et les résultats ne doivent pas être altérés.


## Source snapshot relocation

Pour la cohorte de classification Rev2, la sortie a d'abord été écrite dans `results/models_v2/`, puis les artefacts ont été déplacés dans le chemin canonique `results/models/`. Le script conservé `src/classification_models.py` a été ajusté ensuite uniquement pour viser les chemins canoniques `results/models/` et `results/processed/`. Les fonctions d'architecture/entraînement n'ont pas été changées, mais un snapshot octet-pour-octet du script à l'instant initial des runs n'a pas été conservé séparément. Le hash du verrou correspond au script path-normalisé utilisé pour l'audit/gel, et non à un snapshot byte-identique de la commande d'entraînement antérieure.


## Agrégat de runs initial obsolète

`results/processed/CLASSIFICATION_RUN_SUMMARY.json` a été écrit à la reprise de la cinquième graine (`seed 3037`) et ne comptait alors que les 9 runs exécutés pendant cette commande de reprise. Il ne représente pas la cohorte totale. Le sommaire réconcilié `CLASSIFICATION_RUN_SUMMARY_RECONCILED.json`, calculé depuis les 45 JSON effectivement présents, est le seul agrégat global à utiliser. Le fichier initial est conservé parce qu’il fait partie de la trace de gel, et n’a pas été écrasé.


## Initialisation K-means B10/B11

Dans `fit_probe_bank`, les mises à jour supervisées sont propres aux shards et les masques OOF retirent la sonde propriétaire, mais l'initialisation KMeans de chaque sonde voit l'ensemble des `X_train` sans labels. Le registre JSON la qualifie comme initialisation globale non supervisée. Cela relève de `transductive_train_X`, pas d'une fuite de labels, mais pas d'un OOF strictement fold-pure en caractéristiques. L'ablation KMeans limitée à chaque shard n'a pas été exécutée. A0 Rev2, en revanche, initialise chaque fold global sur ses indices d'entraînement uniquement.

## CNC DIV : densité du diviseur

Le pilote DIV respecte le support admissible `[-1,-0.25] U [0.25,3]`, mais il a échantillonné les moitiés négative/positive à 50/50. La distribution exacte induite par `c+1`, avec `c` uniforme dans `[-2,2]` et le voisinage du pôle exclu, n'est pas équilibrée 50/50 (les supports ont des longueurs 0.75 et 2.75). Ce run est donc uniquement un pilote de support et non une réplication exacte de la distribution du graphe f2. Il doit être refait avec une densité induite correcte avant toute composition CNC-2.

## Extension de trace multi-domaines

Les 90 runs concentric2/rotated_moons2 ont été exécutés via `src/multi_domain_dev.py`, qui importe `classification_models` comme module. Leur JSON contient les historiques MLP par époque, le hidden size, les compteurs, les métriques, les temps de fit, latences, prédictions validation et hashes de config/checkpoint/source. Cela comble pour ces deux domaines la lacune d'historique MLP identifiée sur XOR8. Les états d'optimiseur restent non sauvegardés. Les 45 runs XOR8 initiaux ne sont pas réentraînés pour reconstituer les historiques manquants, en particulier après l'incident d'ouverture de son holdout.
