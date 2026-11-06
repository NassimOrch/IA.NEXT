# Rapport de livraison incrémentale AAM O94_3

## Description

O94_3 corrige le parcours « Observer » d’O94_2. Le mode d’observation passive démarre une collecte depuis une source sélectionnée et autorisée; il crée lui-même le JSONL et le rapport d’arrêt. Il ne réclame pas un fichier `blackbox_live.jsonl` préfabriqué. L’import de traces existantes, le sondage actif d’un processus qui parle JSON Lines et la capture passive sont des parcours distincts.

## Architecture

- Collecteur filesystem : observe les créations, modifications et suppressions pendant la session, garde une séquence et une chaîne de hashes, exclut ses propres sorties du périmètre surveillé, respecte les budgets et écrit le rapport final.
- Collecteur de processus : échantillonne les informations exposées pour un PID choisi; les accès refusés restent des erreurs déclarées.
- Collecteur réseau : adaptateur TShark avec métadonnées/PCAPNG et option explicite pour les payloads. Les tests sont exécutés avec fixtures; aucune capture réelle sur carte réseau n’est déclarée dans cet environnement.
- Intégration de modèles : backends Transformers local, TorchScript PyTorch local, adaptateur d’architecture pour `state_dict`, Ollama et endpoint OpenAI-compatible; les secrets ne sont pas écrits dans la configuration persistée.
- Composition : catalogue de compétences/méthodes/règles, candidats tirés des traces, séparation train/holdout, compilation DSL vers artefact JSON versionné et exécution bornée.
- RAG : moteur sémantique, retrieval O92 et six fichiers historiques protégés conservés byte-à-byte; les tests de RAG/SMS/résolution restent séparés de l’observation.

## Pipeline complet

1. Préflight : consultation de `chemins_O94.json`, formalismes, checklists séquentielles et registres d’erreurs parent/incrémentaux.
2. Observation : sélection d’une source autorisée et d’un budget; démarrage du worker; collecte; production automatique de la trace et du rapport.
3. Analyse : vérification des séquences, hashes, types d’événement et erreurs d’accès.
4. Acquisition de briques : exact-lookup uniquement pour les cas train non ambigus; méthodes/règles depuis l’observation passive restent candidates avec revue nécessaire.
5. Composition : compilation DSL, validation des références, écriture de l’artefact, test séparé.
6. Intégration : tests locaux et fixtures des adaptateurs; le vrai service externe n’est pas simulé comme s’il était disponible.
7. Non-régression : tests RAG/SMS, comparaison SHA-256 des fichiers protégés, lots historiques segmentés.
8. Sauvegarde et livraison : savepoint intégré, manifests internes, CRC, extraction propre et tests depuis l’extraction.

## Commandes principales

```bash
python -m compileall -q aam_o93 tests scripts
python -m pytest -q tests/test_o943_passive_observation.py tests/test_o943_cli_live_e2e.py
python -m pytest -q tests/test_o943_learned_blocks_and_composition.py
xvfb-run -a python -m pytest -q tests/test_o943_ui_contracts.py
python -m pytest -q tests/test_p3_semantic_rag.py tests/test_o940_rag_resolution.py tests/test_o940_real_sms_corpus_sample.py tests/test_o940_real_sms_retrieval.py tests/test_o940_memory_resolution.py tests/test_o94_rag_adaptive.py
python -m aam_o93 observe-live --source-kind filesystem --authorize-source --root ./dossier_a_observer --seconds 10 --interval .05 --max-events 5000
```

Le chemin `observe-live` doit créer sa trace à la demande. La commande n’exige aucun JSONL préalable.

## Résultats

- RAG/SMS/résolution/adaptatif : 47 tests passés en régression P5.
- Parité RAG : 6 fichiers protégés identiques par SHA-256 à O94_2; le rapport `rapport_O94_3/rag_parity_O94_0_O94_1_O94_2.json` compare également les versions parentes historiques.
- Régression P6 : 15 lots `PASS_BOUNDED`, 60 fichiers de tests P6 couverts exactement une fois, sans omission ni doublon; 321 tests et 21 sous-tests déclarés passés. Avec P5 : 368 tests rapportés.
- Compilation Python : `compileall` a examiné 328 fichiers Python sans erreur.
- Documents : `formalisme_O94_3.tex` et `laboratoire_O94_3.tex` compilent chacun deux fois avec `pdflatex -halt-on-error`.
- Observation live filesystem/CLI, UI scroll, TorchScript CPU et composition DSL passent leurs tests ciblés; l’archive finale et ses contrôles sont consignés dans le manifeste externe `O94_3_final_delivery_verification.json`.

## Interprétation

Les résultats prouvent les comportements testés dans leur périmètre, pas la reconstruction générale de tout programme arbitraire. Une observation de fichiers ou de métadonnées de processus ne révèle pas automatiquement une architecture interne. Le lookup exact d’exemples connus ne démontre pas une généralisation hors domaine.

## Conséquences théoriques, conceptuelles et opérationnelles

- Théoriques : séparation nette entre observation passive, sondage actif, import dataset et inférence de compétence.
- Conceptuelles : une observation passive fournit des événements et des invariants candidats; il faut des preuves distinctes pour promouvoir une méthode/règle en compétence exécutable.
- Opérationnelles : les traces sont créées par AAM; les budgets et erreurs sont visibles; les collecteurs dépendent des sources et permissions locales; les modèles externes réels doivent être fournis par l’utilisateur.

## Conclusion et statut

O94_3 corrige les défauts identifiés dans l’observation live, la visibilité des modèles, le défilement et la composition tout en préservant le RAG historique. La capture réseau réelle sur une interface, un fournisseur LLM distant, les capteurs physiques et le clonage généralisé d’un logiciel restent des périmètres non démontrés dans cet environnement; ils ne sont ni déclarés impossibles ni présentés à tort comme déjà réalisés.


## Retest P8 — cycle d’arrêt réseau et rapport

La première extraction candidate a échoué dans le test du backend TShark/dumpcap simulé : le JSONL et le PCAPNG étaient créés, mais l’appel d’arrêt pouvait retourner avant que le rapport final soit écrit. Le diagnostic isolé a confirmé que le rapport existait après une attente plus longue. La cause était un nettoyage réseau redondant (dans `_run_network` puis dans `_finalize`) associé à une fenêtre de jointure courte.

Correction : le finaliseur central est désormais l’unique propriétaire de l’arrêt des outils, le délai d’attente par défaut de `stop()` est porté à 10 secondes, et le test réseau exige explicitement `worker_alive=false` ainsi que la présence du rapport. Le retest ciblé passe (1 test) et le gate/préflight post-correction retourne `PASS_BOUNDED`. Le premier échec et ses reçus restent conservés dans `P8_candidate_verification.json` et le registre d’incidents ; la reconstruction complète du candidat est nécessaire avant la clôture P8.


### Candidat extrait après correction

Le premier candidat (SHA-256 `d1fb9562fd6c03f83529ab363c1423aa88e62a03b2abbf813201892b61f77de1`) est conservé comme tentative historique en échec dans `receipts/O94_3/P8_candidate_attempt1_failure.json`; il échouait à l’arrêt du backend réseau avant l’écriture du rapport. Après correction et retest, le nouveau candidat (SHA-256 `719cb17d1cab84a8b261aed0c4c2dd8cc91926410fc61371c4ff0e3dbb3bdc88`) passe après extraction fraîche : `compileall` réussi, 19 tests live/UI/adaptateurs/composition réussis, 47 tests RAG/SMS/résolution réussis, commandes CLI réussies et contrôles d’intégrité ZIP/manifestes réussis. Le total des deux lots pytest ciblés est de 66 tests réussis sur ce candidat.
