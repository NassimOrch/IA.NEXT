# Correctif préenregistré v1.2 — composition de composants

**Horodatage :** 2026-10-28, avant la nouvelle exécution de composition.

## Motif
Lors de l'audit, une divergence a été trouvée entre le protocole v1.1 et l'exécution initiale : le protocole indiquait les graines de composition 411, 522, 633, tandis que le lanceur a réutilisé 714, 825, 936. Cette divergence est conservée et documentée ; les anciens chunks sont archivés comme artefacts supersédés et ne sont pas agrégés dans les résultats de composition présentés comme confirmatoires.

## Correctif limité
Ce correctif ne change ni tâches, ni modèles, ni tailles, ni budgets, ni métriques, ni règles d'exclusion. Il ne change que la séquence de graines, afin de suivre la section 3 du protocole v1.1 : `two_moons` et `breast_cancer`, graines 411, 522, 633 (six chunks). Le découpage utilise `seed + 100`, l'initialisation enseignant `seed + 7000`, et l'index de répétition dérive de l'ordre fixe `[411, 522, 633]`.

## Contrôles maintenus
- Le même modèle enseignant MLP à 16 unités cachées.
- 16 sondes RBF scalaires ajustées seulement sur entrées d'entraînement et activations observées sur train.
- 12 centres RBF en 2D, 8 en 30D ; Adam à 0,012, 150 époques.
- Évaluation sur test gelé, remplacements de 1, 4 et 16 unités ; lecteur aval source conservé.
- Les anciens résultats 714/825/936 restent accessibles dans `audit/superseded_composition_chunks_v1_1/` et ne sont pas effacés ni mélangés aux nouveaux.
- Aucun choix de modèle ou de métrique n'est fait à partir des nouveaux scores de test.

## Empreintes avant exécution
Les SHA-256 du présent correctif et des scripts de composition/finalisation sont enregistrés dans `audit/gel_composition_v1_2_sha256.json` avant de lancer les six chunks.
