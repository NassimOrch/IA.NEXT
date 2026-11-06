# Audit AAM O94_0

Cette archive contient la base de preuves O94_0 : registre maître et alias, formalismes, rapport de laboratoire, checklists et incidents, reçus O94_0, modules de code reliés à R1–R3, tests cités et références théoriques sélectionnées.

## Architecture auditée

- R1 : conservation des enregistrements structurés ; réponse unique dans le chat ; provenance et diagnostics dans le panneau Détails.
- R2 : récupération RAG avant la génération ; preuve et demande passées séparément ; mode RAG direct explicite ; délégation vers une instance AAM choisie avec garde de récursion.
- R3 : maître → micro-RAG → feuilles sélectionnées ; profondeur progressive ; intégrité hashée ; résolution mémoire hiérarchique de journal événementiel.

## Lire les preuves

1. Commencer par `registre_prouves_O94_0.json` et `formalisme_O94_0.tex`.
2. Vérifier les résultats quantifiés dans `laboratoire_O94_0.tex` et les reçus `logs/O94_0/`.
3. Lire les deux checklists d'incidents : les premières erreurs sont conservées et leurs résolutions font référence aux retests.
4. Vérifier `PACKAGE_MANIFEST.json` et `AUDIT_MANIFEST_SHA256.json` après extraction.

Les statuts PASS sont limités aux tests référencés. Ils n'établissent pas une réussite universelle, ne prouvent pas la vérité factuelle des sources et ne remplacent pas des essais contre des serveurs externes ou du matériel réel.
