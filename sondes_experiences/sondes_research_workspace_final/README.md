# Workspace — recherche sur les sondes adaptatives

Date de création : 2026-10-30

## Objectif

Espace non destructif dédié à l'exécution et à la traçabilité du prompt de recherche révisé (`prompt_ex2.json`). Il sert à reconstruire expérimentalement des sondes adaptatives, étudier l'émergence progressive de la coordination globale, puis vérifier les résultats sur des domaines extérieurs.

## Règles

- Les archives et résultats sources sont conservés dans `versions/sondes_v001__2026-10-30/legacy_reference/` sans modification.
- Chaque campagne substantielle reçoit un nouveau dossier versionné `versions/sondes_vNNN__YYYY-MM-DD/` ; le numéro le plus élevé est la version la plus récente.
- Chaque version possède son propre README, protocole, code, configurations, journaux, résultats bruts/traités, figures, rapports, tests et checksums.
- Aucun dossier abandonné n'est supprimé. Son README indique `ABANDONED`, la date, le motif, les essais, résultats et ressources consommées.
- Les résultats bruts ne sont jamais réécrits silencieusement. Les corrections produisent de nouveaux artefacts versionnés.
- L'exploration ne reçoit aucun plafond arbitraire. Elle dépend des ressources réellement accessibles et des permissions effectives.

## Version courante

Voir [`WORKSPACE_INDEX.md`](WORKSPACE_INDEX.md). La version la plus récente est `sondes_v009__2026-10-30` ; voir `WORKSPACE_INDEX.md`.

## Livrables finaux

- Rapport exécutif : `versions/sondes_v009__2026-10-30/reports/synthese_executive.md`
- Rapport technique : `versions/sondes_v009__2026-10-30/reports/rapport_technique_final.md`
- Audit intégrité/conformité : `versions/sondes_v009__2026-10-30/reports/audit_integrite_et_conformite.md`
- Contrôle reproductible : `versions/sondes_v009__2026-10-30/scripts/audit_delivery.py`
