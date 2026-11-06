# EX10 v011 — rapport final des expériences

## Statut et périmètre

- Variantes 1 et 2 : réplication v010 Wisconsin exacte (B10/B11/A0) avec scripts/hyperparamètres/graines et splits EX8 v010 ; SMS réel secondaire, déjà historiquement exposé.
- Variante 3 : campagnes complètes CNG/CNC ; 460 runs CNG (candidats, MLP appariés, ablations) + 90 runs CNC (sondes individuelles, C1/C2/C3).
- 1 695 évaluations one-shot sur les partitions test, extrapolation, frontière et décalage de graphe ; modèles gelés avant ouverture.
- Aucun résultat n’a servi à modifier ou sélectionner les modèles après le scoring test.

## Variante 1/2 — classification (EX8 v010)

Wisconsin : B10 0.041390 (5/5 contre MLP apparié et GE4X), B11 0.044425 (5/5 et 5/5), A0 0.043068 (3/5 et 3/5). SMS : B10 0.100201, B11 0.103492, A0 0.106820 ; les trois perdent 0/5 face aux MLP appariés et GE4X. SMS est déjà exposé historiquement.

Le détail par graine est dans `CLASSIFICATION_REPRODUCTION_EX8_V010.md` et les CSV `CLASSIFICATION_REPRODUCTION_PER_SEED.csv` / `CLASSIFICATION_REPRODUCTION_SUMMARY.csv`.

## Variante 3 — CNG

CNG couvre les quatre tâches : sin(x), x1*x2, x1^2+x2, sin(x1*x2)+x3 ; cinq graines par tâche. Modèles G1 single, G2 moyenne M=2/4/7, G3 composition apprise M=1/2/4/7 ; chaque candidat possède un MLP apparié en paramètres. G3/M7 comprend sept ablations leave-one-probe-out. D=4, K=8, centres et largeurs par centre apprenables, KMeans entraînement uniquement, Adam, batch 64, 500 époques max, patience 30.

460 runs CNG ont été validés. Holdout rows: 1380. Le tableau complet de comparaison candidat/MLP est `CNG_CANDIDATE_VS_MLP_SUMMARY.csv`; les ablations LOO sont `CNG_LEAVE_ONE_PROBE_OUT_SUMMARY.csv`.

| Fonction | Split | Candidate | MAE candidate | MAE MLP | Wins/5 |
|---|---|---|---:|---:|---:|
| f1_sin | boundary | G1_SINGLE | 0.039166 | 0.0154401 | 0/5 |
| f1_sin | boundary | G2_MEAN_M2 | 0.027285 | 0.00885977 | 0/5 |
| f1_sin | boundary | G2_MEAN_M4 | 0.0254876 | 0.0070929 | 0/5 |
| f1_sin | boundary | G2_MEAN_M7 | 0.0276347 | 0.00631233 | 0/5 |
| f1_sin | boundary | G3_LEARNED_M1 | 0.0391723 | 0.0190824 | 0/5 |
| f1_sin | boundary | G3_LEARNED_M2 | 0.0228228 | 0.0119504 | 0/5 |
| f1_sin | boundary | G3_LEARNED_M4 | 0.015346 | 0.00691956 | 0/5 |
| f1_sin | boundary | G3_LEARNED_M7 | 0.0114718 | 0.00594116 | 0/5 |
| f1_sin | extrapolation | G1_SINGLE | 0.652332 | 0.375098 | 0/5 |
| f1_sin | extrapolation | G2_MEAN_M2 | 0.649991 | 0.479617 | 0/5 |
| f1_sin | extrapolation | G2_MEAN_M4 | 0.642778 | 0.592162 | 0/5 |
| f1_sin | extrapolation | G2_MEAN_M7 | 0.648546 | 0.649458 | 3/5 |
| f1_sin | extrapolation | G3_LEARNED_M1 | 0.618357 | 0.332698 | 0/5 |
| f1_sin | extrapolation | G3_LEARNED_M2 | 0.592607 | 0.453099 | 1/5 |
| f1_sin | extrapolation | G3_LEARNED_M4 | 0.567753 | 0.582193 | 2/5 |
| f1_sin | extrapolation | G3_LEARNED_M7 | 0.546621 | 0.640393 | 5/5 |
| f1_sin | test | G1_SINGLE | 0.0134553 | 0.00854823 | 1/5 |
| f1_sin | test | G2_MEAN_M2 | 0.00633295 | 0.00544552 | 0/5 |
| f1_sin | test | G2_MEAN_M4 | 0.00467526 | 0.00448945 | 2/5 |
| f1_sin | test | G2_MEAN_M7 | 0.004911 | 0.00430206 | 2/5 |
| f1_sin | test | G3_LEARNED_M1 | 0.0145011 | 0.0109586 | 2/5 |
| f1_sin | test | G3_LEARNED_M2 | 0.00607423 | 0.00711106 | 4/5 |
| f1_sin | test | G3_LEARNED_M4 | 0.0035195 | 0.00467682 | 4/5 |
| f1_sin | test | G3_LEARNED_M7 | 0.00257097 | 0.00406595 | 5/5 |
| f2_mul | boundary | G1_SINGLE | 0.531238 | 0.0650249 | 0/5 |
| f2_mul | boundary | G2_MEAN_M2 | 0.0575218 | 0.0478307 | 1/5 |
| f2_mul | boundary | G2_MEAN_M4 | 0.051653 | 0.0434573 | 2/5 |
| f2_mul | boundary | G2_MEAN_M7 | 0.0422445 | 0.0426812 | 2/5 |
| f2_mul | boundary | G3_LEARNED_M1 | 0.517256 | 0.0627259 | 0/5 |
| f2_mul | boundary | G3_LEARNED_M2 | 0.191496 | 0.0477397 | 4/5 |
| f2_mul | boundary | G3_LEARNED_M4 | 0.0223973 | 0.0437913 | 5/5 |
| f2_mul | boundary | G3_LEARNED_M7 | 0.0164976 | 0.0403507 | 5/5 |
| f2_mul | extrapolation | G1_SINGLE | 1.89834 | 0.615233 | 0/5 |
| f2_mul | extrapolation | G2_MEAN_M2 | 0.823281 | 0.500173 | 0/5 |
| f2_mul | extrapolation | G2_MEAN_M4 | 0.889105 | 0.446355 | 0/5 |
| f2_mul | extrapolation | G2_MEAN_M7 | 0.896291 | 0.430837 | 0/5 |
| f2_mul | extrapolation | G3_LEARNED_M1 | 1.6704 | 0.607294 | 0/5 |
| f2_mul | extrapolation | G3_LEARNED_M2 | 0.821787 | 0.501679 | 3/5 |
| f2_mul | extrapolation | G3_LEARNED_M4 | 0.494226 | 0.455295 | 1/5 |
| f2_mul | extrapolation | G3_LEARNED_M7 | 0.474681 | 0.431776 | 0/5 |
| f2_mul | test | G1_SINGLE | 0.315376 | 0.0298749 | 0/5 |
| f2_mul | test | G2_MEAN_M2 | 0.026898 | 0.021028 | 2/5 |
| f2_mul | test | G2_MEAN_M4 | 0.0232762 | 0.021839 | 3/5 |
| f2_mul | test | G2_MEAN_M7 | 0.013455 | 0.0230995 | 5/5 |
| f2_mul | test | G3_LEARNED_M1 | 0.296195 | 0.028269 | 0/5 |
| f2_mul | test | G3_LEARNED_M2 | 0.113705 | 0.0211174 | 3/5 |
| f2_mul | test | G3_LEARNED_M4 | 0.0106879 | 0.0221535 | 5/5 |
| f2_mul | test | G3_LEARNED_M7 | 0.00713849 | 0.021387 | 5/5 |
| f3_square_plus | boundary | G1_SINGLE | 1.45074 | 0.129997 | 0/5 |
| f3_square_plus | boundary | G2_MEAN_M2 | 0.759371 | 0.0809639 | 0/5 |
| f3_square_plus | boundary | G2_MEAN_M4 | 0.22671 | 0.0560941 | 0/5 |
| f3_square_plus | boundary | G2_MEAN_M7 | 0.202749 | 0.0453576 | 0/5 |
| f3_square_plus | boundary | G3_LEARNED_M1 | 0.949223 | 0.12698 | 1/5 |
| f3_square_plus | boundary | G3_LEARNED_M2 | 0.625594 | 0.0797148 | 3/5 |
| f3_square_plus | boundary | G3_LEARNED_M4 | 0.0312129 | 0.0541914 | 5/5 |
| f3_square_plus | boundary | G3_LEARNED_M7 | 0.027143 | 0.0466646 | 4/5 |
| f3_square_plus | extrapolation | G1_SINGLE | 3.51605 | 1.36216 | 0/5 |
| f3_square_plus | extrapolation | G2_MEAN_M2 | 2.57909 | 1.05472 | 0/5 |
| f3_square_plus | extrapolation | G2_MEAN_M4 | 2.23531 | 0.864009 | 0/5 |
| f3_square_plus | extrapolation | G2_MEAN_M7 | 2.21214 | 0.726747 | 0/5 |
| f3_square_plus | extrapolation | G3_LEARNED_M1 | 2.64794 | 1.35486 | 1/5 |
| f3_square_plus | extrapolation | G3_LEARNED_M2 | 1.99948 | 1.05871 | 3/5 |
| f3_square_plus | extrapolation | G3_LEARNED_M4 | 1.01393 | 0.842329 | 1/5 |
| f3_square_plus | extrapolation | G3_LEARNED_M7 | 0.977009 | 0.732991 | 0/5 |
| f3_square_plus | test | G1_SINGLE | 1.07984 | 0.0700639 | 0/5 |
| f3_square_plus | test | G2_MEAN_M2 | 0.535934 | 0.0400714 | 0/5 |
| f3_square_plus | test | G2_MEAN_M4 | 0.106924 | 0.0276772 | 0/5 |
| f3_square_plus | test | G2_MEAN_M7 | 0.0923934 | 0.0210943 | 0/5 |
| f3_square_plus | test | G3_LEARNED_M1 | 0.696803 | 0.067435 | 1/5 |
| f3_square_plus | test | G3_LEARNED_M2 | 0.460953 | 0.040284 | 1/5 |
| f3_square_plus | test | G3_LEARNED_M4 | 0.0143808 | 0.0259309 | 5/5 |
| f3_square_plus | test | G3_LEARNED_M7 | 0.0124899 | 0.0211546 | 4/5 |
| f4_sin_product_plus | boundary | G1_SINGLE | 0.464786 | 0.252067 | 0/5 |
| f4_sin_product_plus | boundary | G2_MEAN_M2 | 0.356414 | 0.167018 | 0/5 |
| f4_sin_product_plus | boundary | G2_MEAN_M4 | 0.231469 | 0.144831 | 0/5 |
| f4_sin_product_plus | boundary | G2_MEAN_M7 | 0.208096 | 0.135887 | 0/5 |
| f4_sin_product_plus | boundary | G3_LEARNED_M1 | 0.463433 | 0.236914 | 0/5 |
| f4_sin_product_plus | boundary | G3_LEARNED_M2 | 0.336324 | 0.167304 | 0/5 |
| f4_sin_product_plus | boundary | G3_LEARNED_M4 | 0.182991 | 0.150662 | 1/5 |
| f4_sin_product_plus | boundary | G3_LEARNED_M7 | 0.125008 | 0.137205 | 3/5 |
| f4_sin_product_plus | extrapolation | G1_SINGLE | 0.859996 | 0.6528 | 0/5 |
| f4_sin_product_plus | extrapolation | G2_MEAN_M2 | 0.817459 | 0.540085 | 0/5 |
| f4_sin_product_plus | extrapolation | G2_MEAN_M4 | 0.682079 | 0.5005 | 0/5 |
| f4_sin_product_plus | extrapolation | G2_MEAN_M7 | 0.682579 | 0.487073 | 0/5 |
| f4_sin_product_plus | extrapolation | G3_LEARNED_M1 | 0.820052 | 0.62074 | 0/5 |
| f4_sin_product_plus | extrapolation | G3_LEARNED_M2 | 0.725167 | 0.528852 | 0/5 |
| f4_sin_product_plus | extrapolation | G3_LEARNED_M4 | 0.535488 | 0.508496 | 1/5 |
| f4_sin_product_plus | extrapolation | G3_LEARNED_M7 | 0.486806 | 0.484403 | 2/5 |
| f4_sin_product_plus | test | G1_SINGLE | 0.388163 | 0.175846 | 0/5 |
| f4_sin_product_plus | test | G2_MEAN_M2 | 0.2602 | 0.12231 | 0/5 |
| f4_sin_product_plus | test | G2_MEAN_M4 | 0.14651 | 0.107668 | 0/5 |
| f4_sin_product_plus | test | G2_MEAN_M7 | 0.127587 | 0.104431 | 1/5 |
| f4_sin_product_plus | test | G3_LEARNED_M1 | 0.38168 | 0.164096 | 0/5 |
| f4_sin_product_plus | test | G3_LEARNED_M2 | 0.254646 | 0.121394 | 0/5 |
| f4_sin_product_plus | test | G3_LEARNED_M4 | 0.124435 | 0.11199 | 1/5 |
| f4_sin_product_plus | test | G3_LEARNED_M7 | 0.0857974 | 0.105238 | 3/5 |

## Variante 3 — CNC sondes élémentaires

Six opérateurs (ADD/SUB/MUL/DIV/EXP/LOG), cinq graines chacun. Paramètres D=4/K=8, centres et largeurs par centre apprenables ; KMeans train-only ; Adam 1e-3, batch 64, maximum 500 époques, patience 30. Test, frontière et extrapolation opérationnelle sont séparés.

| Opération | Split | MAE moyenne | RMSE moyen |
|---|---|---:|---:|
| ADD | boundary | 0.0337026 | 0.068813 |
| ADD | operation_extrapolation | 0.249259 | 0.52701 |
| ADD | test | 0.0167768 | 0.0250002 |
| DIV | boundary | 1.11291 | 1.73485 |
| DIV | operation_extrapolation | 0.499231 | 0.96946 |
| DIV | test | 0.262589 | 0.492961 |
| EXP | boundary | 0.148228 | 0.174482 |
| EXP | operation_extrapolation | 3.67244 | 6.17828 |
| EXP | test | 0.0213267 | 0.0294782 |
| LOG | boundary | 0.0913133 | 0.117587 |
| LOG | operation_extrapolation | 0.700291 | 0.891568 |
| LOG | test | 0.00651557 | 0.00992323 |
| MUL | boundary | 0.566759 | 0.788765 |
| MUL | operation_extrapolation | 1.9916 | 2.56228 |
| MUL | test | 0.374903 | 0.513696 |
| SUB | boundary | 0.0328122 | 0.0705951 |
| SUB | operation_extrapolation | 0.245456 | 0.524993 |
| SUB | test | 0.0200283 | 0.0368425 |

## Variante 3 — graphes CNC : compositions

C1 : sondes opérationnelles individuelles de la même graine, gelées, sans entraînement du graphe. C2 : initialisation par les mêmes checkpoints d’opération et fine-tuning conjoint sur le jeu train du graphe. C3 : MLP direct apparié au nombre de paramètres uniques du sous-graphe, et CoreProbe/AdaptiveRBF direct. Le baseline native exact calcule l’oracle arithmétique sans apprentissage (non comparable comme modèle appris). Les erreurs par noeud intermédiaire sont sauvegardées et contrôlées.

| Graphe | Split | Variante | MAE moyenne | RMSE moyen |
|---|---|---|---:|---:|
| G1_ab_plus_exp | boundary | C1_FROZEN | 0.525656 | 0.554555 |
| G1_ab_plus_exp | boundary | C2_JOINT | 0.0868086 | 0.113959 |
| G1_ab_plus_exp | boundary | C3_DIRECT_MLP | 0.0227495 | 0.0376481 |
| G1_ab_plus_exp | boundary | C3_DIRECT_RBF | 0.147373 | 0.19091 |
| G1_ab_plus_exp | boundary | NATIVE_EXACT | 0 | 0 |
| G1_ab_plus_exp | graph_domain_shift | C1_FROZEN | 0.376625 | 0.435306 |
| G1_ab_plus_exp | graph_domain_shift | C2_JOINT | 0.183148 | 0.274871 |
| G1_ab_plus_exp | graph_domain_shift | C3_DIRECT_MLP | 0.062745 | 0.120023 |
| G1_ab_plus_exp | graph_domain_shift | C3_DIRECT_RBF | 0.295394 | 0.419756 |
| G1_ab_plus_exp | graph_domain_shift | NATIVE_EXACT | 0 | 0 |
| G1_ab_plus_exp | test | C1_FROZEN | 0.536045 | 0.56087 |
| G1_ab_plus_exp | test | C2_JOINT | 0.0821666 | 0.108634 |
| G1_ab_plus_exp | test | C3_DIRECT_MLP | 0.0161133 | 0.0219165 |
| G1_ab_plus_exp | test | C3_DIRECT_RBF | 0.132373 | 0.172796 |
| G1_ab_plus_exp | test | NATIVE_EXACT | 2.16255e-08 | 3.60518e-08 |
| G2_ab_over_c_plus_1 | boundary | C1_FROZEN | 0.699419 | 0.892707 |
| G2_ab_over_c_plus_1 | boundary | C2_JOINT | 0.129815 | 0.192794 |
| G2_ab_over_c_plus_1 | boundary | C3_DIRECT_MLP | 0.0544121 | 0.106946 |
| G2_ab_over_c_plus_1 | boundary | C3_DIRECT_RBF | 0.115187 | 0.186652 |
| G2_ab_over_c_plus_1 | graph_domain_shift | C1_FROZEN | 0.483708 | 0.663022 |
| G2_ab_over_c_plus_1 | graph_domain_shift | C2_JOINT | 0.242068 | 0.430113 |
| G2_ab_over_c_plus_1 | graph_domain_shift | C3_DIRECT_MLP | 0.146186 | 0.336636 |
| G2_ab_over_c_plus_1 | graph_domain_shift | C3_DIRECT_RBF | 0.255456 | 0.508249 |
| G2_ab_over_c_plus_1 | test | C1_FROZEN | 0.493429 | 0.591204 |
| G2_ab_over_c_plus_1 | test | C2_JOINT | 0.0862103 | 0.116193 |
| G2_ab_over_c_plus_1 | test | C3_DIRECT_MLP | 0.0246943 | 0.0428663 |
| G2_ab_over_c_plus_1 | test | C3_DIRECT_RBF | 0.0726878 | 0.111032 |
| G3_log_squares_plus_exp | boundary | C1_FROZEN | 0.607038 | 0.638386 |
| G3_log_squares_plus_exp | boundary | C2_JOINT | 0.0333986 | 0.0380017 |
| G3_log_squares_plus_exp | boundary | C3_DIRECT_MLP | 0.0501118 | 0.0676963 |
| G3_log_squares_plus_exp | boundary | C3_DIRECT_RBF | 0.145453 | 0.158541 |
| G3_log_squares_plus_exp | boundary | NATIVE_EXACT | 0 | 0 |
| G3_log_squares_plus_exp | graph_domain_shift | C1_FROZEN | 0.663438 | 0.766761 |
| G3_log_squares_plus_exp | graph_domain_shift | C2_JOINT | 0.266361 | 0.370657 |
| G3_log_squares_plus_exp | graph_domain_shift | C3_DIRECT_MLP | 0.0720344 | 0.12331 |
| G3_log_squares_plus_exp | graph_domain_shift | C3_DIRECT_RBF | 0.348494 | 0.415825 |
| G3_log_squares_plus_exp | graph_domain_shift | NATIVE_EXACT | 0 | 0 |
| G3_log_squares_plus_exp | test | C1_FROZEN | 0.515519 | 0.536178 |
| G3_log_squares_plus_exp | test | C2_JOINT | 0.0202079 | 0.0244269 |
| G3_log_squares_plus_exp | test | C3_DIRECT_MLP | 0.00962999 | 0.0129681 |
| G3_log_squares_plus_exp | test | C3_DIRECT_RBF | 0.0739963 | 0.088866 |
| G3_log_squares_plus_exp | test | NATIVE_EXACT | 3.44162e-08 | 4.73784e-08 |

## Ressources et temps

L’inférence a été profilée séquentiellement sur CPU (1 thread), avec cinq warmups et vingt répétitions, batch 1 et 64, pour les 550 checkpoints. Les mesures par modèle sont dans `CORE_SEQUENTIAL_INFERENCE_PROFILE.csv`. Les durées de fit/RSS sont conservées avec leur statut individuel : 370/550 lignes `RECORDED_NO_OVERLAP_DETECTED` et 180/550 `CONTENDED_OR_UNVERIFIED`. Les 180 lignes contended/unverified ne servent à aucune comparaison ; les 370 lignes sans chevauchement détecté restent descriptives et ne constituent pas une preuve de vitesse générale. Le profilage d’inférence séquentiel est mesuré séparément. Aucun compteur d’énergie ni compteur FLOPs/MAC matériel instrumenté fiable n’a été obtenu ; les MAC/RBF affichés sont des estimations structurelles. Le nombre de paramètres et les latences mesurées ne remplacent pas ces mesures.

## Contrôles anti-triche et intégrité

- 550/550 runs (460 CNG + 90 CNC) reconstruisent leurs prédictions de validation depuis checkpoints ;
- 65 jeux train/validation et les splits train 630 / validation 135 / test 135 par tâche ;
- 80 frontières, 30 extrapolations d’opérations et 20 extrapolations CNG contrôlées avant ouverture ;
- verrou pré-test : 550 modèles, 195 fichiers holdout opaques, 3 037 empreintes ;
- scoring holdout one-shot : 1 695 enregistrements, marqueur `COMPLETE`, aucun entraînement ni sélection ;
- audit post-test : 1 695/1 695 prédictions et métriques recalculées avec delta maximal 0 ; 90/90 fichiers de noeuds ; 3 037/3 037 hashes ;
- les holdouts sources n’ont pas été rouverts par l’auditeur post-test ;
- six tests unitaires invariants ; audit final : suite d’invariants 6/6 PASS, intégrité des artefacts de classification et des profils ressources PASS, CRC de l’archive de livraison contrôlé au packaging.

## Limites explicites

SMS est un domaine réel mais historiquement exposé, et Wisconsin demeure une partition de développement déjà utilisée. Les jeux CNG/CNC sont synthétiques et évaluent la capacité à apprendre des fonctions opératoires et leurs compositions, pas la généralisation vers un corpus réel. Les tests et stress tests ont été ouverts seulement après gel des 550 modèles ; leurs résultats restent descriptifs et ne servent pas à une nouvelle sélection. Le profilage est CPU et ne fournit pas de consommation énergétique ; les chronométrages d’entraînement sont non comparables en raison de la concurrence CPU.

