# Audit AAM O94.6

Cette archive rassemble le rapport d’essais, les checklists séquentielles, les registres d’erreurs, les reçus de phases, les journaux bruts, les preuves des tâches réelles, les oracles de test conservés séparément du runtime, les manifestes et les reçus de validation du packaging.

## Lecture des preuves

- `receipts/O94_6/P8_fresh_extract_full_matrix.json` décrit la matrice des 92 fichiers de test exécutés sur une extraction neuve du candidat : 12 lots, 449 réussites cumulées, 0 échec, 0 timeout.
- `logs/O94_6/P8_extract_matrix_XX_of_12.log` et les `*_driver.log` contiennent les sorties brutes; les hashes sont inscrits dans le reçu de matrice.
- `real_task_tests/O94_6_replay/evidence/` contient notamment les requêtes, sorties exactes, prompt capturés, traces et reçus des tests.
- `real_task_tests/O94_6_replay/oracles/` reste séparé du code runtime afin que les attentes d’évaluation ne soient pas présentées comme des connaissances intégrées au modèle.
- `release_reports/P8_final_release_validation.json` lie la release au SHA-256 exact du ZIP modèle et enregistre aussi la réserve sur le code retour externe du smoke test ciblé.

`PASS_BOUNDED` veut dire que les critères testés sont passés dans les bornes documentées; ce n’est pas une certification universelle de chaque capacité imaginable. Les poids utilisateur SmolLM2-360M n’étaient pas présents dans l’environnement d’audit et n’ont pas été prétendus testés.
