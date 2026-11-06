# P05 — Rapport d’intégration CEGIS / correction / apprentissage

## Description
La phase P05 intègre l’apprentissage par correction dans la machine autoritaire AAM O82_0. Le learner reste séparé du verifier et de la policy; aucune réponse métier n’est codée dans le noyau.

## Architecture
`LEARN` pilote un `CEGISLoop` persistant : hypothèse → test des observations → contre-exemples → correction candidate → ajout de sonde séparatrice → retest → évaluation holdout/OOD → capsule de compétence → admission conditionnelle. `Engine.LEARN` écrit les itérations et la complétion dans le ledger, puis récupère à nouveau la mémoire et planifie explicitement les vues manquantes avant `VERIFY`.

## Pipeline complet
`INIT → OBSERVE → RETRIEVE → REFINE/INFER → TEST → CORRECT/LEARN → CEGIS → HOLDOUT/OOD → RETRIEVE → VERIFY → MEMORIZE → ACT → DONE`. En EXPERIMENT, la capsule reste `CANDIDATE_SKILL`; en FINAL, une promotion exige validation holdout/OOD et absence de teacher.

## Commandes d’exécution
Depuis `Dmodel_AAM_O82_0/` :

```bash
PYTHONPATH=src python -W error::ResourceWarning -m unittest tests.test_p05_cegis tests.test_learning tests.test_learning_protocol tests.test_p05_engine_learning tests.test_bundle_skill tests.test_state_p02 tests.test_core -v
```

Pour le flux PC :

```bash
PYTHONPATH=src python -m aam_o82 run --problem examples/task.json --contract examples/echo_contract.json --budget '{"time":10,"compute":10,"memory":10,"energy":10,"parallelism":1,"external_quota":10}' --mode EXPERIMENT
```

## Résultats
18/18 tests ciblés P05/P02/core passent avec `ResourceWarning` traité comme erreur. Le cycle runtime d’apprentissage produit `CEGISIteration` et `LearningCompleted`, conserve les corrections, respecte le cutover teacher et rend la compétence acquise réutilisable. La trajectoire de compétence atteint `VERIFY → MEMORIZE → ACT → DONE` lorsque l’horizon contient le cycle terminal.

## Interprétations des résultats
Le pipeline d’apprentissage est désormais une capacité du runtime et non un service externe isolé. Les erreurs observées pendant P05 ont distingué les défauts du modèle des dérives de banc : le cas de compétence était un horizon de test trop court, tandis que la logique LEARN→observations manquantes était bien un défaut modèle et a été corrigée.

## Conséquence
### Théorique
La boucle erreur/correction devient une transition autoritaire compatible avec l’architecture formelle.
### Conceptuelle
Une erreur guide la recherche mais ne certifie jamais une réponse; la preuve indépendante reste requise.
### Opérationnelle
Le PC peut acquérir, valider et mémoriser une compétence sans teacher dans FINAL, avec traçabilité complète.

## Conclusions
P05 est complètement implémentée pour son périmètre et aucune correction P05 reste ouverte. Les mécanismes de self-observation, découverte et hiérarchie restent des phases séparées et bloquantes conformément au plan maître.

## Statut du model
**P05 = PASS / phase verrouillée.**


## Commandes d'exécution
```bash
cd Dmodel_AAM_O82_0
PYTHONPATH=src python -W error::ResourceWarning -m unittest tests.test_learning tests.test_learning_protocol tests.test_p05_cegis tests.test_p05_engine_learning
```
