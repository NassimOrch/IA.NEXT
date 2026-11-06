# AAM O94.6 — audit expérimental, corrections et preuves

## Démarrage rapide

1. Décompresser `Dmodel_AAM_O94_6.zip` dans un dossier de travail.
2. Créer l'environnement Python recommandé indiqué dans `README.md`/`requirements*.txt`.
3. Depuis la racine du modèle, exécuter `python scripts/preflight_o946.py` et exiger `PASS_BOUNDED` avant d'exécuter une expérience.
4. Lire `RAPPORT_TESTS_O94_6_FR.md` puis `GUIDE_INTERFACE_AAM_O94_6.md` et `GUIDE_PROGRAMMATION_COMPOSITIONNELLE_O94_6.md`.
5. Pour reproduire le processus de facturation, suivre `real_task_tests/O94_6_replay/observed_process/README_REPRODUCTION_SUR_PC.md`.

## Livrables

- `Dmodel_AAM_O94_6.zip`: modèle, code, exemples et tests.
- `Amodel_AAM_O94_6.zip`: audit, reçus, journaux et registres de preuve.
- `suivi_model_AAM_O94_6.zip`: suivi, checkpoints, traces et instructions complémentaires.
- `AAM_O94_6_composition_demo.zip`: composition et projet multi-fichiers de démonstration.

Les empreintes SHA-256 des archives finales sont dans `O94_6_delivery_manifest.json` placé à côté des ZIP; ce manifeste externe évite une dépendance circulaire sur les hashes du paquet.

## Portée

O94.6 corrige les défauts reproduits dans O94.5 (mauvaise entité RAG, perte de sous-questions, gestion de génération longue et intégration des traces). Les rapports différencient RAG-direct, adaptateur de contrat et vrai modèle de langage. L'adaptateur utilisé pour les exemples de Tokyo et de génération longue n'est pas un LLM. Les poids SmolLM2 de l'utilisateur n'étaient pas présents dans l'environnement d'audit.

## Documents

- `formalisme_O94_6.tex` — architecture et contrats formels.
- `laboratoire_O94_6.tex` — protocole et essais reproductibles.
- `RAPPORT_TESTS_O94_6_FR.md` — sorties observées, commandes et interprétations.
- `GUIDE_PROGRAMMATION_COMPOSITIONNELLE_O94_6.md` — tutoriel DSL/compiler.
- `GUIDE_INTERFACE_AAM_O94_6.md` — onglets et contrôles de l'interface.
- `LETTRE_AU_LYCEEN_O94_6.md` — présentation en langage simple.

## Reproduction sur ton PC

Une démonstration de rejeu est disponible sans installation d'outils UI supplémentaires :

```bash
python scripts/o946_replay_invoice_capsule_demo.py --split train
python scripts/o946_replay_invoice_capsule_demo.py --split holdout
```

Sous Windows PowerShell :

```powershell
py -3 scripts\o946_replay_invoice_capsule_demo.py --split train
py -3 scripts\o946_replay_invoice_capsule_demo.py --split holdout
```

Le premier lance six entrées observées et devrait afficher six `PASS_BOUNDED_EXACT_MATCH`; le second donne deux `UNRESOLVED`, parce que les entrées cachées ne sont pas contenues dans la capsule. Pour répéter la capture elle-même, suivez `real_task_tests/O94_6_replay/observed_process/README_REPRODUCTION_SUR_PC.md`.

L'environnement d'audit ne peut pas observer à distance ton PC. Pour observer ton processus local, lance `python scripts/o946_observe_invoice_pipeline.py` ou adapte sa configuration à une cible que tu as le droit d'exécuter. Conserve les traces et les hashes avant de juger la généralisation. La capsule de facturation rejoue exactement six entrées observées; deux entrées tenues à l'écart restent `UNRESOLVED`.


## Validation globale O94.6

La matrice exhaustive segmentée (`receipts/O94_6/P8_fresh_extract_full_matrix.json`) a exécuté 92/92 fichiers de tests en 12 lots : 448 réussites cumulées, 0 échec et 0 timeout. Ce total est une somme de compteurs par processus et ne doit pas être additionné aux tests ciblés répétés ailleurs. Voir `RAPPORT_TESTS_O94_6_FR.md`, sections 20–21, pour les commandes, lots, reçus et hashes. La preuve ne certifie pas le modèle local SmolLM2 dont les poids n’étaient pas disponibles dans cette session, ni l’observation directe du PC physique de l’utilisateur.


La phase P8 est clôturée avec une matrice de 92 fichiers exécutés en lots isolés, 449 réussites cumulées, zéro échec et zéro timeout. Les limites non certifiées (poids SmolLM2 absent de l’environnement et observation physique du PC) sont conservées dans le rapport.
