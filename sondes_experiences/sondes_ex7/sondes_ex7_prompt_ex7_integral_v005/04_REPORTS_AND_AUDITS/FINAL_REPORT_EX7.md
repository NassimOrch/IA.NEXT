# Rapport final EX7 — compacité vers l'efficience

## Conclusion exécutive

La campagne confirme que l'étape la plus coûteuse de la lignée n'est pas forcément l'ajustement du correcteur : la génération des logits OOF représente une part importante du coût total. Remplacer trois folds par deux folds imbriqués réduit le temps de génération OOF d'environ 54–55 % et le temps total reconstruit d'environ 42 % pour les variantes RBF-Lite à une probe. **C'est le signal positif le plus important d'EX7.**

Cependant, cette réduction ne démontre pas une non-infériorité robuste : Emplica 2-fold est proche en moyenne, mais dépasse la marge descriptive pour certaines graines ; Orchestra 2-fold dépasse la marge de log-loss en moyenne. Et l'inférence ne s'accélère pas de façon démontrée : les p50 sont souvent plus lents et les p99 restent instables. Les modèles sont toujours environ 6–7 s à entraîner dans le pipeline 2-fold, contre environ 0,26 s pour les MLP-ge4x historiques : Emplica RBF-Lite reste environ 25,7× plus lent à entraîner que son MLP-ge4x, et Orchestra environ 23,7×. Les latences p50 agrégées du 2-fold sont également plus lentes aux quatre tailles de batch observées (+1,9 % à +19,4 % selon la famille et le batch). Il s'agit donc d'un gain contre l'ancien pipeline OOF, pas contre le MLP en temps, et pas d'un gain d'inférence.

L'architecture originale **Emplica Orchestra Org** a été implémentée, exécutée et cross-fittée. Elle réalise bien une adaptation globale à deux niveaux (probes→couche, couches→ensemble), avec sorties détachées, optimisateurs et mises à jour séparées, modulation de taux locale et mise à jour périodique. Mais les résultats de validation OOF ne rejoignent pas la qualité des références Emplica/Orchestra OOF et coûtent davantage à produire. L'architecture est une réalisation de l'idée, pas une réussite prédictive/efficience à ce stade.

## Expériences complémentaires terminées après le premier bilan

- Les 6 ablations causales Org (inner-only, outer-only, local-only, global statique, sans modulation du taux, gates uniformes avec modulation) sont exécutées sur 5 graines. `outer_coord_only` obtient 98,59 % d'accuracy, mais 0,06013 de log-loss ; il reste inférieur en log-loss aux références OOF EX6.
- La distillation du RBF-Lite est exécutée sur 20/20 cas. Elle améliore la log-loss contre la base sans correcteur (Emplica 0,03983 ; Orchestra 0,04701), mais ne réduit pas le coût du pipeline (environ 10,9 s et 9,8 s respectivement).
- L'OOF 5-fold est terminé (10/10 : 5 graines Emplica et 5 Orchestra). Il ne préserve pas la qualité de référence (Emplica RBF-Lite 0,04512 vs 0,03637 ; Orchestra RBF-Lite 0,05964 vs 0,03982). Les temps ont été exclus de toute comparaison normalisée en raison des reprises sur checkpoints.

## Décisions

1. **Ne pas remplacer les références EX6** par les correcteurs légers 3-fold : ils perdent de la log-loss.
2. **Conserver Emplica 2-fold RBF-Lite** comme hypothèse de développement à retester : baisse du pipeline d'environ 42,9 %, log-loss moyenne à +4,5 %, mais une graine présente une dégradation importante et la non-infériorité par graine est refusée.
3. **Ne pas retenir Orchestra 2-fold comme remplaçant** : log-loss moyenne à +9,1 % par rapport à la référence, au-delà de la convention +5 %.
4. **Ne pas annoncer de parallélisation gagnante** sur CPU : processus OOF et threads inter-couches sont plus lents ; vectorisation a un effet dépendant du batch.
5. **Conserver Orchestra Org comme branche expérimentale**, mais pas comme candidate efficiente/qualité équivalente ; les ablations causales ont été exécutées, mais aucune configuration ne rejoint la qualité OOF EX6 ; des ablations complémentaires resteront nécessaires pour rechercher une combinaison compétitive.
6. **Ne pas revendiquer une économie de mémoire/énergie** : énergie, mémoire d'activations et peak RSS isolé ne sont pas mesurés de manière fiable.
7. **Ne pas revendiquer de confirmation externe** : aucun dataset du lot de sources n'est vierge et validé pour ce rôle.

## Verdict

`INCOMPLET — DÉVELOPPEMENT UNIQUEMENT — VALIDATION EXTERNE NON ÉTABLIE`.

Le but EX7 — convertir la compacité en gain global de temps et de consommation sans perte de qualité — n'est **pas atteint**. Un axe concret mérite une nouvelle expérience indépendante : réduire le coût de cross-fitting (2-fold) et améliorer le correcteur Emplica autour de RBF-Lite, en repréenregistrant les marges et en testant sur un nouveau domaine jamais vu. Il faut ensuite optimiser le noyau d'inférence et mesurer la mémoire/énergie avant de parler de gain global.

Les résultats détaillés, scripts, checkpoints, prédictions, incidents et limites se trouvent dans les dossiers `results/`, `src/`, `logs/` et `reports/` de cette version.
