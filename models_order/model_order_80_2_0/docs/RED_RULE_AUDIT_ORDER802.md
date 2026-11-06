# Audit des règles rouges ORDER80.2

## Règle 1 — aucun verdict externe prématuré

Le moteur n'interprète pas `UNRESOLVED` comme impossibilité, falsité ou impossibilité de vérification. `UNRESOLVED` signifie uniquement qu'aucun certificat complet n'a été produit et accepté par le noyau pendant l'exécution observée.

Le statut `VERIFIED_COMPLETE` ne peut apparaître qu'avec une preuve complète dont les obligations locales ferment au noyau.

## Règle 2 — aucune triche ni sabotage

Le code exécutable ne contient pas une solution spécifique au domaine cible. Les informations documentaires et web sont séparées du stock d'axiomes formels. Les certificats observés sont revalidés avant utilisation.

Le moteur n'introduit pas non plus de branche spéciale disant que la cible doit réussir ou échouer.

## Règle 3 — le modèle fait le jeu

Le contrôleur n'insère aucune étape de démonstration spécifique. Il fournit seulement :

- la tâche formalisée ;
- les interfaces d'observation ;
- les règles du calcul ;
- la décomposition générique ;
- la mémoire de certificats vérifiés.

Le moteur recherche lui-même les applications de règles et d'observations disponibles.

## Audit automatique

`self_test.py` vérifie :

- fermeture des hypothèses ;
- revalidation des lemmes ;
- adaptation de l'observation ;
- web et recherche configurables ;
- import de bibliothèque ;
- absence de plusieurs marqueurs de solution codée en dur dans les sources exécutables.
