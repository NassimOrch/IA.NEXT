# AAM O82 — Rapport P09 Auto-observation

## Description
Implémentation des états auto-observables autorisés, déclencheurs prioritaires, intervention causale appariée et méta-policy candidate.

## Architecture
`SelfObserver` contrôle les champs observables, rejette les champs non autorisés, mesure les interventions sur cas appariés et produit des méta-policies candidates. `Engine` persiste les événements `SelfObserved`; `MemoryQuotient` persiste les méta-policies.

## Pipeline complet
`event -> trigger -> paired intervention -> effect -> candidate meta-policy -> admission gate`.

## Commandes d'exécution
```bash
PYTHONPATH=src python -m unittest tests.test_self_observation -v
PYTHONPATH=src python scripts/test_all.py
```

## Résultats
Le gate P09 a atteint 31/31 tests `PASS`, dont intégration Engine/ledger, rejet de champs interdits, causalité appariée, comparabilité des ressources, absence d'auto-promotion en `EXPERIMENT` et admission conditionnelle en `FINAL`.
