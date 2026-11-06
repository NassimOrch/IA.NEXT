# P4 — clarification de l'appariement et supersession de l'audit P_total

Date : 2026-11-04.

Le rapport directeur `rapport_prigramme_expermentale_EX12_NEXT_0.tex`, lignes 511–515, exige que le MLP principal soit apparié au nombre de **paramètres entraînables** à ±1 %. Il précise séparément que le stockage, les buffers et les autres ressources doivent être rapportés. Le premier audit P4 a appliqué à tort ±1 % au nombre total de scalaires persistants (`P_total`) et a donc masqué un écart d'environ 22 % des paramètres entraînables pour C3/C4.

Le premier audit, ses CSV et son script historique sont conservés sous les noms `*_V1_TOTAL_PERSISTENT_LEGACY.*` et dans `04_code/audit_p4_fairness.py`. Ils ne constituent pas l'audit P4 final. L'addendum `03_design/P4/P4_TRAINABLE_PARAMETER_MATCH_ADDENDUM.json` a été gelé avant l'entraînement des 160 contrôles MLP additionnels.

L'audit corrigé `04_code/audit_p4_trainable_match_v2_1.py` compare R0/C2 à M0_CORE et C3/C4 aux contrôles MLP additionnels dédiés. Il vérifie 320 paires, 160 contrôles P4 distincts, la provenance, les configurations d'entraînement, les seeds, la normalisation, les hashes et l'écart des paramètres entraînables. Les quatre variantes sont dans ±1 % sur 80/80 paires chacune.

Cette correction ne modifie aucun candidat P3, split, label, prédiction ou checkpoint. Aucun test ni holdout n'a été ouvert.
