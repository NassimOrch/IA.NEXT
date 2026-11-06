# eGenBrain_v0 — paquet d’exécution local

## Description et nature exacte

eGenBrain_v0 est un moteur relationnel de **recherche et restitution**. L’apprentissage compile les exemples, leurs multiplicités, occurrences lexicales, arêtes d’ordre et références de provenance dans SQLite. Il ne s’agit ni d’un Transformer ni d’un décodeur libre token par token. Lorsqu’un statut `FOUND` est retourné, la sortie est la réponse d’un exemple admissible du split `train`.

La couverture et la classification sont mesurées dans les journaux d’audit joints séparément. La conformité logicielle, l’intégrité du modèle et la qualité empirique sont des dimensions distinctes; les mesures faibles ou absences de réponse sont conservées telles quelles.

## Archive autonome — base complète incluse

Cette archive unique contient directement `model/eGenBrain_v0.sqlite3`, la base SQLite complète de **516 423 680 octets**. Aucun ZIP `part2`/`part3` ni réassemblage des fragments n’est nécessaire. SHA-256 attendu de la base : `c843c256a3ce2591b27ca1cde208e29e20143d540483fcb2b23049333c0a5d4a`.

Après extraction, depuis la racine du dossier `eGenBrain_v0`, vérifiez la base avec `python scripts/verify_integrity.py --model model/eGenBrain_v0.sqlite3`, puis lancez `./run.sh` (Linux/macOS) ou `run.bat` (Windows). Le script `scripts/reassemble_model.py` est conservé pour compatibilité : si la base complète est déjà présente et valide, il contrôle son SHA-256 et s’arrête sans la réécrire. Les entrées `parts` de `model/model_manifest.json` sont des métadonnées de provenance du découpage source et ne désignent pas des fichiers à extraire de cette archive. Aucun téléchargement réseau ni paquet externe n’est utilisé pour le runtime.

## Prérequis

- Python 3.10 ou plus récent.
- Bibliothèque standard Python uniquement pour l’API, le moteur, le chat web, le réassemblage et les tests.
- Aucun service distant, CDN ou accès réseau extérieur nécessaire.
- La base SQLite complète est incluse dans cette archive; le lancement vérifie sa taille et son SHA-256 avant de démarrer.

## Démarrer le chat

Linux/macOS, depuis la racine extraite :

```sh
./run.sh
```

Windows :

```bat
run.bat
```

Puis ouvrir `http://127.0.0.1:8000`. Le serveur écoute par défaut uniquement sur loopback. `Ctrl+C` arrête le serveur.

## Commandes de vérification et de reproduction

```sh
python scripts/reassemble_model.py
python scripts/verify_integrity.py --model model/eGenBrain_v0.sqlite3
python -W error::ResourceWarning -m unittest discover -s tests -v
python -m egenbrain.evaluate --model model/eGenBrain_v0.sqlite3 --out logs/evaluation_reproduction.json
```

Le build de référence utilise les sources JSONL et l’archive SMS de `data/dataset/`. Le lecteur Parquet optionnel est conditionné à la disponibilité de PyArrow : pour reproduire exactement le périmètre du build livré lors du réentraînement, exécuter dans un environnement sans PyArrow. Le runtime de chat reste en bibliothèque standard uniquement. Le rebuild est :

```sh
python -m egenbrain.train --data data/dataset --output model/eGenBrain_v0.sqlite3
python scripts/verify_integrity.py --model model/eGenBrain_v0.sqlite3 --skip-expected-hash
```

Le rebuild remplace la base réassemblée; copiez-la au préalable si vous souhaitez préserver l’artefact livré. La disposition déterministe de la base reconstruite peut différer selon la version de Python/SQLite; les comptes de données et les invariants sont les critères de reproduction, tandis que le SHA-256 du modèle livré identifie les octets du modèle livré.

## Données et portée

Le build validé a lu 127 286 enregistrements prompt/réponse et les a regroupés en 105 519 paires tâche/prompt/réponse canoniques; les multiplicités et références de source sont conservées. Les 4 783 paires conversationnelles valides se réduisent à 17 paires distinctes. Une ligne JSONL mal formée a été exclue sans réparation. Le fichier Parquet brut est livré à `data/dataset/0000.parquet`. Le lecteur `_read_parquet_optional` essaie d’utiliser PyArrow lorsqu’il est installé; il était indisponible lors du build de référence, donc le Parquet n’a pas été ingéré dans la base mesurée. Le runtime de chat n’en a pas besoin. Si PyArrow est installé lors d’un réentraînement, le corpus `question`/`answer` peut être ajouté à la tâche `math_qa` et la base reconstruite différera du snapshot livré. Le fichier original est préservé octet par octet.

Les relations non annotées restent `unknown`; aucune fréquence lexicale n’est promue en causalité certifiée. Le résultat est un moteur de recherche/restitution relationnelle et non une garantie de vérité factuelle ou de génération libre.

## Répertoires

- `egenbrain/` : moteur, apprentissage, évaluation et serveur HTTP.
- `web/` : interface de chat, CSS et JavaScript locaux.
- `model/eGenBrain_v0.sqlite3` : base SQLite complète, incluse directement dans le paquet. `model/model_manifest.json` documente aussi les fragments source historiques.
- `data/dataset/` : sources exactes utilisées dans le build de référence.
- `data/dataset/0000.parquet` : source Parquet préservée; non ingérée dans le build de référence (adaptateur PyArrow optionnel).
- `scripts/` : réassemblage, intégrité et scripts d’exécution.
- `tests/` : tests unitaires et API.

Les preuves théoriques par lignes de code, les journaux et les checklists sont livrés dans les archives d’audit et de suivi.
