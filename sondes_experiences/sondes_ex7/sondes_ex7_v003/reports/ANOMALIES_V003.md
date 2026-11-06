# Journal des anomalies et décisions — V003

## A-001 — Consolidation JSON finale

- **Événement :** le premier passage de consolidation a échoué après les entraînements et les profils, lorsqu'une jointure d'étiquettes a créé un tableau vide et une valeur `NaN` interdite par `allow_nan=False`.
- **Impact :** aucun checkpoint, prédiction, métrique brute, profil de latence ou état d'entraînement n'a été supprimé. La consolidation agrégée n'a pas été finalisée au premier passage.
- **Correction :** le mapping des noms de bras a été corrigé et seule l'étape de consolidation a été relancée. Les modèles n'ont pas été réentraînés.
- **Trace :** `logs/run_v003.stderr.log`, `logs/run_v003.stdout.log`; le journal original est conservé.
- **Statut :** résolu ; données brutes conservées.

## A-002 — Comparaison de métriques float32

- **Événement :** le premier audit indépendant a relevé une différence de log-loss d'environ 1,27×10⁻⁸ pour une seed, due aux probabilités float32 dont la somme est à moins de 9×10⁻⁸ de 1.
- **Correction :** tolérance du seul audit de reproduction portée à 1×10⁻⁷, adaptée à la précision stockée ; les prédictions et métriques n'ont pas été modifiées.
- **Statut :** résolu ; audit final 91/91.

## A-003 — Temps d'entraînement partiel

- **Observation :** le chronomètre `fit_seconds` commence après création des modules, initialisation KMeans, tenseurs et optimiseurs.
- **Impact :** les résultats ne représentent pas le temps d'entraînement complet de bout en bout. Les temps d'initialisation sont non mesurés.
- **Décision :** rapporter les secondes comme temps de boucle d'entraînement/validation uniquement ; interdire toute revendication d'accélération end-to-end training.
- **Statut :** limite non résolue dans cette version.

## A-004 — Mémoire / énergie / opérations

- **Observation :** RSS est échantillonné dans un processus partagé et l'allocateur conserve des caches. Énergie absente. Le proxy MAC linéaire omet les opérations RBF non linéaires.
- **Décision :** mémoire comparative isolée, énergie et FLOP complets classés `NON MESURÉ`.
- **Statut :** non mesuré, pas un succès ni un échec.
