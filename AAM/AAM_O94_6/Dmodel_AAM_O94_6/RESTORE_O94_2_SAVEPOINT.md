# Restauration du point de sauvegarde O94.2

Le dossier `sav_AAM_O94_2/current/` contient les fichiers contrôlés par `sav_AAM_O94_2/savepoint_manifest.json`.

1. Extraire le paquet du modèle ou du suivi dans un dossier de travail accessible en écriture.
2. Exécuter d’abord le contrôle non destructif : `python scripts/o942_restore_savepoint.py --root .` (depuis la racine du modèle).
3. Si le contrôle retourne `PASS_BOUNDED`, une restauration volontaire peut être demandée avec `python scripts/o942_restore_savepoint.py --restore --root .`.
4. Relancer `python -m aam_o93 preflight` et lire `logs/O94_2/`.

La restauration vérifie l’intégralité du manifeste avant la première écriture, refuse les chemins absolus/traversants et n’écrase pas les sources du parent O94.1. Le mode par défaut est uniquement un contrôle, pas une restauration.
