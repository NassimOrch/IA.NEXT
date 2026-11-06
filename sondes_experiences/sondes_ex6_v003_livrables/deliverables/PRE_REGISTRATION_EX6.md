# PRE_REGISTRATION_EX6 — Plan prospectif de confirmation

**Statut : DOCUMENT DE PRÉ-ENREGISTREMENT POUR LES PROCHAINES CAMPAGNES, PAS POUR LES PILOTES DÉJÀ EXÉCUTÉS.**

Les pilotes contenus dans `results/raw/` ont été réalisés pendant l'élaboration opérationnelle d'EX6. Ce document est rédigé après ces pilotes ; il ne peut donc pas les rendre rétroactivement pré-enregistrés. Les pilotes restent descriptifs et développement historiques. Aucun jeu test historique ne sera réutilisé comme test confirmatoire.

## 1. Question et hypothèses

Pour chacune de Replica, Emplica simple et Emplica Orchestra, tester si le système complet :
1. atteint une qualité non inférieure à un MLP compétent sur accuracy **et** log-loss ;
2. contient au moins quatre fois moins de paramètres numériques persistants que son MLP-ge4x apparié ;
3. consomme moins de ressources sur chaque dimension mesurée ;
4. est plus rapide en entraînement complet et en inférence.

Les hypothèses ne prédisent aucun résultat. Un critère manquant ou non satisfait interdit le succès global.

## 2. Données et gel

Avant la campagne confirmatoire :
- choisir un ou plusieurs domaines qui n'ont jamais été inspectés ou utilisés dans EX2–EX6 ;
- enregistrer provenance, version, licence, date, groupes/sujets et protocole de nettoyage ;
- fixer train/adaptation/validation/test par identifiants, avec un chargeur n'exposant pas les lignes test avant gel ;
- séparer strictement toute préparation/apprentissage de transformation au seul train autorisé ;
- publier les hashes du manifeste des lignes, split, preprocessing, code, config et graines ;
- geler architecture, recherche, marges, sélection, activation et script avant test.

Le Wisconsin `v009` et tout dataset historique des workspaces antérieurs restent développement. Le split historique n'est pas un substitut à un test vierge.

## 3. Marges de non-infériorité

Aucune marge numérique n'est présupposée dans cette révision : elle doit être justifiée par l'application, la variabilité de mesure et l'effet minimal pertinent, puis renseignée et gelée dans `configs/confirmatory_preregistration.json` **avant tout accès aux labels du test**. La marge doit être définie séparément pour accuracy et log-loss, par domaine. L'absence de marge justifiée implique une comparaison descriptive seulement et interdit la revendication de non-infériorité.

Plan statistique minimal :
- comparaisons appariées sur les mêmes exemples et partitions ;
- bootstrap au niveau sujet/groupe quand nécessaire ;
- IC pour la différence candidate − MLP ;
- nombre de graines et jeux indépendants déterminés avant exécution ;
- correction de multiplicité lorsque plusieurs candidates/couches sont sélectionnées ;
- pas d'interprétation des graines répétées comme des échantillons indépendants.

## 4. Comparateurs et budgets

Pour chaque candidate et graine :
- MLP matched au `P_total` complet de la candidate ;
- MLP-ge4x tel que `P_MLP_total / P_candidate_total >= 4`, vérifié après sérialisation ;
- même données, prétraitement autorisé, split, métriques, hardware, budget de recherche et politique d'arrêt ;
- tout prétraitement, centre fixe, buffer, gate, table, copy frozen et optimizer state recensé.

Les MLP sont des réseaux denses compétents et réglés sans handicap. Toute modification de leur capacité impose un nouveau compte et une nouvelle mesure du ratio.

## 5. Protocoles expérimentaux à pré-enregistrer

### Replica
Pré-définir les modes distincts : partition d'experts, partition de calcul interne, partition de batch, partage de valeurs intermédiaires. Vérifier hash/égalité du clone et invariance des tenseurs figés. Documenter gradients, synchronisation et allocations. Mesurer primaire seul, duplicata sériel, duplicata réellement parallèle, contrôle sans duplication. Distinguer entraînement et inférence ; ne pas annoncer de gain d'entraînement à partir d'un benchmark d'inférence.

### Emplica simple
Comparer au minimum :
- hétérogène, variantes différentes par couche ;
- homogène, même variante partout, choisie sur boucle de validation ;
- spécialiste, variante choisie pour chaque couche par sélection imbriquée/OOF ;
- mono-couche et ablations sans correction/communication.
Pré-définir le nombre de couches, le nombre de sondes/couche, la représentation transmise et les budgets. Toute correction apprise sur sorties train doit utiliser prédictions OOF ou un équivalent sans fuite.

### Emplica Orchestra
Définir par avance adaptation locale et globale interne `theta_{l,i}`, `phi_l`, ainsi que la coordination externe `psi`. Comparer hétérogène, homogène, spécialiste, gate externe fixe et conditionné par X, ablation sans global externe, ablation sans messages, une seule couche, toutes couches. Correcteurs OOF, seuils de cascade, calibration et activation sont ajustés uniquement sur données permises, puis gelés. Publier couverture et qualité conditionnelle pour chaque chemin.

## 6. Mesures

Pour tout candidat et MLP : paramètres complets, bytes sérialisés, MAC/FLOP, évaluations de distances/RBF/exponentielles, temps total bout en bout, temps de convergence, latence batch 1/16/64/256 selon domaine, p50/p95/p99, throughput, RSS/VRAM de pointe, mémoire d'activation, état d'optimiseur, synchronisation, coût des gates/copies et énergie si mesurable. Warmup, répétitions, randomisation de l'ordre et synchronisation backend sont décrits. Un axe obligatoire non mesuré interdit le succès global.

## 7. Règle de verdict

`SUCCÈS GLOBAL` seulement si toutes les conditions sont satisfaites et auditables. Sinon séparer exactement : `SUCCÈS PARTIEL`, `ÉCHEC SUR CRITÈRE MESURÉ`, `NON CONCLUANT`, `INCOMPLET`. Aucun axe ne compense l'échec d'un autre. Toutes les graines, erreurs et runs interrompus restent publiés.
