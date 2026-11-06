# Limites et éléments non démontrés EX7

1. **Domaine** : Wisconsin historique uniquement ; aucune confirmation externe vierge. Généralisation non établie.
2. **Non-infériorité** : cinq graines sur un seul split ne suffisent pas à démontrer une non-infériorité populationnelle. La convention accuracy −0,5 pp / log-loss +5 % est descriptive. Emplica 2-fold RBF-Lite n'est pas stable par graine ; Orchestra 2-fold dépasse la marge de log-loss.
3. **Parallélisation** : expérience uniquement sur CPU. Processus OOF et threads inter-couches ralentissent le calcul sur cet environnement. Aucun essai CUDA/GPU.
4. **Latence 2-fold** : p50/p95/p99 présents, mais références et nouveaux candidats n'ont pas le même nombre de répétitions (200 contre 40) ; comparaison descriptive seulement. Un profil 5 graines strictement apparié à 100 répétitions a été tenté mais s'est interrompu avant sauvegarde et n'est pas utilisé.
5. **Ressources** : énergie, DRAM, mémoire d'activations et peak RSS isolé NON MESURÉS. La RSS EX6 signalait déjà une contamination par allocateur/cache et n'est pas fiable pour les comparaisons cross-model.
6. **Ablations Org** : hiérarchie récursive, cascade vs couches indépendantes, vectorisation, OOF et correcteurs ont été exécutés. Les six bras causaux inner-only, outer-only, local-only, global statique, sans modulation LR, et LR modulé avec poids uniformes sont terminés (30/30), mais leurs résultats ne démontrent pas une qualité comparable aux OOF EX6.
7. **Comparateurs MLP** : les MLP-ge4x EX6 sont des comparateurs historiques, et non de nouveaux fits dédiés à chaque architecture EX7. Les ratios de paramètres ont été vérifiés ; aucune revendication de non-infériorité MLP n'est faite pour tous les nouveaux bras.
8. **Compacité vs calcul** : P_total réduit n'implique ni moins de MACs, ni moins d'appels de noyaux, ni moins de temps ; la taille des paramètres est un indicateur distinct.
9. **2-fold** : temps pipeline reconstruit dans l'audit ressource. Le champ `candidate_training_total_seconds` du fichier résultat par graine n'intègre pas les initialisations mesurées séparément et ne doit pas être utilisé seul comme coût total.
10. **Temps de construction Org** : la modulation généralisée pour 5 probes/7 couches est une extension de la formule documentée pour N=4 ; les valeurs doivent être considérées comme une nouvelle variante expérimentale.
11. **Parallélisme des optimisateurs** : les probes locales dans Orchestra Org ont des optimiseurs séparés mais sont mises à jour séquentiellement par la boucle de référence ; la possibilité d'un vrai calcul parallèle optimisé sans duplication mémoire n'est pas validée.
12. **Données illisibles/qualité** : `0000.parquet` non décodé ; Screenplay doublonné ; JSONL final tronqué. Aucun de ces jeux n'a été utilisé.

13. **OOF 5-fold** : les 10 exécutions sont terminées (Emplica 5/5 ; Orchestra 5/5). Les temps globaux restent non comparables à cause des reprises sur checkpoints partiels ; la qualité log-loss est inférieure à la référence 3-fold pour les deux familles.
14. **Distillation** : 20/20 runs terminés ; la log-loss s'améliore contre le modèle sans correcteur, mais le pipeline total ne diminue pas matériellement car le coût OOF reste dominant.
