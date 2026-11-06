# FulleGenBrain_f4_v0

**Moteur compositionnel local, auditable et reprenable, issu du formalisme FulleGenBrain 4.**

FulleGenBrain_f4_v0 implémente un AST JSON fermé, un validateur statique, un interpréteur explicite de 29 opérateurs, une mémoire SQLite versionnée, un journal d'audit hashé, une recherche paresseuse avec reprise CEGIS, un contrôleur ASCRC et des adaptateurs spécialisés à activation explicite.

Le formalisme d'architecture est l'autorité principale. La théorie de programmation compositionnelle définit les contrats sémantiques. Le prototype d'interface sert de référence UX mais ne remplace pas ces deux sources. Les adaptations issues de ORDER, AAM et eGenBrain restent identifiées par origine, version, licence observée et état d'exécutabilité.

## État et portée

- Le noyau intégré et les fonctions décrites comme implémentées sont couverts par la suite de tests et les preuves fournies.
- Le modèle ne prétend pas démontrer automatiquement la correction universelle d'un programme. Une recherche épuisée, un budget atteint, un résultat `PARTIAL` ou l'absence de contre-exemple dans un périmètre limité ne sont pas une preuve universelle.
- Les appels LLM/RAG/réseau ne sont pas configurés implicitement. L'interface locale lie uniquement les opérations explicitement exposées.
- La base SQLite historique eGenBrain v4 reste **PARTIAL** : le fragment `part01` est validé, mais le fragment `part02` déclaré dans le manifeste est absent de l'archive fournie. Aucun octet n'est inventé. La voie mesh typée indépendante est intégrée et testée; la reconstitution du stockage historique MG n'est pas revendiquée.
- Les archives de livraison excluent les arbres historiques complets, les jeux d’entraînement, les tests amont, les rendus, les anciennes générations et les bases de données source. Elles ne gardent que le code/configuration/assets runtime indispensables aux adaptateurs actuellement branchés, avec attribution et notices séparées. Les droits de ces composants amont ne sont pas réputés couverts par la licence non commerciale du code FulleGenBrain; une revue des droits reste nécessaire avant toute redistribution publique.

## Pré-requis

- Python **3.11 ou ultérieur** (validation effectuée avec CPython 3.13.5).
- Bibliothèque standard Python uniquement pour le noyau natif; aucun paquet tiers n'est requis à l'exécution du noyau. Les tests utilisent `pytest` (dépendance de développement). Les exécutables amont gardent leurs propres prérequis indiqués dans leurs dossiers.
- Linux, macOS ou Windows avec Python disponible. Les permissions mode-bit `0700/0600` sont renforcées sur POSIX; sous Windows, les ACL natives s'appliquent.

## Démarrage rapide

Depuis la racine extraite du projet :

```bash
./run_fullegenbrain.sh --data-dir ./data-local doctor
./run_fullegenbrain.sh --data-dir ./data-local test
./run_fullegenbrain.sh --data-dir ./data-local run examples/addition_program.json --input-file examples/addition_input.json
./run_fullegenbrain.sh --data-dir ./data-local serve --host 127.0.0.1 --port 8765
```

Sous Windows, utiliser `run_fullegenbrain.bat` avec les mêmes arguments. Une alternative sans lanceur : `PYTHONPATH=src python3 -m fullegenbrain --data-dir ./data-local doctor`.

L'interface s'ouvre ensuite à `http://127.0.0.1:8765/`. Le serveur refuse les adresses non loopback, valide l'hôte/origine, impose une limite de requête JSON et sert les assets locaux sans CDN. Gardez `--data-dir` dans un dossier privé et sauvegardez-le avant de supprimer ou de modifier ses fichiers.

## Guides complets

- [Guide CLI français](docs/GUIDE_CLI_FR.md)
- [Guide de l'interface locale](docs/GUIDE_INTERFACE_FR.md)
- [Réconciliation et provenance des sources](docs/source_reconciliation.md)
- [Formalisme opérationnel f4_v0](formalisme_operationnel_FulleGenBrain_f4_v0.tex)
- [Formalisme FulleGenBrain 5](formalisme_FulleGenBrain_5.tex)
- [Théorie de programmation compositionnelle 3](theorie_programation_compositionnelle_3.tex)
- [Notices des sources amont](THIRD_PARTY_NOTICES.md)

## Commandes utiles

```bash
./run_fullegenbrain.sh --data-dir ./data-local doctor
./run_fullegenbrain.sh --data-dir ./data-local components
./run_fullegenbrain.sh --data-dir ./data-local adapters
./run_fullegenbrain.sh --data-dir ./data-local inspect-sources
./run_fullegenbrain.sh --data-dir ./data-local validate examples/addition_program.json --input-file examples/addition_input.json
./run_fullegenbrain.sh --data-dir ./data-local synthesize --grammar examples/identity_grammar.json --examples examples/identity_examples.json --search-id identity-demo-001 --max-candidates 20
./run_fullegenbrain.sh --data-dir ./data-local resume identity-demo-001 --max-candidates 20
./run_fullegenbrain.sh --data-dir ./data-local memory check
./run_fullegenbrain.sh --data-dir ./data-local ascrc-plan examples/ascrc_plan.json
```

Les commandes JSON renvoient un statut et, lorsque pertinent, des diagnostics, des traces, des coûts et des identifiants de reprise. Les codes de sortie et statuts sont décrits dans le guide CLI.

## Tests et vérification

Le paquet `Dmodel` fournit des auto-contrôles exécutables sans installer de dépendances de développement :

```bash
./run_fullegenbrain.sh --data-dir ./data-local doctor
./run_fullegenbrain.sh --data-dir ./data-local test
python3 scripts/verify_vendored_files.py
python3 scripts/verify_deliverable_archive.py /chemin/vers/Dmodel_FulleGenBrain_f4_v0.zip
```

Le contrôle de compilation LaTeX est disponible si une distribution LaTeX (`pdflatex`) est installée :

```bash
python3 scripts/validate_latex_sources.py
```

La suite pytest intégrée complète, ses fixtures, `pytest.ini` et `requirements-dev.txt` sont livrés dans `suivi_model_FulleGenBrain_f4_v0.zip`, non dans le paquet d'exécution autonome. Pour exécuter cette suite, fusionnez les fichiers de suivi dans le même arbre de projet que `Dmodel`, installez `python3 -m pip install -r requirements-dev.txt`, puis lancez :

```bash
PYTHONPATH=src python3 -W error::ResourceWarning -m pytest -q
```

Les suites amont ont été exécutées séparément pendant l’audit de développement; leurs résultats, les reçus et les empreintes sont dans l’archive d’audit. Les anciens dépôts de sources et leurs tests ne sont pas inclus dans les trois ZIP de livraison. Les quelques modules amont nécessaires au fonctionnement des adaptateurs restent dans `vendor/`, séparés par composant et décrits par `vendor/runtime_vendor_manifest.json`.

## Organisation

- `src/fullegenbrain/` : application, runtime, CLI, adaptateurs et GUI.
- `web/` et `src/fullegenbrain/ui_static/` : assets UI locaux.
- `vendor/` : sous-ensemble runtime des composants spécialisés réellement branchés, manifestes de hashes et notices; les dépôts historiques complets ne sont pas livrés.
- `examples/` : entrées JSON reproductibles.
- `spec/` : schémas JSON nécessaires à la validation du runtime.
- `tests/` : suite intégrée.
- `scripts/` : validation, sauvegardes, benchmarks et empaquetage reproductible.
- `docs/reports/` et `logs/` : rapports, reçus et journal d'exécution; les données runtime privées restent hors du dépôt.

## Licence

Les fichiers originaux de l'intégration FulleGenBrain sont soumis à la [licence non commerciale](LICENSE). Elle ne remplace ni n'étend les licences des éléments amont; consultez les [notices de tiers](THIRD_PARTY_NOTICES.md). Aucun droit commercial n'est accordé par défaut.
