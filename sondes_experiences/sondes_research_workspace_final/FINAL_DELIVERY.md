# Livraison finale — sondes adaptatives

**Version courante : `sondes_v009__2026-10-30`**

## Fichiers principaux

- `WORKSPACE_INDEX.md` : historique des neuf versions et statuts.
- `versions/sondes_v009__2026-10-30/reports/synthese_executive.md` : résultats principaux.
- `versions/sondes_v009__2026-10-30/reports/rapport_technique_final.md` : analyse technique complète.
- `versions/sondes_v009__2026-10-30/reports/audit_integrite_et_conformite.md` : conformité au prompt accessible et réserves.
- `versions/sondes_v009__2026-10-30/results/processed/audit_integrity_summary.json` : audit machine-lisible.
- `versions/sondes_v009__2026-10-30/scripts/reproduce_external.sh` : commande de reproduction des validations externes et audit.
- `SHA256SUMS_WORKSPACE.txt` : manifest SHA-256 des fichiers du workspace (hors manifeste lui-même).

## Intégrité

Le dernier audit a vérifié 143 JSONL (56 617 lignes, aucune invalide), les prédictions de test/validation, les métriques recalculées, les préprocesseurs joblib et les archives ZIP sources. Deux JSON historiques contiennent NaN pour des écarts-types indéfinis ; leurs originaux sont préservés et des copies strictes JSON corrigées avec `null` se trouvent dans le rapport v009.

Les chevauchements historiques entre partitions de test externes sont documentés dans les rapports et dans `results/processed/audit_integrity_summary.json` : Wisconsin 15/86 ; SMS 132/777. Les partitions internes v009 ne se chevauchent pas.

## Prompt exécuté

Le prompt accessible et intégré au workspace est `prompt_ex2.json` v1.1, SHA-256 `5dbd370ae49bb02897327b3f896c4737958065a7e5948fb923bfaf74068483b9`. Aucun fichier nommé `prompt_2.json` n'a été trouvé dans l'espace de fichiers. La conformité revendiquée porte donc sur ce prompt v1.1 accessible, pas sur un éventuel prompt_2 distinct.
