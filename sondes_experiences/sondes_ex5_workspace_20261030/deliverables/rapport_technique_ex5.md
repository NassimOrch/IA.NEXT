# EX5 — Rapport technique consolidé

## Versions

| Version | Campagne | État |
|---|---|---|
| v001 | RETRO/factoriel, proportions, OOF et premières hiérarchies Q/A | Exécutée ; doublon RETRO audité |
| v002 | Adam/AdamW, gel/dégel et alternance A↔B | Exécutée ; contrôles stricts passés |
| v003 | Wine/Digits, gel pré-test et bootstrap apparié | Exécutée ; NI conjointe non démontrée |
| v004 | Ablations hiérarchiques Q/A | Exécutée ; ressources de cascade défavorables |
| v005 | Partage d'encodeur/centres micro-MIXA | Exécutée ; réduction de paramètres, qualité/latence insuffisantes |
| v006 | PCA question-only et micro-MIXA | Exécutée ; six candidats, doublons de registre audités |
| v007 | Profilage TorchScript/Numba du candidat Q-only | Exécutée sans réentraînement ; parité stricte vérifiée |

## Paramètres et comparateurs

Le compte complet `P_total` inclut les prétraitements, buffers, centres, gates et paramètres fixes nécessaires à l'inférence. L'audit global contient **437 lignes ge4x**, ratio minimum **4,000735×**, zéro ratio sous 4. Le mapping détaillé est `audit_ratios_mlp_ge4x_global.csv`. Les MLP sont mutualisés uniquement par budget total exact et graine ; les liens candidat/graine sont individualisés.

Les correcteurs OOF sont explicitement reliés aux caches MLP dans `oof_mlp_comparison_links.csv` : 20 liens (2 candidats × 5 graines × matched/ge4x), 10 MLP physiques réutilisés. Pour chaque OOF, `P_total=1160`, MLP ge4x `P_total=4649`, ratio `4,007759×`. Les comparateurs ont les mêmes cibles de validation par graine et hashes vérifiés.

## Calcul indépendant des métriques et intégrité

Le script `scripts_audit_global_ex5.py` examine les versions v001–v007. Dernier résultat : 1 850 JSON valides dans v001–v007, 53 registres JSONL/1 720 lignes valides, 1 313 références checkpoints sans échec, 1 162 pointeurs prédictions canoniques sans échec, 826 prédictions recalculées sans divergence, 437 ratios ge4x conformes. Les dix prédictions OOF ont été recalculées par `calc_metrics` avec un écart maximal de 0,0 à l'enregistrement. Les 25 exports v007 ont un SHA-256 conforme à `checksums/model_artifacts_sha256.csv`.

## Séparation des données

Wisconsin est historiquement exposé et sert au développement. Wine/Digits ont été gelés avant test avec hash de prompt, candidats, code et configuration ; les graines ne sont pas traitées comme sujets indépendants. Pour Q-only, l'encodeur n'utilise que X_train ; Y_train n'est cible de loss que dans les bras déclarés supervisés. Le forward d'inférence utilise X uniquement. Les résidus answer-side OOF viennent de plis où chaque ligne est prédite par un modèle qui ne l'a pas vue.

## Ressources et limites

Les MACs forward, temps d'entraînement, latences p50/p95, RSS et bytes de déploiement sont rapportés lorsque présents. Les MACs complets d'entraînement ne sont pas mesurés de manière instrumentée ; l'énergie et la VRAM ne sont pas mesurées ; RSS/checkpoint/états optimiseurs ne sont pas uniformes dans toutes les anciennes branches. Les campagnes principales montrent que la latence batch1 et le temps d'entraînement sont généralement supérieurs à ceux du MLP ge4x. Le profilage v007 confirme que le tracing conserve les logits mais ne réduit pas assez la latence ; les chemins optimisés qui échouent la tolérance de parité sont exclus.

## Tests

- v001 final integrity : overall pass ; 532 références de checkpoints sans échec, 495 références canoniques de prédiction sans échec dans ce validateur local, 36 anciens pointeurs superseded documentés, ratios et gels conformes.
- v001 Adam freeze semantics : exécuté ; sémantiques de gel et contrôles négatifs consignés.
- v002 alternance/Adam : PASS.
- v003 split test : PASS.
- v004 : 2 passed ; v005 : 1 passed ; v006 : 3 passed ; v007 : 3 passed.
- Tests workspace OOF : 4 passed (appariement MLP + audit de complétude OOF).
- Audit global : pass, zéro anomalie de parsing/hash/métrique/ratio.

L'ancien test v001 `test_ex5_integrity.py` et l'ancien test global EX4 v007 restent des contrôles historiques obsolètes ; les raisons et leurs références superseded sont documentées. Ils ne sont pas présentés comme réussis.
