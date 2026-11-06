# Porte P1 — Préenregistrement EX11

Date : 2026-11-03 (Africa/Algiers)

## État

**PASS avec reconstruction versionnée v2.2.0.** Le prompt antérieur annoncé dans les échanges n'a pas été retrouvé dans les espaces accessibles ; la version actuelle est explicitement une reconstruction, et non une récupération.

## Contrôles documentaires

- JSON `prompt_ex11.json` lisible et valide.
- Corps `prompt` et copie `PRE_REGISTRATION_EX11.md` synchronisés octet pour octet après retrait du conteneur JSON.
- SHA-256 des quatre entrées sources comparés aux fichiers présents ; les archives ZIP passent `unzip -t`.
- Les sources `Replica_U_0.tex` et `th_sondes_core_test_1.tex` restent spécifications expérimentales, non preuves de performance.
- Règles rouges explicites : aucune réussite/échec présumé, aucun sabotage direct/indirect, aucune suppression sélective, aucun tuning sur test, OOF strict, prétraitement train-only, comparateurs GE4X réellement >=4.0.
- Trois branches méthodologiquement séparées : REPLICA-U, CNG, CNC ; branche D séparée pour D1_SEQ/D2_VEC/D3_SHARED.
- Budgets, seeds, métriques, splits et livrables obligatoires explicités.

## Audit des données

- `datasets_arff.zip` CRC PASS, SHA-256 vérifié.
- 13/13 ARFF parsés ; zéro valeur manquante, zéro valeur numérique non finie.
- Doublons X, groupes à labels contradictoires et recouvrements inter-jeux reportés dans `data/metadata/dataset_audit_v002.json`.
- GINA : frontière 3153 Train / 315 Valid et checksums de features vérifiés ; split d'origine préservé.
- 65 splits sur cinq seeds ; les lignes, groupes, classes, CSV, hashes et modes des tests sont validés indépendamment dans `data/metadata/splits_independent_verification.json`.

## SHA-256

Consulter `checksums/phase1_sha256.txt` et `data/metadata/splits_manifest.json` pour les empreintes canoniques.

## Décision de passage

P0 et P1 sont considérées terminées. P2 (implémentation logicielle et tests) peut commencer. Aucun résultat scientifique de modèle n'est revendiqué à cette porte.

## Addendum protocole v2.3.0 — 2026-11-03

Le préenregistrement courant est `prompt_ex11.json` version `2.3.0-reconstructed`. Le corps JSON et `PRE_REGISTRATION_EX11.md` sont identiques octet pour octet ; consulter `checksums/prompt_ex11_v2.3.0.sha256`. La version v2.3 ajoute une contrainte de comparabilité CNC : C3 et C4 partagent le même ordre de mini-batches pour un couple graphe/seed, leurs initialisations restant indépendantes.

La suite logicielle courante est **24/24 PASS**. Cette validation ferme les tests unitaires/structurels, pas les campagnes scientifiques. Les scripts confirmatoires ont été revus et compilés ; seuls les runs présents dans les registres doivent être comptés comme exécutés.
