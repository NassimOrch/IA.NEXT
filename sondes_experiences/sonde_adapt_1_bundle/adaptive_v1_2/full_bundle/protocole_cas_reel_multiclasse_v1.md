# Protocole complémentaire préenregistré v1 — reconnaissance réelle multiclasse

**Date de gel :** 2026-10-28, avant exécution de ce complément.
**Rôle :** compléter, sans remplacer ni mélanger, les expériences primaires déjà exécutées. Ce protocole a été ajouté car le benchmark réel principal précédent (cancer du sein, 569 exemples, binaire) était trop petit et simple pour constituer à lui seul une étude de cas d'usage suffisamment riche.

## Question
Les résultats d'apprentissage par sonde et la substitution de composants persistent-ils sur un jeu réel de reconnaissance d'écriture manuscrite à 10 classes, avec une entrée de 64 variables et des conditions d'apprentissage comparables ?

## Données et partitions
- Jeu public local `sklearn.datasets.load_digits` : 1 797 images manuscrites en niveaux de gris 8×8, pixels quantifiés, 10 classes.
- Aucune récupération réseau ni sélection par résultats de test.
- Graines/splits confirmatoires : 1428, 2539, 3640.
- Split stratifié : 60 % train, 20 % validation, 20 % test ; standardiseur ajusté sur train seulement.
- Les données de test et leurs labels ne sont accessibles qu'à l'évaluateur après gel des modèles/probes.

## Classification primaire
Comparaison sur chaque split :
1. A : RBF adaptative avec centres, largeurs et lecture entraînables.
2. B : mêmes familles RBF ; quatre taux de mise à jour par groupe sont appris par hypergradients train/validation ; l'architecture RBF et l'algorithme restent prédéfinis.
3. Contrôle RBF fixe : centres et largeurs fixes, seule la lecture est entraînée.
4. D : MLP 64-16-tanh-10.

A et D ont exactement 1 210 paramètres entraînables. B utilise la même architecture et le même nombre de paramètres finaux, avec un surcoût d'apprentissage méta. Le contrôle fixe a 170 paramètres entraînables ; il n'isole donc pas parfaitement adaptation et capacité. Les quatre modèles utilisent 220 époques finales ; les taux de B sont appris sur des épisodes train/validation puis gelés avant ajustement final. Les métriques principales sont accuracy, balanced accuracy, F1 macro et log-loss. Les graines prévues et les métriques sont fixées avant exécution.

## Composition secondaire
Pour chaque graine, un MLP enseignant 64-16-tanh-10 est entraîné sur train+validation. Pour chaque unité cachée, une RBF scalaire est entraînée uniquement sur paires (entrée, activation cachée observée) de train+validation. Après gel, on remplace les activations de 1, 4 puis 16 unités au test et on conserve explicitement le lecteur de sortie enseignant. On mesure accuracy, accord avec le réseau enseignant et RMSE des logits. Cette condition est un remplacement de composants, pas un modèle étudiant autonome.

- La composition est limitée à trois graines fixées, 8 centres RBF par unité cachée et 80 époques.
- Les hyperparamètres ne sont pas choisis à partir des résultats du test.
- Les paramètres enseignant ne sont pas passés aux fonctions de fitting des sondes ; seules les activations observées sur train+validation sont utilisées.

## Anti-fuite et contrôle
- Hachage SHA-256 des lignes brutes avant séparation et vérification de disjonction par split.
- Standardisation ajustée sur train uniquement.
- API d'entraînement séparées des labels du test.
- Sauvegarde des prédictions gelées avant calcul des résultats agrégés.
- Graine d'initialisation de la sonde distincte de la graine de split/cible.
- Reproductibilité vérifiée par réexécution d'un sous-ensemble, puis vérification des prédictions et fichiers.

## Limites d'interprétation
Le jeu est réel et multiclasse, mais demeure un benchmark public compact de laboratoire. Il ne prouve pas la performance d'un système de reconnaissance en production. Les trois splits offrent une réplication limitée ; les intervalles sont descriptifs. La composition conserve le lecteur de sortie source et n'établit pas l'autonomie d'un modèle entièrement reconstruit.
