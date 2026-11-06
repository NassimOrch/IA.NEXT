# Rapport REPLICA-U — EX11

Snapshot de génération : 2026-11-03 12:28:14 UTC

## Statut des campagnes

- v003 : 65/65 blocs terminés, tous audités ; **exploratoire avec déviation** (modèles finaux sur `i_fit`, pas sur la totalité du train extérieur).
- v004 : 11/65 blocs dataset×seed présents dans les artefacts complets à ce snapshot ; statut `INCOMPLETE_QUOTA` tant que les 65 ne sont pas terminés. Processus runner : PID 11597 si toujours actif au moment de la consultation.
- v004 réentraîne les modèles finaux sur tout le train extérieur après sélection des durées à l’intérieur du train ; inclut backbone, C1 routeur seul, teacher, T0, students 64/32 et 32/16, MLP appariés et MLP GE4X.
- Les audits v004 recalculent les métriques depuis les logits NPZ, contrôlent les neuf checkpoints, la configuration, l’OOF owner map/logits et le refit complet.
- Aucun test tabulaire scellé n’a été ouvert. Tous les scores présentés ici sont validation uniquement.

## Log-loss moyenne v004 sur les blocs terminés

| Dataset | n graines | Backbone | Teacher | Student 64/32 | Student 32/16 | MLP matched 64/32 | MLP GE4X |
|---|---:|---:|---:|---:|---:|---:|---:|
| dataset_31_credit-g | 5 | 0.52306 | 0.55872 | 0.51119 | 0.51387 | 0.50785 | 0.50998 |
| dataset_44_spambase | 5 | 0.19504 | 0.19294 | 0.17418 | 0.17881 | 0.17918 | 0.18193 |
| dataset_50_tic-tac-toe | 1 | 0.06890 | 0.05469 | 0.07915 | 0.07173 | 0.05879 | 0.06272 |

Les moyennes ne doivent être comparées qu’avec les mêmes seeds et le même dataset. Spambase n’a pas encore cinq seeds au snapshot courant.

## Interprétation et limites

- Le teacher n’est pas automatiquement supérieur au backbone ; la distillation peut aider ou nuire selon le domaine.
- La performance du student doit être comparée au MLP apparié et au backbone, pas uniquement au teacher.
- Une log-loss seule ne suffit pas : accuracy, balanced accuracy, macro-F1, Brier et temps par étape restent reportés dans chaque JSON.
- Les timings de REPLICA sont end-to-end au niveau run, mais ceux mesurés sous concurrence CPU doivent être considérés comme potentiellement contendus ; le profil final isolé reste nécessaire.
- Les runs v003 sont conservés dans leur registre mais ne sont pas regroupés avec v004 dans les verdicts confirmatoires.

## Artefacts

- Registres : `logs/append_only/replica_u_campaign_v003.jsonl`, `replica_u_campaign_v004.jsonl`.
- Rapports par run : `results/replica_u/REPLICA_*_v003.json` et `*_v004.json`.
- OOF : `results/replica_u/*_oof_train.npz`.
- Prédictions : `results/predictions/REPLICA_*_validation.npz`.
- Checkpoints : `results/checkpoints/REPLICA_*`.
- Audit : `results/audits/replica_artifact_audit_v001.json`, `replica_artifact_audit_v002.json`.
