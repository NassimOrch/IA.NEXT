# Rapport de validation — P03 : gouvernance, checklists et sauvegardes

**Modèle :** `FulleGenBrain_f4_v0`  
**Date :** 26 octobre 2026  
**Statut :** `PASS` après création, vérification et restauration de sauvegarde.

## 1. Description

P03 met en place un protocole d'exécution traçable : chemins déclarés, phases séquentielles, registres d'erreurs séparés, journaux de commandes et snapshots avec manifeste de hashes.

## 2. Architecture

- `chemins_FulleGenBrain_f4_v0.json` décrit les racines de travail, sauvegarde, sources et livrables.
- `checklist_de_travail_FulleGenBrain_f4_v0.json` définit les phases et critères de sortie.
- `checklist_erreurs_no_model.json` et `checklist_erreurs_model.json` séparent les erreurs de l'infrastructure/harness de celles du modèle.
- `scripts/run_checked.py` relit les contrôles avant exécution et enregistre commande, code retour, stdout/stderr, reçu et snapshot.
- `scripts/savepoint.py` produit des snapshots manifestés et publiés atomiquement.

## 3. Pipeline complet

1. Lire les chemins, la checklist active et les deux registres d'erreurs.
2. Exécuter le préflight et vérifier que les chemins correspondent aux racines déclarées.
3. Lancer une commande sous le runner contrôlé.
4. Enregistrer le code retour et les sorties, et ouvrir une entrée d'erreur si l'exécution échoue.
5. Créer un snapshot privé avec manifeste SHA-256 et publier le pointeur après écriture.
6. Restaurer un snapshot dans un répertoire séparé et vérifier tous les fichiers restaurés.
7. Ne résoudre une erreur qu'avec un reçu de retest concluant et une référence explicite.

## 4. Commandes d'exécution

```sh
python scripts/run_checked.py --label p03-preflight --kind no_model -- python scripts/preflight.py --read-only-check
python scripts/run_checked.py --label p03-savepoint-restore-smoke --kind no_model -- python scripts/savepoint.py --help
```

Le reçu historique `logs/P03/savepoint_restore_smoke.stdout.json` et les manifests de snapshot constituent les preuves de création/restauration. Pour une reproduction intégrale, utiliser les commandes exactes consignées sous `logs/executions/P03/`.

## 5. Résultats

- Les deux checklists d'erreurs existent et sont JSON valides.
- Le préflight valide les chemins et la structure des registres.
- La création et la restauration des snapshots ont été testées; un contrôle postérieur vérifie 1 300 fichiers dans une sauvegarde de développement.
- Une collision de nom temporaire entre deux snapshots rapprochés a été détectée puis corrigée avec un identifiant unique et une publication atomique; l'entrée historique est conservée avec sa résolution.

## 6. Interprétation des résultats

La sauvegarde atteste l'intégrité des fichiers capturés au moment du snapshot, pas la justesse sémantique de chaque fonction. La restauration testée complète le contrôle de création; le journal d'exécution conserve aussi les échecs intermédiaires.

## 7. Conséquences théoriques, conceptuelles et opérationnelles

### Théoriques

Chaque étape importante possède une identité de contrôle et une chaîne de preuve reproductible.

### Conceptuelles

Un échec de test ou d'outil fait partie de l'historique et doit être résolu explicitement, non supprimé.

### Opérationnelles

Les snapshots et registres rendent les reprises possibles et préviennent le mélange de résultats provenant de versions de travail différentes.

## 8. Conclusions

Les racines de chemin, checklists, runner et mécanisme de sauvegarde/restauration sont disponibles et testés.

## 9. Statut du modèle

**P03 : `PASS` dans le périmètre de gouvernance et de restauration vérifié.** La qualité du code reste décidée par les phases de validation fonctionnelle ultérieures.
