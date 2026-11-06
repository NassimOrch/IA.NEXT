# P06 — Rapport auto-observation / causalité / prédiction

## Description
La phase P06 transforme l’auto-observation en capacité runtime autoritaire. Elle conserve la séparation entre observation de l’état interne, vérification externe et vérité de tâche.

## Architecture
`SELF_OBSERVE` est un état explicite de la machine. Il mémorise la raison d’interruption et l’état appelant, construit une prédiction de prochaine observation, réserve les ressources correspondantes sans certifier le résultat, puis reprend l’état non terminal déclaré. Les interventions causales utilisent des cas appariés, des ressources comparables et une métrique vérifiée; la méta-policy ne devient `VERIFIED_META_POLICY` qu’après effet positif en FINAL.

## Pipeline complet
`événement interne → request/self-trigger → SELF_OBSERVE → SelfObserved → prediction/reservation → éventuelle intervention causale → persist evidence/meta-policy → RESUME(return_state) → RETRIEVE/continuation`. Une prédiction ne peut ni clôturer un contrat ni supprimer une vérification nécessaire.

## Commandes d'exécution
```bash
PYTHONPATH=src python -W error::ResourceWarning -m unittest tests.test_self_observation tests.test_state_p02 tests.test_p05_cegis tests.test_learning tests.test_learning_protocol tests.test_p05_engine_learning tests.test_bundle_skill tests.test_p04_memory -v
```

## Résultats
34 tests combinés P02–P06 passent avec `ResourceWarning` fatal. Les tests couvrent le trigger prioritaire, l’absence de supervision cachée, le resume dynamique, la causalité appariée, la persistance après recovery, la réservation/consommation et le cutover de méta-policy.

## Interprétations des résultats
L’auto-observation est désormais une branche de contrôle et non un simple journal. La prédiction reste explicitement non certifiante, tandis que la causalité fournit une preuve expérimentale séparée avant toute promotion de stratégie.

## Conséquence
### Théorique
Le processus d’apprentissage peut être observé comme objet interne sans fusionner observation et vérité.
### Conceptuelle
Une stratégie peut être proposée, causée et comparée avant son admission.
### Opérationnelle
Le runtime peut réserver puis consommer une ressource prévue et récupérer une trace causale complète après reconstruction mémoire.

## Conclusions
Toutes les exigences P06 sont couvertes sans ajout de solution métier codée. Les phases P07–P10 restent séparées et bloquantes.

## Statut du model
**P06 = PASS / phase verrouillée.**
