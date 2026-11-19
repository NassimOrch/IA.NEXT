# Revue croisée des formalismes non neuronaux — eSonde v8

Date : 17 novembre 2026 (Africa/Algiers)  
Phase : `P0_SOURCE_RECONCILIATION` — `IN_PROGRESS`  
Nature : lecture ciblée de familles documentaires et comparaison d'admissibilité; ce rapport ne prétend pas remplacer l'examen de chacun des 1 925 fichiers de `formalismes/`.

## 1. Description et périmètre

Cette revue relie les modèles de `theorie_emp/formalismes/` aux objectifs précis de v8 : chat prompt/réponse, cohérence conversationnelle et généralisation, conservation de l'identité Obsiss, poids historiques immuables et exclusion totale des neurones, MLP, Transformers, embeddings appris et mécanismes entraînés apparentés.

Les résultats rapportés par les documents sources restent attribués à leurs propres bancs d'essai. Un PASS de composant, une exactitude sur un domaine fini ou une compilation LaTeX ne sont pas convertis en preuve de dialogue général.

## 2. eGenBrain v4 — provenance, types, inférences et lecteur Parquet

**Sources examinées :**
- `formalismes/eGenBrain/Dmodel_eGenBrain_v4/README.md` ;
- `formalismes/eGenBrain/Amodel_eGenBrain_v4/README_AUDIT.md` ;
- `formalismes/eGenBrain/Amodel_eGenBrain_v4/documents/formalime_eGenBrain_v4.tex` ;
- code `Amodel_eGenBrain_v4/egenbrain/`, en particulier `core.py`, `mesh_v4.py`, `observations.py`, `parquet_flat.py`, `v4.py` et `trace_store.py`.

**Architecture source.** Maillage relationnel typé comprenant faits/occurrences, types, règles multi-prémisses, opérateurs typés, provenance et certificats. Le code distingue les données observées, dérivées et supposées; la transitivité et la symétrie ne sont pas ajoutées implicitement. Les nombres décimaux/rationnels et les unités sont traités explicitement dans les règles qui les supportent. Le lecteur Parquet dispose d'un `CompactReader`, du décodage Snappy, des niveaux hybrides et des valeurs `BYTE_ARRAY`; son helper `read_question_answer` est conçu pour un schéma avec colonnes `question`/`answer`, d'où son refus initial — correct — du schéma OASST1.

**Résultats source et portée.** L'audit v4 rapporte 136/136 tests locaux, 66 inférences brutes sur 11 cas et six modes, 8/8 routes positives et 3/3 cas d'abstention dans un micro-monde fini. L'intégration documentée utilise une tâche déterminée et des certificats. Ces résultats n'établissent ni l'induction ouverte, ni la généralisation de domaine, ni la cohérence d'une réponse conversationnelle libre. Le document distingue ses niveaux de généralisation; les combinaisons inédites d'opérateurs connus ne sont pas confondues avec l'induction de nouveaux opérateurs.

**Conséquence v8.** Reprendre comme principes d'ingénierie : typage des relations, provenance des occurrences, séparation observé/dérivé/supposé, preuve vérifiable d'une inférence bornée, et primitives de lecture Parquet. Ne pas reprendre comme moteur de dialogue : base persistante de faits, récupération documentaire ou réponse préfabriquée. L'adaptateur OASST1 peut réutiliser le décodeur bas niveau, mais garde un mapping de schéma et des tests propres. L'absence de preuve de sémantique ne doit pas être remplacée par un certificat de provenance.

## 3. NGeGenBrain v2 — laboratoire mécaniste à composants incompatibles et sous-ensembles admissibles

**Sources examinées :** `formalismes/NGeGenBrain/Dmodel_NGeGenBrain_v2/README.md`, code `discovery/`, `composition.py`, `adapters/`, rapports et résultats `SYNTH-PARITY-4`.

**Architecture source.** Le cœur importe la bibliothèque standard, mais PyTorch est optionnel pour l'instrumentation neuronale. Le dépôt contient explicitement adapters PyTorch/Hugging Face, hooks d'activations, réseaux synthétiques, MLP et mini-Transformers. Il contient aussi des outils distincts d'induction GF(2) pour XOR/parité, de recherche arithmétique dans une grammaire finie déclarée, de construction de contre-exemples, de validation des hypothèses et de journal append-only hashé.

**Résultats source et portée.** Le cas `SYNTH-PARITY-4` utilise 12 observations d'entraînement, quatre holdout et un domaine exhaustif de seize entrées; le résultat exact rapporté concerne cette fonction et cette classe de règles. La reconstruction du mini-Transformer synthétique interroge des contextes d'un modèle artificiel miniature et ne reconstitue pas un LLM réel. Le README précise aussi qu'aucun checkpoint LLM externe n'a été chargé pendant l'audit, faute de dépendances et de poids disponibles.

**Conséquence v8.** Exclure complètement des chemins d'exécution et dépendances v8 : `torch_adapter`, `huggingface adapter`, hooks, mini-Transformer, MLP, instrumentation et reconstruction à partir d'activations neuronales. Les outils purement non neuronaux d'induction dans une classe déclarée peuvent être évalués comme tests bornés de règles sur des sous-problèmes; ils ne constituent pas le générateur de langage. Les limites de la grammaire d'hypothèses doivent rester explicites.

## 4. eLLM v1 — exclusion complète

**Source examinée :** `formalismes/eLLM/Dmodel_eLLM_v1/README.md` et documents d'audit associés.

Le système enveloppe un checkpoint causal Transformer pré-entraîné (SmolLM2 par défaut), observe ses états cachés contextualisés et apprend un adaptateur de sondes multi-résolution dont les corrections affectent les logits et reçoivent une perte prédictive. C'est directement incompatible avec la contrainte rouge eSonde v8. Ce composant et ses poids ne sont pas repris. Les travaux théoriques autour des partitions/empreintes peuvent être comparés au niveau abstrait, sans importer le runtime ni ses états cachés.

## 5. FulleGenBrain 4 — contrats de composition et allocation, non intégration générale

**Sources examinées :** `formalismes/FulleGenBrain/FulleGenBrain_4_dossier_complet_avc_interface/README_FulleGenBrain_4.md`, `deliverables/formalisme_FulleGenBrain_4.tex`, `deliverables/prouve_et_tracabilite_FulleGenBrain_4.json` et les prototypes de référence cités par le README.

**Apports.** Contrats typés, composition explicite, séparation entre composant candidat, testé et certifié, provenance, contre-exemples, versionnage réversible, budgets de ressources et politique d'allocation. La spécification met en garde contre l'assimilation de mise en veille et d'allocation à une réduction de l'espace combinatoire, et conditionne les garanties d'anti-famine à des hypothèses exposées.

**Statut source.** Le registre de preuve donne `FORMALIZED_ARCHITECTURE_WITH_LOCAL_ASCRC_REFERENCE_PROTOTYPE; END_TO_END_INTEGRATION_NOT_EVALUATED`. L'interface est `SPECIFICATION_ONLY_NOT_APPLICATION_IMPLEMENTATION`; les tests référencés concernent les prototypes locaux. Les 29 opérateurs compositionnels sont spécifiés, mais le README ne revendique pas un runtime unifié de bout en bout ni une preuve formelle machine-checkée de tous les théorèmes.

**Conséquence v8.** Retenir le principe de contrats explicites et de statuts épistémiques traçables pour les modules Obsiss, profil, candidats, sélection et sortie. Ne pas intégrer le système complet ASCRC, la mémoire vivante, les 29 opérateurs ou une interface multi-espace tant qu'une utilité marginale mesurée n'est pas démontrée. Ces additions ne sont pas nécessaires au chat et augmenteraient la surface d'intégration.

## 6. AAM O94.6 — séparation tâche/sous-questions/statuts et vérification indépendante

**Sources examinées :** `formalismes/AAM/AAM_O94_6/Amodel_AAM_O94_6 - Copie/README_AUDIT_O94_6.md`, `README_O94_6_FR.md`, rapport de tests et formalismes O94.6.

**Apports.** Enveloppe de tâche, conservation des sous-questions, distinction entre récupération documentaire directe, adaptateur de contrat et vrai modèle de langage, traces de génération longue, statuts d'interruption, vérificateur séparé et séparation stricte entre oracles d'audit et runtime.

**Résultats source et portée.** L'audit décrit une matrice de 92 fichiers exécutés en lots et 449 réussites cumulées, confirmées par le reçu brut P8_candidate_extraction_full_matrix_raw.json et P8_final_release_validation.json (92 fichiers, 12 lots, zéro échec, zéro timeout); les mentions 448 de deux passages de clôture intermédiaires sont des textes obsolètes. Le replay de facturation donne six cas observés rejoués exactement et deux holdout `UNRESOLVED`; cela ne prouve pas la généralisation hors capsule. Les poids SmolLM2 utilisateur n'étaient pas présents dans l'environnement d'audit, et le README précise que certains adaptateurs d'exemple ne sont pas des LLM.

**Conséquence v8.** Reprendre les enveloppes de tâche, la conservation de toutes les contraintes du prompt, les statuts d'exécution et le vérificateur d'évaluation indépendant. Ne pas reprendre RAG-direct, mémoire documentaire ou adaptateur déterministe comme substitut à la génération chat. L'abstention reste une fonction de configuration du produit mais doit être désactivée pour les campagnes d'évaluation demandées.

## 7. ORDER80.2.2 — séparation de l'insight et de la résolution

**Sources examinées :** `formalismes/models_order/model_order_80_2_2_CORRIGE_HIERARCHICAL_STRICT/docs/README_ORDER8022.md`, `GENERAL_SOLVER_CONTRACT.md`, `BENCHMARK_SEMANTICS.md`, `ALGORITHM_ORDER8022.md`.

Le cycle source observe, tente une résolution, observe à nouveau, puis décompose quand l'observation est épuisée; chaque sous-problème répète le cycle. Une nouveauté documentaire vérifiée déclenche un retest de la racine et des sondes voisines. Surtout, `DOCUMENTED_INSIGHT` n'est pas `SOLVED`: seule une vérification de domaine explicite peut promouvoir une réponse au statut de résolution. Le synthétiseur général est extractif et déterministe, non un moteur sémantique universel.

**Conséquence v8.** Réutiliser cette séparation comme nomenclature d'audit de réponse (information observée, hypothèse, inférence, vérifiée / non vérifiée). Ne pas utiliser le RAG extractif ni la mémoire `news/` comme moteur de réponse. Le cycle hiérarchique complet est conçu pour recherche documentaire et décomposition; il n'est pas importé tel quel dans le chat sans preuve qu'il améliore les réponses.

## 8. Théorie des empreintes et document d'observation : apports et défauts constatés

**Source examinée :** `formalismes/models_order/model_math_order_O76_CORRIGE_O76_1_1/sources/model_s/th_emp_observation_formalisme_0.tex` (495 lignes, hash source `02475788cb4371663635b0550fd0b59c61d6d8d16b18ccb98283795c86213b6b`).

Le texte distingue existence ontologique et existence relative à un système, disponibilité observationnelle globale et observabilité locale, l'interaction et l'opérateur d'observation. Il définit l'empreinte `I_F^P(x)` et l'indiscernabilité relative à une empreinte; la factorisation par le quotient est conditionnelle à la constance sur chaque fibre. Ce formalisme donne un fondement direct aux tests de collision, aux paraphrases observationnellement indiscernables, aux contrastes minimaux et à la couverture contextuelle.

Il traite également la récursion, l'auto-observation et deux notions de mémoire. Le texte reconnaît lui-même que la mémoire ontologique reste un objet ouvert et que certaines affirmations sont des axiomes ou thèses conceptuelles, pas des propositions démontrées à partir du noyau des empreintes. Pour eSonde, ces sections ne justifient pas de substituer une mémoire de faits à une capacité de génération.

**Défauts source reproduits en diagnostic sans modifier l'original :** (i) `\DeclareMathOperator{\Im}{Im}` entre en conflit avec `\Im` déjà défini; (ii) dans le passage sur la mémoire évolutive, un second `\[` est ouvert au sein d'un affichage mathématique déjà ouvert, conduisant ensuite à `Double subscript` sur `\Mevo_{t+1}`. Le document source est conservé byte-identique; les défauts sont inscrits dans l'audit, pas corrigés silencieusement dans le corpus.

## 9. Tableau de décision pour eSonde v8

| Famille | Éléments réutilisables à évaluer | Éléments exclus du runtime v8 | État de la preuve |
|---|---|---|---|
| eGenBrain v4 | provenance, types, certificat borné, primitives Parquet | moteur RAG/faits comme générateur | micro-monde fini; aucune preuve de chat libre |
| NGeGenBrain v2 | induction GF(2)/arithmétique non neuronale sous grammaire déclarée; contre-exemples | PyTorch, hooks, MLP, mini-Transformer, HF | cas synthétiques bornés seulement |
| eLLM v1 | comparaison abstraite théorie d'empreintes | Transformer, états cachés, adaptateur appris, loss/logits | incompatible par construction |
| FulleGenBrain 4 | contrats, provenance, statuts, contre-exemples | intégration ASCRC complète, mémoire vivante, 29 opérateurs dans le runtime | prototypes locaux; E2E non évalué |
| AAM O94.6 | enveloppe tâche, suivi sous-questions, vérification/statuts | RAG-direct ou adaptateur déterministe comme générateur | tests bornés; replay holdout non résolu |
| ORDER80.2.2 | `DOCUMENTED_INSIGHT` ≠ `SOLVED`, retest et vérification de domaine | synthétiseur extractif comme chat IA, mémoire RAG | recherche documentaire déterministe |
| théorie observation | empreintes, fibres, équivalence, factorisation conditionnelle | mémoire ontologique comme moteur d'intelligence | noyau formel + axiomes/conjectures distincts |

## 10. Implications opérationnelles et critères expérimentaux

Les sources ci-dessus suggèrent des tests, non des conclusions d'efficacité :

1. Vérifier la provenance et le typage des occurrences sans présumer une entailment ou une causalité à partir de la seule succession.
2. Mesurer la contribution marginale des seize observations par ablation, tout en conservant les identités individuelles des Obsiss.
3. Mesurer les fibres d'indiscernabilité sur paraphrases, substitutions de référents, négation, temporalité, changement d'intention et contrastes minimaux.
4. Évaluer les statuts de preuve de réponse sans leur donner de rôle de générateur ni injecter les sorties attendues dans le modèle.
5. Évaluer les composants non neuronaux bornés séparément, sans faire passer le succès sur une grammaire finie pour un transfert général.
6. Conserver l'option de non-réponse configurable, `OFF` par défaut et `OFF` pour les essais de génération.

Aucune de ces tâches n'est considérée exécutée par ce rapport. Elles doivent entrer dans le laboratoire avec hypothèses, baselines, splits, mesures et critères de réfutation préenregistrés.

## 11. Commandes et reproductibilité de la présente revue

Cette revue documentaire a été produite avec les fichiers déjà extraits sous `eSonde_v8_workspace/source/`; aucune expérience d'inférence eSonde n'a été lancée pendant cette lecture. Vérification des sources sélectionnées :

```bash
sha256sum <source-file>
sed -n '1,240p' <text-file>
pdflatex -halt-on-error -interaction=nonstopmode <diagnostic-copy.tex>
```

La lecture approfondie porte sur les fichiers nommés dans les sections 2 à 8 et les extraits précisément identifiés; elle ne prétend pas avoir épuisé toutes les variantes historiques de chaque famille.

## 12. Conclusions et statut

Cette revue fournit une carte de réutilisation prudente des formalismes. eGenBrain donne des outils solides de type/provenance et un lecteur Parquet, pas un générateur de chat. NGeGenBrain contient des voies non neuronales limitées mais aussi de nombreuses voies neuronales à exclure. eLLM est incompatible. FulleGenBrain et AAM proposent des contrats et des structures d'audit utiles mais leurs résultats restent bornés et plusieurs intégrations sont explicitement non évaluées. ORDER80.2.2 contribue surtout à la discipline de vérification. La théorie des empreintes aide à formaliser l'observation et les collisions, sans justifier la mémoire comme substitut d'intelligence.

**Statut P0 : `IN_PROGRESS`.** La revue ciblée de ces familles est terminée pour les fichiers listés, mais 1 925 fichiers sont recensés dans `formalismes/`; l'inventaire structurel ne vaut pas lecture fichier par fichier. Les autres variantes, codes, campagnes et liens source→expérience doivent encore être lus avant clôture P0. Aucune prédiction de réussite ou d'échec du modèle n'est formulée.
