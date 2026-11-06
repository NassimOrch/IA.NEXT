# EX9 v011 — Ablations B10 (table seule)

## Périmètre et statut

35 exécutions ont été réalisées : 7 variantes × 5 graines (1501, 1607, 1717, 2029, 3037). Chaque exécution réutilise le backbone B10 Rev2 déjà entraîné et gelé ; seuls les paramètres de table/de factorisation sont réappris. Les seuls exemples consultés sont les 600 observations train et les 240 observations validation de `xor8` EX9. Aucun test ou holdout n’a été généré ou chargé.

**Statut obligatoire : `DEV_ABLATION_COMPLETE`, exploratoire et non confirmatoire.** La validation avait déjà servi à sélectionner les checkpoints B10. Ces ablations ont été lancées après le verrou principal et ne constituent donc pas une cohorte confirmatoire pré-enregistrée indépendamment. La famille des ablations (quantiles, retrait des signaux, hard/soft, cardinalité, factorisation et régularisation) figurait déjà dans `prompt_ex9.json` et `PRE_REGISTRATION_EX9.md`, mais les configurations et le script exacts de ce lot n’avaient pas leur propre hash gelé avant l’exécution.

## Résultats agrégés

| Variante | États | P_total | Log-loss moyenne (ET) | Δ moyen vs B10 original | Fit complet reconstruit (s) | p50 batch 1 E2E (ms) |
|---|---:|---:|---:|---:|---:|---:|
| CODEBOOK_2X2 | 4 | 375 | 0.546467 (0.018898) | -0.003514 | 0.845 | 0.3258 |
| FACTORIZED_3PLUS3 | 9 | 385 | 0.544697 (0.020119) | -0.005284 | 0.830 | 0.4573 |
| HARD_3X3 | 9 | 400 | 0.545809 (0.021114) | -0.004172 | 0.932 | 0.3954 |
| NO_DISAGREEMENT | 3 | 370 | 0.544668 (0.021249) | -0.005313 | 0.913 | 0.4431 |
| NO_MARGIN | 3 | 370 | 0.544885 (0.019465) | -0.005096 | 0.874 | 0.3515 |
| NO_REGULARIZER | 9 | 400 | 0.545455 (0.020478) | -0.004526 | 0.840 | 0.3945 |
| Q25_Q75 | 9 | 400 | 0.545382 (0.020060) | -0.004599 | 0.852 | 0.4268 |

Le B10 EX9 original a une log-loss validation moyenne de **0,549981**, `P_total=400`, fit end-to-end moyen **1,251 s**, latence batch 1 p50 **0,4076 ms**. Le B11 EX9 original est à **0,554089**, `P_total=351`, fit **0,712 s**, p50 **0,2326 ms**. Les MLP B10 associés sont à **0,314458** (apparié) et **0,300874** (≥4×).

Les 7 nouvelles variantes ont des log-loss moyennes comprises entre 0,544668 et 0,546467 : elles améliorent descriptivement le B10 de base sur cette validation déjà utilisée, mais restent nettement derrière les MLP. Cette petite amélioration ne permet pas de départager les variantes, car les mêmes labels de validation ont déterminé les checkpoints et l’arrêt anticipé. Aucun test statistique confirmatoire n’est rapporté.

## Lecture des compromis

- `NO_MARGIN` et `NO_DISAGREEMENT` réduisent le nombre de lignes de table de 9 à 3 et le `P_total` de 400 à 370. Le gain de taille est réel mais la latence moyenne reste supérieure au B11 et au MLP.
- `CODEBOOK_2X2` utilise quatre états (20 logits de table) et `P_total=375`. C’est la variante la plus compacte de ce lot, sans gain prédictif confirmatoire.
- `FACTORIZED_3PLUS3` réduit les paramètres de table de 45 à 30 (`P_total=385`) mais n’accélère pas l’inférence dans ce profil CPU ; il est même le plus lent de ce lot en batch 1.
- `HARD_3X3` et `Q25_Q75` ne donnent pas d’avantage stable évident. Le remplacement du flou par des memberships dures et le déplacement des quantiles n’ont pas démontré de généralisation.
- `NO_REGULARIZER` ne démontre pas d’avantage de coût ou de qualité par rapport au réglage original.

## Traçabilité et intégrité

- 35 JSON de résultats, 35 checkpoints de table, 35 configurations.
- Les checkpoints contiennent les tables et référencent le checkpoint B10 parent par chemin et SHA-256 ; les poids de backbone ne sont pas dupliqués.
- `src/audit_b10_ablations.py` reconstruit chaque modèle depuis son checkpoint parent + checkpoint de table, recalcule les 35 vecteurs de probabilités et la log-loss, recompte `P_total` et vérifie les hashes.
- Audit : **35/35 PASS**, erreur maximale entre prédictions reconstruites et enregistrées = 0 ; écart maximal de log-loss = 0.
- `VARIANT_REGISTRY_B10_ABLATIONS.csv` est le registre complémentaire append-only logique du lot. Le `VARIANT_REGISTRY.csv` principal et le `MODEL_LOCK.json` original n’ont pas été modifiés.

## Ce que ce lot ne démontre pas

Aucune variante ne bat les MLP sur la validation `xor8`. Aucune amélioration n’a été confirmée sur un jeu réel vierge. Aucune preuve énergétique, MAC/FLOPs complet, RSS peak ou généralisation externe n’est produite. Les ablations se limitent à la table de fusion ; elles ne testent pas la déduplication/partage du calcul RBF, la distillation vers un gate, le pruning, la vectorisation de kernels ou la compilation optimisée. B10 reste sensiblement plus lent que le B11 et les MLP dans ces mesures CPU.

## Artefacts

- Runs : `results/ablations/b10_table/`
- Configurations : `configs/xor8_B10_*_seed*.json`
- Registre : `VARIANT_REGISTRY_B10_ABLATIONS.csv`
- Agrégats : `results/processed/B10_ABLATION_AGGREGATES.csv` et `B10_ABLATION_SUMMARY.json`
- Audit : `results/processed/B10_ABLATION_INTEGRITY_AUDIT.json`
- Script exact : `src/b10_ablation_study.py`
- Auditeur : `src/audit_b10_ablations.py`
- Premier lancement de l’auditeur avec référence de hash erronée conservé dans `B10_ABLATION_INTEGRITY_AUDIT_FIRST_ATTEMPT.json`; l’auditeur corrigé a passé les 35 runs.
