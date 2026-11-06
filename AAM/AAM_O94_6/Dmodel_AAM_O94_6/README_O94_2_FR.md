# AAM O94.2 — guide rapide

## Démarrage

- Windows : extraire intégralement l’archive, puis ouvrir `run_AAM_O94_2.bat` (ou PowerShell `run_AAM_O94_2.ps1`).
- Linux/macOS : `./run_AAM_O94_2.sh`.
- Diagnostic avant UI : `python -m aam_o93 preflight`.
- Statut runtime : `python -m aam_o93 status`.

Le lanceur vérifie Python 3.11+, Tkinter, les formalismes, les checklists, les registres d’erreurs et les hashes du point `sav_AAM_O94_2`. En cas de blocage sous Windows, il conserve le diagnostic dans `logs/O94_2/launcher_windows.log` et garde la console ouverte. Un succès de préflight prouve la cohérence des fichiers, pas la disponibilité de chaque modèle externe ou périphérique.

## Observer en boîte noire

L’onglet **Observer** expose deux contrats différents :

1. **Capture active d’un jeu de cas** : JSON, JSONL/NDJSON, CSV ou TSV. `case`/`cases` et plusieurs enveloppes courantes sont acceptées. Les champs entrée, sortie attendue, partition et collection peuvent être automatiques ou configurés explicitement. Les limites de cas, temps et taille de sortie sont visibles.
2. **Observation live JSON Lines** : AAM démarre un processus autorisé persistant sans shell. Il lit une valeur JSON par ligne sur `stdin` et émet exactement une réponse par ligne sur `stdout`. Une trace est ajoutée et synchronisée au fil des échanges. Les sondes automatiques génèrent des variantes de l’entrée initiale et les envoient réellement à la cible; les réponses viennent de la cible, elles ne sont pas inventées par le moteur.

Exemple de capture en lot :

```bash
python -m aam_o93 blackbox-capture dataset.json --command-json '["python","cible.py"]' \
  --trace-out captures/trace.jsonl --authorize-target-execution \
  --max-cases 2000 --max-total-seconds 600 --records-key case \
  --input-key prompt --target-key answer --split-key fold
```

Exemple de capture live :

```bash
python -m aam_o93 blackbox-live --command-json '["python","-u","cible_jsonl.py"]' \
  --trace-out captures/live.jsonl --authorize-target-execution \
  --duration-seconds 600 --max-events 2000 --response-timeout 10
```

**Contrat important :** le mode interactif observe réellement les appels effectués pendant que le processus reste actif, mais la cible doit implémenter le protocole JSON Lines. Un logiciel GUI opaque, une base de données distante, une caméra en continu ou un processus sans canal d’entrée/sortie instrumentable nécessitent un adaptateur dédié (API, hooks autorisés, capture d’écran/capteur, connecteur DB, etc.). La trace seule ne prouve pas une reconstruction générale du programme; toute reproduction doit être évaluée sur des cas tenus à l’écart.

## Modèles locaux et distants

L’onglet **Modèles locaux / PyTorch** expose :

- les checkpoints locaux Transformers/poids de type Hugging Face lorsqu’ils sont compatibles avec la pile installée ;
- les serveurs locaux Ollama et les endpoints compatibles OpenAI ;
- le contrat `pytorch_adapter` pour relier un fichier de poids `.pt/.pth` à son architecture et à ses fonctions de génération/entraînement.

Un fichier de poids PyTorch ne décrit pas universellement son architecture : un adaptateur explicite peut être nécessaire. Le chargement d’un script Python adaptateur demande une confirmation explicite et son SHA-256 est inscrit dans le profil. La politique d’entraînement sépare les lignes train du holdout. La préparation de paires ou l’export d’un dataset n’est pas présenté comme une mise à jour effective des poids.

## Programmation par composition

L’onglet **Programmation par composition** édite une DSL JSON versionnée qui compose des compétences, méthodes et règles du catalogue. Le compilateur refuse les identifiants qui ne sont pas enregistrés et n’exécute pas de code arbitraire injecté dans une composition. Les compositions doivent être testées sur leurs domaines cibles et ne sont promues en compétences réutilisables qu’après une validation indépendante.

## Validation de l’incrément O94.2

La matrice segmentée de cette livraison couvre les 60 fichiers `test_*.py` présents exactement une fois, au moyen de 30 reçus `PASS_BOUNDED` (349 tests et 21 sous-tests rapportés comme passés, aucun échec ni test sauté). La réconciliation se trouve dans `logs/O94_2/T45_full_regression_matrix_reconciliation.json`. La compilation Python figure dans `T31_compileall.json`; les compilations LaTeX finales des deux sources sont consignées dans `T40_formalism_compile_final.json` et `T41_laboratory_compile_final.json`. Les tests détaillés d’intégration modèles, boîte noire et UI sont référencés dans le registre de preuves.

Ce statut signifie que les vérifications du code et du paquet exécutées ici ont passé leurs critères bornés. Il ne certifie pas encore une exécution native Windows, chaque modèle tiers, un entraînement réel sur les poids d’un utilisateur, ni la reproduction universelle d’un programme opaque.

## Contrôles et sauvegarde

- `checklist_de_travail_O94_2.json` décrit les phases et leurs critères de sortie.
- `checklist_erreurs_model_O94_2.json` et `checklist_erreurs_no_model_O94_2.json` gardent les incidents et leurs retests.
- `chemins_O94.json` sépare les chemins O94.1 historiques des chemins O94.2 actuels.
- `sav_AAM_O94_2/` contient une copie restaurable des fichiers versionnés et un manifeste SHA-256.
- `logs/O94_2/` contient les reçus et les sorties des exécutions.

Les objectifs de reconstruction logicielle arbitraire, observation multimodale continue générique, compatibilité de toutes architectures tierces et entraînement réel de poids externes restent évalués adapter par adapter. Ils ne sont ni remplacés par une simulation, ni déclarés accomplis parce que l’interface existe.


Le test E2E `T63_blackbox_live_cli_e2e.json` couvre également la fermeture CLI de `blackbox-live` : démarrage de cible persistante, deux échanges observés, `:quit`, code retour zéro et rapport durable. Un ZIP antérieur avait omis le dernier correctif de fermeture : T88 conserve cet échec. Le candidat reconstruit depuis l’arbre courant passe une extraction fraîche (T93), dont le CLI live capture deux événements, produit un rapport STOPPED durable et retourne le code 0. Le manifeste exact de la livraison finale est dans le sidecar externe `O94_2_final_delivery_verification.json`.
