# Rapport de clôture documentaire et d'intégrité EX5 — v001 à v007

Date : 30 octobre 2026. Prompt actif : EX5 révision 1.1, SHA-256 `88f67fc34bf34c5ca0817da42a057ed71dfb092cfb33720be5532da96bab3291`.

## 1. Portée du contrôle

Le prompt contient les sections 0 à 17. Les exigences de reprise non redondante, conservation des sources, RETRO/Adam, proportions fixe/adaptative, optimisation micro-MIXA, alternance A↔B, deux niveaux question/réponse, OOF, comparateurs MLP, transferts, ressources, anti-triche et livrables sont reliées à des scripts, registres, checkpoints, prédictions et rapports dans v001–v007. Le tableau de conformité demeure l'autorité pour le statut de chaque sous-exigence ; la présence d'un artefact ne signifie pas que le critère scientifique correspondant est réussi.

## 2. Exhaustivité des familles livrées

Le catalogue compte 338 couples candidat/registre explicites, 53 registres JSONL, 1 608 lignes avec identifiant candidat, et les familles : RETRO/Adam, proportions/gates/géométries micro-MIXA, partage encodeur/centres, PCA question-only, alternance correctrice, hiérarchie Q/A, résidu OOF, comparateurs MLP, transfert externe et profilage CPU. Les scripts, configs, données/manifests, modèles/reprises, prédictions et agrégats sont recensés par version dans `catalogue_artifacts_versions_ex5.json`; l'index des campagnes fournit la liaison scripts↔registres↔données↔tests.

## 3. OOF — audit de complétude

La branche `TWO_LEVEL_OOF_RESIDUAL` comprend les scripts source et dépendances ; cinq graines × cinq folds (25 modèles base), 25 checkpoints optimizer-resume, 25 marqueurs de fin, cinq caches OOF, dix composites finaux (deux têtes × cinq graines), dix états optimizer-resume de tête, dix métriques, dix prédictions et vingt liens MLP. Le manifeste comprend 162 entrées et zéro manque requis. Chaque train-row reçoit une prédiction issue du fold qui ne l'a pas entraînée ; les partitions des folds sont des compléments exacts, les logits OOF, logits validation, prédictions du composite et métriques sont reproduits avec écart maximal 0. Le forward de l'ensemble est `forward(self, x)` et aucun accès test n'est déclaré.

L'appariement utilise dix modèles MLP physiques existants, partagés explicitement par budget total et graine, pour 20 liens logiques : dix matched et dix ge4x. `P_sonde_total=1160`, `P_MLP_ge4x=4649`, donc ratio `4.00775862`. Aucun MLP n'a été réentraîné pour cette formalisation.

## 4. Nomenclature canonique

`MIXA` désigne la famille générique définie dans EX3 ; `micro-MIXA` désigne la reconstruction compacte définie en EX4 et étudiée en EX5. `MiXA`/`mixa` sont des alias de casse de `MIXA`; `micro-MiXA`/`micro-mixa` sont des alias de casse de `micro-MIXA`. `mixa_micro_d4_k8` est un identifiant historique relié à micro-MIXA. Aucune implémentation ou résultat distinct n'a été retrouvé sous les graphies de casse. La valeur 528 coefficients des débris reste non vérifiable. Les registres bruts conservent leurs noms d'origine.

## 5. Tests et intégrité

Tests versionnés : v001 final integrity et sémantique Adam PASS ; v002 gel alterné et sémantique Adam PASS ; v003 séparation externe PASS ; v004 deux tests PASS ; v005 un test PASS ; v006 trois tests PASS. Les trois fonctions de test v007 ont été invoquées individuellement et passent ; une collecte pytest globale a dépassé la fenêtre de commande, donc aucune suite globale v007 PASS n'est revendiquée. Les deux tests OOF (ancien appariement et audit de tous les artefacts) donnent quatre tests PASS au total.

Audit global versions : 1 850 JSON valides ; 53 JSONL / 1 720 lignes ; 1 313 références checkpoint sans erreur ; 1 162 références de prédiction canoniques sans erreur ; 40 pointeurs historiques superseded préservés ; 826 prédictions recalculées sans divergence ; 437 liens MLP ge4x, minimum 4.000735×.

Audit workspace final : 3 951 fichiers non-cache ; 1 865 JSON valides ; 53 JSONL et 1 720 lignes valides ; 60 CSV rectangulaires ; zéro erreur parsing/forme ; prompt externe/interne identique au SHA attendu ; aucun symlink sortant. Manifeste : `sha256_manifest_workspace_final.csv`.

## 6. Exceptions et limites

Les doublons et anciennes pointeurs sont conservés, signalés et traités dans les agrégats sans altérer les sources. Les prototypes compilés ne passant pas la parité stricte sont explicitement exclus. Banknote/MAGIC n'ont pas pu être téléchargés à cause du DNS runtime ; aucun résultat n'est inventé. L'environnement est CPU-only : énergie et VRAM non mesurées ; les MACs complets d'entraînement et une télémétrie RSS homogène restent indisponibles. Les comparaisons externes Wine/Digits ne démontrent aucune non-infériorité conjointe.

## 7. Verdict

L'exécution et l'audit des axes réalisables sont documentés jusqu'à v007. Les livrables couvrent les familles, scripts, données, comparateurs et variantes, dont l'OOF complète. Cependant, plusieurs exigences obligatoires restent bloquées/non mesurées et aucune candidate ne franchit la règle rouge de bout en bout. **EX5 n'est pas déclaré intégralement satisfait au sens de réussite scientifique.**
