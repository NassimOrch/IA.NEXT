# EX12 P2 — Rapport de criblage architectural

## Statut et périmètre

Criblage exploratoire uniquement. 80/80 configurations logiques exécutées avec succès : 4 fonctions synthétiques × 2 graines × 10 variantes (7 sondes/graphes et 3 MLP appariés). Les modèles ont été ajustés sur train et sélectionnés sur validation. Aucun tableau test/holdout n’a été généré ou lu. Les 80 premières tentatives ayant échoué sur `yva` manquant sont conservées dans `P2_RUN_REGISTRY.jsonl`; six tentatives de reprise interrompues sont conservées dans le registre retry; 80 nouvelles tentatives logiques ont finalement réussi.

## Audit d’intégrité

- Runs logiques réussis : 80/80.
- Tentatives de reprise interrompues conservées : 6.
- Tentatives initiales échouées conservées : 80.
- Artefacts complets par run : 80/80.
- Problèmes de hash, métriques recalculées, splits ou paramètres : 0.
- Accès au test/holdout : NONE.
- Provenance runner : 25 runs associés à `p2_screen_v2.py`, 55 runs à `p2_screen_resume.py`; chaque run est aussi associé aux hashes de `ex12_models.py` et `generate_p2_data.py`.

Les métriques MAE, RMSE, NMAE et R² ont été recalculées depuis les prédictions sauvegardées. Le dénominateur NMAE est l’écart-type population de `y_train`, exclusivement.

## Résultats descriptifs agrégés

| Variante | Runs | NMAE moyen | NMAE médian | Temps entraînement médian (s) | Temps total médian (s) | P_train médian | P_total médian | Victoires MLP | ΔNMAE moyen | Ratio temps entraînement médian |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| C1 | 8 | 0.14085 | 0.07901 | 0.853 | 0.925 | 313 | 575 | 0/8 | 0.11141 | 1.38574 |
| C2 | 8 | 0.01983 | 0.01308 | 0.861 | 0.921 | 569 | 575 | 3/8 | -0.00962 | 1.37242 |
| C3 | 8 | 0.02827 | 0.01474 | 0.861 | 0.884 | 441 | 575 | 2/8 | -0.00117 | 1.40237 |
| C4 | 8 | 0.02386 | 0.01092 | 0.968 | 1.003 | 450 | 584 | 5/8 | -0.00568 | 1.61321 |
| G1 | 8 | 0.11797 | 0.02921 | 4.778 | 5.087 | 432 | 574 | 0/8 | 0.08731 | 5.26359 |
| G2 | 8 | 0.11863 | 0.03285 | 3.779 | 3.950 | 432 | 574 | 0/8 | 0.08797 | 4.72227 |
| M0_AFFINE | 8 | 0.02954 | 0.01229 | 0.592 | 0.611 | 583 | 589 | 0/0 | — | — |
| M0_CORE | 8 | 0.02945 | 0.01089 | 0.616 | 0.728 | 570 | 576 | 0/0 | — | — |
| M0_GRAPH | 8 | 0.03066 | 0.01089 | 0.647 | 0.933 | 570 | 576 | 0/0 | — | — |
| R0 | 8 | 0.02066 | 0.01257 | 0.783 | 0.869 | 569 | 575 | 4/8 | -0.00879 | 1.28089 |

## Comparaisons appariées

Les comparaisons sont appariées par fonction et graine, avec les MLP dont le budget total persistant est le plus proche. Les 56 écarts NMAE et ratios de temps sont dans `P2_PAIRED_COMPARISONS.csv`. Les marges P0 sont affichées à titre descriptif mais ne sont pas utilisées pour un verdict confirmatoire.

| Candidate | Victoires validation / 8 | ΔNMAE moyen vs MLP | Ratio médian temps d’entraînement | Ratio médian temps total |
|---|---:|---:|---:|---:|
| R0 | 4/8 | -0.00879 | 1.28 | 1.26 |
| C1 | 0/8 | 0.11141 | 1.39 | 1.31 |
| C2 | 3/8 | -0.00962 | 1.37 | 1.44 |
| C3 | 2/8 | -0.00117 | 1.40 | 1.28 |
| C4 | 5/8 | -0.00568 | 1.61 | 1.51 |
| G1 | 0/8 | 0.08731 | 5.26 | 4.39 |
| G2 | 0/8 | 0.08797 | 4.72 | 4.27 |

## Décision de sélection pour P3

R0, C2 et C4 sont retenus comme candidats exploratoires pour la généralisation multi-graines. C3 reste un contrôle structurel afin d’isoler l’effet de la correction affine. C1, G1 et G2 ne sont pas promus dans la branche principale P3 : ils ont 0/8 victoires appariées; G1/G2 présentent un coût d’entraînement élevé. C5 et C6 restent différés/non implémentés selon la décision P1.

Cette sélection est uniquement un filtre exploratoire fondé sur validation. Elle ne signifie pas que les candidats retenus surpassent les MLP. Aucun test statistique confirmatoire n’est justifié avec seulement deux graines par fonction.

## Conclusions et limites

P2 montre une forte dépendance à la tâche. Les centres fixes seuls (C1) échouent sur certaines fonctions; les graphes dynamiques (G1/G2) sont nettement plus coûteux et n’améliorent pas les validations observées. R0, C2 et C4 fournissent des signaux ponctuels, mais leurs temps d’entraînement médians dépassent ceux des MLP appariés dans l’ensemble de l’échantillon pilote. La priorité EX12 — être au moins aussi rapide et léger — n’est donc pas satisfaite par P2.

P2 ne teste ni extrapolation, ni frontière, ni OOD, ni classification, ni énergie, ni GPU. Ces aspects sont réservés aux phases ultérieures ou explicitement non mesurés. Les 2 graines de P2 ne sont pas comptées comme la campagne de 10 graines de P3.

## Artefacts

- `04_code/analyze_p2.py` — calcul complet de l’audit et des agrégats.
- `09_analysis/P2/P2_ALL_RUNS.csv` — 80 runs, métriques et ressources.
- `09_analysis/P2/P2_PAIRED_COMPARISONS.csv` — 56 comparaisons candidate/MLP.
- `09_analysis/P2/P2_VARIANT_SUMMARY.csv` — résumé par variante.
- `00_governance/P2_VALIDATION_SELECTION.json` — sélection pré-P3.
- `03_design/P2_VARIANT_REGISTRY_FINAL.json` — statut réel de toutes les variantes.
- `09_analysis/P2/P2_RUN_SCRIPT_PROVENANCE.json` — correspondance des 80 runs aux scripts exacts et hashes.
- `00_governance/P2_RUN_REGISTRY_RETRY1.jsonl` — registre append-only canonique de reprise.
- `00_governance/P2_RUN_REGISTRY.jsonl` — registre initial (80 échecs conservés).

Statut du rapport : exploratoire, train/validation seulement; aucune affirmation confirmatoire.
