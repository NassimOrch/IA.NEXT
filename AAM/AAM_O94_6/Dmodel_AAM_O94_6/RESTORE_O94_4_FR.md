# Restauration et vérification O94.4

1. Extraire `Dmodel_AAM_O94_4.zip` dans un dossier vide.
2. Depuis la racine extraite, exécuter `python -m aam_o93 preflight`.
3. Vérifier que `sav_AAM_O94_4/savepoint_manifest.json` et `sav_AAM_O94_4/current/` existent. Le manifeste contient des chemins relatifs et les SHA-256 du correctif incrémental.
4. Les versions parentes O94.1/O94.2/O94.3 sont conservées. Pour restaurer le seul overlay O94.4, copier les fichiers listés dans `sav_AAM_O94_4/savepoint_manifest.json` depuis `sav_AAM_O94_4/current/` à la racine de travail, puis exécuter le préflight.
5. `Amodel_AAM_O94_4.zip` conserve les rapports d'audit, checklists, commandes et reçus; `suivi_model_AAM_O94_4.zip` conserve le point de sauvegarde et les journaux/tests de validation.

Un manifeste valide prouve l'intégrité des fichiers listés, pas la réussite universelle du modèle. Les capteurs matériels, fournisseurs externes et performances de généralisation doivent être re-testés dans l'environnement cible.
