# Guide de l'interface graphique — eSonde v7

## 1. Objet

La GUI est une fenêtre de dialogue simple. Elle propose une transcription, une zone de saisie, le bouton Envoyer et une case facultative de non-réponse. Elle n'ajoute aucune fonction hors du chat.

La population débute à dix Obsiss. Le runtime peut augmenter l'effectif si la dynamique d'interaction ou la stabilité de la décision n'atteint pas les critères déclarés. Le nombre disponible affiché dans la barre d'état est un plafond, pas un objectif d'utilisation.

## 2. Lancement

Prérequis : Python 3.10+ et Tkinter. NumPy est facultatif.

```bash
python RUN_GUI.py
```

Linux/macOS : `./RUN_GUI.sh`. Windows : `RUN_GUI.bat`.

## 3. Utilisation

1. Au lancement, la GUI effectue le préflight et vérifie le checkpoint.
2. Saisir le message dans le champ inférieur.
3. Appuyer sur Envoyer ou `Ctrl+Entrée`.
4. La réponse produite est ajoutée à la transcription.
5. Les tours user/assistant sont conservés dans l'historique temporaire de cette fenêtre et transmis au tour suivant.

La case « Autoriser la non-réponse » est décochée par défaut. Tant qu'elle demeure décochée, le moteur ne peut pas remplacer sa continuation par une chaîne vide à cause de son incertitude interne. Une erreur technique reste signalée comme erreur.

## 4. Convergence et population Obsiss

Le runtime commence à dix Obsiss et vérifie les critères internes de stabilité. Lorsque les critères ne sont pas atteints, il augmente la population de manière géométrique jusqu'au nombre disponible. Les détails figurent dans le JSON de résultat et les traces. La GUI affiche le nombre maximum disponible, non le nombre effectivement utilisé par chaque tour.

L'accord interne ne garantit pas l'exactitude factuelle. Les réponses doivent être évaluées séparément sur des dialogues de test.

## 5. Contrôles, erreurs et sauvegardes

Le préflight vérifie les checklists, les chemins, le snapshot, le manifeste et le hash du checkpoint avant chaque génération. Une anomalie critique bloque le tour. Les erreurs sont inscrites dans `checklist_erreurs_model.json`, puis un snapshot post-incident est tenté. Les résultats réussis alimentent `preuves_eSonde_v7.json` et sont suivis d'un snapshot post-exécution.

La génération utilise un thread de calcul pour garder la fenêtre réactive. Les mises à jour de l'interface sont exécutées sur le thread principal de Tk.

## 6. Fichiers et confidentialité

Les traces sont écrites dans `runs_v7/`. Elles peuvent inclure des marqueurs de prompt et de réponse ou des observations de candidat. Les fichiers d'historique, les réponses et les traces peuvent être sensibles ; ne pas partager ces dossiers sans contrôle préalable.

## 7. Dépannage

- **La fenêtre ne s'ouvre pas** : vérifier `python -c "import tkinter"`.
- **État Bloqué** : lire le message, exécuter `python RUN_CLI.py verify`, puis contrôler les chemins et les manifestes.
- **La réponse n'apparaît pas** : consulter `runs_v7/` et `checklist_erreurs_model.json`.
- **Le calcul est long** : conserver le processus et les traces ; toute interruption externe est inscrite comme incident et le résultat est incomplet.
- **Mémoire limitée** : utiliser le CLI avec `--n-obsiss 10` pour un essai plafonné et reproductible, sans modifier le checkpoint.
