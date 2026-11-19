# Synthèse critique des sources théoriques et modèles — eSonde v8

## 1. Portée et règle de provenance

Cette synthèse s'appuie sur les documents source présents sous `theorie_emp/`, notamment `PCH/`, `formalismes/`, les rapports d'expérience, README et audits. L'inventaire SHA-256 individuel couvre 2 018 fichiers de `theorie_emp`; le sous-arbre `formalismes/` en contient 1 925. Les documents clés ont été extraits dans `FORMALISMES_KEY_DOCS_EXTRACT_20261117.md`. Les PDFs et images restent inventoriés par taille/hash/métadonnées, sans lecture de leur contenu, conformément à la priorité demandée. Cette synthèse n'affirme pas que les 1 925 fichiers ont tous fait l'objet d'une lecture humaine ligne par ligne : la revue de chaque expérience et de chaque sous-archive reste un critère ouvert de P0.

## 2. Théorie des empreintes (DDD, ordre 5)

### Objets source
La théorie organise l'observation par sondes, signatures/empreintes, relations d'indiscernabilité, fibres, quotients, factorisation, seuils, trajectoires, contraintes, apprentissage et généralisation. La généralisation est formulée relativement à une famille d'observations : deux objets indiscernables pour une famille de sondes sont réunis dans une même fibre/équivalence. Le quotient est donc relatif à ce qui est effectivement observé.

### Usage retenu pour Obsiss
Les 16 observations d'eSonde doivent être traitées comme 16 canaux/dimensions d'observation explicites, mais chaque Obsiss reste un observateur individuel portant sa propre identité/perspective. Une signature Obsiss doit conserver (i) la valeur de chaque observation, (ii) la provenance du signal, (iii) la stabilité sous perturbations contrôlées et (iv) la distinction entre absence d'observation et valeur nulle.

### Réserve logique
L'équivalence observationnelle ne prouve pas l'équivalence sémantique, la vérité ou l'identité des comportements hors des sondes. Une généralisation sur le quotient exige une condition de factorisation de la sortie à travers l'empreinte, ou une mesure empirique de la violation. La stabilité du rang/vote ne doit jamais être assimilée à la vérité.

## 3. PCH : noyau mathématique exploitable et branches exclues

### Noyau du routage variationnel (source v11)
Pour un ensemble fini de contextes `C={1,...,K}`, chaque contexte possède un ensemble admissible non vide, fermé et convexe `M_c` dans un espace euclidien fini-dimensionnel. La fonctionnelle source est :

`J_c(u;w) = 1/2 ||u-w||^2 + lambda_ctx,c dist(u,M_c)^2 + lambda_ridge,c ||u||^2`.

Avec `lambda_ctx,c > 0` et `lambda_ridge,c >= 0`, elle est fortement convexe en `u`, de module `mu_c=1+2 lambda_ridge,c`; le minimiseur est unique. La normalisation positive par `mu_c` conserve le minimiseur et donne une fonction valeur réduite `Vtilde_c(w)`, égale à une enveloppe de Moreau. Pour un nombre fini de contextes, le routage dur sélectionne `argmin_c Vtilde_c(w)`. Le soft-routing entropique donne `p_c ∝ exp(-beta Vtilde_c(w))` et converge vers le contexte unique lorsque `beta` tend vers l'infini. La stabilité du contexte sélectionné est conditionnée à une marge stricte positive entre la meilleure branche et les autres.

### Adaptation possible, non encore validée
Une adaptation purement mathématique à l'espace des 16 observations est candidate : `w ∈ R^16`, sans embedding, sans PCA, sans réseau de routage. Les ensembles `M_c` et les coûts doivent être définis sans mémoriser des paires prompt/réponse ni coder la réponse attendue. Leur construction, leur calibration, les critères d'admissibilité, la stabilité et la généralisation doivent être spécifiés et testés avant intégration. La seule existence du minimiseur proximal ne démontre ni pertinence du contexte ni qualité de réponse.

### Branches strictement exclues du runtime normatif
- Les expériences Cas 3 normalisé décrites dans `report_cas3_normalized_complete.tex` utilisent un encodeur SentenceTransformer gelé, une PCA ajustée sur calibration, et des QP CVXPY/OSQP. Ces résultats sont conservés comme observations historiques mais ne sont pas transférés dans eSonde v8.
- Les variantes d'apprentissage de routage décrites dans `pch_esm_4_v5_partie_valid_exp_v2_routage_3_arch.tex` entraînent un réseau de routage ou utilisent distillation/pré-routage appris. Elles sont incompatibles avec l'interdiction neuronale et ne sont pas reprises.
- PCH-ESM ajoute décomposition spectrale, projecteurs, têtes linéaires/affines et apprentissage par alternance. Ces éléments ne sont pas nécessaires au noyau proximal et ne sont pas retenus dans l'architecture minimale v8.

### Résultats expérimentaux PCH à ne pas surinterpréter
Le rapport Cas 3 indique 13 blocs/54 runs : 7 blocs satisfont le critère normalisé scripté, 6 échouent. Les verdicts portent sur `rho_gap` et `operator_gap`, pas sur la qualité de classification. Dans les expériences 20news20 en dimension 16, l'oracle peut atteindre environ 0.96 alors que le routage observé reste proche de la baseline (~0.56) et que la précision de contexte est ~0.50. Dans les expériences 20news4, des cas de routage améliorent les résultats mais sans loi monotone universelle. Les expériences ex20/ex21 montrent une stabilité géométrique presque sans gain utile; ex22/ex26/ex27 illustrent un écart oracle/routé et un routage qui peut même dégrader le score. La conséquence exploitable est une question de recherche sur l'accès au contexte et la marge de routage, pas une preuve de performance de chat.

## 4. eGenBrain v4 et v1

### Ce que les sources établissent
Le runtime eGenBrain v4 préserve une base MG historique et ajoute un maillage inférentiel typé/certifié, avec SQLite, règles et opérations explicites. Le README précise que le démarrage vierge ne possède pas de capacité d'apprentissage ou de généralisation non mesurée. L'audit rapporte 136/136 tests, 66 inférences brutes sur 11 cas × 6 modes, et 8/8 dérivations positives + 3/3 abstentions dans les micro-mondes finis. Le facteur `dozen=12` est une primitive fournie. Ces résultats ne prouvent pas l'induction autonome d'opérateurs ni l'intelligence générale.

Le décodeur Parquet intégré est orienté schéma `question`/`answer`; l'adaptateur OASST1 a réutilisé ses primitives de lecture (CompactReader, Snappy, niveaux hybrides, BYTE_ARRAY) et ajouté BOOLEAN scalaire. Le décodeur d'origine a donc été utilisé comme base technique, sans lui attribuer une compatibilité qu'il n'avait pas.

### Usage retenu
Provenance stricte, décodage, validation des structures, contrôles d'intégrité et séparation entre sortie d'exécution et scoring post-hoc. L'approche de certificats vérifiables peut inspirer les vérificateurs de propriétés déterministes du runtime.

### Non-reprise
La base MG, le retrieval et le maillage de faits ne deviennent pas le moteur de génération d'eSonde v8 : ce serait substituer une mémoire/recherche documentaire au cœur d'intelligence dialogique visé. Les micro-cas arithmétiques ne remplacent pas OASST1.

## 5. NGeGenBrain v2

Le système est un laboratoire d'étude mécaniste et de reconstruction fonctionnelle, avec adapters instrumentables, interventions, découverte dans des classes d'hypothèses et reconstruction symbolique. L'audit rapporte 52 tests V2 et 65 tests V1, ainsi que des reconstructions synthétiques sur parité et un minuscule Transformer causal. Le README et l'audit déclarent explicitement qu'aucun LLM Hugging Face réel n'a été chargé; les résultats sont bornés aux modèles synthétiques et domaines finis fournis. Le code inclut des adapters PyTorch et des expériences neuronales : ils sont exclus du runtime eSonde v8. Les concepts de protocole aveugle, d'hypothèses falsifiables, d'interventions appariées, de journaux chaînés et de contre-exemples sont des idées de méthode d'audit, non des composants du modèle.

## 6. eLLM v0

Le README/audit décrivent un prédicteur probabiliste à n-grammes variables entraîné sur 80 paragraphes français (split 64/8/8). Sur le test réservé de 8 documents/328 tokens, perplexité 217.039 contre 449.916 pour le baseline unigramme et exactitude top-1 21.04%. La documentation signale elle-même que des générations peuvent être incohérentes, courtes ou incorrectes. Il constitue un comparateur statistique utile pour mesurer les transitions locales, mais ne doit pas être pris comme solution suffisante au chat ni comme simple table de mémoire.

## 7. AAM O82 / ROCA-D

Le README décrit une architecture non-LLM avec observation contractuelle, empreintes partielles, retrieval mémoire obligatoire, suffisance décisionnelle, politique lexicographique, correction/CEGIS, capsules de compétences, auto-observation, décomposition et replay. Le runtime est fortement gouverné par le contrat et la mémoire. Les idées de ledger, replay, séparation raw/dérivé, recovery et critères de suffisance peuvent améliorer l'auditabilité. Le retrieval obligatoire, les capsules/mémoires et la boucle de compétences ne sont pas repris comme cœur du chat v8, car le but est de ne pas remplacer l'intelligence par la mémoire et d'éviter la complexité gratuite.

## 8. O76 et modèles d'ordre

O76 est un moteur de preuve mathématique exacte avec certificats rejouables et vérificateur indépendant; son statut `UNRESOLVED` ne signifie pas impossibilité. Les idées pertinentes sont la séparation preuve/hypothèse, le certificat rejouable, le contre-certificat et le contrôle indépendant. Elles peuvent servir à vérifier les propriétés formelles de PCH et de l'empreinte. Le solveur mathématique lui-même n'est pas un moteur de dialogue.

Les modèles ORDER utilisent des boucles de résolution, décomposition, retest racine, peer-probes, journalisation et mémoire de connaissances documentaires. Leur discipline de statut et de retest est utile pour la méthode; le cycle mémoire/recherche et l'orchestration générale ne sont pas incorporés automatiquement au moteur de chat.

## 9. EX8 et comparateurs MLP

Les dossiers EX8 B10/B11 contiennent des comparateurs MLP explicitement interdits pour l'architecture cible. Le rapport B10 sur Wisconsin donne une moyenne log-loss 0.04139 contre 0.05473 pour le MLP apparié et 0.05080 pour le MLP plus large, sur cinq graines; toutefois l'IC t apparié à 95% recouvre zéro et le test exact bilatéral donne p=0.0625. Le rapport note aussi une latence B10 environ 2.85× celle du gate B11 et l'absence de victoire B10 sur SMS. Ces résultats ne sont pas une preuve générale et ne justifient aucune reprise des comparateurs ou de leurs composants.

## 10. Conséquence pour l'architecture eSonde v8

1. Garder les 16 observations existantes comme espace d'observation explicite; ne pas créer de nouvelle dimension sans preuve d'apport marginal.
2. Conserver les Obsiss comme population d'observateurs distincts; mesurer leur contribution marginale, leur redondance et la stabilité inter-prompt.
3. Étudier un PCH proximal 16D pur, à contextes finis et critères entièrement définis, uniquement après construction d'une définition non mémorielle des ensembles contextuels.
4. Utiliser les transitions OASST1 et associations agrégées comme signaux d'apprentissage observables, pas comme réponse pré-enregistrée ni table prompt→réponse.
5. Réserver la validation/test aux mesures et ne pas introduire de référence de réponse dans le runtime.
6. Exclure explicitement tout réseau, neurone, MLP, embedding appris, SentenceTransformer, PCA sur embeddings, transformer, gate neuronal et rétropropagation.
7. Les certificats, invariants et stabilité algorithmique ne seront pas assimilés à la qualité sémantique; celle-ci sera mesurée séparément par génération libre et jugement de cohérence/contextualité.

## 11. Statut P0

La synthèse et les extraits approfondis couvrent les familles principales et les documents pivots identifiés. P0 reste ouvert tant que le registre de revue de chaque sous-archive/expérience n'a pas été complété, que les variantes historiques et leurs sorties n'ont pas toutes été rapprochées de leurs scripts et données, et que les défauts CLI/GUI/preflight v8 consignés ne sont pas traités dans leur phase autorisée. Aucune conclusion anticipée sur la réussite ou l'échec d'eSonde v8 n'est formulée.

## 12. Formalismes empiriques d'observation et O78

`th_emp_observation_formalisme_0(1).tex` définit l'observation fonctionnelle par interaction, distinction accessible et rétroaction. Il distingue explicitement observation, découverte et conscience; une boucle de rétroaction n'est pas automatiquement une observation. Le document introduit toutefois comme axiome de modèle l'émergence de l'observation lors d'une première boucle locale/globale. Il pose aussi une « mémoire ontologique » comme principe de fondation, tout en précisant que son domaine et ses propriétés ne sont pas entièrement construits mathématiquement. Cette branche n'est donc pas un fondement obligatoire du runtime eSonde v8 : les définitions opérationnelles d'observation peuvent inspirer les tests, mais les axiomes de mémoire ontologique et de conscience ne sont pas introduits dans le moteur.

`formalisme_empirical.tex` et `formalisme_empirical_O78_1_2.tex` traitent de l'empreinte de programmes AST : motifs invariants, fréquences, stabilité, graphe de relations, fermeture compositionnelle et synthèse d'AST dans une classe finie. Le document précise que la complétude est conditionnelle à la présence de la cible dans la fermeture finie et à un vérificateur décidable; la nouveauté structurelle n'implique pas nouveauté sémantique. L'empreinte O78 est explicitement une mémoire évolutive de motifs. Cette architecture n'est pas reprise comme cœur de chat, mais la discipline de classe d'hypothèses, de preuve conditionnelle et de vérification indépendante est pertinente.

## 13. Dossiers d'expériences EX4 à EX12 et sondes adaptatives

Les README des expériences indiquent plusieurs familles de sondes adaptatives RBF/MIXA, des coordinateurs, des gates, de l'optimisation Adam/hypergradient et des comparateurs MLP. Ces expériences sont importantes pour l'historique des idées mais leurs architectures ne sont pas importées dans eSonde v8, car elles violent directement ou indirectement l'interdiction neuronale ou reposent sur des fonctions RBF apprenables apparentées à des unités neuronales.

- EX4 : sur Wisconsin, aucune des 12 familles v006 ne satisfait toutes les conditions préenregistrées; sur Iris, égalité ponctuelle d'accuracy mais log-loss/latence défavorables dans certains cas. Le transfert reste exploratoire.
- EX5 : 437 comparaisons physiques ge4x auditées, mais aucune candidate ne démontre simultanément la non-infériorité prédictive et toutes les dimensions de ressources. OOF et hiérarchies Q/A sont plus lentes en entraînement et batch 1 que les MLP de référence.
- EX6 : verdict INCOMPLET; paramètres conformes au ratio, mais pas d'avantage de vitesse et métriques souvent inférieures.
- EX7 V003 : réduction structurelle de paramètres (1 341 vs 6 712) mais accuracy/log-loss et latence restent derrière les MLP appariés dans le résumé fourni.
- EX8 B10 : log-loss Wisconsin meilleur que le MLP apparié sur cinq graines, mais IC apparié recouvre zéro et test exact bilatéral p=0.0625; latence 2.853× B11. Le résultat est exploratoire et ne se reproduit pas sur SMS selon les README.
- EX9 : les sondes perdent contre les MLP sur XOR8 et les deux domaines synthétiques supplémentaires; les branches MLP sont exclues du runtime v8.
- EX11 : protocole très strict de partitions et de pré-enregistrement, mais au snapshot README 31/65 blocs REPLICA-U terminés; autres campagnes confirmatoires pas encore démarrées.
- EX12 : protocole séquentiel P0–P7; le paquet P1 indique que les scripts producteurs originaux de certains runs ne sont pas retrouvés, sans inférer sabotage ou suppression intentionnelle.
- NG-ADAPT global : 198 entraînements sur six tâches, 49/49 contrôles d'audit; le README signale explicitement une dérive possible sous labels trompeurs et des phases partielles. Ces résultats ne sont pas des preuves d'une supériorité générale.

Ces dossiers sont conservés comme sources de méthodes (pré-enregistrement, seeds, partitions gelées, audit indépendant, ablations, journaux append-only), pas comme autorisation de réutiliser leurs réseaux, neurones, MLP, RBF apprenables, gates ou optimiseurs de gradient.

## 14. Point mathématique à vérifier dans la transposition PCH

Le noyau PCH v11 autorise `lambda_ridge >= 0`; dans ce cas, la borne de Lipschitz `1/(1+2 lambda_ridge)` vaut 1 lorsque `lambda_ridge=0`, donc le mapping est non expansif, mais pas nécessairement une contraction stricte. Les théorèmes de pré-routage qui supposent un facteur `rho<1` doivent imposer `lambda_ridge>0` ou démontrer une autre source de forte convexité. La formalisation v8 fixe bien `lambda_r>0` pour sa version simplifiée; ce choix doit être conservé dans les cinq passes et dans le code. Il ne faut pas importer les énoncés PCH généraux en oubliant cette condition.

## 15. PCH-LLM complet et frontière d'exclusion

Le document `PCH/llm_pch/llm_pch.tex` est une proposition d'architecture complète, mais elle n'est pas compatible avec les règles rouges v8 : elle spécifie un embedding de tokens appris `E_theta`, un MLP résiduel dans chaque bloc PCH et un débruiteur latent `mu_theta` dans la diffusion inverse. L'absence d'attention standard ne la rend donc pas non neuronale. Ce document est analysé comme branche historique et n'est pas importé, même indirectement, dans le runtime v8. Le seul noyau PCH retenu comme candidat est le problème proximal convexe explicite et le routage par valeurs réduites, sans encodeur, embedding, PCA, réseau résiduel, gate appris ni diffusion neuronale.

## 16. Correction de périmètre AAM et eLLM v1

La branche AAM la plus récente présente dans les sources est **AAM O94.6** (et non uniquement O82). Son formalisme et son rapport O94.6 décrivent un système de tâches, décomposition multi-question, RAG, routage vers fournisseurs de génération, persistance mémoire/récompense, composition et observation de processus. La campagne revendique 92 fichiers de tests, 449 réussites cumulées, zéro échec et zéro timeout pour les scénarios bornés; les capsules de processus observé rejouent 6/6 entrées vues et laissent 0/2 holdouts `UNRESOLVED`. Les poids SmolLM2-360M n'étaient pas disponibles, et les tests d'adaptateur ne sont pas des générations LLM. Pour eSonde v8, les statuts d'exécution, séparation oracle/runtime, journal append-only et preuve indépendante sont des pratiques d'audit utiles; RAG, fournisseurs externes, mémoire persistante, composition d'outils et boucles de récompense ne sont pas intégrés au cœur du chat.

**eLLM v1** est distinct d'eLLM v0 : il enveloppe un checkpoint causal préentraîné Transformers (SmolLM2-135M-Instruct par défaut), apprend des sondes multi-résolution à partir des états cachés et injecte un résidu de fingerprint dans les logits avec perte prédictive. Il requiert donc un Transformer/poids préentraînés, des embeddings et des sondes apprises; il est strictement exclu du runtime v8. La théorie DDD et ses tests de quotient fini peuvent être étudiés indépendamment, mais les implémentations qui observent des états cachés et les adaptateurs appris ne sont pas repris.

## 17. FulleGenBrain 4

Le dossier FulleGenBrain 4 décrit quatre plans coordonnés : catalogue/compositions, runtime/contrôleur, évolution/découverte, mémoire/ressources. Il comprend programmation compositionnelle, ASCR/ASCRC, mémoire vivante, activation/veille/réveil, découverte de règles, clonage comportemental, modèle du monde conditionnel, provenance et contrôleurs de ressources. Le README précise que l'interface est une spécification cible, que les 29 opérateurs ne sont pas tous réunis dans un runtime unifié et que les garanties anti-famine sont conditionnelles. Cette famille est beaucoup trop large pour être importée comme moteur de chat v8 sans démonstration d'utilité marginale; sa mémoire persistante, son clonage et sa programmation compositionnelle ne répondent pas au périmètre chat seul. Seules la discipline de statut, la traçabilité des composants et la vérification de contrats peuvent être adaptées au protocole de recherche.

## 18. eGenBrain v4 : statut exact de la généralisation

Le formalisme v4 sépare faits observés/dérivés/assumés, types, provenance, hyperrègles, opérateurs et certificats. La campagne de 66 inférences sur 11 micro-mondes rapporte 8/8 cas positifs de composition dans le mode maillage complet et trois abstentions correctes; les primitives (dont dozen=12) et les règles sont explicitement fournies. Le rapport indique que le parseur naturel est une grammaire bornée, que l'induction de règles non déclarées reste ouverte, et que la généralisation de la capsule observée est 0/2 sur les holdouts. La valeur pour eSonde v8 est la provenance et la distinction entre observations et dérivations, pas un moteur de faits/règles qui remplacerait la génération de langage.

## 19. Décodeur Parquet eGenBrain et adaptation OASST1

Le code source `Amodel_eGenBrain_v4/egenbrain/parquet_flat.py` est un lecteur autonome d'un sous-ensemble Parquet : footer Thrift Compact Protocol, pages BYTE_ARRAY, PLAIN/dictionary, SNAPPY et niveaux hybrides; son contrat est explicitement question/answer et il refuse les autres schémas. Le script v8 `decode_oasst1_parquet.py` importe sans modification `CompactReader`, `_snappy`, `_hybrid`, `_plain_byte_arrays`, `ParquetFormatError` et `_decode_column` de ce lecteur; il ajoute un adaptateur pour les colonnes BOOLEAN scalaire `review_result`, `deleted`, `synthetic`, tout en conservant les champs textuels OASST1 nécessaires. Les types physiques et encodages non pris en charge sont refusés, pas devinés. Il s'agit donc d'une adaptation documentée du décodeur eGenBrain, pas d'une affirmation que son API question/answer lisait OASST1 sans modification.

## 20. Résultats croisés des campagnes de sondes adaptatives (EX7–EX12)

Les dossiers EX7–EX12 ne sont pas le modèle Obsiss v6/v7. Ils étudient surtout des sondes adaptatives RBF, coordinateurs, gates, HC-RBF, réseaux denses MLP ou architectures hybrides. Les MLP sont des comparateurs explicites; plusieurs candidates RBF sont des unités à centres apprenables, donc elles sont exclues du runtime v8 même lorsqu'elles n'emploient pas de MLP.

- **EX7 V003 OuterCoord-Lite-7x1** : cinq seeds sur le split Wisconsin historique; 1 341 paramètres contre 1 349 pour le MLP apparié et 5 375 pour le GE4X. Accuracy 97,88 %, log-loss 0,06806; le MLP apparié a log-loss 0,05136. La candidate échoue la marge log-loss sur les quatre références. Latence batch 1 ~0,290 ms contre ~0,025 ms MLP. Résultat de simplification structurelle, pas architecture gagnante ni holdout externe.
- **EX8 B10/B11** : cinq seeds Wisconsin, log-loss B10 0,04139 vs MLP apparié 0,05473, mais split historiquement exposé; test XOR8 non scoré car le loader du checkpoint échoue avant prédiction. Les ablations restent descriptives et le résultat ne généralise pas aux domaines EX9.
- **EX9** : 45 runs XOR8, 35 ablations, 90 runs additionnels sur concentric2 et rotated_moons2. Les candidates B10/B11/A0 sont très derrière les MLP en validation/test sur ces domaines; les tests holdout ont été ouverts une fois et audités 90/90. Les sondes sont environ 12–22× plus lentes dans le profil CPU rapporté. Aucun domaine réel externe vierge n'est validé.
- **EX10** : 90 runs de classification et 550 runs CNG/CNC, plus scoring one-shot de 1 695 enregistrements; les audits sont très complets, mais CNG/CNC évaluent des tâches mathématiques synthétiques, pas le chat. Les mesures ressources indiquent absence de FLOPs matériels et d'énergie, et une partie des mesures de temps d'entraînement est explicitement contendue/non vérifiée.
- **EX11** : les phases P0/P1/P2 sont vérifiées, mais P3 incomplet (REPLICA-U v004 11/65 au snapshot), P4 test scellé non ouvert, P5 partiel. D1/D2 ont 40/40 équivalences sorties/gradients et un gain microbenchmark 1,75–4×; D3 reste non confirmée. CNG/CNC et REPLICA utilisent PyTorch/MLP/AdaptiveRBF, donc pas de transfert architectural.
- **EX12 HC-RBF** : toutes les portes P0–P7 passent dans le rapport, mais le verdict scientifique reste mixte : 11/16 contrastes primaires non inférieurs en interpolation, 7/16 rejettent l'égalité; extrapolation seulement 4/16 favorables, et latence pipeline batch 1 1,82–2,25× le MLP. HC-RBF utilise `tanh(Wx+b)` et unités RBF; exclu de v8 au regard de l'interdiction neuronale/RBF.
- **NG-ADAPT global** : 198 entraînements sur six tâches, 49/49 contrôles indépendants; les effets de coordination varient selon la tâche et la mise à jour en ligne sous labels trompeurs peut dériver. Les sondes adaptatives RBF et optimiseurs de gradient ne sont pas repris.

La leçon utilisable pour le protocole v8 est méthodologique : pré-enregistrement, splits immuables, contrôles one-shot, recalcul indépendant des métriques, séparation des résultats exploratoires/confirmatoires, profils ressources isolés, et statut explicite `NOT_RUN`/`INCOMPLETE_QUOTA`. Les résultats des modèles neuronaux ou RBF ne constituent pas des résultats d'eSonde v8 et ne sont pas des preuves de sa réussite ou de son échec.

## 21. EX4–EX6 : familles MIXA, OOF et ressources

- **EX4** : plusieurs versions de sondes et comparateurs, registres v005/v006/v008/v009; les audits conservent même un `FAIL ATTENDU` de comptage v007 dû à l'extension du registre. Les artefacts validés et les résultats de test sont séparés. Ces sondes sont des branches de recherche distinctes de l'Obsiss original.
- **EX5** : RETRO/Adam, proportions fixe/adaptative, correcteur alterné A↔B, micro-MIXA hiérarchique Q/A, résidus OOF, partage encodeur/centres, PCA question-only, transferts Wine/Digits et profilage CPU. L'audit couvre 3 951 fichiers non-cache, 826 recalculs et 437 liens MLP GE4X; il indique explicitement qu'aucune candidate ne satisfait simultanément non-infériorité prédictive et toutes les dimensions de ressources. OOF est exact dans le cadre de son protocole mais plus lent en entraînement et latence batch 1 que MLP GE4X.
- **EX6** : version V003 et audits finaux, avec paramètres, métriques recalculées, checkpoints et rapports; les résultats sont issus des mêmes familles de sondes/MLP. Les scripts et logs sont conservés, mais ils ne sont pas importés dans le runtime chat v8.

Ces expériences ne doivent pas être utilisées pour renommer les Obsiss en RBF/probes adaptatives. Le terme « sonde » recouvre ici plusieurs objets expérimentaux différents : les Obsiss de la base v6/v7, les sondes adaptatives RBF des campagnes EX4–EX12 et les observateurs NGeGenBrain. Leur identité mathématique et logicielle doit rester distincte.

## 22. ORDER80.4.7 — transfert de compétences par maître boîte noire

ORDER80.4.7 décrit `Teacher LLM → 5 spécialistes → micro master → OIFL → final ORDER`, avec observation de la perte, attention surface/focused, entraînement, choix de focus et orchestration `prompt → think → rethink → act`. Le rapport donne un teacher Transformer causal réel de 111 424 paramètres, 123 événements d'observation, un split temporel 32/8 et un transfert OOD faible pour la prédiction de perte (MAE 1.56257 sur 12 probes nouvelles). Sur le nouveau dataset, le mode surface est meilleur que focused dans le profil rapporté; le focus n'est donc pas universel. Le final utilise des compétences acquises, du RAG et un état de mémoire vide au démarrage.

Ce système n'est pas transféré dans eSonde v8 : il dépend d'un teacher LLM et d'une chaîne de compétences acquises, de RAG et de mémoire. Il ne répond pas à la contrainte d'une architecture autonome non neuronale et sans moteur mémoire. Ses conclusions OOD sont utiles comme rappel qu'une acquisition locale de compétences ne garantit pas une généralisation uniforme.

## 23. Audit du code eGenBrain v4 et réutilisation non architecturale de ses observations

Le code `Amodel_eGenBrain_v4/egenbrain/observations.py` implémente quatre échelles opérationnelles emboîtées : `lexical_identity`, `ordered_alignment`, `relational_ecosystem`, `provenance`. Chaque niveau inclut le précédent dans son payload; l'égalité à une échelle plus fine implique donc l'égalité aux échelles plus grossières. Le module fournit les empreintes SHA-256, les clés de partition structurelles, le premier niveau distinguant deux candidats, les comptes de classes d'équivalence et un test de raffinement monotone. Le docstring précise expressément qu'il s'agit de probes opérationnelles finies, pas d'une distance sémantique universelle ni d'un certificat de vérité.

C'est une contribution méthodologique utile pour le laboratoire Obsiss : après génération libre, calculer les classes d'équivalence induites par chaque canal et par des sous-familles de canaux, mesurer le raffinement marginal de chaque observation et identifier les canaux redondants. La mesure doit être faite sur les mêmes prompts et candidats, sans injecter la réponse cible dans les observations. Elle ne doit pas devenir un nouveau score de qualité du modèle.

Le code `core.py` reste une base de tokenisation, signatures lexicales, splits et retrieval de faits/réponses. `mesh_v4.py` implémente un stockage SQLite de faits, relations, règles et dérivations décimales certifiées; `v4.py` arbitre maillage certifié → retrieval v3 → abstention. Le code est non neuronal selon le scan statique, mais il est fortement dépendant d'une base persistante, de règles explicites et d'un fallback retrieval. Ce n'est pas le cœur génératif demandé; seules les observations finies et la séparation preuve/retrieval sont retenues comme outils d'audit.

## 24. Portée exacte de la théorie DDD — généralisation, expériences et no-go

La définition DDD de « généralisation observationnelle » est relative au quotient global induit par les régimes admissibles : elle garantit la factorisation des quantités constantes sur les fibres et précise explicitement qu'elle ne donne pas accès aux distinctions absentes du quotient. Ce concept n'est donc pas, à lui seul, une preuve de généralisation statistique hors distribution ou de qualité de chat. Dans eSonde v8, il doit être relié à des tests sur prompts inédits, paraphrases, domaines et contextes tenus à l'écart.

L'annexe expérimentale du monde fini utilise 100 objets, 10 propriétés cachées et une famille croissante de sondes, sans apprentissage ni optimisation. Elle vise la reconstruction de partitions, seuils, arbre, mesure et courbe à partir des réponses. Le texte rapporte un résultat `curve_and_measure: FALSIFIED`, puis l'attribue à une convention de test (`jump at b` vs `jump immediately after alpha`) sans joindre le script source `puzzle_experiment.py` dans le sous-arbre examiné. L'affirmation que l'échec est uniquement un artefact de script n'est donc pas reproduite indépendamment ici; elle reste un diagnostic rapporté. Le résultat ne doit pas être effacé ni transformé en succès vérifié.

Le « chat de Naszimger » et la « double fente » sont explicitement des analogies structurelles dans l'espace des empreintes. La probabilité de branche y est définie par un échantillonnage uniforme `|B|/|A|`, non déduite de la mesure de seuils et non assimilée à une probabilité quantique. Le texte refuse explicitement de conclure sur la physique de Schrödinger. Ces exemples illustrent la logique de fibres/raffinement, pas une capacité d'intelligence ou une loi physique.

Le transport observationnel démontre une factorisation unique des opérations qui préservent les fibres; le document précise qu'il ne prouve ni accélération matérielle, ni supériorité computationnelle. Le no-go « pas de pont magique » interdit d'interpréter une transformation interne comme une modification d'un monde externe sans pont de réalisation et vérification séparés.

L'ordre 5 conserve également des contre-exemples et limites importants : cas vides/singletons pour les normalisations, supremum non atteint, distribution de seuils sans affectation aux paires, reparamétrisation non injective qui fusionne des niveaux, et conditions d'admissibilité pour A*. O49–O51 ont des frontières de code/artefacts; le texte précise que l'opération `relax` du code O51 ne traite que son premier argument et ne doit pas servir de preuve d'une relaxation correcte. Les résultats O49–O51 dont le code manque sont des résultats rapportés, non des reproductions indépendantes.

## 25. Vérification du point O51 `relax`

Le livre DDD affirme que le code O51 fourni implémente `relax` en évaluant seulement son premier argument. Dans le sous-arbre `theorie_emp/formalismes` inspecté, aucun package O51 exécutable ni fonction correspondante n'a été localisé; le code concret trouvé est celui de `model_order_59_corrige/src/order59/core.py`, où `relaxation(c, weaker)` combine bien les deux entrées par disjonction et possède un test `test_constraint_relax_uses_both_inputs`. Les textes O51 et leurs duplications apparaissent dans plusieurs copies du DDD, mais pas le package O51 incriminé. La conclusion exacte est donc : l'audit DDD rapporte le défaut O51; le code original O51 n'est pas disponible dans le sous-arbre vérifié; O59 contient une correction explicite, sans que cela permette de reconstituer l'implémentation O51 manquante.

## 26. Défaut de sûreté trouvé dans le code ORDER59 associé

Le code `models_order/model_order_59_corrige/src/order59/core.py` corrige bien `relaxation(c,weaker)` en disjonction des deux contraintes, et son test couvre les cas `x=1`, `x=2`, `x=3`. Mais `Constraint.holds()` intercepte toute exception du prédicat et retourne `True`. Cette politique est fail-open : une erreur d'évaluation peut rendre une contrainte vraie, et dans une disjonction elle peut faire accepter un état non vérifié. Le test fourni ne couvre pas ce cas. Ce code ne sera pas réutilisé dans eSonde v8; toute vérification déterministe v8 doit distinguer `TRUE`, `FALSE` et `ERROR/UNKNOWN`, et ne jamais transformer une exception en satisfaction.

## 27. NGeGenBrain v3.1 — révision plus récente que v2

La branche NGeGenBrain v3.1 doit être distinguée de v2 : elle charge réellement trois checkpoints locaux (SmolLM2 GGUF Q8_0 ~134,5M paramètres, TinyLLM PyTorch/SentencePiece ~76,9M et l'étudiant v3.1 ~55,6k) et exécute des observations/interventions directes. Le générateur étudiant est un byte-GRU v3.0 gelé; un routeur d'observation appris de 1 032 paramètres est ajouté à partir d'embeddings d'octets et de représentations récurrentes. Le produit est donc neuronal (GRU et routeur appris) et exclu du runtime v8.

Le rapport v3.1 annonce 66/66 tests, 65/65 régressions V1, comparaison directe sur 16 textes anglais et 8 chinois, et préservation exacte de 24 logits du générateur v3.0. BPB anglais : SmolLM2 1.2910, TinyLLM 2.1308, étudiant 2.9968; BPB chinois : TinyLLM 1.6790, SmolLM2 3.6776, étudiant 31.6871. Le routeur multi-vues obtient 9/32 (28.1%) sur le holdout frais contre 12.5% uniforme et 2/16 sur validation. Les interventions sur les blocs source sont effectuées sur un prompt par modèle; le rapport dit explicitement que les labels de couches ne sont pas des labels sémantiques certifiés et que la reconstruction mécaniste complète n'est pas démontrée.

Cette branche fournit des pratiques d'audit (comparaison même texte, BPB entre tokenizers, intervention `zero_update` préservant la connexion résiduelle, contrôle exact des logits, séparation de la génération et de la voie analytique). Aucune de ses couches, GRU, embeddings, routeur ou poids n'est transféré dans eSonde v8.

## 28. AAM O82.2 / ROCA-D — système non-LLM à mémoire obligatoire

La branche O82.2 décrit un runtime standard-library-first non-LLM avec observation contractuelle, empreintes partielles, retrieval mémoire obligatoire, suffisance décisionnelle, politique lexicographique, bundles, correction/CEGIS, capsules de compétences, auto-observation causale, découverte de probes, décomposition, root-retest, recovery et replay. Les rapports P05/P06/P07 et P11/P12 revendiquent des gates de tests bornés, notamment mémoire/retrieval et hiérarchie, mais l'architecture reste explicitement centrée sur une mémoire persistante consultée après chaque observation. C'est incompatible avec la règle eSonde v8 de ne pas substituer la mémoire à l'intelligence dialogique et avec le périmètre chat prompt/réponse sans moteur d'outils.

Les pratiques de gouvernance indépendantes (préflight, checklists hors runtime, ledger append-only, `UNRESOLVED` scoped, séparation proposition/preuve, tests de recovery) peuvent inspirer le protocole de développement et d'audit v8. Elles ne sont pas incorporées au moteur de génération. O94.6 est une évolution de cette famille vers RAG, fournisseurs de génération et orchestrations plus étendues; la conclusion de non-transfert du cœur mémoire demeure.

## 29. AAM O81 — expériences « réelles » mais non conversationnelles

`O81_0_1_real_world_experiment.tex` décrit une architecture observation/fingerprint/déficit/policy/learner/skill/holdout-OOD/runtime/mémoire/replay sur trois tâches tabulaires scikit-learn : Wisconsin, Wine et Diabetes. Les deux tâches de classification atteignent respectivement 29/30 et 31/35 prédictions runtime correctes; Diabetes reste `UNRESOLVED` et la compétence est rejetée. Le rapport note un self-health `PAS_BIEN` constant malgré des traces sans erreur d'étape, montrant que l'auto-évaluation interne et l'exactitude externe sont deux mesures distinctes.

`O81_0_3_language_real_experiment.tex` porte sur classification SMS spam/ham (5 574 SMS anglais et table multilingue), pas sur génération de réponses conversationnelles. Les compétences L1/L2 sont des classifieurs d'arbres; runtime 10/20 pour L1 et 18/20 pour L2 sur les cas présentés, et RAG lexical Recall@1=0.1667, Recall@3=0.8333. Ces résultats ne doivent pas être présentés comme une évaluation de chat, ni comme un corpus prompt/réponse. La méthode de séparation train/holdout/OOD, vérités externes, admission/rejet et replay peut inspirer le protocole de validation v8, mais l'architecture classifieur/mémoire/RAG n'est pas importée.

## 30. ORDER77 — synthèse de programmes, non génération de dialogue

ORDER77-1.4 est un runtime de synthèse de programmes Python à partir de `ProblemSpec`, d'une empreinte programmatique, d'un catalogue de 14 stratégies (BFS, Dijkstra, DP, chaînes, etc.), d'un constructeur AST, d'un contrôle statique puis d'une validation dynamique sur les exemples du contrat. Il stocke des observations de stratégie (empreinte, stratégie, succès, raison, provenance), pas le code source, et distingue `VERIFIED`, `SYNTHESIZED_UNVERIFIED` et `UNRESOLVED`. Le rapport revendique une campagne externe de 325 cas fuzz et une falsification d'un opérateur modifié; la validation demeure conditionnée au jeu d'exemples et n'établit pas la correction universelle.

Ce modèle n'est pas un moteur de langage naturel ou de chat : ses stratégies sont des constructeurs spécialisés et son contrat est un JSON structuré. Il ne doit pas être utilisé pour transformer un prompt conversationnel en une liste de scripts prédéfinis. Les idées de séparation contrat/artefact, contrôle AST, provenance, test de falsification et statut explicite sont des pratiques de validation; la mémoire de stratégies et le catalogue de programmes ne sont pas transférés au cœur eSonde v8.

## 31. Formalisme « sonde adaptative » et distinction avec Obsiss

`sonde_adapt_global_research_final/source_copies/etude_et_formalisme_sonde_adaptative_1.tex` distingue cinq niveaux : fonction observable, inclusion représentationnelle, approximation statistique, substitution composée et équivalence mécaniste. Il prouve qu'une fonction affine suivie d'une activation appartient à une classe qui la définit explicitement; il prouve aussi la non-identifiabilité d'une fonction arbitraire à partir d'un nombre fini d'observations, et une borne d'erreur aval sous hypothèse Lipschitz. Les résultats RBF sont limités à certaines cibles artificielles/benchmarks; la composition conserve le lecteur aval du MLP et l'écart de logits augmente avec le nombre d'unités remplacées. Le document conclut que l'universalité RBF, l'équivalence mécaniste et la substitution autonome de réseaux entiers ne sont pas établies.

Cette distinction est importante pour le vocabulaire v8 : les Obsiss ne sont pas les « sondes adaptatives » RBF de ces campagnes. Les Obsiss sont des observateurs populationnels signés sur les 16 dimensions; les RBF sont des fonctions à centres et largeurs apprenables, souvent entraînées par Adam et comparées à des MLP. Les expériences RBF/MLP sont exclues de l'architecture v8. Les définitions de revendications, la non-identifiabilité finie et la propagation Lipschitz peuvent inspirer les preuves et tests, sans importer l'algorithme RBF.

## 32. AAM O90 — formalisation et laboratoire comme source de méthode

O90 est l'un des dossiers théoriques les plus proches de l'ambition d'intelligence forte : il sépare un vecteur de dimensions de mesure opérationnelle (référence, contexte, invariance, composition, contrefactuel, planification, acquisition, transfert, correction, méta-observation, ressources) de toute affirmation philosophique globale. Il formalise observation traçable, empreinte, équivalence, factorisation de tâche, sélection active de sondes, compétence comme artefact exécutable, généralisation relative, contre-exemples, vérification séparée et gouvernance des certificats. Il distingue explicitement couverture exacte et couverture généralisée.

Le laboratoire O90 compare six variantes V1–V6. La V6 FHVP (empreinte–habileté–vérification–pilotage) reçoit 4,60/5 dans un barème architectural pondéré; le texte dit explicitement que ce score est une décision architecturale révisable, pas un score d'entraînement ni un résultat d'O90. O90 lui-même n'est pas implémenté dans ce dossier. Les cycles O81/O82/O85 relus montrent des exemples de réussite exacte avec couverture généralisée nulle, et un HOLDOUT parfait suivi d'un OOD faible (O81 : 1,0 HOLDOUT, 0,1667 OOD vs baseline 0,4). Les résultats O85 restent hétérogènes : macro P6 66,07% HOLDOUT / 67,66% OOD rapporté, G7 19,30% OOD et G6 42,80% OOD. Ces données illustrent pourquoi la couverture exacte, le transfert et les familles critiques doivent être séparés.

### Éléments méthodologiques transférables à eSonde v8
- Définir plusieurs dimensions de qualité du chat, sans les confondre avec les 16 canaux d'observation Obsiss. Les 16 canaux décrivent les signaux observés; le vecteur O90 décrit les capacités évaluées.
- Séparer `exact_covered` de `generalized_covered`; une réponse retrouvée par association exacte ne prouve pas la généralisation.
- Tester paraphrases, noms/attributs permutés, combinaisons inédites, contexte multi-tour, langues/domaines tenus à l'écart, perturbations, distracteurs, négation, référence et contrefactuels.
- Séparer le générateur et l'évaluateur; l'évaluateur ne doit pas voir les labels ou la mémoire d'acquisition.
- Préenregistrer les splits, seeds, métriques et seuils; au moins cinq graines lorsque le coût le permet, et publier le nombre exact.
- Évaluer après sérialisation/rechargement et démarrage à froid, pour détecter les dépendances cachées à l'état d'acquisition.
- Garder un statut d'incident `UNRESOLVED` dans l'audit sans autoriser le moteur à s'abstenir dans les expériences normatives; non-réponse désactivée dans le générateur.
- Utiliser les métriques par famille et les planchers critiques; aucune moyenne ne doit masquer une faiblesse de cohérence, d'ancrage ou de transfert.

### Éléments non transférés au moteur
Le cycle O90 V6 inclut mémoire brute/épisodes/empreintes/compétences/certificats, capsules de skills, exact-memory, RAG optionnel, décomposition, compositeur relationnel et méta-contrôleur. Malgré sa sophistication, ce noyau persistant de compétences/mémoires ne sera pas importé tel quel dans eSonde v8, dont la règle rouge interdit de remplacer l'intelligence de dialogue par une mémoire d'exemples ou de réponses. Les concepts de compétence peuvent être utilisés comme catégories d'évaluation, pas comme une bibliothèque de réponses préfabriquées.

## 33. AAM O83–O88 : langage AAM-native, mémoire et mécanismes candidats

### O83 — langage Prompt/Think/Rethink/Act
O83 est le plus directement orienté chat parmi les formalismes AAM examinés : texte naturel → atomes token/caractère opaques → empreinte TF-IDF → récupération de mémoire → profils structurés → candidats stateful/stateless/composition → rethink → rendu naturel + JSON. Son banc comprend 52 exemples (34 TRAIN, 9 HOLDOUT, 9 OOD), huit intentions et deux langues. A4 obtient 88,9% d'intention HOLDOUT et 55,6% OOD, 100% de langue; le modèle garde une erreur OOD explicite (« See you later, take care » routé vers location). Les essais montrent que la répétition d'exemples identiques n'apporte pas de gain mesuré et que l'ajout d'exemples distincts améliore le banc.

Mais O83 déclare explicitement que la réponse naturelle provient des unités de surface présentes dans la mémoire de réponse; le score de rethink compare des candidats mémorisés et la composition assemble des clauses déjà observées. C'est donc un prototype retrieval/mémoire de chat, pas une démonstration de génération ouverte ni une solution à l'exigence d'intelligence non mémorielle. Il est conservé comme baseline historique et source d'interface, pas comme architecture normative v8.

### O83.2 — empreinte relationnelle hiérarchique
Le formalisme O83.2 ajoute graphe relationnel, filtration local/contextuel/global, empreinte locale, empreinte contextuelle orientée, digest global factorisé, récursion relationnelle, canonicalisation de sous-graphes, quotients relationnels, witnesses de raffinement et sélection de probes par hitting-set. Le théorème de raffinement monotone est conditionnel à la conservation exacte du niveau inférieur dans le tuple supérieur; la séparation `Psi_r` reste une hypothèse sur une classe déclarée, et la simulation du laboratoire ne prouve pas l'injectivité universelle. Cette structure pourrait produire des preuves de raffinement des observations, mais elle ajoute un graphe, une mémoire d'empreintes et des niveaux récursifs. eSonde v8 ne l'adopte pas par défaut : les 16 canaux Obsiss fournissent déjà un espace d'observation explicite, et tout raffinement relationnel doit démontrer un apport marginal.

### O86.1 — recherche de pondération AAM-native
O86.1 compare intersection, union, rareté, distance, transition, compatibilité de conséquence et support. Tous les mécanismes candidats sont ex aequo à 0,4375 sur la validation interne; la formule `0.5 I - D` est retenue par tie-break déterministe, pas par supériorité. Les essais signalent copie mémoire dominante, 0/4 compositions exactes et 0/4 cas de généralisation forte A+D exacte. L'architecture est non neuronale, mais son cœur reste la sélection de candidats mémoire et la composition de fragments mémorisés. Elle ne constitue pas un générateur ouvert.

### O87.1 — recherche d'une loss/attention AAM
O87 sépare LLM-R (référence Transformer), AAM1 (cible AAM-only) et AAM-P (observateur AAM-only), sans transfert de l'état LLM vers AAM1. Les trajectoires AAM courtes donnent une formule de loss avec Spearman 0,5 sur une seed, mais les trois réplications choisissent trois mécanismes différents (`aam_attention_search`, `jaccard_weighted_rarity`, `symbolic_formula`). La loss n'atteint pas les critères de stabilité/causalité. L'attention candidate donne un signal mais n'est pas stable entre seeds/ordres. Ce laboratoire fournit une bonne séparation de rôles et des contrôles, pas un mécanisme de sens établi.

### O88 — séparation représentation / interaction / référence
O88 utilise un corpus SMS de 5 574 messages (4096/512/512/454), un LLM-R indépendant comme référence et un AAM1 sans Transformer/GRU/LSTM/Seq2Seq/embeddings/états LLM. Les familles F0–F5 utilisent notamment n-grammes de caractères hachés et buckets génériques. F4 atteint 0,9564 OOD naturel; F0/F4/F5 choisissent `competition` sur 5/5 seeds. Toutefois la recherche de loss perd sa structure après retrait de tendance (corrélation brute médiane absolue ~1, médiane après detrending 0,09524), les interventions ciblées ne dépassent pas le contrôle aléatoire de façon directionnelle, et les 1 920 constructions testées sont classées `overlap` : aucune nouveauté de génération n'est retenue. Le rapport conclut « mécanisme insuffisamment identifié », sans conclure à l'impossibilité d'AAM.

### Conséquences pour eSonde v8
Les contributions transférables sont : séparation stricte entre observateur, cible et évaluateur; test ON/OFF des mécanismes d'attention; distinction entre nouveauté réelle et chevauchement/recombinaison; suivi des trajectoires sur plusieurs seeds; contrôle de tendance et d'identifiabilité; et maintien des erreurs lexicales OOD. Les éléments non transférés sont les mémoires de réponses, retrieval, prototypes d'intention, composition de clauses mémorisées, LLM-R injecté, ou les scores heuristiques qui ne sont pas démontrés comme mesure de cohérence.

## 34. ORDER72–ORDER75 : modèles émergents et solveurs exacts

- **O72** : modèle de monde émergent avec représentation relationnelle, opérations internes, validation de preuves, mémoire de monde et décision; il n'est pas un générateur de langage naturel autonome.
- **O73 eC-ng** : chaîne langage/contrat/noyau/preuve/observation, avec adaptateur linguistique externe et stockage de compétences; le composant de langage n'est pas autonome et la mémoire reste centrale.
- **O74 eC-4** : architecture de contrôle autour d'un LLM gelé, avec monde interne, vérificateur, planification, outils, mémoire et budget. Le LLM reste un composant neuronal externe; architecture hors contrainte v8.
- **O75.1** : utilise réellement Supra-50M local pour compréhension/formulation, puis grounding déterministe, noyaux spécialisés, ProofBridge et checkpoints. Le benchmark Z340 reste `UNRESOLVED` malgré une classification d'intention correcte; le texte de sortie du LLM est répétitif et ne déchiffre pas le cas. Cette architecture ne peut pas être importée car elle embarque un Transformer et un système de mémoire/contrats spécialisés.
- **O75 Math O75.2** : solveur exact sans LLM pour polynômes, Gröbner, Sturm, inégalités, nombres, matrices et domaines finis, avec certificats rejouables et états `PROVEN/UNRESOLVED/ERROR`. C'est un solveur mathématique symbolique spécialisé, pas un modèle de chat. La distinction entre preuve, calcul incomplet et erreur est utile pour l'audit, mais le solveur ne devient pas le cœur eSonde.

Les éléments transposables restent des garanties de provenance, de séparation entre proposition et preuve, de checkpoint atomique, de test sans oracle et de statut d'exécution; les modèles du monde, solveurs spécialisés, mémoires et backends LLM ne sont pas intégrés.

## 35. Construction réelle des poids Obsiss V6 et implications

Le `TRAIN_RESULT.json` et `esonde_v6/model.py` établissent que `weights.bin` est construit à partir de deux vecteurs de base calculés sur TRAIN : moyenne des vecteurs locaux (`base_hidden`) et combinaison du vecteur global et de la moyenne locale par document (`base_published`). Pour chaque indice Obsiss, `build_weights()` applique une permutation signée déterministe de ces deux vecteurs, dérivée du couple `(global_seed,index)`, puis quantifie en int16. Le million d'Obsiss ne correspond donc pas à un million de paramètres indépendamment optimisés; chaque ligne est une perspective déterministe distincte sur deux vecteurs de base, puis évolue via l'état d'interaction. Cette diversité doit être mesurée (unicité, corrélations, diversité de vote, apport marginal) avant de conclure à l'indépendance de la population. Le manifeste `TRAINED` qualifie la construction/statistique, pas un apprentissage par gradient.

Le split v6 est de 14 545 TRAIN, 3 VALIDATION et 4 TEST après déduplication, pour 260 969 tokens TRAIN et 48 520 types. Il est donc trop petit en validation/test pour soutenir seul une affirmation générale. Cette faiblesse de puissance statistique explique la priorité d'OASST1 v8, sans prédire son résultat.

## 36. Pipeline génératif v6/v7 et statut du raffinement discret

Le générateur original n'est pas seulement un tableau de transitions : il combine beam n-gramme, expansion par graphe de cooccurrence symétrique intra-texte, cinq signaux de classement, fusion de rangs égaux, puis un raffinement de segment masqué. Le raffinement choisit le token le moins soutenu, masque une courte plage contiguë, propose un infill à partir des contextes gauche/droit, puis accepte seulement si l'énergie interne diminue. Le code l'appelle `absorbing-MASK refinement` et précise qu'il est heuristique, non Gibbs exact. L'énergie est un NLL n-gramme + pénalité de répétition − PMI interne; elle n'est pas une mesure humaine de cohérence.

Ce pipeline est un candidat génératif non neuronal important à préserver et formaliser, car il fait plus que récupérer une réponse complète. Il doit cependant être évalué en génération libre, avec analyse des pseudo-mots, de l'ancrage prompt, des répétitions, des réponses hors sujet et de la diversité. Le formalisme v8 actuel ne détaille pas encore toutes les règles de `diffusion_refine()`; cette omission doit être corrigée avant la phase d'implémentation finale. Les fonctions `answer_question()` et `infill_text()` ne doivent pas devenir des modes UI distincts; l'infill reste interne au raffinement du chat.

## 37. Découverte critique : deux bases 16D couplées par hypothèse

Le checkpoint V6 et les états P/R vivent dans un espace de 16 CountSketch buckets hashés (features locales/globales); les 16 canaux V7 vivent dans un autre espace, nommé et ordonné manuellement (transitions, associations, morphologie, rôle, polarité, temporalité, etc.). `ObsissPopulation` exige seulement `dimension==16` et ajoute le vecteur CountSketch P/R aux poids Obsiss avant de les appliquer aux rangs des canaux V7. L'égalité de dimension n'établit pas l'alignement des bases. Il s'agit d'une hypothèse cachée majeure à vérifier.

Le laboratoire doit comparer le couplage actuel, l'absence de q dans les poids de canaux, q comme signal séparé, des permutations fixes préenregistrées et une transformation linéaire estimée sur TRAIN puis gelée. Ces essais ne doivent pas guider artificiellement le modèle vers les réponses attendues; ils doivent être sélectionnés sur VALIDATION et confirmés sur TEST. L'identité et les lignes Obsiss restent intactes.

Autre distinction : le chat v7 utilise le premier état exact V6 `F_h/F_p` et n'exécute pas la diffusion de voisinage V6 dans son hot path; `diffusion_refine()` est un second opérateur, séparé, de masquage/réinfill de texte. Les deux mécanismes doivent être formalisés séparément.

## 38. Profil OASST1 : statistique agrégée, multilinguisme et bornes

Le profil v8 contient un seul `everyday_dialogue` et agrège 48 549 exemples non vides issus de 48 557 lignes TRAIN. Il conserve 57 884 ancres, 252 793 tokens réponse distincts, 252 103 clés bigrammes, 1 762 580 clés trigrammes et 6 950 298 occurrences de tokens. Il ne stocke pas les paires brutes ni les réponses complètes, seulement des compteurs ancre→token et des transitions internes aux réponses; c'est une statistique de génération, pas une mémoire épisodique. La distinction ne suffit pas à prouver la généralisation : les associations peuvent mémoriser des cooccurrences fréquentes et doivent être évaluées sur des prompts/paraphrases/arbre inédits.

Le constructeur ignore actuellement `row.lang` et mélange au moins 20 langues dans le même profil (TRAIN : en 21 954, es 14 294, ru 3 739, zh 1 730, de 1 699, fr 1 380, etc.). Le sélecteur de langue V6 ne conditionne pas ces tables OASST1. Il faut comparer le profil mixte à des profils/conditionnements par langue dans le cadre du chat, sans ajouter de fonction de traduction.

Les paramètres `K=16` dernières ancres uniques, top-128 arêtes par ancre, top-64 continuations bigrammes/trigrammes, top-256 débuts de réponse et support minimal de deux ancres sont des bornes non validées. Le laboratoire doit mesurer leur impact sur la couverture, le contexte long, les langues rares et la génération libre. Les limites ne seront ni conservées ni retirées par intuition seule.

## 39. Lecture intégrale de PCH routage v11 — preuves et hypothèses

Le manuscrit v11 (702 lignes) pose une famille finie de contextes `C={1,…,K}`, chacun avec un ensemble convexe fermé non vide `M_c`, puis une énergie quadratique + distance au contexte + ridge. Les résultats d'analyse convexe sont globalement corrects sous ces hypothèses : unicité du minimiseur local, identification à une prox/enveloppe de Moreau, gradient explicite, valeur globale comme minimum fini, cellules strictes/points de bord, routage entropique softmax et convergence du pré-roulage sous contraction.

Trois réserves doivent rester explicites pour l'adaptation eSonde :
1. Le manuscrit suppose le noyau PCH « déjà défini et validé »; cela ne constitue pas une validation empirique sur le langage, et les ensembles `M_c` ne sont pas construits à partir des 16 observations Obsiss dans ce texte.
2. La normalisation `J_c/μ_c` ne change pas le minimiseur local, mais elle change les valeurs comparées entre contextes. La prétention que cela place les contextes sur une échelle « canonique » est un choix de routage, pas une conséquence de la seule convexité; il faut ablater la normalisation et mesurer le biais induit.
3. Le pré-roulage suppose un facteur de contraction `ρ_c<1`. La forte convexité de la fonctionnelle proximale suggère une preuve directe d'une borne de contraction, mais le manuscrit pose l'hypothèse sans la dériver. Cette preuve doit être ajoutée avant d'utiliser le pré-roulage comme certificat.

Le noyau proximal simple-hull de la formalisation v8 n'est donc pas automatiquement équivalent au routage multi-contextes v11. Le laboratoire doit définir comment les contextes `M_c` sont obtenus sans labels de réponse, comparer valeurs brutes/normalisées, route dur/soft et single-hull/multi-contextes, puis mesurer l'effet sur le chat. La convexité seule ne prouve pas l'amélioration de la cohérence.

## 40. ORDER69 et ORDER71 — méthodes de sondage, publicité et limites

**ORDER69** formalise la composition parallèle/séquentielle de sondes, les sondes relationnelles/mirror, les trajectoires parallèles et le changement de repère/oubli. Son théorème de limite dit qu'une composition déterministe de sorties déjà égales ne peut pas séparer une paire; une composition parallèle ne peut que raffiner la partition. Le critère target-free `G_H(c)=H_2(Π_{P∪{c}})-H_2(Π_P)` mesure l'apport d'une sonde sur un domaine fini sans utiliser la bonne réponse. Les résultats O69.1 (2→4 classes avec A⊗B; 1→3 avec miroir) sont des certificats finis de laboratoire, non des universalités. Les trajectoires, la fusion Markovienne et l'oubli sont liés à une mémoire temporelle; ils ne sont pas importés dans le chat v8.

**ORDER71** prolonge DDD avec contraintes typées, déficit exact, plan d'expérience, compilateur, certificat de publicité, décision publique, adéquation sémantique, pruning conservateur et niveaux de preuve. Le document distingue explicitement compilation correcte, dépendances publiques et adéquation sémantique; deux premières ne garantissent pas la troisième. Il documente une fuite de cible dans un ancien benchmark O70 (`correct/public_score` accessibles à l'évaluateur) et refuse de réutiliser ce protocole. Il indique aussi que l'attention WM O70 est locale au domaine d'entraînement, non preuve de raisonnement universel. O71 contient une mémoire et un backend attentionnel optionnel; ils ne sont pas repris.

### Apports transférables
- Utiliser le raffinement des partitions et l'entropie de partition target-free pour mesurer la contribution de chaque canal Obsiss sans injecter de réponses cibles.
- Si deux états sont identiques sur les 16 observations, aucune recombinaison déterministe de ces seules observations ne peut les séparer; il faut une nouvelle information observable, pas une transformation cosmétique.
- Distinguer validité du pipeline, provenance/publicité des entrées, adéquation au sens du prompt et qualité de la réponse.
- Prévoir tests positifs, négatifs, ablations, contre-factuels et replay; conserver le statut `OPEN` quand une capacité n'est pas établie.
- Ne jamais laisser l'évaluateur lire la cible ou un champ de vérité cachée pendant la génération/notation.

Ces principes sont des outils d'audit et de recherche, pas des composants de mémoire ou d'attention ajoutés au runtime.

### Disponibilité des branches historiques citées
Le texte ORDER69 renvoie à une formulation O65 et ORDER71 à un backend O70/WM attention, mais aucune source O65/O70 exécutable n'a été localisée dans `theorie_emp/` ni dans les sous-dossiers `formalismes/` extraits. Les théorèmes abstraits d'O69/O71 peuvent être vérifiés à partir de leurs textes; leurs résultats de laboratoire O69.1 et O70 sont des résultats rapportés dans les manuscrits, non des reproductions indépendantes de code dans le présent audit. Aucune composante attentionnelle O70 n'est importée.

## 41. Rapport PCH Cas 3 normalisé — stabilité mathématique vs performance routée

Le rapport PCH agrège 13 blocs ex1–ex13 (54 runs) puis un tableau complémentaire ex20–ex29. Le pipeline expérimental est explicitement : encodeur SentenceTransformer gelé, PCA ajustée sur calibration, contextes `M_c` comme enveloppes convexes des embeddings de calibration, projections/minimiseurs/prox résolus par QP (CVXPY/OSQP), jacobiens par différences finies. L'encodeur SentenceTransformer est neuronal et ne peut pas être transféré dans eSonde v8; les résultats aval ne sont pas des résultats Obsiss.

Le verdict « supporté » de 7/13 blocs porte seulement sur les écarts normalisés `rho_gap` et `operator_gap` sous seuils `1e-4`; il ne porte pas sur la classification ni sur le chat. Le rapport montre précisément que l'oracle de contexte peut être très performant alors que le routage automatique reste faible : sur 20news20 en dimension 16, ex8 donne oracle 0,96094 mais routed 0,56563 et contexte correct 0,49688; sur ex26/ex27 l'oracle est ~0,99 tandis que le routé reste ~0,55. Ex24/ex25 sont le meilleur compromis du lot, mais le domaine reste la classification 20news.

La conclusion réutilisable est limitée mais importante : la stabilité mathématique du noyau proximal et l'utilité opérationnelle du routage sont deux questions séparées; le routage est le goulot dans ces essais. Pour eSonde v8, cela justifie une comparaison rigoureuse single-hull vs routage variationnel, mais ne prouve pas que PCH améliore le dialogue. Le SentenceTransformer, les embeddings et la PCA entraînée restent exclus.

### Artefacts PCH réellement disponibles
Le sous-dossier PCH contient les manuscrits TeX, rapports, PDFs, quelques fichiers TXT de conception et checklists, mais aucun script Python d'expérience ni CSV/JSON de runs dans ce sous-arbre. Le rapport Cas 3 décrit les 54 runs et les résultats, mais les scripts, paramètres exécutés et résultats bruts ne sont pas fournis ici; ces résultats restent donc rapportés par le manuscrit, non reproduits dans cet audit. Les notes `arch_route_1/2` et `pch_checklist_route` distinguent une première purification single-hull et une extension multi-contextes avec score de routage; elles confirment que la construction/sélection des contextes est un problème séparé du noyau proximal.

## 42. Extension PCH de routage par gain — correction mathématique nécessaire

`pch_routing_theory_extension.tex` propose un routeur plus intéressant que la comparaison de minima bruts : gain local `Δ_c(w)=J_c(w;w)-J_c(u_c^*(w);w)`, normalisé par `J_c(w;w)+ε`, puis maximisation du gain relatif. L'invariance du gain à un recentrage additif est correcte. La stabilité par marge et la convergence du softmax vers le routeur dur sont correctes sous les hypothèses écrites.

Mais la proposition de bornes contient une erreur formelle : elle affirme `R=1` si et seulement si `w` est déjà minimiseur. Or, si `w` est minimiseur, `u*=w`, donc `Δ=0` et `R=0`. De plus, pour `ε>0`, `Δ≤J(w;w)` implique strictement `R≤J/(J+ε)<1` lorsque `J>0`; l'égalité 1 n'est jamais atteinte. La propriété correcte sous unicité est `R=0` si et seulement si `w` est déjà minimiseur, et `0≤R<1`.

Deux autres hypothèses ne sont pas garanties dans le manuscrit : (i) `DΠ_M(u*)` peut ne pas exister lorsque la projection sur un polytope change de face; le tie-breaker `Xi` doit exiger une régularité démontrée ou utiliser une quantité définie partout; (ii) « quasi-égalité numérique » n'est pas définie dans la règle lexicographique et exige une tolérance préenregistrée. Enfin, la construction des contextes repose sur embeddings de calibration et la théorie du projecteur limite; ces objets ne sont pas établis dans l'espace 16D Obsiss. Cette extension n'est donc pas intégrée telle quelle. Elle devient une variante de recherche à corriger et comparer à v11, pas un routeur déjà validé.

## 43. Formalisme général NGeGenBrain d'observation — contribution centrale à Obsiss

Le traité `NGeGenBrain_observation_formalisme_full_0.tex` (2 097 lignes) est une base méthodologique importante, distincte de l'implémentation neuronale NGeGenBrain v3.1. Il formalise l'observation comme protocole versionné, distingue observation/mesure/enregistrement/empreinte/invariant/interprétation, prouve la factorisation par fibres, formalise la redondance et la fermeture observationnelle des sondes, les échelles et seuils, les vues multi-facettes, la sélection active, les interventions appariées, l'identifiabilité relative, les mécanismes exécutables, l'autonomie et la validation indépendante.

Ses résultats particulièrement utiles pour les 16 Obsiss sont :
1. Une propriété est déterminable par les observations si et seulement si elle est constante sur les fibres de l'empreinte; une distinction absente ne peut pas être recréée par une recombinaison déterministe.
2. L'ajout d'un canal ne peut que raffiner la partition; son apport strict doit être mesuré sur les paires qu'il sépare réellement. Les canaux empiriquement redondants peuvent être identifiés sur un domaine, sans prétendre à une redondance universelle.
3. L'entropie de partition / gain de séparation target-free peut mesurer l'apport d'une sonde sans injecter de réponse attendue. Pour eSonde, cette mesure doit être séparée de la qualité de génération.
4. Une observation stable, une mesure répétée, une invariance sous transformation et une stationnarité temporelle sont des propriétés différentes.
5. Un résumé statistique n'est pas un mécanisme : un profil OASST1 agrégé peut soutenir la génération sans prouver que le système est autonome ou généralise.
6. L'autonomie du paquet exige que les sorties dépendent uniquement du code, des poids, de l'état et des dépendances déclarées; tout appel caché à un LLM/oracle invaliderait cette revendication.
7. La fidélité comportementale, la généralisation, la fidélité interventionnelle et l'identification mécaniste sont des niveaux distincts; aucun niveau supérieur ne découle automatiquement d'un test inférieur.

Le traité comporte aussi des chapitres d'observation live continue et d'interventions internes LLM (activations, attention, gradients, MLP) conditionnels aux capacités du modèle. Ces modalités neuronales ne sont pas transférées à eSonde v8; seules les méthodes comportementales, structurelles, non neuronales, d'intervention sur ses propres opérateurs, de provenance et de validation sont applicables.

### Suite `next_1` et provenance de la théorie d'observation
La suite `NGeGenBrain_observation_formalisme_next_1.tex` développe la distinction entre empreinte et observation brute, invariance déclarée, information résiduelle, unicité invariant/variant (somme directe ou rang plein dans le cas linéaire), reconstruction conditionnelle et procédure de recherche. Le volume `full_0` indique intégrer cette suite. Le fichier `next_0` référencé par certains textes n'a pas été trouvé comme fichier distinct dans l'archive extraite; il n'est pas inventé ni traité comme une source indépendante. La portée de la théorie est donc celle des deux fichiers effectivement disponibles `full_0` et `next_1`.

## 44. eGenBrain v1 — moteur de faits typés et mémoire explicite

eGenBrain v1 est un système non neuronal de facts/relations typés, validation de provenance, règles déterministes, mémoire persistante et retrieval. Son formalisme garantit des opérations sur des faits structurés et distingue provenance/certification; il ne décrit pas un générateur conversationnel général. La version v4 ajoute des outils d'observation, un décodeur Parquet à schéma question/réponse et des diagnostics de raffinement, mais reste orientée facts/mesh/retrieval. Aucun graphe de faits ni base de réponses n'est importé dans eSonde v8. Le décodeur eGenBrain est utilisé uniquement comme primitive de lecture lorsque son schéma correspond; le schéma OASST1 a nécessité un adaptateur de colonnes distinct.
