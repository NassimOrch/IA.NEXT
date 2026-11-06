# Rapport CNC — EX11

## Protocole
Six spécialistes (ADD/SUB/MUL/DIV/EXP/LOG), entraînés sur les distributions opératoires réellement induites par g1–g3. C1 gèle les spécialistes ; C2 les ajuste conjointement. C3 MLP direct ; C4 AdaptiveRBF directe ; C5 oracle exact. Les compositions g4/g5 sont générées après gel des modèles. Seeds planifiées : dix.

## Runs persistés (3 enregistrements au registre)

### CNC_composition_1501_v003 — COMPLETED_VALIDATION_AND_HELDOUT_COMPOSITION

Graine : 1501. Code SHA-256 : `2158497cad596671fde3e9a6e5038929dbcb727217bd52b98cccdfe897780847`.

| Opération | MAE validation spécialiste | Temps train (s) | Époques |
|---|---:|---:|---:|
| ADD | 0.005068 | 136.83 | 190 |
| SUB | 0.001881 | 24.18 | 184 |
| MUL | 0.374047 | 39.17 | 75 |
| DIV | 0.083477 | 75.53 | 500 |
| EXP | 0.000604 | 34.59 | 123 |
| LOG | 0.001029 | 56.59 | 377 |

| Graphe | C1 MAE val. | C2 MAE val. |
|---|---:|---:|
| g1 | 0.501331 | 0.505065 |
| g2 | 0.603099 | 0.615614 |
| g3 | 0.251196 | 0.042173 |

| Composition inédite | C1 MAE | C2 MAE |
|---|---:|---:|
| g4 | 1.111216 | 1.067698 |
| g5 | 0.287935 | 0.336804 |

| Graphe direct | MLP MAE val. | AdaptiveRBF MAE val. | Paramètres MLP | Paramètres sonde |
|---|---:|---:|---:|---:|
| g1 | 0.003893 | 0.524146 | 1217 | 65 |
| g2 | 0.035084 | 0.686955 | 1217 | 65 |
| g3 | 0.004826 | 0.413400 | 1217 | 65 |

### CNC_composition_1501_v004 — COMPLETED_VALIDATION_AND_HELDOUT_COMPOSITION

Graine : 1501. Code SHA-256 : `c05cc6860e08f92a7452eae1296bac71a6e80e5cb6deca8f134d22af8a5c5d21`.

| Opération | MAE validation spécialiste | Temps train (s) | Époques |
|---|---:|---:|---:|
| ADD | 0.006492 | 149.83 | 220 |
| SUB | 0.001881 | 22.59 | 184 |
| MUL | 0.374047 | 42.20 | 75 |
| DIV | 0.083477 | 69.33 | 500 |
| EXP | 0.000604 | 35.34 | 123 |
| LOG | 0.001029 | 51.34 | 377 |

| Graphe | C1 MAE val. | C2 MAE val. |
|---|---:|---:|
| g1 | 0.501952 | 0.507227 |
| g2 | 0.601931 | 0.629592 |
| g3 | 0.248540 | 0.040166 |

| Composition inédite | C1 MAE | C2 MAE |
|---|---:|---:|
| g4 | 1.110613 | 1.075295 |
| g5 | 0.288875 | 0.411692 |

| Graphe direct | MLP MAE val. | AdaptiveRBF MAE val. | Paramètres MLP | Paramètres sonde |
|---|---:|---:|---:|---:|
| g1 | 0.003893 | 0.528221 | 1217 | 65 |
| g2 | 0.035084 | 0.200826 | 1217 | 65 |
| g3 | 0.004826 | 0.413213 | 1217 | 65 |

## Limites

- v003 utilisait initialisation aléatoire des centres C4 ; il est exploratoire.
- v004 utilise KMeans train-only pour C4, mais la graine d’ordre des mini-batches C3/C4 n’était pas appariée. Il reste donc descriptif/partiel et ne constitue pas la confirmation stricte de la comparaison directe.
- v005 corrige le batch-order pairé ; non exécuté à ce snapshot.
- Une seule seed v004 ne peut pas établir une généralisation reproductible. Le coût et la qualité doivent être agrégés sur les dix graines.

## Conclusion provisoire

C2 donne une amélioration spectaculaire sur g3 mais pas sur l’ensemble des graphes : il détériore g1/g2 et les compositions g5. La généralisation par composition reste mixte. C4 économise beaucoup de paramètres face au MLP direct (65 contre 1217, ratio ≈18,7×), mais il est nettement moins précis sur g1–g3 et met parfois plus de temps à entraîner. Cela montre que la compression paramétrique ne garantit ni précision ni vitesse.
