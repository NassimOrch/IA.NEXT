# AAM O94 — dossier de travail

O94 part du modèle O93_1 fourni et maintient la trace des changements. Version Python : `0.94.0`.

## Démarrage
Depuis le dossier extrait :

```bash
python -m aam_o93 status
python -m aam_o93 --help
python -m aam_o93 ui
```

Le runtime consulte les formalismes, checklists et registres d'erreurs au préflight. Il faut conserver les documents O94 et historiques distribués à la racine. L'autonomie est démarrée par l'interface ; arrêter la boucle par le contrôle d'arrêt avant de fermer si un arrêt explicite est nécessaire.

## Modèle de langue
Le moteur contient des capsules locales compactes entraînables et une passerelle optionnelle de génération vers un serveur local configuré. Il n'inclut pas les poids d'un LLM fondation généraliste. Dans Internet / API, sélectionner `openai_compatible` ou `ollama`, entrer l'URL de base et l'identifiant du modèle. Les serveurs de boucle locale sont prévus par défaut ; un serveur distant exige l'option Internet activée et un hôte approuvé. La clé facultative se transmet par `AAM_LOCAL_LLM_API_KEY` dans l'environnement du processus ; elle n'est pas stockée dans les réglages.

## État de preuve
Les statuts sont bornés aux commandes réellement exécutées. Les mécanismes synthétiques et mockés ne démontrent pas une validation sur Windows, capteurs physiques, serveur LLM réel ni l'intégralité du corpus SMS de 5 574 lignes. Consulter `registre_prouves_O94.json`, `checklist_de_travail_O94.json`, `laboratoire_O94.tex` et `formalisme_O94.tex`.


## Installation portable et démarrage O94
Le cœur du runtime et l’interface Tk utilisent la bibliothèque standard Python 3.11+; l’interface graphique requiert Tk/Tcl. Sous Windows, lancer ``run_AAM_O94.bat` ou `run_AAM_O94.ps1`; sous Linux/macOS, lancer `./run_AAM_O94.sh`. Les commandes CLI restent disponibles avec `python -m aam_o93 --help` et `python -m aam_o93 status`.

`chemins_O94.json` distingue les chemins absolus du poste de build des chemins portables. Pour retrouver le layout prévu, extraire les trois ZIP dans un même répertoire; le point de sauvegarde se trouve dans `suivi_model_AAM_O94/sav_AAM_O94/`. Les outils de build/audit O94 ne sont pas nécessaires pour lancer l’UI. Les décodeurs image/audio/vidéo sont optionnels et ne déclarent pas une compréhension sémantique quand ils n’ont produit que des mesures brutes. Voir `requirements-optional-parquet.txt` et les dépendances système notées dans ce fichier.

## Audit et limites de validation
Le `MANIFEST_SHA256.json` de la livraison est un manifeste O94 rafraîchi sur les fichiers effectivement packagés; il exclut les fichiers-manifest eux-mêmes afin d’éviter une référence circulaire. `verify_manifest.py .` vérifie l’ensemble de ses lignes. Les résultats d’intégrité ZIP/CRC, de ré-extraction et les empreintes externes des trois archives sont dans l’archive d’audit et le manifeste externe de livraison.
