# Filiation technique micro-MIXA → OOF → Emplica / Orchestra OOF → EX7

## Chaîne de conception

1. **micro-MIXA** : famille compacte de probes RBF avec mélange local/global et adaptation paramétrique. Implémentation source clé : `inputs/ex6_reference/src/ex6_mixa_engine.py` ; modules partagés dans `ex6_common.py`.
2. **OOF** : cross-fitting pour produire, pour chaque exemple d'entraînement, un logit de base émis par un modèle qui n'a pas vu cet exemple. En EX6, 3 folds stratifiés ; chaque modèle de fold utilise un split interne train/early-stop, puis prédit le fold retenu. Le modèle complet est entraîné sur tout le train et le correcteur est ajusté sur `(X_train, logits_OOF_train)` ; validation utilise `(X_val, logits_base_full_val)`.
3. **Emplica OOF** : stack de couches Emplica avec correcteur résiduel OOF. La variante de référence EX6 a 8 295 paramètres, 98,59 % accuracy et log-loss 0,03637 sur cinq graines.
4. **Orchestra OOF** : stack de couches avec coordination globale externe conditionnée par l'entrée et correcteur OOF. Référence : 8 512 paramètres, 98,12 % accuracy, log-loss 0,03982.
5. **EX7** : conserver la sémantique OOF ; réduire le nombre de folds et la complexité correcteur ; profiler calcul/latence ; implémenter en plus la version originale récursive Orchestra Org décrite par les sources.

## Source de globalité consultée

Le formalisme source décrit `pi_i = softmax(phi_i)` sur les probes, une mise à jour du coordinateur sur l'objectif global à partir de sorties locales détachées, une modulation des taux locaux et une mise à jour périodique (toutes les cinq époques dans le protocole source). La formule historique pour N=4 est `eta_i = eta0*(0.5+2*pi_i)`. EX7 teste explicitement l'extension généralisée `eta0*(0.5+N*pi_i)` pour N=5, et l'extension externe `eta0*(0.5+L*rho_l)` pour L=7 ; ces généralisations sont des extensions, pas des résultats déjà validés par la source.

## Implémentation originale Orchestra Org

`src/run_orchestra_org_recursive.py` : chaque couche agrège 5 probes avec un coordinateur interne `softmax(phi_l)` ; les couches sont coordonnées par un coordinateur externe `softmax(Psi)` ; les objectifs des coordinateurs utilisent des sorties détachées et des labels train autorisés ; les optimiseurs locaux sont séparés par probe ; les taux locaux sont modulés par les poids internes et externes. La variante principale est en cascade, et l'ablation indépendante coupe la communication inter-couches tout en conservant les deux niveaux de coordination.

Ce n'est pas l'ancien gate externe conditionné à l'entrée : il s'agit bien de deux niveaux de coordination adaptative récursive. La dénomination « Org » signale la topologie originale; le coordinateur est centralisé, non fédéré ou privé.

## Flux de calculs

```text
X_train
  └─ shards stratifiés par couche/probe
       └─ probes locales q_lj
            └─ coordinateur interne pi_l = softmax(phi_l)
                 └─ sortie de couche h_l
                      └─ coordinateur externe rho = softmax(Psi)
                           └─ logit global z
                                └─ objectif global / update périodique

OOF : répétition du fit du modèle de base sur les folds autorisés
  └─ logits out-of-fold des seules observations train
       └─ correcteur compact appris sur X_train + logits_OOF_train
```
