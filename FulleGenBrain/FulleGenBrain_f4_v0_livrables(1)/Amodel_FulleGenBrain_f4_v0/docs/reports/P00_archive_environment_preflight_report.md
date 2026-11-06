# Rapport de validation — P00 : archive et environnement

**Modèle :** `FulleGenBrain_f4_v0`  
**Date :** 26 octobre 2026  
**Statut :** `PASS` selon les preuves conservées; ce rapport ne prétend pas qu'une archive d'entrée absente puisse être reconstruite.

## 1. Description

P00 établit l'identité des entrées, l'intégrité structurelle de l'archive source, l'inventaire des archives imbriquées et la capacité disponible dans l'environnement avant toute extraction ou modification.

## 2. Architecture

Le préflight distingue l'archive reçue (`source_orderX_0.zip`), les sources formelles canoniques, les versions historiques ORDER/AAM/eGenBrain, l'arbre de travail, le répertoire de sauvegarde et les livrables. Les données d'entrée sont analysées séparément de l'arbre de travail.

## 3. Pipeline complet

1. Vérifier que l'archive source existe et relever sa taille et son SHA-256.
2. Exécuter le test CRC du conteneur ZIP et inventorier ses membres.
3. Repérer les archives imbriquées et enregistrer leur intégrité quand elles sont présentes.
4. Relever l'espace disque disponible et les chemins racines.
5. Enregistrer les fichiers annoncés mais absents, sans les fabriquer.
6. Conserver les preuves dans `spec/evidence/source_archive_inventory.json` et les artefacts de suivi.

## 4. Commandes d'exécution

Depuis la racine du projet :

```sh
unzip -tq /mnt/data/source_orderX_0.zip
sha256sum /mnt/data/source_orderX_0.zip
python scripts/run_checked.py --label p00-preflight-final --kind no_model -- python scripts/preflight.py --read-only-check
```

Le journal d'exécution du projet est la référence des commandes réellement lancées; les commandes ci-dessus décrivent une reproduction sur l'environnement source fourni.

## 5. Résultats

- Archive source déclarée : `source_orderX_0.zip`, 493 682 442 octets.
- SHA-256 relevé : `e423f5f207eba4b38ed5606da81e00eb74504410f77c251a82dcef23a1ee3303`.
- Test ZIP/CRC : réussi.
- Inventaire : 17 entrées de premier niveau selon le reçu de préflight.
- Fragment `eGenBrain_v4.sqlite3.part01` présent et conforme à l'empreinte de source; `part02` absent de l'archive fournie. Le rapport de reconstitution reste donc `PARTIAL` au lieu d'inventer les octets manquants.
- Espace disque enregistré dans les journaux de préflight et vérifié de nouveau durant P12.

## 6. Interprétation des résultats

L'intégrité CRC garantit seulement que les membres ZIP présents sont lisibles; elle ne signifie pas que tous les fragments externes attendus ont été fournis. Le statut `PARTIAL` du jeu SQLite historique est donc distinct du statut d'intégrité du conteneur principal.

## 7. Conséquences théoriques, conceptuelles et opérationnelles

### Théoriques

Le périmètre du raisonnement est limité aux artefacts réellement disponibles et identifiés par empreinte.

### Conceptuelles

Une donnée manquante est signalée comme telle, non remplacée par un contenu synthétique.

### Opérationnelles

Les chemins sources et de sauvegarde sont centralisés dans `chemins_FulleGenBrain_f4_v0.json`; le dépôt peut être audité sans confondre archive reçue et espace de travail.

## 8. Conclusions

Les critères P00 sont satisfaits pour l'archive reçue, l'inventaire et le préflight. L'absence du fragment historique `part02` demeure une réserve de données explicitement suivie.

## 9. Statut du modèle

**P00 : `PASS` pour l'identification et l'intégrité des entrées disponibles.** Cela ne constitue pas une preuve de complétude des données historiques absentes ni un pronostic sur les performances du modèle.
