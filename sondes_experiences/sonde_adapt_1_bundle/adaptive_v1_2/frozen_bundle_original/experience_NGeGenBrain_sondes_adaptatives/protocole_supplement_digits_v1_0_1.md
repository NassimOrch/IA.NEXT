# Correctif administratif v1.0.1 — audit JSON du supplément digits

Le lancement initial du protocole supplémentaire v1.0 a exécuté les entraînements et évaluations, puis a échoué lors de la sérialisation du rapport d'audit : le comptage des classes avait des clés tuple qui ne sont pas valides en JSON. Les fichiers CSV de prédictions, résultats, composition et fidélité avaient déjà été écrits.

Ce correctif change exclusivement la représentation JSON du résumé des comptes de classes du registre d'audit, en utilisant des clés chaîne `split -> classe -> nombre`. Il ne change aucun générateur, split, seed, paramètre, appel d'entraînement, métrique ni prédiction. Avant la relance, les SHA-256 des CSV issus du premier passage ont été enregistrés dans `audit/digits_before_audit_fix_sha256/results.sha256`. Après la relance, le script compare les empreintes, qui doivent être identiques.
