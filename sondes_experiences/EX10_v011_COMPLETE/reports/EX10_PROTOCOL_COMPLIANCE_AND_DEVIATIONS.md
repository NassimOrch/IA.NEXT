# EX10 v011 — conformité protocole et déviations

## Variantes 1 et 2

Les scripts EX8 v010 ont été réutilisés sans modification algorithmique. Les splits, graines `[1501,1607,1717,2029,3037]`, paramètres et comparateurs MLP appariés/GE4X sont conservés. Les cinq backbones historiques B10/B11 ont été réutilisés, et A0 charge les checkpoints globaux V009 prévus par le runner original. `run_pca_v010.py` ne diffère que par la résolution du chemin racine. Wisconsin et SMS sont des réplications sur jeux déjà exposés ; ils ne sont pas présentés comme holdouts vierges.

## Variante 3

CNG comprend quatre tâches, cinq graines, huit architectures et huit MLP appariés par tâche/graine, plus sept ablations LOO de G3/M7 par tâche/graine : 460 runs. CNC comprend six sondes élémentaires × cinq graines (30 runs) et trois compositions × cinq graines × C1/C2/C3-MPL/C3-RBF (60 runs) : 90 runs. Les protocoles train-only KMeans, centres et largeurs RBF apprenables, Adam, batch 64, 500 époques maximum et patience 30 sont enregistrés par configuration.

## Gel et holdouts

Le modèle-lock pré-test a été créé avant lecture des tests : 3 037 fichiers hashés, 550 modèles et 195 fichiers de test/stress conservés opaques. Le scoring a été lancé une seule fois et a écrit 1 695 lignes. Le post-audit n'a recalculé les métriques qu'à partir des fichiers de prédictions persistés et vérifié les hashes sources en mode octet ; il n'a pas rouvert les arrays sources de test ni relancé de modèle.

## Déviation/limite majeure : chronométrage d'entraînement

Deux runners CPU ont temporairement tourné en concurrence pendant une partie de la campagne. Le profil détaillé marque 370/550 durées `RECORDED_NO_OVERLAP_DETECTED` et 180/550 `CONTENDED_OR_UNVERIFIED`. Les 180 dernières sont exclues de toute comparaison de durée ; les autres restent descriptives, sans revendication de vitesse générale. Le profilage d'inférence CPU séquentiel homogène des 550 checkpoints est distinct et vérifié : 1 thread, batches 1/16/64/256, 5 warmups et 50 répétitions. Une seconde trace séquentielle conservée utilise batches 1/64 et 20 répétitions. Il n'y a pas de mesures d'énergie et pas de compteurs FLOPs/MAC matériels instrumentés fiables ; seuls des comptes structurels sont rapportés.

## Données sources

Le corpus SMS est utilisé pour l'extension classification secondaire. Wisconsin est conservé pour la réplication EX8. Les datasets de scénarios de l'archive source ne sont pas des tâches numériques/classification appropriées aux architectures testées ; ils ne sont pas utilisés. Les benchmarks CNG/CNC sont générés mathématiquement à partir des graphes théoriques ; les générateurs, graines, manifests et fichiers sont inclus.

## Quarantaine

Les essais frais de classification non conformes et les anciennes exécutions CNC concurrentes sont conservés dans `results/attempts/` et `results/core/quarantine/`, séparés des résultats principaux. Aucun artefact quarantiné n'est inclus dans les agrégats valides.

## Audits d'artefacts supplémentaires

- Classification : 90 fichiers de résultats, 90 checkpoints et 90 fichiers de prédictions vérifiés par SHA-256 ; 30 historiques embarqués dans les JSON et 60 historiques séparés contrôlés ; 100 fichiers modèle présents en incluant les 10 backbones partagés.
- Profil ressources : 550 identifiants uniques, 550 checkpoints vérifiés et 2 200 profils batch vérifiés.
- Tests invariants : 6/6 PASS.
