# Audit de eLLM_v0 — version 0.2.0

Ce dossier regroupe les scripts de vérification, les résultats de tests et d'expériences, les captures Chromium, le smoke du serveur/CLI, les incidents historiques conservés et les rapports/formalismes LaTeX.

## Lecture recommandée

1. `reports/rapport_eLLM_v0.tex` décrit l'ensemble du processus selon le format demandé : description, architecture, pipeline complet, commandes, résultats, interprétations, conséquences, conclusions et statut.
2. `reports/formalime_model_eLLM_v0.tex` détaille les équations réellement instanciées dans le code. Le nom `formalisme_model_eLLM_v0.tex` est fourni comme alias orthographique identique.
3. `final_integration_smoke.json`, `browser_ui_test.json` et `experiments/` contiennent les résultats agrégés ; le dossier `logs/` contient les journaux correspondants.
4. `incidents/` conserve les erreurs rencontrées, leurs corrections et leur statut, au lieu de les effacer de l'historique.
5. `MANIFEST_SHA256.json` permet de vérifier les fichiers de l'archive après extraction.

## Résultats importants

- Le checkpoint du modèle contient un prédicteur probabiliste interpolé à n-grammes variables, pas un Transformer.
- Corpus de démonstration : 80 paragraphes ; split de livraison 64/8/8 ; checkpoint SHA-256 `3e42677b469937ba688022c30d968752c412c09eaabe3d826d2712f6e84590dc`.
- Perplexité du test réservé : 217.0393 contre 449.9162 pour le baseline unigramme sur le même split.
- Suite finale : 38 tests unitaires/HTTP ; smoke serveur/CLI : 17 contrôles ; Chromium DOM avec API mockée : PASS.
- Invariants structurels : 80 états, 512000 triplets, zéro violation dans le domaine fini enregistré.
- Validation de portabilité après extraction propre : 38/38 tests et routes locales principales PASS; détails dans `experiments/clean_extraction_portability.json`.

Ces résultats ne certifient pas une compréhension générale ni une performance sur des corpus externes. Le rapport documente leur portée précise.

## Rejouer les contrôles

En extrayant les trois archives dans un même dossier, lancer les commandes du rapport depuis `Dmodel_eLLM_v0/`. Les scripts d'audit résolvent leur racine relativement à leur propre fichier et peuvent être exécutés depuis `Amodel_eLLM_v0/`. Certaines expériences nécessitent Playwright/Chromium pour le test navigateur ; cela concerne l'audit seulement, pas l'application livrée.
