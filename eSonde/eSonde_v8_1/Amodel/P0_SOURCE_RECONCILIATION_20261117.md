# Rapport P0 — Réconciliation des sources eSonde v8

## Description
Reprise de l'état de travail à partir de l'archive source réellement présente et des artefacts eSonde v8 conservés dans `/mnt/data`. Ce rapport distingue l'inventaire exhaustif, les inspections approfondies réalisées, les essais réellement exécutés et les travaux encore ouverts.

## Architecture et corpus source
- Archive principale : `eSonde_v7_continous_v2.zip`.
- SHA-256 observé : `026226bd2d7d842e73f24b1ad185a87ab7ae1bb0b320132259c8ed70b77f2512`.
- `unzip -t` : toutes les entrées ZIP vérifiées, aucune erreur de structure détectée.
- Arborescence extraite : Dmodel v7, Amodel v7, suivi v7, Dmodel/eGenBrain v4 et `theorie_emp`.
- `theorie_emp` : 2 018 fichiers, 88 807 602 octets selon l'inventaire SHA-256 existant; 266 `.tex`, 471 JSON, 591 Markdown, 60 sources Python, 114 tableaux CSV, 108 PDF et autres fichiers d'expérience.
- PCH : 85 fichiers; 34 fichiers TeX; versions successives PH/PCH/PCH-ESM, routage variationnel, résultats et checklists. Les PDF n'ont pas été relus, conformément à la priorité donnée aux sources LaTeX et aux fichiers texte.
- `formalismes` : 1 925 fichiers, dont 659 dans `sondes_experiences`, couvrant AAM, eGenBrain, NGeGenBrain, eLLM, modèles d'ordre et expériences de sondes. Le manifeste `source_inventory_theorie_emp.jsonl` donne taille, SHA-256 et métadonnées structurales fichier par fichier.

## Inspection approfondie réalisée
- Le noyau `DDD_Base_theorie_des_empreintes_complete_order_5.tex` a été cartographié par chapitres : observables/sondes, indiscernabilité/fibres/quotients, factorisation, seuils, trajectoires, apprentissage/généralisation, contraintes, recherche, imagination, bisimulation et statut des résultats.
- Les formalismes empiriques `formalisme_empirical.tex`, `formalisme_empirical_O78_1_2.tex` et `th_emp_observation_formalisme_0(1).tex` ont été identifiés et leurs structures logiques examinées. Les notions de mémoire ontologiques/évolutives ne sont pas confondues avec une mémoire conversationnelle du runtime.
- PCH : les versions successives PH/PCH/PCH-ESM et les textes de routage ont été examinés structurellement; le noyau proximal convexe est retenu comme candidat mathématique 16D. Les branches utilisant embeddings pré-entraînés, Sentence-Transformers ou PCA sont exclues du runtime normatif.
- eGenBrain : le fichier `parquet_flat.py` a été lu. Son lecteur `read_question_answer` prend en charge un sous-ensemble précis BYTE_ARRAY/PLAIN/dictionary/SNAPPY et un schéma question/answer; il ne peut pas décoder directement OASST1. L'adaptateur OASST1 réutilise ses primitives CompactReader, Snappy, hybrid-level et BYTE_ARRAY et ajoute le décodage BOOLEAN scalaire.
- eSonde v7 : le runtime actif comprend `activation.py`, `context.py`, `dialogue_learning.py`, `generation.py`, `observers.py`, `semantic_space.py`, `supervisor.py`, `recorder.py` et les composants v6. Les seize observations sont des fonctions explicites du texte/contexte/candidat, et les Obsiss sont des identités individuelles de la population du checkpoint.

## OASST1 : provenance et intégrité
Révision `fdf72ae0827c1cda404aff25b6603abec9e3399b`, source OpenAssistant/oasst1, licence déclarée Apache-2.0. Les deux Parquet sources sont présents et leurs hashes sont consignés dans `derived/OASST1_chat/dataset_manifest.json` :
- train : 84 437 lignes, SHA-256 `bbfadf5ed1278ba2208c837fdcad865adf65f5df55d80abadab2745db13fcb5e`;
- validation source : 4 401 lignes, SHA-256 `24002597bb13a7edd42d92f773762f25e285f72c31a70449393d0ded1dc7b416`.

Le total de 88 838 identifiants de message est unique. Les splits dérivés sont train 48 557 exemples, validation 2 495 et test réservé 2 653; aucun arbre conversationnel ne traverse les splits. Les fichiers dérivés et leurs hashes sont enregistrés dans le manifeste. La source validation reste réservée au test selon la politique du projet; la validation de sélection est dérivée par arbres depuis le train.

## Intégrité et sauvegarde
- L'archive source passe `unzip -t`.
- Le savepoint parent `pre_oasst1_full_training_20261117T123500` a été revérifié : 334/334 fichiers listés, zéro absence, zéro divergence de taille/hash. Quatre manifests imbriqués ne sont pas inclus dans son manifeste parent; ils sont des fichiers de contrôle présents dans les sous-arbres.
- Un nouveau savepoint pré-exécution a été créé après l'ajout des documents de recherche et l'intégration du routage chat v8. Son manifeste est vérifié séparément et référencé dans `chemins_eSonde_v8.json`.
- Le checkpoint original reste en lecture seule; SHA-256 de `weights.bin` attendu : `8526943d1528418fa8bbbf9128b61b5e1acd90a16eeb7cc062e18864b083dff4`.

## Résultats, interprétation et conséquences
Les pilotes d'ancrage et de transitions sont uniquement teacher-forced et de petite taille. Ils guident les expériences suivantes, mais ne démontrent ni cohérence libre ni généralisation. Le profil OASST1 initial n'était pas raccordé au chemin CLI car `everyday_dialogue` n'était pas sélectionné par le classificateur de profils; cette anomalie a été corrigée dans le runtime v8 afin que toutes les requêtes suivent le profil de chat unique.

## Limites et travaux encore ouverts
L'inventaire et les hashes couvrent chaque fichier, mais un inventaire structurel de 2 018 fichiers ne signifie pas que chaque ligne de chacun des 1 925 fichiers du sous-dossier `formalismes` a été relue manuellement. Les longues expériences et les branches de livraison imbriquées restent en revue approfondie. P0 demeure ouvert tant que les sous-dossiers de formalismes/expériences n'ont pas tous une fiche de revue et que le raccordement OASST1 n'a pas passé les tests d'intégration.

## Conclusion et statut
P0_SOURCE_RECONCILIATION : EN COURS. Les sources sont présentes et l'intégrité des archives et données clés est vérifiée. Aucune affirmation de validation complète de toutes les théories ou de qualité du modèle n'est faite.

## Addendum — intégration du profil OASST1 et correction de diagnostic
La construction agrégée sur disque a consommé les 48 557 lignes du split TRAIN dérivé (48 549 exemples prompt/réponse non vides), avec 57 884 ancres, 252 793 tokens de réponse distincts, 1 771 923 arêtes bigrammes et 3 937 224 arêtes trigrammes avant top-k. Le profil final publié fait 178 134 753 octets, SHA-256 `24780eea05de8cb8c77a772f8d03776adc33dc497fcb7d6e896690f8e99ce0e6`. Le fichier porte `neural_components: []`; le checkpoint original demeure inchangé (SHA-256 `8526943d1528418fa8bbbf9128b61b5e1acd90a16eeb7cc062e18864b083dff4`).

Correction : le diagnostic initial selon lequel `everyday_dialogue` n'était pas reconnu par le classificateur était inexact. `detect_profile()` renvoyait déjà `everyday_dialogue` et `PROFILE_IDS` l'autorisait. Le problème réel était l'absence du fichier de profil v8 finalisé dans `models/eSonde_v8/dialogue_profiles.json`; ce fichier a maintenant été produit et le CLI/GUI le charge à cet emplacement.

Les tests ciblés chat v8 passent 10/10; la suite active complète `pytest tests/` passe 51/51. Les anciens tests de routage screenplay/MathQA ont été conservés en fichiers `.v7_historical` et ne sont pas activés dans v8, dont le périmètre fonctionnel est le chat prompt/réponse uniquement. P0 reste EN COURS : la cartographie et les hashes de 2 018 fichiers ne prouvent pas une lecture sémantique ligne à ligne de toutes les expériences imbriquées; la revue approfondie des formalismes et expériences doit être achevée avant passage de phase.
