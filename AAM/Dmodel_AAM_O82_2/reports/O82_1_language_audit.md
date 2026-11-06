# Audit de branche O82_1

## Description
Cette branche incorpore la correction de généralisation textuelle générique au parent correspondant.

## Architecture
Exact-match mémoire prioritaire, puis n-grammes de caractères hachés appris sur train seulement ; prédictions généralisées non-certifiantes sous contrat exact sans preuve externe propre au cas.

## Pipeline complet
Acquisition train -> empreintes -> learner généralisant -> holdout/OOD -> vérification -> mémoire -> runtime exact/candidate -> audit.

## Commandes d'exécution
`PYTHONPATH=src python scripts/test_all.py`
`PYTHONPATH=src python scripts/validate_o82.py --output reports/O82_1_validation_final.json`
`PYTHONPATH=src python scripts/benchmark_o82.py --output reports/O82_1_benchmark_final.json`
`PYTHONPATH=src python -m aam_o82 audit`

## Résultats
115/115 tests PASS pour O82_1 ; 59/59 pour O82_c0. Holdout anglais : 81.81% couverture, 81.67% accuracy. OOD anglais : 79.79% couverture, 79.39% accuracy.

## Interprétations des résultats
La branche élargit fortement la couverture par rapport au parent, sans supprimer la voie de preuve exacte.

## Conséquence : théorique, conceptuelle, opérationnelle
Théorique : coexistence exacte/généralisée sous hiérarchie de preuve. Conceptuelle : mémoire comme première voie, apprentissage généralisant comme voie candidate. Opérationnelle : surcharge temporelle mais RSS proche du parent.

## Conclusions
La correction est légitime et expérimentalement bénéfique sur le corpus réel.

## Statut du modèle
PASS technique ; performance de généralisation significativement améliorée, encore inférieure au contrôle externe sur accuracy brute.
