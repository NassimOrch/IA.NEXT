# Rapport P3 — tâches, généralisation et criblage multi-graines

**Expérience :** EX12_NEXT_0  
**Statut :** campagne exploratoire terminée ; aucun accès au test ni au holdout  
**Pré-enregistrement :** `03_design/P3/P3_PREREGISTRATION.json`  
**Plan gelé :** `03_design/P3/P3_VARIANT_PLAN.json`

## 1. Périmètre et statut

La campagne couvre 8 tâches, 10 graines pilotes, 6 slots de modèles et 480 runs logiques : 4 fonctions principales, 2 fonctions de composition diagnostiques, 1 jeu tabulaire de régression (Diabetes, train/validation uniquement) et 1 classification binaire synthétique. Les régimes de régression sont interpolation, frontière, extrapolation et shift ; la classification comprend interpolation et shift. Les tâches g5/g6 sont diagnostiques et n’ont pas servi à la sélection des checkpoints ou hyperparamètres.

Le registre append-only comporte 493 tentatives : 480 succès logiques, 13 tentatives initiales échouées et aucune interruption non résolue. Les 13 échecs initiaux proviennent d’un défaut de l’audit de couverture (`xv[0]` transmis au lieu du batch `xv`) après calcul/entraînement ; la version fautive, les logs et les statuts sont conservés. Les reprises réussies sont des tentatives distinctes.

## 2. Intégrité et traçabilité

- 71 fichiers de données et 664 arrays vérifiés ; aucun écart de hash, shape ou dtype.
- 480 configurations logiques uniques exécutées ; 2 400 fichiers de run vérifiés par hash.
- 1 620 couples prédiction/vérité terrain audités et 1 620 métriques recalculées.
- 320 paires de budgets de paramètres vérifiées.
- 22 contrôles unitaires du pipeline réussis lors de l’exécution directe de `04_code/test_p3_pipeline.py`.
- Les scripts cités dans les métadonnées des runs ont tous une version exacte retrouvée dans `04_code/` et leurs hashes concordent (le hash historique `train_p3.py` de la première version correspond à `train_p3_v1.py`, tandis que la version corrigée correspond à `train_p3.py`).
- `test_access=NONE`, `holdout_access=NONE`.

Le fichier initial `P3_METRIC_SUMMARY.csv` ne couvrait que les métriques de régression. Pour inclure la classification sans mélanger les familles de métriques, la synthèse canonique a été reconstruite dans `P3_METRIC_SUMMARY_CANONICAL.csv` et contrôlée par `P3_SUMMARY_REBUILD_AUDIT.json`. Les intervalles des deltas appariés sont descriptifs et exploratoires ; aucune conclusion confirmatoire ou revendication de significativité n’est formulée.

## 3. Appariement des paramètres

Les 320 comparaisons candidate–MLP sont toutes dans la tolérance pré-enregistrée de ±1 % du budget total persistant. Le pire écart absolu est 0.849 %. Les maxima par variante : R0 0.679 %, C2 0.679 %, C3 0.679 %, C4 0.849 %. Le critère historique GE4X n’est pas utilisé.

## 4. Résultats de régression — moyenne sur dix graines

La métrique principale est la NMAE normalisée par l’écart-type de la cible d’entraînement ; plus bas est meilleur. Les nombres sont des moyennes descriptives sur dix graines, sans test confirmatoire.

| Tâche | MLP de référence | R0 | C2 | C3 | C4 |
|---|---:|---:|---:|---:|---:|
| f1_sin | 0.1050 | 0.1931 | 0.1891 | 0.2792 | 0.1741 |
| f2_mul | 0.0700 | 0.0276 | 0.0203 | 0.0309 | 0.0327 |
| f3_square_plus | 0.0767 | 0.0532 | 0.0427 | 0.0585 | 0.0367 |
| f4_sin_product | 0.1084 | 0.0607 | 0.0614 | 0.1061 | 0.0708 |
| g5_sin_mul_plus_square | 0.0698 | 0.0693 | 0.0677 | 0.0703 | 0.0704 |
| g6_log_quadratic_rational | 0.0285 | 0.0288 | 0.0292 | 0.0349 | 0.0286 |
| diabetes_sklearn | 0.6016 | 0.5917 | 0.5911 | 0.5981 | 0.5850 |

### Lecture par fonction

- **f1_sin :** les quatre variantes HC-RBF perdent nettement contre le MLP en interpolation ; C4 est la moins mauvaise mais ne récupère pas l’écart.
- **f2_mul :** HC-RBF gagne en interpolation ; C2 est le meilleur des candidats HC-RBF (NMAE 0,0203 contre 0,0700 pour M0_CORE). En extrapolation, les variantes HC-RBF se dégradent davantage que le MLP.
- **f3_square_plus :** R0/C2/C4 améliorent l’interpolation ; C4 atteint 0,0367 contre 0,0950 pour M0_AFFINE. L’extrapolation reste défavorable aux HC-RBF.
- **f4_sin_product :** R0/C2 gagnent contre M0_CORE en interpolation et en extrapolation dans cette configuration ; C3 est proche du MLP en interpolation.
- **g5 et g6 :** tâches secondaires et diagnostiques uniquement. g5 reste proche en interpolation, mais l’extrapolation HC-RBF est moins bonne ; g6 favorise plutôt les MLP.
- **Diabetes :** sur l’unique split train/validation (309/66), les HC-RBF ont une NMAE validation légèrement inférieure au MLP apparié. Le holdout de 67 observations demeure scellé ; aucune conclusion à son sujet n’est possible.

### Extrapolation

La dégradation hors support est nette sur plusieurs tâches. Pour `f1_sin`, M0_CORE a une NMAE extrapolation de 1,073 contre 1,267–2,135 pour HC-RBF. Pour `f3_square_plus`, le MLP est à 0,967 contre 1,081–1,241. Pour g5, le MLP est à 0,725 contre 0,867–0,916. Pour g6, le MLP est à 0,212 contre 0,263–0,295. Pour `f2_mul`, les HC-RBF sont à 0,743–0,942 contre 0,382 pour le MLP. L’interpolation ne permet donc pas de conclure sur l’extrapolation.

## 5. Classification binaire synthétique

| Modèle | Accuracy interpolation | Log-loss interpolation | Accuracy shift | Log-loss shift |
|---|---:|---:|---:|---:|
| M0_CORE | 0.6747 | 0.5938 | 0.6753 | 0.6017 |
| M0_AFFINE | 0.6933 | 0.5875 | 0.6757 | 0.6057 |
| R0 | 0.6667 | 0.6135 | 0.6617 | 0.6192 |
| C2 | 0.6880 | 0.6054 | 0.6887 | 0.6032 |
| C3 | 0.6658 | 0.6125 | 0.6803 | 0.6118 |
| C4 | 0.6587 | 0.6203 | 0.6678 | 0.6180 |

Les HC-RBF ont une log-loss moins bonne que leur MLP apparié : deltas moyens +0,0197 (R0), +0,0116 (C2), +0,0187 (C3) et +0,0328 (C4). C2 améliore légèrement l’accuracy moyenne, mais la log-loss reste moins bonne. Le jeu est synthétique et ne prouve pas la performance sur un domaine externe.

## 6. Temps d’entraînement descriptifs

Les temps P3 ne sont pas des benchmarks ressources formels ; P5 doit mesurer séparément latence, mémoire, débit et coût complet. Les ratios médians candidat / MLP apparié, sur dix graines, sont :

| Tâche | R0 | C2 | C3 | C4 |
|---|---:|---:|---:|---:|
| diabetes_sklearn | 1.97× | 1.75× | 1.75× | 3.21× |
| f1_sin | 1.13× | 0.99× | 1.06× | 1.53× |
| f2_mul | 1.13× | 1.88× | 1.06× | 1.28× |
| f3_square_plus | 1.72× | 1.67× | 1.70× | 1.82× |
| f4_sin_product | 1.87× | 1.61× | 1.42× | 1.51× |
| g5_sin_mul_plus_square | 1.40× | 1.36× | 1.39× | 1.61× |
| g6_log_quadratic_rational | 1.48× | 1.46× | 1.50× | 1.64× |
| tabular_nonlinear_binary | 1.65× | 1.68× | 1.54× | 1.87× |

Les candidats HC-RBF sont plus lents à entraîner dans la plupart des tâches ; quelques exceptions locales existent, mais ne forment pas un avantage stable. P3 ne permet donc pas de revendiquer un gain de ressources.

## 7. Limites et décision

1. P3 est exploratoire, pas confirmatoire. Les dix graines ne correspondent pas à dix jeux externes indépendants ; Diabetes conserve un seul split de petit échantillon.
2. UCI Adult n’a pas été téléchargé (échec DNS du dépôt officiel) et aucune donnée fictive n’a été substituée.
3. Aucun test, aucun holdout, aucun holdout historique EX11 n’a été consulté.
4. L’énergie n’a pas été mesurée et les temps d’entraînement P3 sont descriptifs.
5. Les HC-RBF gagnent sur certaines fonctions et perdent sur d’autres ; les MLP restent meilleurs sur f1_sin et sur la log-loss de classification.
6. Le surcoût d’entraînement reste une difficulté prioritaire.

**Décision P3 : PASS pour la couverture tâches/généralisation exploratoire et l’intégrité des données.** P4 peut maintenant auditer formellement l’appariement MLP. Aucun verdict de supériorité générale n’est autorisé.

## 8. Artefacts de reproduction

- Données : `02_data/P3_pilot/`
- Pré-enregistrement et variante : `03_design/P3/P3_PREREGISTRATION.json`, `P3_VARIANT_PLAN.json`
- Générateur : `04_code/generate_p3_data_v1.py`
- Entraîneur exact corrigé : `04_code/train_p3.py` ; première version fautive : `04_code/train_p3_v1.py`
- Modèles et kernels : `04_code/ex12_models.py`, `04_code/hc_kernels.py`
- Audits : `04_code/audit_p3.py`, `04_code/verify_p3_data.py`
- Résumés : `04_code/summarize_p3.py`
- Registre : `00_governance/P3_RUN_REGISTRY.jsonl`
- Runs complets : `06_runs/P3/`
- Recalcul : `09_analysis/P3/P3_FULL_INTEGRITY_AUDIT.json`, `P3_PER_SEED_METRICS.csv`, `P3_PAIRED_COMPARISONS.csv`, `P3_PAIRED_COMPARISONS_WITH_CI.csv`, `P3_METRIC_SUMMARY_CANONICAL.csv`
