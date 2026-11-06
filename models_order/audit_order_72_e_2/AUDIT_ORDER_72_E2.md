# ORDER72 e2 — Audit expérimental et anti-fuite

## Objet
Cette archive conserve les sources, datasets, checkpoints, résultats bruts et protocoles nécessaires pour reproduire l'expérience de l'intuition de liaison des trajectoires.

## Contrat expérimental
Apprentissage : `(F_P, F_T, F_C, F_S, y)`.

Déploiement : `(F_P, {(F_Ti,F_Ci)}) -> choix`, sans `F_S`.

`F_S` est uniquement une cible d'apprentissage. Le checkpoint runtime n'a pas d'encodeur de solution.

## Anti-oracle
La référence de solution sert aux labels hors ligne et à l'évaluation. Elle n'est jamais fournie au runtime du modèle. La certification exacte est séparée et le guide n'est pas appelé dans CERTIFY.

L'audit est logiciel et reproductible ; il ne prétend pas établir une probabilité mathématique d'erreur ou de triche exactement nulle.

## Correction importante
La première représentation d'empreinte utilisée pendant la construction de e2 créait des collisions entre actions différentes. Elle a été remplacée par une empreinte hybride composée de 60 composantes sémantiques et de 12 bits d'identité SHA-256 de la représentation canonique. Le dataset et le modèle final ont été régénérés après cette correction.

## Dataset final
Train: 3263 requêtes / 280 problèmes / 8 familles.
Val: 877 / 70 / 8 familles.
Test: 535 / 90 / 8 familles.
OOD: 870 / 70 / familles hanoi4 et puzzle8, absentes de l'entraînement.

## Résultats micro-modèle
Test: top-1 69.3458 %, MRR 0.8257321, rang moyen 1.4841.
OOD: top-1 28.8506 %, MRR 0.5373372, rang moyen 2.6483.
Permutation identité: 200/200.
Argument F_S au runtime: absent.

## Intégration O72, 30 problèmes appariés
Parent O72 e1 + ancienne intuition: 7/30, 60.933 nœuds, 44.000 appels WM, 0.4303 s.
O72 e2 sans nouveau guide: 7/30, 60.933 nœuds, 44.000 appels WM, 0.3969 s.
O72 e2 + intuition liaison: 15/30, 61.367 nœuds, 44.367 appels WM, 0.4822 s.

Le guide modifie donc la recherche, mais n'entraîne pas une réduction automatique des simulations WM. Sur ce banc, le succès augmente alors que le nombre d'appels WM et le temps augmentent légèrement.

## Limites
Le dataset utilise principalement des préfixes de trajectoires proches du hasard autour de trajectoires de solution vérifiées. Il ne couvre pas encore de manière riche les détours arbitraires réellement productifs. L'OOD faible montre que l'abstraction apprise n'est pas universelle.
