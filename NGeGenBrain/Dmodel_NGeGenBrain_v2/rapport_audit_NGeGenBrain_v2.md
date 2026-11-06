# Rapport d’audit — NGeGenBrain_v2

- Date : `2026-10-27`.
- Version : `2.0.0.dev0` (version de développement instrumentable).
- Exécution officielle : `20261027T153351Z`.
- Espace d'expérience actif : `benchmarks/results/20261027_official/workspace_20261027T153351Z`.
- Origine : sources/tests V1 conservés dans `legacy_NGeGenBrain_v1/`; archives de référence conservées dans `references/`.

## 1. Portée de l'audit

Audit de la structure V1, conservation des capacités de l'ancienne suite, formalisme V2, code, tests, CLI, interface Web locale, laboratoire synthétique, journaux chaînés, intégrité JSON/ZIP, rapport LaTeX et préparation de livraison. Aucune architecture V1 n'a été remplacée silencieusement. La cartographie formalisme→modules→tests→preuves se trouve dans `NGeGenBrain_v2_mise_en_oeuvre.json`, `chemins_NGeGenBrain_v2.json` et `preuves_NGeGenBrain_v2.json`.

## 2. Vérifications logicielles exécutées

- Compilation Python (`compileall`) : PASS.
- Compilation du formalisme LaTeX avec `pdflatex -halt-on-error` dans un répertoire temporaire : PASS.
- Tests V2 : **52/52 passés**, journal `audit/test_runs/v2_unit_integration_tests_final.log` (exécution indépendante enregistrée).
- Tests de régression V1 : **65/65 passés**, journal `audit/test_runs/v1_preserved_regression_tests_final.log`.
- CLI : initialisation, benchmark aveugle, audit des registres, composition, découverte numérique, planification, contre-exemples, balayage causal, ladder synthétique : PASS.
- JSON du projet : **83/83 fichiers JSON parsés sans erreur** au contrôle source de cette version; la liste détaillée est dans `audit/validation_receipt.json`.
- Les trois archives V1 de référence embarquées ont passé `zipfile.testzip()` (**3/3 CRC valides**).
- Registres de l'expérience officielle : tous les hash-chains sont valides.

Reçu détaillé : `audit/validation_receipt.json`; reçu des contrôles par composants : `audit/component_validation_receipt.json`; résumé : `audit/validation_summary.md`. Les 17 contrôles composants documentés ont passé individuellement. La génération du package et le contrôle clean-room des archives restent des étapes séparées. Les tests V1/V2 ont été exécutés séparément avec sorties brutes rattachées par hash. Une tentative d'exécution globale dépassait le budget temporel du superviseur d'outil; cet arrêt n'est pas codé ni interprété comme un résultat de test.

- Un défaut de résolution d’imports entre `reconstruction.py` et le paquet `reconstruction/` a été détecté par la vérification CLI clean-room, corrigé en déplaçant l’implémentation publique vers `reconstruction/engine.py` et en exportant explicitement l’API du paquet. Deux tests de non-régression couvrent désormais cet import ; la CLI a été relancée après correction.

## 3. Évidence expérimentale principale

- Benchmark : `SYNTH-PARITY-4`.
- Lignes discovery : `12` ; holdout : `4`.
- Exactitude holdout : `1.0` ; exactitude de la table finie interrogée : `1.0`.
- Échelle d'instrumentation : `8` architectures synthétiques, dont mini-Transformer encodeur et mini-Transformer causal génératif. Cette échelle teste forward/capture/intervention/génération, elle ne prouve pas la reconstruction de chaque modèle.
- Intervention locale `zero` sur `xor_layers.0.positive`, entrée `[1,0,0,0]` : delta L2 `2.0`.
- Balayage : `8` entrées, `2` effets non nuls, `6` effets nuls.
- Contrôle négatif positif : candidat incomplet détecté comme erroné sur `8` lignes, avec `4` contre-exemples.

## 4. Réserve concernant un véritable LLM

Aucun modèle pré-entraîné Hugging Face n'a été chargé : `transformers` et un checkpoint local n'étaient pas disponibles, et l'installation de dépendances distantes n'a pas été possible dans cet environnement. L'adapter local Hugging Face est livré, mais non validé ici sur un checkpoint réel. **L'analyse et la recomposition d'un LLM externe sont donc NON EXÉCUTÉES**; ce constat ne démontre ni réussite ni échec de la méthode.

## 5. Risques et périmètre

- Les méthodes de découverte opèrent dans des classes/grammaires déclarées, pas dans une classe universelle de toutes les fonctions possibles.
- L'intervention causale est limitée aux capacités effectivement fournies par l'adapter et aux entrées testées.
- La reconstruction actuelle valide une fonction booléenne finie et symbolique; elle ne récupère pas les poids et ne prouve pas l'équivalence causale d'un réseau.
- Le graphe de circuits est un graphe d'influences observées et de dépendances; il ne constitue pas à lui seul une ontologie causale exhaustive.
- L'interface Web est volontairement locale (loopback) et l'adapter HF a `trust_remote_code=False`, `local_files_only=True` par défaut.
- Les archives finales et leur clean-room verification sont documentées dans `cleanroom_archive_validation_receipt.json` dans le bundle d'audit/suivi final; le dépôt de travail contient le reçu source ci-dessus.

## 6.1 Recherche affine sur vocabulaire large

La suite de tests comprend deux contrôles dédiés à la recherche sur des vocabulaires plus grands : une recherche sur un vocabulaire synthétique de 32 000 tokens dans la classe `small_coefficient_modular_affine_v1`, puis un test du sélecteur `auto` avec vocabulaire 257. La première vérifie une règle cible dans la classe de coefficients déclarée `{−1,0,1}` (9 paires de coefficients, puis calcul du biais depuis les données d'entraînement), avec une complexité annoncée `O(9*n)`. Ces essais valident l'implémentation et la recherche sur les données synthétiques du test ; ils ne démontrent pas la découverte d'une règle arbitraire dans un LLM réel.

## 7. Conclusion d'audit

Les éléments livrés étayent les fonctionnalités explicitement testées, dans leur domaine exact. Ils n'étayent aucune affirmation de reconstruction complète d'un LLM pré-entraîné. Les systèmes de validation et de traçabilité ne préprogramment ni réussite ni échec : ils enregistrent les résultats obtenus, les limites de portée, les contre-exemples et les expériences non exécutées.
