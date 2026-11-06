# Audit du protocole EX7 et décision de portée — V003

## Documents et entrées utilisés

- Prompt de projet EX7 JSON fourni dans V005, copié à l'identique (`inputs/prompt_ex7.json`).
- Pré-enregistrement V003 gelé avant les nouveaux entraînements (`configs/PRE_REGISTRATION_V003.json` et `.md`).
- Snapshot V002 de V005 : code historique `ex6_common.py`, `run_orchestra_org_recursive.py`, `run_orchestra_org_ablations.py`, résultats bruts, prédictions et checkpoints des bras de référence.
- NPZ `wisconsin_dev_only_v002.npz` : 341 train, 85 validation, 57 adaptation ; 30 caractéristiques. Le fichier n'a aucun tableau de test externe.
- Hashes et références : `EX6_REFERENCE_BUNDLE_MANIFEST.json`, `REFERENCE_INTEGRITY_V003.json`, `AUDIT_INDEPENDENT_V003.json`.

## Décision sur la portée

V003 est une expérience incrémentale focalisée sur la simplification de la coordination externe, et non une répétition de toute la campagne EX7. Les campagnes V001/V002 et les tests d'Org récursive/ablation sont conservés comme références historiques ; dix bras historiques sont réutilisés seulement après contrôle de hashes. La nouveauté V003 est la candidate `OuterCoord-Lite-7x1` et ses comparateurs MLP recalculés.

Les cinq graines pré-enregistrées sont 1501, 1607, 1717, 2029, 3037. CPU, un thread, float32. Le train et la validation sont identiques pour tous les modèles. La sélection du checkpoint est basée sur log-loss validation (`min_delta=0,0005`, patience 20). Le jeu d'adaptation est non utilisé. Le test externe n'est ni fourni dans le NPZ ni ouvert.

## Points de conformité et limites connues

- Les MLP matched et ge4x sont de vrais réseaux denses entraînés avec les mêmes partitions, les mêmes seeds racines et le même critère de sélection par validation. L'écart des initialisations MLP est déterministe et explicitement enregistré. Une vaste recherche hyperparamétrique MLP additionnelle n'a pas été faite ; le comparatif reste une expérience à réglages gelés, pas une preuve que le meilleur MLP possible a été trouvé.
- Les centres AdaptiveRBF sont initialisés sur les caractéristiques Xtr entières sans labels ; les losses supervisées de chaque probe utilisent uniquement son shard. Cette décision est mentionnée car la séparation des shards ne couvre pas l'initialisation non supervisée.
- Le gate ne reçoit que les logits détachés pour son objectif ; le propriétaire de chaque ligne est exclu du cross-fit gate. L'inférence dense utilise les sept branches.
- Le `fit_seconds` commence après l'initialisation du modèle/KMeans et du matériel d'optimisation ; init, prétraitement initial et sérialisation ne sont pas inclus. Les temps full end-to-end d'entraînement sont `NON MESURÉ`.
- La latence inference dispose de deux scopes : modèle seul sur tenseurs standardisés et raw-end-to-end incluant le scaler Torch. Les deux sont enregistrés sans les confondre.
- RSS échantillonné dans un processus séquentiel partagé, mémoire isolée comparable `NON MESURÉ`; énergie `NON MESURÉ`; FLOP/MAC complet `NON MESURÉ`.
- Wisconsin est historiquement exposé ; aucune validation externe confirmatoire n'est établie.

## Résultat de l'audit

L'audit indépendant V003 vérifie les entrées, hashes, 15 prédictions nouvelles, métriques recalculées, 10 références historiques, couverture des profils latence, sources Python et JSON : **91/91 contrôles passent**. Voir `AUDIT_INDEPENDENT_V003.md`.
