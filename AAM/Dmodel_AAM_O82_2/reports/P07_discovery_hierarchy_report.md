# AAM O82 — Rapport P07 Découverte, hiérarchie, composition et root-retest

## Description
P07 intègre dans la boucle autoritaire les capacités qui existaient précédemment comme services isolés : découverte validée de probes, autorisation dynamique, observation du probe découvert, décomposition structurelle, exécution de contrats enfants, agrégation de preuves, composition de skills vérifiées et root-retest du problème parent.

## Architecture
Le contrôleur reste l’autorité des transitions. `DISCOVER_PROBE` produit une probe vérifiée sur des partitions train/validation disjointes ; cette probe est enregistrée et ajoutée au contrat effectif. `DECOMPOSE` produit des contrats enfants ; chaque enfant possède son épisode et son budget, puis ses résultats sont agrégés sans réutiliser une preuve non produite. `SkillComposer` admet une composition seulement après validation holdout/OOD. `RootRetester` réexécute le contrat parent avec les capacités nouvellement disponibles, sans récursion de retest dans l’enfant.

## Pipeline complet
`RETRIEVE -> DISCOVER_PROBE -> OBSERVE(discovered probe) -> RETRIEVE -> ... -> RootRetest -> VERIFY` ou `RETRIEVE -> DECOMPOSE -> Child execution -> ChildEvidenceAggregated -> RETRIEVE -> RootRetest -> VERIFY` ; la composition validée déclenche également `skill_composition -> RootRetest`.

## Commandes d'exécution
```bash
cd Dmodel_AAM_O82_0
cat AAM_independent_governance/checklist_erreurs_no_model.json >/dev/null && cat AAM_independent_governance/checklist_erreurs_model.json >/dev/null
PYTHONPATH=src python -W error::ResourceWarning -m unittest tests.test_hierarchy_discovery -v
```

## Résultats
Le gate P07 retourne `10/10 PASS`. La preuve de découverte bout en bout confirme `ProbeDiscovered`, l'autorisation dynamique, `ObservationReceived` pour le probe découvert, `RootRetest` et `RootRetestIntegrated`. La décomposition exécute effectivement les enfants et agrège leurs preuves. La composition positive aboutit à `VERIFIED_SKILL` et programme un root-retest.

## Interprétations des résultats
La capacité de découverte n'est pas une simple API : elle devient une transition atteignable du contrôleur et le produit découvert redevient une capacité admissible du même problème. La hiérarchie est réellement exécutée et non seulement décrite. Le root-retest ferme la boucle entre changement de capacité et revalidation du parent.

## Conséquence
### Théorique
Le système peut enrichir son espace de vues sans transformer une hypothèse de découverte en vérité terminale ; la vérification reste distincte de l'exploration.
### Conceptuelle
La hiérarchie et la découverte deviennent des extensions de l'espace des empreintes et des compétences, avec retour explicite au problème racine.
### Opérationnelle
Les nouveaux probes et compétences sont traçables, autorisés, budgetés et rejouables dans le ledger.

## Conclusions
P07 matérialise la récursivité opérationnelle attendue par `model_AAM_O82.tex` sans coder de réponses métier particulières.

## Statut du model
**P07 = PASS / phase verrouillée.**
