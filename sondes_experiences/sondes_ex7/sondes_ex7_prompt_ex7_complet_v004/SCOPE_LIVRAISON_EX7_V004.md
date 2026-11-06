# Périmètre de la livraison EX7 V004

Cette archive est volontairement limitée aux artefacts directement liés à `prompt_ex7.json` et à son exécution.

## Inclus

- Un seul snapshot de workspace : `sondes_ex7_v002__2026-10-31` (V002). Le snapshot V001 n'est pas inclus : l'audit de comparaison n'a trouvé aucun chemin de fichier propre à V001 ; V002 contient 50 chemins supplémentaires et les versions actualisées de quatre fichiers modifiés.
- Le prompt EX7 exact, ses configurations, pré-enregistrement, audits, journaux, codes, prédictions, métriques, résultats bruts et checkpoints.
- Toute la branche Emplica Orchestra Org récursive de bout en bout : code d'architecture, coordination interne/externe, entraînements racine, checkpoints, fits OOF (tous folds), correcteurs, sorties de couches, prédictions, ablations, variantes capacité/profondeur, benchmarks de vectorisation/parallélisme, MLP appariés, audits de parité et rapports.
- Les expériences non récursives EX7 (correcteurs allégés, distillation/base-only, comparaisons OOF 2/5 folds, compression structurelle, export/quantification, mesures de latence et de ressources) puisque elles appartiennent au protocole EX7.
- Les deux rapports consolidés les plus récents qui avaient été produits après le snapshot V002.
- Un minimum d'inputs de référence indispensable aux scripts EX7 : Wisconsin développement uniquement, références gelées Emplica/Orchestra OOF et les deux modules importés par le code EX7. Les autres sources EX6 sont exclues.

## Exclus

- Archives complètes `last_sources.zip`, EX4, EX5, EX6 et workspaces historiques.
- Le snapshot V001 redondant et les archives ZIP de livraisons antérieures : seul le workspace V002, qui couvre les chemins de V001 et ajoute les réconciliations, est inclus.
- Les copies de CSV/audits supplémentaires déjà identiques aux fichiers du workspace V002.
- Les contenus génériques de l'environnement non liés à EX7.

## Note de reproductibilité

Les références Emplica OOF / Orchestra OOF et les deux modules hérités sont des dépendances minimales explicitement conservées parce que les scripts EX7 les importent ou s'y comparent. Cela ne remplace pas et ne contient pas les archives complètes EX4–EX6. Les données Wisconsin restent un split historique de développement ; aucune confirmation externe vierge n'est revendiquée.

## Statut scientifique

La branche récursive originale est implémentée et ses campagnes prévues sont exécutées ; cela ne signifie pas que l'objectif global de vitesse/ressources sans perte de qualité est atteint. Les rapports distinguent les réussites partielles, résultats négatifs et mesures indisponibles.
