# Supplément RBF-R1 — boucle d'empreinte causale pour la reconstruction

**Gel du protocole avant exécution.** Ce supplément ne remplace ni ne recalcule les 148 lignes historiques de `results/reconstruction/`. Il vérifie une propriété absente de leur boucle initiale : ici l'empreinte calculée avant la mise à jour décide effectivement si cette mise à jour est autorisée.

## Question

Sur la tâche synthétique `x -> f_theta(x) -> g_psi(f_theta(x)) ≈ x`, est-ce qu'une règle de quarantaine déclenchée par l'erreur pré-update aide à préserver les performances de reconstruction, par rapport à une mise à jour après chaque observation et à un contrôle de suppression aléatoire ? La campagne est exploratoire, pas confirmatoire.

## Modèles et données

- Les deux architectures déjà présentes sont reprises : `RBF2_free_global` et `RBF2_free_tanh_global`.
- Les mêmes graines de modèle de la tâche sont utilisées : 101, 202 et 303.
- Les partitions sont celles de `run_reconstruction_experiment.py`: 1 440 train, 360 validation, 240 adaptation, 360 test. Le scaler est ajusté sur train seulement.
- Chaque modèle est ajusté sur la seule partition train; la validation sert seulement à fixer le seuil q90. Les données de test ne sont jamais consultées par la fonction d'update.

## Ordre causal et empreinte

À chaque observation d'adaptation : (i) calculer `yhat_before`; (ii) acquérir la mesure réelle `x_obs`; (iii) calculer `r = ||x_obs - yhat_before||_2`, disponibilité, provenance, hash de l'entrée et surprise quadratique; (iv) produire la décision; (v) mettre à jour les paramètres si la décision l'autorise; (vi) passer à l'observation indépendante suivante. Aucun label ou signal d'évaluation de test n'est disponible dans cette boucle.

Le seuil `tau` est le quantile empirique 0,90 des résidus L2 sur la validation propre, évaluée avant adaptation. La politique empreinte saute l'update si `r > tau`. Le contrôle aléatoire saute 10 % des mises à jour selon un générateur distinct. Le contrôle `no_update` ne met à jour aucun paramètre. Le contrôle `unconditional_update` met à jour à chaque observation disponible.

## Conditions

1. `clean` : mesure d'adaptation originale.
2. `missing_30pct` : 30 % des observations sont masquées; aucune cible n'est imputée.
3. `measurement_noise_sigma_0_10` : bruit gaussien indépendant d'écart-type 0,10 ajouté à l'observation mesurée avant prédiction et utilisation; la cible en ligne est cette mesure bruitée, et non la donnée propre cachée.
4. `shift_x0_plus_0_75` : translation de +0,75 dans la première coordonnée normalisée; la cible d'adaptation est l'entrée décalée effectivement observée.

Les tests source et décalé/bruité sont des évaluations finales sur des points indépendants de l'adaptation. Les tests bruités évaluent l'auto-reconstruction de la mesure bruitée, pas la débruitage vers une cible propre.

## Critères et sorties

RMSE, MAE, R², erreur de vecteur p90/max, nombre d'updates, événements empreinte, temps d'adaptation, métriques par seed et résumés descriptifs. Trois graines sont insuffisantes pour une revendication confirmatoire. Conserver les résultats négatifs et l'intégralité des journaux.
