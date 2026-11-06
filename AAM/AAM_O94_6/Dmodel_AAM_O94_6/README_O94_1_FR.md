# AAM O94.1 — guide de prise en main

## Démarrer localement

Prérequis : Python 3.11 ou supérieur. L'interface de bureau requiert Tk/Tcl fourni avec une installation Python appropriée.

- Windows : double-cliquer `run_AAM_O94_1.bat`. Les anciens noms `.bat` présents dans l’archive redirigent vers ce lanceur. En cas d’échec, la console reste ouverte et affiche le diagnostic. Le journal persistant est `logs/O94_1/launcher_windows.log`. `run_AAM_O94_1.ps1` reste disponible dans PowerShell.
- Linux/macOS : `./run_AAM_O94_1.sh`.
- CLI : `python -m aam_o93 --help`, puis `python -m aam_o93 status`, `python -m aam_o93 base-blocks` ou `python -m aam_o93 ui`.

La version n'embarque pas par défaut les poids d'un LLM fondation ou toutes les dépendances optionnelles multimodales. L'installation des dépendances dépend du backend voulu. `requirements_O94_optional.txt` répertorie quelques paquets optionnels; `requirements-optional-parquet.txt` est séparé. OCR via Tesseract et les flux audio/vidéo via FFmpeg/FFprobe nécessitent les exécutables correspondants.

## Modèles externes

Les exemples de manifestes se trouvent dans `examples/model_integration/` : backend local Ollama, API compatible OpenAI et Transformers local. Enregistrer un manifeste avec `python -m aam_o93 model-register <fichier.json>`, consulter `models-list`, puis générer via `model-generate <id> <prompt>`. La politique `model-train` respecte le contrat du backend déclaré; elle ne garantit pas qu'un fournisseur acceptera l'entraînement ni qu'un poids aura été modifié. Les tests de la livraison utilisent des fixtures simulées et n'affirment pas qu'un endpoint réel est accessible.

## Capture boîte noire

O94.1 ajoute une capture active autorisée à base de commande avec arguments contrôlés et entrées JSON, puis une capsule de replay autonome sans rappel automatique de la cible source. Une entrée qui n'est pas dans la capsule renvoie `UNRESOLVED`, et non une valeur inventée. Ce mécanisme restitue exactement les cas connus; il ne reconstruit pas par lui-même l'algorithme général, une GUI arbitraire, un appareil physique, une base distante ou un flux vidéo. Exécuter une cible signifie bien exécuter un programme réel : utiliser uniquement une cible autorisée et isoler les programmes non fiables en VM/conteneur.

## RAG, mémoire, résolution et autonomie

Le runtime conserve les mécanismes RAG/mémoire préexistants avec les ajouts O94.1, les briques de base, les profils d'intégration et la résolution sous budget. Les sources d'entreprise peuvent être traitées localement selon leur politique de stockage; l'utilisation d'un modèle HTTP ou d'Internet sort des garanties strictement locales. Ne transmettez pas de documents confidentiels à un endpoint distant sans autorisation et configuration appropriées.

## État des validations

`laboratoire_O94_1.tex`, `formalisme_O94_1.tex`, `registre_prouves_O94_1.json`, les deux checklists d'erreurs et `logs/O94_1/` séparent les preuves et les gaps. La régression fractionnée a reçu des résultats réussis pour 57/57 modules couverts (331 tests et 21 sous-tests rapportés passés). Les tests Windows natifs, fournisseurs LLM/poids réels, capteurs physiques, OCR/GUI génériques et migrations SQL opérationnelles ne sont pas déclarés exécutés. Le clonage de logiciels complets, la génération en série de PDF à partir d'un gabarit arbitraire et le déploiement réseau autonome restent des objectifs à valider par cas d'usage dédiés; cette non-validation n'est pas une conclusion d'impossibilité.

## Intégrité et sauvegarde

`MANIFEST_SHA256.json` couvre les fichiers de l'archive (à l'exclusion des deux fichiers de manifestes pour éviter un hash circulaire). `chemins_O94.json` indique les chemins relatifs, les livrables et le point de sauvegarde. Le dossier `sav_AAM_O94_1` est distribué dans l'archive de suivi et comprend son propre manifeste ainsi que les copies des fichiers modifiés et les reçus de phase.
