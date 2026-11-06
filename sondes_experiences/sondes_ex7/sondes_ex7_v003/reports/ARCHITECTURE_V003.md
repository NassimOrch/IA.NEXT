# Architecture V003 — OuterCoord-Lite-7x1

## Intention

Réduire Orchestra Org 7×5 à sept sondes locales indépendantes et un seul coordinateur global externe. La candidate retire la cascade et les sept coordinateurs internes. Elle conserve une coordination globale `rho` apprise, mise à jour séparément des sondes.

## Calcul à l'entraînement

1. Le train (341 lignes) est réparti une seule fois en sept shards stratifiés, mutuellement disjoints, à partir de `seed + 7001`.
2. Sept `AdaptiveRBF` (`d=4`, `k=8`, deux logits) sont initialisées avec des seeds dérivées de la graine racine.
3. Chaque probe est optimisée avec sa propre instance Adam et uniquement les lignes de son shard pour la loss supervisée locale. Les centres RBF sont initialisés par KMeans sur les caractéristiques de l'ensemble `Xtr` (sans labels) ; cette initialisation globale est explicitement conservée comme nuance méthodologique : les mises à jour supervisées, elles, restent shard-local.
4. Le coordinateur unique est `rho = softmax(rho_logits)`. Toutes les cinq époques, les logits des probes sont calculés sans gradient sur le train. Pour chaque ligne, la probe propriétaire de son shard est masquée ; les six autres sont renormalisées. Seuls les paramètres `rho_logits` reçoivent le gradient de cette loss de coordination.
5. La sélection du checkpoint se fait sur log-loss de validation : `min_delta=0,0005`, patience 20, LR divisé par deux après 7 et 14 époques stagnantes, plafond de sécurité 300 époques.

## Inférence

Les sept probes sont toutes exécutées sur chaque exemple. Leurs logits sont combinés par le même `rho` global. Il n'y a ni early-exit, ni activation conditionnelle, ni sélection de probes à l'exécution. Le gate est global au modèle, pas une fonction des entrées de l'exemple.

## Comptage

- `P_train=1 281` paramètres entraînables, y compris les sept logits du coordinateur.
- `P_gate=7` paramètres du coordinateur externe, inclus dans `P_train` (ne pas les ajouter une seconde fois).
- `P_preprocessor=60` coefficients de StandardScaler (30 moyennes + 30 échelles).
- `P_total=1 341` paramètres persistants déployés.
- `P_fixed_and_buffers_in_model=0`, `P_extra_fixed=0` selon le comptage du script hérité ; aucun modèle dormant n'est préalloué.
- Les checkpoints incluent le scaler. Les poids et sorties sont float32.

## Différences structurales

| Propriété | Orchestra Org historique | V003 |
|---|---:|---:|
| Couches | 7 | 7 experts indépendants |
| Probes par couche | 5 | 1 |
| Probes totales | 35 | 7 |
| Coordinateurs internes | 7 | 0 |
| Coordinateur externe | 1 | 1 |
| Cascade | oui | non |
| Entrée de chaque expert | X et état/cascade selon la couche | même X standardisé |
| Activation conditionnelle | non | non |

La V003 est donc une simplification de topologie et de capacité, pas encore une architecture sparse au runtime. Les sept branches restent évaluées à chaque prédiction.
