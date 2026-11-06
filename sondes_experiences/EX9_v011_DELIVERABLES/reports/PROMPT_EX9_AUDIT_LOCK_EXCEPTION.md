# Exception documentaire au verrou multi-domaines — EX9 v011

Date : 2 novembre 2026.

## Résultat

Le snapshot pré-test `MODEL_LOCK_MULTI_DOMAIN.json` comprend 295 entrées. La vérification post-test donne **294/295 correspondances exactes** (SHA-256 et taille). L'unique divergence est le rapport documentaire `reports/PROMPT_EX9_AUDIT.md`, mis à jour après le gel pour consigner les résultats et la reprise.

| Champ | Valeur |
|---|---|
| Entrées gelées | 295 |
| Entrées identiques | 294 |
| Exceptions | 1 |
| Chemin exceptionnel | `reports/PROMPT_EX9_AUDIT.md` |
| SHA-256 gelé | `b929309ed84030016f3890dccb2f1892c3f5cb14816eb3159c3f20196ef41fd5` |
| Taille gelée | 6104 octets |
| SHA-256 courant | `2019675099cda14fd525e44626081aeab27697d81467e3adfa3b4a52b5be0463` |
| Taille courante | 8896 octets |

## Portée

Le fichier est explicatif et ne participe pas à l'entraînement, à la création des datasets, au prétraitement, à la génération du holdout, aux prédictions ou au calcul des métriques. Tous les chemins de modèles, données, configurations, scripts de génération/entraînement/évaluation et prédictions inclus dans le verrou restent identiques. Le verrou pré-test n'a pas été réécrit.

Formulation exacte : **294/295 fichiers identiques ; une exception documentaire post-gel explicitement déclarée ; modèles, protocole, données et code expérimental vérifiés inchangés**. Ne pas annoncer 295/295. Voir aussi `results/processed/MULTI_DOMAIN_LOCK_POSTTEST_AUDIT.json`.
