# EX12 P0 — Rapport de clôture documentaire

- Gate : **PASS**
- Date UTC : `2026-11-04T11:11:37.880797+00:00`
- Prompt SHA-256 : `ebb4d770a638434854b5b941a0634d4c1cd2661cab49fb8e39e1b69a9cb544a0`
- Rapport .tex SHA-256 : `98a8fdec7100b1847f8510aff1a721fb3b7787d267589572fdcb2b8ca54e2375`
- Vérifications : 17/17 PASS.

## Gaps non bloquants déclarés

- `prompt_ex10.json` absent ; les artefacts primaires EX10 sont audités et la référence EX8 V010 est étiquetée comme telle.
- `arch_up_test_0.zip` absent ; aucun résultat EX0 n’est inféré.
- `prompt_ex11.json` est explicitement une reconstruction v2.3.1.
- EX8 v1.0 et v1.1 ont des métadonnées différentes mais un corps de prompt identique ; v1.1 est la révision retenue pour EX8 V010.

## Décisions gelées

- Comparaison `P_total` à ±1 % ; ancien GE4X retiré.
- Marges de qualité/ressources et définitions consignées dans `00_governance/P0_DECISIONS.json`.
- 10 seeds pilote et 20 seeds confirmatoires, disjointes, gelées dans `00_governance/seed_manifest.json`.
- Aucun entraînement n’a eu lieu pendant P0.

## Portée du PASS

Ce PASS clôt exclusivement P0. P1 doit être exécutée et disposer de sa propre `phase_gate.json` PASS avant tout entraînement.
