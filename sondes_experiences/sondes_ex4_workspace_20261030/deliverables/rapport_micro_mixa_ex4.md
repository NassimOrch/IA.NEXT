# Étude micro-MIXA — EX4 v008 et transfert v009

## Définition reconstruite
Les débris EX3 citent `mixa_micro_d4_k8` et 528 coefficients sur ModeChoice, mais ni le code exact ni les checkpoints EX3 ne sont disponibles. La reconstruction EX4 n'affirme donc pas répliquer le prototype ; elle teste l'hypothèse hybride explicitement : un expert RBF adaptatif micro d=4/k=8, une branche RBF fixe d=4/k=8, puis un agrégateur. Les ablations comparées sont adaptatif seul, fixe seul, mélange égal, gate global appris et gate conditionnel à l'entrée.

## Wisconsin v008 — cinq graines

| Variante | P_total (scaler inclus) | Accuracy | Log-loss |
|---|---:|---:|---:|
| Adaptative seule | 242 | 96,71 % | 0,07579 |
| Fixe seule | 242 | 94,12 % | 0,17291 |
| Mélange égal | 424 | 97,18 % | 0,08456 |
| Gate global | 426 | 96,94 % | 0,07516 |
| Gate entrée | 486 | 97,18 % | 0,08707 |

Les MLP ge4x appariés ont des log-loss moyennes de 0,05121 à 0,05439 et des accuracies de 97,88 à 98,35 %. Le mélange égal gagne en accuracy sur la branche adaptative seule mais dégrade sa log-loss ; le gate global se rapproche de l'adaptatif sans atteindre le MLP. L'ablation fixe seule est nettement plus faible et lente. Cette campagne est historique/développementale, pas une validation confirmatoire.

## Transfert Iris v009 — cinq graines

Le jeu local scikit-learn contient 150 exemples, 4 variables et 3 classes ; les partitions fixes ont 90 train, 20 validation, 10 adaptation et 30 test. Quatre bras ont été préenregistrés sur cinq initialisations : adaptatif seul et les trois modes micro-MIXA (mélange égal, gate global, gate conditionnel). Les deux états `fixed_only` incomplets du pré-vol ont été quarantinés et exclus ; la branche fixe seule est déjà mesurée sur Wisconsin et n'a pas été réentraînée sur Iris.

| Candidate | P_sonde total | MLP ge4 P_total | Ratio | Accuracy test sonde / MLP | Log-loss test sonde / MLP |
|---|---:|---:|---:|---:|---:|
| Adaptative seule | 95 | 387 | 4,074× | 95,33 / 96,67 % | 0,16466 / 0,09761 |
| Mélange égal | 182 | 731 | 4,016× | 96,00 / 96,67 % | 0,12062 / 0,09633 |
| Gate global | 184 | 739 | 4,016× | 96,67 / 96,67 % | 0,14282 / 0,09331 |
| Gate conditionnel | 192 | 771 | 4,016× | 96,67 / 96,67 % | 0,17272 / 0,09420 |

Les ratios comptent aussi les huit valeurs numériques du StandardScaler des deux côtés. Sur 30 observations de test, les trois micro-MIXA ont la même accuracy moyenne que le MLP ge4x ou en sont proches, mais leur log-loss est plus élevée. Ce profil est compatible avec une séparation de classes correcte mais une calibration/probabilité moins bonne ; il ne suffit pas à établir une non-infériorité formelle.

## Coûts de calcul et stockage
| Candidate | Fit sonde (s) | Fit MLP (s) | Latence médiane B1 sonde / MLP (ms) | MAC analytiques sonde / MLP | Octets modèle + scaler sonde / MLP |
|---|---:|---:|---:|---:|---:|
| Adaptative seule | ND* | 0,337 | 0,03890 / 0,01384 | 72 / 329 | 3 221 / 3 933 |
| Mélange égal | 1,625 | 0,275 | 0,08059 / 0,01411 | 144 / 630 | 4 991 / 5 341 |
| Gate global | 1,344 | 0,258 | 0,08921 / 0,01468 | 146 / 637 | 5 372 / 5 405 |
| Gate conditionnel | 2,280 | 0,260 | 0,08966 / 0,01410 | 152 / 665 | 5 561 / 5 469 |

*ND : cinq checkpoints adaptatifs terminés avaient été sauvegardés lors du premier pré-vol ; l'interruption a eu lieu après sauvegarde des poids mais avant écriture des métriques/historiques. Les poids ont été restaurés et les prédictions/metrics/latences de validation/test recalculées sans réentraînement ; les durées de fit, époques et traces détaillées n'étaient plus disponibles et ne sont pas imputées.

Les micro-MIXA réduisent le nombre de MACs analytiques et, pour certaines variantes, les octets du modèle. En revanche, la latence CPU mesurée est 5,5–6,4 fois celle du MLP ge4x ; le fit est aussi 5,2–8,8 fois plus long sur les trois MIXA entraînés sur Iris. Le gate conditionnel dépasse même légèrement le MLP en taille sérialisée combinée. Ces résultats n'établissent donc pas un avantage de ressources global.

## Conclusion
La piste micro-MIXA est récupérable et vaut la peine d'être conservée comme famille architecturale ; le résultat ne valide pas encore l'objectif. La réduction des paramètres et des MACs analytiques ne s'est pas traduite en log-loss ni en latence inférieures au MLP. La taille d'Iris et la répétition sur cinq initialisations (mêmes 30 cas de test, donc pas 150 observations indépendantes) imposent une interprétation exploratoire.
