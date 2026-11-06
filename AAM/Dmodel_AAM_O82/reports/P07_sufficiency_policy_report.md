# AAM O82 — Rapport P07 Suffisance et politique

## Description
Validation de la suffisance décisionnelle, de l'abstention, de la policy lexicographique/Pareto, de la valeur marginale des probes et des bundles.

## Architecture
`Memory retrieval -> candidates -> sufficiency predicate -> hard filters -> verification gain -> Pareto/resource efficiency -> lexicographic choice -> sequential/bundle acquisition`.

## Pipeline complet
`observation -> retrieval -> sufficiency? -> verify/close OR policy -> next probe/bundle -> retrieval -> repeat`.

## Commandes d'exécution
```bash
PYTHONPATH=src python -m unittest tests.test_policy -v
PYTHONPATH=src python -m unittest tests.test_bundle_skill -v
```

## Résultats
La mémoire par sous-empreinte peut fermer une décision après raffinement; plusieurs décisions vérifiées ne suffisent pas; les contraintes scope/level/safety sont obligatoires; le gain de vérification domine les économies de ressources dans l'ordre lexicographique; les bundles admissibles s'exécutent réellement en parallèle. Gate P07: PASS.
