# Protocole préenregistré — NG-ADAPT-DIGITS10-R1

**Gel du protocole :** 29 octobre 2026, avant le smoke test.  
**Question :** les tendances observées sur les tâches binaires se maintiennent-elles sur le problème multiclasse `load_digits` (chiffres 8×8, dix classes) ? Ce protocole est exploratoire et ne remplace ni les résultats binaires ni les expériences historiques.

## Données, déduplication et partitions

- Source locale : `sklearn.datasets.load_digits`, jeu public intégré à scikit-learn. Valeurs pixel d'origine dans `[0,16]`, divisées par 16 avant mise à l'échelle.
- Chaque image est représentée par 64 caractéristiques, étiquette entière `0..9`.
- Avant le split, les vecteurs de caractéristiques exactement identiques sont groupés par SHA-256 et une seule occurrence est retenue, sans conditionner la décision de déduplication à l'étiquette. Les conflits d'étiquettes pour un même vecteur sont comptés et consignés; aucune correction silencieuse.
- Partition stratifiée et fixe par indices : test 15 %; du reste, une partition provisoire de 25/85 est réservée puis scindée en validation 60 % / adaptation 40 %, ce qui vise train/validation/adaptation/test = 60/15/10/15 % environ. Graines de split dérivées de `task_seed=20261126`.
- Le `StandardScaler` est ajusté sur train uniquement, puis appliqué aux quatre partitions. Les hash de caractéristiques brutes et hash des indices de partition sont archivés. Toute intersection exacte entre partitions est une erreur.

## Architectures A–K

Le runner réutilise les familles et le contrat opérationnel de la campagne principale, avec la sortie adaptée à dix classes :

- A/F : MLP tanh à une couche cachée de 16 unités; F reçoit l'adaptation en ligne après prédiction.
- B/G : quatre sondes RBF adaptatives, shards train disjoints, agrégation uniforme; G boucle en ligne.
- C/H : mêmes sondes avec poids de coordination partagés `softmax(phi)` et mise à jour centralisée; H boucle en ligne.
- D/I : sondes locales avec activation `tanh` sur les logits; I boucle en ligne.
- E/J : sondes coordonnées avec `tanh`; J boucle en ligne.
- K : contrôle RBF à 16 centres et largeurs fixes; seuls poids de sortie et biais sont entraînés.

Les modèles RBF adaptatifs ont quatre centres par sonde. Les familles sont entraînées 90 époques avec les taux d'apprentissage hérités du protocole principal. Graines de modèle : `1501`, `1607`, `1717`. Le MLP et les sondes ont des nombres de paramètres proches par construction, mais K a une capacité plus faible; les temps observés ne valent pas égalisation stricte FLOPs/RSS.

## Ordre, adaptation et séparation des données

- Ajuster le modèle sur train seulement; validation sert à fixer un seuil descriptif q95 de résidu multiclass (norme L1 du vecteur one-hot moins la probabilité) pour journalisation. Ce seuil ne sélectionne pas les hyperparamètres.
- Pour F–J, au cours du flux d'adaptation, journaliser la prédiction avant observation, révéler ensuite l'étiquette d'adaptation, calculer l'empreinte et mettre à jour le modèle local. Cette boucle reproduit le mode « observation/empreinte puis mise à jour »; elle ne prétend pas que la valeur q95 décide du routage. La version causale du gate reste FBR-1, dans son propre protocole.
- Les étiquettes test ne sont ni transmises à la boucle ni utilisées pour calibrer un seuil. Le test est évalué une seule fois, après adaptation.

## Mesures préspécifiées

Accuracy, macro-précision, macro-rappel, macro-F1, log-loss multiclasse, Brier multiclasse (`moyenne des sommes des carrés des 10 erreurs de probabilité`), macro ROC-AUC one-vs-rest, ECE top-label à 10 intervalles, matrice de confusion, temps de train, temps d'adaptation, temps d'inférence, paramètres entraînables/partagés, mises à jour, messages estimés et prédictions par exemple.

Les contrastes appariés par graine sont descriptifs; avec trois graines, les intervalles t à 95 % ne sont pas confirmatoires. Aucun sweep d'hyperparamètres, arrêt anticipé ou choix sur test. Toutes les graines, erreurs et sorties négatives restent archivées.

## Intégrité et reprise

Chaque couple `(graine, architecture)` possède un checkpoint contenant métriques, prédictions, traces d'empreinte et SHA-256 de configuration. La reprise ne recalcule pas un checkpoint complet si sa clé protocole/configuration correspond. Le runner échoue en présence d'un checkpoint à configuration différente au lieu de le réutiliser silencieusement.

Le smoke test est uniquement un contrôle logiciel; ses métriques ne sont jamais agrégées à la campagne 90 époques. Les résultats restent marqués exploratoires, même si toutes les exécutions passent.
