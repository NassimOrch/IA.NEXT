# Environnement et dépendances

## Environnement observé

- OS : Linux x86_64, noyau `6.18.55`
- Python : 3.13.5
- NumPy 2.3.5; pandas 2.2.3; SciPy 1.17.0; scikit-learn 1.8.0; PyTorch 2.10.0+cpu; Matplotlib 3.10.8; jsonschema 4.26.0
- Outils système : `unzip`, `zipinfo`, `pdftotext`, `latexmk`, `pdflatex`
- Modèles CPU pour cette campagne; aucun accélérateur GPU utilisé.
- Absents : `pyarrow`, `duckdb`, `polars`, `fastparquet` et `parquet-tools`; donc pas de lecture du contenu des fichiers Parquet dans ce travail.

## Méthodes de récupération

L'appel initial de l'outil Python visible a échoué avec `ChatGPTAgentToolRateLimitException`; cela n'indiquait pas une panne du système Python. Le shell système a ensuite exécuté `python3`, `zipfile`, `unzip`, `hashlib`, les scripts d'expériences et LaTeX. Les calculs longs ont été divisés par tâche; l'appel monolithique interrompu est conservé dans les logs puis les tâches ont été reprises séparément. Aucun résultat du run interrompu n'a été traité comme résultat complet.

## Reproduire

Les commandes exactes et modes d'exécution sont dans `REPRODUIRE_LES_EXPERIENCES.md`. Les logs `.stdout.log`, `.stderr.log` et `.exitcode` sont conservés sous `logs/`. Les versions de modules et variables de protocole sont référencées dans `run_config.json` par tâche, `reconstruction_config.json` et `loop_robustness_config.json`.


## Validation étendue du corpus source

La vérification récursive a haché 14 970 entrées de fichiers présentes dans les deux arbres extraits (copies non dédupliquées), environ 1,248 Go. Un scanner indépendant a contrôlé la syntaxe de 2 045 chemins Python (0 erreur AST), la syntaxe des fichiers JSON/JSONL et la signature de 106 PDF. Il a identifié deux chemins de logs JSON vides chacun présents dans les deux arbres et une dernière ligne tronquée dans `batch_dataset.jsonl`; les journaux bruts restent inchangés. Le détail et les empreintes sont dans `results/source_audit/recursive_source_file_manifest.csv` et `.json`. Les PDF ont uniquement été contrôlés à la signature par ce scanner; le formalisme prioritaire a, lui, été compilé/rendu séparément.
