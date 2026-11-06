# Audit des sources — EX8 v010

## Périmètre

Le workspace versionné est `EX8/versions/sondes_ex8_v010__2026-11-01/`. Les copies d’archives sous `inputs/` sont des références immuables ; les nouveaux runs, scripts et rapports v010 sont écrits dans cette version. Le pointeur `EX8/ACTIVE_VERSION.txt` indique la version active.

Les sources disponibles comprennent le workspace EX8 v001, le dossier de reprise v009, les sources consolidées EX4–EX7, les prompts de projets EX3–EX7, les sources de SMS et les bundles de formalisation. Elles ont été inventoriées et leurs checksums conservés. Dix archives ZIP imbriquées ont passé `ZipFile.testzip()` sans membre corrompu.

## Lignée RETRO

- **V007 maturation** : alpha global initialement nul ; EMA de perte locale train/OOF ; cinq observations consécutives de ralentissement relatif inférieur à 1 % ; rampe linéaire de 30 époques. C’est la logique retenue pour v010.
- **EX5 RETRO** : certains contrôleurs reposaient sur l’adaptation. Cette logique n’est pas reprise pour sélectionner/activer les modèles v010, car elle violerait le gel de l’adaptation.
- **EX6 v003** : expériences d’optimiseurs et de sémantique, pas une preuve d’une architecture RETRO exécutée.

## Sources historiques utilisées

Les 60 références de v001 (PCA concaténée et V004 OOF-0/1/2/3 sur cinq graines, plus les MLP correspondants) ont été recalculées depuis leurs prédictions sauvegardées et leurs checkpoints/hashes. Elles sont conservées sous le statut `HISTORICAL_V001_VERIFIED`, jamais mélangées aux nouveaux runs v010. Aucun résultat A/B annoncé dans l’ancienne continuation sans artefacts n’a été promu en résultat.

## Empreintes

Les archives sources sont listées dans `deliverables/SOURCE_ZIP_AUDIT.csv` et `deliverables/V010_SOURCE_ARCHIVES_CRC_AUDIT.csv`. Le manifeste SHA256 complet de la version est dans `checksums/SHA256SUMS.txt`.
