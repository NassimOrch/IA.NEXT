# Rapport de transfert externe — Iris EX4 v009

## Provenance et taille
Le bras local est `sklearn.datasets.load_iris`, 150 lignes, 4 caractéristiques, 3 classes. La documentation scikit-learn décrit la copie comme la version alignée sur `R datasets::iris` et différente de l'archive UCI sur deux points. Le jeu exact chargé est archivé en CSV/NPZ et identifié par SHA-256. Iris n'a pas été trouvé dans les archives sources EX4 fournies ; cela établit seulement son absence de ces fichiers, pas qu'il soit inédit dans toute l'histoire du projet.

## Partition et protocole
Split seed 20261030, tailles fixes train=90, validation=20, adaptation=10, test=30 ; cinq seeds d'initialisation. StandardScaler ajusté sur train uniquement. Quatre candidates gelées (adaptatif seul et trois variantes micro-MIXA), MLP matched et ge4x. Le plus petit ratio total ge4x, scaler inclus, est 4,015625×. Les états, prédictions de validation et configurations sont archivés et hashés avant l'évaluation test ; le journal indique le gel puis l'ouverture du test, sans optimisation post-test.

**Réserve d'isolation :** l'API scikit-learn matérialise le tableau complet en mémoire, et le splitteur stratifié utilise le vecteur des classes pour assigner les identifiants de partition ; le CSV/NPZ source complet a aussi été conservé avant le gel. En revanche, les lignes test ne servent ni au scaler, ni aux gradients, ni à l'arrêt, ni aux métriques, ni à la sélection de candidate avant le gel. Cette expérience ne revendique pas une isolation mémoire/processus absolue : l'exception liée à l'API et au split est exposée dans `data_manifest/ex4_iris_isolation_caveat.json`.

## Résultat test (n=30; moyenne sur 5 initialisations)
| Candidate | Accuracy | Log-loss | MLP ge4 accuracy | MLP ge4 log-loss | Ratio P_total |
|---|---:|---:|---:|---:|---:|
| Adaptative seule | 0,9533 | 0,16466 | 0,9667 | 0,09761 | 4,0737× |
| MIXA mélange égal | 0,9600 | 0,12062 | 0,9667 | 0,09633 | 4,0165× |
| MIXA gate global | 0,9667 | 0,14282 | 0,9667 | 0,09331 | 4,0163× |
| MIXA gate conditionnel | 0,9667 | 0,17272 | 0,9667 | 0,09420 | 4,0156× |

Les métriques sont recalculées à partir des prédictions brutes dans `scripts/audit_iris_transfer.py`. Comme n=30, chaque erreur change l'accuracy de 3,33 points. Les cinq initialisations réutilisent les mêmes 30 observations ; leurs résultats ne multiplient pas le n indépendant. Aucun test de non-infériorité formelle n'est revendiqué.

## Coûts et limites
La taille, les MAC analytiques, la latence CPU et les temps d'entraînement sont rapportés dans `results/processed/ex4_iris_ge4x_resource_performance_summary.csv`. Les MAC omettent non-linéarités, exponentielles, opérations élémentaires et coût de l'optimiseur ; ce ne sont pas des compteurs matériels. RSS est un relevé global du processus. CUDA/VRAM et énergie ne sont pas mesurés. Les cinq checkpoints adaptatifs terminés dans le pré-vol sont récupérés depuis les états sauvegardés ; les temps d'entraînement et historiques non enregistrés restent ND. Deux états fixed-only incomplets sont quarantinés.

## Données additionnelles non obtenues
Les tentatives de récupération UCI Banknote Authentication (1 372 lignes, 4 caractéristiques) et MAGIC Gamma Telescope (19 020 lignes, 10 caractéristiques) ont échoué : le conteneur ne pouvait pas résoudre les hôtes de téléchargement et le navigateur ne permettait pas de récupérer les archives ZIP binaires dans ce contexte. Aucun résultat n'est revendiqué pour ces deux jeux. Ils auraient été des candidats de transfert externes plus substantiés qu'Iris ; leur indisponibilité est un obstacle technique concret, non une préférence de protocole.

## Portée
Iris fournit un seul transfert exploratoire sur données locales packagées, pas une confirmation multi-domaines. La cible EX4 n'est pas atteinte simultanément : les MLP conservent une meilleure log-loss, une latence plus faible, et un coût d'entraînement inférieur sur les bras micro-MIXA mesurables.
