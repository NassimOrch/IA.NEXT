# EX12 — Rapport confirmatoire P7 : résultats de test

**Date de clôture : 2026-11-04**  
**Statut de porte : PASS (12/12 contrôles)**

## 1. Objet et portée

P7 est la campagne confirmatoire finale pré-enregistrée d’EX12. Elle évalue quatre variantes HC-RBF (R0, C2, C3, C4) contre des MLP appariés par nombre de paramètres entraînables, sur quatre fonctions synthétiques de régression et vingt graines confirmatoires. La comparaison primaire porte sur NMAE normalisée par l’écart-type de la cible calculé exclusivement sur le jeu d’entraînement. La marge de non-infériorité est +0,02 (différence candidat − MLP).

**Portée limitée :** P7 confirme uniquement les quatre tâches synthétiques primaires indiquées ci-dessous. Les résultats Diabetes et classification du pilote P3 restent exploratoires ; ils ne deviennent pas des résultats confirmatoires par extrapolation. Aucun holdout historique EX3–EX11 n’a été utilisé.

## 2. Protocole gelé et accès au test

- Tâches primaires : `f1_sin`, `f2_mul`, `f3_square_plus`, `f4_sin_product`.
- 20 graines confirmatoires disjointes des 10 graines pilotes.
- Huit slots par tâche×graine : R0/C2/C3/C4 et MLP apparié M0_MATCH_R0/C2/C3/C4.
- 640 entraînements : 4 tâches × 20 graines × 8 slots.
- Paramètres entraînables appariés à ±1 % lorsque réalisable ; écart maximal vérifié : 0,9238 %. Les centres fixes, buffers, normaliseurs et `P_total` sont déclarés séparément.
- Train : 1 200 observations ; validation : 240 par régime ; test : 1 000 par régime. Régimes : interpolation, frontière, extrapolation et shift.
- Sélection du checkpoint : interpolation validation uniquement. Les autres régimes de validation sont diagnostiques.
- Les modèles, configs, scripts et manifests ont été gelés avant génération des tests. Le SHA-256 du gel est `a43e56047af7bc8496dcb94d5c2835c9bc553d8c24891949c4f42869361206bd`.
- Après gel, 80 jeux de test (640 arrays) ont été générés et contrôlés ; SHA-256 du manifeste : `b9944b13b909fe74e9b3480f926bdd1c56950080d2431516e821e241b1dcff99`.
- Scoring unique : 640 modèles × 4 régimes = 2 560 évaluations. Aucune ré-optimisation, sélection ou ré-entraînement post-test.

## 3. Intégrité et réconciliation

| Contrôle | Résultat |
|---|---:|
| Entraînements confirmatoires | 640/640 |
| Modèles scorés | 640/640 |
| Scores modèle×régime | 2 560/2 560 |
| Jeux test | 80/80 |
| Arrays test | 640/640 |
| Comparaisons appariées par graine et régime | 1 280/1 280 |
| Contrastes primaires (4 tâches × 4 variantes) | 16/16 |
| Artefacts gelés vérifiés | 4 257/4 257 |
| Divergences de métriques / SHA après audit | 0 |

La recomputation des métriques depuis les prédictions sauvegardées est activée et l’audit de score passe 11/11 contrôles. Les fichiers bruts de prédiction, métriques, scripts et registres sont livrés dans le workspace.

## 4. Résultats primaires : interpolation

Différence = NMAE(HC-RBF) − NMAE(MLP apparié). Une valeur négative favorise HC-RBF. Chaque ligne est calculée sur 20 différences appariées par graines ; IC à 95 % apparié. Les p-values sont corrigées par Holm sur les 16 contrastes primaires. La non-infériorité utilise la marge candidat−MLP ≤ +0,02 et une correction Holm unilatérale.

| Tâche | Variante | Différence moyenne | IC95 % | p Holm bilatéral | p Holm NI | NI ? |
|---|---:|---:|---:|---:|---:|:---:|
| f1_sin | R0 | +0.08343 | [+0.03606, +0.13080] | 0.01568 | 1 | Non |
| f1_sin | C2 | +0.10378 | [+0.05125, +0.15631] | 0.006193 | 1 | Non |
| f1_sin | C3 | +0.13418 | [+0.09919, +0.16917] | 2.554e-06 | 1 | Non |
| f1_sin | C4 | +0.04370 | [+0.00465, +0.08276] | 0.1511 | 1 | Non |
| f2_mul | R0 | -0.01408 | [-0.04922, +0.02106] | 0.412 | 0.1415 | Non |
| f2_mul | C2 | -0.02375 | [-0.05665, +0.00915] | 0.2946 | 0.03555 | Oui |
| f2_mul | C3 | -0.03716 | [-0.07581, +0.00149] | 0.1757 | 0.02083 | Oui |
| f2_mul | C4 | -0.05679 | [-0.10532, -0.00827] | 0.1449 | 0.01464 | Oui |
| f3_square_plus | R0 | -0.03482 | [-0.05974, -0.00991] | 0.06074 | 0.0009645 | Oui |
| f3_square_plus | C2 | -0.03419 | [-0.05762, -0.01076] | 0.05273 | 0.0006808 | Oui |
| f3_square_plus | C3 | -0.03390 | [-0.06488, -0.00292] | 0.1511 | 0.007812 | Oui |
| f3_square_plus | C4 | -0.05666 | [-0.08450, -0.02883] | 0.005069 | 9.65e-05 | Oui |
| f4_sin_product | R0 | -0.04361 | [-0.06433, -0.02289] | 0.003961 | 2.583e-05 | Oui |
| f4_sin_product | C2 | -0.04659 | [-0.06602, -0.02716] | 0.001067 | 6.104e-06 | Oui |
| f4_sin_product | C3 | -0.03941 | [-0.06599, -0.01282] | 0.05273 | 0.0009023 | Oui |
| f4_sin_product | C4 | -0.03553 | [-0.05025, -0.02081] | 0.001061 | 1.626e-06 | Oui |

**Synthèse primaire : 11/16 contrastes passent le test de non-infériorité ajusté. 7/16 rejettent l’égalité à zéro après correction de Holm bilatérale.** Les contrastes significatifs ne sont pas tous à l’avantage du même modèle : f1_sin R0/C2/C3 défavorisent HC-RBF ; f3_square_plus C4 et f4_sin_product R0/C2/C4 favorisent HC-RBF.

**Erratum de synthèse :** le compte exact recalculé depuis `P7_TEST_PRIMARY_HOLM_16.csv` est 7/16 contrastes bilatéraux significatifs après correction de Holm. Toute synthèse préliminaire indiquant 4/16 est supersédée par ce compte audité.

## 5. Généralisation par régime

| Régime | Contrastes tâche×variante | Différence NMAE moyenne | Contrastes favorables à HC-RBF |
|---|---:|---:|---:|
| interpolation | 16 | -0.00571 | 12/16 |
| boundary | 16 | -0.03192 | 15/16 |
| extrapolation | 16 | +0.20559 | 4/16 |
| shift | 16 | +0.00298 | 12/16 |

Moyenne des 16 contrastes par régime :

| Tâche | Interpolation | Frontière | Extrapolation | Shift |
|---|---:|---:|---:|---:|
| f1_sin | +0.0913 | -0.0068 | +0.2626 | +0.1289 |
| f2_mul | -0.0329 | -0.0257 | +0.4327 | -0.0386 |
| f3_square_plus | -0.0399 | -0.0353 | +0.1491 | -0.0429 |
| f4_sin_product | -0.0413 | -0.0599 | -0.0220 | -0.0355 |

L’extrapolation est le point faible principal : différence moyenne +0,20559 sur les 16 contrastes ; seulement 4/16 contrastes favorisent HC-RBF, et ces quatre cas concernent `f4_sin_product`. Sur `f1_sin`, `f2_mul` et `f3_square_plus`, les quatre variantes sont moins bonnes que leur MLP apparié en extrapolation. Le shift moyen est proche de zéro (+0,00298), mais le signe dépend fortement de la tâche : `f1_sin` est défavorable aux sondes tandis que les trois autres tâches sont favorables. La frontière favorise HC-RBF dans 15/16 contrastes.

## 6. Coût et efficacité : confrontation P5

Les statistiques de ressources ci-dessous proviennent du **benchmark canonique P5 V3** et du `P5_phase_gate.json` (PASS 15/15). P5 a profilé 560 modèles, 13 440 cellules timing, 1 075 200 latences élémentaires, 2 560 comparaisons appariées de latence, 320 paires mémoire et 320 paires de temps de pipeline. Le protocole utilisait CPU mono-thread, float32, batches 1/16/64/256, deux chemins (modèle seul et normalisation+modèle), et trois blocs indépendants de 80 mesures.

Les ratios sont candidat/MLP : >1 signifie HC-RBF plus lent ou plus volumineux. Le chemin « full » inclut la normalisation. Le temps d’entraînement P5 est une durée de pipeline P3/P4 incluant initialisation, validation, diagnostics de couverture et écriture des artefacts ; il est descriptif, pas une mesure pure de l’optimiseur. La taille mémoire est la taille exacte des tenseurs/buffers/normaliseur; RSS est un indicateur process-level non attribuable proprement à un modèle. Aucune mesure d’énergie ou GPU n’est disponible.

| Variante | p50 modèle seul B1 | p50 pipeline B1 | p50 pipeline B256 | Temps pipeline enregistré | Stockage tenseurs | NMAE régression P5 | Log-loss classification P5 | NMAE Diabetes P5 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| R0 | 1.894× | 1.825× | 2.586× | 1.483× | 0.996× | 1.343× | 1.034× | 0.989× |
| C2 | 1.903× | 1.824× | 2.609× | 1.515× | 0.996× | 1.186× | 1.021× | 0.988× |
| C3 | 2.048× | 1.955× | 2.922× | 1.445× | 1.269× | 1.634× | 1.021× | 0.992× |
| C4 | 2.386× | 2.254× | 3.104× | 1.622× | 1.280× | 0.988× | 1.034× | 0.974× |

Aucune des quatre variantes n’est plus rapide sur le batch 1 dans les comparaisons V3 (fraction de paires plus rapides = 0 dans les 80 paires de chaque variante, sur les deux chemins). Les ratios de latence p50 batch 1 pipeline sont compris entre 1,82× et 2,25× ; au batch 256, entre 2,59× et 3,10×. Les temps de pipeline d’entraînement sont 1,44× à 1,62× ceux du MLP, avec la réserve méthodologique indiquée ci-dessus. Les tailles de tenseurs sont proches pour R0/C2, mais supérieures d’environ 27–28 % pour C3/C4. Ces mesures ne satisfont donc pas l’objectif prioritaire d’efficacité, même lorsque certaines métriques de qualité P5 sont favorables.

Les résultats P7 de temps mural d’entraînement confirmatoire, calculés directement depuis les 80 paires par variante, donnent en complément :
- R0 : ratio médian 3.376×, ratio moyen 3.414×, plus rapide dans 15/80 paires.
- C2 : ratio médian 1.418×, ratio moyen 1.541×, plus rapide dans 19/80 paires.
- C3 : ratio médian 1.534×, ratio moyen 1.728×, plus rapide dans 8/80 paires.
- C4 : ratio médian 1.661×, ratio moyen 2.005×, plus rapide dans 3/80 paires.

Ces ratios confirmatoires sont descriptifs et ne remplacent pas le protocole V3 P5.

**Réconciliation de comptage :** un message d’avancement antérieur avait attribué à P5 640 modèles et 256 000 latences. Ce comptage était incorrect et confondait une autre série d’artefacts avec le benchmark P5 canonique. Les chiffres faisant autorité sont ceux du gate P5 : 560 modèles et 1 075 200 latences. Les 640 modèles et 2 560 évaluations sont les chiffres de P7 (campagne confirmatoire test), pas P5.

## 7. Verdict scientifique

P7 fournit un résultat mixte et fortement dépendant de la tâche : certaines variantes HC-RBF sont non inférieures ou meilleures sur `f2_mul`, `f3_square_plus` et `f4_sin_product` en interpolation, mais aucune variante n’est non inférieure sur `f1_sin` avec la marge pré-enregistrée. La généralisation frontière est encourageante en moyenne ; l’extrapolation échoue nettement sur trois des quatre fonctions.

L’objectif prioritaire d’efficacité n’est pas atteint sur la plateforme et les tailles mesurées : R0/C2/C3/C4 sont toutes plus lentes que les MLP appariés, demandent davantage de temps de pipeline d’entraînement et présentent une mémoire de tenseurs plus élevée pour C3/C4. Les gains de micro-kernel P1 (vectorisation) ne se traduisent pas en performance de bout en bout ; le coût du modèle complet et des opérations RBF reste déterminant.

**Conclusion :** les résultats ne valident pas HC-RBF comme remplacement général ou plus efficace des MLP. Ils montrent des niches de qualité prédictive sur certaines fonctions et des limites d’extrapolation et de ressources qui réfutent toute revendication générale de supériorité à ce stade. Le résultat est négatif pour le critère prioritaire de rapidité/ressources, mixte pour la précision et la généralisation.

## 8. Limites

1. Les tests confirmatoires primaires concernent quatre fonctions synthétiques ; ils ne démontrent pas une généralisation à des domaines réels, à des réseaux profonds ou à des architectures neuronales générales.
2. Diabetes et classification ne disposent pas ici d’un test confirmatoire P7 ; leurs résultats P3/P5 sont exploratoires.
3. Les benchmarks de ressources sont CPU mono-thread sur la plateforme documentée ; aucun résultat GPU ou mesure énergétique n’est revendiqué.
4. La campagne de spécialistes P6 a identifié seulement sept centres répondant aux critères stricts stabilité+utilité, tous pour `g5_sin_mul_plus_square`, ce qui ne soutient pas une spécialisation générale.
5. Les lacunes de provenance P1_RUN_001/002 et les 123 lignes P6 v1 sans hash de script sont décrites dans des rapports distincts. Les scripts P7 et les artefacts gelés sont hashés.

## 9. Artefacts sources de ce rapport

- `09_analysis/P7/P7_TEST_SCORE_AUDIT.json` — audit 11/11.
- `09_analysis/P7/P7_TEST_PRIMARY_HOLM_16.csv` — 16 contrastes primaires complets.
- `09_analysis/P7/P7_TEST_PAIRED_SUMMARY.csv` — 64 résumés par tâche/variante/régime.
- `09_analysis/P7/P7_TEST_PAIRED_BY_SEED.csv` — données appariées par graine.
- `08_benchmarks/P7/P7_TEST_SCORE_REGISTRY.jsonl` — registre de scoring.
- `08_benchmarks/P7/P7_TEST_SCORING_SUMMARY.json` — résumé du scoring.
- `03_design/P7/P7_FINAL_MODEL_FREEZE.json` et `02_data/P7_confirmatory/P7_TEST_DATA_MANIFEST.json` — gels et manifests.
- `09_analysis/P5_V3_LATENCY_OVERALL.csv` et `P5_V3_PARETO_SCORECARD.csv` — agrégats canoniques de ressources.
- `04_code/audit_analyze_p7_test.py` — audit et analyse statistique.
- `04_code/generate_p7_confirmatory_final_report.py` — génération de ce rapport.

**Rédaction :** rapport généré à partir des registres et tableaux d’audit EX12. **Statut de signature :** document produit par le système d’analyse de cette session ; ce n’est pas une signature numérique certifiée ni une expertise judiciaire.
