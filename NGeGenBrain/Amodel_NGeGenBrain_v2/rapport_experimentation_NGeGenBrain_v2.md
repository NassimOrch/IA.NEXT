# Rapport d’expériences officiel — NGeGenBrain_v2

- Date UTC : `2026-10-27T15:33:59Z`
- Environnement : `Linux-6.18.55-x86_64-with-glibc2.41` / Python `3.13.5`
- Intégrité des registres : **VALIDE**

## 1. Reconstruction synthétique aveugle

- Benchmark : `SYNTH-PARITY-4`
- Classe d’hypothèses : affine booléenne / XOR
- Lignes découverte : 12
- Lignes holdout : 4
- Exactitude holdout : 1.0
- Exactitude sur la table complète observée : 1.0
- Domaine exhaustif : `True`
- Reconstruction : `VALIDATED_ON_SUPPLIED_HOLDOUT`

Interprétation : le candidat a reproduit la fonction binaire étudiée sur les 16 entrées observées, dont 4 réservées au holdout. Cela valide ce cas fonctionnel borné uniquement. Cela n’établit ni l’équivalence causale du réseau, ni la reconstruction de ses poids, ni la reconstruction d’un LLM.

## 2. Échelle de modèles synthétiques

Le banc de test a exercé huit niveaux de modèles synthétiques : fonction linéaire, parité logique, interactions, représentations distribuées, voies concurrentes, composition hiérarchique, mini-Transformer encodeur et mini-modèle causal génératif. Pour chaque niveau, le moteur a exécuté une requête boîte noire et une capture/intervention sur le modèle instrumentable. Le modèle causal a aussi généré des tokens. Ce sont des tests de l’infrastructure d’observation/instrumentation ; seul le cas parité 4 bits ci-dessus est une reconstruction fonctionnelle aveugle évaluée.

## 3. Intervention causale instrumentée

- Hypothèse enregistrée avant test : `HYP-a41ec984b018`
- Expérience : `EXP-c98bcb46b7a9`
- Cible : `xor_layers.0.positive`
- Intervention : `zero` sur l’entrée `[1,0,0,0]`
- Delta L2 observé : `2.0`
- Statut de l’hypothèse après le test : `SUPPORTEE`

Ce résultat soutient uniquement l’effet local prédit dans cette configuration ; d’autres entrées, contrôles et interventions sont nécessaires pour identifier une fonction générale.

## 4. Balayage causal et contrôle négatif

- Entrées balayées : `8`
- Effets comparables : `8`
- Effets non nuls : `2`
- Minimum / maximum du delta L2 : `0.0` / `2.0`

Le balayage inclut des cas avec effet nul et des cas avec effet non nul. Il ne représente que les huit entrées prédéfinies et ne justifie pas une généralisation à toutes les entrées.

## 5. Contrôle adversarial par contre-exemples

- Candidat volontairement incomplet : `{'features': [0, 1], 'bias': 0, 'complexity': 2}`
- Lignes évaluées : `8`
- Contre-exemples détectés : `4`

Ce contrôle positif confirme que le chemin de détection peut signaler un candidat insuffisant sur les observations fournies ; il ne mesure pas la couverture des contre-exemples hors échantillon.

## 6. Découverte numérique

- Classe : `numeric_expression_grammar_v1`
- Statut : `CANDIDATE_FOUND`
- Candidat : `{"op": "add", "args": [{"op": "var", "index": 0}, {"op": "var", "index": 1}]}`
- Validation indépendante : `{"evaluated": true, "count": 3, "correct": 3, "accuracy": 1.0, "errors": [], "tolerance": 1e-09}`

## 7. Composition déclarative

- Sortie : `{"y": 1}`

## 8. Périmètre non exécuté

Aucun modèle LLM externe n’a été chargé ; l’adapter Hugging Face n’a pas été exercé sur des poids réels, car `transformers` et un checkpoint local n’étaient pas disponibles. Cette absence d’expérience n’est ni une preuve de réussite, ni une preuve d’échec du protocole sur les LLM.
## 9. Reconstruction d’un Transformer causal synthétique entraîné

- Statut découverte-règle : `VALIDATED_GREEDY_BEHAVIOR_ON_HELDOUT_AND_COMPOSED_TRAJECTORIES`
- Contextes train/holdout : `20` / `5`
- Exactitude holdout : `1.0`
- Concordance des trajectoires générées après composition : `1.0`
- Reconstruction table/logits : `VALIDATED_ON_QUERIED_FINITE_CONTEXT_DOMAIN_AND_COMPOSED_TRAJECTORIES`
- Concordance exacte des logits observés : `1.0`
- Concordance des générations composées : `1.0`

Portée : le système a produit deux implémentations indépendantes à partir des sorties d’un minuscule Transformer causal synthétique dont l’inspection interne était désactivée : un modèle par règle découvert sur les contextes de découverte et validé sur des contextes réservés, ainsi qu’un modèle de table reproduisant exactement les logits des contextes interrogés et leurs trajectoires composées. Ce résultat n’établit pas l’équivalence des circuits internes et ne se généralise pas automatiquement à un LLM de taille réelle.


## 10. Recherche de prochain-token sur vocabulaire large

Les tests de contrat de la recherche affine modulaire utilisent un jeu synthétique à vocabulaire `V = 32 000`, avec huit contextes d'entraînement. Dans la classe explicitement déclarée `small_coefficient_modular_affine_v1`, le moteur trouve une candidate unique de coefficients `(previous=0, current=1, bias=1)` et vérifie les huit lignes d'entraînement. La classe examine neuf paires de coefficients `(a,b) ∈ {-1,0,1}²`, puis calcule les biais compatibles ; la complexité annoncée est `O(9*n)` pour cette classe, pas pour toutes les fonctions possibles. Un autre test vérifie la sélection automatique de cette stratégie pour `V=257` et la généralisation sur les observations réservées. Ces résultats sont des tests synthétiques de l'algorithme, pas une expérience sur les poids d'un LLM réel.
