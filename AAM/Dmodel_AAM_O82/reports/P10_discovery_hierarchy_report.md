# AAM O82 — Rapport P10 Découverte et hiérarchie

## Description
Validation de la découverte de probes par composition, de la composition de compétences, de la décomposition structurelle et du root-retest.

## Architecture
`ProbeDiscoveryEngine` explore des compositions de probes admissibles et exige une amélioration sur induction et validation séparées. `SkillComposer` exige des dépendances vérifiées et compatibles. `StructuralDecomposer` ne fait qu'ouvrir des enfants structurels et `RootRetester` rejoue le parent avec le budget restant.

## Pipeline complet
`candidate composition -> induction/validation -> register -> skill composition -> structural decomposition -> child execution -> root retest`.

## Commandes d'exécution
```bash
PYTHONPATH=src python -m unittest tests.test_hierarchy_discovery -v
PYTHONPATH=src python scripts/test_all.py
```

## Résultats
Le gate P10 a atteint 37/37 tests `PASS` avant l'ouverture de P11, avec intégration du probe découvert au registry, liens parent-enfant valides, compatibilité des compétences et root-retest exécuté réellement.
