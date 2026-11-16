# Provenance et intégrité — eSonde v7

## Checkpoint

Le checkpoint livré est conservé sous `models/eSonde_v6/`. Le fichier `weights.bin` fait 64 000 000 octets et a pour SHA-256 :

`8526943d1528418fa8bbbf9128b61b5e1acd90a16eeb7cc062e18864b083dff4`

Le fichier `language_stats.json` a pour SHA-256 `08534e7e4c73ce34e9431277409149d64e0851b7087d73605c4ce0d409ff4e83`. Le manifeste `training_split_manifest.jsonl` a pour SHA-256 `0e8484b94b8af43cadd0f1968a460f03f6dccd47a0b4358037fe2791b2e6435f`.

Les poids n'ont pas été réentraînés pour cette révision v7. Les paramètres originaux sont interprétés par le nouvel opérateur d'observation ; il n'y a aucune prétention d'un nouveau checkpoint appris.

## Données sources

Les jeux de données originaux et l'archive téléversée ne sont pas inclus dans le paquet Dmodel. Les sources, audits, résultats, logs, hashes, rapports et références d'expériences sont conservés dans Amodel et suivi. Le manifeste de séparation indique quels contenus lourds n'ont pas été copiés.

## Savepoint

Un savepoint est un snapshot du code et du checkpoint. Son manifeste enregistre chaque chemin, taille et SHA-256. Le point de sauvegarde courant est référencé dans `sav_eSonde_v7_reference.json`. Avant génération, le préflight vérifie le manifeste et le checkpoint actif. Après génération ou incident, un snapshot supplémentaire est créé.

## Nature des preuves

Un SHA-256 vérifie que les octets correspondent à une empreinte enregistrée. Il ne prouve pas l'origine humaine, l'auteur, la vérité d'une réponse ou l'intégrité d'un résultat au-delà du moment de calcul. Aucun certificat ou signature personnelle n'est revendiqué ici.
