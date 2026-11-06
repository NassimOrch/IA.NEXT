# Correction alternée et hiérarchie question/réponse

## Correction résiduelle A↔B (v002)

Sept configurations pré-enregistrées ont été exécutées sur cinq graines (35 entraînements de sondes), avec comparateurs MLP matched et ge4x. Les deux groupes sont présents dans le modèle complet ; le ratio ge4x porte sur les deux groupes, pas seulement l'actif. Les phases enregistrent rôle actif/correcteur, résidus, cycles et états d'optimiseur.

| Variante | Accuracy validation | Log-loss validation | P_total | MLP ge4x P_total |
|---|---:|---:|---:|---:|
| A→B résiduel, adaptatif/adaptatif | 97,41 % | 0,06883 | 424 | 1 712 |
| B→A résiduel | 96,47 % | 0,06692 | 424 | 1 712 |
| A→B sans terme résiduel | 97,65 % | 0,08444 | 424 | 1 712 |
| entraînement conjoint | 97,41 % | 0,07044 | 424 | 1 712 |

Les contrôles stricts de gel vérifient bitwise les paramètres et états Adam du sous-ensemble correcteur gelé. Le MLP ge4x moyen est autour de 0,05383 de log-loss et 0,97882 d'accuracy. La branche alternée réduit les MACs et bytes, mais elle augmente le temps d'entraînement et la latence d'inférence (environ 0,076–0,106 ms contre ≈0,018 ms MLP). Elle ne passe pas la règle rouge.

## Architecture à deux niveaux questions → réponses (v001/v004)

Les topologies testées comprennent hybride/hybride, fixe→adaptatif, adaptatif→fixe, Q-only adaptatif, Q-only fixe, hybride avec gate global, contrôle réponse neutre, réponse-side seule et entraînement supervisé conjoint. `forward(X)` ne reçoit que X ; `Y_train` est utilisé comme cible de loss uniquement pour les bras supervisés. L'encodeur Q-only strict n'accède pas aux labels.

Le contrôle Q-only hybride à gate global atteint sur Wisconsin validation `accuracy=97,88 %`, `log_loss=0,05219`, `P_total=566`; son MLP ge4x a `P_total=2 273`, `log_loss≈0,05261`. Il est proche sur validation, mais le pipeline complet de pré-entraînement coûte ≈8,36 s contre ≈0,33 s pour le MLP et la latence p50 ≈0,166 ms contre ≈0,0155 ms. La règle rouge échoue nettement.

Le mode fixe→adaptatif est instable (accuracy ≈85,4 %, log-loss ≈0,311). Adaptatif→fixe obtient une accuracy haute mais une log-loss encore dégradée et un entraînement très lent de la tête fixe. Le contrôle supervisé conjoint n'est pas un Q-only non supervisé : l'original brut contient une étiquette de métadonnée trop large, conservée, et un fichier de correction d'audit la requalifie correctement.

## Résidu OOF

Le correcteur adaptatif out-of-fold atteint `accuracy≈97,65 %`, `log_loss≈0,05218`, `P_total=1 160`; son MLP ge4x a environ `P_total=4 649`, log-loss≈0,05037. Les plis OOF empêchent chaque observation de contribuer à l'apprentissage du modèle de base qui produit sa prédiction d'entraînement. Le pipeline est compact en paramètres mais plus coûteux, et la qualité probabiliste reste derrière le MLP.

## Addendum — appariement OOF vérifié

L'appariement OOF a été reconstruit par graine et budget total exact. Le correcteur adaptatif et le correcteur fixe ont chacun cinq comparaisons `matched` et cinq `ge4x`. Les MLP sont dix modèles physiques partagés par les deux candidates parce que leur `P_total=1160` est identique et que les graines sont appariées ; aucun entraînement MLP supplémentaire n'a été réalisé. Les MLP matched ont 1 151 paramètres (ratio 0,99224×), ge4x 4 649 (4,007759×). Les métriques de toutes les prédictions OOF et MLP ont été recalculées ; targets de validation et hashes sont cohérents. Les détails sont dans `oof_mlp_comparison_links.csv`, `oof_validation_metrics_audit.csv` et `rapport_oof_mlp_appariement_ex5.md`.
