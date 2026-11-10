# Guide complet de l'interface graphique — eSonde v3

## 1. Prérequis et lancement

Python 3.10+ et Tcl/Tk (module `tkinter`) sont requis. Le moteur CLI reste utilisable sans Tkinter. L'interface ne requiert aucun paquet Python tiers ni accès réseau.

Depuis le dossier livré :

```bash
python run_esonde_gui.py
```

Raccourcis : `run_esonde_gui.sh` sous Linux/macOS, `run_esonde_gui.bat` sous Windows. Sur Linux, installer le paquet Tcl/Tk de la distribution si `import tkinter` échoue. Vérifier avec `python -m tkinter`.

## 2. Modèle courant

Le champ **Modèle courant** est initialisé sur `models/esonde_v3_demo_checkpoint.json`, checkpoint d'exemple livré avec son sidecar. Utiliser **Parcourir…** pour sélectionner un autre checkpoint JSON. Les actions qui chargent un modèle vérifient les empreintes et la structure du checkpoint ; conserver le JSON et le fichier `.sha256` ensemble.

Le fichier de sortie par défaut de l'entraînement GUI est `models/esonde_v3_gui_model.json`. Le chemin du modèle courant est remplacé seulement après la réussite du travail d'entraînement. Le modèle courant doit être un fichier valide ; un nom de fichier absent n'est pas créé par le simple fait de lancer l'interface.

## 3. Onglet « Entraînement / mise à jour »

Champs :
- **Corpus d'entraînement** : fichier(s) ou dossier(s) de textes UTF-8 ; plusieurs chemins peuvent être séparés par `;`.
- **Corpus validation** : facultatif lors d'un entraînement, obligatoire pour le bouton de recalibration ; sert uniquement à calibrer COORD.
- **Fichier modèle de sortie** : destination du JSON et de son sidecar SHA-256.
- **Corpus à ajouter** et **Identifiant de lot** : nouveau lot disjoint à intégrer au modèle courant.

Boutons :
- **Entraîner** : crée un nouveau modèle depuis train et, si fourni, calibre COORD sur validation.
- **Démo intégrée** : réalise l'entraînement d'essai sur les petits textes inclus.
- **Mettre à jour le modèle courant** : ajoute le lot portant l'identifiant déclaré ; IDs et SHA-256 dupliqués sont refusés.
- **Recalibrer COORD** : recalcule les poids sur un corpus de validation indépendant sans réentraîner les familles.
- **Supprimer un lot (reconstruction exacte)** : reconstruit toutes les structures depuis le registre des lots conservés. Les anciens checkpoints sans ledger complet refusent explicitement l'opération.

Les checkpoints récents conservent le texte des lots et de validation ; ils contiennent donc des données du corpus. Ne pas partager un checkpoint sans vérifier confidentialité et droits.

## 4. Onglet « Génération »

Saisir le prompt, choisir le nombre maximal de tokens (1 à 2048) et la stratégie `greedy` ou `sample`, puis cliquer **Générer**. `greedy` choisit le candidat de tête ; `sample` échantillonne avec la graine déterministe de l'interface. La génération affiche le texte et sa trace JSON dans le journal commun.

BYTE peut proposer des chaînes UTF-8 non vues ; la recherche top-k est approximative (beam) et son paramètre de largeur conditionne le coût de génération. Une génération vide ou de faible qualité est une sortie à examiner, pas une exception à transformer en texte de substitution.

## 5. Onglet « Évaluation / récupération »

**Corpus de test** + **Évaluer (score)** : calcule les métriques next-token sur un corpus indépendant. Les contenus connus de train/validation sont rejetés par empreinte. Le résultat comprend le nombre de cibles, la log-loss, la perplexité, les précisions top-k et les diagnostics de contexte.

**Requête de récupération** + **Récupérer des contextes** : expose les contextes associés et leurs attributions RETR lorsque disponibles. La récupération n'invente pas une source pour les candidats sans preuve.

## 6. Onglet « Inspection / audit »

Choisir `SEQ`, `SKIP_REL`, `MORPH`, `SEM`, `DISC`, `RETR`, `BYTE` ou `COORD`, éventuellement fournir une clé JSON exacte, puis cliquer **Inspecter**. **Audit de pureté / état** contrôle les imports/constructions du runtime et l'état du modèle. **Informations modèle** affiche version, configuration et manifeste.

La zone **Relations composées (A — relation — B)** permet d'ajouter les filtres gauche, relation et droit ; un champ vide n'ajoute pas de filtre. **Candidats de coréférence / alias de surface** analyse le texte saisi et expose les candidats accompagnés de preuves. Le système ne force pas de décision finale et n'est pas un résolveur pronominal complet.

## 7. Exécution asynchrone et journal

Les opérations longues sont lancées dans un thread de travail ; les résultats et exceptions sont transférés au thread UI par une file. Les contrôles sont désactivés pendant l'exécution concurrente. Le journal en bas de fenêtre affiche les résultats JSON, avertissements et erreurs ; la barre de statut indique la fin ou le type d'erreur.

Attendre le statut « Terminé » avant de fermer la GUI lors d'un entraînement ou d'une mise à jour. Vérifier la présence du checkpoint et de son sidecar dans le dossier de sortie.

## 8. Problèmes courants

- `No module named tkinter` : installer/activer Tcl/Tk ; utiliser la CLI si l'interface graphique n'est pas disponible.
- Modèle courant absent : utiliser Parcourir… ou entraîner via l'onglet prévu ; le chemin par défaut désigne le checkpoint livré.
- SHA-256 mismatch / sidecar manquant : restaurer le couple JSON+sidecar d'une sauvegarde intègre ; ne pas régénérer un sidecar à partir d'un fichier suspect.
- Corpus UTF-8 invalide ou vide : corriger le chemin/l'encodage et contrôler que le dossier contient des documents reconnus.
- Refus pour chevauchement train/validation/test : créer des splits disjoints au niveau contenu, pas seulement au niveau nom de fichier.
- GUI en environnement sans affichage : utiliser Xvfb pour les tests ou la CLI pour travailler sans écran.

## 9. Confidentialité

Aucun corpus n'est envoyé à un service externe par la GUI. Les checkpoints récents peuvent toutefois embarquer les textes de train/validation et les références de provenance ; protégez-les de la même manière que les corpus sources.
