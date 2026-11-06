# Reproduction fidèle EX8 v010 — variantes B10, B11 et A0

## Périmètre et fidélité

Les scripts EX8 v010 ont été réutilisés. Les splits Wisconsin `wisconsin_dev_only_v002.npz`, le jeu SMS train/validation `sms_v010_train_validation_only.npz`, les graines `[1501, 1607, 1717, 2029, 3037]` et les hyperparamètres propres aux runners v010 sont conservés. Le runner A0 ne diffère que par son chemin racine : il accède aux checkpoints globaux historiques du bundle V009, qui sont les checkpoints attendus par le code EX8. La définition mathématique des modèles et les hyperparamètres ne sont pas modifiés. Les cinq backbones B10/B11 de la campagne v010 sont réutilisés comme dans la méthode historique ; les têtes de coordination et les évaluations sont reproduites.

Les six séries candidate/domaine reproduisent les métriques EX8 à une tolérance de `1e-12`. Les scripts `common_v010.py`, `v004_engine_v010.py`, `run_action_language_v010.py` et `run_sms_action_language_v010.py` sont byte-identiques aux sources EX8. `run_pca_v010.py` ne diffère que par la résolution du chemin vers les artefacts historiques V009 inclus. `run_sms_replication_v010.py` ne diffère que par les chemins des dépendances SMS, déplacées dans la capsule autonome EX10 ; l'audit confirme que les adaptations sont limitées à ces chemins, sans changement d'algorithme.

## Wisconsin — split de développement historique

| Seed | B10 | MLP B10 | GE4X B10 | B11 | MLP B11 | GE4X B11 | A0 | MLP A0 | GE4X A0 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1501 | 0.045076 | 0.053096 | 0.053883 | 0.046396 | 0.054935 | 0.050348 | 0.060174 | 0.054935 | 0.055044 |
| 1607 | 0.038921 | 0.054432 | 0.050224 | 0.039187 | 0.053316 | 0.052841 | 0.062761 | 0.053316 | 0.050219 |
| 1717 | 0.034758 | 0.052606 | 0.051364 | 0.043614 | 0.052171 | 0.049118 | 0.037964 | 0.052171 | 0.046170 |
| 2029 | 0.047049 | 0.055490 | 0.050497 | 0.048249 | 0.054411 | 0.055613 | 0.042374 | 0.054411 | 0.055376 |
| 3037 | 0.041145 | 0.058011 | 0.048047 | 0.044681 | 0.056623 | 0.053295 | 0.012068 | 0.056623 | 0.051747 |

## Résumé Wisconsin

| Variante | Candidate LL | MLP apparié | MLP GE4X | Wins apparié | Wins GE4X | P_total | Latence p50 b1 (ms) | Fit moyen (s) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| B10 | 0.041390 | 0.054727 | 0.050803 | 5/5 | 5/5 | 884 | 0.406 | 1.178 |
| B11 | 0.044425 | 0.054291 | 0.052243 | 5/5 | 5/5 | 835 | 0.133 | 0.967 |
| A0 | 0.043068 | 0.054291 | 0.051711 | 3/5 | 3/5 | 806 | 0.241 | 1.001 |

**Interprétation :** B10 et B11 battent leurs MLP appariés et leurs MLP GE4X sur 5/5 graines. A0 gagne 3/5, pas 5/5. Les graines sont des initialisations sur le même split, et non cinq datasets indépendants.

B10 possède la log-loss moyenne la plus basse (`0.041390` contre `0.044425` pour B11), mais sa latence p50 batch 1 moyenne est d’environ `0.406 ms` contre `0.133 ms` pour B11, soit environ `3.05×`. La qualité seule ne démontre donc pas que B10 est globalement meilleur que B11 en coût/rapidité.

## SMS — corpus réel secondaire, déjà historiquement exposé

| Seed | B10 | MLP B10 | GE4X B10 | B11 | MLP B11 | GE4X B11 | A0 | MLP A0 | GE4X A0 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1501 | 0.103979 | 0.074288 | 0.084250 | 0.106146 | 0.074288 | 0.074919 | 0.107900 | 0.073418 | 0.078287 |
| 1607 | 0.103055 | 0.078190 | 0.076582 | 0.108156 | 0.078190 | 0.082624 | 0.109445 | 0.070708 | 0.075547 |
| 1717 | 0.101752 | 0.074817 | 0.081009 | 0.103365 | 0.074817 | 0.082818 | 0.111876 | 0.075140 | 0.082685 |
| 2029 | 0.099701 | 0.074546 | 0.077649 | 0.105179 | 0.074546 | 0.088808 | 0.102404 | 0.071751 | 0.073264 |
| 3037 | 0.092516 | 0.068792 | 0.084838 | 0.094616 | 0.068792 | 0.086583 | 0.102477 | 0.072403 | 0.077141 |

## Résumé SMS

| Variante | Candidate LL | MLP apparié | MLP GE4X | Wins apparié | Wins GE4X | P_total | Latence p50 b1 (ms) | Fit moyen (s) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| B10 | 0.100201 | 0.074127 | 0.080866 | 0/5 | 0/5 | 1632 | 0.335 | 1.728 |
| B11 | 0.103492 | 0.074127 | 0.083151 | 0/5 | 0/5 | 1583 | 0.114 | 1.500 |
| A0 | 0.106820 | 0.072684 | 0.077385 | 0/5 | 0/5 | 1112 | 0.201 | 4.144 |

SMS est une réplication secondaire sur un corpus réel déjà exposé historiquement. Les trois sondes perdent 0/5 fois contre les MLP appariés et 0/5 contre les MLP GE4X. SMS ne constitue pas une confirmation vierge.

## Contrôles de provenance

- `results/processed/CLASSIFICATION_REPRODUCTION_AUDIT.json` : PASS.
- `results/processed/CLASSIFICATION_REPRODUCTION_PER_SEED.csv` : trente comparaisons candidate/MLP avec ratios de paramètres.
- `results/processed/CLASSIFICATION_REPRODUCTION_SUMMARY.csv` : agrégats par variante et par domaine.
- Les checkpoints, historiques et prédictions des candidats ont passé les contrôles SHA-256.
- Les MLP appariés et GE4X sont inclus comme résultats et modèles distincts.
- Aucune partition test n’a été lue dans cette reproduction.
- Les essais frais non conformes sont conservés en quarantaine sous `results/attempts/`, distincts des réplications exactes.

## Conclusion

La reprise EX10 reproduit les résultats Wisconsin sans les modifier : B10 et B11 conservent leurs gains sur le split historique ; A0 conserve un gain partiel avec variance importante. Les résultats négatifs SMS montrent que ces performances ne se généralisent pas automatiquement. La validation externe sur un dataset réellement vierge reste à effectuer.
