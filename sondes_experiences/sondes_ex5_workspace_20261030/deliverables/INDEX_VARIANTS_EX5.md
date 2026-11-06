# Catalogue exhaustif des variantes et artefacts EX5

Ce catalogue complète le prompt actif EX5 v1.1 et couvre les versions expérimentales v001 à v007.

## Familles et couverture

| Famille canonique | Versions | Contenu |
|---|---|---|
| `RETRO_AND_ADAM` | v001 | Calendriers alpha/beta, maturation, contrôles, couplages gamma/delta/gradient, optimiseurs et gel strict |
| `MIXA_GENERAL` | référence EX3 | Définition générale adaptatif + banque fixe + mélange appris |
| `MICRO_MIXA_PROPORTIONS` | v001–v006 | Proportions fixes/adaptatives, égal, gates global/entrée, géométries |
| `MICRO_MIXA_SHARED` | v005–v006 | Partage encodeur/centres, gates et comparaison de coûts |
| `MICRO_MIXA_PCA_Q` | v006 | Question-only PCA, fixe/adaptatif/hybride et ablations |
| `ALTERNATING_ERROR_CORRECTOR` | v001–v002 | Rôles A↔B, résidus, ordres, unités hétérogènes, cycles stricts |
| `TWO_LEVEL_QUESTION_ANSWER` | v001–v004 | Hybride/hybride, fixe→adaptatif, adaptatif→fixe et ablations X/Y |
| `TWO_LEVEL_OOF_RESIDUAL` | v001 | Correcteur de réponse avec prédictions train out-of-fold, tête fixe/adaptative |
| `EXTERNAL_TRANSFER` | v001–v003 | Wine/Digits, pré-enregistrement, gel, prédictions et statistiques |
| `DEPLOYMENT_PROFILE` | v007 | TorchScript, Numba, contrôle de parité et latence CPU |

## Nombres de registres

- 7 versions expérimentales distinctes, v001 à v007.
- 53 registres JSONL bruts.
- 338 couples `version × candidate_id × registre` avec identifiant explicite.
- 1 608 lignes de registres possèdent un identifiant de candidat ; les autres lignes brutes (historiques, journaux ou télémétrie) restent dans les fichiers JSONL source.
- Le détail ligne/fichier/candidate figure dans `catalogue_variantes_ex5.csv` et le détail de tous les registres dans `catalogue_registres_ex5.csv`.
- Le mappage par version des scripts, données, checkpoints, résultats bruts et rapports est dans `catalogue_artifacts_versions_ex5.json`.

## OOF : contenu et statut

L'OOF n'est pas un résumé isolé : il comprend le script source et ses dépendances, les 25 modèles de base (5 plis × 5 graines), les 25 checkpoints de reprise avec état optimiseur et leurs marqueurs, les cinq caches OOF, les dix checkpoints composites finaux (tête adaptative/fixe × cinq graines), dix reprises de tête avec état Adam, dix fichiers de métriques, dix fichiers de prédictions et vingt liens MLP matched/ge4x (dix modèles MLP physiques réutilisés par clé de capacité et graine).

Le manifeste dédié `oof_artifact_manifest_ex5.csv` recense ces artefacts et leurs hashes SHA-256. `oof_artifact_audit_ex5.json` confirme : 25/25 folds, 10/10 composites, 20/20 comparaisons, aucune référence manquante, prédictions identiques à la réinférence du composite (écart maximal 0), métriques recalculées (écart maximal 0), et interface `forward(self, x)` uniquement.

## Noms MIXA / MiXA

Consulter `NOMENCLATURE_EX5.md` et `nomenclature_registry_ex5.json`. `MIXA` (famille générale) et `micro-MIXA` (reconstruction compacte) sont distincts. `MiXA` et `micro-MiXA` sont des alias de casse seulement ; aucune implémentation autonome sous ces graphies n'a été trouvée dans les sources. Les fichiers historiques ne sont jamais renommés.

## Règle de lecture

Les fichiers sous `versions/*/results/raw/` et `results/models/` sont les sources d'autorité. Les CSV et rapports sont des agrégats ou des audits. Les doublons de registre, pointeurs remplacés, prototypes invalidés et variantes échouant la parité sont conservés et explicitement signalés ; ils ne sont pas retirés du workspace.
