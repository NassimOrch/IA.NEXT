# Rapport exécutif EX5 — 30 octobre 2026

## Décision

**EX5 a exécuté ses principaux bras expérimentaux, mais l'objectif scientifique final n'est pas atteint.** Plusieurs architectures ont une capacité inférieure au MLP de comparaison et toutes les candidates intéressantes ont des compromis qui empêchent de satisfaire simultanément la précision, la log-loss et les ressources. La règle rouge n'est donc pas passée.

## Ce qui a été expérimenté

- RETRO : 12 calendriers/contrôles, cinq graines par candidat ; 61 lignes brutes dont une duplication candidate/seed conservée et signalée, soit 60 couples uniques.
- Optimiseurs : 25 entraînements (Adam keep/no-freeze/rebuild/reset, AdamW), dont 20 phases gelées contrôlées bitwise.
- Proportion fixe/adaptative : A4/F0, A3/F1, A2/F2, A1/F3, A0/F4, cinq graines ; budget constant 788 paramètres totaux pour ce balayage.
- Portes et géométries : portes globales/conditionnelles conjointes ou gelées ; cinq géométries égal-gate et cinq gate×géométrie.
- Alternance A↔B : cinq ablations initiales, puis variante stricte sur cinq graines avec deux cycles complets sans amélioration avant arrêt.
- Deux niveaux question→réponse : hybride/hybride, fixe→adaptatif, adaptatif→fixe ; contrôle question-only X, réponse supervisée Y-cible ; plus résidu OOF adaptatif et fixe.
- Généralisation : Wine et Digits, nouveaux splits à indices test aveugles aux labels et features, gel pré-test puis évaluation descriptive.

## Candidats de développement

Le meilleur bras micro-MIXA simple selon la log-loss de validation est `A3_F1_d4_k4_input_gate` : `P_total=800`, accuracy moyenne 0,97412 et log-loss 0,06187. Son MLP ge4x compte 3 230 paramètres (4,0375×), accuracy 0,98588 et log-loss 0,05076. Le temps d'entraînement moyen est 0,583 s contre 0,297 s ; latence médiane batch 1 ≈0,168 ms contre 0,0139 ms. Le modèle sonde est plus petit sur disque de déploiement (11 989 contre 15 965 octets), mais perd sur qualité et latence.

Le correcteur résiduel OOF adaptatif obtient une log-loss de validation de 0,05218 pour 1 160 paramètres, proche mais encore supérieure au MLP ge4x (0,05037 ; 4 649 paramètres, ratio minimum 4,0078×). Accuracy : 0,97647 contre 0,98588 ; latence batch 1 ≈0,341 ms contre 0,0166 ms ; durée totale ≈2,138 s contre 0,268 s.

## Hiérarchie question/réponse

Après harmonisation du seed 1501 selon le critère Q-only relatif, `ADAPTIVE_THEN_FIXED` donne accuracy 0,98118, log-loss 0,06914 pour 262 paramètres. Son MLP ge4x donne 0,97882 et 0,05291, avec latence ≈0,0148 ms contre 0,0584 ms pour la sonde. `HYBRID_HYBRID` : 0,97412 / 0,05881, MLP ge4x 0,97647 / 0,05280. `FIXED_THEN_ADAPTIVE` est très instable (0,85412 / 0,31111).

## Tests et généralisation

Les nouveaux splits Wine (36 cas test) et Digits (360 cas test) ont été créés sans consulter les valeurs X/Y test au moment du choix des indices. Le manifeste `FROZEN_BEFORE_TEST_FEATURE_OR_LABEL_ACCESS` confirme le gel des checkpoints et prédictions de validation avant accès test. Les cinq graines utilisent le même jeu test : ce ne sont pas cinq échantillons indépendants. Wine gate input a une log-loss moyenne test 0,02373 contre 0,02523 pour son MLP ge4x, mais accuracy 0,99444 contre 1,0 et latence environ neuf fois plus élevée ; cette petite différence sur 36 cas n'établit pas une non-infériorité. Sur Digits, MLP ge4x domine nettement.

## Conformité et limites

Le ratio paramétrique ge4x est respecté pour toutes les comparaisons listées dans le registre : minimum global 4,000735×. Les hashes de 532 références checkpoint et 495 références canoniques de prédiction passent ; 1 148 JSON et 32 JSONL (829 lignes) se parsèrent ; les métriques recalculées concordent. Les 36 pointeurs v3 historiques non uniques sont conservés et remplacés par les sidecars corrigés, sans altérer le registre d'origine.

Les limites qui empêchent de déclarer EX5 achevé au sens strict : marges de non-infériorité non pré-enregistrées, pas de CIs/bootstrap appariés ni matrices de confusion publiées, MACs d'entraînement non mesurés, énergie absente, VRAM indisponible CPU, RSS non isolé pour toutes les mesures, Banknote et MAGIC non téléchargés (DNS `Could not resolve host`). Les candidats ne satisfont pas la règle rouge sur les mesures disponibles.
