# Algorithme ORDER80.2.1 — spécification opérationnelle

## A. État initial

Le moteur charge `task.json`, `references.json` et `memory.json`. La mémoire n'est pas présumée correcte : elle est réutilisée uniquement selon les métadonnées de vérification enregistrées.

## B. Observation

Chaque ronde observe un sous-ensemble contrôlé : bootstrap → focused → expanded → broad. La recherche web ajoute des requêtes différentes issues du problème, du domaine, des lacunes et des termes réellement observés. Le RAG dynamique est rescanné à chaque ronde.

Les unités déjà vues sont éliminées par identifiant/hash. Une page web identique n'est pas comptée comme une nouvelle connaissance.

## C. Synthèse

La synthèse générale est extractive et déterministe : elle sélectionne des phrases de référence selon le recouvrement avec le problème et les critères déclarés. Chaque étape porte sa provenance.

Cette couche ne prétend pas transformer une affirmation documentaire en vérité universelle.

## D. Vérification

Le vérificateur général exige : évidence non vide, provenance présente, absence de lacunes déclarées et nombre minimal de sources distinctes. Un vérificateur de domaine peut être ajouté séparément pour des garanties plus fortes.

## E. Mémoire / nouveauté

Un candidat `PASS` est fingerprinté. S'il n'existe pas déjà, il est enregistré dans la mémoire et sous `news/`. Un candidat déjà présent produit `NOT_NOVEL`.

## F. Boucle longue

En cas de rejet, l'état du candidat et ses lacunes alimentent la prochaine vague de recherche. Si aucun progrès n'est disponible, le moteur attend avec un sommeil borné, écrit `CURRENT_REQUEST.json` et surveille le RAG. Ainsi, l'augmentation de durée ne se réduit pas à revérifier le même état.

## G. Fin

La boucle se termine par solution validée, interruption, expiration du budget ou absence de solution au sein du run. Aucune fin négative n'est interprétée comme impossibilité du problème.
