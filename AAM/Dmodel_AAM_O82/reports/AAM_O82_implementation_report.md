# AAM O82 — Rapport d'implémentation

## Description
Cette release implémente ROCA-D conformément à `model_AAM_O82.tex` : observation dégradée, empreintes partielles, retrieval mémoire obligatoire, suffisance décisionnelle, policy lexicographique/Pareto, bundles, apprentissage CEGIS, capsules de compétences, auto-observation causale, découverte de probes par composition, décomposition structurelle, root-retest, recovery, ledger et replay.

## Architecture
Le noyau est organisé en `contracts -> probes -> fingerprint -> memory -> sufficiency/policy -> verification -> engine`, complété par `learning`, `self_observer`, `discovery`, `composition`, `hierarchy`, `validation`, `benchmark` et `governance`.

Les raws sont archivés par hash; la mémoire utilise SQLite plus journaux append-only; les invalidations et les certificats sont rejouables; `FINAL` n'exécute que les compétences vérifiées compatibles.

## Pipeline complet
```text
preflight
-> contract
-> observe_min
-> raw/fingerprint
-> retrieve
-> decision_sufficiency
-> refine/bundle
-> verify
-> act OR correct/learn
-> discovery/decomposition/root-retest
-> self-observe
-> ledger/replay/recovery
```

L'acquisition suit `train -> CEGIS -> holdout -> OOD -> verification -> admission`, avec séparation stricte entre `EXPERIMENT` et `FINAL`.

## Commandes d'exécution
```bash
PYTHONPATH=src python -m aam_o82 doctor
PYTHONPATH=src python scripts/test_all.py
PYTHONPATH=src python scripts/validate_o82.py
PYTHONPATH=src python scripts/benchmark_o82.py
o82 acquire --dataset examples/demo_dataset.jsonl --contract examples/echo_contract.json --mode FINAL --workdir runs/acquire_final
o82 replay --episode <id> --workdir runs/runtime
```

Les commandes du README sont la source opérationnelle pour Linux/macOS/Windows et correspondent aux signatures actuelles du CLI.

## Résultats
P04: socle PC validé; P05: observation/raw/fingerprint validés; P06: mémoire quotient/recovery validés; P07: suffisance/policy/bundles validés; P08: apprentissage/correction 23/23 sur le gate correspondant; P09: auto-observation 31/31; P10: découverte/hierarchie 37/37; P11: validations adverses/ablations 45/45; P12: benchmark CLI et répétabilité logique PASS.

Le gate fonctionnel global final comporte 49/49 tests verts, incluant le test anti-hardcode non-régressif ajouté après P12. `scripts/validate_o82.py` retourne PASS, le benchmark P12 retourne PASS, et le scanner statique final retourne PASS. Le détail reproductible est enregistré dans `reports/P11_validation.json` et `reports/P12_benchmark.json`.
