# Analyse comparative et limites — résultats observés

## 1. Conclusion scientifique principale

Les résultats soutiennent une affirmation locale : une sonde RBF paramétrique et adaptative peut apprendre les quatre tâches de classification étudiées ; une sonde RBF entraînée sur des observations entrée-sortie peut approximer certaines fonctions de neurones artificiels simples en distribution ; des sondes ainsi apprises peuvent remplacer des composants cachés dans une composition tout en changeant mesurablement les sorties du réseau.

Ils ne démontrent pas qu'un neurone quelconque est universellement un cas particulier de sonde, qu'une sonde peut toujours retrouver le mécanisme interne d'un neurone, ni qu'une collection de sondes compose nécessairement un modèle autonome équivalent. Les résultats sont compatibles avec l'approximation fonctionnelle sous une classe et un budget précis.

## 2. Classification : tâche apprise par la sonde

Moyennes sur trois partitions/graines, exactitude (%) :

| Tâche | RBF fixe | RBF adaptative A | Taux d'adaptation B méta-appris | MLP référence |
|---|---:|---:|---:|---:|
| Deux lunes | 85,37 ± 1,16 | 93,61 ± 0,56 | 95,74 ± 0,58 | 90,74 ± 2,52 |
| Cercles | 90,56 ± 1,11 | 94,35 ± 0,89 | 94,72 ± 1,11 | 94,44 ± 1,21 |
| Produit/XOR bruité | 91,85 ± 1,85 | 94,17 ± 0,48 | 93,80 ± 1,12 | 94,26 ± 0,42 |
| Cancer du sein (benchmark public) | 91,81 ± 1,34 | 96,49 ± 1,52 | 98,25 ± 0,88 | 97,95 ± 1,01 |

A est compétitive dans toutes les tâches. B obtient l'exactitude moyenne la plus élevée sur deux lunes, cercles et le benchmark public, mais n'est pas meilleure sur le produit/XOR. B reçoit 700 époques finales contre 220 pour A/MLP/contrôle dans l'analyse primaire. L'analyse secondaire où toutes les méthodes ont 700 époques finales montre que l'écart A/B est beaucoup plus petit ; B supporte toujours en plus 35 étapes de méta-ajustement. Les résultats ne justifient donc pas d'attribuer tout l'écart principal au méta-apprentissage.

Le contrôle fixe n'a que 17 paramètres entraînables, contre 65 en dimension 2 et 513 sur 30 variables. Son infériorité ne mesure donc pas isolément l'effet de l'adaptation : capacité et adaptativité varient ensemble.

## 3. Sonde imitant un neurone isolé

Neuf neurones cibles boîte noire (trois par famille tanh/ReLU/sigmoïde) ont été interrogés avec 64, 256 ou 1024 paires d'entrée-sortie. Le test IID contient 4000 entrées nouvelles par cible. Les moyennes sont calculées en moyennant d'abord les trois initialisations de sonde par cible, puis les trois cibles indépendantes par famille.

| Famille cible | Paires observées | MAE | RMSE | R² |
|---|---:|---:|---:|---:|
| tanh | 64 | 0,0482 ± 0,0312 | 0,0718 ± 0,0436 | 0,9898 ± 0,0081 |
| tanh | 256 | 0,0382 ± 0,0215 | 0,0501 ± 0,0264 | 0,9951 ± 0,0031 |
| tanh | 1024 | 0,0324 ± 0,0171 | 0,0427 ± 0,0218 | 0,9963 ± 0,0022 |
| ReLU | 64 | 0,0806 ± 0,0281 | 0,1152 ± 0,0290 | 0,9887 ± 0,0031 |
| ReLU | 256 | 0,0715 ± 0,0386 | 0,1015 ± 0,0599 | 0,9926 ± 0,0024 |
| ReLU | 1024 | 0,0676 ± 0,0362 | 0,0929 ± 0,0459 | 0,9936 ± 0,0010 |
| Sigmoïde | 64 | 0,0166 ± 0,0032 | 0,0234 ± 0,0038 | 0,9807 ± 0,0253 |
| Sigmoïde | 256 | 0,0159 ± 0,0043 | 0,0207 ± 0,0042 | 0,9869 ± 0,0161 |
| Sigmoïde | 1024 | 0,0157 ± 0,0047 | 0,0200 ± 0,0052 | 0,9889 ± 0,0127 |

La fidélité IID est élevée sur cette famille, et elle s'améliore généralement avec davantage de données. Toutefois, la cible affine+activation en dimension 2 ne possède que trois paramètres continus, tandis que la sonde RBF à 20 centres en possède 81. La démonstration montre l'approximation par un modèle plus expressif, pas l'identité des représentations ni une efficacité paramétrique équivalente.

### Robustesse hors distribution — analyse exploratoire

Quand les entrées sont translatées de (+1,5, −1,5) sans réentraînement, l'erreur augmente nettement. Avec un budget de 1024 paires, le RMSE passe de 0,0929 à 0,7149 pour ReLU, de 0,0427 à 0,1792 pour tanh, et de 0,0200 à 0,1386 pour la sigmoïde. Une faible erreur IID ne suffit donc pas à soutenir l'extrapolation robuste.

## 4. Composition : remplacement de composants

La version de composition retenue utilise les graines prévues par la correction v1.2 : 411, 522 et 633. Les deux tâches sont deux lunes et le benchmark public du cancer du sein. Le réseau enseignant possède 16 unités cachées. Chaque sonde est ajustée sur des activations observées en train ; les activations de test ne servent qu'à l'évaluation. Le lecteur aval du réseau enseignant reste en place.

| Tâche | Unités remplacées | Exactitude enseignant (%) | Exactitude après (%) | Écart moyen absolu des logits |
|---|---:|---:|---:|---:|
| Deux lunes | 1 | 92,87 ± 2,05 | 92,96 ± 1,89 | 0,016 ± 0,001 |
| Deux lunes | 4 | 92,87 ± 2,05 | 92,41 ± 1,85 | 0,089 ± 0,051 |
| Deux lunes | 16 | 92,87 ± 2,05 | 88,52 ± 1,43 | 0,469 ± 0,164 |
| Cancer du sein | 1 | 97,66 ± 1,01 | 97,95 ± 0,51 | 0,133 ± 0,025 |
| Cancer du sein | 4 | 97,66 ± 1,01 | 98,25 ± 0,88 | 0,454 ± 0,046 |
| Cancer du sein | 16 | 97,66 ± 1,01 | 98,83 ± 1,01 | 1,596 ± 0,042 |

L'exactitude sur le benchmark public augmente dans les résultats obtenus, mais l'écart des logits s'accroît fortement. Le changement de classe peut rester rare même si les valeurs internes divergent considérablement. La fidélité du composant doit donc être évaluée par les sorties et par les conséquences de composition, pas uniquement par l'exactitude finale.

Les sondes de composition ont 49 paramètres chacune en 2D et 257 en 30D ; chaque neurone enseignant possède respectivement 3 ou 31 paramètres d'entrée. Le budget n'est pas comparable. Le lecteur source est conservé, ce qui interdit de présenter l'expérience comme une reconstruction autonome complète.

## 5. Intégrité, correction de protocole et reproductibilité

### Éléments vérifiés

- Zéro hachage de ligne partagée entre train, validation et test pour les partitions auditées (17 907 enregistrements).
- Les signatures des fonctions d'ajustement n'acceptent pas les étiquettes test ni les paramètres de cible ; la fonction d'imitation reçoit les entrées et sorties observées et une graine indépendante de sonde.
- Les neuf cibles, trois budgets et trois initialisations sont présents (81 essais d'imitation).
- Les six chunks de composition v1.2 couvrent exactement deux tâches × graines 411/522/633.
- Le réexécutable deux lunes/graine 411 produit un JSON SHA-256 identique à son résultat précédent. Les relances de classification et d'imitation ont aussi été comparées octet par octet dans le dossier d'audit.
- Les empreintes sont calculées sur les artefacts livrés ; elles n'établissent pas la validité de la méthode en soi.

### Divergence reconnue

L'audit a repéré que la première exécution de composition avait utilisé à tort les graines de classification 714/825/936, alors que le protocole prévoyait 411/522/633 pour cette partie. Les fichiers sont préservés sous `audit/superseded_composition_chunks_v1_1/`; ils ne sont pas inclus dans les synthèses confirmatoires finales. Le protocole correctif v1.2 et le lanceur de composition ont été hachés avant l'exécution corrigée. Les scripts de génération de rapports et de manifeste ont été retouchés après calcul pour distinguer correctement les graines et les versions ; ces changements administratifs ne modifient pas l'apprentissage des modèles ni les prédictions déjà gelées et ils sont traçables par les empreintes de livraison.

### Limites restantes

- L'audit s'exécute dans le même environnement local, pas dans un sandbox OS adversarial. Une inspection de signatures et de code ne prouve pas l'absence de tout canal caché.
- Trois graines de classification et trois cibles par famille ne fournissent qu'un petit nombre d'unités statistiques indépendantes ; les intervalles sont descriptifs.
- Les neurones imités sont des fonctions scalaires affines+activation en deux dimensions, et non des neurones récurrents, normalisés ou dépendant d'un contexte riche.
- Le dataset cancer du sein est un benchmark public de machine learning, pas une expérience clinique réelle.
- Aucune preuve mathématique d'équivalence universelle n'est produite.

## 6. Verdict par hypothèse

- **H1 — capacité d'apprentissage de tâche :** soutenue pour les quatre tâches et les budgets testés.
- **H2 — imitation entrée-sortie de neurones :** soutenue pour trois familles de neurones artificiels simples, sur les distributions testées et avec un nombre de paramètres de sonde supérieur.
- **H3 — généralisation :** soutenue sur IID tenu à part ; pas soutenue comme garantie sous décalage d'entrée.
- **H4 — composition :** partiellement soutenue comme remplacement fonctionnel local ; la fidélité des logits se dégrade lorsque davantage d'unités sont substituées, et le système conserve le lecteur source.
- **H5 — généralité :** non établie au-delà des tâches, familles, budgets et graines testés.
- **H6 — neurone cas particulier de sonde :** compatible avec une interprétation opérationnelle et une possibilité d'approximation, mais non démontrée au sens mathématique universel.

## 7. Complément réel multiclasse : chiffres manuscrits

Un protocole complémentaire `protocole_cas_reel_multiclasse_v1.md` a été gelé avant exécution. Il utilise `sklearn.datasets.load_digits` : 1 797 images manuscrites 8×8, 64 entrées, dix classes. Les splits stratifiés sont 60/20/20, graines 1428/2539/3640, et le standardiseur est ajusté sur train seulement. A/B/MLP ont exactement 1 210 paramètres entraînables ; le contrôle RBF fixe en a 170.

| Méthode | Exactitude (%) | Balanced accuracy (%) | F1 macro (%) | Log-loss | Paramètres entraînables |
|---|---:|---:|---:|---:|---:|
| RBF fixe | 76,67 ± 3,38 | 76,66 ± 3,38 | 76,48 ± 3,37 | 1,304 ± 0,004 | 170 |
| RBF adaptative A | 87,31 ± 3,52 | 87,34 ± 3,49 | 87,34 ± 3,45 | 0,752 ± 0,055 | 1 210 |
| RBF à taux méta-appris B | 78,33 ± 2,27 | 78,28 ± 2,22 | 78,00 ± 2,11 | 1,419 ± 0,026 | 1 210 |
| MLP de référence | 96,76 ± 1,16 | 96,77 ± 1,16 | 96,77 ± 1,16 | 0,126 ± 0,032 | 1 210 |

Les écarts sont des écarts-types sur trois partitions, pas des garanties universelles. Les intervalles t descriptifs à 95 % (n=3, 2 degrés de liberté) se trouvent dans `results/digits_synthese_intervalles_95.csv`. Le résultat affaiblit une interprétation optimiste de B : apprendre quatre taux d'adaptation ne suffit pas nécessairement à améliorer la sonde, et la RBF adaptative reste derrière le MLP sur ce problème réel multiclasse. Le résultat défavorable est retenu sans sélectionner une autre graine.

### Composition sur chiffres manuscrits

| Unités remplacées | Exactitude source (%) | Exactitude composée (%) | Accord avec source (%) | RMSE logits |
|---:|---:|---:|---:|---:|
| 1 | 96,76 ± 1,16 | 96,11 ± 1,00 | 99,17 ± 0,00 | 0,389 ± 0,023 |
| 4 | 96,76 ± 1,16 | 95,74 ± 1,28 | 98,15 ± 1,05 | 0,783 ± 0,022 |
| 16 | 96,76 ± 1,16 | 86,57 ± 1,95 | 86,94 ± 2,82 | 1,878 ± 0,023 |

Le RMSE moyen des 48 sondes scalaires est 0,5218 sur les activations d'évaluation, versus 0,5184 sur les exemples d'ajustement. Chaque sonde possède 529 paramètres, contre 65 paramètres d'entrée+biais pour une unité cachée du MLP ; le remplacement ne se fait donc pas à budget égal. Comme le lecteur de sortie source est conservé, le test démontre une substitution de composants, pas une reconstruction autonome.

### Audit séparé du complément

`audit/audit_integrite_digits.json` indique `PASS` pour les contrôles effectivement réalisés : hashes gelés identiques, 12 résultats de classification, 4 320 prédictions de test uniques et alignées, 9 résultats de composition, 48 fidélités d'unités, 3 240 prédictions de composition sans duplicat, 5 391 entrées de registre de partitions et zéro chevauchement de hash de caractéristiques entre train/validation/test dans chaque split. L'audit reste limité : il ne démontre pas l'absence de tout canal caché dans l'environnement local.


## 8. Supplément séparé préenregistré : chiffres manuscrits 3 contre 8 (64 dimensions)

Ce supplément est distinct du test multiclasse à dix chiffres décrit plus haut. Le protocole `protocole_supplement_digits_v1_0.md` et sa correction administrative `protocole_supplement_digits_v1_0_1.md` sont fournis avec leurs empreintes. Le jeu public scikit-learn est filtré aux étiquettes originales 3 et 8 : 357 exemples, 64 intensités de pixels. Il s'agit d'une tâche binaire de benchmark, pas d'une expérience de reconnaissance en production.

| Méthode | Paramètres entraînables | Exactitude (%) | F1 (%) | ROC-AUC | Log-loss |
|---|---:|---:|---:|---:|---:|
| RBF fixe | 17 | 91,20 ± 4,47 | 91,35 ± 4,29 | 0,9727 ± 0,0183 | 0,3516 ± 0,0301 |
| RBF adaptative A | 1 057 | 95,37 ± 2,89 | 95,40 ± 2,84 | 0,9951 ± 0,0047 | 0,1521 ± 0,0320 |
| RBF à taux méta-appris B | 1 057 | 96,76 ± 2,12 | 96,73 ± 2,11 | 0,9979 ± 0,0019 | 0,0827 ± 0,0234 |
| MLP de référence | 1 057 | 99,07 ± 1,60 | 99,07 ± 1,60 | 1,0000 ± 0,0000 | 0,0216 ± 0,0207 |

Les chiffres sont les moyennes ± écarts-types sur trois graines (714, 825, 936). B est compétitive, mais ne dépasse pas le MLP. Le contrôle fixe a 17 paramètres contre 1 057 dans les autres variantes ; cette comparaison ne permet donc pas d'isoler l'effet de l'adaptation à capacité égale.

| Unités cachées remplacées | Exactitude enseignant (%) | Exactitude après remplacement (%) | Écart moyen absolu de logits |
|---:|---:|---:|---:|
| 1 | 98,15 ± 3,21 | 98,15 ± 3,21 | 0,1224 ± 0,0269 |
| 4 | 98,15 ± 3,21 | 97,22 ± 2,41 | 0,4937 ± 0,0011 |
| 16 | 98,15 ± 3,21 | 95,83 ± 0,00 | 1,9688 ± 0,0808 |

L'erreur de fidélité d'activation des sondes en dimension 64 est MAE 0,2599 ± 0,0089, RMSE 0,3301 ± 0,0237 et R² 0,8677 ± 0,0201. Chaque sonde scalaire a 529 paramètres, contre 65 pour une unité cachée enseignante ; le remplacement laisse le lecteur aval du MLP intact. La fidélité locale est donc une approximation à budget non égal, non une reconstruction autonome.

### Incident de sérialisation documenté

Le premier passage du supplément a terminé les calculs, l'entraînement et l'écriture des prédictions/CSV, mais a échoué au sérialiseur JSON de l'audit à cause de clés tuple. Le correctif v1.0.1 a modifié la sérialisation administrative uniquement. Les cinq artefacts principaux hachés avant/après correction sont octet pour octet identiques ; les empreintes sont dans `audit/audit_digits_supplement.json`, `audit/digits_before_audit_fix_sha256/results.sha256` et `audit/digits_after_audit_fix_sha256/results.sha256`.

### Conclusion complémentaire

Les résultats soutiennent une approximation fonctionnelle de certains composants neuronaux simples, y compris sur des entrées à 64 dimensions, et illustrent que le remplacement peut augmenter la divergence des logits avec le nombre d'unités remplacées. Ils ne démontrent ni une équivalence mathématique générale, ni que la sonde peut apprendre tout neurone, ni un système autonome sans composant source conservé.

## 8. Complément déjà exécuté : chiffres 3 contre 8

Un supplément séparé avait déjà été exécuté avec le protocole gelé `protocole_supplement_digits_v1_0.md` et son correctif administratif v1.0.1. Je n'ai pas relancé cette expérience. Elle filtre `load_digits` sur les classes 3 et 8 (357 images, 64 caractéristiques), avec les graines 714/825/936. Son audit d'origine indique que les quatre CSV clés et le registre de partitions sont identiques octet par octet avant et après la correction limitée au sérialiseur JSON.

| Méthode | Exactitude (%) | F1 (%) | ROC-AUC | Log-loss | Paramètres entraînables |
|---|---:|---:|---:|---:|---:|
| RBF fixe | 91,20 ± 4,46 | 91,35 ± 4,29 | 0,9727 ± 0,0182 | 0,352 ± 0,030 | 17 |
| RBF adaptative A | 95,37 ± 2,89 | 95,40 ± 2,84 | 0,9951 ± 0,0047 | 0,152 ± 0,032 | 1 057 |
| RBF à taux méta-appris B | 96,76 ± 2,12 | 96,73 ± 2,10 | 0,9979 ± 0,0019 | 0,083 ± 0,023 | 1 057 |
| MLP | 99,07 ± 1,60 | 99,07 ± 1,60 | 1,0000 ± 0,0000 | 0,022 ± 0,021 | 1 057 |

Dans cette classification binaire restreinte 3-vs-8, B dépasse A dans les essais effectués mais reste sous le MLP. Ce résultat ne doit pas être mélangé au benchmark à dix classes : les tâches, tailles de données, paramètres du MLP (1 057 vs 1 210) et protocoles sont distincts.

La composition de ce supplément avait une exactitude source moyenne de 98,15 %. Après substitution de 1/4/16 unités, l'exactitude était respectivement de 98,15/97,22/95,83 %, tandis que l'écart moyen absolu des logits augmentait de 0,122 à 0,494 puis 1,969. Chaque sonde de composant a 529 paramètres, contre 65 par neurone cible, et la lecture de sortie source reste en place.

Le rapport complet de ce supplément est `rapport_supplement_cas_reel_digits.pdf`, avec source `.tex`, protocole, CSV, registre de partitions et audit d'origine. Son protocole est une extension exploratoire séparée, pas le protocole primaire v1.1.


## Réplication strictement isolée v1.2

Cette réplication est rapportée séparément, sans agrégation avec les graines de la première campagne. Elle couvre quatre tâches (deux lunes, cercles, XOR produit et Wine binaire), trois graines neuves, et quatre méthodes par split. Les tableaux détaillés, les métriques d'imitation (9 cibles × 3 budgets × 3 graines) et les résultats de composition (6 systèmes, 96 sondes de composants) sont dans les CSV `strict_isolation_*_v1_2`.

Résultats principaux issus des CSV : B à taux méta-appris atteint 97,59 % d'exactitude moyenne sur deux lunes; sur cercles A et B sont pratiquement à égalité (94,63 % et 94,54 %); sur Wine binaire le MLP atteint 100 % et A/B 98,15/99,07 %; sur XOR produit A/B/MLP sont proches (93,89/93,61/93,15 %). L'imitation présente des R² moyens de 0,980–0,997 selon la famille et le budget, sur 4000 points de test par cible. Ces scores sont limités aux familles et domaines d'entrée évalués.

En composition, sur deux lunes, remplacer 16 unités fait passer l'exactitude moyenne de l'enseignant (95,74 %) à 90,56 %; sur Wine binaire, l'exactitude reste élevée mais l'écart absolu moyen des logits atteint 1,082. Le readout source est conservé : ces expériences n'établissent pas une reconstruction autonome.

L'audit v1.2 indique PASS_WITH_LIMITATIONS pour les trois phases. Les 18 sorties d'inférence gelée ont été rejouées et sont identiques octet par octet; la vérification est consignée dans `audit/strict_isolation_v1_2_inference_replay.json`. La portée reste limitée aux contrôles réels exécutés, et ne prétend pas à une garantie absolue contre tout canal auxiliaire.
