# Rapport P4 — appariement équitable MLP et recalcul des métriques

**Expérience :** EX12_NEXT_0  
**Statut :** P4 PASS — appariement primaire sur paramètres entraînables.  
**Références :** `rapport_prigramme_expermentale_EX12_NEXT_0.tex` lignes 511–515 ; addendum gelé `03_design/P4/P4_TRAINABLE_PARAMETER_MATCH_ADDENDUM.json`.

## 1. Objet

P4 corrige l'appariement initial P3 pour respecter le critère du rapport directeur : le MLP principal doit être apparié au nombre de paramètres **entraînables** à ±1 %. `P_total` (paramètres entraînables, buffers fixes, état du normaliseur et scalaires persistants) est rapporté séparément et n'est pas utilisé comme substitut au compte de paramètres entraînables. Le ratio GE4X historique est retiré d'EX12.

## 2. Exécution des contrôles MLP additionnels

Le registre `P4_RUN_REGISTRY.jsonl` contient 160 runs logiques réussis : 80 `M0_C3_TRAINABLE` et 80 `M0_C4_TRAINABLE`, couvrant huit tâches et dix graines chacune. Il conserve également une tentative interrompue (`g6_log_quadratic_rational`, graine 934109236, `M0_C4_TRAINABLE`) sans checkpoint ni prédictions ; la reprise réussie existe sous un identifiant A02 différent. Cette interruption n'est pas supprimée et ne crée aucun trou logique dans le quota de 160 contrôles.

## 3. Appariement primaire : paramètres entraînables

| Variante | Paires | Écart moyen baseline/candidate | Écart médian | Écart absolu maximal | Paires dans ±1 % |
|---|---:|---:|---:|---:|---:|
| R0 | 80 | 0.273% | 0.355% | 0.693% | 80/80 |
| C2 | 80 | 0.273% | 0.355% | 0.693% | 80/80 |
| C3 | 80 | 0.697% | 0.899% | 0.960% | 80/80 |
| C4 | 80 | -0.470% | -0.655% | 0.905% | 80/80 |

L'audit exhaustif a contrôlé 320 paires candidate–MLP : R0/C2 utilisent M0_CORE (80 paires chacune) ; C3/C4 utilisent les contrôles supplémentaires M0_C3_TRAINABLE/M0_C4_TRAINABLE (80 paires chacun). Les 160 nouveaux contrôles P4 sont utilisés exactement une fois. Aucune paire n'excède 1 % d'écart en paramètres entraînables. Les buffers, normaliseurs et scalaires persistants sont enregistrés séparément.

## 4. Recalcul des métriques et intégrité

- Paires candidate–baseline : 320.
- Comparaisons tâche × graine × régime : 1 080.
- Valeurs de métriques recalculées depuis les prédictions sauvegardées : 8 960.
- Fichiers de run contrôlés par empreinte : 2 800 ; divergence : 0.
- Tolérance de recomputation : 2×10⁻⁶, motivée par la sérialisation float32 des prédictions alors que les métriques initiales ont été calculées avant cette sérialisation.
- Hashes de checkpoint, prédictions, métriques, historique et config : aucune divergence.
- Accès test/holdout : NONE.

Les sorties complètes sont dans `09_analysis/P4/P4_PAIRED_METRIC_REANALYSIS.csv` et ses résumés par variante et régime. Le tableau descriptif utilise NMAE normalisée train pour régression et log-loss pour classification ; une victoire signifie seulement une valeur candidate plus faible sur la graine considérée, sans test de significativité.

### Lecture exploratoire corrigée

Sur 270 comparaisons graine×régime par variante, les nombres de victoires en métrique primaire (plus faible = meilleur) sont : R0 110/270 ; C2 130/270 ; C3 117/270 ; C4 130/270. Ce comptage agrège des tâches et régimes hétérogènes et n'est pas un test statistique global. Les résultats sont variables : C2 est nettement meilleur que son MLP apparié sur `f2_mul` en interpolation (NMAE moyenne 0,0203 contre 0,0700, 7/10 graines), mais toutes les variantes sont moins bonnes sur plusieurs extrapolations. Pour `f1_sin` en interpolation, les quatre variantes perdent en moyenne face au MLP apparié. En classification synthétique, les log-loss moyennes des quatre candidates restent supérieures à celles du MLP apparié.

Ces résultats sont exploratoires et ne permettent aucune revendication de supériorité générale. P5 doit mesurer ressources end-to-end et stabilité selon les marges gelées ; P6 étudiera complémentarité/ablations.

## 5. Supersession de l'audit initial

Le premier audit P4 vérifiait ±1 % sur `P_total`, conduisant à un faux sentiment d'appariement entraînable pour C3/C4. Il est conservé sous `P4_FAIRNESS_AUDIT_V1_TOTAL_PERSISTENT_LEGACY.json` et fichiers associés. Il est supersédé par `P4_FAIRNESS_AUDIT.json`, `P4_PARAMETER_MATCH_AUDIT.csv` et le script `audit_p4_trainable_match_v2_1.py`. Le rapport de clarification explique l'origine et la correction, sans modifier les résultats de P3.

## 6. Scripts et reproduction

- Entraînement MLP additionnel : `04_code/train_p4_mlp_match.py`.
- Audit d'appariement primaire : `04_code/audit_p4_trainable_match_v2_1.py`.
- Recalcul des métriques et empreintes : `04_code/audit_p4_metrics_v1_1.py`.
- Pré-enregistrement : `03_design/P4/P4_TRAINABLE_PARAMETER_MATCH_ADDENDUM.json`.
- Registre complet : `00_governance/P4_RUN_REGISTRY.jsonl`.
- Configurations, checkpoints, prédictions et historiques : `06_runs/P4_MLP_TRAINABLE/`.

## 7. Décision

**P4 : PASS.** Les 320 paires respectent le critère directeur ±1 % sur paramètres entraînables, les 160 contrôles ajoutés sont complets, les métriques et hashes sont vérifiés, aucun test/holdout n'a été ouvert. Les résultats de qualité restent exploratoires ; ils ne constituent pas un verdict confirmatoire.
