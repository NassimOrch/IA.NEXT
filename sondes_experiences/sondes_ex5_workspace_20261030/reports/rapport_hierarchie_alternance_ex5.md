# Rapport hiérarchique question→réponse et alternance A↔B

## Cloisonnement questions/réponses

Les trois topologies question→réponse ont cinq graines. Le niveau Q-only expose uniquement `X` à son interface et le pré-entraînement autoencodeur reconstruit `X_train` sans `Y`. Les labels `Y_train` servent uniquement de cibles de perte du niveau réponse. L'API d'inférence est `forward(x)` ; aucun label n'est passé au modèle. Les deux nouveaux runs Q-only seed 1501 remplacent uniquement ce seed dans le résumé harmonisé pour HYBRID_HYBRID et ADAPTIVE_THEN_FIXED ; les traces anciennes restent conservées.

| Topologie | P sonde | Accuracy | Log-loss | MLP ge4 ratio min | Accuracy MLP | Log-loss MLP |
|---|---:|---:|---:|---:|---:|---:|
| HYBRID_HYBRID | 564 | 0.97412 | 0.05881 | 4.0301× | 0.97647 | 0.05280 |
| FIXED_THEN_ADAPTIVE | 314 | 0.85412 | 0.31111 | 4.0860× | 0.97882 | 0.05315 |
| ADAPTIVE_THEN_FIXED | 262 | 0.98118 | 0.06914 | 4.0153× | 0.97882 | 0.05291 |
| TWOLEVEL_OOF_RESIDUAL_ADAPTIVE | 1160 | 0.97647 | 0.05218 | 4.0078× | 0.98588 | 0.05037 |
| TWOLEVEL_OOF_RESIDUAL_FIXED | 1160 | 0.97647 | 0.06856 | 4.0078× | 0.98588 | 0.05037 |

`ADAPTIVE_THEN_FIXED` donne l'accuracy moyenne la plus élevée des trois topologies (0,98118) mais log-loss 0,06914 contre 0,05291 pour le MLP. `HYBRID_HYBRID` atteint 0,05881 contre 0,05280. `FIXED_THEN_ADAPTIVE` est instable et sensiblement moins bon. Les comparateurs MLP ne sont pas de nouveaux entraînements redondants : ils sont liés par budget exact et seed au cache de comparaison commun, et figurent explicitement dans `twolevel_and_alternating_MLP_comparators.csv`.

## Correcteur résiduel OOF

Le bras adaptatif OOF utilise 5 folds : chaque ligne du train est prédite par un modèle de base qui ne l'a pas vue ; le niveau correcteur apprend les résidus sur ces logits OOF. Résultat validation : accuracy 0,97647, log-loss 0,05218, `P_total=1160`. Le MLP ge4x correspondant est 0,98588 / 0,05037, 4649 paramètres (4,0078×). Latence médiane batch 1 du système OOF ≈0,341 ms contre ≈0,01655 ms ; fit total ≈2,138 s contre ≈0,268 s. Le correcteur fixe est moins bon (log-loss 0,06856). La validation commune utilisée pour early stopping des folds est une limite de sélection/optimisation à mentionner ; aucune donnée test n'a été utilisée.

## Alternance A↔B

Les cinq familles initiales sont comparées ; la version stricte ajoute cinq graines, exige deux cycles complets A→B consécutifs sans nouvelle amélioration avant arrêt (cycles effectivement 2 à 5), et vérifie bitwise les poids et l'état Adam de la branche gelée. Avec `P_total=424`, le MLP ge4x est 1712 paramètres (4,0377×). La variante stricte atteint accuracy 0,97647/log-loss 0,06960 contre MLP 0,98118/0,05201 ; latence batch 1 ≈0,189 ms contre 0,01383 ms ; la taille déployée 23 001 octets est aussi supérieure aux 10 013 octets du MLP dans cet enregistrement. La mécanique d'alternance est validée, pas sa performance.
