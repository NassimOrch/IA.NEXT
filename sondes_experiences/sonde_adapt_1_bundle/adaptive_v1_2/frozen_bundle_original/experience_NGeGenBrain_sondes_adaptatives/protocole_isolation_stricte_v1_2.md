# Protocole confirmatoire v1.2 — isolation stricte et partitions inédites

Date de gel : 28 octobre 2026. Version indépendante de v1.1.

## Pourquoi une version v1.2

La v1.1 a servi à auditer les barrières de permissions et à rejouer les tâches existantes. L'inspection des constantes a révélé que ses graines de classification et de composition étaient déjà celles du banc principal. Elle ne doit donc pas être présentée comme une réplication indépendante sur de nouvelles partitions. Ses résultats restent un audit de séparation des rôles et de sensibilité d'initialisation, non un nouveau test confirmatoire.

La v1.2 reprend le même principe de sonde et le même protocole d'observation, mais utilise des graines et des partitions distinctes des résultats antérieurs. Les résultats historiques ne sont pas chargés par le contrôleur d'évaluation pendant l'entraînement ni utilisés pour sélectionner les modèles v1.2. Les correspondances avec les historiques ne seront faites qu'en audit final, et uniquement pour vérifier la non-réutilisation des identifiants/graines.

## 1. Sonde testée — provenance obligatoire

La sonde est l'extension paramétrée du formalisme d'observation de `NGeGenBrain_observation_formalisme_full_0.tex`, explicitée dans `formalisme_sonde_adaptative.tex`. Le formalisme original spécifie un opérateur d'observation (version, domaine/codomaine, acquisition, préconditions, budget, intrusion, sérialisation, contrôles) mais ne fait pas de l'apprentissage une propriété automatique de toute sonde. La modification expérimentale paramètre une famille RBF :

\[
P_\theta(x)=b+\sum_{j=1}^{K} w_j\exp\!\left(-\frac{\|x-c_j\|^2}{2\exp(\lambda_j)^2}\right),\qquad
\theta=(c_j,\lambda_j,w_j,b).
\]

Pour A/C, centres, largeurs, poids et biais sont optimisés par gradient sur les signaux autorisés. Le témoin fixe garde les centres et largeurs non entraînables. Pour B, la famille fonctionnelle reste identique ; les quatre taux de groupe sont initialisés de manière neutre à 0,015 chacun et sont ensuite estimés par hypergradients sur les épisodes train/validation autorisés. L'architecture et la mise à jour par gradient restent préprogrammées : B n'apprend pas un optimiseur général depuis zéro.

## 2. Conditions et graines gelées

- Classification : `two_moons`, `circles`, `xor_product`, `wine_binary`; les trois tâches synthétiques sont régénérées avec les graines de générateur 20261121, 20261122 et 20261123, et le cas réel utilise le jeu Wine (source distincte de breast-cancer et digits); graines de split `[1501, 1607, 1717]`; quatre méthodes A, B, sonde RBF fixe et MLP.
- Imitation boîte noire : 9 neurones-sources à graines `[401,402,403,503,504,505,607,608,609]`, réparties avant l'évaluation entre trois familles d'activation définies par la cible; budgets d'observation `[64,256,1024]`; trois initialisations de sonde `[1011,2022,3033]`; 4 000 entrées de test indépendantes par cible-budget. Les cibles sont des fonctions neuronales artificielles à deux entrées ; la sonde ne reçoit que les paires `(x,N(x))` d'entraînement.
- Composition : tâches fraîches `two_moons` et `wine_binary`; graines `[2401,2503,2609]`; remplacement de `[1,4,16]` unités cachées parmi 16. Le readout du MLP enseignant est conservé explicitement ; cette intervention n'est pas un étudiant autonome.
- Les partitions synthétiques v1.2 proviennent de nouvelles données générées et le cas réel Wine est un jeu distinct; les graines v1.2 sont distinctes des graines historiques du banc principal (`[714,825,936]` en classification et composition; les neuf graines antérieures d'imitation sont `[107,110,113,208,211,214,309,312,315]`). Les initialisations de sonde d'imitation v1.2 sont `[1011,2022,3033]`, distinctes de `[111,222,333]`.

## 3. Règles d'accès et séparation des rôles

- Le contrôleur racine construit les partitions et garde le générateur de cibles, les références du test et les clés de correspondance.
- Chaque appel d'apprentissage reçoit un répertoire opaque privé, accessible en lecture/écriture uniquement à l'identité du rôle concerné pendant cet appel. Les autres répertoires de cibles restent possédés par root, mode 0700, sous un parent non listable.
- Les rôles d'apprentissage n'ont pas accès aux sources oracle, aux paramètres cachés des cibles, aux sorties de test, aux labels de test ou aux fichiers d'apprentissage d'un autre appel.
- Le rôle d'inférence séparé ne reçoit que les X de test et les modèles gelés. Il ne peut pas lire les labels du test.
- Toutes les prédictions d'un bloc sont produites avant que le contrôleur ouvre le coffre des labels pour calculer les métriques. Aucun modèle n'est mis à jour après le gel.
- L'imitation autorise les seules observations `(x,N(x))` fournies au budget déclaré. C'est le signal d'entraînement attendu, pas un contournement.

## 4. Audit préalable et sorties

Avant exécution, les hashes SHA-256 du protocole, des modèles, du worker, du contrôleur et des deux sources théoriques sont gelés dans `audit/strict_isolation_v1_2_preexecution_hashes.json`. Les pilotes v1.0/v1.1 ne sont pas intégrés aux résultats v1.2.

Sorties attendues, sans réutilisation d'anciennes métriques :
- classification : 48 lignes (4 tâches × 3 graines × 4 méthodes) et toutes les prédictions individuelles;
- imitation : 81 évaluations (9 cibles × 3 budgets × 3 initialisations) et 324 000 lignes de prédiction approximativement (si chaque combinaison évalue exactement 4 000 points);
- composition : 18 évaluations (2 tâches × 3 graines × 3 niveaux de remplacement), 96 modèles de composants (6 systèmes × 16 unités) et métriques de fidélité locale.

Les nombres ci-dessus sont les tailles prévues, pas des résultats. Les décomptes réels, réussites/échecs et métriques seront rapportés exclusivement à partir des fichiers créés par cette exécution.

## 5. Critères d'invalidation

Une étape est invalide si : un rôle d'apprentissage peut lire un label/test X interdit ou une cible sœur; les hashes révèlent un chevauchement exact d'entrées entre train et test; le code gelé diffère avant l'exécution; les lignes/identifiants sont incomplets ou dupliqués; les paramètres sont changés après gel; ou un résultat est sélectionné selon les scores de test. Une erreur technique ou un audit post-traitement défectueux est documenté séparément et ne doit pas transformer des sorties manquantes en résultats.

## 6. Limites non négociables

Les contrôles de permissions de système d'exploitation et les inspections statiques ne prouvent pas l'absence de tout canal indirect. Le cas Wine est binaire (classe 0 contre classes 1/2) pour rester comparable à la tête de classification binaire; le benchmark multiclasses digits reste un résultat antérieur distinct. Les fonctions à imiter sont une classe réduite de neurones artificiels et les tests ne prouvent pas une équivalence universelle. Le benchmark breast-cancer et les tâches publiques ne sont pas des outils de décision clinique. Une bonne imitation locale ou la conservation du readout original ne signifie pas reconstruction autonome d'un réseau.

## 7. Capsules logicielles par rôle (règle anti-triche renforcée)

Chaque rôle reçoit une capsule de code distincte, copiée avant exécution dans un répertoire possédé par son identité système, répertoire en mode `0500` avec scripts/modules en mode `0400`. Le parent des capsules est non listable par les comptes de rôle (`0711`), tandis que les capsules des autres rôles n'autorisent ni lecture ni traversée. Le paquet source complet est rendu non traversable/non lisible par les comptes de rôle pendant toute la série (`ROOT` mode `0750`), jusqu'au nettoyage explicite après les dernières exécutions.

- `ngb_imit` reçoit uniquement `strict_imitation_worker_v1_2.py` et `strict_models_imitation_v1_2.py`, qui implémentent une RBF générique et ne contiennent pas la formule/classe des cibles.
- `ngb_comp` reçoit uniquement `strict_component_worker_v1_2.py` et `strict_models_component_v1_2.py`, qui apprennent une colonne d'activations fournie dans un fichier d'observation autorisé, sans code d'enseignant ni de readout.
- `ngb_teacher` seul reçoit le code qui construit et entraîne le MLP enseignant.
- `www-data` seul reçoit le code d'inférence qui charge les modèles gelés et produit les prédictions ; il ne peut pas lire les labels de test.
- `ngb_cls` reçoit le code de classification; il ne peut pas lire les capsules enseignant ou évaluateur, ni le paquet source.

La vérification de permissions est faite réellement par `runuser` avec chaque identité, pas seulement en inspectant les modes. Le test de fumée préalable a 13 assertions positives sur des données jetables; il vérifie les interdictions de lecture, les interfaces des workers et l'absence de formule de cible dans les modules d'imitation/composition. Ces tests ne sont pas des résultats scientifiques.

## 8. Gel et audit

Le SHA-256 des sources de référence, de `run_experiment.py` (oracle/contrôleur), du contrôleur v1.2, du protocole et de tous les workers/modules séparés est gelé dans `audit/strict_isolation_v1_2_preexecution_hashes.json` avant la phase scientifique. Toute modification après ce gel invalide la qualification confirmatoire de l'exécution concernée, sauf nouveau numéro de version, nouveau gel et nouvel essai.
