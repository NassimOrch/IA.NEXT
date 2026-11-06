# Protocole EX7, graines et conventions de comparaison

## Statut du document

Le prompt `prompt_ex7.json` constitue le protocole directeur de la campagne. Il conserve le prompt EX6 et ajoute le plan EX7. Ce rapport est une transcription et une clarification du protocole effectivement appliqué ; il ne prétend pas être un pré-enregistrement statistique indépendant, horodaté auprès d'un tiers. Les variantes structurelles et de capacité ont été ajoutées après les premiers résultats et doivent être considérées comme des explorations de développement dont les configurations exactes sont dans les scripts et résultats bruts.

## Question principale

Transformer la compacité des systèmes Emplica OOF / Orchestra OOF en gains observables de calcul, de latence ou de ressources, sans perte prédictive matériellement importante. Les références EX6 restent les références historiques gelées : Emplica OOF (8 295 paramètres, accuracy 98,59 %, log-loss 0,03637) ; Orchestra OOF (8 512 paramètres, accuracy 98,12 %, log-loss 0,03982).

## Données et séparation

- Jeu utilisé : Wisconsin historique, split de développement EX6 uniquement.
- Train / validation : artefacts et identifiants conservés dans `inputs/ex6_reference/`.
- Graines principales : `1501, 1607, 1717, 2029, 3037`.
- Aucun test vierge externe accepté ni ouvert.
- La validation historique est un split de développement ; aucune métrique de la campagne ne constitue une confirmation externe.

## Règles OOF / arrêt

- Référence EX6 : 3 folds stratifiés avec split interne (20 %) de chaque train-fold pour early stopping.
- Nouveaux 2-fold et 5-fold : les folds externes sont strictement séparés ; un split interne dans les exemples du train-fold choisit l'époque ; le modèle prédit ensuite le fold externe tenu à l'écart. Chaque exemple de train reçoit une prédiction hors-fold, jamais in-sample.
- Arrêt utilisé dans les bras concernés : `min_delta=5e-4`, `patience=20`, sauf contrôle historique explicitement repris.
- Orchestra Org : 7 couches × 5 probes pour le modèle principal ; mises à jour de coordination toutes les cinq époques ; adaptation interne `pi_l=softmax(phi_l)`, adaptation externe `rho=softmax(Psi)`, objectifs de coordination sur sorties détachées et optimiseurs séparés.
- La modulation `eta0*(0.5+N*pi)*(0.5+L*rho)` pour N=5 et L=7 est une généralisation EX7 de la formule de la source N=4, pas une formule déjà validée empiriquement par la source.

## Marges de qualité de développement

Convention descriptive : baisse d'accuracy maximale de 0,5 point de pourcentage et augmentation relative de log-loss au plus 5 %, examinées par graine et sur l'agrégat. Ces marges ne sont pas une preuve statistique de non-infériorité populationnelle. Une moyenne acceptable ne masque pas une graine fortement dégradée.

## Mesures

Accuracy, macro-F1, balanced accuracy, log-loss, Brier, ECE, ROC-AUC si calculable ; paramètres entraînables, buffers/fixes, préprocesseur, paramètres totaux et taille de checkpoint ; temps base, OOF, correcteur et pipeline ; batchs 1/16/64/256, p50/p95/p99 et débit ; mesures d'opérateurs par profiler avec limites documentées. Energie, DRAM, mémoire activations et peak RSS isolé sont `NON MESURÉS` lorsqu'une mesure fiable n'est pas disponible.

## Ordre de sélection

Aucune sélection n'a utilisé un test externe. Les résultats par graines, checkpoints et métriques sont conservés. Les variants 2-fold/5-fold sont des conceptions différentes de 3-fold ; leur vitesse n'est jamais présentée comme équivalente à l'OOF de référence sans examiner la qualité. Les mesures de latence non appariées (durées de répétition différentes) sont descriptives uniquement.
