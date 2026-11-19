# Diagnostic Obsiss held-out — premier token de réponse

## Description
Expérience P0 `V8-P0-OBSISS-HELDOUT-NEXT-TOKEN-001` exécutée sur 12 contextes extraits du split TEST tree-isolated OASST1. Elle évalue seulement le classement de candidats pour le premier token, pas la génération complète d'une réponse. La non-réponse est désactivée. Le token cible n'est consulté qu'après classement pour calculer les métriques.

## Architecture et variantes
256 Obsiss actifs, dimension 16, limite de 16 candidats. Cinq variantes sont comparées : historique V7, sans contexte propre, sans observation croisée, sans les deux signaux, et permutation croisée identité.

## Pipeline et commande
Le script `experiments/run_obsiss_heldout_token_ranking.py` lit `derived/OASST1_chat/test.jsonl`, choisit deux exemples par langue (en, es, fr, de, ru, zh), propose les candidats sans accès au token cible, exécute P/R Obsiss, puis calcule les rangs après classement. Le journal conserve les 12 exemples. Le résultat JSON est le reçu primaire.

## Résultats
- 12 exemples évalués ; 16 candidats par exemple.
- Rappel du pool de candidats : **1/12 = 8,33 %** pour chacune des cinq variantes.
- MRR : **0,020833** pour chacune des cinq variantes.
- Le seul token cible présent dans le pool est `das` (allemand), au rang 4 ; les 11 autres cibles sont absentes du pool avant le classement.
- Les changements de paramètres déplacent certains top-1/top-5, mais n'améliorent pas les métriques de récupération de la cible sur cet échantillon.
- Durée enregistrée : environ 10,84 secondes.
- Résultat JSON SHA-256 : `4d97e25e03ddffdf99936f21e12d0d165d1d470888a61f33dcf58fba0fd1fd9f`.

## Interprétation
Sur cet échantillon restreint, le goulot principal observé est la proposition/couverture des candidats : le classement Obsiss ne peut pas classer un token qui n'a pas été proposé. L'égalité des métriques entre variantes ne prouve pas l'équivalence des mécanismes ; elle reflète ici surtout l'absence de la cible dans 11 pools et un unique rang 4. L'échantillon de 12 ne permet pas une conclusion générale sur le modèle ni sur les langues.

## Conséquences
- Théoriques : séparer explicitement le rappel du pool de candidats et la qualité du classement conditionnelle à la présence de la cible.
- Conceptuelles : stabilité interne du vote et qualité de réponse ne sont pas assimilables.
- Opérationnelles : prochaine expérience à préenregistrer sur un échantillon plus large, avec analyse du rappel à chaque source de proposition ; aucune génération libre n'est lancée par ce diagnostic.

## Conclusion et statut
`COMPLETED_COMPONENT_DIAGNOSTIC`; résultat de rappel défavorable sur ce petit échantillon, sans constituer un verdict sur la possibilité d'amélioration du modèle. P0 reste `IN_PROGRESS`; P3 reste `NOT_STARTED`.

## Preuves et intégrité
- Données TEST SHA-256 : `65819ed0582f9cde0fbe9a5a322c6354081d289967e4474a0ba3db0801153f44`.
- Profil SHA-256 : `c517a0a5023add538d7588853652cc01cc7e5f3b305e404d34df6d35cc881544`.
- Poids SHA-256 : `8526943d1528418fa8bbbf9128b61b5e1acd90a16eeb7cc062e18864b083dff4`.
- Résultat SHA-256 : `4d97e25e03ddffdf99936f21e12d0d165d1d470888a61f33dcf58fba0fd1fd9f`.
