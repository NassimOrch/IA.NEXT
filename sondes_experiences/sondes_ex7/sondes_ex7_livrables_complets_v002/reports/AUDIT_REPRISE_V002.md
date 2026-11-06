# Audit de reprise et de non-répétition — EX7 V002

## Pourquoi une V002

L'archive `sondes_ex7_livrables_complets_v001.zip` était lisible et son CRC ZIP était valide, mais elle avait été créée avant l'intégration de tous les artefacts présents dans le workspace. La comparaison de l'arborescence courante avec le ZIP V001 identifie **306 fichiers de workspace absents de V001** (148 JSON, 127 checkpoints `.pt`, 20 CSV, 5 scripts Python, 5 NPZ et 1 rapport Markdown). Il s'agissait d'une archive incomplète par rapport au workspace, pas d'une corruption des fichiers sources.

V002 copie le workspace complet au moment de la consolidation, intègre les résultats de comparaison supplémentaires, réconcilie les compteurs de la branche récursive, recalcule les manifestes et reconditionne une archive entièrement vérifiée.

## Travaux repris sans réentraînement

1. Réconciliation des agrégats existants et ajout des comparaisons MLP appariées (même graine) pour les 30 ablations, les 10 variantes de correcteur d'étage et les cinq modèles racine.
2. Réconciliation séparée des cinq entraînements racine et des quinze fits temporaires de folds OOF.
3. Intégration des tables appariées déjà calculées pour 60 variantes structurelles, 25 variantes capacité, 15 correcteurs OOF Org.
4. Contrôle du bras `centers_k4` : 5/5 graines, checkpoint et lignes par graine présents.
5. Contrôle complet de l'architecture Org récursive : source, checkpoints racine, folds, prédictions et correcteurs.
6. Revalidation des formats, données, scripts, checkpoints et hashes ; aucune campagne de modèle terminée n'a été relancée.

## Résultats de l'agrégation additionnelle

- Ablations Org : 30 lignes, six bras, cinq graines chacun.
- Correcteurs d'étages : 10 lignes, deux bras, cinq graines chacun ; temps pipeline reconstruit avec génération OOF + fit base + fit correcteur.
- Modèles racine Org : cinq lignes, cinq graines.
- Tous les ratios de paramètres appariés de ces comparaisons sont ≥4.

Les fichiers par graine et agrégés se trouvent sous `deliverables/` et `results/metrics/`, avec préfixes `EX7_ORCHESTRA_ORG_ABLATIONS_MLP_COMPARISONS_`, `EX7_ORCHESTRA_ORG_STAGE_OOF_MLP_COMPARISONS_`, et `EX7_ORCHESTRA_ORG_BASE_MLP_COMPARISONS_`.

## Bilan intégrité

L'audit de la lignée récursive et des variantes a zéro erreur et zéro avertissement. Le contrôle de lecture du workspace source v001 a chargé tous les JSON/CSV/NPY/NPZ/checkpoints et analysé les scripts Python. Les tableaux ont des colonnes rectangulaires et les arrays numériques sont finis. La V002 contient des manifestes SHA-256 et l'archive ZIP est vérifiée après construction.

**Aucun fichier source ni résultat brut historique n'a été effacé ou écrasé dans V001 ; V002 est un instantané additionnel.**
