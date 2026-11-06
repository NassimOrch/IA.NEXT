# Appariement OOF — MLP matched/ge4x et audit indépendant

Les deux modèles OOF (correcteur adaptatif et correcteur fixe) ont été appariés aux MLP du cache existant `mixa_proportion_mlp_runs.jsonl`, par `P_total_probe=1160` et graine exacte. Aucun MLP n’a été réentraîné. L’appariement est désormais explicite dans `oof_mlp_comparison_links.csv` (20 liens candidate × seed × comparaison).

| Candidate | P sonde | P MLP | Ratio | Acc sonde | LL sonde | Acc MLP ge4x | LL MLP ge4x | Temps pipeline sonde | Latence sonde batch1 | Temps MLP ge4x | Latence MLP ge4x |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| OOF adaptive | 1160 | 4649 | 4.00776× | 97.6471% | 0.05218 | 98.5882% | 0.05037 | 2.138 s | 0.3407 ms | 0.268 s | 0.0166 ms |
| OOF fixed | 1160 | 4649 | 4.00776× | 97.6471% | 0.06856 | 98.5882% | 0.05037 | 1.992 s | 0.3670 ms | 0.268 s | 0.0166 ms |

## Lecture

- Les deux candidats utilisent 1 160 paramètres totaux (ensemble des cinq modèles de base, correcteur et scaler inclus). Les MLP `ge4x` ont 4 649 paramètres, soit 4,00776×. Les MLP `matched` ont 1 151 paramètres (ratio 0,99224×), ce qui est un appariement pratique à ±0,8 %, et non une égalité parfaite.
- Le correcteur adaptatif OOF obtient une log-loss moyenne de validation de 0,05218 ; le MLP ge4x obtient 0,05037. Le correcteur fixe obtient 0,06856. L’accuracy moyenne des deux candidats OOF est 97,65 %, contre 98,59 % pour le MLP ge4x.
- Le coût de cinq modèles de base est inclus dans le temps de pipeline et le déploiement OOF. Le fit adaptatif OOF prend en moyenne 2,138 s contre 0,268 s pour le MLP ge4x ; la latence batch 1 moyenne est 0,341 ms contre 0,0166 ms. La candidate ne satisfait donc pas la règle rouge de ressources.
- Les résidus d’entraînement sont calculés à partir des prédictions out-of-fold (chaque ligne entraînement est prédite par un modèle qui ne l’a pas vue) ; les labels validation/test ne construisent pas les résidus. Les traces indiquent `test_partition_accessed=false`.
- Les métriques ont été recalculées depuis les prédictions brutes avec `calc_metrics` du module commun ; tous les écarts max sont sous `1e-7`. Les hashes de cinq checkpoints et cinq fichiers de prédictions pour chaque candidate correspondent.
- Le MLP du cache est partagé entre les deux candidates OOF car leur `P_total` et leur split/graine sont identiques. Cette réutilisation est explicitement documentée et ne compte pas comme dix MLP fraîchement entraînés.
