# AAM O94_0 — notice portable

Cette édition incrémente O94 et traite explicitement les retours R1, R2 et R3. Elle conserve les formalismes, jeux de données et traces historiques utiles à l'audit.

## Démarrage local

Prérequis : Python 3.11 ou plus récent, et Tcl/Tk pour l'interface graphique. Depuis le dossier extrait, lancer le script adapté au système :

- Windows : `run_AAM_O94_0.bat` ou `run_AAM_O94_0.ps1`
- Linux/macOS : `./run_AAM_O94_0.sh`

En ligne de commande :

```sh
python -m aam_o93 status
python -m aam_o93 --help
python -m aam_o93 ui
```

Les lanceurs se placent dans le dossier contenant le modèle et définissent `PYTHONPATH` localement ; ils ne dépendent pas du chemin du poste de build. Le premier démarrage peut demander la configuration facultative de connecteurs externes.

## Contrat R1 — réponse et détails

La conversation affiche le texte de réponse uniquement. Sources, score de recherche, état du pipeline, motif de fallback, provenance et empreintes techniques sont exposés dans le panneau **Détails**. Le mode d'extraction directe du RAG est une option explicite ; ce n'est pas le parcours de génération par défaut.

## Contrat R2 — génération après récupération

Le parcours standard est : requête utilisateur → sélection RAG hiérarchique → génération par le backend sélectionné → réponse nettoyée et détails séparés. Le générateur local compact peut être choisi sans serveur distant. Un backend AAM compatible peut être sélectionné explicitement en remplacement du LLM ; la question et les preuves sont transmises séparément, et le routage ne doit pas basculer silencieusement vers un autre backend.

Le paquet ne contient pas de poids de LLM fondation généraliste pré-entraîné et n'intègre pas un interpréteur Python autonome. Les connecteurs OpenAI-compatible/Ollama et leurs serveurs doivent être configurés séparément si souhaités. Les clés API doivent être fournies par variable d'environnement, par exemple `AAM_LOCAL_LLM_API_KEY`, jamais inscrites dans les fichiers de réglage.

## Contrat R3 — mémoire progressive

Le RAG et la mémoire utilisent une indexation maître → micro-espace → enregistrements atomiques. La profondeur choisie régit le budget de résolution ; la lecture approfondie consulte les enregistrements nécessaires sans déverser systématiquement l'ensemble du corpus ou du journal dans le contexte. Les empreintes et la provenance permettent de contrôler l'intégrité des feuilles lues.

## Contrôles et portée

`MANIFEST_SHA256.json` et `PACKAGE_MANIFEST_SHA256.json` décrivent les fichiers distribués, à l'exclusion des manifestes eux-mêmes pour éviter une référence circulaire. Le manifeste externe `O94_0_livraison_manifest.json` donne les tailles et SHA-256 finaux des livrables.

Les tests locaux couverts et leurs limites figurent dans `registre_prouves_O94_0.json`, `checklist_de_travail_O94_0.json`, `laboratoire_O94_0.tex` et `formalisme_O94_0.tex`. La validation locale n'équivalait pas à un essai natif Windows/NTFS, à la validation d'un service LLM externe réel, ni à un parcours exhaustif de tous les 5 574 SMS. Les adaptateurs et les échantillons réussis sont rapportés avec leur portée exacte.

## Restaurer les sources et les preuves

Le ZIP du modèle est utilisable indépendamment du dossier de travail de construction. Le ZIP de suivi contient le point `sav_AAM_O94_0` et ses manifestes. L'archive d'audit contient les rapports de base et l'addendum O94_0. Comparer les SHA-256 avec le manifeste externe après téléchargement ou transfert.
