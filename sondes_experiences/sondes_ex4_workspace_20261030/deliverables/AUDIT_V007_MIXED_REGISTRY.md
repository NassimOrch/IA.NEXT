# Audit de la campagne v007 et séparation des registres

## Constat
Le registre brut v007 contient 95 lignes sonde alors que le test d'intégrité propre à la campagne initiale attend 14 candidates × 5 graines = 70 lignes. L'écart de 25 lignes correspond à cinq ablations micro-MIXA supplémentaires, chacune testée sur les cinq graines : adaptatif seul, fixe seul, mélange égal, gate global et gate conditionnel à l'entrée. Le script de test non filtré échoue donc à dessein sur ce registre mélangé (`Expected 14 candidates x 5 seeds, got 95`). Cela ne signifie pas que les 70 lignes initiales ont été altérées ; cela signifie que le test ancien ne doit pas être appliqué au registre étendu sans filtrage.

## Récupération contrôlée
`versions/sondes_ex4_v008__2026-10-30/scripts/audit_micro_mixa_recovery.py` récupère uniquement les 25 lignes des cinq bras micro-MIXA/add-on, leurs prédictions et historiques, et les comparateurs MLP correspondants. Le rapport `results/processed/ex4_micro_mixa_recovery_audit.json` conclut `PASS_FILTERED_MICRO_MIXA_RECOVERY` : 25 entraînements sonde, 30 MLP distincts, 50 comparaisons appariées, ratio ge4x minimal 4,01878×, métriques recalculées depuis les prédictions, test non consulté.

Le précédent rapport de récupération v007 filtre séparément les 70 lignes des 14 candidates initiales (`PASS_FILTERED_ORIGINAL_CANDIDATES`). Aucun agrégat issu des 95 lignes non filtrées n'est utilisé dans les conclusions. Les fichiers bruts restent conservés et l'audit v008 garde une copie des 25 lignes sélectionnées.

## Correction de métadonnées
Le registre brut micro-MIXA portait `adaptation_partition_used_for_controller=true` par héritage d'un champ générique. Le code `MicroHybrid` ne reçoit que `Xtr/ytr`, n'indexe pas la partition adaptation et optimise branches et gate sur train. La valeur brute n'a pas été réécrite ; v008 ajoute un champ d'audit `audit_verified_adaptation_partition_used=false` et explique la divergence. Cette correction d'interprétation doit accompagner toute réutilisation des lignes.

## Décision d'intégrité
- v007 brut : **registre mixte, non conforme au test de comptage historique**.
- v007 initial filtré : **PASS**, 70/70 runs sonde.
- micro-MIXA filtré en v008 : **PASS**, 25/25 runs sonde, ratios et prédictions.
- Aucun test Wisconsin n'a été ouvert dans ces deux audits.
