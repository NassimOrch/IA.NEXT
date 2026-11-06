# Addendum de protocole — isolation locale renforcée v1.1

Date de gel : 2026-10-28 (heure du système inscrite dans `audit/strict_isolation_v1_1_preexecution_hashes.json`).

## 1. Statut des tentatives précédentes

La tentative v1.0 est classée **PILOTE NON CONFIRMATOIRE**. Elle a commencé avant que l'ensemble des empreintes de préexécution soit gelé. En outre, sa première conception plaçait plusieurs entrées de cibles dans un répertoire lisible par la même identité de rôle. Même si les scripts n'ouvraient que le fichier passé en argument, les permissions Unix n'empêchaient pas un processus de lire les autres fichiers de cette identité. Ces sorties et journaux sont exclus des résultats confirmatoires de la réplication v1.1 ; ils ne remplacent ni ne modifient les résultats primaires déjà archivés.

## 2. But

Répéter les vérifications de classification, d'imitation boîte noire et de composition déjà prévues, avec des processus OS séparés et une frontière d'accès par appel d'apprentissage. L'objet est de renforcer l'audit anti-fuite ; il ne s'agit pas de prétendre qu'un bac à sable local protège contre root, un noyau compromis ou tous les canaux auxiliaires.

## 3. Isolation par appel

Chaque appel d'entraînement reçoit un répertoire privé distinct sous `private_items/`. Le parent est root-owned en mode `0711` (traversable mais non listable). Chaque répertoire d'item reste root-owned `0700` sauf pendant son appel prévu ; pendant ce seul appel, il est temporairement donné à l'identité de rôle correspondante, en `0700`, avec les fichiers en `0600`. Tous les autres items restent root-only `0700`. Après le processus, les items et les modèles générés sont rendus à root, puis les seuls checkpoints nécessaires sont copiés dans le répertoire d'inférence `www-data`.

Les entraînements sont séquentiels au sein d'une identité de rôle lorsqu'une identité est réutilisée. Ainsi, aucune identité ne peut lire les observations d'une autre cible pendant son appel actif. Les appels de composant ne reçoivent qu'une seule colonne d'activation observée sur le train et les entrées correspondantes. Les paramètres de l'enseignant ne sont pas accessibles à l'identité de formation de composant.

## 4. Rôles et informations

- `ngb_cls` : un unique couple tâche/partition à la fois, avec train et validation autorisés ; aucun test, aucun coffre de labels, aucun code oracle.
- `ngb_imit` : une cible et un budget opaque à la fois ; seulement les couples entrée-sortie observés du train. Les entrées/sorties de test et la table cible-token restent inaccessibles.
- `ngb_teacher` : un seul split d'entraînement à la fois ; train uniquement pour entraîner l'enseignant et observer ses activations train.
- `ngb_comp` : un seul composant cible à la fois ; entrées train et activations train d'une seule unité.
- `www-data` : inférence sur X de test et modèles gelés ; aucun label de test.
- `root` : préparation des données/références, changement des permissions et calcul des métriques après génération des prédictions.

Le code d'oracle et le contrôleur principal sont temporairement inaccessibles aux identités d'apprentissage durant les appels d'entraînement. Les permissions effectives sont vérifiées sous les identités réelles, y compris la non-lecture d'un item frère.

## 5. Correction de neutralité pour la condition B

Dans la réplique v1.1 seulement, les quatre taux initiaux de mise à jour méta-appris sont initialisés de façon symétrique, à 0,015 (zéro logit sous la borne 0,03), plutôt que par une liste de taux différents choisie manuellement par groupe. Les gradients d'hyperparamètres sur la validation autorisée apprennent ensuite les taux. Le schéma de mise à jour par gradient reste préspécifié ; la condition B n'est toujours pas une découverte ex nihilo d'un optimiseur.

Cette correction rend la réplique B volontairement non identique à la B historique. Les comparaisons d'identité octet/score ne sont exigées que pour A, le contrôle fixe et le MLP, qui ne changent pas. L'écart de B est publié comme analyse de sensibilité et non masqué.

## 6. Plan expérimental gelé

- Classification : tâches `two_moons`, `circles`, `xor_product` et benchmark public `breast_cancer`, graines 714/825/936, même logique de partition que le dossier primaire. Quatre méthodes : A RBF adaptative, B taux méta-appris avec initialisation neutre, RBF fixe et MLP. Trois partitions par tâche.
- Imitation : neuf cibles scalaire boîte noire, familles ReLU/tanh/sigmoid, budgets 64/256/1024, graines sonde 111/222/333, 4000 entrées test par cible-budget. Le token cible est opaque dans le processus d'apprentissage.
- Composition : tâches `two_moons` et `breast_cancer`, graines 411/522/633, MLP enseignant à 16 unités, imitation indépendante de chaque activation cachée à partir du train, remplacement de 1/4/16 unités. Le readout aval original reste conservé ; cela ne constitue pas un modèle autonome.

## 7. Règles d'intégrité

- Préenregistrer et hacher le protocole, les modèles de travail et le contrôleur avant toute exécution confirmatoire v1.1.
- Contrôler le chevauchement des partitions par empreinte de lignes.
- Vérifier les droits de lecture autorisés et interdits sous chaque compte.
- Vérifier que les sorties d'inférence sont produites avant ouverture du coffre de labels.
- Enregistrer les prédictions brutes, tailles des partitions, budgets, logs, graines et SHA-256.
- Ne pas effacer les tentatives pilotes ; les marquer comme non confirmatoires.
- Aucun contrôle ne prouve une absence absolue de canal caché ; l'audit indique exactement la portée de ses garanties.

## 8. Limites d'interprétation

Le protocole teste une extension paramétrée RBF de la définition observationnelle de NGeGenBrain ; l'apprentissage n'est pas une propriété automatiquement impliquée par la définition de sonde source. Les résultats peuvent étayer une approximation empirique de certaines fonctions/activations sur le domaine testé. Ils ne démontrent pas une équivalence universelle. La composition conserve le readout aval. Les benchmarks publics sont des tâches de laboratoire et non une validation de production.
