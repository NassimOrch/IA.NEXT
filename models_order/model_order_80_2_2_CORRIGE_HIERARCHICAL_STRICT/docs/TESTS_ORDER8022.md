# Tests ORDER80.2.2

```bash
python3 -m pytest -q
python3 self_test_order8022.py
python3 -m compileall -q .
```

La suite valide : boucle hiérarchique, décomposition unique par nœud, retest racine, peer-probes, séparation documentaire/solution, RAG dynamique hérité, contrôles web et absence de modification du manifeste en `--no-web`.

Le benchmark externe O80.2.1/O80.2.2 se trouve dans l’audit de release et comprend six problèmes : mathématiques résolu facile, mathématiques résolu difficile, deux problèmes mathématiques ouverts, un problème d’ingénierie résolu et un problème historique non résolu.
