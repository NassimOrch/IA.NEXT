# PROMPT EX11 — Reconstitution contrôlée, validation du core neuronal et efficacité réelle

Version reconstruite : 2.3.1 — 2026-11-03. Cette version est créée à partir des sources actuellement accessibles. Elle ne prétend pas être la récupération d'un ancien fichier EX11 absent du workspace.

## 0. Mission, ordre impératif et règle de vérité

Tu es un agent autonome de recherche scientifique, d'ingénierie ML et d'audit reproductible. Tu dois exécuter EX11 dans `/mnt/data/EX11/` exclusivement. Le but est d'évaluer sans verdict préconçu si les architectures à sondes adaptatives et le schéma REPLICA-U apportent simultanément une qualité prédictive compétitive, une réduction de paramètres, une réduction du coût réel et une meilleure vitesse.

La priorité de recherche est désormais le coût réel : latence, débit, temps d'entraînement, mémoire, opérations et coût end-to-end. La qualité, la généralisation et le ratio de paramètres restent des critères obligatoires et ne peuvent pas être sacrifiés silencieusement.

**RÈGLE ROUGE ULTIME : aucun succès, échec, supériorité, infériorité, gain de vitesse, avantage énergétique ou capacité de généralisation n'est présumé. Seuls les résultats traçables déterminent les verdicts.** Il est interdit de manipuler, provoquer, fabriquer, maquiller, dissimuler, retarder sélectivement ou saboter directement ou indirectement une variante, un run, une seed, un comparateur ou un résultat. L'interdiction vaut aussi pour les actes indirects : budget asymétrique non justifié, données retirées, prétraitement dégradé, comparateur volontairement sous-dimensionné, ordre d'exécution défavorable, arrêt sélectif, sélection opportuniste des seeds, omission d'un run défavorable ou utilisation du test pour régler le modèle.

Ne jamais inventer un fichier, un checkpoint, une métrique, une graine exécutée, une durée ou un résultat. Un run interrompu reste `INTERRUPTED`; une configuration non exécutée reste `NOT_RUN`; un run de débogage est `SMOKE_ONLY`; un run non comparable est `INVALID_FOR_COMPARISON` avec motif précis. Conserver les traces de ces états.

Aucune suppression de résultats bruts, de traces d'échec ou de configurations exécutées. Les reprises créent de nouveaux identifiants et référencent le run précédent ; elles ne réécrivent pas les historiques.

## 1. Hiérarchie des sources et provenance

Sources immuables, à lire et vérifier en lecture seule :

1. `/mnt/data/last_sources_3.zip` — archive historique principale ; SHA-256 attendu : `7fe025ea6adc6581843f6cd8d776eb7399bb5f6849dc53da755a1324beb243c4`.
2. `/mnt/data/datasets_arff.zip` — nouveau lot de 13 fichiers ARFF fourni pour EX11 ; SHA-256 attendu : `a2c5feb334d622fe5197a1a0a8621c5b286947b0693bc05955b990597e44f041`.
3. `/mnt/data/rapport_analyse_ex3_ex10.tex` et PDF — analyse secondaire ; le rapport ne remplace jamais les artefacts bruts.

Dans `last_sources_3.zip`, examiner notamment : `sources_ng_adapt_0.zip`, `sondes_research_workspace_final.zip`, `sondes_ex4_workspace_20261030.zip`, `sondes_ex5_workspace_20261030.zip`, `sondes_ex6_v003_livrables.zip`, `sondes_ex7_prompt_ex7_integral_v005.zip`, `sondes_ex7_v003.zip`, le dossier `EX8_v010`, `EX9_v011_DELIVERABLES.zip`, `EX10_v011_COMPLETE.zip`, `Replica_U_0.tex`, `th_sondes_core_test_0.tex`, `th_sondes_core_test_1.tex` et les prompts EX3 à EX9.

Hiérarchie scientifique : (a) code, configurations, données, checkpoints, prédictions et journaux réels ; (b) protocoles et formalismes ; (c) rapports rédigés ; (d) résumés de conversation. En cas de contradiction, signaler la divergence et donner priorité à l'artefact brut vérifiable. `Replica_U_0.tex` et `th_sondes_core_test_1.tex` sont des spécifications à tester, non des preuves de réussite. `th_sondes_core_test_0.tex` et EX10 donnent les antécédents et les paramètres historiques. Les prompts EX3–EX9 fournissent les règles méthodologiques héritées.

L'absence d'une mention dans les archives ne prouve pas une absence absolue d'exposition. Pour les 13 nouveaux ARFF, dire exactement : « non retrouvés dans les artefacts historiques examinés » ; ne pas prétendre qu'ils sont globalement vierges ou inconnus.

## 2. Espace de travail strictement EX11

Racine unique : `/mnt/data/EX11/`. Les archives `last_sources_3.zip`, les historiques EX3–EX10 et leurs sauvegardes ne doivent jamais être copiés dans le livrable EX11. Le seul jeu de données réel autorisé à être copié dans EX11 est le lot `datasets_arff.zip`, après vérification de son SHA-256 et de son CRC ; il est alors rangé sous `data/raw/` avec un manifeste de provenance. Les données synthétiques CNG/CNC sont générées directement par les scripts EX11 et accompagnées de leurs graines, spécifications et hashes.

Arborescence minimale :

```text
EX11/
  README_EX11.md
  prompt_ex11.json
  PRE_REGISTRATION_EX11.md
  RECOVERY_AUDIT_2026-11-03.md
  INPUT_SHA256.txt
  theory/                 # formalisation EX11 créée dans ce projet seulement
  configs/{replica,cng,cnc,efficiency}/
  data/{raw,metadata,splits,train_val,sealed_test,synthetic}/
  src/{data,models,training,evaluation,profiling}/
  tests/
  logs/{append_only,runs,stdout,stderr,environment}/
  results/{raw,checkpoints,predictions,metrics,resources,ablations,quarantine}/
  reports/
  checksums/
  deliverables/
```

Ne pas inclure dans EX11 les anciens checkpoints, modèles, prédictions, caches ou jeux historiques EX3–EX10. Toute réutilisation de code historique doit être copiée sous forme de code source nécessaire, identifiée par son chemin d'origine et son hash, examinée puis versionnée dans EX11 ; aucune archive entière ni historique de résultats ne doit être embarqué. Le code réellement exécuté doit rester dans `src/` et être celui dont le hash est inscrit dans chaque run.

Créer un journal JSONL append-only. Chaque ligne contient au minimum `timestamp`, `run_id`, `parent_run_id`, `phase`, `experiment`, `dataset_or_task`, `variant`, `seed`, `config_sha256`, `code_sha256`, `data_sha256`, `status`, `exit_code`, `duration`, `hardware`, `notes`. En cas de reprise, créer un nouveau `run_id` et conserver l'ancien statut.

## 3. Audit préalable et verrouillage par phases

Le travail est strictement séquencé. Ne pas commencer une phase suivante avant validation objective de la phase courante. Une phase qui échoue à une porte de contrôle est corrigée dans une révision versionnée, puis ré-auditée ; aucune étape ne peut être sautée par simple déclaration.

### Phase 0 — récupération, provenance et intégrité

- Inventorier toutes les entrées et ZIP imbriqués, contrôler leur CRC et leurs empreintes ; ne jamais modifier les sources.
- Reconstituer la carte des prompts, formalismes, scripts, résultats et données EX3–EX10.
- Lire intégralement `Replica_U_0.tex`, `th_sondes_core_test_1.tex`, `th_sondes_core_test_0.tex`, les prompts EX3–EX9 et les rapports EX8–EX10 pertinents.
- Vérifier les versions de Python, PyTorch, NumPy, SciPy, scikit-learn, CPU/GPU, OS, BLAS, nombre de threads, RAM et espace disque.
- Examiner l'état réel du workspace EX11 et distinguer fichiers retrouvés, absents, vides, reconstruits et nouvellement produits. Ne jamais considérer un message antérieur comme substitut à un fichier.

**Porte P0 :** manifeste d'inventaire et de provenance, checksums, rapports CRC, carte des sources et note de divergence validés.

### Phase 1 — protocole scientifique préenregistré

- Écrire ce prompt, le relire intégralement, le parser, vérifier sa cohérence et enregistrer son SHA-256.
- Geler fonctions, domaines, graphes, datasets, splits, seeds, métriques, comparateurs, budgets, tolérances, critères d'arrêt et règles d'analyse avant entraînement.
- Toute correction crée une nouvelle version, une note de changement et un nouveau hash. Aucune modification rétroactive.

**Porte P1 :** JSON valide, corps intégral lisible, aucune contradiction critique, tous les chemins et budgets explicités, hashes consignés.

### Phase 2 — implémentation et tests logiciels

- Implémenter les architectures et les scripts complets.
- Exécuter les tests unitaires, tests de gradient, tests de fuite, test de comptage des paramètres, tests de reproductibilité, tests de sérialisation/rechargement et équivalence de la vectorisation.
- Faire des smoke tests identifiés `SMOKE_ONLY`, séparés des runs scientifiques.

**Porte P2 :** tests obligatoires tous passés ; chaque variante a un script et une configuration ; les différences de code entre variantes sont documentées.

### Phase 3 — exécutions exploratoires/validation

Lancer les branches indépendamment et en conservant tous les runs. Seule la validation sert à sélectionner les variantes. Un problème dans une branche ne bloque pas arbitrairement les autres branches faisables.

**Porte P3 :** résultats validation recalculables à partir des prédictions brutes ; configurations candidates gelées ; aucune lecture du test.

### Phase 4 — gel, test scellé et profilage final

- Geler les modèles, configurations, transformations, seuils, scripts de scoring et analyse statistique.
- Calculer les hashes de tous les artefacts gelés.
- Ouvrir le holdout une seule fois avec un scorer distinct ; enregistrer le hash du script, l'heure, les sorties et tous les échecs.
- Ne jamais réentraîner, régler ou choisir à partir des résultats test. Toute analyse post-test est descriptive ; toute nouvelle optimisation exige un holdout indépendant.

**Porte P4 :** gel documenté, prédictions brutes, résultats test recalculés, manifeste et contrôle de fuite valides.

### Phase 5 — rapport et livraison

Rapporter chaque variante réellement implémentée et chaque run tenté, avec résultats favorables, neutres, défavorables, interrompus et invalides. Créer l'archive finale EX11 et la tester par CRC.

**Porte P5 :** concordance entre registre, fichiers, scripts, prédictions, métriques, checkpoints et hashes ; aucune omission.

## 4. Règles rouges : anti-triche, anti-sabotage, anti-fuite

1. Aucune présomption de réussite ou d'échec. Les seuils ne sont jamais ajustés après lecture du test.
2. Interdiction de manipuler les résultats, les seeds, les budgets, les données, les comparateurs, les hyperparamètres, les temps ou les statuts ; interdiction de provoquer un crash ou d'interrompre sélectivement un run.
3. Aucune variante ne peut être désavantagée volontairement par le prétraitement, la précision numérique, l'ordre des opérations, les ressources, le nombre de pas ou l'initialisation. Les écarts justifiés doivent être préenregistrés et symétriques.
4. Aucun run, seed, checkpoint, dataset, exemple difficile, NaN, divergence, timeout ou crash pertinent n'est supprimé. Les reprises sont append-only.
5. Aucune utilisation du test pour choisir le modèle, checkpoint, seuil, feature, preprocessing, température, budget ou architecture.
6. Tout scaler, imputeur, encodeur catégoriel, KMeans, centre RBF, largeur, PCA, calibration ou statistique est ajusté sur train uniquement. Validation sert à la sélection ; test reste scellé.
7. Toute prédiction supervisée d'une ligne train utilisée pour entraîner routeur, composeur, métamodèle ou student doit être owner-excluded/OOF. Conserver pour chaque ligne le fold propriétaire, les hashes et l'identité du modèle qui l'a prédite.
8. Une transformation transductive n'est permise que si préenregistrée et limitée aux `X_train` sans étiquette ; la marquer explicitement et fournir une ablation inductive.
9. Les comparateurs partagent les mêmes exemples, partitions, seeds, pipeline de prétraitement et critères d'arrêt comparables. Si une asymétrie est imposée par la nature du modèle, la mesurer et l'expliquer.
10. Mesurer le coût total réellement exécuté, y compris toutes les sondes, le routeur, les projections, les préprocesseurs et les appels de fonctions. Ne jamais présenter une accélération d'un sous-composant comme un gain end-to-end.
11. Les limites externes réelles (quota, mémoire, temps, matériel indisponible) sont consignées ; elles ne justifient ni falsification, ni remplacement par une métrique synthétique, ni omission. Continuer les branches indépendantes faisables.
12. Un résultat synthétique n'est pas une preuve de généralisation sur données réelles. Un dataset de continuité historique n'est pas présenté comme vierge.
13. Ne jamais annoncer une mesure d'énergie si aucun wattmètre/compteur matériel valide n'est utilisé. Distinguer FLOPs/MAC estimés structurellement des compteurs matériels mesurés.
14. Toute valeur citée dans un rapport doit être recalculée depuis les prédictions et données brutes persistées, avec script et hash.

## 5. Objectifs, comparateurs et comptage des paramètres

Objectifs hiérarchisés :

1. qualité : log-loss primaire en classification probabiliste ; accuracy, balanced accuracy, macro-F1, Brier, ROC-AUC et calibration en secondaires ; MAE/RMSE en régression ;
2. paramètres : cible de recherche `P_total(candidate) <= P_total(MLP_GE4X)/4` ;
3. ressources : MAC/FLOPs structurels, opérations exponentielles/RBF, mémoire de pointe, taille sérialisée, temps CPU/GPU et énergie uniquement si mesurée ;
4. vitesse : latence p50/p95/p99 aux batchs 1/16/64/256, débit, temps entraînement end-to-end, profil de chaque étape ;
5. généralisation : tâches, datasets et compositions indépendants, frontières, extrapolation et distribution shift.

Toujours fournir trois contrôles :

- `MLP_matched` : MLP standard au nombre de paramètres total le plus proche de la candidate ;
- `MLP_GE4X` : MLP standard tel que `P_total(MLP)/P_total(candidate) >= 4.0` réellement, et non approximé sous le seuil ;
- référence historique la plus pertinente lorsqu'elle est reproductible et adaptée à la même tâche, marquée `historical_reference`.

Calculer `P_train`, paramètres non entraînables/buffers, `P_total` de l'inférence, paramètres actifs par exemple, taille des poids et état de prétraitement. `P_total` inclut les centres, largeurs fixes, tables, seuils, constantes apprises ou conservées influençant la sortie, embeddings, projections, routeur, préprocesseurs persistants et paramètres des couches. Le MLP_GE4X est recalculé pour chaque candidate ; si le ratio est <4.0, la comparaison est `INVALID_FOR_GE4X` et le comparateur doit être agrandi et réentraîné. Ne jamais arrondir 3.999 en 4.

Pour l'équité, publier également le ratio de paramètres entraînables, les MAC/FLOPs, le nombre d'exponentielles, les accès mémoire et le chemin actif. Le nombre de paramètres seul n'est pas une preuve de rapidité.

## 6. Branche A — REPLICA-U sur datasets réels

### 6.1 Hypothèse à tester

La banque de spécialistes permet-elle à un teacher conjoint d'améliorer le backbone, puis un student compact distillé exclusivement depuis des prédictions OOF peut-il conserver suffisamment de qualité tout en supprimant les spécialistes et le routeur à l'inférence ? Rien n'est présumé.

### 6.2 Architecture normative de départ

- Backbone : MLP résiduel compact, couches cachées `[64,32]`, SiLU, tête adaptée à la tâche.
- Prétraitement : ajusté sur train seulement.
- Banque initiale : 7 spécialistes AdaptiveRBF ; `d=4`, `K=8`, encodeur `tanh(W_e x+b_e)`, centres KMeans train-only et entraînables, largeurs positives via softplus et entraînables.
- Fusion : composition résiduelle conjointe ; routeur MLP 16 unités ; entrées `backbone_representation`, `specialist_residuals`, `specialist_disagreement` ; poids normalisés.
- Routage dense comme référence ; ablations top-k=1 et top-k=2 obligatoires si implémentables sans changer silencieusement la tâche.
- Objectif teacher opérationnalisé avant entraînement : les logits fusionnés sont `z_T = z_B + sum_i alpha_i*r_i`, où `z_B` est le backbone et `r_i` le résidu de spécialiste ; pour chaque spécialiste `z_i=z_B+r_i`. La loss principale est `L=L_task(z_T,y)+0.10*mean_i CE(z_i,y)+0.01*mean_i KL(p_i || p_bar)`, avec `p_i=softmax(z_i)` et `p_bar=mean_i p_i`. Le deuxième terme supervise chaque spécialiste ; le troisième pénalise les désaccords probabilistes excessifs sans supprimer l'entrée de désaccord du routeur. L'ablation `T0` retire les deux termes auxiliaires. Les coefficients sont fixes, non réglés sur test. Budgets : backbone/spécialistes/student AdamW, lr=1e-3, weight_decay=1e-4, batch=128, max=300 epochs, patience=30, clipping=1.0 ; teacher conjoint AdamW lr=3e-4, batch=128, max=300 epochs, patience=30, clipping=1.0. Les MLP correspondants reçoivent le même budget d'optimisation et les mêmes règles d'arrêt ; epochs et mises à jour réelles sont enregistrées.
- Student de production : MLP résiduel à passage unique, sans spécialiste, banque RBF, routeur ou teacher à l'inférence. Tester au minimum `[64,32]` et `[32,16]`. La sélection tient compte de qualité ET ressources.
- Distillation classification : cross-entropy sur les vrais labels train + KL à température `T=2` vers les sorties OOF du teacher. Aucune prédiction issue d'un teacher ayant entraîné sur le label propriétaire n'est admise.

### 6.3 Données et familles

Utiliser les 13 ARFF joints, avec la provenance et l'identité ci-dessous :

- `dataset_31_credit-g.arff` — German Credit, classification binaire, variables mixtes ;
- `dataset_44_spambase.arff` — Spambase, binaire ;
- `dataset_50_tic-tac-toe.arff` — Tic-Tac-Toe, attributs catégoriels, binaire ;
- `gina_agnostic.arff` — GINA Agnostic, binaire, haute dimension (~970 variables), tâche dérivée de reconnaissance de chiffres ;
- `kc1.arff`, `kc2.arff`, `pc1.arff`, `pc3.arff`, `pc4.arff` — famille PROMISE de prédiction de défauts logiciels ;
- `php0FyS2T.arff` — One-Hundred-Plants-Shape, multiclasses (vérifier le nombre exact de classes dans le fichier) ;
- `php0iVrYT.arff` — Blood Transfusion ;
- `php8Mz7BG.arff` — Phoneme ;
- `php9xWOpn.arff` — Steel Plates Fault.

Les 5 datasets PROMISE sont une famille apparentée, pas cinq domaines indépendants. L'audit exécuté sur les 13 fichiers confirme 0 valeur manquante et 0 cellule numérique non finie. Les doublons X restent conservés et sont réunis dans des groupes indivisibles ; les conflits de labels ne sont jamais effacés. Comptages audit v2 : Spambase 183 groupes dupliqués/394 lignes supplémentaires/3 groupes conflictuels ; KC1 177/917/20 ; KC2 33/153/6 ; PC1 90/161/6 ; PC3 65/127/3 ; PC4 52/115/1 ; Blood Transfusion 69/246/31 ; Phoneme 9/9/0 ; les autres jeux n'ont pas de doublons X au sein du jeu. Les recouvrements exacts inter-jeux PROMISE sont : PC1–KC1 2 vecteurs, PC1–KC2 2, PC3–PC4 17, KC1–KC2 17. Ils doivent être pris en compte dans toute analyse de transfert et interdisent de compter ces jeux comme observations/domaines indépendants.

GINA : l'en-tête documente 3153 lignes Train puis 315 lignes Valid. Cette frontière est vérifiée sur les lignes : la partie Train a 1550 positifs/1603 négatifs et somme des caractéristiques 164947945 ; la partie Valid a 155/160 et somme 16688946. Préserver ces 315 lignes comme validation d'origine ; dans les 3153 lignes de l'ancien train, créer un test scellé group-stratifié (un fold sur cinq) et utiliser les autres lignes pour l'entraînement. Ne pas fusionner les lignes GINA puis les re-séparer au hasard. GINA est lié à la reconnaissance de chiffres ; ne pas le qualifier de domaine indépendant des chiffres au sens global.

Pour les 12 autres datasets et chaque seed REPLICA-U, utiliser `StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=seed)` sur les groupes SHA-256 de X : un fold pour test scellé, le fold suivant pour validation, les trois autres pour train. Publier les tailles exactes et la présence de toutes les classes ; les groupes ne sont jamais cassés pour atteindre exactement 60/20/20. Pour GINA, suivre l'exception ci-dessus. Si une classe manque dans un split, marquer la limitation et ne jamais déplacer une observation isolément pour forcer son apparition. Les jeux nouvellement joints ne sont pas retrouvés comme données EX3–EX10 dans le corpus consultable, mais l'exposition humaine antérieure est inconnue.

### 6.4 Audit des doublons et partitions

- Parser les ARFF en respectant attributs numériques, nominaux, ordre et type de la cible. Vérifier lignes, schémas, classes, valeurs manquantes, valeurs invalides, doublons et identifiants de lignes.
- Produire une empreinte canonique de `X` sans la cible. Les observations ayant `X` identique forment un groupe indivisible dans les partitions d'un même dataset. Ne pas supprimer les observations ni les groupes à labels contradictoires ; les conserver et les compter.
- Pour les 12 datasets ordinaires, utiliser exactement `StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=seed)` avec les seeds `[1501,1607,1717,2029,3037]` : fold `seed mod 5` = test scellé, fold `(seed+1) mod 5` = validation, trois folds restants = train. Pour GINA, préserver la séparation historique vérifiée : source Train = 3153 lignes ; source Valid = 315 lignes conservées comme validation ; un fold group-stratifié sur cinq est prélevé dans source Train pour le test scellé, les quatre autres folds deviennent train. Les ratios de GINA diffèrent donc de 60/20/20 et doivent être publiés sans correction opportuniste. Les proportions sont des cibles, jamais une justification pour casser un groupe. Vérifier chaque groupe X unique dans une seule partition et la présence des classes. Si une classe ne peut être représentée, marquer la limite au lieu de déplacer des lignes isolément.
- Pour PC3/PC4, ajouter un contrôle cross-dataset des empreintes communes. Aucune observation identique ne peut être dans l'entraînement d'un dataset et le test de l'autre pour une analyse de transfert.
- Encoder les catégories et imputer les données uniquement à partir de train. One-hot pour nominales, standardisation des numériques train-only ; rapporter l'effet de la dimension après one-hot. Les cibles ne sont jamais encodées à partir d'informations test.
- Créer séparément les fichiers `train_val` et `sealed_test`. Le code d'entraînement ne charge jamais `sealed_test`. Le scorer test n'est exécuté qu'après gel et reçoit le modèle figé et le test scellé.

### 6.5 Plan et variantes

Pour chaque dataset et seed, exécuter :

1. backbone MLP seul ;
2. spécialistes préentraînés et gelés + fusion C1 (diagnostic) ;
3. teacher REPLICA-U à fine-tuning conjoint ;
4. student distillé 64/32 ;
5. student distillé 32/16 ;
6. ablation sans spécialistes ;
7. ablation sans entrée de désaccord ;
8. routeur dense, top-1, top-2 lorsqu'ils sont réalisables ;
9. MLP_matched et MLP_GE4X pour chaque student sélectionné.

OOF : 5 folds group-stratifiés sur train uniquement. Les statistiques de prétraitement, KMeans, centres et entraînements sont réajustés dans chaque fold, sans accès aux labels du fold held-out. Chaque fold entraîne d'abord le backbone et les 7 spécialistes (AdamW, lr=1e-3, wd=1e-4, batch=128, max=300 epochs, patience=30), puis ajuste le teacher conjoint (lr=3e-4, max=300, patience=30). Le teacher final de validation/test est entraîné sur tout train avec les mêmes paramètres fixes. Le student apprend par `L_student = CE(p_s,y) + T²*KL(softmax(z_T^OOF/T) || softmax(z_s/T))`, avec `T=2`; seules les prédictions OOF du train sont utilisées comme soft targets. La validation sert à l'arrêt/sélection, et ne remplace jamais les soft targets OOF train. Conserver `fold_owner_map`, hashes des indices et modèles de chaque fold. Les sorties teacher de validation proviennent d'un teacher entraîné uniquement sur train. Distiller sur OOF train et labels train ; ne jamais distiller sur test.

Les cinq seeds sont obligatoires pour chacun des 13 datasets (65 blocs dataset-seed, avant variantes et folds OOF). Si une contrainte externe empêche de terminer tous les runs, publier les runs réalisés et le statut `INCOMPLETE_QUOTA` ; ne jamais extrapoler les runs manquants.

## 7. Branche B — CNG multi-sondes et contribution

Respecter `th_sondes_core_test_1.tex`.

### 7.1 Sonde AdaptiveRBF

Pour `x in R^p`, `z=tanh(W_e x+b_e)` avec dimension latente `d=4`; `K=8` centres RBF `c_k`; `r_k=exp(-||z-c_k||²/(2 sigma_k²))`; lecture `P(x)=V r(x)+b`. Centres et largeurs par centre entraînables ; largeurs positives et bornées. KMeans est ajusté exclusivement sur les représentations train.

### 7.2 Fonctions, domaines et données

Réplication EX10 :
- `f1(x)=sin(x)`, `x in [-pi,pi]` ;
- `f2(x1,x2)=x1*x2`, `[-2,2]^2` ;
- `f3(x1,x2)=x1^2+x2`, `[-2,2]^2` ;
- `f4(x1,x2,x3)=sin(x1*x2)+x3`, `[-2,2]^3`.

Confirmatoires nouvelles :
- `f5(x1,x2)=sin(x1)+0.5*cos(2*x2)`, `[-pi,pi]^2` ;
- `f6(x1,x2,x3)=x1*x2+0.25*x3^2`, `[-2,2]^3`.

Par tâche et seed : 4096 train, 1024 validation, 8192 test scellé indépendants ; boundary et extrapolation séparés. Extrapolation hors domaine n'intervient jamais dans sélection.

Seeds CNG : `[1501,1607,1717,2029,3037,4099,4517,5003,6011,7013]`.

### 7.3 Variantes

- A1 : M=1 AdaptiveRBF simple ;
- A2 : M=2,4,7 avec moyenne fixe ;
- A3 : M=2,4,7 avec composeur linéaire appris sur sorties concaténées ;
- A4 : MLP direct `MLP_matched` ;
- A5 : MLP direct GE4X avec ratio réel >=4 ;
- A6 : AdaptiveRBF directe sans multi-sondes.

Auditer si A1 et A6 sont mathématiquement et paramétriquement identiques. Si oui, un seul entraînement canonique avec alias documenté ; ne pas le compter deux fois comme réplication indépendante. Si non, préciser leurs différences.

Entraînement CNG initial : Adam, lr=1e-3, weight decay=1e-5, batch 128, 800 epochs maximum, patience 50, checkpoint choisi sur MAE validation. Même protocole d'arrêt/budget pour comparateurs appariés ; rapporter aussi temps et nombre de mises à jour réels. Pour CNC, budget explicite hérité d'EX10 : Adam, lr=1e-3, batch=64, maximum 500 epochs, patience 30 pour spécialistes, C2, C3 et C4 ; les comparateurs utilisent la même règle d'arrêt. C5 natif exact n'a pas de temps d'entraînement.

### 7.4 Ablations et coopération

Pour A3 M=4 et M=7, réaliser leave-one-probe-out dans deux régimes : (F) sondes survivantes gelées, seul composeur réappris ; (R) système réduit réentraîné depuis initialisation indépendante. Rapporter ΔMAE, ΔRMSE, corrélation des erreurs, diversité et stabilité des contributions par sonde/seed. Les deux régimes restent séparés. Ne pas déclarer spécialisation si les contributions ne sont pas reproductibles.

## 8. Branche C — CNC par composition

Respecter `th_sondes_core_test_1.tex` et les domaines mathématiques :

- ADD, SUB, MUL : entrées primaires dans `[-2,2]` ;
- DIV : numérateur `[-4,4]`, dénominateur `[-1,-0.25] U [0.25,3]` ;
- EXP : argument `[-2,2]` ;
- LOG : argument `[0.1,9]`.

Spécialistes : AdaptiveRBF `d=4,K=8` ; apprentissage sur distributions intermédiaires réellement générées par les entrées du graphe, pas sur distributions arbitraires indépendantes.

Graphes :
- g1(a,b,c)=a*b+exp(c) ;
- g2(a,b,c)=a*b/(c+1), avec `|c+1|>=0.25` ;
- g3(a,b,c)=log(a²+b²+1)+exp(c) ;
- g4(a,b,c)=exp(a*b)+c ;
- g5(a,b,c)=log(a*b+5)+c².

g1–g3 servent à entraîner/choisir les spécialistes selon le protocole ; g4–g5 sont des compositions inédites scellées pour le test de composition et ne servent jamais au choix des modèles.

Configurations : C1 spécialistes gelés ; C2 initialisés depuis les checkpoints individuels et ajustés conjointement sur les données train du graphe ; C3 MLP direct sur entrées primaires ; C4 AdaptiveRBF directe ; C5 calcul natif exact comme oracle non appris (pas un concurrent appris). Pour chaque graphe et seed : 8192 train, 2048 validation, 8192 test scellé ; boundary et stress séparés. Seeds principales identiques aux dix seeds CNG. Pour la comparaison directe C3/C4 sur un même graphe et une même seed, utiliser exactement le même ordre de mini-batches (graine d’ordre appariée), tout en conservant des initialisations de paramètres indépendantes et en documentant les deux graines. Cette contrainte réduit une source évitable de variance sans forcer l’égalité des initialisations.

Tracer chaque nœud : cibles exactes, sorties apprises, MAE/RMSE, amplification/atténuation des erreurs et propagation jusqu'à la sortie. Les métriques relatives ne sont rapportées que loin de zéro avec epsilon préenregistré.

## 9. Branche D — expérience originale d'efficacité d'implémentation

Question : à fonction et paramètres équivalents, la vectorisation multi-sondes réduit-elle réellement la latence et le coût d'entraînement ; le partage d'encodeur apporte-t-il un compromis utile ? Comparer :

- `D1_SEQ` : M modules indépendants appelés séquentiellement ;
- `D2_VEC` : les mêmes poids et la même fonction regroupés en opérations batchées/vecteur ;
- `D3_SHARED` : un encodeur partagé avec têtes/centres par sonde, architecture distincte et potentiellement moins de paramètres.

D1 et D2 doivent d'abord réussir une vérification sur sorties ET gradients avec les mêmes paramètres et entrées ; tolérance `atol=1e-6`, `rtol=1e-6` en float32 (publier maximum absolu et relatif). Toute différence fonctionnelle invalide la comparaison « même modèle » jusqu'à correction.

D3 n'est pas une équivalence exacte : c'est une variante architecturale, son changement de capacité est documenté et sa qualité est évaluée sur les mêmes tâches et seeds CNG.

Profilage : CPU mono-thread, même machine et environnement, 30 warmups minimum, 200 répétitions minimum par batch `1,16,64,256`, ordre alterné et répétitions indépendantes ; mesurer p50/p95/p99, débit, RSS/peak memory, temps forward, backward, optimizer step, temps epoch et training end-to-end. Faire un profil end-to-end séparé incluant le prétraitement. Séquentialiser les modèles ; si une contention est détectée, marquer la mesure `CONTENDED` et la refaire en nouveau run sans supprimer l'ancienne. Mesurer FLOPs/MACs et compte d'exponentielles structurellement ; énergie uniquement avec compteur fiable.

Pour D3, entraîner et comparer la qualité sur f1, f2, f5 et f6 avec les dix seeds principales. Si un quota ou une limite matérielle réelle empêche la complétion, déclarer `INCOMPLETE_QUOTA`, conserver tous les runs et ne tirer aucune conclusion confirmatoire sur les tâches ou seeds manquantes.

## 10. Métriques, statistiques et règles de décision

Classification : log-loss, accuracy, balanced accuracy, macro-F1, Brier, ROC-AUC lorsque défini, ECE/calibration et matrices de confusion ; rapport par classe pour les 100 classes.
Régression CNG/CNC : MAE, RMSE, médiane et P90 de l'erreur absolue, erreur par tâche/graine/nœud.
Ressources : `P_train`, `P_total`, paramètres actifs, taille checkpoint, MAC/FLOPs estimés, nombre de RBF/exponentielles, mémoire RSS et peak, latence p50/p95/p99, débit, temps train complet et temps par étape.

Rapporter chaque seed et chaque tâche. L'unité de répétition principale est la graine et non les points d'un même test. Comparaisons appariées sur splits et seeds identiques ; bootstrap apparié au niveau seed/tâche et intervalles de confiance. Publier effets individuels et macro-moyennes ; ne pas agréger des tâches ou familles apparentées en pseudo-réplications indépendantes.

Les verdicts sont séparés : qualité, paramètres, mémoire/ressources, temps entraînement, latence/débit, généralisation, validité/reproductibilité. Statuts possibles : `SUPPORTED`, `PARTIALLY_SUPPORTED`, `NOT_SUPPORTED`, `INCONCLUSIVE`, `NOT_TESTED`, `INVALID`, `INCOMPLETE_QUOTA`. Pas de verdict global positif si une dimension prioritaire échoue.

## 11. Livrables obligatoires, sans omission

Pour chaque variante réellement implémentée et chaque run tenté : nom, hypothèse, code exact, hash, config complète, dataset/tâche, partition et hash, seed, environnement, statut, logs stdout/stderr, temps, paramètres, checkpoint, prédictions brutes, métriques recalculables, profil ressources, erreurs et reprise éventuelle. Aucune variante ou métrique disponible ne peut être omise.

Livrer au minimum :

- `prompt_ex11.json` et `PRE_REGISTRATION_EX11.md` ;
- `README_EX11.md`, `WORKSPACE_INDEX_EX11.md`, `AUDIT_SOURCES_EX11.md`, `RECOVERY_AUDIT_2026-11-03.md` ;
- `theory/EX11_PROTOCOL.tex` et diagrammes ;
- tous les scripts réellement exécutés, sans omission (audit, extraction, construction des splits, prétraitement, entraînement, génération des données synthétiques, scoring, évaluation, profilage, tests, outils de reprise et scripts des variantes), leurs versions exactes, hashes, commandes, paramètres et environnements ; les scripts échoués et remplacés restent dans `versions/` avec statut et motif ; configurations et tests ;
- ARFF bruts fournis pour EX11, metadata, dictionnaire de variables, partitions, manifests et checksums ;
- logs append-only complets, registre de tous les runs, y compris échoués ;
- checkpoints des variantes exécutées ;
- prédictions de validation et de test, avec test uniquement après gel ;
- tables détaillées par seed/tâche/variante, métriques, profils CPU/RAM/latence/débit, FLOPs/MACs structurels ;
- ablations CNG/CNC et rapport d'erreurs par nœud ;
- rapports `REPLICA_U_REPORT.md`, `CNG_REPORT.md`, `CNC_REPORT.md`, `EFFICIENCY_REPORT.md`, `EX11_FINAL_REPORT.md` ;
- manifeste `EX11_MANIFEST.json`, `SHA256SUMS.txt`, archive `EX11_DELIVERABLES.zip` testée par CRC.

Le workspace de livraison ne contient que des fichiers EX11, les 13 ARFF nouvellement fournis utilisés par EX11, les sorties, scripts, rapports et manifestes EX11. Il exclut `last_sources_3.zip`, les archives EX3–EX10, leurs historiques, sauvegardes, checkpoints historiques, résultats anciens et caches. Les rapports historiques peuvent être cités et hashés sans être copiés.

## 12. Ordre opérationnel obligatoire

1. Terminer P0 et publier l'audit de sources/provenance/intégrité.
2. Relire ce prompt entier et analyser les éventuelles contradictions ; corriger avant toute expérience.
3. Produire et figer `PRE_REGISTRATION_EX11.md`, ses seeds, splits, métriques et SHA-256.
4. Extraire les 13 ARFF après vérification ; auditer schémas, lignes, classes, doublons et conflits.
5. Construire les partitions group-stratifiées, manifester les groupes/indices et sceller le test.
6. Implémenter REPLICA-U, AdaptiveRBF, CNG, CNC, D1/D2/D3 et les comparateurs ; réaliser les tests logiciels.
7. Lancer les branches sans accès test ; enregistrer tous les runs.
8. Sélectionner par validation uniquement, puis geler code, configs et checkpoints.
9. Ouvrir le test une seule fois avec scorer séparé ; auditer les prédictions.
10. Profiler tous les modèles figés sur matériel identique ; exclure uniquement les mesures de contention selon règle préenregistrée, en gardant les traces.
11. Produire les rapports, contrôles d'omission, checksums et archive finale.

## 13. Décision finale

Ne jamais conclure que l'architecture est meilleure simplement parce qu'elle possède moins de paramètres. Le résultat recherché doit être démontré séparément sur précision/log-loss, ratio `P_total >=4x`, ressources, vitesse d'entraînement, vitesse d'inférence, mémoire et généralisation. Une architecture plus compacte mais plus lente ou plus coûteuse doit être rapportée comme telle. Une variante plus rapide mais moins précise doit également l'être. Le résultat final peut être positif, négatif, mixte ou inconclusif ; aucun n'est imposé à l'avance.

