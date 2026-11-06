# Delta ORDER80 → ORDER80.1

| Aspect | ORDER80 | ORDER80.1 |
|---|---|---|
| Observation formelle | document/théorèmes activés par lots | unités théorème par théorème |
| Observation documentaire | document | chunks RAG |
| Observation par enfant | dépend fortement de l'état global | cycle complet indépendant par nœud |
| Observation après échec | oui | oui, avec requête et récupération ciblées |
| Web | absent | provider configurable |
| Bibliothèques | absent | racines locales configurables |
| Propagation | retest racine | retest racine + peer probes |
| Décomposition | séquents | même, mais récursive à tous niveaux |
| Vérification | récursive sur arbre de règles, contexte implicite | noyau avec comptage explicite des hypothèses ouvertes + revalidation des lemmes |
| Mémoire | preuves vérifiées | même principe, version rehaussée du format |
| Audit | résumés et logs | + contenu exact observé, trace de noyau détaillée |


## ORDER80.2 correction

Fixed a proof-closure defect in `_projection`: when the requested projection equals its source, the original assumption proof is preserved instead of replacing it by a bare `exact` node. This prevents a global sequent assumption from remaining open in otherwise valid certificates. A focused regression test covers the case.
