# AAM O82 — Rapport P08 Apprentissage et correction

## Description
Validation de l'apprentissage comportemental générique, holdout/OOD, correction CEGIS, capsules de compétences et séparation EXPERIMENT/FINAL.

## Architecture
`Dataset split -> learner -> failure/correction loop -> candidate capsule -> holdout -> OOD -> verifier -> admission -> FINAL retrieval`.

## Pipeline complet
`train -> evaluate train -> disagreement -> correction -> candidate -> holdout -> OOD -> verification -> conditional admission`.

## Commandes d'exécution
```bash
PYTHONPATH=src python -m unittest tests.test_learning tests.test_learning_protocol -v
PYTHONPATH=src python scripts/validate_o82.py
```

## Résultats
Le cycle de correction est persistant; `EXPERIMENT` ne promeut pas automatiquement; `FINAL` exige holdout/OOD et interdit le teacher actif; une compétence acquise est ensuite retrouvable au runtime. Le gate correspondant à l'apprentissage est PASS.

## Interprétations des résultats
Learning and correction are integrated into runtime control.

## Conséquence
### Théorique
Candidate learning remains separated from FINAL certification.
### Conceptuelle
CEGIS output can be re-retrieved and its required views acquired before verification.
### Opérationnelle
Les artefacts et traces restent persistants et rejouables dans le protocole de la phase.

## Conclusions
La phase satisfait son gate documentaire et fonctionnel au niveau des essais enregistrés.

## Statut du model
**PASS / phase verrouillée au moment du rapport.**
