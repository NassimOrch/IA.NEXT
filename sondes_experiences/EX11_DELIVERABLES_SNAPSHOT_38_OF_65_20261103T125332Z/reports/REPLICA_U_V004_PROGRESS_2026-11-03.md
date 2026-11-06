# REPLICA-U v004 — progression confirmatoire

Snapshot : 2026-11-03 12:34 UTC. Runs de validation complets inscrits : **16/65** sur **4/13** datasets présents. Test scellé non ouvert. Les rapports v004 déclarent `final_models_refit_scope=all_outer_train`.

La campagne est séquentielle ; les temps ne sont pas contaminés par une autre campagne d’entraînement EX11 au moment de ce snapshot. Les chiffres suivants sont validation-only et provisoires jusqu’à la fermeture des cinq graines/datasets.

| Dataset | Runs | Student 64/32 log-loss | Backbone | MLP matched | Wins student vs matched |
|---|---:|---:|---:|---:|---:|
| dataset_31_credit-g | 5/5 | 0.511185 | 0.523057 | 0.507849 | 1/5 |
| dataset_44_spambase | 5/5 | 0.174179 | 0.195039 | 0.179177 | 3/5 |
| dataset_50_tic-tac-toe | 5/5 | 0.065201 | 0.083897 | 0.048941 | 0/5 |
| gina_agnostic | 1/5 | 0.244389 | 0.256619 | 0.222599 | 0/1 |

## Lecture prudente

- German Credit (5/5) : student 64/32 améliore le backbone en moyenne mais ne bat le MLP apparié que 1/5 seeds ; le MLP apparié a la meilleure log-loss moyenne.
- Spambase (5/5) : student 64/32 améliore le backbone et bat le MLP apparié sur 3/5 seeds ; les moyennes restent proches.
- Tic-Tac-Toe (5/5) : le MLP apparié est nettement meilleur que le student 64/32 sur les cinq seeds ; ne pas agréger avec les autres jeux comme s’il s’agissait d’une réplication homogène.
- GINA (1/5) : première graine seulement ; aucun verdict.

## Limites

Ces résultats ne sont pas des scores de test. Les 13 datasets appartiennent à des familles et régimes différents ; les cinq jeux PROMISE sont apparentés. Les métriques et durées par run sont conservées dans les JSON de résultats, les checkpoints, les prédictions et les configurations. Le rapport final ne sera établi qu’après 65/65 ou statut `INCOMPLETE_QUOTA` explicite.
