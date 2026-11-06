# Audit de complétude — Emplica Orchestra Org récursive (EX7)

**Conclusion d'exécution : COMPLÈTE pour la branche récursive prévue dans EX7.** L'architecture n'est pas restée à l'état de conception : le code, les entraînements principaux, le cross-fitting OOF, les correcteurs, les sorties d'étages et les ablations sont présents et contrôlés. Cela ne signifie pas que les objectifs scientifiques de qualité/vitesse sont atteints.

## 1. Architecture effectivement implémentée

Script principal : `src/run_orchestra_org_recursive.py`.

- **7 couches × 5 probes = 35 probes** dans l'architecture principale.
- Répartition adaptative/fixe par couche : `5/0`, `1/4`, `1/4`, `4/1`, `3/2`, `1/4`, `3/2`, soit 18 probes adaptatives et 17 probes fixes.
- **Global interne** : chaque couche a ses paramètres de coordination `phi_l`; `pi_l = softmax(phi_l)` pondère les sorties de ses cinq probes.
- **Global externe** : les couches sont pondérées par `rho = softmax(Psi)`; le coordinateur externe possède son état distinct.
- **Récursion/cascade** : la représentation cumulée des sorties de couches précédentes est concaténée à l'entrée des couches suivantes. Le contrôle « couches indépendantes » désactive cette communication tout en gardant les deux niveaux globaux.
- **Adaptation locale** : un optimiseur propre à chaque probe; les exemples sont répartis en cinq shards stratifiés par couche.
- **Adaptation globale** : objectifs supervisés de coordination calculés sur les sorties locales détachées du graphe des paramètres locaux; mise à jour toutes les cinq époques.
- **Modulation du taux local** : extension EX7 `eta0 × (0.5 + N × pi_lj) × (0.5 + L × rho_l)` avec `N=5`, `L=7`.

Le formalisme global utilisé provient du mécanisme source `softmax` des logits globaux, et non du gate externe conditionné par l'entrée. Les deux niveaux de coordination sont distincts. La mise à l'échelle de la formule N=4 vers N=5 et son ajout au niveau L=7 sont des extensions EX7 explicitement déclarées, non des théorèmes de convergence.

**Précision de fidélité :** les chaînes `equal/input/global` associées aux compositions historiques des couches sont conservées dans les métadonnées de configuration. Le `ProbeSet` récursif utilise cependant le même coordinateur global appris `softmax(phi_l)` pour les probes de chaque couche; ces étiquettes historiques ne déclenchent pas de gate input-conditioned distinct. Cette branche Org est donc la récursion à deux niveaux de globalité définie dans la section G du prompt, pas une reproduction de toutes les anciennes familles de gate EX6 à l'intérieur de chaque couche.

## 2. Entraînements principaux — 5/5

Graines principales : `1501`, `1607`, `1717`, `2029`, `3037`. Chaque graine a un checkpoint complet, un JSON de run et des prédictions de validation. Les dimensions de données contrôlées sont 341 exemples d'entraînement, 85 de validation et 30 variables.

| Mesure | Résultat moyen sur 5 graines |
|---|---:|
| Paramètres totaux | **6 712** |
| Accuracy | **98.35 %** (écart-type 0.64 points) |
| Log-loss | **0.06187** (écart-type 0.01388) |
| Fit du modèle de base | **5.92 s** |

Les cinq runs sont dans `results/metrics/EX7_ORCHESTRA_ORG_PER_SEED.csv` et les artefacts portent les préfixes `orchestra_org_recursive_7x5_seed{seed}_cascade` dans `results/raw/` et `results/models/`.

## 3. Cross-fitting OOF récursif — 5/5 graines, 15/15 folds

Script : `src/run_orchestra_org_oof.py`.

Pour chaque graine : 3 folds stratifiés externes; chaque fold conserve 20 % de son sous-ensemble d'entraînement comme arrêt anticipé interne; le fold OOF extérieur n'est jamais utilisé pour l'arrêt anticipé. Les vérifications reconstruites depuis les graines confirment que chaque ligne train reçoit exactement une prédiction OOF. Les logits ont la forme `(341, 2)` et sont finis. Les empreintes des 15 checkpoints de fold et celles des prédictions OOF sont vérifiées.

Les trois correcteurs du modèle récursif sont complets sur les cinq graines : `temp_bias`, `linear_context`, `rbf_lite_1probe`.

| Variante | Accuracy | Log-loss | OOF génération | Fit correcteur | Pipeline reconstruit |
|---|---:|---:|---:|---:|---:|
| base_only | 98.35% | 0.06187 | 0.00 s | 0.000 s | 5.92 s |
| temp_bias | 98.35% | 0.06195 | 15.77 s | 0.172 s | 21.86 s |
| linear_context | 98.12% | 0.05765 | 15.77 s | 0.231 s | 21.92 s |
| rbf_lite_1probe | 97.88% | 0.05535 | 15.77 s | 0.292 s | 21.99 s |

Le RBF-Lite 1 probe est le meilleur log-loss des trois correcteurs récursifs, mais sa log-loss moyenne (0,05535) reste au-dessus des références EX6 Emplica OOF (0,03637) et Orchestra OOF (0,03982). Il est donc une réalisation fonctionnelle, pas un remplaçant compétitif de ces références.

## 4. Correcteurs sur les sorties des couches — 10/10

Script : `src/run_ex7_org_stage_oof.py`. Deux variantes × cinq graines, avec logits OOF à chaque couche et couverture vérifiée.

| Variante | Accuracy moyenne | Log-loss moyenne | Fit du correcteur |
|---|---:|---:|---:|
| stage_gate_only | 98.35% | 0.06018 | 0.192 s |
| stage_affine_gate | 98.35% | 0.05996 | 0.205 s |

Ces deux sorties d'étages ne rejoignent pas non plus les log-loss des correcteurs OOF EX6.

## 5. Ablations et contrôle de communication

- Six ablations causales × cinq graines : **30/30**.
- Contrôle cascade complète : **5/5**.
- Contrôle couches indépendantes : **5/5 runs uniques**, en plus des résultats de cascade.
- Les couches indépendantes conservent les deux niveaux de coordination, mais coupent les dépendances inter-couches. Le benchmark threads inter-couches reste négatif sur le CPU testé.

Les ablations et les comparaisons sont dans `EX7_ORCHESTRA_ORG_ABLATIONS_AGGREGATES.csv`, `EX7_ORCHESTRA_ORG_ABLATIONS_PER_SEED.csv` et `EX7_ORCHESTRA_ORG_PARALLEL_LAYERS_PER_SEED.csv`.

## 6. Anomalies de consolidation identifiées et corrigées

Deux compteurs précédents mélangeaient les catégories d'exécution, sans corruption des données d'expérience :

1. Le statut principal utilisait un glob qui comptait les **15 fits temporaires des folds OOF** comme 15 graines supplémentaires. Le compte correct est **5 modèles principaux + 15 fits de fold OOF**, listés séparément dans `EX7_ORCHESTRA_ORG_FOLD_FITS.csv`.
2. Le script des couches indépendantes ajoutait deux fois les cinq mêmes résultats (retour de fonction puis relecture des JSON). Le statut a été dédupliqué par `run_id` : **5 runs uniques**, pas 10.

Les modèles et résultats bruts n'ont pas été supprimés ou réentraînés. Les scripts de consolidation et de contrôle ont été corrigés afin qu'une future relance ne recrée pas ces compteurs erronés.

## 7. Vérifications d'intégrité spécifiques à la branche récursive

<badge color="success">{audit['status']}</badge>

- 5/5 modèles de base présents; checkpoints chargeables; SHA-256 checkpoint et prédictions identiques aux champs des résultats.
- 5/5 campagnes OOF présentes; 3 folds par graine; couverture des 341 lignes train exactement une fois; empreintes d'indices conformes.
- 15/15 checkpoints OOF de fold et logits OOF de forme correcte, sans valeurs non finies.
- 10/10 corrections sur sorties d'étages; 30/30 ablations; 25/25 variantes capacité; 60/60 variantes structurelles.
- 5/5 contrôles de couches indépendantes uniques après déduplication.
- `test_opened=false`; aucune partition de test vierge n'a été ouverte.

Le rapport machine détaillé est `results/metrics/EX7_RECURSIVE_ORG_AUDIT.json`.

## Verdict

**La version récursive est bien implémentée et exécutée de bout en bout pour les expériences prévues dans EX7.** En revanche, elle ne démontre pas encore une amélioration globale : sa chaîne OOF complète est coûteuse, sa qualité moyenne reste en retrait par rapport aux correcteurs OOF EX6, et le parallélisme CPU naïf ne l'accélère pas. Le statut correct est donc : **branche récursive terminée expérimentalement, mais non compétitive et non validée extérieurement**.
