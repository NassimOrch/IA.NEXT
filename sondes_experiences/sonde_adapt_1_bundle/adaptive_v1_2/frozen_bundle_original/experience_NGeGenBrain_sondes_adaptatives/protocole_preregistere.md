# Protocole préenregistré — NGeGenBrain : sonde adaptative et neurones artificiels

**Version :** 1.1-confirmatoire indépendante  
**Gel du protocole :** avant l'exécution confirmatoire de ce bundle  
**Statut :** protocole local horodaté et haché ; ce n'est pas un préenregistrement tiers, public ou horodaté par un registre indépendant.  
**Question principale :** dans quelles conditions une sonde adaptative apprend-elle une tâche, imite-t-elle la fonction entrée-sortie d'un neurone observé, et remplace-t-elle des composants neuronaux en composition ?

## 1. Documents théoriques de référence

- `NGeGenBrain_observation_formalisme_full_0.tex`, définition d'une sonde comme opérateur d'observation spécifié par identifiant/version, domaine, codomaine, acquisition, préconditions, budget, intrusion, sérialisation et contrôle ; une application d'observation est notée \(\Phi(p,x,f)\).
- `rapport_experience_sondes_adaptatives.tex`, étude antérieure `two moons` comparant MLP, RBF adaptatives et RBF fixes. Cette étude est une référence exploratoire et n'est pas mélangée aux résultats confirmatoires ci-dessous.

## 2. Conditions comparées

1. **A — Sonde RBF adaptative naturelle :** ensemble de fonctions radiales à centres, largeurs, poids de lecture et biais ajustables, entraîné par Adam sur les étiquettes de la tâche.
2. **B — Sonde avec mécanisme d'adaptation appris :** même famille RBF ; quatre taux de mise à jour par groupe de paramètres sont optimisés au moyen d'hypergradients sur des épisodes support/requête provenant des partitions train/validation. Le gradient et la forme RBF restent préspécifiés. Cela teste l'apprentissage d'une partie du mécanisme d'adaptation, pas une règle d'apprentissage émergente sans structure.
3. **Contrôle — Sonde RBF fixe :** centres et largeurs fixes, lecture linéaire entraînable.
4. **D — Neurone/réseau de référence :** MLP à une couche cachée de 16 unités tanh pour la classification.
5. **C1 — Imitation isolée :** régression RBF sur des couples entrée/sortie d'un neurone cible en boîte noire ; la fonction d'ajustement ne reçoit ni la graine ni la famille d'activation de la cible, ni ses paramètres.
6. **C2 — Imitation compositionnelle :** une sonde scalaire RBF imite les activations de neurones cachés observées à partir de l'entrée. On remplace dans le MLP enseignant 1, 4 ou 16 unités. Le lecteur de sortie original est conservé : il s'agit d'un diagnostic de substitution de composants, pas d'un étudiant autonome.

## 3. Tâches et partitions

Tâches de classification : `two_moons`, `circles`, `xor_product` (synthétiques) et `breast_cancer` (jeu réel public Wisconsin Diagnostic Breast Cancer disponible dans scikit-learn ; benchmark informatique seulement, aucune conclusion clinique).

- Graines d'initialisation confirmatoires : **714, 825, 936**.
- Générateurs de données synthétiques : graines fixes **20261028**, **20261029**, **20261030** respectivement.
- Partition stratifiée : 60 % entraînement, 20 % validation, 20 % test, avec graines de découpage `seed + 100` et `seed + 117` dans le second découpage.
- Le `StandardScaler` est ajusté exclusivement sur le sous-ensemble train (60 %). La transformation est ensuite appliquée aux trois partitions.
- Les modèles finaux de classification sont réajustés sur train+validation (80 %) une fois les taux de mise à jour de B appris ; le test n'est utilisé qu'après gel de tous les paramètres.

## 4. Paramètres gelés

- MLP : 16 unités tanh, Adam, taux 0,01, weight decay 1e-4, 220 époques.
- Sonde RBF adaptative A : 16 centres, centres et log-largeurs apprenables, lecture scalaire, Adam, taux 0,01, weight decay 1e-4, 220 époques.
- Contrôle fixe : même nombre de centres initialisés sur les données train+validation ; centres/largeurs fixes ; seuls les poids de lecture et le biais sont entraînés par Adam, taux 0,01, 220 époques.
- B : 35 étapes d'hypergradient ; mini-lot support de taille min(64,n_train), requête de validation de taille min(96,n_val) ; quatre taux bornés dans (0,0,03). Pour l'étape virtuelle, l'actualisation utilise une normalisation du gradient documentée dans le code ; après méta-ajustement, les taux appris sont utilisés comme taux par groupe d'Adam pour 700 époques. Cette méthode n'est pas appelée apprentissage autonome général : c'est un méta-ajustement de taux par tâche.
- Imitation isolée : budgets de **64, 256, 1024** couples entrée/sortie ; 4000 requêtes de test indépendantes par cible ; 9 cibles cachées (graines évaluateur 107, 110, 113, 208, 211, 214, 309, 312, 315 : trois cibles par famille tanh/ReLU/sigmoïde) et 3 initialisations de sonde indépendantes (111, 222, 333) ; RBF à 20 centres, Adam 0,015, 240 époques.
- Composition : tâches `two_moons` et `breast_cancer`, graines 411/522/633 ; MLP enseignant entraîné sur le sous-ensemble train ; 16 sondes scalaires ; 12 centres en 2D et 8 centres en 30D ; Adam 0,012, 150 époques par sonde ; remplacement ordonné des unités 0, puis 0–3, puis des 16 unités.

## 5. Métriques prédéfinies

- Classification : exactitude (principale), F1, ROC-AUC, log-loss et Brier. Résumés : moyenne et écart-type entre trois graines. Les métriques sont descriptives ; trois graines ne suffisent pas à revendiquer une supériorité générale.
- Imitation isolée : RMSE et R² sur les 4000 sorties de test ; MAE en complément. La famille d'activation est une métadonnée d'évaluation, non une entrée de l'entraîneur de sonde.
- Composition : MAE/RMSE/R² des activations par neurone, exactitude finale, variation moyenne absolue des logits par rapport au MLP enseignant, pour 1/4/16 remplacements.
- Aucune hypothèse ne sera déclarée démontrée par simple similarité de scores. L'équivalence exacte exige une preuve adaptée, pas seulement des échantillons.

## 6. Règle rouge et compartimentation

- Les fonctions d'ajustement ne reçoivent jamais les étiquettes de test.
- La fonction d'imitation isolée reçoit seulement `(x_train, observed_y_train, probe_seed)` ; aucun paramètre du neurone et aucune métadonnée de famille n'est transmis.
- Les probes de composition reçoivent `(x_train, activation_observée_du_neurone)` ; les activations de test sont utilisées seulement dans l'évaluateur après gel.
- Les graines de sonde sont indépendantes des graines des cibles. Les données de test sont séparées avant standardisation et entraînement.
- Le code et les appels de fonctions seront audités. L'audit de code ne constitue pas une preuve de sécurité contre un processus hostile ayant un accès arbitraire au système de fichiers ; le rapport indiquera cette limite.
- Les références d'évaluation sont présentes dans les artefacts postérieurs au gel pour permettre la reproduction et la vérification. Elles ne sont pas des entrées des fonctions d'apprentissage.

## 7. Exclusions et décisions

- Toutes les tentatives de mise au point antérieures à ce protocole sont considérées exploratoires et ne sont pas combinées aux résultats finaux.
- Aucune graine, tâche ou méthode ne sera exclue en fonction des scores finaux.
- Les résultats négatifs, les régressions et les écarts de fidélité seront reportés.
- Si une erreur de protocole est détectée, les résultats concernés seront signalés comme invalides et ne seront pas silencieusement remplacés.

## 8. Limites prévues

- Les trois tâches synthétiques n'établissent pas la validité sur tous les problèmes.
- Le benchmark du cancer du sein n'est pas une validation clinique.
- La sonde RBF imite une famille de neurones simples et des activations d'un MLP de petite taille, pas l'ensemble des neurones possibles.
- B apprend une partie choisie à l'avance du mécanisme d'adaptation ; il ne découvre pas son architecture et ne constitue pas un méta-optimiseur universel.
- La composition conserve la lecture finale du MLP original et n'est pas un modèle entièrement autonome.
- Les résultats de trois graines sont exploratoires ; tout intervalle statistique sera interprété prudemment.
