# Protocole supplémentaire pré-exécution — classification manuscrite 3 contre 8

**Version :** supplement v1.0
**Statut :** analyse supplémentaire, séparée de l'expérience principale et préenregistrée avant l'exécution de ce supplément. Elle est ajoutée pour étudier un cas réel à 64 caractéristiques pixel et une composition haute-dimensionnelle ; elle ne remplace ni ne requalifie les résultats primaires déjà obtenus.

## Question
Les quatre méthodes de classification déjà définies dans le protocole principal se comportent-elles de façon comparable sur un jeu réel d'images manuscrites, et la substitution de neurones cachés par des sondes reste-t-elle fidèle dans ce cas à 64 dimensions ?

## Données
Utiliser exclusivement `sklearn.datasets.load_digits`, filtrer les exemples dont l'étiquette vaut 3 ou 8, coder 3 comme 0 et 8 comme 1. Les 64 caractéristiques sont les intensités pixels d'une image 8×8. Le jeu filtré contient les exemples réels du benchmark livré avec scikit-learn. Aucun téléchargement externe n'est requis.

## Conditions, partitions et budgets
- Graines de modèle/split : 714, 825, 936.
- Séparation stratifiée imbriquée 60 % train, 20 % validation, 20 % test : premier split test 20 % avec `random_state=seed+100`, second split validation 25 % du reste avec `random_state=seed+117`.
- StandardScaler ajusté sur le train uniquement.
- Quatre méthodes identiques aux méthodes primaires : sonde RBF adaptative A (220 époques), sonde à taux par groupe méta-appris B (35 étapes d'hypergradient, 700 époques finales), contrôle RBF fixe (220 époques) et MLP tanh de 16 unités (220 époques). A, B final, fixe et MLP s'entraînent sur train+validation après sélection des taux B sur train/validation.
- Composition : MLP enseignant de 16 unités entraîné sur train uniquement. Chaque unité cachée est imitée à partir des activations observées sur train seulement, par une sonde RBF scalaire de 8 centres, Adam 0,012, 150 époques. Remplacement de 1, 4 ou 16 unités, en conservant explicitement la lecture de sortie de l'enseignant. Cette condition mesure la propagation d'erreur, pas un étudiant autonome.
- Budgets de référence : chaque neurone MLP d'entrée 64D a 65 paramètres (poids et biais) ; chaque sonde RBF scalaire à 8 centres en 64D a 529 paramètres. Cet écart est déclaré avant calcul.

## Règle rouge
Les labels de test et les références de test ne sont jamais fournis aux fonctions d'ajustement. Les prédictions et références servent à calculer les métriques après gel. Les identifiants sources et hachages de lignes sont enregistrés pour vérifier l'absence de recouvrement interdit. Aucune sélection d'architecture, d'hyperparamètre, de graines ou de métrique n'est effectuée sur les résultats de test.

## Métriques
Classification : accuracy, F1, ROC-AUC, log-loss et Brier. Composition : erreur MAE/RMSE/R² d'activation cachée, accuracy finale et écart absolu moyen de logits par rapport au réseau enseignant.

## Limites de portée
Cette analyse supplémentaire a été ajoutée après l'expérience primaire initiale ; elle est préenregistrée avant son exécution mais reste exploratoire par rapport au projet général. Le binaire 3-vs-8 ne représente pas la reconnaissance générale de 10 chiffres, et `load_digits` est un benchmark de machine learning, pas un déploiement opérationnel.
