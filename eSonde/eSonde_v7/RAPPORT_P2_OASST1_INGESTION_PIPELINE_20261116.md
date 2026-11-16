# Rapport P2 — pipeline d'ingestion conversationnelle OASST1

**Date :** 16 novembre 2026  
**Objet :** ajouter une source de dialogues multi-tours à l'apprentissage statistique natif Obsiss, sans introduire d'architecture neuronale.

## Résumé

Le manque de dialogues ordinaires canoniques dans les sources originales est documenté : 17 paires chat canoniques seulement, principalement orientées vers l'écriture de scénarios. Une source de conversation annotée plus large a été identifiée : OpenAssistant/oasst1. La fiche officielle indique une licence Apache-2.0, 10 364 arbres ready et 88 838 messages, avec alternance `prompter`/`assistant` et relations parent/enfant exploitables pour conserver l'historique d'un échange.

Le pipeline d'ingestion, les règles de partitionnement et les tests ont été implémentés puis renforcés. Le parcours local synthétique valide le contrôle SHA, la lecture gzip jusqu'à EOF, les sorties des trois partitions, les empreintes, l'absence de chevauchement d'arbres et la construction d'un profil à partir du seul TRAIN. Le téléchargement du fichier de données n'a cependant pas été possible depuis cet environnement : la résolution DNS de `huggingface.co` a échoué. L'intégration réelle et l'entraînement OASST1 restent donc non exécutés. Aucun exemple OASST1 n'est comptabilisé comme entraîné.

## Implémentation

Script : `tools/prepare_oasst1_obsiss_dialogue.py`  
Tests : `tests/test_oasst1_obsiss_ingestion.py`  
Spécification et usage : `experiments/datasets/OASST1_obsiss_dialogue/README_IMPORT.md`

Le script exige l'empreinte SHA-256 officielle de l'export messages. Il reconstruit les contextes par `parent_id`, groupe d'abord par `message_tree_id`, puis affecte chaque arbre entier à une partition déterministe 90/5/5. Les réponses cibles sont exclusivement les messages de rôle assistant. Le profil candidat ne lit que le fichier TRAIN et contient des statistiques agrégées, non une table de réponses mémorisées.

## Résultats des tests locaux

- 10/10 tests réussis après durcissement : 8 tests initiaux plus rejet des rôles non alternés et un test de bout en bout synthétique gzip → JSONL → partitions → profil TRAIN-only.
- Répartition par hash déterministe vérifiée.
- Reconstruction multi-tour et historique assistant/prompter vérifiés.
- Branches sœurs conservées comme cibles distinctes.
- Cycles, IDs dupliqués, arbres mélangés et rôles inconnus rejetés.
- Aucun modèle ni poids eSonde exécuté ou modifié pour ce pipeline.

## Source et licence

OpenAssistant/oasst1, fiche officielle : https://huggingface.co/datasets/OpenAssistant/oasst1  
Export ready messages : https://huggingface.co/datasets/OpenAssistant/oasst1/resolve/main/2023-04-12_oasst_ready.messages.jsonl.gz  
Licence annoncée : Apache-2.0. Empreinte SHA-256 attendue : `286a6e9a5a413b3272ae9c0b5a20d327983dea1c24342ae28cb244a6da65185c`.

## État et limite de preuve

Ce livrable est un pipeline reproductible testé sur des fixtures synthétiques, et non un corpus importé ni un profil appris. La validation sur les 88 838 messages, les mesures VALIDATION/TEST, la sélection du poids de fusion et l'intégration Dmodel restent des étapes non exécutées en raison de l'indisponibilité réseau de cet environnement. Elles ne doivent pas être présumées.

L'architecture retenue reste Obsiss/sondes P/R. Aucune donnée ne justifie une modification des poids V6 ni l'introduction de neurones/MLP.
