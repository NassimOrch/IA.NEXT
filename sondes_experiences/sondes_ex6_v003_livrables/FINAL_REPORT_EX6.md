# FINAL_REPORT_EX6

Date : 2026-10-31  
Version : `sondes_ex6_v001__2026-10-31`  
Statut général : **INCOMPLET — aucun succès global établi**

## 1. Résumé exécutif

Le prompt `prompt_ex6.json` révision 1.0.1 a été construit à partir des prompts EX3, EX4, EX5, des workspaces récents et des formalismes de sondes/adaptation globale. Il a été relu et contrôlé structurellement. Il comprend les trois familles voulues (Replica, Emplica simple, Emplica Orchestra), les règles anti-triche et anti-sabotage, la règle rouge de neutralité, le gel des tests, les comparateurs MLP, le comptage complet, les mesures de ressources, les règles OOF, la traçabilité, les livrables et le verdict sans présupposé.

Quatre pilotes quantifiés ont été exécutés sur cinq graines chacun, sur le split historique Wisconsin de développement :
- Replica par partition des experts avec copie figée ;
- Emplica simple hétérogène, 7 couches × 5 sondes ;
- Orchestra hétérogène avec gate externe scalaire appris ;
- Orchestra homogène MIXA global-gate.

**Constat principal :** les quatre bras satisfont le rapport de paramètres `P_MLP_ge4x / P_sonde >= 4`. Aucun ne démontre l'accélération recherchée. Les Emplica/Orchestra testés sont environ 5,7–6,1× plus lents à l'entraînement et 91,7–103,4× plus lents en p50 batch 1 que leur MLP-ge4x sur ce CPU. Replica est 23,1× plus lent en mode sériel et 72,2× en mode parallèle ; son gain d'entraînement n'a pas été mesuré. Les métriques de qualité ponctuelles sont inférieures aux MLP-ge4x en moyenne.

Un contrôle indépendant des checkpoints a aussi été fait sur les 20 paires candidate/MLP-ge4x : le nombre d'éléments tensoriels du state_dict correspond exactement à `P_total - 60` (les 60 coefficients du scaler) ; les états primaire/clone de Replica sont égaux tenseur par tenseur. Des exports d'inférence contenant poids + scaler ont été générés et leur taille sérialisée est plus faible que celle des MLP-ge4x appariés (cf. `results/metrics/deployment_export_sizes.csv`).

Aucune campagne n'a utilisé un domaine externe vierge, aucune marge de non-infériorité n'avait été pré-enregistrée et plusieurs éléments obligatoires de la spécification ne sont pas exécutés. Le statut honnête est donc `INCOMPLET`, avec des échecs sur des critères de vitesse déjà mesurés.

## 2. Résultats agrégés des pilotes

Valeurs = moyenne de cinq graines sur le même split de validation historique (85 observations). La précision est affichée en pourcentage. Les temps sont des moyennes inter-graines.

| Architecture | P sonde | P MLP-ge4x | Ratio | Accuracy sonde / MLP | Log-loss sonde / MLP | Fit sonde / MLP | p50 batch 1 sonde / MLP |
|---|---:|---:|---:|---:|---:|---:|---:|
| Replica sériel (duplication figée) | 2 260 | 9 071 | 4,014× | 97,647 / 98,588 % | 0,05218 / 0,05041 | NON MESURÉ / 0,252 s* | 0,351 / 0,0152 ms |
| Emplica simple hétérogène 7×5 | 7 010 | 28 046 | 4,001× | 98,353 / 98,588 % | 0,04597 / 0,04429 | 1,849 / 0,309 s | 1,842 / 0,0186 ms |
| Orchestra hétérogène, gate externe scalaire | 7 017 | 28 079 | 4,002× | 97,647 / 98,824 % | 0,05892 / 0,04464 | 1,745 / 0,309 s | 1,920 / 0,0186 ms |
| Orchestra homogène MIXA global | 6 712 | 26 858 | 4,001× | 97,647 / 98,824 % | 0,07021 / 0,04621 | 1,549 / 0,252 s | 1,676 / 0,0183 ms |

\* Pour Replica, le temps de 0,252 s est celui du MLP-ge4x ; le temps d'entraînement de la copie Replica est `NON MESURÉ`. Le temps source historique du pipeline sonde était 2,138 s moyen contre 0,252 s pour MLP-ge4x, mais ce n'est pas une mesure d'entraînement d'une Replica partagée.

### 2.1 Détail des paramètres persistants

| Candidate | P_train | P_fixed / buffers dans le modèle | Prétraitement | P_total |
|---|---:|---:|---:|---:|
| Replica (primaire + copie figée) | 1 100 | 1 100 | 60 | 2 260 |
| Emplica simple hétérogène | 4 198 | 2 752 | 60 | 7 010 |
| Orchestra hétérogène | 4 205 | 2 752 | 60 | 7 017 |
| Orchestra homogène MIXA | 4 260 | 2 392 | 60 | 6 712 |

Pour Replica, `P_train` désigne le primaire historique entraînable ; la seconde copie est gelée et comptée dans `P_fixed`, même si elle conserve des tenseurs dupliqués inutilisés par son chemin d'inférence. Les deux copies sont toutes deux comptées. Les comptes des trois piles incluent les bases/buffers fixes dans la colonne correspondante. Un audit indépendant des state_dict confirme pour chacune `P_total - 60` éléments de tenseur persistants dans le modèle ; les 60 coefficients restants sont les paramètres du scaler.

### 2.2 Lecture par critère

**Paramètres :** succès du seuil 4× pour ces quatre pilotes seulement. Le compte comprend les paramètres dupliqués, fixes, buffers et prétraitement déclarés. Le ratio n'est pas une preuve de moindre coût d'exécution.

**Qualité :** les valeurs ponctuelles des candidates sont moins bonnes que le MLP-ge4x en moyenne sur les deux métriques principales. Pour Emplica simple, l'écart moyen est modeste (−0,235 point d'accuracy ; log-loss +0,00168). Pour Orchestra, les écarts sont plus marqués. Pour Replica, accuracy −0,941 point et log-loss +0,00176. Aucun résultat ne peut être qualifié de non-inférieur : les marges de non-infériorité n'avaient pas été fixées avant l'expérience, et les graines sont évaluées sur les mêmes 85 observations.

**Vitesse :** tous les bras Emplica/Orchestra sont nettement plus lents que le MLP-ge4x. Les ralentissements moyens p50 batch 1 sont respectivement 99,1×, 103,4× et 91,7×. Replica sériel est 23,1× plus lent que son MLP-ge4x ; la version parallèle est 72,2× plus lente. La duplication n'a pas réduit le travail total et le parallélisme testé ajoute des frais de coordination.

**Ressources :** le comptage paramétrique a été recalculé depuis les tensors des checkpoints. Les exports inférence poids+scaler sont plus petits en octets pour les sondes que pour les MLP-ge4x : Replica 32,3 kB vs 39,6 kB (ratio 0,817) ; Emplica simple 98,3 kB vs 115,5 kB (0,851) ; Orchestra hétérogène 98,6 kB vs 115,6 kB (0,853) ; Orchestra homogène 97,7 kB vs 110,6 kB (0,883). Ce sont les tailles de fichiers de ces exports, non le coût mémoire complet d'exécution. Les MAC/FLOP/kernel counts, RSS/activation memory, énergie et profil déploiement complet n'ont pas été mesurés de manière exhaustive. Il est donc impossible d'affirmer une consommation totale plus faible.

## 3. Détails d'interprétation

### Replica
Le clone est figé et non optimisé indépendamment. Le partage des experts [0,1,2] et [3,4] reproduit les sorties primaires avec une différence maximale de logits de `9,54e-7` et une différence maximale de probabilités vs l'archive de `1,19e-7` sur les cinq graines. C'est une parité numérique à tolérance flottante, pas une identité bit à bit.

Le p50 sériel (0,351 ms) est légèrement inférieur à la référence primaire (0,403 ms) dans ce benchmark ; cependant il reste très loin du MLP-ge4x (0,0152 ms). L'exécution parallèle mesurée est encore plus lente (1,094 ms). La copie est entièrement comptée en paramètres et en stockage. Ce pilote ne démontre ni un gain d'entraînement ni une réduction de coût arithmétique : il partitionne un sous-ensemble d'experts et conserve les mêmes calculs fonctionnels.

### Emplica simple
Le bras 7×5 hétérogène passe le ratio de paramètres, mais ne démontre aucun avantage de vitesse. Son accuracy moyenne est proche du MLP-ge4x, mais sa log-loss est plus élevée. Les bras homogène sélectionné comme « meilleur » par sélection imbriquée, spécialiste par couche, OOF inter-couches et allocations alternatives ne sont pas complets.

### Emplica Orchestra
La forme testée contient un gate externe scalaire appris par couche ; ce n'est qu'une instanciation partielle de l'adaptation globale externe. Le gate n'est pas conditionné par X. Les couches ne disposent pas du correcteur OOF inter-couches demandé et le spécialiste par couche n'est pas exécuté. L'hétérogène et l'homogène ont des résultats de qualité moins bons et sont très lents.

L'essai d'early exit est exploratoire uniquement. Pour le seuil 0,98, il active en moyenne 6,47 couches sur 7, conserve l'accuracy observée mais dégrade la log-loss et ne réduit le p50 batch1 que de façon limitée. Il reste très loin du MLP. Les seuils ont été balayés sur la validation de développement ; aucune conclusion générale n'en découle.

## 4. Contrôle indépendant des prédictions

62 fichiers de prédictions (candidates et comparateurs) ont été recalculés depuis les probabilités enregistrées :
- écart maximal sur accuracy : 0 ;
- écart maximal sur log-loss : 8,46×10⁻⁹.

Ce contrôle confirme la cohérence interne entre prédictions sauvegardées et métriques des résumés. Il ne prouve ni l'isolation stricte du test ni la généralisation ; les données sont historiquement exposées.

## 5. Données, environnement et limites

- Split historique Wisconsin v009 : train 341, validation 85, adaptation 57, test 86.
- Dataset déjà présent et utilisé dans les travaux antérieurs ; développement uniquement.
- Le chargeur a matérialisé la source Wisconsin complète en mémoire via scikit-learn, puis sélectionné les partitions autorisées ; les lignes test n'ont pas été transmises aux modèles ni utilisées pour l'optimisation/sélection. Cette approche n'offre pas l'isolation stricte d'un chargeur qui ne dévoile jamais le test.
- Cinq graines sur le même split ne constituent pas cinq jeux indépendants.
- CPU AMD EPYC 9V74, 3 CPU visibles, PyTorch CPU, sans GPU, 1 thread PyTorch.
- Les temps d'entraînement reportés sont des temps de fit modèle ; ils n'incluent pas de façon homogène l'ensemble des coûts de chargement, clustering/initialisation, prétraitement, sérialisation et orchestration.
- Pas de mesures d'énergie, mémoire d'activation, RSS de pointe complet, VRAM, p99 ou batch256.
- Pas de domaines externes vierges et pas de NI pré-enregistrée.
- La première campagne a été exécutée via des cellules interactives, puis des scripts autonomes ont été sauvegardés/ajustés ; la trace des cellules est conservée, mais le SHA exact du code chargé par chaque run n'est pas attesté. L'identité code-run est `NON VÉRIFIÉE` pour la campagne initiale.

## 6. Travaux qui restent obligatoires

1. Replica pendant l'entraînement avec équations de gradient/synchronisation ; partition interne des kernels/centres ; contrôle parallèle sans copie.
2. Emplica homogène-best et spécialiste par couche avec sélection imbriquée/OOF ; interfaces contrôlées ; correction OOF par couches.
3. Orchestra complet : `theta_{l,i}`, `phi_l`, `psi` explicites ; gate externe input-conditioned ; OOF inter-couches ; communication ; activation/cascade ; toutes les ablations demandées.
4. Profiler les coûts complets sur des batchs réalistes, latences p50/p95/p99, RAM/activation/bytes/énergie si possible.
5. Choisir les marges NI avec justification et les enregistrer avant accès aux labels externes.
6. Geler code/config/splits et confirmer sur plusieurs domaines véritablement non exposés.
7. Réaliser l'audit indépendant de fin de campagne et mettre à jour la matrice des verdicts.

## 7. Verdict final

- **Replica :** le clonage figé préserve numériquement la sortie et le ratio de paramètres passe ; aucun gain de vitesse vs MLP, pas de mesure d'entraînement Replica ; critère rapidité échoué sur les chemins mesurés.
- **Emplica simple :** ratio de paramètres passé ; accuracy/log-loss ponctuelles légèrement en retrait ; vitesse d'entraînement et latence nettement échouées ; variantes requises non achevées.
- **Emplica Orchestra :** ratio passé dans les deux pilotes ; qualité et vitesse inférieures au MLP-ge4x ; architecture complète demandée non réalisée.
- **Succès global : NON ÉTABLI.**
- **Statut de campagne : `INCOMPLET`.**

Aucun résultat ne permet d'affirmer que les sondes sont plus rapides ou consomment moins de ressources que le MLP dans les implémentations testées. Les économies de paramètres observées sont réelles pour les quatre pilotes, mais insuffisantes pour satisfaire la règle rouge conjointe.
