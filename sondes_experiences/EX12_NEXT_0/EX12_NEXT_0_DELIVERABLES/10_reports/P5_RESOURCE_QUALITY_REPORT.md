# EX12 — Rapport P5 : qualité, latence, coût et stabilité

> Statut de phase : **PASS sur complétude et traçabilité des mesures**. Ce statut ne signifie pas que les critères d’efficacité sont satisfaits. Les résultats ci-dessous sont exploratoires et fondés exclusivement sur les données de validation P3/P4 ; aucun test/holdout n’a été ouvert.

## 1. Périmètre et protocole

- 640 checkpoints uniques : 480 runs P3 et 160 MLP additionnels P4 ; 80 checkpoints par slot (M0_CORE, M0_AFFINE, R0, C2, C3, C4, M0_C3_TRAINABLE, M0_C4_TRAINABLE).
- Comparaisons candidates/MLP : R0 et C2 contre M0_CORE ; C3 contre M0_C3_TRAINABLE ; C4 contre M0_C4_TRAINABLE. 80 paires par variante, soit 320 paires.
- CPU mono-thread, affinité CPU 0, environnement Python 3.13.5, PyTorch 2.10.0+cpu, NumPy 2.3.5 ; CUDA indisponible.
- Batches 1, 16, 64, 256 ; 20 warm-ups et 100 mesures par batch et checkpoint. Chaque modèle a été mesuré dans un processus frais et séquentiel.
- Latence du `forward` seulement ; chargement, normalisation, initialisation et premier appel à froid sont enregistrés séparément.
- Entraînement : total reconstruit à partir du temps de fit P3/P4 et de composants de prétraitement mesurés à nouveau ; ce n’est pas une mesure continue par chronomètre unique. Pour P4, l’initialisation du MLP est aussi ajoutée car son timer de fit démarrait après création du modèle.
- Mémoire : pic RSS/USS et hausse incrémentale au-dessus du baseline du processus ; l’énergie est `NOT_MEASURED` faute de wattmètre matériel fiable.
- Qualité : métriques de validation gelées P3/P4, appariées par tâche et graine. Les intervalles t à 95 % sont descriptifs sur 10 graines ; pas de revendication confirmatoire ni correction de multiplicité P7 à cette phase.

## 2. Intégrité et traçabilité

- 640/640 lignes de registre SUCCESS, 640 run IDs uniques et 640 fichiers de mesures par modèle.
- 256 000 valeurs brutes de latence présentes (640 × 4 batchs × 100 répétitions) ; 2 560 synthèses modèle×batch.
- 320/320 paires candidate/MLP établies ; 4 480 lignes qualité graine×métrique conservées.
- 0 checkpoint manquant ; 0 mismatch SHA-256 entre registre et checkpoint ; 0 batch manquant ; 0 mismatch ID / fichier brut.
- Un démarrage de worker `P5_PILOT_001` a échoué avant le chargement d’un modèle (appel interdit à `torch.set_num_interop_threads` dans worker forké). Cet échec de harness est conservé dans `P5_EXECUTION_ATTEMPTS.jsonl`; les 640 mesures sont les succès post-correction.
- Les 8 tout premiers pilotes ne comportent pas de champ `benchmark_script_sha256`. Le fichier source `benchmark_p5_resources_v1.py` est conservé ; le diff avec la version de campagne ne montre comme différences que le champ de provenance ajouté dans le JSON de sortie et les messages de progression. Les 632 mesures suivantes enregistrent explicitement le hash v1.

## 3. Résultats de ressources : médianes des ratios candidat / MLP

Un ratio inférieur à 1 favorise la sonde. Le seuil d’acceptation de la préinscription est ≤1,10 pour p50/p95 et mémoire, ≤1,25 pour temps d’entraînement.

| Variante | p50 B1 | p95 B1 | p50 B256 | p95 B256 | Temps entraînement | Pic RSS incrémental |
|---|---:|---:|---:|---:|---:|---:|
| R0 | 1.942× | 2.156× | 2.739× | 2.244× | 1.478× | 1.650× |
| C2 | 1.948× | 2.150× | 2.863× | 2.334× | 1.507× | 1.509× |
| C3 | 2.102× | 2.112× | 3.133× | 2.770× | 1.411× | 1.550× |
| C4 | 2.464× | 2.551× | 3.359× | 2.856× | 1.611× | 1.558× |

### Nombre de paires respectant les seuils

| Variante | B1 p50 ≤1,10 | B1 p95 ≤1,10 | B256 p50 ≤1,10 | Entraînement ≤1,25 | Mémoire ≤1,10 | B1 p50 plus rapide |
|---|---:|---:|---:|---:|---:|---:|
| R0 | 0/80 | 8/80 | 0/80 | 20/80 | 0/80 | 0/80 |
| C2 | 0/80 | 10/80 | 0/80 | 17/80 | 0/80 | 0/80 |
| C3 | 0/80 | 7/80 | 0/80 | 31/80 | 0/80 | 0/80 |
| C4 | 0/80 | 4/80 | 0/80 | 14/80 | 0/80 | 0/80 |

**Constat principal :** aucune variante ne gagne en p50 batch 1 dans les 80 paires, et les ratios médians de latence sont entre 1,94× et 2,46× au batch 1, puis 2,74× à 3,36× au batch 256. Les temps d’entraînement reconstruits sont 1,41× à 1,61× ; la hausse médiane de RSS est 1,51× à 1,65×. Aucune variante ne satisfait le seuil mémoire sur les 80 paires. Les gains de paramètres à égalité ne se traduisent donc pas ici par un gain d’exécution.

## 4. Qualité de validation — synthèse sans mélange des tâches

Les différences sont calculées `candidate − MLP`; pour NMAE/log-loss, une valeur négative favorise le candidat. Pour accuracy, une valeur positive favorise le candidat. Les tableaux exhaustifs par tâche/régime et par graine sont fournis en CSV.

Exemples de résultats :
- `f2_mul`, interpolation : C2 a un delta NMAE moyen de −0,0497 (7/10 graines gagnantes), mais son intervalle t à 95 % [−0,1207 ; +0,0212] inclut zéro.
- `f2_mul`, extrapolation : tous les candidats perdent en moyenne ; deltas NMAE R0 +0,4243, C2 +0,5606, C3 +0,3707, C4 +0,4864.
- `f4_sin_product`, interpolation : tous les candidats affichent une amélioration moyenne (R0 −0,0477 ; C2 −0,0470 ; C3 −0,0061 ; C4 −0,0384), avec des intervalles qui excluent zéro pour R0, C2 et C4.
- `tabular_nonlinear_binary`, log-loss interpolation : R0 +0,0197 ; C2 +0,0116 ; C3 +0,0124 ; C4 +0,0202. Les quatre dépassent le seuil de dégradation +0,01, en moyenne.

| Variante | Groupes qualité dans seuil | Groupes hors seuil |
|---|---:|---:|
| R0 | 18/29 | 11/29 |
| C2 | 21/29 | 8/29 |
| C3 | 20/29 | 9/29 |
| C4 | 18/29 | 11/29 |

Ces comptes appliquent les marges préenregistrées aux moyennes appariées des 10 graines par tâche/régime : NMAE delta ≤+0,02 ; accuracy delta ≥−0,005 ; log-loss delta ≤+0,01. Les comptes ne remplacent pas l’examen des intervalles et ne sont pas des tests confirmatoires.

## 5. Pareto par tâche

`P5_PARETO_FRONTIER_BY_TASK.csv` calcule une frontière séparée pour chaque tâche, sans agréger des unités de qualité différentes entre domaines. Les axes minimisés sont la qualité primaire d’interpolation, la qualité secondaire extrapolation (ou shift en classification), la latence p50 batch 1, le temps d’entraînement reconstruit et le pic RSS incrémental. Le nombre de paramètres est présenté mais n’est pas un objectif Pareto puisque la comparaison EX12 est à budget entraînable égal.

## 6. Limites et conclusion de phase

- Plateforme uniquement CPU, sans GPU disponible ; résultats de latence non généralisables à d’autres matériels.
- La variabilité de queue est importante ; tous les p95/p99 et toutes les observations brutes sont conservés, sans suppression d’outliers.
- Le temps d’entraînement est reconstruit à partir de composants distincts et non chronométré dans une seule fenêtre continue.
- Pas de mesure d’énergie ; aucune estimation logicielle n’est substituée à une mesure physique.
- Aucune donnée test/holdout n’a été consultée. Ces résultats restent exploratoires et la sélection confirmatoire demeure à venir.

**Verdict P5 :** porte PASS pour complétude et reproductibilité des mesures ; **aucune variante HC-RBF ne satisfait les objectifs d’efficacité face au MLP sur la plateforme testée**. Les résultats ne justifient donc pas une revendication d’efficacité supérieure. Les améliorations de qualité restent dépendantes de la tâche et ne compensent pas les surcoûts observés. Le travail poursuit en P6 pour falsifier/étudier la complémentarité et les contributions locales, pas pour supposer qu’elles existent.

## 7. Fichiers de preuve

- `08_benchmarks/P5/P5_RUN_RESOURCE_REGISTRY.jsonl`
- `08_benchmarks/P5/P5_LATENCY_RAW.csv`
- `08_benchmarks/P5/P5_MODEL_RESOURCE_SUMMARY.csv`
- `09_analysis/P5/P5_PAIRED_RESOURCE_COMPARISONS.csv`
- `09_analysis/P5/P5_RESOURCE_AGGREGATES_BY_TASK_BATCH.csv`
- `09_analysis/P5/P5_RESOURCE_AGGREGATES_BY_VARIANT.csv`
- `09_analysis/P5/P5_PAIRED_QUALITY_BY_SEED.csv`
- `09_analysis/P5/P5_QUALITY_AGGREGATES_BY_TASK_REGIME.csv`
- `09_analysis/P5/P5_PARETO_FRONTIER_BY_TASK.csv`
- `09_analysis/P5/P5_RECONCILIATION_AUDIT.json`
- `04_code/benchmark_p5_resources_v1.py` et `04_code/analyze_p5.py`, `04_code/finalize_p5.py`
- `03_design/P5/P5_RESOURCE_PREREGISTRATION.json`
