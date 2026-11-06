# Architecture ORDER80.2.1

```text
CLI
 │
 ▼
GeneralResearchEngine
 ├── ReferenceCatalog
 │    ├── racines locales
 │    ├── références web
 │    ├── allowlist contenu
 │    └── allowlist moteurs de recherche
 │
 ├── GeneralLocalObserver
 │    └── chunks + hash + protection symlink/taille
 │
 ├── SecureWebObserver
 │    ├── URL policy
 │    ├── DNS/public-IP validation
 │    ├── TLS hostname verification
 │    ├── redirect revalidation
 │    └── bounded text retrieval
 │
 ├── AdaptiveSearchPlanner
 │    └── requêtes évolutives depuis problème + observations + lacunes
 │
 ├── GeneralSolutionSynthesizer
 │    └── synthèse extractive avec provenance
 │
 └── GeneralMemory
      ├── artefacts vérifiés
      └── news/<revision>_<fingerprint>/
```

L'ancien noyau formel ORDER80.2 et les anciens contrôleurs sont conservés sous `legacy_order8020/` uniquement pour la traçabilité de l'évolution. Le point d'entrée de la release 8.0.2.1 ne dépend d'aucun corpus ou résultat spécifique à une cible particulière.
