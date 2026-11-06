# AAM O82 — Rapport P05 Observation et empreintes

## Description
Validation des probes, contrats d'observation, conservation raw, empreintes partielles, témoins et budgets.

## Architecture
`ProbeRegistry -> contract validation -> raw archive -> FingerprintEngine -> witnesses -> BudgetLedger -> EventLedger`.

## Pipeline complet
`probe admissible -> coût -> observation -> raw/hash -> empreinte partielle -> witness -> persistance -> retrieval-ready`.

## Commandes d'exécution
```bash
PYTHONPATH=src python -m unittest tests.test_observation -v
PYTHONPATH=src python -m unittest tests.test_core.CoreTests.test_bundle_budget_sum -v
```

## Résultats
Les probes interdites et observations invalides sont rejetées; les raws sont conservés et relisibles; les témoins `VERIFIED` exigent des preuves; les budgets et l'exécution de bundles sont vérifiés. Gate P05: PASS.
