# PILOT_EXECUTION_NOTES_EX6

**Nature : note rétrospective des pilotes. Ces essais sont descriptifs et historiques, non confirmatoires.**

## 1. Environnement

- Date d'exécution : 2026-10-31.
- Système : Linux 6.18.57 x86_64.
- CPU visible : AMD EPYC 9V74 80-Core Processor, 3 CPU logiques/physiques exposés au processus.
- RAM totale rapportée : 6,24 GB.
- Python 3.13.5 ; PyTorch 2.10.0+cpu ; scikit-learn 1.8.0.
- CUDA/GPU : indisponible ; toutes les mesures sont CPU.
- Thread PyTorch fixé à 1 pendant les mesures.
- Dataset : Wisconsin Diagnostic, split historique EX4 v009 : train 341, validation 85, adaptation 57, test historique 86.
- Graines : 1501, 1607, 1717, 2029, 3037.
- Les métriques prédictives rapportées ici concernent la validation de développement, pas le test.

Le chargeur utilise `sklearn.load_breast_cancer()` qui matérialise l'ensemble du dataset en mémoire avant de sélectionner les indices autorisés ; les identifiants des lignes test sont consultés pour le contrôle de disjonction. Les lignes test n'ont pas été fournies aux transformations, entraînements, sélections, prédictions ou métriques, mais l'isolation physique stricte demandée par EX6 n'est pas démontrée. En outre, le dataset et ses partitions sont historiquement exposés. Cela interdit toute revendication confirmatoire.

## 2. Contrôle de recalcul

62 jeux de prédictions enregistrés (candidates et MLP matched/ge4x) ont été relus et leurs accuracy/log-loss recalculées indépendamment. Écart maximal :
- accuracy : 0 ;
- log-loss : 8,46e-9.

Les fichiers portent `test_partition_accessed=false`. Ce drapeau est un contrôle de l'appel du script ; il ne neutralise pas l'exposition historique du dataset ni la matérialisation du dataset source complet par le chargeur.

## 3. Replica

Point de départ : modèle OOF adaptatif historique, `P_total` source 1 160. Le pilote duplique le modèle ; le primaire calcule les folds [0,1,2] et le duplicata figé [3,4], sorties fusionnées en 3/5 et 2/5. La copie est `requires_grad=False`, exclue de l'optimiseur et ne reçoit aucun `optimizer.step()`. C'est un pilote d'inférence avec clone figé, pas une méthode de co-entraînement.

Comptage complet de la candidate dupliquée : 2 260 paramètres ; comparateur MLP-ge4x : 9 071, ratio 4,0137. La comparaison MLP-ge4x a été réajustée au modèle dupliqué, pas au modèle source.

Moyennes de cinq graines :
- candidate : accuracy 97,647 %, log-loss 0,05218 ;
- MLP-ge4x : accuracy 98,588 %, log-loss 0,05041 ;
- p50 batch 1 sériel : 0,3508 ms ; exécution « parallèle » : 1,0936 ms ; référence primaire : 0,4031 ms ;
- MLP-ge4x p50 batch 1 : 0,01516 ms ;
- entraînement historique du primaire : 2,138 s en moyenne ; MLP-ge4x : 0,2515 s.
- temps d'entraînement propre à Replica : **NON MESURÉ** (la copie est une copie inférence-only après entraînement).

Sur cinq graines, l'écart maximal primaire/clône est 9,54e-7 sur les logits ; l'écart maximal annoncé entre probabilités recalculées et référence archivée est 1,19e-7. Il s'agit d'une parité numérique à tolérance flottante, pas d'une identité bit à bit. La duplication n'a pas réduit le travail arithmétique total ; elle a partitionné les experts. Le parallélisme CPU testé est plus lent. La latence sérielle reste environ 23,1 fois celle du MLP-ge4x.

## 4. Emplica simple — pile hétérogène de 7 couches × 5 sondes

Les 7 couches contiennent 5 sondes chacune (35 au total), avec un bras hétérogène de variantes adaptatives/fixes/MIXA/gates. Les sorties sont propagées dans une pile résiduelle avec entraînement conjoint du modèle. Ce pilote ne constitue pas une comparaison complète des bras homogène et spécialiste avec sélection imbriquée ; ces derniers sont traités séparément ou restent à faire selon le cas.

Moyennes cinq graines :
- `P_total` sonde 7 010 ; MLP-ge4x 28 046 ; ratio 4,00086 ;
- accuracy 98,353 % vs 98,588 % ;
- log-loss 0,04597 vs 0,04429 ;
- fit candidat 1,849 s vs 0,309 s (5,98× plus lent) ;
- p50 batch 1 candidat 1,842 ms vs 0,01859 ms (99,1× plus lent).

Le ratio de paramètres est passé ; les mesures de vitesse ne passent pas. La qualité est légèrement inférieure aux valeurs ponctuelles du MLP-ge4x ; aucune marge de non-infériorité n'ayant été pré-enregistrée, aucune NI ne peut être revendiquée.

## 5. Emplica Orchestra — couche externe scalar gate, couches hétérogènes

Le pilote comporte 7 couches hétérogènes et un gain externe scalaire appris par couche (`sigmoid(psi_l)`). Chaque couche possède sa structure interne locale/global-gate. C'est une première approximation du schéma utilisateur, pas sa réalisation complète : le gate externe n'est pas conditionné par X ; la correction OOF inter-couches n'est pas implémentée ; le bras spécialiste et toutes les ablations ne sont pas exécutés.

Moyennes cinq graines :
- `P_total` sonde 7 017 ; MLP-ge4x 28 079 ; ratio 4,00157 ;
- accuracy 97,647 % vs 98,824 % ;
- log-loss 0,05892 vs 0,04464 ;
- fit candidat 1,745 s vs 0,309 s (5,65× plus lent) ;
- p50 batch 1 candidat 1,920 ms vs 0,01856 ms (103,4× plus lent).

Les gates ont été apprises et toutes sont non-nulles sur l'exemple inspecté ; ce n'est pas une preuve de spécialisation fonctionnelle ni de généralisation.

### Early exit diagnostique

Sur la seule graine 1501, des seuils de confiance ont été balayés sur la validation déjà utilisée en développement. À seuil 0,98 : 6,47 couches en moyenne, accuracy 97,65 %, log-loss 0,05628, p50 batch1 1,535 ms. Le chemin complet de cette graine était environ 1,761 ms p50. Le gain de latence est faible ; la log-loss se dégrade ; la candidate reste très lente face au MLP. Les seuils ont été choisis sur le même ensemble de validation : résultats purement exploratoires, pas preuve d'une politique de cascade généralisable.

## 6. Orchestra homogène — mêmes 5 MIXA global-gate experts par couche

Pilote : 7 couches, chacune construite avec la même variante MIXA global-gate. Coordination externe scalaire. Cinq graines.

Moyennes :
- `P_total` 6 712 ; MLP-ge4x 26 858 ; ratio 4,00149 ;
- accuracy 97,647 % vs 98,824 % ;
- log-loss 0,07021 vs 0,04621 ;
- fit 1,549 s vs 0,252 s (6,13× plus lent) ;
- p50 batch1 1,676 ms vs 0,01828 ms (91,7× plus lent).

Le bras homogène n'est pas un « meilleur modèle homogène » choisi par validation imbriquée ; il constitue un seul pilote contrôlé avec une variante connue.

## 7. Éléments non exécutés ou non mesurés

- Replica pendant l'entraînement, règles de gradient et gain de convergence.
- Partition interne complète des calculs d'une même sonde, contrôle parallèle sans duplication et mesures énergie.
- Emplica `EMP_HOMO_BEST` avec sélection imbriquée, `EMP_LAYER_SPECIALIST`, recherche d'allocation, OOF inter-couches.
- Orchestra `ORCH_SPECIALIST`, gate externe conditionné par X, gate statique pré-enregistré, correction d'erreurs OOF inter-couches, cascade validée sur données indépendantes, toutes les ablations.
- Domaines/datasets externes non exposés.
- Temps bout en bout complet incluant toutes préparations/charges/initialisations pour chaque configuration.
- RSS de pointe cohérent, mémoire activation, VRAM, énergie/joules, p99 fiable, tailles batch 256 et profils déploiement.
- Marges NI pré-enregistrées et inférence statistique confirmatoire.
- Généralisation inter-domaines et test externe vierge.

## 8. Provenance du code d'exécution

Les résultats des premières campagnes ont été produits par des cellules interactives de la session (les principales cellules de construction, entraînement, Replica, Orchestra homogène, early exit et audit sont conservées dans `logs/pilot_execution_trace_cells.md`). Les scripts autonomes visibles dans `src/` ont été sauvegardés/ajustés après la génération des premiers fichiers de résultats. Ils sont des supports de reprise et de reproduction prospective, mais leur SHA-256 ne peut pas être présenté comme le hash exact du code chargé au moment de chaque run. L'identité exacte code-run est donc **NON VÉRIFIÉE** pour cette campagne initiale. Toute nouvelle campagne doit utiliser les scripts versionnés actuels, inscrire le hash de code/config dans chaque run et écrire sous un nouvel ID.

## 9. Lecture honnête

Tous les bras testés passent le ratio `P_MLP/P_sonde >= 4` par leur MLP-ge4x correspondant. Aucun ne démontre une accélération : les trois Emplica/Orchestra sont beaucoup plus lents sur le CPU mesuré ; Replica parallèle est lui aussi plus lent, et Replica sériel reste très loin du MLP. Les qualités ponctuelles sont légèrement ou nettement inférieures aux MLP-ge4x selon les bras. Les résultats ne satisfont donc pas le succès global. L'état honnête de la campagne est `INCOMPLET`.
