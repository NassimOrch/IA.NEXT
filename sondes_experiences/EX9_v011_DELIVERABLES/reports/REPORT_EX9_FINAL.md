# EX9 v011 — rapport final d'exécution et audit

Date d'état : 2 novembre 2026.

## Verdict exécutif

Le prompt `prompt_ex9.json` est construit, syntaxiquement valide et audité vis-à-vis des exigences données. Les sources EX3–EX8 et les traces EX8 v010 ont été récupérées/historisées, en particulier B10/B11. L'exécution EX9 a comporté 45 runs de classification XOR8, 35 ablations B10, 9 pilotes CNG/CNC, puis 90 runs additionnels sur deux domaines synthétiques pré-déclarés. Les deux holdouts de ces domaines ont été scorés une fois après un verrou séparé.

**Verdict scientifique actuel : les gains historiques Wisconsin de B10/B11 ne se généralisent pas aux trois domaines synthétiques essayés.** B10, B11 et A0 sont nettement derrière leurs MLP appariés et ≥4× sur XOR8 en validation, concentric2 et rotated_moons2 en validation/test. Les sondes ont aussi une latence d'inférence CPU beaucoup plus élevée. Le critère « moins de paramètres que MLP_GE4X » est satisfait ; la qualité et la rapidité ne le sont pas dans ces expériences. Aucun jeu réel externe vierge n'a été validé. L'exécution complète du programme scientifique reste donc partielle malgré les livrables et audits effectués.

## 1. Sources et protocole

- `last_sources_3.zip` (336 478 208 octets) a été testé/extrait via shell ; CRC des archives imbriquées vérifiés.
- Prompts EX3, EX4, EX5, EX6, EX7 et EX8 relus ; leurs règles indépendantes du projet sont synthétisées dans `prompt_ex9.json` et auditées dans `reports/PROMPT_EX9_AUDIT.md`.
- Les snapshots historiques EX3–EX8, les données et les checkpoints restent à l'extérieur de `EX9_v011`. Aucun ZIP historique n'est copié dans le livrable.
- `sonde_adapt_global_research_final.zip` n'existe pas comme archive distincte dans l'entrée reçue ; il n'est pas déclaré comme inspecté sous ce nom.
- `prompt_ex9.json` et `deliverables/prompt_ex9.json` sont byte-identiques et leur SHA-256 concorde.

## 2. B10/B11 historiques EX8 — récupération complète

Le dossier EX8 B10 contient configurations, scripts exacts, poids, historique, prédictions, diagnostics de table/codebook, comparateurs MLP et manifestes. L'audit d'intégrité du bundle est PASS.

| Variante | Log-loss Wisconsin | MLP apparié | MLP ≥4× | Gains par seed | P_total EX8 | p50 batch1 EX8 |
|---|---:|---:|---:|---:|---:|---:|
| B10 | 0,04138964 | 0,05472717 | 0,05080315 | 5/5 | 884 | ~0,332 ms |
| B11 | 0,04442526 | 0,05429128 | 0,05224341 | 5/5 | 835 | ~0,116 ms |

Backbone commun : cinq AdaptiveRBF parallèles d=4/K=4, 20 évaluations RBF par observation. B10 utilise marge et désaccord, memberships floues 3×3, table 9×5 et softmax de ligne pour pondérer les cinq logits ; B11 utilise un gate softmax standard. B10 est ~2,85× plus lent que B11 sur p50 batch1. Différence B10−B11 moyenne −0,003036 ; IC t et bootstrap imbriqué incluent 0 ; test exact de signes bilatéral p=0,0625. Les cinq seeds partagent le même split Wisconsin : ces résultats restent des résultats de développement historiques, pas une preuve confirmatoire indépendante.

## 3. Cohorte XOR8 Rev2 — réplication de développement

45 runs (B10, B11, A0 × cinq seeds, chacun avec MLP apparié et MLP_GE4X), JSON/checkpoints sauvegardés. Audit métrique validation PASS 45/45. MLP_GE4X respecte `P_total_MLP / P_total_candidate ≥4.0` pour chaque paire.

| Candidate | Log-loss validation | MLP apparié | MLP ≥4× | P_total candidate / GE4X | Gains vs MLP |
|---|---:|---:|---:|---:|---:|
| B10 | 0,549981 | 0,314458 | 0,300874 | 400 / 1 602 | 0/5 |
| B11 | 0,554089 | 0,306784 | 0,301720 | 351 / 1 404 | 0/5 |
| A0 | 0,450060 | 0,303134 | 0,304630 | 608 / 2 438 | 0/5 |

Le test XOR8 a été généré en mémoire après le lock, mais l'évaluateur a échoué au chargement du checkpoint `__main__.MLP` avant la première prédiction. Il n'y a aucune prédiction ni métrique de test XOR8. Selon la règle anti-triche, ce holdout est déclaré consommé/compromis et n'a pas été relancé. Le lock `MODEL_LOCK.json` est une photographie pré-test ; la réalité de l'ouverture est indiquée dans `SEALED_TEST_FAILURE.json` et `reports/PRE_TEST_CURRENT_STATUS.md`.

## 4. Ablations supplémentaires B10

35 runs (7 familles de table × cinq seeds), backbone B10 existant gelé ; la validation XOR8 réutilisée. Audit indépendant PASS 35/35, erreur maximale de prédiction/log-loss = 0. Les variantes testées : quantiles 25/75, absence marge, absence désaccord, hard 3×3, codebook 2×2, sans régularisation et factorisation additive 3+3.

Meilleure log-loss moyenne descriptive : NO_DISAGREEMENT 0,544668 ; CODEBOOK_2X2 0,546467 ; FACTORIZED_3PLUS3 0,544697. Elles restent très loin des MLP (~0,30) et la latence reste supérieure. La validation a servi à la sélection de table : statut exploratoire/non confirmatoire. `HARD_3X3` a fait l'objet d'un contrôle de binning ; aucun seuil exact n'est touché sur les 5 train/validation, et les deux conventions produisent zéro mismatch.

## 5. Domaines synthétiques additionnels : validation et tests scorés

Deux domaines présents dans le pré-enregistrement initial mais non exécutés jusque-là ont été réalisés après un pré-enregistrement additionnel : `concentric2` (train/validation seeds 61101/61201, test 61301) et `rotated_moons2` (62101/62201, test 62301). Chaque domaine a 600 train, 240 validation, 1 200 test ; cinq seeds de modèles ; 3 candidates et deux MLP comparateurs par candidate. 45 runs/domaine, 90 au total. Les historiques MLP complets sont stockés dans ces nouveaux runs.

Audit validation : PASS 90/90 ; erreur max de prédiction = 0, log-loss = 0 ; matrices et scaler hashés ; tous les MLP_GE4X ≥4×.

### Résultats validation

| Domaine | Candidate | Candidat | MLP apparié | MLP ≥4× | Gains candidat / comparateurs |
|---|---|---:|---:|---:|---:|
| concentric2 | B10 | 0,282177 | 0,045578 | 0,039877 | 0/5 ; 0/5 |
| concentric2 | B11 | 0,284219 | 0,046408 | 0,039040 | 0/5 ; 0/5 |
| concentric2 | A0 | 0,199706 | 0,039272 | 0,042231 | 0/5 ; 0/5 |
| rotated_moons2 | B10 | 0,293651 | 0,154635 | 0,153480 | 0/5 ; 0/5 |
| rotated_moons2 | B11 | 0,291933 | 0,154494 | 0,153687 | 0/5 ; 0/5 |
| rotated_moons2 | A0 | 0,269514 | 0,153671 | 0,153051 | 0/5 ; 0/5 |

### Résultats synthétiques confirmatoires (holdouts ouverts une fois)

Verrou séparé `MODEL_LOCK_MULTI_DOMAIN.json` : 295 SHA-256. Le préflight a chargé les 90 checkpoints avant génération test. 90 prédictions ont été calculées, sans modification de modèle après ouverture. L'audit métrique depuis les labels/probabilités sauvegardés passe 90/90, écart nul ; aucun générateur ni forward model n'a été rappelé lors de l'audit.

| Domaine | Candidate | Log-loss test | Accuracy | MLP apparié | MLP ≥4× | Gains candidate / comparateurs |
|---|---|---:|---:|---:|---:|---:|
| concentric2 | B10 | 0,255830 | 0,8433 | 0,063186 | 0,059463 | 0/5 ; 0/5 |
| concentric2 | B11 | 0,255024 | 0,8433 | 0,064854 | 0,058597 | 0/5 ; 0/5 |
| concentric2 | A0 | 0,200912 | 0,9228 | 0,059220 | 0,060707 | 0/5 ; 0/5 |
| rotated_moons2 | B10 | 0,256111 | 0,8963 | 0,122245 | 0,121291 | 0/5 ; 0/5 |
| rotated_moons2 | B11 | 0,255320 | 0,8940 | 0,122342 | 0,121378 | 0/5 ; 0/5 |
| rotated_moons2 | A0 | 0,232610 | 0,9170 | 0,121618 | 0,121019 | 0/5 ; 0/5 |

Pour les 12 comparaisons, le delta moyen `candidate − MLP` est positif et l'IC bootstrap imbriqué à 95 % (10 000 réplications, seeds et observations) reste entièrement positif. Les cinq seeds de modèles partagent toutefois le même dataset test ; ces intervalles décrivent cette partition, pas l'incertitude entre domaines. Détails : `deliverables/SYNTHETIC_CONFIRMATION_EX9.md`.

## 6. Vitesse et ressources

Sur les deux domaines 2D, p50 E2E batch1 CPU moyen des candidates : B10 ~0,367–0,385 ms, B11 ~0,205–0,223 ms, A0 ~0,291–0,346 ms ; les MLP appariés se situent ~0,017 ms. Les sondes sont donc environ 12–22× plus lentes en ce profil. Les temps d'entraînement sont variables : B11 parfois plus rapide qu'un MLP apparié, A0 parfois plus lent ; pas d'avantage stable des sondes.

P_total est bien inférieur aux MLP_GE4X (≥4×), mais souvent proche du MLP apparié. Les proxies MAC structurels ne couvrent pas les exponentielles RBF, distances, softmax et coordination complète ; ils ne sont pas un comptage FLOPs fiable. FLOPs/MAC end-to-end, RSS peak isolé par run, énergie et profil GPU ne sont pas mesurés. Le profil CPU a 20 warmups et 40 répétitions : p95/p99 restent indicatifs.

## 7. Coeur neuronal CNG/CNC

`th_sondes_core_test_0.tex` a été relu, et les incohérences de domaines d'opérandes, interpolation/extrapolation et normalisation cible ont été formalisées dans `th_sondes_core_test_1.tex`. Le PDF compile. 9 pilotes train/validation seulement : 3 CNG pour sin(x) M1/M2 mean/M2 linear et 6 spécialistes CNC ADD/SUB/MUL/DIV/EXP/LOG en M1 ; audit indépendant PASS 9/9. CNG mean M2 améliore légèrement MAE/RMSE face à M1 mais double environ les paramètres. Aucun graphe composé C1/C2, aucun M=1/2/4/7 complet sur plusieurs fonctions, aucun MLP comparateur. Le pilote DIV a le bon support mais une densité positive/négative 50/50 non conforme à la distribution exacte induite ; il est pilote de support uniquement.

## 8. Traçabilité, integrity et conformité

- Prompt JSON root/deliverables byte-identique.
- Archives sources et workspaces inventoriés ; sources originales restent hors EX9.
- Lock XOR8 historique : 151 empreintes pré-test vérifiées ; statut réel d'échec exposé séparément.
- Lock des deux domaines synthétiques : snapshot pré-test de 295 empreintes ; l'audit post-test retrouve 294/295 fichiers identiques. L'unique divergence est le rapport documentaire `reports/PROMPT_EX9_AUDIT.md`, mis à jour pour consigner la reprise ; aucun modèle, code expérimental, configuration, donnée ni prédiction n'a changé. Détail : `reports/PROMPT_EX9_AUDIT_LOCK_EXCEPTION.md` et `results/processed/MULTI_DOMAIN_LOCK_POSTTEST_AUDIT.json`.
- Registres : 83 entrées dans le registre initial, appendix de reclassification, 35 ablations, 90 runs multi-domaines ; pilotes CNG/CNC 9 ; aucune tentative supprimée.
- Les historiques MLP sont manquants sur les 45 runs XOR8 initiaux ; les 90 nouveaux runs ont les historiques complets. Les états d'optimiseur n'ont pas été sauvegardés. Voir `TRACE_CAPTURE_GAP.md`.
- `sonde_adapt_global_research_final.zip` n'est pas présent séparément dans l'archive reçue.
- Aucun dataset réel externe vierge n'a été récupéré (environnement hors-ligne/DNS ; PyArrow absent). SMS, Wisconsin, Iris et Breast ont déjà été exposés historiquement et ne sont pas réutilisés comme holdout vierge.

## 9. Ce qui reste non exécuté

1. Confirmation sur dataset réel externe vierge, gel préalable et prétraitement approprié.
2. Ablations B10/B11 end-to-end : KMeans strictement shard-pure, partage/déduplication du calcul RBF, distillation du gate/action language, lookup plus petit, kernels vectorisés/compilés, coût complet.
3. Série A0 : local-only/global-only, PCA 1/4/8, centres partagés, fusions et hybrides dans une matrice multi-domaines.
4. CNG complet M=1/2/4/7 sur les fonctions de base, comparateurs MLP, tests extrapolation et ablations gelées/ré-entraînées ; CNC C1/C2/C3 composé et fine-tuning conjoint.
5. MAC/FLOPs complet, mémoire peak RSS isolée, consommation énergie.
6. Capturer états d'optimiseur et historiques manquants des premiers runs XOR8 serait impossible à reconstituer fidèlement sans réexécution ; aucune trace n'a été inventée.

## Conclusion

B10/B11 restent des résultats historiques intéressants sur Wisconsin et méritent une recherche ciblée ; B10 n'a pas prouvé qu'il est plus efficace que B11, puisque son action-language coûte plus cher en latence. Mais l'exécution EX9 n'a pas confirmé la qualité face aux MLP dans les trois domaines synthétiques et montre une forte pénalité de vitesse CPU. La compression de paramètres face au grand MLP est réelle, mais elle n'établit pas l'équivalence fonctionnelle recherchée. Aucun modèle n'est promu gagnant. La prochaine étape rationnelle est d'obtenir un dataset réel vierge approprié, puis d'étudier le coût du backbone RBF et du routage sur une implémentation optimisée avant de développer encore la sophistication du gate.
