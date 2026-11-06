# Rapport pré-test — cohortes synthétiques EX9 concentric2 / rotated_moons2

Date : 2026-11-02. Ce document précède volontairement l'ouverture des seeds test.

## Préflight attendu

- Deux domaines synthétiques pré-déclarés dans PRE_REGISTRATION_EX9_REV2 : `concentric2` et `rotated_moons2`.
- 600 lignes train + 240 validation par domaine ; aucune ligne test générée.
- Cinq seeds de modèle ; trois candidates (B10/B11/A0) ; deux MLP comparateurs par candidate.
- 45 runs complets par domaine, 90 au total ; 90 JSON + 90 checkpoints + 90 configurations.
- Les checkpoints ont des classes module-qualified `classification_models.*`, non `__main__.*`.
- Audit validation indépendant : PASS 90/90 ; erreur max prédiction 0 ; écart max log-loss 0 ; hashes train/validation cohérents ; MLP_GE4X ≥4.0 à chaque run.

## Résultats de développement visibles avant le test

`reports/MULTI_DOMAIN_SYNTH_DEV_REPORT.md` contient les agrégats et les comparaisons. Les trois candidates perdent sur la log-loss validation face à leurs MLP dans les deux domaines, sans exception sur les cinq seeds de modèle. Les candidates sont aussi nettement plus lentes en latence batch 1 CPU. Tous les résultats sont conservés ; aucune candidate n'est éliminée après lecture des scores.

## Verrou

Le fichier `MODEL_LOCK_MULTI_DOMAIN.json` contient les SHA-256 de chaque JSON/checkpoint/config, des données train/validation, des manifestes, du prompt, du pré-enregistrement, du driver, de l'auditeur et de l'évaluateur one-shot. Le préflight de désérialisation doit charger 90/90 checkpoints avant toute génération de données test.

Les tests générés avec les seeds 61301 et 62301 seront une confirmation **synthétique uniquement**. Le domaine `xor8` demeure définitivement compromis/non scoré après son échec d'ouverture antérieur. Aucun de ces résultats n'est une confirmation sur données réelles externes.
