# EX12 P6 — Rapport de falsification et de complémentarité

## Portée et règle d’interprétation

P6 teste si les centres ont des contributions utiles et des rôles reproductibles entre graines. La phase ne teste pas la qualité finale sur test : seuls les jeux train/validation P3 ont été utilisés. Les critères de spécialiste ont été figés avant les ablations dans `03_design/P6/P6_PREREGISTRATION.json`. Un centre n’est qualifié de spécialiste calculatoire reproductible dans un contexte donné que s’il satisfait simultanément les seuils de stabilité inter-graines et d’utilité prédictive corrigée par Holm. Aucun sens sémantique, causal ou universel n’est inféré.

## Exhaustivité observée

- Modèles candidats P3 : 320 ; analyses P6 réussies : 320 / 320.
- Unités modèle-centre : 10240 (= 320 × 32).
- Lignes LOO développées par modèle et régime : 34560.
- Permutations : 1600 (= 320 × 5), toutes conformes selon `torch.allclose(atol=rtol=1e-6)`.
- Paires inter-graines uniques : 1440; opérations de matching groupe : 2160; appariements centre-centre : 46080.
- Hypothèses de rôles : 1024 (= 8 tâches × 4 variantes × 32 centres).
- Accès au test et aux holdouts : NONE pour les runs P6.

## Résultat sur la spécialisation

- Stabilité des rôles : 549/1024 (53.6%).
- Utilité significative après correction de Holm : 9/1024 (0.88%).
- Spécialistes satisfaisant simultanément les deux familles de critères : 7/1024 (0.68%).
- Corrélation moyenne signée des profils appariés : 0.6747; médiane : 0.7539.

Le résultat ne soutient pas l’hypothèse d’une spécialisation générale des 32 centres. Il soutient une conclusion plus étroite : quelques centres dans la tâche `g5_sin_mul_plus_square`, principalement dans les variantes hybrides/adaptatives C2/C3/C4, satisfont les seuils pré-enregistrés. La majorité des centres ne satisfait pas simultanément la stabilité et l’utilité statistique.

### Résultats par variante

| Variante | Hypothèses | Stables | Utiles (Holm) | Spécialistes conjoints | Corrélation moyenne | Delta moyen de perte après refit |
|---|---:|---:|---:|---:|---:|---:|
| C2 | 256 | 153 | 3 | 3 | 0.7061 | 0.002949 |
| C3 | 256 | 120 | 4 | 2 | 0.6412 | 0.003072 |
| C4 | 256 | 96 | 2 | 2 | 0.5949 | 0.001476 |
| R0 | 256 | 180 | 0 | 0 | 0.7569 | 0.003150 |

### Sept centres satisfaisant les deux critères

| Tâche | Variante | Groupe | Graine ancre | Centre | Corrélation moyenne | Matches ≥0,50 / 9 | Accord de signe | Hausse moyenne de perte | p Holm |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| g5_sin_mul_plus_square | C2 | local | 1573268818 | 4 | 0.751 | 8/9 | 0.889 | 0.02059 | 0.0052554 |
| g5_sin_mul_plus_square | C2 | local | 1573268818 | 13 | 0.745 | 8/9 | 1.000 | 0.02332 | 0.048126 |
| g5_sin_mul_plus_square | C2 | local | 1573268818 | 20 | 0.767 | 9/9 | 1.000 | 0.02616 | 0.00013349 |
| g5_sin_mul_plus_square | C3 | local | 1573268818 | 25 | 0.843 | 9/9 | 1.000 | 0.02028 | 0.01718 |
| g5_sin_mul_plus_square | C3 | local | 1573268818 | 29 | 0.755 | 8/9 | 1.000 | 0.03405 | 0.021332 |
| g5_sin_mul_plus_square | C4 | local | 1573268818 | 25 | 0.772 | 8/9 | 1.000 | 0.01454 | 0.0033835 |
| g5_sin_mul_plus_square | C4 | local | 1573268818 | 29 | 0.736 | 8/9 | 1.000 | 0.02750 | 0.00011393 |

## Falsifications et diagnostics négatifs

- Les permutations de centres préservent la fonction lorsque les centres, largeurs et poids de sortie sont permutés ensemble au sein de chaque partition. Il s’agit d’un contrôle d’équivariance/représentation de la même fonction, pas d’une preuve de spécialisation.
- L’analyse de similarité des effets a trouvé 338 profils modèle avec au moins un effet de centre à variance nulle; au total 338 vecteurs d’effet de centre sont constants ou quasi constants selon le seuil pré-enregistré (1e-12).
- 16826 corrélations de Pearson hors diagonale indéfinies à cause d’une variance nulle ont été explicitement mises à zéro et signalées. Elles ne sont pas interprétées comme une absence réelle de relation.
- Les matrices de corrélation contiennent des contributions fortement corrélées et anticorrélées selon la tâche et la variante ; un poids de readout isolé ne prouve donc pas qu’un centre constitue un expert indépendant.
- Le rôle est mesuré sur un probe commun de validation sans labels pour le matching Hungarian. Les effets utiles, eux, sont évalués avec les métriques de validation prévues par le pré-enregistrement.
- Les rôles sont propres aux tâches/régimes mesurés et ne doivent pas être généralisés à d’autres domaines.

## Intégrité et écarts de provenance

- Vérification SHA-256 des données, checkpoints P3, prédictions, configurations, historiques, métriques, CSV LOO et profils : PASS (0 divergences).
- Un profil NPZ partiel non référencé est conservé : il provient de la tentative A01 interrompue pour la source `P3_tabular_nonlinear_binary_s934109236_R0_A01`; la tentative A02 est la réussite retenue. Aucun CSV LOO n’est orphelin.
- Le registre contient 321 événements STARTED, 320 résultats SUCCESS et 1 événement(s) INTERRUPTED. L’interruption a été enregistrée explicitement et n’est pas comptée comme une réussite.
- 123 succès historiques v1 n’enregistrent pas le hash du script dans leur enregistrement terminal. Le fichier `run_p6_ablation_v1.py` existe et son hash actuel est `9d7daec37b6e7808e0e24ee799ca428639908fbe6a6e7c4725010d2329280a30`, mais l’identité byte-for-byte au moment de lancement des runs v1 n’est pas prouvable avec les métadonnées historiques. Ce point est un déficit de liaison provenance, pas une preuve d’absence de script ni de sabotage.
- Les scripts v2/v3 et les scripts de réanalyse et de matching contiennent des hashes dans leurs registres ou rapports.

## Verdict P6

**La phase P6 est complète au sens opérationnel et documentaire** : le quota, les permutations, les analyses de similarité et les 1 024 tests de rôles ont été exécutés et audités. **L’hypothèse d’une spécialisation généralisée n’est pas confirmée.** Sept centres seulement satisfont simultanément les critères stricts, tous dans la tâche `g5_sin_mul_plus_square`. Les données ne justifient ni une revendication d’interprétabilité générale ni une architecture multi-experte universelle.

Le statut PASS de la porte P6 qualifie la complétude et l’intégrité des expériences prévues, non la réussite de l’hypothèse scientifique.
