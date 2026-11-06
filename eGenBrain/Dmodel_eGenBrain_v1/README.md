# eGenBrain_v1 — moteur relationnel et interface locale

## 1. Description et portée

eGenBrain_v1 implémente un moteur de **recherche/restitution relationnelle traçable** piloté par les formalismes joints `eGenBrain_1.tex` et `DDD_Base_theorie_des_empreintes_complete_order_5.tex`. Il n'est pas un Transformer et ne prétend pas produire une réponse à chaque requête : un résultat peut être `FOUND`, `NO_MATCH` ou `UNKNOWN`. Une réponse `FOUND` provient d'un exemple du split `train`, accompagné de références vers les observations sources; les réponses tenues à l'écart servent uniquement au banc d'évaluation.

Le modèle persiste un brain par observation source, fusionne les identités lexicales et les relations d'ordre dans un maillage global, conserve la provenance et construit un maillage contextuel à la requête. Les relations non annotées restent `unknown`; aucune causalité/anti-causalité n'est inférée depuis une fréquence lexicale seule. Le fichier d'annotations explicites se trouve dans `data/annotations/relations.jsonl`.

## 2. Réassembler le modèle distribué

La base de référence fait environ 1,65 Go. Dans les livrables, elle est distribuée en blocs placés sous `model/parts/` dans deux archives Dmodel. Extrayez **les deux ZIP dans le même répertoire**, en conservant les chemins, puis lancez `python3 scripts/reassemble_model.py` (Windows : `py -3 scripts\reassemble_model.py`). Le script vérifie la taille et le SHA-256 de chaque bloc, reconstitue un temporaire, puis vérifie la taille et le SHA-256 de la base complète avant publication atomique. `run.sh`/`run.bat` tentent ce réassemblage automatiquement si la base de référence est absente.

Ne supprimez pas les fragments avant que le réassemblage et le contrôle d'intégrité aient réussi. Un fichier `model/eGenBrain_v1_distribution_manifest.json` liste les fragments, leurs tailles et leurs hashes.

## 3. Démarrer

Prérequis : Python 3.10+; aucun paquet Python externe n'est requis pour le runtime ni le lecteur Parquet intégré.

**Linux/macOS** :

```sh
./run.sh
```

**Windows** :

```bat
run.bat
```

Puis ouvrez `http://127.0.0.1:8765`. Le serveur écoute par défaut sur loopback. `Ctrl+C` arrête le serveur. L'interface utilise ses propres fichiers HTML/CSS/JS; aucun CDN ou service externe n'est requis. Variables optionnelles : `EGENBRAIN_HOST`, `EGENBRAIN_PORT`, `EGENBRAIN_MODEL`.

## 4. Studio web et commandes

L'interface propose un espace **Chat** et un **Studio**. Le Studio inspecte et charge des datasets, permet de sélectionner les champs prompt/réponse et le type de tâche, de lancer un entraînement dans une nouvelle base isolée, de suivre le job, d'évaluer validation/test, d'activer explicitement un modèle terminé, de consulter statistiques/provenance et d'utiliser une console de commandes applicatives. La console expose les opérations du modèle; elle n'exécute volontairement pas un shell système arbitraire.

Formats pris en charge pour l'inspection/import : JSON, JSONL/NDJSON, CSV, TSV, Parquet (`question`/`answer` via lecteur standard-library dédié), et ZIP contenant CSV/TSV/JSON/JSONL ou `SMSSpamCollection`. L'import n'efface pas ni ne répare silencieusement le fichier source. Les conflits de schéma et lignes invalides doivent rester visibles dans les journaux.

Commandes applicatives disponibles depuis la racine :

```sh
python -m egenbrain --help
python -m egenbrain chat --message "texte à interroger" --task chat
python -m egenbrain inspect-dataset --path data/dataset/0000.parquet
python -m egenbrain train --data data/dataset --output model/eGenBrain_v1_trained.sqlite3
python -m egenbrain evaluate --model model/eGenBrain_v1.sqlite3 --split test --max-per-class 5 --max-math-examples 5 --out logs/eval.json
python -m egenbrain serve --model model/eGenBrain_v1.sqlite3 --host 127.0.0.1 --port 8765
python -m egenbrain verify --model model/eGenBrain_v1.sqlite3
```

L'entraînement CLI produit une nouvelle base et ne remplace/active jamais automatiquement le modèle courant. `./train.sh` ou `train.bat` construit `model/eGenBrain_v1_trained.sqlite3`, vérifie l'intégrité SQLite et conserve les journaux dans `logs/`.

## 5. Vérification, tests et reproduction

```sh
python scripts/verify_integrity.py --model model/eGenBrain_v1.sqlite3
python -W error::ResourceWarning -m unittest discover -s tests -v
python -m egenbrain.evaluate --model model/eGenBrain_v1.sqlite3 --out logs/p5_reproduction.json --split test --max-per-class 5 --ablation-per-class 1 --max-math-examples 5
```

`model/eGenBrain_v1_manifest.json` documente les octets et le SHA-256 du modèle de référence. Si vous vérifiez un modèle fraîchement entraîné, utilisez `--skip-expected-hash` (le contrôle SQLite, les clés étrangères et les splits reste actif) ou passez un manifeste adapté. Toute évaluation doit enregistrer le split, la graine, les limites d'échantillonnage, les métriques, la latence, les résultats `NO_MATCH/UNKNOWN` et le hash avant/après.

## 6. Datasets et état d'entraînement de référence

Le build livré a lu 134 759 observations brutes issues de quatre sources : JSONL batch, JSONL screenplay, ZIP SMS (fichier original et variante augmentée) et `0000.parquet`. Les observations sont conservées dans 134 759 brains durables, agrégées en 112 992 exemples canoniques, avec 125 453 identités de tokens, 1 811 636 lignes d'index occurrence/token et 756 568 arêtes globales.

La seule anomalie de parsing source connue est `batch_dataset.jsonl`, ligne 784, JSON mal formé, explicitement exclu sans réparation. Les multiplicités des doublons sont conservées. Les splits sont séparés au niveau des groupes de prompt; le maillage et l'index global d'apprentissage ne comprennent que `train`.

## 7. Résultats d'évaluation et interprétation

L'intégrité, la provenance structurelle, le chargement/entraînement via web, l'activation explicite et la persistance de configuration ont été testés avec résultats positifs consignés sous `logs/`. Ces contrôles ne garantissent pas la qualité sémantique. Les expérimentations de référence ont révélé des `NO_MATCH` sur les exemples de chat et de mathématiques échantillonnés, des SMS corrects pour une partie des exemples et des faux positifs possibles sur les uploads personnalisés. Ces résultats sont conservés dans les journaux et décrits dans `rapport_eGenBrain_v1.tex`; aucune conclusion universelle n'est inférée de petits échantillons.

La couverture anti-causale reste partielle : le corpus ne fournit pas d'annotations vérifiées en quantité et les relations non annotées demeurent `unknown`. Le test synthétique prouve que le chemin de stockage d'une annotation explicite existe, pas que le corpus comporte des causalités validées.

## 8. Structure

- `egenbrain/` : tokenisation, brains, fusion, recherche, évaluation, chargement de données, API et CLI.
- `model/eGenBrain_v1.sqlite3` : modèle de référence construit et audité.
- `data/dataset/` : sources brutes incluses.
- `data/source/` : sources théoriques utilisées comme références.
- `web/` : interface locale du chat/Studio.
- `tests/` : tests unitaires et d'intégration.
- `scripts/` : audit structurel, vérification et reassemblage du modèle distribué en morceaux.
- `logs/`, checklists, checkpoint et preuves JSON : traces consultables de chaque phase.

Voir `formalisme_eGenBrain_v1.tex` (copie de compatibilité : `formalime_eGenBrain_v1.tex`) pour le formalisme exact du code livré et `rapport_eGenBrain_v1.tex` pour le rapport complet par phase. La concordance théorie → code → tests/résultats est énumérée dans `preuves_eGenBrain_v1.json` et `prouves_eGenBrain.json`.
