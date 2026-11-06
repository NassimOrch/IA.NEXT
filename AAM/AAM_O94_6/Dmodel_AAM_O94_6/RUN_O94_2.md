# Lancer et diagnostiquer AAM O94.2

1. Extraire `Dmodel_AAM_O94_2.zip` dans un dossier local accessible en écriture.
2. Lancer `run_AAM_O94_2.bat` sous Windows ou `./run_AAM_O94_2.sh` sous Linux/macOS.
3. Si le préflight bloque, lire son rapport JSON. Sous Windows, ouvrir `logs/O94_2/launcher_windows.log`.
4. Vérifier les versions et contrôles avant modification :

```text
python -m aam_o93 preflight
python -m aam_o93 status
python -m aam_o93 --help
```

Pour les captures, utiliser des commandes argv sous forme de liste JSON et ne pas activer l’exécution d’une cible si son origine/autorisation n’est pas vérifiée. Les traces restent dans le dossier défini par l’utilisateur. Pour un modèle local personnalisé, confirmer le script adaptateur uniquement après inspection.

Pour reproduire les tests depuis l’environnement de développement :

```text
python -m compileall -q aam_o93 tests
python -m pytest -q tests/test_o942_live_observation.py tests/test_o941_model_integration.py
xvfb-run -a python -m pytest -q tests/test_o931_ui_smoke.py tests/test_o931_language_model_training_surface.py
```

Le test sur une machine Windows réelle et les fournisseurs/poids/capteurs de l’utilisateur ne peuvent pas être remplacés par les tests simulés. Consigner leur environnement et leurs reçus lors de la validation cible.
