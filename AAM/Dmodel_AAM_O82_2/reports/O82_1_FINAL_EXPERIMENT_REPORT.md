# Rapport final d'expérience — O82_1

## Description
O82_1 est la branche corrigée issue de O82_0. Elle a été testée sur des SMS réels provenant du corpus `SMSSpamCollection`, sur holdout anglais, OOD anglais, OOD multilingue et perturbations textuelles.

## Architecture
La branche conserve ROCA-D : observation dégradée, empreintes partielles, retrieval mémoire, suffisance, policy, bundles, CEGIS, mémoire, self-observation, discovery, décomposition, recovery/replay et surfaces O81. Elle ajoute un learner textuel générique par n-grammes de caractères hachés, placé après l'exact-match et soumis au truth gate.

## Pipeline complet
Provenance dataset -> train only -> apprentissage exact+généralisé -> holdout/OOD -> perturbations -> runtime exact closure -> runtime generalized candidate -> contrôle de ressources -> audit.

## Commandes d'exécution
```bash
PYTHONPATH=src python scripts/test_all.py
PYTHONPATH=src python scripts/validate_o82.py --output reports/O82_1_validation_final.json
PYTHONPATH=src python scripts/benchmark_o82.py --output reports/O82_1_benchmark_final.json
PYTHONPATH=src python -m aam_o82 audit
```

## Résultats
Les deux branches ont passé leur suite complète : O82_1 = 115/115, O82_c0 = 59/59. Sur 5031 lignes anglaises à provenance sûre, holdout = 753 et OOD = 757. La version corrigée couvre 81.81 % du holdout avec 81.67 % d'accuracy globale et 99.84 % de précision sélective, puis 79.79 % de couverture OOD avec 79.39 % d'accuracy globale et 99.50 % de précision sélective.

Sur le test de perturbation de 600 SMS, la couverture passe de 3.5 % pour les parents à 87.33 % pour O82_1, avec 87.0 % d'accuracy et 99.62 % de selective accuracy.

Ressources d'acquisition complète anglaise : O82_1 = 15.99 s, 117344 KB RSS, 36208 KB de sorties ; O82_c0 = 16.25 s, 113144 KB RSS, 53176 KB.

## Interprétations des résultats
Le gain est principalement un gain de couverture et de robustesse, pas une simple hausse de mémorisation. L'exact-match reste prioritaire. Les prédictions généralisées inédites restent candidates sous un contrat exact lorsqu'aucune preuve externe propre au cas courant n'est disponible.

## Conséquence : théorique, conceptuelle, opérationnelle
Théorique : séparation entre preuve de compétence et preuve du cas. Conceptuelle : mémoire exacte et généralisation sont deux tempos distincts. Opérationnelle : coût d'acquisition plus élevé mais surcharge RSS modérée.

## Conclusions
La correction est légitime et confirmée par les tests réels. Elle réduit fortement la dépendance à l'empreinte exacte sans introduire de réponse métier codée.

## Statut du modèle
PASS technique et expérimental sur le protocole enregistré ; la généralisation reste perfectible par rapport au contrôle externe et ne constitue pas une garantie universelle.
