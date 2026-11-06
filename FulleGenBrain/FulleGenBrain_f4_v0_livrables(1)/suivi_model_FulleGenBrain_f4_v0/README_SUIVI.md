# Notices et provenance des composants amont

Le noyau original FulleGenBrain_f4_v0 est couvert par la licence non commerciale du fichier `LICENSE`. Cette licence ne remplace pas les conditions des sources historiques conservées dans `vendor/`, `spec/upstream/` et `spec/upstream/sources/`.

Le relevé complet est dans [`vendor/UPSTREAM_NOTICES.md`](vendor/UPSTREAM_NOTICES.md) et les empreintes sont dans [`vendor/vendor_manifest.json`](vendor/vendor_manifest.json). L'outil `scripts/verify_vendor_sources.py` vérifie les fichiers vendoriés contre les manifestes source.

Résultat de l'audit des paquets fournis :

- **AAM O82_0** : les métadonnées du paquet déclarent `dependencies = []`; aucun grant de licence autonome distinct n'a été trouvé dans le paquet fourni.
- **ORDER O76** : `LICENSE.txt` est une note d'attribution/dépendances, pas une licence complète. Le fichier de dépendances déclare la bibliothèque standard Python.
- **ORDER 80.2.2** : l'exécution intégrée force `--no-web`; le paquet fourni n'expose pas de grant de licence autonome distinct.
- **eGenBrain v4** : seule la voie mesh typée et les données retenues sont distribuées comme fonctionnelles. Le stockage MG historique n'est pas reconstruit, car `model/.chunks/eGenBrain_v4.sqlite3.part02` manque dans les archives reçues.
- **AAM O82_2, AAM O94.6 et ORDER 80.4.7** : éléments de comparaison ou d'audit; ils ne sont pas promus silencieusement en adaptateurs exécutables.

Ces constatations décrivent les fichiers examinés; elles ne constituent pas un avis juridique ni une confirmation de propriété. Pour redistribuer un composant dont la licence n'est pas clairement indiquée, obtenir l'autorisation nécessaire auprès du titulaire des droits.
