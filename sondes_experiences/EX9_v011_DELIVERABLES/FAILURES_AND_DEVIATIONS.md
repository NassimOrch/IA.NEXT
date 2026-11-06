# Échecs, écarts et limites — EX9 v011

## Sources / données

- `sonde_adapt_global_research_final.zip` n'est pas présent en tant qu'archive séparée dans `last_sources_3.zip`; ne pas le déclarer inspecté comme archive autonome.
- Le moteur PyArrow est absent ; `0000.parquet` n'a pas pu être chargé complètement. Les métadonnées footer suggèrent un schéma question/réponse, mais il n'est pas utilisé.
- L'environnement n'a pas d'accès DNS opérationnel ; aucun dataset externe réel neuf n'a pu être récupéré/validé/licencié.
- SMS, Wisconsin et autres domaines précédemment exposés EX3–EX8 ne sont pas considérés comme holdouts vierges.

## Exécution Rev1 — invalidée avant test

Le prototype initial avait deux problèmes méthodologiques : arrêt des folds OOF A0 consultant les labels des folds tenus à l'écart ; MLP_GE4X dimensionné sous le seuil après comptage du prétraitement. Les artefacts Rev1 sont gardés sous `results/models/quarantine_first_pass/`, annotés invalides et exclus de toute statistique finale. Aucun holdout n'avait été ouvert.

## Exécution Rev2 — classification

- Le protocole Rev2 corrige l'OOF par entraînement à 100 époques fixes sans lire les labels held-out et règle le dimensionnement GE4X sur P_total complet.
- Une longue commande s'est interrompue après quatre graines terminées ; la cinquième a été reprise séparément. Les fichiers partiels et journaux sont conservés. Le jeu complet `xor8` comprend finalement 45 JSON + 45 checkpoints, cinq graines pour B10/B11/A0 et les deux MLP par candidate.
- Le domaine `xor8` est synthétique uniquement, sélection/validation ; il ne représente pas un dataset réel ou un test multi-domaines.
- L'audit log-loss indépendant passe avec tolérance numérique 1e-8.

## CNG/CNC

- Un pilote CNG `sin(x)` avec M=1 et M=2 (mean/linear) a été exécuté sur train/validation uniquement, une seed modèle et une génération train/validation.
- Six pilotes de spécialistes CNC ont été exécutés sur train/validation uniquement, un seed par opération. Les domaines ADD/DIV/LOG ont été rectifiés pour les entrées de graphes, mais la composition des graphes entiers C1/C2 n'a pas été exécutée.
- Non exécuté : les quatre fonctions CNG complètes, M=1/2/4/7, cinq seeds, MLP apparié/4×, ablations de retrait gelées et réentraînées ; CNC graphes C1/C2/C3, MLP direct, AdaptiveRBF direct, propagation d'erreur end-to-end, test scellé et statistiques multi-seeds.

## Ressources

- Le matériel est CPU seulement. Aucun GPU, énergie, MAC/FLOPs complet et mémoire RSS peak homogène.
- Latence mesurée 20 warmups/40 répétitions ; percentiles élevés incertains à ce nombre d'observations.
- Les essais complets demandés par le prompt dépassent le débit pratique de cette session CPU, donc aucune fausse prétention à l'exhaustivité n'est faite. Les variantes non exécutées sont explicitement indiquées.

## Compilation TeX

La première compilation de `th_sondes_core_test_1.tex` échouait car `\\RaggedRight` n'était pas fourni par les packages chargés. `ragged2e` a été ajouté et la compilation `pdflatex -halt-on-error` réussit ; journal conservé dans `logs/latex_core_test_1.log`.


## Holdout synthétique : ouverture avortée (ne pas relancer)

Après gel (`MODEL_LOCK.json`, 151 empreintes), `score_sealed_test.py` a écrit le marqueur `SEALED_TEST_OPENED.json`, puis a appelé le générateur `xor8` (labels créés en mémoire). Le premier chargement de checkpoint a échoué car PyTorch cherchait `__main__.MLP` ; les classes n'étaient pas liées dans le contexte `__main__` de l'évaluateur. Aucun fichier de prédiction ni score test n'a été écrit. Par règle anti-triche, le holdout est maintenant traité comme consommé/compromis et ne sera pas scoré par relance. L'incident complet est `SEALED_TEST_FAILURE.json`. Les métriques de validation gelées restent intactes.

## Lot supplémentaire d'ablations B10 (post-lock, validation seulement)

Sept variantes de table ont été implémentées sur les backbones B10 Rev2 déjà gelés, pour cinq graines, soit 35 runs supplémentaires. Elles sont exploratoires (`DEV_ABLATION_COMPLETE`) : elles réutilisent le split `xor8` train/validation déjà exposé, et leur arrêt de table observe la validation. Même si le prompt et la pré-inscription générale annonçaient cette famille d'ablations, le script/config exacts de ce lot n'ont pas eu de gel hashé séparé avant exécution ; elles ne constituent donc pas une cohorte confirmatoire indépendante.

Le premier passage de `src/audit_b10_ablations.py` a signalé 35 écarts de hash parce que l'auditeur comparait par erreur le hash de son propre fichier avec celui du script expérimental. Aucun modèle, résultat, checkpoint ou donnée n'était en cause. Cet échec d'outil est conservé dans `results/processed/B10_ABLATION_INTEGRITY_AUDIT_FIRST_ATTEMPT.json`. La comparaison a été corrigée pour référencer `b10_ablation_study.py`, puis l'audit complet a passé 35/35 runs, avec égalité exacte des prédictions reconstruites à la précision du fichier JSON.

Les variantes améliorent légèrement la log-loss de validation du B10 de base, mais restent très loin des MLP ; cet effet ne peut pas être interprété comme amélioration confirmée. Les rapports détaillent le coût et les limites.

## Audits supplémentaires finaux

- `src/audit_checkpoint_deserialization.py` : 45/45 checkpoints classification Rev2 lisibles, sans accès au test.
- `src/audit_core_pilot.py` : 9/9 checkpoints CNG/CNC rechargés ; prédictions et MAE/RMSE originales recalculées exactement à la précision enregistrée.
- `src/audit_b10_ablations.py` : 35/35 checkpoints/tableaux reconstruits ; prédictions et log-loss recalculées exactement.
- Le journal append-only a été complété après l'événement initial de gel pour consigner l'ouverture avortée du holdout, les audits de checkpoints et le lot d'ablations.

## Traçabilité de provenance étendue

`inputs/source_tree_inventory_addendum.json` ajoute des arbres SHA-256 pour les neuf répertoires source extraits et calcule le SHA-256 de l'archive `last_sources_3.zip`. Le fichier demandé `sonde_adapt_global_research_final.zip` reste absent en tant qu'entrée autonome ; aucun fichier ne lui a été substitué silencieusement.


## Reprise du 2 novembre 2026 — audits et extensions après interruption

- Aucun run Rev2 xor8, pilote CNG/CNC, ablation B10 ou holdout xor8 n'a été relancé. Les checkpoints des 45 runs principaux et les audits déjà PASS ont été vérifiés.
- Le lot des 35 ablations B10 a été conservé. Un audit des seuils a trouvé zéro égalité exacte avec les quantiles en train et validation sur les cinq seeds ; les deux implémentations de binning produisent donc les mêmes indices sur les données réellement utilisées.
- Deux domaines synthétiques pré-enregistrés restants ont été exécutés : 45 runs par domaine (B10/B11/A0 et MLP apparié/GE4X × cinq seeds), soit 90 runs. Tous les historiques MLP ont été sauvegardés dans cette cohorte.
- Audit validation multi-domaines : PASS 90/90, erreur max de prédiction = 0, erreur max de log-loss = 0. L'auditeur initial a d'abord échoué car il reconstruisait le scaler par une formule et avait une tolérance trop stricte ; il a été corrigé pour réutiliser exactement `StandardScaler.fit().transform()`. Aucun entraînement n'a été relancé.
- Un lock séparé de 295 hashes a été gelé et 90 checkpoints chargés avant d'appeler les générateurs test. Les tests synthétiques concentric2/rotated_moons2 ont été scorés une seule fois, 90 prédictions. L'audit post-score (depuis labels/probabilités sauvegardés seulement, sans générateur ni forward model) passe 90/90. Vérification finale du snapshot : 294/295 fichiers correspondent exactement ; une seule exception est le rapport explicatif `reports/PROMPT_EX9_AUDIT.md`, mis à jour post-gel. Tous les chemins de modèles/données/configurations/scripts expérimentaux restent identiques. Cette exception documentaire est détaillée dans `reports/PROMPT_EX9_AUDIT_LOCK_EXCEPTION.md` et le JSON d'audit.
- Résultats négatifs : B10/B11/A0 perdent 5/5 contre MLP apparié et GE4X sur les deux domaines synthétiques test. Aucun modèle n'a été modifié après test.
- Aucun jeu réel externe vierge n'a pu être récupéré ; les résultats sont synthétiques. FLOPs/MAC complets, RSS peak isolé et énergie restent non mesurés. Les graphes CNC C1/C2 et ablations avancées d'end-to-end ne sont pas exécutés.
