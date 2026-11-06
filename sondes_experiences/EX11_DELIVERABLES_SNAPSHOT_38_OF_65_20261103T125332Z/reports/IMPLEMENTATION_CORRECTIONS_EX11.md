# EX11 — registre des corrections d'implémentation et déviations

Date de consolidation : 2026-11-03 (UTC). Ce document complète le pré-enregistrement ; il ne réécrit aucun résultat antérieur.

## 1. Principe de versionnement

Chaque run est conservé avec son identifiant, son code, sa configuration et ses artefacts. Une version corrigée produit un nouvel identifiant et un nouveau registre. Les fichiers historiques ne sont ni écrasés ni supprimés. Les résultats d'une version non conforme restent accessibles mais ne sont pas agrégés dans les résultats confirmatoires.

## 2. Branche REPLICA-U

### v003 — exploratoire avec déviation

L'audit du code v003 a trouvé que les modèles finaux étaient entraînés sur le sous-ensemble `i_fit` utilisé pour la sélection interne, au lieu d'être réinitialisés puis réentraînés sur toutes les lignes du train extérieur. Le script ne fournissait pas non plus l'ensemble complet des comparateurs/ablations demandés dans le pré-enregistrement : C1 routeur seul avec spécialistes et backbone gelés, T0 sans perte auxiliaire, MLP apparié au student 32/16. Le routage top-k v003 calculait les sept résidus avant d'appliquer le masque top-k ; il ne réduisait donc pas le coût des spécialistes.

Les exécutions v003 sont des exécutions réelles et leurs fichiers sont conservés. Elles sont classées `EXPLORATORY_PROTOCOL_DEVIATION`, et ne fondent pas le verdict confirmatoire REPLICA-U.

### v004 — chemin corrigé, pas encore confirmé par campagne complète

Le code v004 réalise les cinq folds OOF, sélectionne les durées sur un split intérieur, réinitialise et réentraîne les modèles finaux sur tout le train extérieur, et inclut C1, T0, les deux students, leurs MLP appariés et le MLP GE4X. La sélection des durées utilise désormais un préprocesseur ajusté exclusivement sur le sous-ensemble intérieur `i_fit`; le préprocesseur final est réajusté ensuite sur l'ensemble du train extérieur. Cette séparation évite que les statistiques de validation intérieure influencent le prétraitement utilisé pour sélectionner les durées.

Un test unitaire vérifie que le scaler ne voit que `i_fit`, et un autre vérifie que C1 ne met à jour que le routeur, que les poids gelés restent inchangés et que le nombre de lignes d'entraînement est enregistré. Le script est compilé ; aucune campagne v004 complète n'est déclarée tant que les runs et leurs audits ne sont pas produits.

### Ablations de routage

Les ablations top-1/top-2/post-hoc sur modèles v003 sont des diagnostics de qualité seulement. Le code appelle tous les spécialistes avant la sélection top-k ; aucun gain de latence n'est revendiqué. Une vraie économie de calcul exige une architecture de routage précoce et doit être évaluée comme une nouvelle variante.

## 3. Branche D — efficacité d'implémentation

### D3Q v001 — exploratoire

La campagne historique D3Q v001 utilise l'initialisation aléatoire des centres et son MLP GE4X n'est pas systématiquement au moins quatre fois plus grand que D1/D2. Les résultats v001 demeurent archivés comme exploratoires. Les temps de ses exécutions longues sont en outre susceptibles d'être perturbés par la concurrence CPU avec REPLICA-U.

### D1/D2 microbenchmark

Le microbenchmark initial a été exécuté sur CPU mono-thread avant les campagnes lourdes. Il compare les mêmes poids/fonctions, avec 30 warmups et 200 répétitions par batch. Le contrôle étendu vérifie sorties, gradients d'entrée et gradients paramètres sur dix seeds et quatre batches (40 cas), tolérance absolue et relative 1e-6. Résultat : 40/40 cas passent. Cela démontre l'équivalence numérique dans les conditions testées, non une supériorité universelle de vitesse sur tout matériel.

La RSS enregistrée au niveau processus est une mesure de high-water mark partagée et non une mesure isolée de la mémoire de chaque variante. Aucun compteur d'énergie exploitable (RAPL/powercap ou mesure externe fiable) n'est disponible dans l'environnement ; aucune conclusion énergétique ne doit être tirée.

### D3Q v004 — confirmatoire préparé

Le script v004 initialise les centres de D1/D3 par KMeans sur les seules données d'entraînement, copie les poids exacts de D1 vers D2 et dimensionne le MLP de référence à `>=4x` le nombre de paramètres de la plus grande des trois variantes D1/D2/D3. Il utilise des splits synthétiques train/validation séparés, les mêmes seeds et le même ordre de mini-batches pour les variantes appariées. Le script compile, mais aucun résultat v004 ne sera déclaré avant exécution, persistance et réconciliation des checkpoints/prédictions.

## 4. Branche CNG

Les runs CNG v001 utilisent des centres initiaux aléatoires et ne sont pas confirmatoires. Le script CNG v003 préparé utilise KMeans train-only et le même ordre de mini-batches pour les variantes comparées d'une même tâche/graine. Le MLP GE4X est dimensionné par rapport à A3-M7, la plus grande sonde de la grille. Le registre v003 est distinct des registres v001/v002. La campagne CNG v003 n'est pas déclarée exécutée tant que le registre et les artefacts ne l'attestent.

Pour les ablations LOO, v002 réutilise le checkpoint et les prédictions exacts du modèle complet au lieu de le réentraîner à chaque reprise ; il arrête la reprise si un artefact orphelin partiel est détecté. Ce script est prêt mais non exécuté.

## 5. Branche CNC

CNC v003 est conservé comme exploratoire : son C4 direct utilisait des centres aléatoires. CNC v004 initialise C4 par KMeans sur les seules données d'entraînement. Le premier run v004 (seed 1501) a terminé et ses checkpoints, prédictions, métriques et code/hash doivent être audités séparément. Il ne représente qu'une graine sur dix ; les neuf autres graines ne sont pas déclarées réalisées.

Dans CNC, `g1`–`g3` servent à construire/apprendre et choisir les spécialistes et le composeur ; `g4`–`g5` sont générés après gel de C1/C2 et servent de compositions inédites. `SUB`, absent de g1–g3, utilise un jeu de données opératoire standalone explicitement documenté. Ce choix doit rester visible dans les résultats et ne doit pas être présenté comme apprentissage de SUB à partir des graphes.

## 6. Accès test et statut des métriques

Les runs en cours ne consomment que train/validation. Les données ARFF scellées restent hors des scripts d'entraînement et en lecture seule. Tous les nombres communiqués avant le gel final sont des résultats de validation ou de holdout de composition synthétique, et non des performances sur les tests tabulaires scellés. Aucun test tabulaire scellé n'est ouvert dans les résultats actuellement documentés.

## 7. Verdicts permis

Les anciennes versions peuvent étayer une hypothèse exploratoire. Elles ne remplacent pas les versions corrigées. En l'absence d'une campagne complète (seeds, checkpoints, prédictions, contrôles indépendants et ressources), le statut est `INCOMPLETE_QUOTA` ou `NOT_TESTED`, jamais un succès implicite.

## 8. Synchronisation finale JSON/Markdown (audit 2026-11-03)

Un contrôle strict en octets a détecté que le champ `prompt` de `prompt_ex11.json` et `PRE_REGISTRATION_EX11.md` différaient uniquement par le saut de ligne final. Le contrôle antérieur avait déclaré à tort une identité exacte. Le champ JSON a été synchronisé sur le préenregistrement complet ; `revision.prompt_body_sha256` enregistre maintenant le SHA-256 du corps. Vérification après écriture : identité octet pour octet et hash correct. Cette correction documentaire n'a modifié aucun script, dataset, split, checkpoint, prédiction ou métrique.

## Addendum — comparabilité CNC et CNG, 2026-11-03

- Le contrôle CNC a relevé que la comparaison directe C3_MLP/C4_AdaptiveRBF de v004 utilisait deux graines d'ordre de mini-batches distinctes. Le code v004 et ses résultats sont conservés sans modification. Le nouveau `train_cnc_composition_v005.py` utilise une graine d'ordre appariée par graphe/seed, tout en gardant des initialisations de poids indépendantes ; `run_cnc_campaign_v005.py` est son runner séquentiel. Tests : `tests/test_cnc_paired_batch_order_v005.py`.
- Le nouveau `train_cng_suite_v004.py` calcule pour chaque candidate A1/A2/A3 son propre MLP apparié et son MLP GE4X réel. Les ratios de paramètres sont écrits par run. Le MLP GE4X ne doit jamais être accepté sous 4.0. KMeans est train-only et l'ordre des mini-batches est partagé au sein de chaque triplet apparié.
- `run_cng_loo_ablation_v004.py` ne réentraîne pas la baseline A3 : il charge et vérifie les checkpoints A3 exacts issus de CNG v004 avant F_FROZEN/R_RETRAIN.
- Ces scripts ont été compilés et couverts par tests, mais aucune de ces nouvelles campagnes n'est déclarée exécutée dans cet addendum.
