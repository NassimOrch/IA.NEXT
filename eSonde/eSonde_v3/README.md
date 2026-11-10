# Schémas d'état

- `model_state.schema.json` : contrat du document modèle complet, version `1.0.0`.
- `probe_family_state.schema.json` : structure commune de l'état sparse de chaque famille.

Le modèle complet embarque une définition locale de la famille dans `$defs` et utilise exclusivement une référence JSON Pointer locale (`#/$defs/probeFamilyState`). Aucun accès réseau n'est requis pour valider le fichier. Le fichier standalone de famille reste fourni pour validation et documentation indépendante.

L'intégrité du payload est `integrity.payload_sha256`, empreinte SHA-256 du JSON canonique sans le champ `integrity`. Un sidecar `MODEL_FILE.sha256` vérifie ensuite les octets du fichier complet. Le code de runtime doit traiter le JSON et le sidecar de façon atomique.

`jsonschema` peut être utilisé comme outil de validation de développement, mais ne fait pas partie des dépendances d'exécution du moteur : celui-ci ne requiert que la bibliothèque standard Python.

Le champ `budget` est facultatif : pour RETR il est un entier non négatif ; les représentations de budget structurées restent autorisées pour d’autres familles.
