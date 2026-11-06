# AAM O82 — Rapport P06 Mémoire quotient

## Description
Validation de la mémoire quotient, du retrieval immédiat, de l'invalidation, de la consolidation non destructive et du recovery.

## Architecture
`RawStore + SQLite MemoryQuotient + append-only memory journal + invalidation log + recovery/replay index`.

## Pipeline complet
`observe -> raw -> fingerprint -> put/retrieve -> invalidate/correct -> consolidate -> recover -> verify raw references`.

## Commandes d'exécution
```bash
PYTHONPATH=src python -m unittest tests.test_memory -v
PYTHONPATH=src python scripts/validate_o82.py
```

## Résultats
Retrieval par sous-empreinte, consolidation avec provenance, invalidation persistante après recovery et détection d'altération raw passent. Gate P06: PASS.
