# EX12_NEXT_0 — Rapport scientifique final et audit de complétude

**Date :** 4 novembre 2026  
**Version du protocole exécuté :** `prompt_ex12.json` v1.0.1 (amendement de capacité P_trainable)  
**Rapport scientifique directeur :** `rapport_prigramme_expermentale_EX12_NEXT_0.tex`  
**Workspace :** `EX12_NEXT_0/`  
**Périmètre :** phases P0 à P7, sans extension post hoc des holdouts.

## Résumé exécutif

EX12 a construit et évalué une famille HC-RBF (Hybrid Coverage-Adaptive Radial Basis Function) en comparaison avec des MLP appariés en nombre de paramètres entraînables. Le critère historique GE4X a été abandonné : le comparateur principal est à P_trainable ±1 %, et les paramètres stockés non entraînables, buffers, normaliseurs et octets de checkpoint sont reportés séparément.

Les phases P0–P7 ont chacune une porte PASS. Cela atteste la complétude et l'intégrité des campagnes selon leurs critères respectifs ; cela ne signifie pas que HC-RBF a gagné scientifiquement. Le verdict expérimental est **mixte sur la qualité prédictive, défavorable sur l'efficacité de bout en bout et faible en extrapolation**.

Sur les quatre tâches confirmatoires synthétiques P7, 11/16 contrastes primaires passent la non-infériorité ajustée (marge NMAE +0,02), et 7/16 rejettent l'égalité à zéro après correction bilatérale de Holm. Les résultats favorables dépendent de la tâche ; sur `f1_sin`, les quatre variantes HC-RBF sont battues en interpolation par le MLP apparié. En extrapolation, l'écart moyen candidat−MLP est +0,20559 NMAE sur les 16 contrastes et seulement 4/16 favorisent HC-RBF. Les benchmarks P5 canoniques montrent une latence batch 1 p50 de 1,82× à 2,25× le MLP sur le pipeline complet, un temps d'entraînement de pipeline enregistré de 1,44× à 1,62×, et une taille exacte des tenseurs de 1,00× pour R0/C2 et 1,27–1,28× pour C3/C4. Aucune variante ne satisfait donc les objectifs prioritaires de vitesse et de ressources sur le matériel mesuré.

La présente conclusion n'établit ni l'impossibilité d'améliorer HC-RBF, ni une supériorité générale du MLP pour tous problèmes. Elle décrit exactement le périmètre testé dans EX12.

## 1. Gouvernance, sources et protocole

### 1.1 Sources historiques consultées

L'archive `last_sources_3.zip` a été vérifiée et extraite récursivement dans `/mnt/data/last_sources_3` après rétablissement de l'accès par `/bin/sh`. Le processus avait `uid=0(root)`. L'extraction principale et les archives imbriquées ont passé les contrôles d'intégrité ZIP consignés dans P0.

Les prompts EX3, EX4, EX5, EX6, EX7, EX8 et EX11 ont été lus et audités. **Aucun `prompt_ex10.json` n'était présent** : les règles EX10 ont été reconstruuites à partir de son README, de ses rapports, scripts et audits, sans présenter ces pièces comme un prompt. EX7 réutilise le corps EX6 avec des addenda ; EX8 a deux jeux de métadonnées (v1.0 et v1.1) avec corps identique ; EX11 est identifié comme une reconstruction versionnée. `arch_up_test_0.zip` est absent de l'archive ; `arch_up_test_1.zip` est présent et a été audité. Ces absences ne sont pas comblées par des résultats inventés.

### 1.2 Règles rouges et équité

Le protocole interdit : d'inférer une réussite ou un échec avant les résultats ; de manipuler données, splits, seeds, métriques, modèles ou temps ; de supprimer les résultats défavorables ; de sélectionner sur test/holdout ; d'ajuster les prétraitements sur validation/test ; de relancer sélectivement des seeds ; de présenter un microbenchmark théorique comme une mesure matérielle ; de confondre inspectabilité et interprétabilité ; et de mélanger les anciens artefacts EX3–EX11 aux données EX12.

Les runs et registres sont append-only. Les échecs initiaux, interruptions, reprises, essais d'auditeur échoués et lacunes documentaires sont conservés et explicitement signalés.

### 1.3 Changement de critère de capacité

P0 a initialement enregistré une règle `P_total` héritée. L'analyse de conformité P4 a identifié que le rapport directeur exigeait en réalité un appariement de **paramètres entraînables** à ±1 %. La correction a été pré-enregistrée avant P4 additionnel et avant tout test P7 dans `PROMPT_CHANGE_CONTROL_v1.0.1.json`, et intégrée dans `prompt_ex12.json` v1.0.1. Le gel P7 vérifie 320 paires et un écart relatif maximal de 0,9238 %. Le GE4X historique n'est pas un objectif EX12.

## 2. Architecture et variantes réellement implémentées

Pour une entrée normalisée, l'encodeur partagé calcule `z(x)=tanh(W_e x+b_e)`. Les centres sont divisés en centres globaux fixes et centres locaux adaptatifs. Les largeurs diagonales positives sont bornées ; chaque centre produit une activation gaussienne `phi_k(x)=exp(-d_k²/2)` ; un readout radial combine les activations. C4 ajoute un chemin affine partagé sur la représentation latente. Aucun MLP caché n'est dissimulé dans le readout HC-RBF.

| Code | Implémentation / rôle | Statut expérimental |
|---|---|---|
| `M0_CORE` | MLP de référence apparié à R0/C2 dans les premières phases | Implémenté, entraîné P2/P3/P5 |
| `M0_AFFINE` | MLP de référence historique apparié à C4 | Implémenté, entraîné P2/P3/P5 |
| `M0_GRAPH` | MLP de contrôle du bras graphique | Implémenté et exploré en P2 |
| `R0` | RBF adaptative, centres locaux KMeans train-only | Implémenté, exploré puis candidat P3–P7 |
| `C1` | Centres globaux fixes uniquement | Implémenté et exploré en P2 ; non promu en P3 |
| `C2` | Centres locaux initialisés par sélection résiduelle diversifiée train-only | Implémenté, exploré puis candidat P3–P7 |
| `C3` | Couverture hybride centres globaux fixes + centres locaux adaptatifs | Implémenté, exploré puis candidat P3–P7 |
| `C4` | C3 + correction affine partagée | Implémenté, exploré puis candidat P3–P7 |
| `G1` | Graphe réel de coordination conditionnée par l'entrée | Implémenté et exploré en P2, non promu dans la campagne confirmatoire |
| `G2` | Contrôle graphe randomisé à séquence de degrés préservée | Implémenté et exploré en P2, non promu dans la campagne confirmatoire |
| `C5` | Modulation faible rang | Différé ; pas de variante P2 complète exécutée |
| `C6` | Sélection top-q parcimonieuse | Différé ; pas de variante P2 complète exécutée |

Le banc P1 a étudié des prototypes de kernels de distance, top-q, faible rang et messages dynamiques. Les kernels top-q, faible rang et messages dynamiques n'ont pas été promus dans le chemin de base : leur coût mesuré n'apportait pas de gain end-to-end fiable. Les prototypes P1 ne doivent pas être confondus avec des variantes C5/C6 entraînées et évaluées en P2/P3.

## 3. Résumé des phases et portes de validation

- **P0 — PASS, 17/17 :** inventaire, audit des prompts, intégrité ZIP, pré-enregistrement, graines et règles rouges.
- **P1 — PASS, 21/21 :** équivalence numérique des sorties/gradients et microbenchmarks CPU des kernels.
- **P2 — PASS, 17/17 :** criblage exploratoire train/validation, 80 configurations logiques et 10 variantes P2.
- **P3 — PASS, 19/19 :** 480 runs exploratoires multi-graines sur huit tâches, sans test/holdout.
- **P4 — PASS, 11/11 :** 320 paires appariées en paramètres entraînables à ±1 %, avec 160 MLP contrôles additionnels C3/C4.
- **P5 — PASS, 15/15 :** benchmark ressources V3 : 560 modèles, 13 440 cellules, 1 075 200 latences.
- **P6 — PASS, 24/24 :** ablations, permutations, diversité, stabilité inter-graines et falsification sur 320 modèles.
- **P7 — PASS, 12/12 :** gel de 640 modèles, génération des tests après gel, scoring unique et audit confirmatoire.

Le PASS de chaque phase signifie que les critères de complétude et d'intégrité de cette phase ont été vérifiés ; le PASS n'est jamais interprété comme un résultat prédictif positif.

## 4. Résultats détaillés par phase

### P1 — kernels et équivalence informatique

Deux microbenchmarks canoniques indépendants (RUN003/RUN004) ont chacun passé 126 cas numériques et 24 000 mesures brutes. L'erreur maximale de sortie complète est 0 ; l'erreur maximale de gradient est `2,98×10⁻⁸`, sous tolérance `1e-6`. Le broadcasting a une accélération médiane de 8,46× et 8,89× contre la référence à boucles ; l'accélération du chemin HC complet est 4,16× et 4,25× sur CPU.

Le top-q a été plus lent que le calcul dense dans toutes les comparaisons appariées du protocole ; le faible rang et les messages à trois tours présentent également un coût élevé. La vectorisation améliore le noyau mais ne garantit pas une accélération de l'architecture complète.

**Lacune de reproductibilité :** les fichiers de résultats P1_RUN_001 et P1_RUN_002 sont conservés, mais leurs scripts source exacts ne sont pas récupérés. RUN001 est un prototype numérique échoué ; RUN002 est exclu des comparaisons top-q non équivalentes. RUN003/RUN004 ont scripts et hashes exacts. Voir `RAPPORT_LACUNES_REPRODUCTIBILITE_P1_RUN001_RUN002.md`.

### P2 — criblage exploratoire contrôlé

Le registre contient 80 succès logiques, 80 premières tentatives échouées (erreur `yva` manquante), et six interruptions de reprise ; ces échecs et interruptions restent conservés. Dix variantes P2 ont été réellement implémentées/explorées : trois baselines MLP (CORE/AFFINE/GRAPH), R0, C1, C2, C3, C4, G1 et G2. C5/C6 restent `DEFERRED_NOT_IMPLEMENTED`.

Le criblage a retenu R0/C2/C3/C4 pour P3. Ce résultat de deux seeds et quatre fonctions est exploratoire, pas confirmatoire.

### P3 — tâches et généralisation exploratoires

480 runs logiques sur huit tâches et dix seeds : quatre fonctions principales (`f1` à `f4`), deux compositions diagnostiques (`g5`,`g6`), Diabetes tabulaire et classification binaire synthétique. Six slots de modèles : R0/C2/C3/C4 et deux MLP initiaux. 71 fichiers/664 arrays de données contrôlés ; 1 620 métriques recalculées ; 13 premières tentatives d'audit échouées conservées, sans interruption non résolue.

Les NMAE moyennes d'interpolation sur dix seeds montrent des résultats dépendant de la fonction : `f1_sin` défavorise toutes les sondes (MLP 0,1050 contre HC-RBF 0,1741–0,2792) ; `f2_mul` favorise HC-RBF (MLP 0,0700, HC-RBF 0,0203–0,0327) ; `f3_square_plus` favorise certaines sondes (MLP 0,0767, C4 0,0367) ; `f4_sin_product` favorise R0/C2 et certains cas. Les tâches `g5/g6` demeurent diagnostiques.

Sur classification binaire synthétique, les log-loss HC-RBF restent supérieures aux MLP appariés : deltas moyens +0,0197 (R0), +0,0116 (C2), +0,0187 (C3), +0,0328 (C4). Sur Diabetes validation, les NMAE HC-RBF sont légèrement inférieures dans ce split unique ; le holdout de 67 observations reste scellé.

### P4 — appariement MLP

L'audit a détecté que le `P_total` pouvait masquer une différence de paramètres entraînables. 160 MLP contrôles supplémentaires ont été entraînés pour C3/C4 ; 320 paires candidates–MLP passent la contrainte `P_trainable ±1 %`. Les 8 960 valeurs de métriques et 2 800 empreintes de fichiers sont recalculées/vérifiées sans divergence. Le test/holdout est resté inaccessible. Les anciennes synthèses `P_total` sont conservées comme analyses historiques mais supersédées pour l'équité principale.

### P5 — ressources canoniques

Le gate P5 canonique est basé sur 560 modèles, 13 440 cellules de timing, 1 075 200 latences élémentaires, 2 560 lignes de latence appariées, 320 paires mémoire et 320 paires de temps de pipeline. CPU mono-thread, float32, batches 1/16/64/256, deux chemins, 3 blocs indépendants de 80 mesures. Les ratios p50 pipeline batch 1 candidat/MLP sont R0 1,825×, C2 1,824×, C3 1,955×, C4 2,254× ; au batch 256 ils sont 2,586×, 2,609×, 2,922×, 3,104×. Fraction de paires plus rapides au batch 1 : 0 pour les quatre variantes.

Les ratios de temps de pipeline enregistrés sont R0 1,483×, C2 1,515×, C3 1,445×, C4 1,622×. Ce temps inclut initialisation, validation, diagnostics et écritures ; ce n'est pas un chronométrage pur de l'optimiseur. Les rapports de stockage exact des tenseurs sont R0 0,996×, C2 0,996×, C3 1,269×, C4 1,280×. Aucun GPU ni compteur d'énergie n'était disponible ; RSS est process-level, non attribuable à un modèle isolé.

**Lacune de reproductibilité :** le script V2 exact référencé par 13 416 cellules historiques n'a pas été retrouvé. Les données sont conservées ; une reproduction V3 indépendante et hashée couvre 13 440 cellules et est comparée aux anciennes. Voir `RAPPORT_LACUNE_REPRODUCTIBILITE_P5_V2.md` et `P5_RESOURCE_REPORT_V3.md`.

**Erratum de comptage :** une synthèse d'avancement avait attribué 640 modèles/256 000 latences à P5. C'était une confusion avec des artefacts P7 ; les comptes canoniques P5 sont 560 modèles et 1 075 200 latences. Voir `10_reports/P5/P5_COUNT_RECONCILIATION.md`.

### P6 — complémentarité et spécialisation

320 modèles candidats, 10 240 unités modèle-centre, 34 560 lignes d'ablation, 1 600 permutations invariantes, 1 440 paires modèles cross-seed, 46 080 appariements centre-centre et 1 024 hypothèses de rôle. Aucune divergence d'intégrité P3/P6 détectée. Les permutations sont group-preserving et respectent les tolérances numériques pré-enregistrées.

Résultat scientifique : 549/1 024 centres passent le seuil de stabilité, 9/1 024 passent le test d'utilité après Holm, et seulement **7/1 024** passent les deux. Les sept sont limités à `g5_sin_mul_plus_square` : C2=3, C3=2, C4=2, R0=0. La spécialisation utile et stable n'est donc pas une propriété générale de l'architecture.

**Lacune de traçabilité :** 123 terminal records P6 v1 ne contiennent pas le hash du script exécuté, même si la source v1 existe actuellement. Le lien cryptographique exact au moment de ces 123 exécutions ne peut pas être prouvé depuis les lignes terminales. Une NPZ partielle d'une tentative interrompue est conservée comme artefact orphelin attendu.

**Incident `manifest_map` :** le rapport séparé `P6_MANIFEST_MAP_INCIDENT_REPORT.pdf` et son dossier d'audit montrent que le manifeste persistant `P3_DATA_MANIFEST.json` est présent (71 entrées), que les runners P6 contiennent la fonction `load_manifest_map()`, et que 320/320 sources se rapprochent sans fichier manquant ni divergence SHA-256. L'audit n'a trouvé aucune suppression persistante ou altération des données. L'incident ne constitue pas une preuve de sabotage.

### P7 — confirmation finale

P7 a gelé 640 modèles (4 tâches primaires × 20 graines × 8 slots), 320 paires candidates–MLP, 4 257 artefacts pré-test et les scripts. La génération test a eu lieu après gel : 80 fichiers, 640 arrays, quatre régimes et 1 000 observations par régime. Scoring unique : 640 modèles × 4 régimes = 2 560 évaluations ; audit 11/11, aucune divergence et aucune sélection/réentraînement après le test.

La métrique primaire est NMAE normalisée par l'écart-type de cible calculé sur train. Sur les 16 contrastes d'interpolation, 11 passent la non-infériorité ajustée (marge +0,02), et 7 montrent une différence significative après Holm bilatéral. Trois contrastes significatifs défavorisent les sondes sur `f1_sin` ; quatre favorisent des variantes sur `f3_square_plus` et `f4_sin_product`. Aucune variante ne gagne universellement.

Par régime, les différences moyennes NMAE candidat−MLP sont interpolation −0,00571, frontière −0,03192, extrapolation +0,20559, shift +0,00298. L'extrapolation est fortement défavorable sur `f1_sin`, `f2_mul`, `f3_square_plus` (toutes les variantes sont plus mauvaises que leur MLP) ; seul `f4_sin_product` est favorable aux sondes en moyenne. La frontière favorise HC-RBF dans 15/16 contrastes. Le shift est variable par tâche.

Le rapport détaillé P7 et tous les tableaux par seed sont dans `10_reports/P7/P7_CONFIRMATORY_FINAL_REPORT.md` et `09_analysis/P7/`. Aucun test confirmatoire de Diabetes ou de classification n'a été réalisé dans P7 ; leurs résultats P3/P5 ne sont pas promus en résultats de test. Le protocole P7 primaire porte sur les quatre fonctions synthétiques déclarées.

## 5. Lacunes documentaires et reproductibilité

Les lacunes suivantes sont explicitement conservées, sans conclusion non démontrée de sabotage ou de vol :

1. `prompt_ex10.json` absent ; protocole EX10 reconstruit depuis les artefacts EX10 disponibles.
2. `arch_up_test_0.zip` absent ; aucune donnée ni aucun résultat EX0 inféré.
3. Scripts sources exacts P1_RUN_001/002 absents ; résultats et logs conservés, mais reproduction byte-identique non démontrable. RUN003/004 sont canoniques et reproductibles.
4. Script P5 V2 exact absent pour 13 416 cellules ; reproduction indépendante V3 complète, hashée et comparée. Les 13 440 cellules V3 sont reproductibles.
5. 123 lignes terminales P6 v1 sans hash de script ; source v1 actuelle disponible, mais identité historique des octets non attestée cryptographiquement.
6. P0 initial `P_total` a été corrigé par addendum v1.0.1 et règle P4 `P_trainable`; les documents historiques restent conservés et explicitement supersédés.

Aucun de ces points ne prouve une intention de sabotage. Un défaut de traçabilité est un défaut de traçabilité ; il doit être documenté et corrigé, sans lui attribuer une cause intentionnelle en l'absence d'éléments.

## 6. Réponse aux critères de recherche

| Critère | Résultat EX12 |
|---|---|
| Qualité prédictive vs MLP | Mixte ; 11/16 non-infériorités en interpolation, mais dépendance forte à la tâche. Classification pilote : log-loss HC-RBF moins bonne. |
| Paramètres à égalité | PASS ; 320 comparaisons P4 et 320 paires P7 à P_trainable ±1 %. GE4X abandonné. |
| Ressources | Échec de l'objectif prioritaire sur CPU mesuré : latence p50 pipeline batch 1 ≈1,82–2,25× MLP ; stockage C3/C4 plus élevé. |
| Entraînement plus rapide | Non démontré ; ratios de pipeline P5 1,44–1,62× et temps mural P7 >1× pour les médianes des quatre variantes. |
| Généralisation | Frontière souvent favorable ; extrapolation défavorable sur trois des quatre tâches confirmatoires ; shift dépend de la tâche. |

## 7. Conclusion générale

EX12 ne valide pas l'hypothèse que HC-RBF remplace généralement un MLP plus efficacement à capacité entraînable égale. L'architecture est mathématiquement spécifiée, plusieurs variantes ont été réellement implémentées et comparées, certaines fonctions montrent un avantage qualitatif, et le mécanisme de couverture apporte des diagnostics mesurables. Cependant, les coûts de calcul et d'entraînement sont nettement plus élevés sur la plateforme CPU mesurée, l'extrapolation reste fragile et la complémentarité des centres n'est prouvée que dans un petit nombre de cas.

Les acquis principaux sont : un protocole d'évaluation strict, une architecture HC-RBF complètement spécifiée, un noyau vectorisé numériquement équivalent, une confrontation à P_trainable égal, une campagne multi-graines et un test confirmatoire verrouillé. Les résultats négatifs et les lacunes de provenance sont conservés et rapportés. Le verdict est donc **scientifiquement mixte mais négatif au regard de l'objectif prioritaire de vitesse/ressources**.

Aucun résultat ne permet d'affirmer une manipulation ou un sabotage des expériences. Les défauts techniques identifiés (scripts manquants, hashes historiques absents, compteurs d'audit corrigés, reports de schéma) sont documentés dans les fichiers d'audit correspondants.

## 8. Carte des livrables et reproduction

- `prompt_ex12.json` et `prompt_ex12_v1.0.0_frozen.json` : prompt exécuté et version d'origine figée ; addendum de changement : `00_governance/PROMPT_CHANGE_CONTROL_v1.0.1.json`.
- `03_design/HC_RBF_FORMAL_SPEC.md` : formalisation architecturale détaillée.
- `04_code/` : scripts de génération, entraînement, évaluation, benchmark, audit, analyse statistique et rapport.
- `05_configs/` : configurations versionnées.
- `06_runs/` et `07_checkpoints/` : modèles, checkpoints, historiques et résultats par run.
- `08_benchmarks/` : registres append-only, latences brutes, benchmarks et scoring.
- `09_analysis/` : métriques recalculées, comparaisons, intervalles, tests et contrôles d'intégrité.
- `10_reports/` : rapports P0–P7, rapports de lacunes, incident `manifest_map`, présent rapport et rapport confirmatoire P7.
- `11_reproducibility/` : versions et commandes de reproduction.
- `12_release/` : manifeste de livraison, checksums et audit de complétude.

Les commandes exactes et versions de bibliothèques sont décrites dans `11_reproducibility/` et dans les métadonnées des runs. Les scripts d'entraînement et de scoring ne chargent jamais les sources historiques. Le paquet de livraison est contrôlé pour ne contenir que des artefacts EX12 ; `last_sources_3`, les anciens workspaces EX3–EX11, archives, sauvegardes et holdouts scellés en sont exclus.

## 9. Signature et portée

**Rédacteur :** ChatGPT, assistant OpenAI — rapport généré à partir des artefacts et registres présents dans `EX12_NEXT_0`, le 4 novembre 2026.

Cette signature est une attribution de rédaction à l'agent. Elle n'est pas une signature numérique certifiée, une certification de personne physique, ni une expertise judiciaire. Les SHA-256 et manifestes du paquet sont fournis séparément pour permettre une vérification technique indépendante.
