# Audit documentaire et des données EX7

## Références de reprise

- Archive de sources reçue : `last_sources.zip` (lot de sources imbriquées antérieur, référencé dans l'inventaire source original).
- Livrables EX6 : `sondes_ex6_livrables_complets_v005.zip` et `sondes_ex6_v003_livrables.zip`.
- Source de définition : `inputs/FORMALISME_ADAPTATION_GLOBALE.pdf` (7 pages) ; le PDF a été rendu et consulté pour éviter d'interpréter le mot « global » comme une simple agrégation statique.
- Inventaire des archives/datasets : `inputs/INVENTAIRE_SOURCES.md` ; définitions et portée : `inputs/DEFINITIONS_THEOREMES_HYPOTHESES.md`.
- Parent prompt : `inputs/prompt_ex6_parent.json` ; prompt EX7 versionné : `prompt_ex7.json`.

## Paquet de référence EX6 embarqué

`inputs/ex6_reference/` contient les modules EX6 nécessaires, le manifeste NPZ Wisconsin développement, les 10 checkpoints base Emplica/Orchestra OOF pour cinq graines, les résumés et les prédictions OOF d'origine. Ce sous-ensemble est en lecture seule du point de vue EX7 et permet de reproduire les essais sans accéder au workspace de travail externe. SHA-256 de la donnée Wisconsin : `93f7a5f6ef8a5daa090bf83f4a2169a9857893f4aca4b700f7b74566b14be1da`.

## Audit de données externe

L'inventaire des sources rapporte : Screenplay 4 000 lignes mais seulement 2 000 objets distincts (2 000 doublons excédentaires) ; `batch_dataset.jsonl` 784 lignes dont la dernière est tronquée ; `0000.parquet` a une signature PAR1 valide mais n'a pas été décodé dans l'environnement ; SMS 5 574 messages, 5 171 textes uniques, déjà utilisé dans une expérience pilote antérieure ; Wisconsin, Digits et Wine ont été exposés dans les campagnes antérieures. Aucun de ces datasets n'est donc retenu comme test externe vierge.

## Provenance et intégrité

Les sources originales demeurent dans les archives sources originales ; EX7 travaille dans un workspace indépendant. Les checkpoints EX6 correspondants et résumés sont embarqués pour traçabilité. Les résultats EX7 sont nouveaux ; les logs de campagne, checkpoints, prédictions, tables, rapports et hashes figurent dans le workspace. Les fichiers historiques ne sont pas modifiés.

## Limites d'audit

Le contenu du Parquet n'est pas analysé ; les doublons Screenplay et la troncature JSONL sont conservés/documentés, pas réparés. Les jeux historiques ne peuvent pas fournir de confirmation externe. La campagne EX7 ne constitue pas une reproduction intégrale de chaque fichier source/artefact historique, seulement des éléments directement liés à la lignée cible.
