# État exhaustif des ablations B10/B11 prévues dans EX9

| Ablation / piste prévue | Statut | Résultat / raison |
|---|---|---|
| B10 fidèle 9×5, memberships floues, seuils 1/3–2/3 | Exécuté dans EX8 et EX9 | Référence historique Wisconsin et réplication de développement `xor8` |
| Quantiles alternatifs 1/4–3/4 | Exécuté, 5 graines | `Q25_Q75`, validation seulement |
| Seuil médian 2×2 | Exécuté, 5 graines | `CODEBOOK_2X2`, 4 états durs |
| Retrait de la marge | Exécuté, 5 graines | `NO_MARGIN`, codebook 3×5 |
| Retrait du désaccord | Exécuté, 5 graines | `NO_DISAGREEMENT`, codebook 3×5 |
| Memberships dures vs floues | Exécuté, 5 graines | `HARD_3X3` contre B10 flou historique |
| Régularisation vs absence de régularisation | Exécuté, 5 graines | `NO_REGULARIZER` comparé au lambda 0,02 |
| Table factorisée | Exécuté, 5 graines | `FACTORIZED_3PLUS3`, 30 paramètres de table au lieu de 45 |
| Codebooks autres tailles/structures que 3, 4 et 9 états | Partiel | Les tailles 3×5, 2×2 (4×5) et 3×3 (9×5) sont représentées ; pas de recherche large de cardinalités |
| Mélange uniforme sans apprentissage de table | Non exécuté comme variante EX9 dédiée | Un gate B11 existe mais il n'est pas un contrôle uniforme constant |
| Gate linéaire/statistique alternatif | Non exécuté | B11 softmax standard est présent ; autres formulations restent ouvertes |
| Table low-rank générale, distillation, pruning d'états, fusion algébrique et partage de calcul RBF | Non exécuté | Travaux de simplification kernel/end-to-end restent ouverts |
| Gate B11 conditionné entrée/désaccord seul ou gate scalaire compact | Non exécuté | B11 fidèle seul a été répliqué |

## Résultat des 35 ablations table-only

Les log-loss moyennes validation sont comprises entre 0,544668 et 0,546467, contre 0,549981 pour B10 initial sur le même split. Ce delta est strictement descriptif : l'arrêt et la sélection utilisent la validation déjà exposée. Toutes les variantes demeurent très loin des MLP `xor8` (~0,30). Les `P_total` réduits passent de 400 à 370–385 ; les latences p50 batch 1 E2E de ces variantes restent entre 0,326 et 0,457 ms, donc supérieures au B11 (0,233 ms) et aux MLP (~0,017–0,018 ms) dans ce runtime CPU.

L'audit indépendant reconstruit les prédictions depuis le checkpoint B10 parent et les poids de table, puis recalcule log-loss et `P_total` : 35/35 PASS. Voir `reports/REPORT_B10_ABLATIONS_EX9.md`.

**Attention :** ces variantes testent les tables de fusion uniquement. Elles ne remplacent pas le besoin de profiler et simplifier le calcul des cinq banques RBF elles-mêmes.
