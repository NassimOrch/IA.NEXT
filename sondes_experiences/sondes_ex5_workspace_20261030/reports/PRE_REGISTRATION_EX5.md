# Pré-enregistrement EX5 v001 — protocole et addenda

- Date : 30 octobre 2026.
- Prompt actif : EX5 v1.1, copié sans modification dans `inputs/prompt_ex5.json`.
- SHA-256 : `88f67fc34bf34c5ca0817da42a057ed71dfb092cfb33720be5532da96bab3291`.
- Seeds modèles : 1501, 1607, 1717, 2029, 3037.
- Développement Wisconsin : partition historique EX4 v009, explicitement non confirmatoire car Wisconsin était déjà exposé dans EX2/EX4.
- Critère d'arrêt entraînement supervisé : log-loss de validation, patience 30 ; baisse du LR après 10/20 époques sans progrès ; aucun plafond d'époques.
- MLP : comparateur `matched` et `ge4x`, compte de paramètres total incluant prétraitement, buffers et état de déploiement ; ratio exact par seed.
- Métriques principales : accuracy et log-loss ; secondaires : macro-F1, balanced accuracy, ECE, Brier/ROC-AUC quand définies.
- Ressources : paramètres, MACs analytiques du forward, temps mural, latence batch 1/16/64, débit, RSS, taille de déploiement/checkpoint. Énergie et VRAM sont marquées indisponibles.
- Test externe : split test choisi par permutation des indices sans lecture de X/Y du test ; train/adaptation/validation stratifiés seulement dans les lignes non-test ; scaler train-only. Gel des modèles, code, prédictions validation et hashes avant ouverture de X_test ou Y_test.

## Addenda append-only

1. `addendum_qonly_convergence_001.json` : pour la reconstruction question-only, MSE de reconstruction sur X_train seulement, amélioration relative minimale `1e-5 × |best|`, patience 30, LR divisé après stale 10/20, sans plafond d'époques.
2. `addendum_mixa_gate_geometry_001.json` : balayage d5 géométries pour le gate conditionnel en gardant A3/F1.
3. `addendum_alternating_strict_cycles_001.json` : arrêt de l'alternance après deux cycles complets A→B consécutifs sans nouveau meilleur score validation ; gel bitwise poids et Adam.
4. `addendum_external_label_blind_split_001.json` : split externe avec indices test aléatoires non stratifiés, avant indexation des valeurs test.
5. `addendum_external_prediction_unique_002.json` : prédictions validation reconstruites depuis checkpoints, nommées dataset/gate/seed, et sidecars canoniques séparés ; aucun fichier brut historique n'est écrasé.

## Limite statistique pré-enregistrée constatée

Le fichier de campagne initial ne fixe pas de marges numériques de non-infériorité (`delta_accuracy`, `delta_log_loss`) avec justification domaine par domaine. Les rapports présentent donc moyennes, écarts-types et comparaisons appariées disponibles, mais ne revendiquent aucune démonstration formelle de non-infériorité. Les marges ne sont pas ajoutées rétroactivement après l'accès aux résultats.
