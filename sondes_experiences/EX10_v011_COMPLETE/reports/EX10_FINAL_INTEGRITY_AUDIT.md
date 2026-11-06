# EX10_v011 — audit final d’intégrité et d’exhaustivité

## Vérifications exécutées sans réentraînement ni réouverture des holdouts

- Tests invariants : **6/6 PASS** (`pytest -q`).
- Classification : **90/90** fichiers de résultats possèdent un checkpoint et des prédictions dont les SHA-256 sont valides ; **90/90** historiques sont vérifiés (30 intégrés au JSON de résultat, 60 stockés séparément). Les 100 fichiers modèle incluent les 90 checkpoints de résultats et 10 backbones partagés.
- Réplication EX8 v010 : **30 comparaisons** (B10/B11/A0 × Wisconsin/SMS × cinq graines), résultats/checkpoints/prédictions validés ; les MLP GE4X sont au moins quatre fois plus grands. Les copies originales des scripts sont préservées et les adaptations de chemins des deux runners concernés sont vérifiées comme telles.
- CNG/CNC pré-test : **550/550** runs, checkpoints, historiques et prédictions de validation audités ; la reconstruction des prédictions depuis les checkpoints a un écart maximal de **0**. Les 65 jeux train/validation/test sont enregistrés en splits séparés de 630/135/135.
- Lock pré-test : **3 037/3 037** empreintes ; 550 modèles et 195 fichiers de holdout/scénarios stress verrouillés avant le scoring.
- Scoring one-shot : marqueur `COMPLETE`, **1 695** enregistrements de prédictions/métriques. L’audit post-test recalcule les métriques depuis les prédictions persistées, sans décoder les fichiers sources de holdout : **1 695/1 695 PASS**, différence absolue maximale **0** ; **90/90** fichiers de diagnostics de noeuds contrôlés.
- Dépendances : le ZIP SMS passe le CRC, le fichier brut concorde avec le contenu de l’archive et les dépendances de prétraitement SMS ainsi que les quinze artefacts globaux V009 nécessaires à A0 passent leurs SHA-256.
- Profil ressources : **550/550** checkpoints correspondants, **2 200/2 200** profils de latence vérifiés (CPU, un thread, batch 1/16/64/256). Les statuts des temps d’entraînement sont conservés : 370 `RECORDED_NO_OVERLAP_DETECTED`, 180 `CONTENDED_OR_UNVERIFIED`. Ces 180 dernières mesures ne fondent aucune comparaison. Les MAC/RBF sont des estimations structurelles ; aucun FLOPs matériel ni aucune énergie n’est mesuré.
- Théorie : les sources TeX `th_sondes_core_test_0.tex` et `th_sondes_core_test_1.tex` et leurs PDFs compilés sont livrés. Les logs de compilation sont conservés.

## Périmètre de livraison

Le paquet contient le workspace EX10_v011 uniquement : toutes les données EX10, configurations, modèles, scripts effectivement utilisés, historiques, prédictions, résultats, rapports, journaux, dépendances minimales documentées et artefacts de quarantaine. Les anciens essais sont conservés séparément sous `attempts`/`quarantine`, sans être intégrés aux agrégats valides.

Les caches régénérables (`.pytest_cache`, `__pycache__`, `.pyc`, `.pyo`) ne sont pas livrés. Aucun dossier source global `last_sources_3.zip` ni workspace complet EX3–EX9 n’est copié. Les références minimales EX8/V009 présentes sous `inputs/` servent uniquement à prouver/rejouer la réplication historique et la dépendance A0 ; elles sont listées dans le manifeste.

## Limites expérimentales maintenues visibles

- Wisconsin est une réplication historique sur un split déjà exposé ; SMS est également historiquement exposé. Aucun des deux n’est qualifié de holdout vierge.
- CNG/CNC évaluent des tâches mathématiques synthétiques tirées des graphes de la théorie ; elles ne démontrent pas une généralisation sur données naturelles.
- Les temps d’entraînement affectés par contention restent identifiés et ne sont pas utilisés comme preuve comparative. Aucun résultat d’énergie n’est revendiqué.
- Le scorer one-shot ne doit pas être relancé ; le marqueur de holdout est `COMPLETE`.
