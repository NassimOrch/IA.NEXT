# Restaurer le point de sauvegarde AAM O94_3

## Contenu

` sav_AAM_O94_3/savepoint_manifest.json` décrit les copies de sauvegarde dans `sav_AAM_O94_3/current/`, relatives à la racine du modèle. Le point sauvegarde les fichiers listés avec SHA-256 et ne remplace pas les sources historiques O94_1/O94_2.

## Vérifier avant de restaurer

1. Extraire complètement `Dmodel_AAM_O94_3.zip` dans un nouveau dossier.
2. Vérifier `SHA256SUMS_O94_3.txt` à l’aide du manifeste externe de livraison.
3. Lancer `python -m aam_o93 preflight` ou le lanceur de la plateforme; le préflight contrôle les phases et les hashes du savepoint.
4. Pour un fichier à restaurer, comparer le hash actuel à `savepoint_manifest.json`, puis comparer à la copie correspondante sous `sav_AAM_O94_3/current/`.
5. Copier uniquement les fichiers que l’on veut restaurer après cette comparaison. Ne jamais remplacer en bloc les répertoires historiques O94_1/O94_2.

## Politique

Les registres d’incidents sont append-only : les erreurs corrigées restent visibles avec leur retest. Un état `PASS_BOUNDED` est la preuve d’un contrôle effectué dans son périmètre, pas une garantie universelle sur une autre machine, un modèle externe ou un capteur non disponible.
