# Rapport de phase P5 v3 — CLI et interface graphique

**Phase :** P5 — flux utilisateur CLI/GUI  
**Statut :** PASS_WITH_DOCUMENTED_PLATFORM_REQUIREMENTS

## 1. Description

P5 vérifie que le runtime expose les opérations déclarées à travers la CLI et l'interface graphique locale, et que les deux interfaces utilisent le même `ProbeModel`.

## 2. Architecture

CLI Python sous `src/esonde/cli.py`, GUI Tkinter sous `src/esonde/gui.py`. Le GUI exécute les travaux longs sur un worker hors du thread d'interface. Le chemin par défaut pointe vers `models/esonde_v3_demo_checkpoint.json` dont JSON et sidecar sont livrés.

## 3. Pipeline complet

Parcours CLI testé : train, update, generate, score, retrieve, inspect, audit, info, demo, relations, coref, retrait de lot, rejet des arguments invalides et vérification de split. Parcours GUI testé : entraînement, génération, score, récupération, inspection/audit, update et calibration ; validation des entrées et exécution hors thread UI.

## 4. Commandes d'exécution

```bash
python run_esonde.py --version
python run_esonde.py --help
PYTHONPATH=src python -m unittest discover -s tests -p 'test_cli_p3.py' -v
xvfb-run -a env PYTHONPATH=src python -m unittest discover -s tests -p 'test_gui_p4.py' -v
python run_esonde_gui.py
```

## 5. Résultats

- CLI : 6/6 tests passés, EXEC-0070.
- GUI : 4/4 tests passés, EXEC-0074.
- `--version` : `eSonde 0.3.0`, `--help` et aides des commandes de base passées, EXEC-0079 et EXEC-0084.

## 6. Interprétation

Les parcours des interfaces sont fonctionnels dans l'environnement et les scénarios testés. Le test GUI sous Xvfb n'établit pas que Tkinter est préinstallé sur toutes les plateformes ; l'utilisateur doit disposer de Tcl/Tk pour utiliser l'interface. La CLI reste indépendante de Tkinter.

## 7. Conséquences

- **Théoriques :** l'interface ne change pas le modèle probabiliste.
- **Conceptuelles :** CLI et GUI sont deux surfaces sur le même runtime et le même checkpoint.
- **Opérationnelles :** guides et chemins par défaut correspondent au code ; Python 3.10+ requis, Tkinter seulement pour GUI.

## 8. Conclusion

Les critères CLI et GUI sont satisfaits par les tests isolés. Le code de retour contrôlé et les durées sont dans les journaux référencés.

## 9. Statut du modèle

P5 fermée pour les scénarios utilisateur recensés ; cela ne valide pas la qualité linguistique générale.
