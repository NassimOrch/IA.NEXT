# Audit de sources — EX9 v011

## Périmètre inspecté
L'archive uploadée `last_sources_3.zip` a été vérifiée par `unzip -t` et extraite par le shell système. ZIPs imbriqués recensés et extraits dans l'espace d'audit hors du workspace livré. L'intégrité CRC est valide pour les archives testées. Les SHA-256 des sources structurantes sont dans `source_provenance_manifest.json`.

## Prompts et règles communes
EX3 établit no-presumption, anti-manipulation, critères qualité/ressources et workspace/livrables. EX4 clarifie ratio 4x sur `P_total`, ressources end-to-end, dynamique RETRO, données exposées et limites historiques. EX5 renforce les audits d'optimiseur, OOF, ablations et architecture hiérarchique. EX6 précise strict OOF, comptage paramètres/buffers, checkpoints/optimizer state, ressources. EX7 ajoute coordination/architecture récursive, compute, validation externe et règles de livraison. EX8 applique ces règles à la PCA corrigée, aux ablations récursives et à B10/B11.

Le prompt EX6 de référence est sous le snapshot `sondes_ex6_v003_livrables/.../inputs/prompt_ex6.json`; le prompt EX7 intégral est `EX7_PROMPT7_COMPLETE_V005/00_PROMPT/prompt_ex7.json`. Le prompt EX8 se trouve dans le paquet EX8 v010. Leur SHA-256 est enregistré.

## B10/B11 : preuves récupérées
Le dossier B10 contient scripts exacts (`run_action_language_v010.py`, `v004_engine_v010.py`, `common_v010.py`), configuration pré-enregistrée, données Wisconsin development-only, 5 paires de runs, checkpoints, historiques, prédictions et résultats. Les manifestes SHA du sous-dossier B10 ont été contrôlés. Le test indépendant `test_v010_integrity.py` est PASS : 90 runs candidats, 160 MLP uniques, 60 runs SMS, 1179 JSON stricts, 155 JSONL stricts, 10 ZIP sources CRC PASS, recalcul log-loss concordant à ~1e-8 ou mieux. Cette preuve valide l'intégrité de l'artefact, pas la généralisation externe.

B10 log-loss par seed : 0.04507602, 0.03892050, 0.03475841, 0.04704858, 0.04114467 (mean 0.04138964). B11 : 0.04639599, 0.03918663, 0.04361378, 0.04824928, 0.04468064 (mean à recalculer par script). B11 bat aussi ses MLP appariés et >=4x sur 5/5 seeds Wisconsin. Les deux sont du développement historique.

B10 coût observé p50 batch1 ~0.332ms, B11 ~0.116ms (B10 2.85x plus lent) et paramètres P_total 884 vs 835 dans EX8. B10 direct advantage B10-B11 CI t and nested bootstrap include zero, exact sign test p=0.0625. Une différence 5/5 n'est donc pas une preuve confirmatoire.

## A0
A0 utilise PCA2 unique ajustée X_train, même base pour train/validation ; RBF global D4/K8 (dans EX8 réutilisé de V001, donc fit cost historique non inclus), OOF global 5 folds et six sondes locales D4/K8 sur PCA2 + global probas OOF. P_total 806, 56 unités centre RBF par exemple, mean LL à recalculer à partir des cinq lignes. EX8 SMS donne un signal négatif pour A0 vs MLP, mais SMS est historiquement exposé.

## Core neural theory
`th_sondes_core_test_0.tex` a une définition AdaptiveRBF, expériences CNG et CNC. L'audit a identifié : domain mismatch des noeuds ADD/DIV/LOG, extrapolation mélangée dans les cubes élargis, normalisation cible manquante, ambiguïté sur ablations probe removal, dépendance CNG->CNC non justifiée, unités indépendantes insuffisamment hiérarchisées. `th_sondes_core_test_1.tex` conserve le document de base et ajoute les corrections normatives EX9.

## Données de `sources_ng_adapt_0.zip`
L'archive contient théorie générale des empreintes, formalisme observation (archive imbriquée), des datasets `Screenplay_dataset.jsonl`, `batch_dataset.jsonl`, `0000.parquet`, SMS. Les deux JSONL ont des doublons/contenus répétitifs (17 contenus uniques estimés) et `batch_dataset.jsonl` contient des lignes invalides ; ce n'est pas un corpus confirmatoire adapté aux comparaisons binaires B10/MLP sans nettoyage indépendant et définition des labels. Le Parquet n'a pas pu être chargé faute de moteur PyArrow dans l'environnement hors-ligne ; inspection footer a trouvé colonnes `question`/`answer`, donc corpus QA/math, pas un benchmark direct de classification B10. SMS est exposé historiquement. Aucun de ces jeux n'est déclaré holdout externe vierge.

## Limites vérifiées
`sonde_adapt_global_research_final.zip` n'apparaît pas comme un fichier séparé dans l'archive livrée ; le paquet `sources_ng_adapt_0.zip` et ses théories/datasets y figurent. Le manifest EX8 v010 compte 11 872 entrées mais inclut des chemins sources/historiques exclus du paquet portable ; il ne faut pas interpréter les absences comme une corruption de fichiers inclus. Le test d'intégrité EX8 spécifique a été exécuté et a PASSé.

L'environnement actuel n'a pas de réseau DNS opérationnel et PyArrow est absent : pas d'installation ni de téléchargement de datasets. Aucun dataset réel neuf confirmé ne peut donc être promis dans cette exécution.

## Catalogue EX8 v010 — variants examinées

Les familles du dossier de résultats EX8 ont été rapprochées du registre `CONFORMITY_MATRIX_V010.csv`, des scripts d'exécution et des agrégats. Résumés de log-loss Wisconsin (moyennes telles que reportées dans le dossier, nombre de graines indiqué) :

| Famille | Variante | n | Log-loss | Lecture de l'expérience |
|---|---|---:|---:|---|
| A | A0 PCA2 corrigée | 5 | 0.043068 | piste locale prometteuse ; IC large, SMS défavorable |
| A | A1 RBF-lite PCA2 | 5 | 0.067596 | 16 au lieu de 56 évaluations RBF, qualité dégradée |
| A | A2 RBF-lite PCA4 | 5 | 0.083119 | dégradation plus forte |
| A | A3 RETRO-lite PCA2 | 5 | 0.062473 | maturation déclenchée 2/5 seulement |
| A | A4 RETRO-full PCA2 | 5 | 0.059165 | aucun déclenchement observé |
| B | B1 greedy/no-OOF | 5 | 0.081404 | signal de fuite/coordination non contrôlée ; non retenu |
| B | B2 joint/no-OOF | 5 | 0.096861 | mauvaise qualité, OOF requis |
| B | B3 COMPACT15_5L | 10 | 0.085554 | référence récursive complète de cette famille |
| B | B4 COMPACT15_3L | 5 | 0.069462 | ablation profondeur |
| B | B5 COMPACT15_K4 | 5 | 0.058617 | évaluation centres 120→60, latence p50 rapportée 0.72→0.62ms mais encore derrière MLP |
| B | B6 corrections de couches L2 / L4 / L2+4 | 5 chacune | ~0.0699 / 0.0687 / 0.0687 | ajout de corrections locales coûteuses |
| B | B7 variance weighting | 5 | 0.06182 | qualité en hausse partielle mais p50 ~1.61ms |
| B | B8 action codebook | 5 | 0.06191 | p50 ~1.72ms, coordination coûteuse |
| B | B9 RETRO outer | 5 | 0.07133 | alpha reste nul au meilleur checkpoint sur les cinq graines |
| B | B10 action language | 5 | 0.04138964 | gagne contre ses MLP appariés et ≥4× 5/5 Wisconsin ; exploration, coûts d'action à disséquer |
| B | B11 standard gate | 5 | 0.04442526 | gagne aussi contre ses MLP appariés et ≥4× 5/5 Wisconsin |

La numérotation des variantes ci-dessus est celle des registres EX8. Les familles de correcteurs B6 comprennent trois branches distinctes et ne sont pas ramenées à un seul run. La variante B8 (`action codebook`) et B10 (`action language`) ne sont pas le même mécanisme : B10 s'appuie sur marges/désaccords, memberships floues et table continue 9×5. B11 est le gate softmax standard sur le backbone commun. Les ablations B1/B2 no-OOF ne sont pas admissibles comme preuve d'un bénéfice de coordination supervisée et doivent rester visibles comme résultats négatifs méthodologiques.

## Résultats MLP EX8 et contrôles

B10 MLP apparié moyen 0.05472717 ; MLP ≥4× moyen 0.050803152. B11 MLP apparié moyen 0.054291276 ; MLP ≥4× moyen 0.052243412. Les comparaisons sont par graine appariée. Les cinq graines partagent le split Wisconsin ; il ne s'agit pas de cinq jeux de données indépendants.
