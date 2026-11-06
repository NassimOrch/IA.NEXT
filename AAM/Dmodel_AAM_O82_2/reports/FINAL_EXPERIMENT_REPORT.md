# AAM O82 — Rapport expérimental comparatif final

## Description
Cette campagne compare O82 primaire, O82_0, O82_1/O82_c0 et les branches corrigées O82_2/O82_c1 sur le dataset réel SMS Spam Collection, en reprenant également le protocole de généralisation de O81 0.3. Les expériences distinguent apprentissage exact par empreinte, généralisation textuelle, apprentissage itératif, observation dégradée, auto-observation et réponse généralisée avec confiance.

## Architecture
Le pipeline évalué suit `problème -> observation contractuelle -> empreinte -> retrieval mémoire -> suffisance -> policy/observation -> vérification -> mémorisation -> action`, avec une voie secondaire de skill généralisée. O82_2/O82_c1 ajoutent un portfolio de learners, un backend `o81_exact_tree`, refit train-only, correction itérative, planification mémoire-guidée des probes et auto-observation causale.

## Pipeline complet
1. Le corpus anglais de référence est construit depuis `SMSSpamCollection`; les traductions sont utilisées uniquement lorsque leur provenance ID/label/source est démontrée.
2. Les modèles parents O82/O82_0 servent de baseline exact-match.
3. O82_1/O82_c0 évaluent la généralisation textuelle.
4. O82_2/O82_c1 ajoutent refit complet sur TRAIN, portfolio de learners et répétition/correction train-only.
5. Le protocole O81 est reproduit avec un arbre générique et comparé sur les mêmes exemples.
6. Observation dégradée et auto-observation sont testées sur des SMS réels et sous budgets contrôlés.
7. Les sorties sont sauvegardées en JSON et les coûts système sont mesurés séparément.

## Commandes d'exécution
Les commandes reproductibles sont conservées dans `experiments/commands/` et dans les rapports de phase. Exemples :
```bash
cd <racine_version>
PYTHONPATH=src python -W error::ResourceWarning -m unittest discover -s tests
PYTHONPATH=src python scripts/validate_o82.py --output reports/final_validation.json
PYTHONPATH=src python scripts/benchmark_o82.py --output reports/final_benchmark.json
PYTHONPATH=src python -m aam_o82 audit
```
Le benchmark expérimental SMS et les commandes O81 sont fournis séparément dans le dossier d'audit afin de préserver la séparation entre runtime et protocole scientifique.

## Résultats
### Parents
O82 primaire et O82_0 ont la même performance sur le corpus complet : holdout anglais 8,76 % de couverture/exactitude et OOD anglais 10,44 %. Leur couverture multilingue OOD reste quasi nulle.

### O82_1 / O82_c0
Sur le corpus anglais complet, les branches généralisées atteignent environ 81,8 % de couverture avec 81,7 % d'accuracy sur le holdout, et environ 79,8 % de couverture avec 79,4 % d'accuracy sur l'OOD anglais. Leur précision sélective reste proche de 99,8 % holdout et 99,5 % OOD.

Sur 600 perturbations textuelles réelles, la couverture passe d'environ 3,5 % pour les parents à 87,33 % pour les branches corrigées, avec environ 87,0 % d'accuracy globale et 99,6 % de précision parmi les cas couverts.

### O82_2 / O82_c1
Le backend `o81_exact_tree` reproduit le protocole O81 0.3 sur L1 : 94,5 % holdout et 79,75 % OOD. Le backend `rich_generic_tree`, sélectionné sur TRAIN-only lorsqu'il est compétitif, atteint 95,5 % holdout et 85,25 % OOD sur L1.

Sur le petit banc itératif L1, deux cycles de correction augmentent la couverture holdout de 81,5 % à 88,0 % et la couverture OOD de 26,0 % à 33,75 %. Une configuration plus poussée de correction à 0,5 a aussi montré un gain supplémentaire sur O82_2. Ces essais utilisent uniquement TRAIN pour arrêter ou choisir les cycles; le holdout/OOD reste invisible pendant l'apprentissage.

### O81 0.3
Le protocole historique O81 0.3 choisit un `tree_classifier` sur une représentation générique, effectue une sélection interne TRAIN-only puis réentraîne le learner choisi sur tout TRAIN avant l'évaluation. Reproduction L1 : 94,5 % holdout et 79,75 % OOD. Cela explique la généralisation observée : la source principale est l'induction d'une représentation/learner générique et le refit complet, pas la répétition seule.

### Observation dégradée
Sur 8 SMS réels, la politique mémoire-guidée résout les cas avec 2 probes pertinentes contre 5 probes en mode exhaustif. Le coût déclaré des probes est d'environ 0,35 contre 1,35, soit une réduction de 74,07 % du coût agrégé déclaré, sans perte de décision sur ce banc. Le temps mur peut toutefois varier avec le parallélisme et ne doit pas être assimilé au coût agrégé.

### Auto-observation
Sur un scénario réel instrumenté avec désaccord, `enabled=true` produit une planification `SELF_OBSERVE`, une observation interne et une réservation de prochaine probe; `enabled=false` produit zéro événement de ce type. Cette capacité est donc causale et conditionnelle, mais son bénéfice n'est pas universellement démontré : elle dépend du déclencheur, du budget et du problème.

### Langage et réponse généralisée
Les modèles O82 traitent effectivement des SMS en langage naturel et peuvent produire une décision textuelle. Une entrée non vue peut produire une `candidate_response` accompagnée d'une confiance, avec `certified=false`. Exemple réel : une perturbation SMS a produit `ham` avec confiance ≈ 0,9126 tout en restant `UNRESOLVED` sous contrat exact. La confiance est donc un score de confiance gradué, pas une probabilité garantie.

Le test multilingue réduit montre que le learner peut généraliser sans recevoir la métadonnée de langue; la langue est utilisée seulement pour la mesure. Aucune preuve n'établit une génération libre comparable à un LLM.

## Interprétations des résultats
La campagne confirme que l'écart O82 initial/O82_0 était principalement un déficit d'induction et de généralisation, non un manque du dataset. L'ajout d'un learner générique sélectionné et refité sur TRAIN, complété par une boucle d'erreur/correction, transforme le comportement exact-match en généralisation mesurable.

La répétition est utile mais ne doit pas être assimilée à « entraîner jusqu'à obtenir le résultat du test ». La règle correcte est : sélectionner et arrêter à partir d'un signal interne TRAIN-only, puis figer avant de consulter holdout/OOD.

L'observation dégradée est cohérente avec l'idée d'effort minimal : la mémoire réduit le nombre de sondes lorsque l'empreinte courante suffit. L'auto-observation est désormais une action causale et non un simple log.

## Conséquences : théoriques
Le modèle AAM dispose maintenant d'une séparation explicite entre mémoire exacte, compétence généralisée candidate et preuve de certification. Cela évite de convertir une simple confiance en vérité.

La politique de sélection peut utiliser une hiérarchie de compétences sans sacrifier l'acquisition adaptative. Le portfolio préserve également le potentiel d'O81 au lieu de l'écraser.

## Conséquences : conceptuelles
La boucle `observer -> empreinte -> retrieval -> correction -> réobservation -> mémoire` devient compatible avec une stratégie de travail progressif et une économie de sondes. L'auto-observation peut en outre apprendre des événements de contrôle et des instruments externes sans recevoir directement la vérité métier.

## Conséquences : opérationnelles
O82_2/O82_c1 demandent plus de calcul d'apprentissage que leurs parents. Les coûts RSS restent proches des versions corrigées précédentes, tandis que la couverture hors-échantillon augmente fortement. Le benchmark OOD externe reste supérieur sur l'anglais complet, ce qui laisse un espace d'amélioration légitime.

## Conclusions
Les corrections O82_2 et O82_c1 sont objectivement justifiées. Elles ne remplacent pas la mémoire exacte : elles lui ajoutent une voie généralisée contrôlée. Elles ne hardcodent pas de réponses SMS et ne lisent pas le label pendant l'inférence.

La principale conclusion méthodologique est que le succès O81 est reproductible lorsqu'on respecte son protocole d'induction générique + sélection TRAIN-only + refit complet. La répétition/correction améliore en plus la couverture, mais ne suffit pas à elle seule.

## Statut du modèle
**O82_2 : expérimentalement validé sur le périmètre courant, non déclaré comme solution universelle.**

**O82_c1 : expérimentalement validé sur le périmètre courant, non déclaré comme solution universelle.**

Les seules exécutions ayant dépassé le temps de la machine sont conservées comme incidents de ressources/harness et ne sont pas transformées en scores. La dernière campagne finale ne contient aucun défaut modèle ouvert dans la gouvernance.
