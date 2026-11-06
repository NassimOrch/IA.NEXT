# Rapport technique EX4 — protocole, implémentation et résultats

## 1. Provenance et reconstruction

L'archive originale `last_sources.zip` et ses ZIP imbriqués ont passé les tests d'intégrité ZIP. Les SHA-256 sont regroupés dans `inputs/source_manifest.json`; `inputs/archive_integrity.json` conserve les résultats `testzip`. Les sources originales ne sont pas modifiées.

La candidate de référence EX2 identifiée dans le workspace archivé est `latent_d16_k32_maturation`, versions v009/v007. Elle sert de point de départ. La campagne EX4 a été codée séparément sous `sondes_research_workspace_ex4/versions/`.

Le workspace EX3 complet, les scripts, checkpoints, prédictions et tableaux bruts ne figurent pas dans l'archive. La récupération de `debrit_0.txt` est décrite séparément et conserve les valeurs EX3 au statut `rapporté_non_vérifiable`.

## 2. Données et partition

Dataset : `sklearn.datasets.load_breast_cancer` (Wisconsin Diagnostic), 569 observations et 30 caractéristiques. Partition reprise du ledger EX2 v009 : train 341, validation 85, adaptation 57, test 86 ; intersections nulles. Le scaler est ajusté sur train seulement. L'adaptation est utilisée comme contrôleur de plateau sans rétropropagation.

**Précision d'accès au test :** l'API sklearn fournit le tableau source complet ; le chargeur matérialise donc `data` et `target` complets en mémoire. Le code construit ensuite `used_rows = train ∪ validation ∪ adaptation`, n'indexe que ces lignes, ajuste/transfère le scaler sur ces lignes et ne passe aucune valeur test au modèle. Les IDs test sont conservés uniquement dans le ledger d'intégrité. Dire « test non utilisé par la modélisation » est exact ; dire « les valeurs test n'ont jamais été chargées dans le processus » serait excessif. Le dataset et ses partitions sont de toute façon historiquement exposés dans EX2.

## 3. Architectures

### 3.1 Expert RBF latent

Chaque expert comprend un encodeur linéaire vers une dimension `d` suivi de `tanh`, des centres RBF `k`, des largeurs apprenables, une tête linéaire et un biais. Les centres/largeurs sont initialisés à partir des seules représentations train avec KMeans ; les experts disposent d'optimiseurs locaux.

### 3.2 Coordination

Les poids globaux sont interpolés :

`w_i(alpha) = (1-alpha)/N + alpha * softmax(phi)_i`.

Contrôles : `none`, `immediate`, `linear`, `maturation_adaptctl`, `retro_adaptctl`, `retro_linear`. La règle d'observation v005/v006 utilise la log-loss adaptation avec patience de cinq observations sans amélioration d'au moins 1e-5 pour ajouter un expert en mode growth ; une fois la capacité max atteinte, une autre période de plateau peut déclencher alpha. Correction issue de l'audit des traces complètes : `maturation_adaptctl` et `retro_adaptctl` atteignent le plateau sur 5/5 seeds d4/k8 (epochs 30, 51, 33, 34, 33), mais toujours après le meilleur checkpoint validation (epochs 20, 28, 21, 26, 25). Le checkpoint choisi a donc `alpha=0` et, pour RETRO, `beta_local=1` ; les métriques reportées ne mesurent pas le comportement mûri. `mixa_micro_d4_k8_adaptctl` atteint également le trigger sur 5/5 seeds après le meilleur checkpoint (epochs 30, 51, 33, 34, 33). `retro_linear` impose dès le début une rampe alpha et beta inverse et ses traces montrent effectivement beta décroissant jusqu'à zéro.

### 3.3 Croissance dynamique

Les variantes `growth` commencent réellement avec un seul expert. Un module supplémentaire est instancié uniquement lorsqu'un plateau du contrôleur adaptation survient. Au checkpoint de validation choisi, les experts au-delà du meilleur `active_count` sont supprimés. Le compte P_total reflète ce graphe déployé, non la capacité maximale théorique.

### 3.4 MIXA

MIXA combine quatre experts adaptatifs d4/k8, une branche RBF fixe (projection, centres et largeurs calculés sur train, enregistrés en buffers), et une porte linéaire à deux sorties. Les états fixes sont inclus dans le modèle. Les ratios sont calculés après ajout du prétraitement partagé.

## 4. Comptage des paramètres et comparateurs MLP

Le `P_total_model_only` compte tous les tensors flottants persistants de `state_dict` et le coefficient de calendrier alpha. L'audit final a ajouté les 60 paramètres numériques du prétraitement commun : 30 moyennes + 30 échelles du StandardScaler. Les ratios principaux sont donc calculés comme :

`P_total_complet = P_total_model_only + 60`

La même charge de prétraitement est ajoutée au MLP et à la sonde. Pour satisfaire le vrai seuil `P_MLP_total / P_sonde_total >= 4`, le MLP-ge4x a été redimensionné à partir du compte complet, seed par seed. 50 nouveaux MLP de largeur correspondante ont été entraînés ; les runs sondes et anciens MLP sont préservés.

Les fichiers de comparaison v006 distinguent `ratio_total_model_only` et `ratio_total` (incluant le scaler). Tous les 60 comparateurs MLP-ge4x passent le ratio ajusté ; la moyenne famille se situe entre 4,0058× et 4,0674×.

La taille du checkpoint PyTorch `state_dict` est mesurée séparément. Les 480 octets de données numériques minimales du scaler sont publiés comme dépendance partagée ; le fichier `.npz` du scaler a également été sauvegardé dans `data_manifest/`.

## 5. Procédure d'entraînement et métriques

Cinq seeds d'initialisation : 1501, 1607, 1717, 2029, 3037. Split seed fixe : 20261035 (ledger EX2 v009). Sélection/arrêt par log-loss validation, patience 30, diminution de LR à 10 et 20 epochs de stagnation, sans plafond d'époque dur. Les mêmes critères de sélection sont appliqués aux MLP.

Métriques : accuracy, macro-F1, balanced accuracy, ROC-AUC, Brier, ECE 10 bins, log-loss. La latence batch 1 est chronométrée après 20 échauffements et 100 répétitions sur CPU, en un thread ; le médian et p95 sont consignés. `train_seconds` couvre la boucle de fit et ses évaluations validation/adaptation, pas uniquement la rétropropagation.

Important : les mêmes données validation servent à choisir le checkpoint et à rapporter les métriques finales. Les scores sont donc développement/validation et peuvent être optimistes. Pas de test final, pas d'IC de non-infériorité, pas de correction multiple, ni de validation multi-domaines dans v006.

## 6. Résultats appariés MLP-ge4x

Résumé des moyennes sur cinq graines ; métriques non pondérées entre seeds :

| Sonde | P_sonde complet | P_MLP complet | Ratio | Acc sonde | Acc MLP | LL sonde | LL MLP | Fit sonde (s) | Fit MLP (s) | Lat méd sonde (ms) | Lat méd MLP (ms) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| d2/k4 growth | 146 | 590 | 4,041 | 0,97882 | 0,97882 | 0,07868 | 0,05552 | 0,358 | 0,286 | 0,07588 | 0,01377 |
| d4/k8 growth | 463,6 | 1 863,8 | 4,018 | 0,97647 | 0,98118 | 0,07791 | 0,05296 | 0,491 | 0,240 | 0,12639 | 0,01398 |
| d8/k4 growth | 356 | 1 448 | 4,067 | 0,97647 | 0,97647 | 0,05952 | 0,05394 | 0,352 | 0,263 | 0,07432 | 0,01390 |
| d4/k16 growth | 443,4 | 1 791,2 | 4,046 | 0,97647 | 0,97882 | 0,06593 | 0,05341 | 0,408 | 0,242 | 0,09725 | 0,01400 |
| d4/k8 maturation | 793 | 3 197 | 4,032 | 0,96706 | 0,98588 | 0,08199 | 0,05057 | 0,550 | 0,210 | 0,20263 | 0,01418 |
| d4/k8 RETRO linear | 793 | 3 197 | 4,032 | 0,96941 | 0,98588 | 0,09493 | 0,05057 | 4,608 | 0,210 | 0,20188 | 0,01418 |
| MIXA d4/k8 | 1 037 | 4 154 | 4,006 | 0,97412 | 0,98118 | 0,09153 | 0,05175 | 0,664 | 0,235 | 0,26547 | 0,01447 |
| d16/k32 baseline | 4 489 | 17 981 | 4,006 | 0,97647 | 0,98824 | 0,07710 | 0,04531 | 0,463 | 0,243 | 0,21094 | 0,01717 |

Les valeurs complètes, par seed, sont dans `results/processed/ex4_paired_comparison_per_seed.csv` et `ex4_paired_comparison_summary.csv`.

## 7. Tests d'intégrité

Le script `tests/test_ex4_integrity.py` est passé. Il vérifie :
- 60 lignes de métriques sonde (12 familles × 5 seeds), 135 MLP uniques et les fichiers de prédictions correspondants ;
- parsing JSONL et recalcul accuracy/log-loss/macro-F1/balanced accuracy depuis les prédictions brutes ;
- formules paramétriques pour les graphes réellement déployés ;
- ratios MLP-ge4x incluant les 60 paramètres du scaler ;
- partitions disjointes, scaler fit sur train, et manifeste d'accès au test.

Sortie : `PASS: JSONL, raw-prediction metrics, parameter counts, per-seed MLP>=4x, partitions and pair table.`

## 8. Ressources mesurées et non mesurées

Mesurées : temps fit (avec validation/adaptation périodiques), latence batch 1 médiane/p95, taille `state_dict`, compte de paramètres, taille minimale du scaler. Environnement : Python 3.13.5, PyTorch 2.10.0+cpu, NumPy 2.3.5, scikit-learn 1.8.0, 1 thread PyTorch, CPU seulement ; `platform.processor()` retourne une chaîne vide et `os.cpu_count()` annonce 3 CPUs logiques disponibles.

Non mesurées : FLOPs/MACs complets, RSS maximum, VRAM, débit multi-batch, énergie, coût total du tuning/recherche, mesure de puissance et profilage détaillé des coûts de prétraitement. Par conséquent, aucune conclusion de conformité complète aux ressources n'est possible. La latence mesurée est beaucoup plus élevée pour toutes les sondes étudiées.

## 9. Déviations et statut

- v001–v003 ont appliqué `transform` à une matrice entière avant la sélection du sous-ensemble ; bien que le scaler ait été fit sur train et que les labels test n'aient pas servi aux métriques, ce flux ne constitue pas une isolation test stricte.
- v003–v004 pré-allouaient des experts non actifs pour les variantes growth ; P_total pouvait donc compter une capacité dormante. Ces versions sont conservées comme traces d'audit, pas comme comparaisons finales.
- v005 a corrigé la croissance dynamique mais omettait le scaler commun dans les ratios : elle est conservée comme campagne intermédiaire.
- v006 réutilise les sondes et refait uniquement les MLP nécessaires après correction du P_total partagé ; aucun entraînement sonde n'a été répété.
- Les comparaisons sont descriptives sur un seul dataset historique, et le workspace EX3 original est absent.

## 10. Reproduction

Depuis le dossier de version v006 :

```bash
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
python src/ex4_micro_benchmark.py --seeds 1501 1607 1717 2029 3037
python tests/test_ex4_integrity.py
```

Le script est idempotent sur les couples `(model_id, model_seed)` déjà enregistrés ; il ne doit pas écraser les sources. Pour reproduire exactement les MLP de v006, le code calcule le dimensionnement ge4x en incluant le scaler partagé.

## 11. Étape scientifique suivante

La piste recommandée à tester sur un domaine réellement indépendant est `micro_d8_k4_growth_adaptctl`, avec une validation séparée de sélection/calibration, un comparateur MLP compétitif, les coûts FLOPs/MAC/RSS et une vraie procédure de non-infériorité sur accuracy et log-loss. Il faut aussi régler le contrôleur pour que la maturation/RETRO s'active dans des conditions pré-enregistrées avant de prétendre évaluer leur mécanisme. Cette recommandation est une priorité expérimentale, pas un statut de gagnant.


---

# 12. Suite d'audit et versionnage v007–v009

## 12.1 Intégrité des campagnes précédentes
Les tests automatiques v005 et v006 ont été relancés sans entraînement : PASS dans les deux cas. v005 confirme 60 runs sonde, 85 MLP et 120 comparaisons appariées ; v006 confirme 60 runs sonde, 135 MLP et 120 comparaisons, dont 60 ge4x. Le test original v007 échoue avec `Expected 14 candidates x 5 seeds, got 95` : le registre contient 70 runs de la campagne 14×5 initiale plus 25 runs de l'add-on micro-MIXA. Ce résultat de test n'est pas masqué ; les campagnes sont séparées par sélection/audit dans v007/v008. Le filtre de récupération initiale retourne `PASS_FILTERED_ORIGINAL_CANDIDATES`, le filtre micro-MIXA v008 retourne `PASS_FILTERED_MICRO_MIXA_RECOVERY`. Voir `AUDIT_V007_MIXED_REGISTRY.md`.

## 12.2 Micro-MIXA récupérée
La reconstruction combine un expert adaptatif d4/k8 et un RBF fixe d4/k8, plus mélange égal, porte globale ou porte conditionnelle. Les résultats complets, paramètres, coûts et limites sont dans `rapport_micro_mixa_ex4.md`. L'audit v008 recalculé confirme 25 sondes, 30 MLP distincts, 50 couples, ratios ge4x ≥4,01878×, et absence d'accès au test Wisconsin. Il repère aussi une métadonnée générique erronée `adaptation_partition_used_for_controller=true`; le code micro-Hybrid n'indexe pas la partition adaptation. Les données sources sont conservées et l'interprétation corrigée est jointe à l'audit, sans réécriture des registres bruts.

# 13. Transfert Iris v009

## 13.1 Provenance et données
`sklearn.datasets.load_iris` fournit 150 observations, quatre variables, trois classes. La documentation scikit-learn indique qu'il s'agit d'une variante alignée sur le jeu R et qu'elle diffère de l'archive UCI sur deux observations. Le snapshot CSV/NPZ exact, la table d'index par partition et le scaler train-only sont enregistrés et hashés. Les partitions sont 90/20/10/30 ; les seeds de modèle sont 1501, 1607, 1717, 2029, 3037. L'adaptation de 10 observations est réservée, mais n'est pas utilisée par le chemin `MicroHybrid` (aucun contrôleur adaptation pour ce bras).

## 13.2 Bras et dimensionnement
Quatre candidates préenregistrées : `micro_adaptive_single_d4_k8`, `micro_mixa_equal_d4_k8`, `micro_mixa_global_gate_d4_k8`, `micro_mixa_input_gate_d4_k8`. La branche `fixed_only` a déjà été testée sur Wisconsin ; le pré-vol Iris a commencé deux initialisations puis a été interrompu avant la complétion de la campagne. Ces deux états ont été déplacés dans `results/models/quarantine_unscored/` et ne figurent dans aucune métrique. Les trois MIXA et les MLP ont été exécutés par écritures JSONL incrémentales. Les cinq adaptatifs ont été restaurés depuis leurs checkpoints complets du pré-vol ; les métriques et les latences ont été recalculées, mais les temps d'entraînement et historiques non sauvegardés sont ND.

MLP ge4x dimensionnés sur P_total incluant les 8 coefficients numériques du StandardScaler :

| Candidate | P sonde total | MLP ge4 P total | Ratio | Largeur MLP |
|---|---:|---:|---:|---:|
| Adaptative seule | 95 | 387 | 4,0737× | 47 |
| Mélange égal | 182 | 731 | 4,0165× | 90 |
| Gate global | 184 | 739 | 4,0163× | 91 |
| Gate entrée | 192 | 771 | 4,0156× | 95 |

L'audit vérifie les ratios pour chaque graine ; minimum validation et test : 4,015625×. Quarante MLP uniques couvrent les comparateurs matched et ge4x.

## 13.3 Résultats test descriptifs

| Candidate | Accuracy sonde | Accuracy MLP ge4x | Log-loss sonde | Log-loss MLP ge4x |
|---|---:|---:|---:|---:|
| Adaptative seule | 0,9533 | 0,9667 | 0,16466 | 0,09761 |
| MIXA mélange égal | 0,9600 | 0,9667 | 0,12062 | 0,09633 |
| MIXA gate global | 0,9667 | 0,9667 | 0,14282 | 0,09331 |
| MIXA gate conditionnel | 0,9667 | 0,9667 | 0,17272 | 0,09420 |

Chaque valeur est la moyenne sur cinq initialisations évaluées sur les mêmes 30 observations de test. Les seeds ne créent pas 150 cas indépendants. La meilleure accuracy MIXA égale celle du MLP ge4x, mais aucune variante n'égale la log-loss moyenne du MLP. Le test n'a pas servi à sélectionner une candidate ni à modifier le prompt. Pas d'inférence de non-infériorité formelle sur n=30.

## 13.4 Ressources Iris

Les MACs présentés sont des estimates analytiques pour les cartes denses, réductions RBF et readouts ; ils omettent exp/tanh, élémentaires, optimiseur et surcoûts Python, et ne sont pas des mesures hardware. La latence batch 1 est mesurée sur CPU. Pour les MIXA :

| Candidate | Fit sonde (s) | Fit MLP ge4x (s) | Latence médiane sonde/MLP (ms) | MAC sonde/MLP | Octets état + scaler sonde/MLP |
|---|---:|---:|---:|---:|---:|
| Adaptative | ND | 0,337 | 0,03890 / 0,01384 | 72 / 329 | 3 221 / 3 933 |
| Equal | 1,625 | 0,275 | 0,08059 / 0,01411 | 144 / 630 | 4 991 / 5 341 |
| Gate global | 1,344 | 0,258 | 0,08921 / 0,01468 | 146 / 637 | 5 372 / 5 405 |
| Gate entrée | 2,280 | 0,260 | 0,08966 / 0,01410 | 152 / 665 | 5 561 / 5 469 |

La latence sonde MIXA est environ 5,5 à 6,4 fois celle du MLP. Le temps fit est environ 5,2 à 8,8 fois plus long pour les trois MIXA entraînés ; la candidate adaptative n'a pas de temps récupérable. Le gate entrée dépasse le MLP en taille sérialisée combinée de quelques octets. Le gain MAC analytique ne se traduit donc pas par une efficacité globale. La VRAM et l'énergie ne sont pas mesurées ; le RSS est global au processus.

## 13.5 Respect du gel et limite d'isolation
Le journal confirme `FREEZE COMPLETE` avant la première sélection de `Xsrc[test]` et les métriques test. Le préfixe du code, le config, le manifeste et le scaler sont hashés dans `ex4_iris_freeze_manifest.json`; une copie exacte du manifeste pré-gel est `ex4_iris_manifest_frozen.json`. Toutefois, `load_iris()` fournit le dataset complet en mémoire avant séparation, le vecteur des étiquettes est utilisé par le splitteur stratifié pour construire les IDs et le snapshot source complet est sauvegardé avant le gel. Les lignes test ne servent pas au scaler, au modèle, aux gradients, à l'arrêt, à la sélection ou aux métriques avant le gel ; néanmoins, l'isolation mémoire/processus absolue n'est pas respectée ni revendiquée. Cette réserve est écrite dans `ex4_iris_isolation_caveat.json`.

## 13.6 Données externes indisponibles
Les téléchargements UCI Banknote Authentication et MAGIC Gamma Telescope ont été tentés, mais le conteneur n'a pas résolu les hôtes (DNS réseau indisponible) ; les ZIP binaires n'ont pas pu être importés. Aucun run de ces datasets n'est revendiqué. Iris est donc le seul nouveau domaine local exploré ; les domaines externes multi-jeux requis pour une confirmation restent non achevés.

## 14. Audit automatique final
`versions/sondes_ex4_v009__2026-10-30/scripts/audit_iris_transfer.py` retourne `PASS_IRIS_TRANSFER_AUDIT` : 20 métriques sondes, 40 MLP, 40 comparaisons validation, 60 métriques/predictions test (20 sondes + 40 MLP), 40 comparaisons test, recalculs métriques depuis prédictions, hashes/checkpoints cohérents, splits disjoints, 2 états fixed-only quarantinés, 5 checkpoints adaptatifs récupérés sans réentraînement, ge4x min 4,015625×.
