# Définitions, théorèmes, hypothèses et portée

## 1. Définition opérationnelle retenue

La source `sonde_adapt_1_bundle.zip` définit la sonde adaptative à partir de `P=(F,U,eta_0)`. Nous conservons cette notation. Pour rendre explicites les limites d'accès, le dépôt ajoute un contrat de données `S_i` dans le commentaire théorique, sans prétendre qu'il faisait partie de la définition originale.

Un réseau est `R=(P_1,...,P_N,C,U_R,eta_R,0)` et son état complet est `eta_R,t=(theta_1,t,...,theta_N,t,phi_t,s_t)`. `theta_i` désigne les paramètres propres d'une sonde; `phi` est l'état partagé (ici quatre logits qui déterminent un mélange softmax); `s_t` contient seulement les états cachés utiles au résultat : état d'optimiseur, compteurs de synchronisation, RNG et provenance.

**Adaptation individuelle** : une règle modifie `theta_i` à partir des observations autorisées à la sonde i et de son contexte. **Adaptation globale** : une règle modifie `phi` ou la loi de coordination et peut conditionner les taux locaux. Le partage de paramètres n'est pas la même chose qu'un entraînement fédéré, ni que l'apprentissage méta de la règle d'optimisation.

## 2. Architecture expérimentale réellement implémentée

- Quatre sondes RBF gaussiennes; quatre centres initiaux par sonde; centres et largeurs sont entraînables.
- Les données train sont réparties en quatre shards stratifiés disjoints pour les mises à jour locales. Un coordinateur centralisé conserve néanmoins l'accès à l'ensemble train pour son objectif global.
- Agrégateur local : moyenne uniforme; agrégateur global : `softmax(phi)` sur les sorties scalaires des sondes.
- Activité optionnelle : `tanh` est appliquée à la sortie scalaire de chaque sonde avant agrégation. Elle n'est pas confondue avec les fonctions de base RBF.
- Taux local : `eta_i = eta0 * (0.5 + 2*w_i)`. `phi` démarre à zéro; pour quatre sondes gelées, `w_i=1/4` et le multiplicateur vaut 1.
- Optimisation locale : BCE-with-logits sur le shard de la sonde. Mise à jour globale toutes les cinq epochs sur les logits combinés calculés sur toutes les données train; les sorties des sondes sont détachées lors de la mise à jour de `phi`.
- Boucle en ligne : prédiction enregistrée avant révélation de l'observation; le label d'adaptation est ensuite révélé, le résidu et la surprise BCE sont enregistrés, puis une mise à jour est appliquée. Le flux d'adaptation est distinct du test final.

## 3. Résultats théoriques exacts

### Proposition A — réduction sans mise à jour globale

Avec même initialisation, mêmes shards, même ordre d'updates et mêmes optimiseurs, si `phi` est gelé à zéro dans la version globale, le softmax reste uniforme. Le multiplicateur de taux local vaut alors `0.5 + 2/4 = 1`. L'ensemble global gelé et l'ensemble local réalisent donc les mêmes mises à jour et les mêmes prédictions, à l'arrondi près. C'est une conséquence algébrique de l'architecture choisie, pas un nouveau théorème d'apprentissage. L'expérience dédiée a observé un écart absolu maximal de probabilité de 0 sur 2 673 prédictions appariées.

### Proposition B — réduction fonctionnelle en une sonde

Si toutes les sorties de sondes sont identiques, `a_i(x)=a(x)`, et les poids de mélange sont non négatifs avec somme 1, alors `sum_i w_i a_i(x)=a(x)`. Il s'agit d'une réduction de la fonction calculée, non d'une preuve d'identifiabilité des paramètres internes.

### Proposition C — erreur de composition

Si `f_tilde` approche `f` à l'erreur uniforme `epsilon_f`, `g_tilde` approche `g` à l'erreur uniforme `epsilon_g` sur le domaine utilisé, et `g` est `L_g`-Lipschitz entre les deux représentations, alors `||g_tilde(f_tilde(x))-g(f(x))|| <= epsilon_g + L_g epsilon_f`. La borne découle de l'inégalité triangulaire; elle ne garantit pas que le problème d'inversion soit soluble.

### Proposition D — non-identifiabilité à partir d'observations finies

Pour des points distincts `S={x_1,...,x_m}` sur la droite, `q(x)=c*prod_j (x-x_j)` s'annule sur tout S mais ne s'annule pas généralement hors de S. Ainsi `f` et `f+q` coïncident sur les observations finies et divergent ailleurs. Un accord sur un ensemble fini n'établit pas une équivalence mécanistique globale. Les résultats particuliers d'identifiabilité nécessitent des hypothèses structurelles plus fortes (par exemple les réseaux tanh minimaux irréductibles de Sussmann, 1992).

### Proposition E — stabilité de descente de gradient sous hypothèses

Si `L` est différentiable, minorée et `M`-lisse, la descente de gradient exacte avec `0 < eta < 1/M` satisfait `L(theta_{t+1}) <= L(theta_t) - eta*(1-M eta/2)*||grad L(theta_t)||^2`. Les hypothèses sont explicites. Elles ne sont pas établies pour le réseau neuronal non convexe, Adam, le coordinateur intermittent ou la boucle en ligne de la présente campagne. Nous ne revendiquons donc aucune convergence générale de ces algorithmes.

## 4. Boucle et filtration d'information

Soit `F_t` l'information révélée jusqu'à t. La prédiction `p_t` doit précéder la révélation de `y_t`; après révélation, `r_t=y_t-p_t` et `BCE_t=-y_t log(p_t)-(1-y_t)log(1-p_t)` peuvent alimenter une fingerprint. La fingerprint est un objet dérivé — timestamp, provenance, version du schéma, prédiction pré-observation, observation, résidu, surprise, masque de manque et SHA-256 — et non une nouvelle mesure indépendante. Si l'observation est manquante, il n'y a pas de résidu valide de label et la mise à jour supervisée correspondante doit être ignorée ou redéfinie.

## 5. Hypothèses préenregistrées vs conclusions empiriques

Hypothèses posées avant la campagne : trois graines d'initialisation (1501, 1607, 1717), partitions stratifiées fixes par tâche, normalisation train-only, A-J plus contrôle K, 90 epochs, métriques primaires accuracy et log-loss; tâches deux lunes, cercles, XOR-produit bruité, Wine binaire et chiffres 3 contre 8. Les tâches synthétiques isolent certains mécanismes et ne prouvent rien sur tous les systèmes d'IA.

Les intervalles t sont descriptifs avec `n=3` graines d'initialisation et un seul split par tâche. Les graines ne sont pas présentées comme des datasets indépendants; aucun test de supériorité confirmatoire n'est revendiqué. Aucune correction de multiplicité de p-values n'est requise puisqu'aucune famille de p-values confirmatoires n'est rapportée.

## 6. Références primaires

- Hornik, Stinchcombe & White (1989), universal approximation, sous hypothèses : https://doi.org/10.1016/0893-6080(89)90020-8
- Sussmann (1992), identifiabilité restreinte des réseaux tanh minimaux irréductibles : https://doi.org/10.1016/S0893-6080(05)80037-1
- Finn, Abbeel & Levine (2017), MAML : https://proceedings.mlr.press/v70/finn17a.html
- Franceschi et al. (2018), optimisation bi-niveau : https://proceedings.mlr.press/v80/franceschi18a.html
- McMahan et al. (2017), FedAvg : https://proceedings.mlr.press/v54/mcmahan17a.html
- Perdomo et al. (2020), performative prediction : https://proceedings.mlr.press/v119/perdomo20a.html
- Kaufman, Rosset & Perlich (2012), data leakage : https://doi.org/10.1145/2382577.2382579
