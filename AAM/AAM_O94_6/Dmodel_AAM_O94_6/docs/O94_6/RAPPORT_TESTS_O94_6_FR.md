# Rapport complet d'audit expérimental — AAM O94.6

**Version auditée :** O94.5 comme référence historique; branche de correction et de tests O94.6 (`0.94.6`).  
**Date de campagne :** 20 octobre 2026 (UTC/local timestamps retained in receipts).  
**Statut :** `PASS_BOUNDED` pour les suites et scénarios nommés dans ce rapport. Ce statut ne signifie pas « intelligence générale démontrée » ni « toutes les tâches universelles achevées ».

## 1. Description et portée

L'audit a cherché à reproduire des anomalies signalées dans O94.5, à tester des trajets exécutables hors des simples tests de présentation, à enregistrer les résultats observés, puis à corriger dans O94.6 les défauts récurrents : pertinence RAG par entité, dispatch multi-question, attente de génération longue, observation par outils externes, compilation de compositions et traçabilité de récompense.

Les essais d'évaluation ont utilisé des sources générées spécifiquement pour l'expérience, gardées à part du code et de l'oracle. Lorsque le code de test connaît une valeur attendue, il ne la fournit qu'au vérificateur externe après la réponse ou compare les résultats calculés à partir de l'entrée. L'oracle historique est `real_task_tests/O94_6_replay/oracles/o945_known_answers.json`; il n'est pas ingéré par `AAMRuntime`. SHA-256 : `f85945389996067617500e875c4a4ba9ca254627ea3f204c9dffc5c104e46147`.

Une distinction essentielle est appliquée dans les résultats :

- **RAG-direct/extractif** : AAM sélectionne un passage, en extrait une réponse et en conserve la provenance; aucun LLM n'est appelé pour produire la réponse.
- **Contrat d'adaptateur** : valide que AAM construit et transmet un prompt correctement, route le modèle configuré, gère la réponse et l'erreur; ne valide pas la qualité sémantique d'un LLM si l'adaptateur est une fixture déterministe.
- **LLM local réel** : nécessite que le runtime et les poids correspondants soient présents, chargés et testés. Le poids utilisateur SmolLM2-360M n'était pas présent dans l'environnement de cette campagne; aucune affirmation de génération réelle avec ces poids n'est faite.
- **Observation/reproduction** : l'observation externe d'entrées/sorties ne prouve pas, à elle seule, l'identification de l'algorithme sous-jacent ni sa généralisation.

## 2. Architecture et pipeline audités

Le chemin de requête est, dans l'implémentation O94.6 :

1. créer et valider un `TaskEnvelope` (ou convertir une chaîne en tâche de chat);
2. enregistrer la priorité causale de la requête et suspendre temporairement les actions d'autonomie lorsqu'elles tournent;
3. détecter les questions coordonnées; si plusieurs sont reconnues, créer une tâche enfant pour chacune et exécuter le pipeline standard séparément;
4. observer la pièce jointe ou le contexte RAG selon les autorisations;
5. récupérer les passages pertinents avec provenance, puis choisir la route (`document_retrieval_semantic`, `document_retrieval_lexical`, `language_generation`, etc.) selon la politique configurée;
6. générer une proposition si un modèle est présent, ou utiliser une réponse RAG directe lorsque cette option est explicitement choisie;
7. conserver statut, sources, hashes, route et temps; une réponse lisible ou un code retour réussi ne démontre pas sa vérité;
8. vérifier le résultat uniquement si un vérificateur indépendant est fourni;
9. écrire les événements causaux mémoire/récompense et reprendre l'autonomie après la requête.

`PASS_BOUNDED` indique que le scénario et ses contrôles explicites ont passé; `UNRESOLVED` indique l'absence de réponse résolue; `ERROR`, `TIMEOUT` et `BLOCKED` ne doivent pas être convertis en succès.

## 3. Référence O94.5 : rejeu des sept prompts historiques

**Corpus :** `real_task_tests/O94_6_replay/runtime_generated_knowledge.txt`  
**SHA-256 corpus :** `213524eb987d4750c86518e81aca4450d0e5694da84850e9e7395f5d5f0c5530`  
**Commande :**

```bash
python scripts/o946_replay_o945_regression.py \
  --project-root . \
  --experiment-dir real_task_tests/O94_6_replay
```

**Reçu :** `receipts/O94_6/P1_o945_replay_execution.json`  
**Journal :** `logs/O94_6/P1_o945_replay.log`  
**SHA-256 du rapport d'expérience :** `a166775592ba518562093000063929048135a2b90339a64ce03c57b6fce94c0e`  
**Résultat :** 7 réponses sur 7 concordent avec l'oracle d'évaluation séparé; ingestion 0,217 s, campagne 2,2492 s.

| Prompt exact | Réponse observée | Source citée | Résultat |
|---|---|---|---|
| `Which warehouse is assigned to station GB-42?` | `Warehouse assignment: Station GB-42 is assigned to Warehouse South.` | `[runtime_generated_knowledge.txt#0:213524eb98]` | PASS_BOUNDED |
| `What is the set point for station GB-42?` | `Its set point is -12 C.` | même source | PASS_BOUNDED |
| `How often is the audit cycle for station GB-42?` | `Its audit cycle is every 21 days.` | même source | PASS_BOUNDED |
| `For station FR-27, which warehouse is assigned?` | `Warehouse assignment: Station FR-27 is assigned to Warehouse North.` | même source | PASS_BOUNDED |
| `What is the set point for station FR-27?` | `Its set point is -8 C.` | même source | PASS_BOUNDED |
| `How often is the audit cycle for station FR-27?` | `Its audit cycle is every 14 days.` | même source | PASS_BOUNDED |
| `What is the required action if station GB-42 is above -10 C for 7 minutes?` | `Operations policy Q7.4: For any refrigeration station whose temperature is above -10 C for more than 6 minutes, isolate that station and notify the duty engineer.` | même source | PASS_BOUNDED |

**Interprétation :** la référence confirme le chemin RAG-direct/extractif pour les données présentes; ce n'est pas un test de raisonnement d'un modèle de langage. Les expériences O94.5 originales où le RAG renvoyait la mauvaise entité sont conservées dans `real_task_tests/O94_6_replay/evidence/o945_regression_replay_initial_fail.json` et `receipts/O94_6/P0_baseline_review.json`, pas effacées.

## 4. Test multi-question sur trois attributs d'une entité

**Prompt exact :**

> For station GB-42, which warehouse is assigned? What is its set point? How often is the audit cycle?

**Commande :** `python scripts/o946_compound_query_trial.py`  
**Preuve détaillée :** `real_task_tests/O94_6_replay/evidence/compound_query_gb42.json`  
**Oracle séparé :** `real_task_tests/O94_6_replay/oracles/compound_gb42_expectations.json` (SHA-256 `24d7db4b306d38f08595f55b266a5164a4ff5e447728d97791efe2f346af349a`, non chargé par AAM).  
**Temps total :** 2,7907 s. **Réponse composée :**

```text
Warehouse assignment: Station GB-42 is assigned to Warehouse South.
Its set point is -12 C.
Its audit cycle is every 21 days.
```

Les trois questions ont leurs propres `task_id`, source, statut et réponse : (1) Warehouse South, (2) -12 C, (3) every 21 days. Le reçu indique `subquestion_count=3`, `each_has_source=true`, les trois statuts `PASS_BOUNDED`, sélection de route `multi_question_orchestration`, oracle non utilisé par le runtime, source identique avant/après (`213524eb...5530`).

Le cas multi-question différent figure dans `tests/test_o946_multi_question.py` :

> Which depot is assigned to asset VX-318, what is its nominal set point, and how often is its audit interval?

Réponses : `Depot Juniper`, `-11.5 C`, `17 days`; test spécifique distinct de la requête GB-42. Le test de question absente attend une réponse non résolue, pas le retour arbitraire de l'entité voisine.

## 5. Chat : modèle présent, modèle absent, réponse longue et erreurs

### 5.1 RAG direct sans modèle intégré

Fiche indépendante : `real_task_tests/O94_6_replay/evidence/P7_independent_service_card_source.txt`, SHA-256 `9867ac27e657dde1e70731b76f7606ab20ea7b218779f852c2076f2a525f3bd1`.

**Prompt exact :** `Which warehouse is assigned to service card XD-620?`  
**Réponse observée :** `Service card XD-620: the assigned warehouse is Willow Quay.`  
**Citation :** `[P7_independent_service_card_source.txt#0:9867ac27e6]`  
**SHA-256 de la réponse :** `b34c625599e193637221436e557d92c782af199c4ea1d0a370d8e7f358345265`  
**Reçu :** `real_task_tests/O94_6_replay/evidence/P7_chat_raw_answer_trials.json`.

C'est un test du chemin **sans modèle**, en RAG-direct extractif. AAM ne devrait pas faire croire qu'un LLM a répondu : le reçu donne `backend=rag_direct`, `model_id=null`, `generation_status=RAG_DIRECT_EXTRACTIVE`.

### 5.2 Modèle intégré + RAG : frontière honnête du test

**Prompt exact :** `What is the set point for service card XD-620?`  
**Réponse exacte observée par l'adaptateur de contrat :**

```text
Generated from supplied test context: [[P7_independent_service_card_source.txt#0:9867ac27e6]] Service card XD-620: the assigned warehouse is Willow Quay. The set point is -14.5 C.
```

Référence SHA-256 de la sortie : `27a8d809e411632532d9afade90b72535367e3c019d6fdda7bddd5f65423a4d3`.  
L'adaptateur `P7_protocol_test_adapter.py` renvoie délibérément la première ligne de contexte sélectionné. Il ne contient pas les faits XD-620. Cela teste la construction/transmission du contexte, le branchement de `language_generation`, le choix du modèle et la provenance. **Ce n'est pas un LLM ni une mesure de qualité sémantique.** La sortie est `GENERATED_UNVERIFIED`; son contrôle qualité dit explicitement `PASS_HEURISTIC_NOT_FACT_VERIFIED`.

### 5.3 Modèle présent sans preuve RAG

Prompt : `Please give a short status sentence for this diagnostic request.`  
Sortie de la fixture : `Generated from supplied test context: AUCUNE PREUVE RAG LOCALE N’A ÉTÉ RETROUVÉE.`  
Statut supérieur : `UNRESOLVED`, donc pas de réussite de fond. L'adaptateur reçoit la demande sans passage pertinent; il ne doit pas inventer un fait absent.

### 5.4 Génération longue et erreur de fournisseur

Commande exacte :

```bash
xvfb-run -a python -m pytest -q \
  tests/test_o946_long_generation_ui.py \
  tests/test_o946_model_absent_rag_fallback.py \
  tests/test_o945_chat_unified_pipeline.py::test_integrated_model_execution_failure_is_visible_and_penalizes_generation_reliability \
  -vv --tb=short
```

Reçu `receipts/O94_6/P3_generation_presence_error_final.json`; journal SHA-256 `6e5e3746e6220130b34033ebfb5d05689288cc305388d48a72d7ead62af53353`; résultat : 3 tests sur 3. Le test de génération retarde volontairement un adaptateur de test et lui fait renvoyer une sortie de plus de 20 000 caractères; la fenêtre attend la réponse et l'affiche entièrement, au lieu d'afficher un message vide. Le texte complet exact reste dans le journal et les assertions du test. Le fournisseur en erreur produit un statut visible `ERROR` et une pénalité de fiabilité; il n'est pas remplacé silencieusement.

### 5.5 Capture directe d'une réponse live

Le reçu `receipts/O94_6/P7_live_answer_evidence.json` enregistre le prompt `For service card XD-620, which warehouse is assigned?`, sa source, la sortie textuelle, les hashes et le vérificateur séparé exécuté **après** le `solve()`. Réponse observée : `Service card XD-620: the assigned warehouse is Willow Quay.` Le vérificateur compare ensuite la réponse à `Willow Quay`; il ne transmet pas cette valeur à `solve()`.

## 6. Résolution continue et récompense causale

**Source indépendante :** `Service record RQ-731: the assigned depot is Harbor East. Its set point is -6.5 C. Its inspection interval is every 11 days.`  
**Question :** `For service record RQ-731, which depot is assigned?`  
**Vérification post-résolution :** contient `Harbor East`, appliquée après la sortie. Le runtime a trouvé la contrainte en un essai, avec `selected_route=document_retrieval_semantic`, `elapsed_seconds≈0.597`, et un événement `reward.verified_policy_updated`. Le rapport de run a SHA-256 `79435df0733d14428997d1abb074286da5298d94c84190e590d53b50d303c6b1`; le hash de sortie est `153470ff16cd905062c7b07ec1cf274f361c1a535a32fc21886e5086f77b81de`.

La réponse n'est pas stockée en clair dans le reçu P6, mais le test de capture P7 ci-dessus donne une sortie textuelle intégrale. Le reçu P6 indique `truth_policy`: réussite d'exécution et notation utilisateur ne remplacent pas le vérificateur. La campagne ciblée de six fichiers passe 16/16 : routage et récompense, pipeline chat, multi-question, fallback RAG sans modèle et attente longue.

**Interprétation :** l'adaptation mesurée ici est une adaptation causale bornée des préférences/fiabilités de route et de compétence. Elle ne démontre pas que le mécanisme récompense/penalité engendre, à lui seul, une intelligence générale.

## 7. Programmation compositionnelle : projet multi-fichiers réel et modifiable

**Composition source** : `examples/compositions/O94_6_project_quality_gate.json`, SHA-256 `8af6f0e7233f50752f14d84e0c0a936e1d6390d29f826093872475ecca7ae7cf`.  
**Projet cible** : `examples/compositions/O94_6_quality_gate_demo/`.  
**Commande directe :**

```bash
cd examples/compositions/O94_6_quality_gate_demo
PYTHONPATH=src python -m assetops.cli --input data/assets.json --max-overdue-days 3
```

**Commande compilation/contrôle par composition :**

```bash
cd <racine-O94.6>
python scripts/o946_run_composition_quality_gate.py \
  --project-root examples/compositions/O94_6_quality_gate_demo \
  --variant-limit 2
```

**Briques de base employées dans le graphe :**

- `workbench.validate_request` : contrôle le périmètre de la requête de compilation;
- `workbench.dispatch` : effectue inventaire, vérification syntaxique/bytecode et tests du projet par l'atelier de code;
- `result.attach_integrity` : assemble les résultats et leur intégrité/hashes.

La composition versionnée a 10 nœuds, une séquence avec arrêt sur erreur, un inventaire de projet, une boucle `map` de contrôles par fichier, une condition sur suffixe `.py`, la compilation multi-fichiers, l'exécution des tests, et une sortie JSON contenant résultats et hashes. Elle compile en source Python et bytecode CPython. Le reçu vérifie le round-trip, 6 sources Python compilées, 0 erreur de compilation, et 5 tests de projet passés; l'équivalence interprétée/compilée est vérifiée. Le code source n'a pas d'import ni de fragment arbitraire injecté par le DSL. L'exécution est avec les permissions courantes (pas un bac à sable).

### Sortie exacte de la démonstration (résumé des quatre lignes)

| Identifiant | Dépôt | Jours de retard | Statut | Action |
|---|---|---:|---|---|
| LM-204 | Cedar | 5 | `HOLD_DISPATCH` | Pause dispatch jusqu'à présence d'une entrée d'audit signée. |
| VX-318 | Juniper | 1 | `AUDIT_OVERDUE` | Planifier l'audit en retard et vérifier la signature. |
| QR-509 | Alder | 0 | `AUDIT_DUE` | Effectuer l'audit maintenant. |
| TS-404 | Birch | 0; échéance dans 5 jours | `MONITOR` | Continuer à surveiller. |

Le vérificateur indépendant recalcule `days_since_last_audit - audit_interval_days` depuis le JSON, puis recalcule les statuts; il n'utilise pas la sortie du compositeur comme oracle. Compteurs : 1 `HOLD_DISPATCH`, 1 `AUDIT_OVERDUE`, 1 `AUDIT_DUE`, 1 `MONITOR`. Le reçu complet et les sources compilées sont sous `real_task_tests/O94_6_replay/evidence/composition_quality_gate/`.

**Frontière d'affirmation :** cela démontre la composition/compilation/exécution d'un workflow d'outils approuvés sur un projet multi-fichiers. L'application d'exemple est un artefact indépendant utilisé pour l'évaluation; le rapport ne dit pas qu'AAM a inventé seul tout le code d'un éditeur de code depuis une instruction en langage naturel.

## 8. Observation d'un processus et reproduction

**Cible externe** : `real_task_tests/O94_6_replay/observed_process/invoice_pipeline_target.py`  
**SHA-256 cible** : `304f0c4c83139ff1b53693c40d6dc73b7b8509b737dfe6e086fc64775d1f16d9`  
**Commande capture/rejeu :** `python scripts/o946_observe_invoice_pipeline.py`  
**Trace JSONL SHA-256** : `afaa23890158ca064018143605d3439eb1cee790fd1ef3ad220fe1a2572c7e38`  
**Capsule SHA-256** : `b4785df4c13e61a5b6e70ee0af302d68d3ee2b3bb09258b2ecfa8e957acfe587`  
**Réplique autonome SHA-256** : `64d7b90216c610cb2b2d22156c7db7440eb40ee29b139972cf667213dfa00b78`.

Le processus traite une facture en plusieurs étapes (`schema_validation`, `line_normalization`, `discount_and_tax`, `finalization`). Exemple réel capturé pour `INV-A101` : deux lignes, sous-total 26 497 centimes, remise 1 325, base taxable 25 822, TVA 5 164, livraison 650, total 30 986 centimes, statut `SETTLED`. La capture exécute la cible comme un sous-processus; elle n'importe pas le code cible.

**Résultats de généralisation :** 8 paires capturées, 6/6 entrées d'apprentissage rejouées à l'identique; les deux cas tenus à l'écart donnent `UNRESOLVED` (0/2 correspondance exacte). Le programme autonome rejoue une table de comportement sur les clés observées, il ne reconstruit pas la logique de facturation générale. Le dossier `observed_process/README_REPRODUCTION_SUR_PC.md` fournit les commandes Windows et Linux/macOS et décrit la vérification des hashes/checkpoints. Répétez ce test sur votre PC pour vérifier l'exécution locale et les droits OS; le travail effectué dans ce conteneur n'a pas observé votre PC physique.

## 9. Évaluation des questions et résultats

### 9.1 « Pourquoi la programmation compositionnelle serait-elle le futur ? »

Il est plus juste de dire qu'elle est **un candidat important**, pas que son adoption universelle est certaine. Ses avantages vérifiables : réutilisation de blocs, explicitation des dépendances, validation par étapes, inspection des composants, compilation reproductible et possibilité de remplacer un bloc sans reconstruire toute l'application. Ses défis : concevoir des contrats stables, debugger les graphes, traiter les effets de bord, versionner les composants et maîtriser les permissions d'exécution. Les langages textuels restent utiles pour les algorithmes, les optimisations, les abstractions non graphiques et les systèmes existants; les deux approches peuvent coexister.

### 9.2 « Pourquoi la réponse longue était-elle vide ? »

Le défaut O94.5 venait du trajet asynchrone/UI : la demande longue pouvait ne pas rester en attente avec une sortie visible jusqu'à la fin. La correction O94.6 est testée par un adaptateur à réponse différée et une sortie de plus de 20 000 caractères; le test vérifie l'attente et la présence de la sortie complète. Les tests vérifient aussi qu'un échec du fournisseur soit présenté et sanctionné dans la fiabilité, plutôt que caché par un fallback silencieux.

### 9.3 État des modèles locaux et SmolLM2

L'intégration accepte des dossiers Transformers et des fichiers de poids pris en charge accompagnés de leur configuration/tokenizer; le registre peut aussi connecter un adaptateur Python personnalisé approuvé avec SHA-256. Cependant, **les poids SmolLM2-360M de l'utilisateur n'étaient pas fournis dans cette session et Transformers n'a pas pu être installé à cause de l'absence de résolution DNS vers l'index de paquets**. Les tests du contrat d'adaptateur ne prouvent donc pas que ces poids ont été chargés, générés ou entraînés ici. Le guide indique les prérequis pour refaire le test sur le PC qui possède les poids et dépendances.

## 10. Commandes de reproduction des preuves

À lancer depuis la racine d'un O94.6 extrait :

```bash
# Contrôle de version et préflight
python scripts/preflight_o946.py
python -m aam_o93 --workspace /tmp/aam-o946-status status

# Rejouer le corpus de sept questions
python scripts/o946_replay_o945_regression.py --project-root . --experiment-dir real_task_tests/O94_6_replay

# Multi-question avec sources et traces séparées
python scripts/o946_compound_query_trial.py

# Projet composé/compilation/exécution
python scripts/o946_run_composition_quality_gate.py --project-root examples/compositions/O94_6_quality_gate_demo --variant-limit 2

# Observation du processus externe + mise à jour des checkpoints/capsule
python scripts/o946_observe_invoice_pipeline.py

# Régression chat, récompense, multi-question, absence de modèle, génération longue
xvfb-run -a python -m pytest -q \
  tests/test_o945_causal_reward_routing.py \
  tests/test_o945_reward_runtime_integration.py \
  tests/test_o945_chat_unified_pipeline.py \
  tests/test_o946_multi_question.py \
  tests/test_o946_model_absent_rag_fallback.py \
  tests/test_o946_long_generation_ui.py
```

Pour une campagne graphique, utiliser Xvfb sous Linux sans écran; sur Windows, lancer `run_AAM_O94_6.bat` ou `run_AAM_O94_6.ps1`. Les reçus sont JSON, les journaux texte conservent les sorties brutes et leurs hashes. Le manifeste `sav_AAM_O94_6/savepoint_manifest.json` établit l'intégrité de la source immuable et du delta O94.6.

## 11. Conséquences

### Théoriques
La séparation observation brute / vues décodées / empreinte / preuve et le traitement des questions indépendamment rend les hypothèses auditées plus explicites. La capsule actuelle révèle néanmoins une distinction fondamentale : mémoriser des observations n'est pas encore inférer l'algorithme qui les a causées.

### Conceptuelles
Une compétence n'est validée que dans le périmètre de ses tests; une composition est vérifiable quand ses briques, entrées, effets et sorties sont traçables. Les récompenses opérationnelles indiquent la fiabilité d'exécution mais ne remplacent pas une preuve indépendante de vérité.

### Opérationnelles
O94.6 donne les sources, commandes, rapports, données et artefacts nécessaires pour répéter les scénarios. Les scénarios boîte noire doivent être rejoués sur le PC du propriétaire pour confirmer le contexte et les permissions propres à ce système. Le contenu généré par un modèle demeure `GENERATED_UNVERIFIED` tant qu'une vérification indépendante ne le confirme pas.

## 12. Conclusions et statut

Les corrections O94.6 établies par des tests portent principalement sur le RAG par entité, le dispatch multi-question, la génération asynchrone, l'observation outil, le compositeur/compilateur et le retour causal. Les preuves positives de ce rapport sont bornées aux données, réglages, logiciels et commandes cités. Le test de généralisation de la capsule est négatif (0/2 holdouts); il est publié tel quel. L'intégration des poids SmolLM2 réels n'a pas été validée sur cette machine. L'objectif d'AAM reste plus large que ce qui peut être inféré de ces mesures; ni succès universel ni échec universel ne sont déduits.

**Statut de cette campagne : `PASS_BOUNDED` pour les scénarios nommés; limites majeures en attente pour l'inférence SmolLM2 réelle et la généralisation d'observation.**

## 13. Preuves brutes complémentaires P7 : question, modèle absent, modèle branché et génération longue

Les reçus suivants ont été produits après la rédaction initiale du rapport et sont conservés dans `real_task_tests/O94_6_replay/evidence/`. Ils incluent les prompts exacts, sorties, temps, sources, empreintes et les limites de la fixture utilisée.

### 13.1 Modèle absent, source RAG présente

Source : `P7_independent_service_card_source.txt`, SHA-256 `9867ac27e657dde1e70731b76f7606ab20ea7b218779f852c2076f2a525f3bd1`.

Prompt : `Which warehouse is assigned to service card XD-620?`

Réponse exacte : `Service card XD-620: the assigned warehouse is Willow Quay.`

SHA-256 de la réponse : `b34c625599e193637221436e557d92c782af199c4ea1d0a370d8e7f358345265`.

Reçu : `P7_chat_raw_answer_trials.json`. Route : `rag_direct`, aucun modèle intégré. Résultat : passage extractif et source traçable; ce n'est pas une réponse de LLM.

### 13.2 Modèle de protocole branché avec source RAG

Prompt : `What is the set point for service card XD-620?`

Sortie exacte :

```text
Generated from supplied test context: [[P7_independent_service_card_source.txt#0:9867ac27e6]] Service card XD-620: the assigned warehouse is Willow Quay. The set point is -14.5 C.
```

SHA-256 : `27a8d809e411632532d9afade90b72535367e3c019d6fdda7bddd5f65423a4d3`.

L'adaptateur `P7_protocol_test_adapter.py` extrait le passage fourni dans le prompt. Il ne porte pas le fait métier dans son code. Cela démontre le routage et le passage du contexte, pas la qualité sémantique d'un modèle de langage. Le reçu marque la sortie `GENERATED_UNVERIFIED`.

### 13.3 Modèle de protocole branché sans RAG

Prompt : `Please give a short status sentence for this diagnostic request.`

Sortie exacte : `Generated from supplied test context: AUCUNE PREUVE RAG LOCALE N’A ÉTÉ RETROUVÉE.`

Statut : `UNRESOLVED`; aucune source n'est citée. Cette fixture n'a pas de connaissance du monde et ne prétend pas remplacer un vrai LLM.

### 13.4 Trois questions dans une seule requête

Prompt : `Which warehouse is assigned to service card XD-620? What is its set point? How often is its inspection interval?`

Réponse exacte :

```text
1. Which warehouse is assigned to service card XD-620?
Service card XD-620: the assigned warehouse is Willow Quay.

2. Regarding card XD-620, What is its set point?
The set point is -14.5 C.

3. Regarding card XD-620, How often is its inspection interval?
The inspection interval is every 19 days.
```

SHA-256 de la réponse composée : `c19d6dce09ea6c8ff958d3d77f278253204ec1785f5b27d8f7b546d840ff8b1d`. La répartition et l'ordre sont testés; le contenu vient des sources récupérées.

### 13.5 Exemple demandé : capitale du Japon

Source de test indépendante : `P7_capital_japan_independent_source.txt` (SHA-256 `85a7c7851b8dc32cf5aacef8fb206b3ab3bed159bc423faebae092772b3334f6`) contenant `Geography reference JPN-104: the capital city of Japan is Tokyo.`

Prompt : `What is the capital of Japan?`

- Avec RAG et sans modèle intégré : `Geography reference JPN-104: the capital city of Japan is Tokyo.` (SHA-256 `7f06ba3883681a8c5e40956b73a9f49a5d6d353923c542b791ebea94fa6f3269`).
- Avec l'adaptateur et RAG : `Context-grounded test response: [[P7_capital_japan_independent_source.txt#0:85a7c7851b]] Geography reference JPN-104: the capital city of Japan is Tokyo.` (SHA-256 `fd337a5e4d3b6dd8ed68099b6404a6bda489e03264dbe0fe2b6079da9940c4a1`).
- Avec l'adaptateur et sans RAG : `Context-grounded test response: AUCUNE PREUVE RAG LOCALE N’A ÉTÉ RETROUVÉE.`; statut `UNRESOLVED` attendu.

Reçu complet : `P7_capital_chat_evidence.json`. L'adaptateur est générique et ne contient pas la valeur Tokyo; celle-ci vient du fichier source. C'est un essai de branchement du pipeline, pas une preuve qu'un LLM réel sait répondre sans son corpus.

### 13.6 Génération longue et affichage du transcript

Prompt : `Produce a detailed status after a deliberately delayed generation; preserve the complete output.`

Sortie : 58 199 caractères, durée 3,2248 s, SHA-256 `fa0c90e8de700034df9f1a935864e6cbee1401c5f436cafe5e30661528e514fd`. Le premier et le dernier marqueur étaient visibles dans le transcript (`first_segment_visible_in_chat=true`, `last_segment_visible_in_chat=true`); hash du transcript visible `0433ad146727275a001c9d74565f1dab54583bcc8a5ebfbca91b862a9215bec3`.

Reçu : `P7_long_generation_raw_evidence.json`. Il s'agit d'une fixture déterministe de test destinée à vérifier le transport et l'affichage d'une sortie longue, et non d'un LLM.

## 14. État de l'observation complexe et de la reproduction

Le processus de facturation a été exécuté dans un sous-processus indépendant. La capture possède huit paires; les six paires d'entraînement se rejouent exactement et les deux cas exclus restent `UNRESOLVED`. Cela prouve un rejeu exact sur les cas observés, pas l'inférence de la logique générale. Le script `scripts/o946_observe_invoice_pipeline.py`, la cible, les cas, les traces, le checkpoint et la capsule sont dans l'archive. La section PC du guide détaille comment l'exécuter localement. La capture de ce rapport a été faite dans l'environnement d'audit et ne doit pas être présentée comme une observation déjà réalisée sur le PC de l'utilisateur.

## 15. Réserve sur les véritables modèles de langage

Le modèle SmolLM2-360M et ses poids n'étaient pas montés dans l'environnement. Le chargement Transformer par poids utilisateur n'est donc pas considéré comme validé par ces essais. Tous les résultats utilisant `python_adapter` sont explicitement étiquetés comme adaptateur de contrat. Il faut exécuter un test local avec le dossier SmolLM2 complet (configuration, tokenizer, poids) pour certifier ce chemin sur le vrai modèle.


## 16. Rejeu autonome de la capsule sur un PC Windows/Linux/macOS

Les artefacts de reproduction locale sont fournis dans `real_task_tests/O94_6_replay/observed_process/`: `invoice_replay_inputs_train.jsonl` (six entrées observées, sorties attendues absentes du fichier), `invoice_replay_inputs_holdout.jsonl` (deux entrées jamais ajoutées à la capsule) et `invoice_replica_standalone.py`. Le wrapper `scripts/o946_replay_invoice_capsule_demo.py` imprime les réponses JSON et un résumé de statut.

Commandes depuis la racine décompressée :

```bash
python scripts/o946_replay_invoice_capsule_demo.py --split train
python scripts/o946_replay_invoice_capsule_demo.py --split holdout
```

Sous Windows :

```powershell
py -3 scripts\o946_replay_invoice_capsule_demo.py --split train
py -3 scripts\o946_replay_invoice_capsule_demo.py --split holdout
```

Résultat du rejeu de six entrées observées :

| Facture observée | Devise | Total produit par la cible (centimes) | Résultat de la capsule |
|---|---:|---:|---|
| INV-A101 | EUR | 30 986 | `PASS_BOUNDED_EXACT_MATCH` |
| INV-A102 | USD | 9 737 | `PASS_BOUNDED_EXACT_MATCH` |
| INV-A103 | GBP | 19 309 | `PASS_BOUNDED_EXACT_MATCH` |
| INV-A104 | EUR | 10 433 | `PASS_BOUNDED_EXACT_MATCH` |
| INV-A105 | CAD | 41 019 | `PASS_BOUNDED_EXACT_MATCH` |
| INV-A106 | JPY | 4 373 | `PASS_BOUNDED_EXACT_MATCH` |
| HOLDOUT-B201 | EUR | 31 589 dans la trace de la cible; aucune sortie répliquée | `UNRESOLVED` |
| HOLDOUT-B202 | USD | 15 876 dans la trace de la cible; aucune sortie répliquée | `UNRESOLVED` |

Le wrapper de rejeu a été exécuté ici avec code retour 0 dans les deux modes : six sorties avec `PASS_BOUNDED_EXACT_MATCH`; deux sorties `UNRESOLVED`. Les reçus shell sont `logs/O94_6/P7_invoice_replica_train_demo.stdout.json` et `logs/O94_6/P7_invoice_replica_holdout_demo.stdout.json`. Ce succès évalue le comportement défini de la capsule; il n'affirme pas qu'elle a inféré la formule générale des factures. Le processus complet observé et ses sorties sont dans `invoice_observation_trace.jsonl` et `observed_invoice_process.json`.


## 17. Correction issue de la suite complète P8 (rejouée après correction)

### 17.1 Incident initial conservé

L’extraction candidate précédente a exécuté 442 tests et imprimé `438 passed, 4 failed, 140 warnings, 21 subtests passed in 301.63s`. Le code retour final du lanceur était `124` (`TIMEOUT_OR_INTERRUPTED`) car le processus ne s’est pas arrêté après le résumé; il a émis des exceptions de finalisation Tkinter (`RuntimeError: main thread is not in main loop`). Ce reçu est conservé à `receipts/O94_6/P8_candidate3_full_suite.json` et **n’est pas considéré comme un succès global**.

Les quatre échecs précis étaient :

1. `test_chat_rag_passes_retrieved_evidence_to_actually_trained_model` — la route choisie devenait `language_generation_after_rag_no_evidence` au lieu de la route RAG attendue.
2. `test_chat_without_a_valid_generator_is_explicitly_extractive` — l’extraction n’incluait pas le fait source `18 degrees Celsius`.
3. `test_explicit_local_backend_receives_o93_semantic_context_not_legacy_search` — le contexte RAG ne passait pas au backend attendu.
4. `test_o945_preflight_uses_release_specific_phase_gate` — l’ancien test exigeait que le garde parent O94.5 accepte un arbre descendant qui a volontairement modifié des chemins communs.

### 17.2 Cause et correction

Le premier défaut a été reproduit sur un document source créé pour l’essai. L’expression régulière des identifiants reconnaissait le groupe grammatical français `faut-il` comme identifiant d’entité; le garde par identifiant écartait ensuite l’unique source pertinente. Les fonctions `tokenize()` et `content_tokens()` partagent maintenant un contrat plus prudent : préfixe acronymique en majuscules, ou suffixe contenant un chiffre. Ainsi `LM-204`, `GB-42` et `Kestrel-17` restent des identifiants atomiques, alors que `faut-il` n’en est plus un. Aucun fait `18 degrees Celsius` n’a été ajouté au runtime.

Le quatrième échec était un contrat de test parent/enfant. O94.5 est immuable; son garde doit refuser les fichiers O94.5 modifiés dans la branche O94.6. Le test enfant vérifie maintenant ce refus parent et demande séparément `PASS_BOUNDED` au garde O94.6, lequel vérifie l’overlay et le snapshot parent indépendant.

### 17.3 Rejeu

Commande :

```bash
python -m pytest -q tests/test_o931_chat_pipeline.py tests/test_o946_hyphenated_entity_disambiguation.py tests/test_o946_entity_rag.py tests/test_o945_standalone_preflight.py
```

Résultat : **18 passed in 21.91s**, code retour `0`, aucune assertion échouée. Reçu : `receipts/O94_6/P8_rag_entity_parent_gate_retest2.json`; journal brut : `logs/O94_6/P8_rag_entity_parent_gate_retest2.log`; SHA-256 du journal : `3ebb8deb0511f61fe4583de588a3d1d5c88f3f0dc772e5969aeeed1b75e2a111`.

Ce rejeu valide ces quatre familles de régression, mais ne remplace pas une suite intégrale fraîche après le correctif. Le nouvel essai intégral sera exécuté avec `scripts/o946_pytest_exit_safe.py`, dont la seule différence est d’éviter la phase de fermeture de l’interpréteur après que pytest a déjà rendu son code retour; les erreurs du corps des tests et le code retour pytest restent visibles et déterminants.


## 18. Rejeu complémentaire après correction du rappel d’entités et du harnais

Cette section ajoute des re-tests P8 postérieurs aux reçus historiques de la section 17. Les reçus d’échecs initiaux restent conservés; cette section ne les remplace pas. Les sorties du runtime et les oracles d’évaluation restent séparés.

### 18.1 Rappel RAG, entités structurées et requêtes multiples

Incident reproduit : la requête `À quelle température faut-il stocker la batterie Velorin ?` était classée `NO_MATCH`, car `faut-il` était transformé en pseudo-identifiant. Le corpus indépendant contient `The Velorin battery must be stored at 18 degrees Celsius.` et a été créé dans le test, pas dans la base de code. La correction reconnaît `LM-204`, `GB-42` et `Kestrel-17` comme identifiants structurés mais ne verrouille plus les hyphens grammaticaux ordinaires comme identifiants. Le test exige explicitement la présence de `18 degrees Celsius` dans les résultats et l’absence de `__entity__faut-il`.

Le batch multi-question emploie aussi trois attributs d’actifs distincts, créés dans le corpus de test :

- Prompt A : `For asset LM-204, which depot is assigned? What is its nominal set point? How often is its audit interval?`
- Source indépendante : `Asset LM-204 is assigned to Depot Cedar. Its nominal set point is -7 C. Its audit interval is every 9 days.`
- Réponses d’évaluation attendues : dépôt `Cedar`, consigne `-7 C`, intervalle `9 days`. Ces valeurs ne sont pas présentes dans le code d’AAM; le test valide les réponses après exécution.

Commande et résultat exacts :

```bash
python -m pytest -q tests/test_o931_chat_pipeline.py tests/test_o946_entity_id_extraction.py tests/test_o946_entity_rag.py tests/test_o946_hyphenated_entity_disambiguation.py tests/test_o946_multi_question.py -vv --tb=short
```

Résultat : **22 passed in 22.85s**, code retour 0, `PASS_BOUNDED`. Journal : `logs/O94_6/P8_chat_rag_multique.log`; SHA-256 : `b5e50a7b79c0405a9c27599ea03145a3f81ac5d8e274b78c9b2d736ada8f6a85`. Reçu : `receipts/O94_6/P8_chat_rag_multique.json`. Un précédent rejeu ciblé des 18 tests RAG/parent-gate a également passé (reçu `P8_rag_entity_parent_gate_retest2.json`), ce qui distingue les corrections fonctionnelles du test d’identité parent-enfant.

### 18.2 Génération longue, absence de modèle et erreurs de fournisseur

Commande :

```bash
python -m pytest -q tests/test_o946_long_generation_ui.py tests/test_o946_generation_timeouts.py tests/test_o946_model_absent_rag_fallback.py tests/test_o945_chat_unified_pipeline.py -vv --tb=short
```

Résultat : **7 passed in 20.67s**, code retour 0. La sortie lente complète arrive dans le transcript; un fournisseur HTTP qui dépasse son délai produit une erreur explicite et n’est pas signalé comme succès; sans modèle intégré, `rag_direct` répond depuis la source observée. Ce lot inclut également la génération via le chat Tk sous Xvfb, l’échec explicite d’un adaptateur et le décodage d’une pièce jointe via le vrai outillage local. Reçu : `receipts/O94_6/P8_generation_long_wait_model_absent_and_chat_integrated.json`; journal SHA-256 : `7f44a85b1e29c625aa849b408aaf94712bc06da37227ac49ec61576c3ed2355d`.

### 18.3 Observation multimodale, compilation compositionnelle et récompense

Commande :

```bash
python -m pytest -q tests/test_o945_observation_multimedia_ffmpeg.py tests/test_o945_observation_reward.py tests/test_o945_composition_compiler_workbench.py tests/test_o946_release_identity.py -vv --tb=short
```

Résultat : **13 passed in 11.45s**, code retour 0. Les tests lancent FFmpeg/FFprobe pour des fichiers audio/vidéo d’essai, Tesseract pour l’OCR d’une image et d’un PDF scanné, suivent empreintes/rapport et testent le workbench compositionnel : compilation Python/bytecode, exécution, sauvegarde, conflit de modification et annulation. Les fragments Python arbitraires restent rejetés. Reçu : `receipts/O94_6/P8_composition_observation_reward_release_identity.json`; journal SHA-256 : `91ba5b2043b178b5c987c8e3e6ab2e82f1dc6ab0ee96465a5eddd6cfc20108f9`.

### 18.4 Résolution continue, retour causal, autonomie et dispatch de compositions

Commande :

```bash
python -m pytest -q tests/test_o945_causal_reward_routing.py tests/test_o945_reward_runtime_integration.py tests/test_o94_trace_resolution_reward.py tests/test_o94_continuous_resolution_ui.py tests/test_o945_chat_composition_dispatch.py tests/test_p6_autonomy.py -vv --tb=short
```

Résultat : **19 passed in 15.40s**, code retour 0. Le lot vérifie que les trois dimensions (fiabilité d’exécution, note utilisateur, validation indépendante) restent distinctes, que les mises à jour causales sont idempotentes, que les routes admissibles s’adaptent après un échec et qu’un résultat n’est pas déclaré vérifié sans vérificateur explicite. Reçu : `receipts/O94_6/P8_continuous_resolution_causal_reward_composition_dispatch.json`; journal SHA-256 : `26dacc2d129813629d4624c5e53abab8882900cbd381ac835518ba0d13204453`.

### 18.5 Résilience du runner et essais non concluants conservés

Un lancement de lot initial a échoué avant collecte avec `ModuleNotFoundError: aam_o93`; le runner ne plaçait pas la racine du projet dans `sys.path`. Un autre lancement n’a pas généré de reçu parce que la fermeture du pipe de sortie attendait un descendant après l’arrêt de `xvfb-run`. Le runner a été corrigé pour ajouter la racine et pour démarrer `xvfb-run` dans un groupe de processus avec délai dur et terminaison de tout le groupe. Un test de contrôle volontaire a imposé un délai de 2 s à une fixture qui attendait 20 s : reçu `TIMEOUT`, code de terminaison `SIGTERM_PROCESS_GROUP`, durée mesurée 2,0073 s, reçu toujours écrit (`P8_runner_timeout_branch_smoke.json`). Cet essai est un test de harnais, **pas** un échec du modèle.

Les quatre reçus fonctionnels ci-dessus totalisent 61 tests passés dans des processus séparés. Certains tests historiques déjà utilisés ailleurs dans le rapport se recoupent avec ces batteries; les nombres ne doivent pas être additionnés au compte historique global comme s’il s’agissait tous de tests uniques. Le précédent run complet avec 4 échecs et teardown bloqué reste enregistré comme échec historique; aucune affirmation de « suite complète O94.6 intégralement verte » n’est faite sur sa base.


## 19. Matrice exhaustive segmentée O94.6

La suite complète a été exécutée depuis la racine O94.6 en 12 processus isolés, avec huit fichiers de test par lot (quatre dans le dernier). Chaque fichier `tests/test_*.py` recensé a été exécuté exactement une fois dans cette matrice. Les reçus individuels et journaux bruts sont conservés dans `receipts/O94_6/` et `logs/O94_6/`.

**Résultat : `PASS_BOUNDED`; 92/92 fichiers exécutés, 448 réussites cumulées par lot, 0 échec, 0 timeout, 12/12 lots `PASS_BOUNDED`.** Le nombre 448 est la somme des compteurs des processus pytest, pas une promesse de 448 identifiants de test uniques lorsque l’on additionne aussi les campagnes ciblées répétées plus tôt dans ce rapport.

| Lot | Fichiers | Réussites pytest | Échecs | Durée (s) | Reçu |
|---|---:|---:|---:|---:|---|
| P8_full_matrix_01_of_12 | 8 | 28 | 0 | 47.431 | `receipts/O94_6/P8_full_matrix_01_of_12.json` |
| P8_full_matrix_02_of_12 | 8 | 48 | 0 | 58.469 | `receipts/O94_6/P8_full_matrix_02_of_12.json` |
| P8_full_matrix_03_of_12 | 8 | 33 | 0 | 37.718 | `receipts/O94_6/P8_full_matrix_03_of_12.json` |
| P8_full_matrix_04_of_12 | 8 | 24 | 0 | 24.124 | `receipts/O94_6/P8_full_matrix_04_of_12.json` |
| P8_full_matrix_05_of_12 | 8 | 24 | 0 | 17.581 | `receipts/O94_6/P8_full_matrix_05_of_12.json` |
| P8_full_matrix_06_of_12 | 8 | 27 | 0 | 19.971 | `receipts/O94_6/P8_full_matrix_06_of_12.json` |
| P8_full_matrix_07_of_12 | 8 | 15 | 0 | 26.503 | `receipts/O94_6/P8_full_matrix_07_of_12.json` |
| P8_full_matrix_08_of_12 | 8 | 34 | 0 | 13.458 | `receipts/O94_6/P8_full_matrix_08_of_12.json` |
| P8_full_matrix_09_of_12 | 8 | 72 | 0 | 34.853 | `receipts/O94_6/P8_full_matrix_09_of_12.json` |
| P8_full_matrix_10_of_12 | 8 | 49 | 0 | 43.257 | `receipts/O94_6/P8_full_matrix_10_of_12.json` |
| P8_full_matrix_11_of_12 | 8 | 53 | 0 | 58.522 | `receipts/O94_6/P8_full_matrix_11_of_12.json` |
| P8_full_matrix_12_of_12 | 4 | 41 | 0 | 4.557 | `receipts/O94_6/P8_full_matrix_12_of_12.json` |

Commande de campagne utilisée par l’orchestrateur : exécution de `scripts/run_o946_test_batch.py` pour chacun des douze lots, avec `pytest -q ... -vv --tb=short`, puis actualisation du snapshot et vérification du gate après chaque lot. La définition de la matrice, les douze listes de fichiers et les hashes de journaux se trouvent dans `receipts/O94_6/P8_segmented_full_test_matrix.json`; le résumé brut contenant les chemins du poste de travail est conservé comme `P8_segmented_full_test_matrix_raw_workspace_paths.json`. Le journal d’orchestration est `logs/O94_6/P8_segmented_full_test_matrix_orchestrator.log`.

Cette matrice résout l’incident historique du runner monolithique qui pendait lors du teardown Tk : ce défaut de harnais n’est pas effacé, mais une alternative segmentée a exécuté l’ensemble des 92 fichiers sans timeout. Les cinq avertissements TorchScript relevés dans d’autres campagnes ciblées restent à traiter/considérer comme avertissements de dépréciation; la matrice segmentée présente ici n’a pas produit d’avertissements dans ses reçus.

La conclusion demeure bornée à l’environnement de test. Cette suite ne prouve pas le chargement réel du fichier SmolLM2 de l’utilisateur (poids non présents dans cette session), ni l’accès aux capteurs physiques/PC de l’utilisateur, ni la généralisation de la capsule d’observation à ses deux cas hors-échantillon. Les preuves et procédures de rejeu local sont fournies séparément.


## 20. Matrice exhaustive exécutée sur une extraction neuve du ZIP candidat

Après la matrice de 92 fichiers sur le workspace source (section 19), le ZIP candidat a été extrait dans un répertoire neuf : `package_verify/model_candidate_extract`. Les checks CRC, les chemins ZIP, les deux manifestes racine, le préflight O94.6 et `compileall` ont réussi avant les essais. Les 92 fichiers `tests/test_*.py` de cette extraction ont ensuite été exécutés exactement une fois dans 12 processus indépendants avec des reçus distincts.

**Résultat sur extraction neuve : `PASS_BOUNDED`; 92/92 fichiers exécutés, 448 réussites cumulées, 0 échec, 0 timeout; 12/12 lots validés.** Après la dernière batterie, le manifeste interne a encore été vérifié (`2781` fichiers, `bad_count=0`), le préflight était `PASS_BOUNDED`, et `compileall` n’a produit aucune erreur.

| Lot | Fichiers | Réussites pytest | Échecs | Durée (s) | Reçu d’extraction |
|---|---:|---:|---:|---:|---|
| P8_extract_matrix_01_of_12 | 8 | 28 | 0 | 57.149 | `receipts/O94_6/P8_extract_matrix_01_of_12.json` |
| P8_extract_matrix_02_of_12 | 8 | 48 | 0 | 48.908 | `receipts/O94_6/P8_extract_matrix_02_of_12.json` |
| P8_extract_matrix_03_of_12 | 8 | 33 | 0 | 38.719 | `receipts/O94_6/P8_extract_matrix_03_of_12.json` |
| P8_extract_matrix_04_of_12 | 8 | 24 | 0 | 21.441 | `receipts/O94_6/P8_extract_matrix_04_of_12.json` |
| P8_extract_matrix_05_of_12 | 8 | 24 | 0 | 17.989 | `receipts/O94_6/P8_extract_matrix_05_of_12.json` |
| P8_extract_matrix_06_of_12 | 8 | 27 | 0 | 18.240 | `receipts/O94_6/P8_extract_matrix_06_of_12.json` |
| P8_extract_matrix_07_of_12 | 8 | 15 | 0 | 22.328 | `receipts/O94_6/P8_extract_matrix_07_of_12.json` |
| P8_extract_matrix_08_of_12 | 8 | 34 | 0 | 12.462 | `receipts/O94_6/P8_extract_matrix_08_of_12.json` |
| P8_extract_matrix_09_of_12 | 8 | 72 | 0 | 33.244 | `receipts/O94_6/P8_extract_matrix_09_of_12.json` |
| P8_extract_matrix_10_of_12 | 8 | 49 | 0 | 33.860 | `receipts/O94_6/P8_extract_matrix_10_of_12.json` |
| P8_extract_matrix_11_of_12 | 8 | 53 | 0 | 50.961 | `receipts/O94_6/P8_extract_matrix_11_of_12.json` |
| P8_extract_matrix_12_of_12 | 4 | 41 | 0 | 4.352 | `receipts/O94_6/P8_extract_matrix_12_of_12.json` |

Les journaux pytest bruts sont `logs/O94_6/P8_extract_matrix_XX_of_12.log`, les journaux de conduite sont les fichiers `*_driver.log` associés, et chacun a un SHA-256 enregistré dans `receipts/O94_6/P8_fresh_extract_full_matrix.json`. La commande de chaque lot utilise `scripts/run_o946_test_batch.py` de l’extraction, qui exécute `xvfb-run -a python -m pytest -q ... -vv --tb=short` avec délai dur et reçu persistant. Le résumé normalisé de cette matrice, la vérification de manifestes, le préflight et `compileall` sont également des reçus de phase P8.

Cette vérification candidate valide le contenu tel qu’il était avant la fermeture de la checklist P8. La release finale sera reconstruite après que la phase est close, puis soumise à une nouvelle extraction propre avec CRC, manifestes, préflight, compilation et tests ciblés. Les poids SmolLM2 de l’utilisateur et son PC physique ne sont toujours pas présents dans cet environnement; aucune preuve ne les prétend testés ici.


### Incident P8 — reçu matriciel volatil dans le snapshot

Une tentative sur une extraction neuve a exécuté le premier lot (8 fichiers, 28 réussites, 0 échec), puis le garde a bloqué la suite parce que `receipts/O94_6/P8_extract_matrix_01_of_12.json` venait d’être réécrit et restait authentifié par l’overlay `sav_AAM_O94_6`. Ce résultat est conservé comme `BLOCKED_PRECONDITION`, pas comme échec du modèle : `receipts/O94_6/P8_matrix_snapshot_mutability_failure.json` et `P8_matrix_snapshot_mutability_partial_matrix.json` conservent la cause, et le journal est `logs/O94_6/P8_matrix_snapshot_mutability_failure.log`.

La correction est générique : `refresh_o946_savepoint.py` exclut maintenant uniquement les reçus P8 de lots matriciels susceptibles d’être réécrits par le runner (`P8_extract_matrix_*` et `P8_full_matrix_*`). Les reçus stables des phases restent dans le snapshot; les reçus matriciels restent dans le paquet et sont reliés aux hashes du résumé de matrice. Un test de régression temp-root confirme la distinction, sans modifier un reçu réel pendant l’essai. Résultat ciblé : **3 tests réussis, 0 échec** dans `receipts/O94_6/P8_matrix_snapshot_policy_retest.json`.

La matrice exhaustive est relancée après cette correction et P8 reste ouvert jusqu’à un résultat complet sur une nouvelle extraction, puis un build/retest final séparé.


## 21. Clôture des phases et politique de release

La phase P8 est clôturée (`COMPLETE_EVIDENCED`) dans `checklist_de_travail_O94_6.json` sur la base du reçu `receipts/O94_6/P8_phase_closure.json`. Le candidat extrait proprement a exécuté les 92 fichiers de tests exactement une fois, en lots isolés; le total des compteurs pytest est de 449 réussites, zéro échec et zéro timeout. La vérification des manifestes a contrôlé 2 manifestes sur le même ensemble de 2781 fichiers et n’a rapporté aucun fichier absent ou hash erroné. Le préflight descendant et `compileall` ont aussi passé.

La fermeture n’efface pas les échecs historiques de la campagne monolithique : ils restent conservés avec leurs traces et sont décrits aux sections précédentes. Le runner segmenté est retenu comme méthode de validation complète car chacun de ses lots quitte proprement et produit un reçu. La construction finale et son extraction sont liées aux hash exacts dans le manifeste externe `O94_6_delivery_manifest.json`, à côté des ZIP.

Les capacités n’ont pas toutes le même niveau de preuve. La voie RAG-direct prouve récupération/extraction, l’adaptateur de protocole prouve l’intégration du contrat mais n’est pas un LLM, la capsule de facturation rejoue six exemples observés tandis que deux cas holdout restent `UNRESOLVED`. La génération avec un poids SmolLM2 utilisateur et l’observation directe du PC physique restent à exécuter sur cet environnement utilisateur, car ces artefacts/accès n’étaient pas présents durant l’audit.
