# Guide spécialisé des théories et formalismes — Bensalem Nassim

**Auteur déclaré : Bensalem Nassim, avec assistance d'IA.** Ce document est un guide de lecture approfondi du répertoire `theories/` et des textes théoriques associés aux architectures et expériences. Les sources de référence et rapports sont principalement rédigés en français. Les lecteurs qui en produisent une traduction assument personnellement sa fidélité et sa diffusion ; une traduction n'est officielle que si l'auteur l'a expressément validée.

> **Règle de lecture scientifique.** Une définition décrit un objet ; une hypothèse propose une relation ; une proposition ou un théorème est valable sous les hypothèses et le cadre écrits ; une implémentation réalise une partie du modèle ; une expérience teste un protocole donné. Une analogie ou une spéculation n'est pas une preuve expérimentale. Les environnements LaTeX `theorem` ou `proof`, la compilation et les rapports d'audit ne remplacent pas une vérification indépendante de la correction mathématique.

## 1. Vue d'ensemble du programme théorique

Les textes théoriques ne forment pas une série de sujets isolés. Ils explorent plusieurs étages d'une même question : **comment un système peut-il observer, distinguer, représenter, relier, composer et vérifier des informations lorsque son accès au monde est partiel, dépendant d'un contexte et limité par des ressources ?**

Une lecture transversale fait apparaître six axes :

1. **Observation et information disponible** : que voit un système, à travers quel protocole, avec quelles pertes et quelles incertitudes ?
2. **Empreintes et équivalence** : quelles différences sont réellement accessibles à l'observateur, et comment raffiner une représentation ?
3. **Architecture de calcul** : comment distribuer les transformations entre sondes, cores et graphes de dépendances ?
4. **Relations et mémoire** : comment relier les observations, contextes, tokens, concepts, résultats et preuves sans inventer de relation non observée ?
5. **Composition et synthèse** : comment construire des programmes ou des comportements à partir de composants typés, contrôlés et vérifiables ?
6. **Apprentissage et recherche** : comment utiliser résidus, contre-exemples, sélection de sondes, mémoire et vérification pour améliorer une solution ?

La vision émergente est celle d'une intelligence artificielle architecturée autour de représentations multi-résolution, de sondes spécialisées, de cores coopératifs, de mémoire relationnelle et de composition vérifiable. Cette vision est une synthèse des pistes contenues dans les sources ; elle ne prétend pas qu'un cerveau artificiel universel réunissant déjà tous ces mécanismes soit livré.

## 2. Théorie des empreintes — `DDD_Base_theorie_des_empreintes_complete_order_5.tex`

### 2.1 Objets mathématiques et intuition

Le texte pose un domaine d'objets `X`, des contextes `P`, une famille de sondes `F` et une fonction d'observation notée dans la source sous la forme `Φ(P,x,f)`. Une sonde interroge un objet dans un contexte ; la réponse obtenue dépend du protocole et de la résolution.

L'**empreinte** d'un objet est le profil structuré de ses réponses aux sondes retenues. Deux objets `x` et `y` sont équivalents pour ce protocole lorsque leurs empreintes coïncident. Cette équivalence ne dit pas que les objets sont identiques en absolu : elle dit qu'aucune des sondes considérées ne les distingue dans le contexte spécifié.

Cette idée est fondamentale : l'identité observable est relative au pouvoir discriminant des observations. En ajoutant des sondes, en modifiant leur contexte ou en augmentant leur précision, une classe auparavant indistinguable peut être divisée en sous-classes.

### 2.2 Fibres, quotient et raffinement

La relation d'égalité des empreintes regroupe les objets en **fibres** ou classes d'équivalence. Le quotient correspondant décrit l'espace des distinctions accessibles au protocole. Une famille de sondes plus riche peut raffiner le quotient : elle ne change pas nécessairement les objets étudiés, mais augmente les distinctions que le système peut établir.

Le texte développe des structures de familles emboîtées, des résolutions, des seuils de séparation et, sous des conditions explicites de hiérarchie, des structures de type ultramétrique. Il examine aussi la capacité effective, la fermeture et la stabilité de certaines représentations. Ces résultats doivent toujours être lus avec leurs hypothèses : une structure ultramétrique n'est pas automatiquement obtenue pour toute famille arbitraire de mesures.

### 2.3 Factorisation par l'empreinte

Une transformation peut être décrite à partir de l'empreinte si elle ne sépare jamais deux objets appartenant à la même fibre. Autrement dit, lorsqu'une sortie dépend uniquement de l'information retenue dans l'empreinte, elle peut se factoriser par l'espace quotient.

Cette propriété donne une règle de cohérence puissante : un système ne doit pas produire une distinction qui exige une information absente de sa représentation. Si deux cas possèdent la même empreinte, toute décision fondée exclusivement sur cette empreinte doit leur attribuer le même résultat, sauf si une nouvelle observation les différencie.

Les notions de témoin et de déficit servent à repérer les insuffisances d'une représentation : une sonde additionnelle peut être nécessaire pour distinguer des cas, une transformation peut ne pas être constante sur une fibre, ou une hypothèse de clôture peut échouer.

### 2.4 Étendue des thèmes du texte

DDD_Base ne s'arrête pas aux classes d'équivalence. Le texte relie l'empreinte à des questions de :

- observation, invariance et changement de contexte ;
- familles de sondes, résolution, seuils et hiérarchies ;
- dynamique, trajectoires, ordre et évolution des empreintes ;
- identité, auto-référence et réflexion interne ;
- apprentissage, généralisation et méta-observation ;
- langage, sémantique, prédiction et génération ;
- transformations certifiées, témoins, déficits et fermeture ;
- contraintes, transfert, recherche et imagination formelle.

Ces thèmes constituent un programme théorique. Leur présence dans le même texte ne prouve pas qu'ils ont tous été implémentés ou validés empiriquement.

### 2.5 Double fente, chat de Naszimger et spéculation quantique

Le texte contient une section consacrée à une « double résolution » avec probabilité émergente et structure de type double fente. Il contient aussi un exemple géométrique de « chat de Naszimger » et une reconstruction de structure de type Schrödinger. Ces exemples sont intéressants précisément parce qu'ils rendent visible la différence entre un état décrit, les distinctions accessibles à un observateur et les informations que le protocole ne permet pas de séparer.

**Ce que le texte affirme et ce qu'il n'affirme pas :** il présente ces constructions comme des exemples internes à la théorie des empreintes. Il précise que le « chat de Naszimger » n'est pas un état physique élémentaire et que la double fente est une analogie structurelle interne au protocole. Il précise également que la reconstruction n'est pas une reconstruction du formalisme quantique de Schrödinger et qu'aucune conclusion physique sur le phénomène quantique n'est déduite de cette analogie.

**Spéculation à explorer :** si certains phénomènes réels dépendaient de ce qu'un dispositif permet de distinguer, les classes d'équivalence observationnelles pourraient fournir un langage pour décrire les informations accessibles avant et après une mesure. Dans une expérience à deux fentes, on pourrait demander si les contextes « chemin non identifié » et « chemin mesuré » correspondent à des familles d'empreintes différentes, et si une règle mathématique sur le raffinement des observations peut retrouver quantitativement les statistiques d'interférence. Pour le chat de Schrödinger, on pourrait distinguer l'état du système, son couplage à l'appareil, l'enregistrement et le point de vue de l'observateur, puis demander si les classes d'empreintes décrivent correctement les transitions entre niveaux de description.

Mais, à ce stade, cela ne constitue pas une explication de la mécanique quantique. Il faudrait notamment : établir une correspondance précise avec les espaces d'états et les observables quantiques ; retrouver la règle de Born ; rendre compte des amplitudes complexes et de l'interférence ; traiter l'intrication et la décohérence ; produire des prédictions nouvelles et quantitatives ; les comparer aux expériences ; et montrer qu'elles ne sont pas simplement une reformulation verbale de la théorie existante. Le formalisme présenté ne dérive pas actuellement ces résultats. Le « chat de Naszimger » ne doit jamais être présenté comme une solution physique déjà établie au paradoxe du chat de Schrödinger.

### 2.6 Autres domaines possibles

En vision, une image peut être représentée par des empreintes à plusieurs échelles ; en robotique, des capteurs différents peuvent produire des classes d'états partiellement compatibles ; en diagnostic, plusieurs symptômes peuvent être insuffisants pour séparer deux mécanismes ; en linguistique, des contextes différents peuvent raffiner l'interprétation d'un mot ; en interprétabilité, des sondes peuvent distinguer des états internes qui semblaient identiques sous une mesure plus grossière. Dans chaque cas, la question scientifique est la même : quelles distinctions l'ensemble de sondes permet-il réellement de soutenir ?

## 3. Formalisme de l'observation — `observation_formalisme_full_0_bundle.zip`

### 3.1 Organisation documentaire

L'archive réunit un texte consolidé `NGeGenBrain_observation_formalisme_full_0.tex`, des sources complémentaires `NGeGenBrain_observation_formalisme.tex`, `...next_0.tex` et `...next_1.tex`, leurs PDF, des chapitres séparés, un README, des informations d'audit, des éléments de traçabilité, des manifestes et des contrôles d'intégrité. L'audit de structure recense 8 parties, 51 chapitres consolidés, 94 définitions, 3 hypothèses explicites et 81 énoncés de type théorème, proposition, lemme ou corollaire avec environnements de preuve. Ces nombres décrivent la structure du document ; ils ne certifient pas indépendamment la validité de chaque démonstration.

### 3.2 Les distinctions conceptuelles

Le formalisme sépare plusieurs notions souvent confondues :

- **objet** : ce dont on cherche à obtenir une connaissance ;
- **contexte** : conditions dans lesquelles l'observation est faite ;
- **protocole/sonde** : opération qui interroge ou transforme l'accès à l'objet ;
- **observation** : résultat obtenu par le protocole ;
- **enregistrement** : trace conservée du résultat ;
- **empreinte** : représentation structurée construite à partir des observations retenues.

Cette séparation permet de poser des questions précises : l'enregistrement conserve-t-il toute l'information de l'observation ? L'empreinte est-elle suffisante pour une décision ? Une transformation déclarée conserve-t-elle les invariants pertinents ? Une observation nouvelle réduit-elle l'incertitude ou ne fait-elle que répéter une information déjà présente ?

### 3.3 Résidus, temps, intervention et problèmes inverses

Les textes explorent les composantes invariantes et variables, les résidus, les traces temporelles, les observations complémentaires, les interventions, l'identifiabilité et les problèmes inverses. Un mécanisme peut être compatible avec plusieurs observations ; dans ce cas, les données disponibles ne suffisent pas à l'identifier de manière unique. Une intervention peut apporter une distinction supplémentaire, mais une intervention isolée ne prouve pas automatiquement une loi causale générale.

Le formalisme invite aussi à traiter le temps et l'échantillonnage avec prudence : connaître des mesures à certains instants ne suffit pas nécessairement à reconstruire ce qui s'est passé entre eux. Une empreinte peut être utile tout en étant volontairement incomplète ; elle ne recrée pas les composantes perdues lors de l'observation ou de la compression.

### 3.4 Spéculation : observation et physique quantique

Une correspondance possible serait de décrire une préparation expérimentale comme un contexte, un appareil comme une famille de sondes, une mesure comme une observation et la sortie conservée comme un enregistrement ou une empreinte. Dans l'expérience des fentes, il serait alors intéressant de formaliser précisément les conditions qui rendent l'information de chemin disponible ou non et de voir si le formalisme peut exprimer la modification des statistiques d'interférence.

Pour le chat de Schrödinger, le cadre peut aider à séparer les niveaux de description : système, environnement, appareil, trace, observateur. Il peut également aider à éviter de confondre ignorance de l'observateur et propriété physique du système. Cependant, il ne résout pas à lui seul le problème de la mesure, ne dérive pas l'équation de Schrödinger et ne démontre pas une interprétation particulière de la mécanique quantique. Une application physique demanderait un pont mathématique explicite, une compatibilité avec les résultats établis et des prédictions risquées susceptibles d'être réfutées.

### 3.5 Autres applications spéculatives

En médecine, ce formalisme pourrait aider à déterminer si des mesures cliniques distinguent réellement plusieurs mécanismes ou seulement plusieurs présentations compatibles. En astronomie et en télédétection, il pourrait aider à caractériser ce que les instruments permettent d'identifier malgré le bruit et les observations indirectes. En chimie et en science des matériaux, il pourrait organiser les signatures observées et les limites d'identifiabilité des mécanismes. En contrôle et en robotique, il pourrait structurer le passage de données capteurs à une représentation d'état, puis à une intervention. Ces pistes restent des programmes d'application à tester.

## 4. Théorie des cores et des sondes — `th_sondes_core_0.tex`, `th_sondes_core_1.tex`

### 4.1 Une sonde comme unité de transformation

Les textes décrivent une sonde comme un opérateur qui prend des entrées et produit des sorties. Selon le cas, elle peut être exacte, symbolique ou apprise. Une sonde adaptative peut approximer une fonction ; un ensemble de sondes peut se répartir un calcul ou représenter plusieurs spécialisations.

Pour AdaptiveRBF, le schéma décrit comprend un encodage latent du type `z = tanh(Wx+b)`, des bases radiales gaussiennes `r_k(z) = exp(-||z-c_k||²/(2σ_k²))`, puis une combinaison de sortie dépendant notamment des paramètres des centres, largeurs et poids. Ce schéma aide à comprendre pourquoi l'architecture n'est pas simplement un MLP renommé : elle repose sur des activations locales à partir de centres et une organisation adaptable de ces centres.

### 4.2 Trois cores, trois rôles

Le **core neuronal** est la partie qui apprend des transformations grâce à des sondes adaptatives. Le **core logique** décrit la structure fonctionnelle : les opérations, leurs dépendances, leur ordre, les éléments indépendants et les résultats réutilisables. Le **core physique** concerne une réalisation matérielle possible : unités de calcul, mémoire, bus, communications, contrôleur, latence, bande passante, énergie et surface.

Cette séparation est importante pour l'architecture informatique. Un graphe logique peut contenir du parallélisme, mais celui-ci ne fournit un gain réel que si le matériel, les communications, l'ordonnancement et les coûts de synchronisation le permettent. La théorie introduit donc des coûts et des états de coordination, avec des actions de type activation, attente, transmission, réutilisation, stockage et fusion.

### 4.3 Spéculation sur des architectures IA et de calcul

On peut imaginer une IA dont les compétences sont réparties entre cores spécialisés : perception, calcul numérique, mémoire, raisonnement symbolique, validation et planification. Le core logique établirait les dépendances et contrats ; le core neuronal apporterait des approximations apprises ; le core physique exécuterait les unités de travail selon les contraintes de ressources.

Cette vision peut être comparée à des architectures neurosymboliques, à des accélérateurs spécialisés et à des systèmes distribués. Elle n'établit pas que le cerveau humain comporte littéralement ces trois cores, ni que le système est plus efficace qu'un GPU ou qu'un MLP. Les comparaisons doivent mesurer qualité, généralisation, latence, consommation, mémoire et coût de coordination.

## 5. Protocoles CNG et CNC — `th_sondes_core_test_0.tex`, `th_sondes_core_test_1.tex`

### 5.1 CNG : cœur neuronal général

Le CNG étudie la coopération d'un ensemble de sondes pour approximer une fonction générale. Les configurations discutées comprennent une AdaptiveRBF unique, des ensembles à moyenne fixe de différentes tailles, des composeurs appris, des MLP à capacité comparable et des variantes spécialisées. L'enjeu est de mesurer si les sondes se complètent, si leur combinaison est utile et dans quels régimes les performances changent.

### 5.2 CNC : cœur neuronal de calcul

Le CNC remplace ou approxime des opérateurs particuliers par des sondes spécialisées : ADD, SUB, MUL, DIV, EXP, LOG et autres opérations du protocole. Des graphes assemblent ces opérateurs pour réaliser une fonction composée. Les configurations expérimentales distinguent notamment des spécialistes gelés, des spécialistes ajustés conjointement, un MLP direct, un opérateur RBF direct et un oracle exact.

Le fait de fournir le graphe initialement est une limite déterminante : démontrer que des opérateurs neuronaux s'exécutent correctement dans un graphe fourni n'est pas démontrer qu'un agent sait découvrir de manière autonome le meilleur graphe pour tout problème.

### 5.3 Ce que montrent les campagnes

EX10 rapporte 460 exécutions CNG et 90 CNC, 1 695 évaluations de test, plusieurs fonctions et cinq seeds dans les ensembles décrits. Les résultats sont mixtes et dépendent de la tâche : certains CNG surpassent des MLP appariés sur certaines fonctions ou zones d'évaluation ; d'autres variantes ou tâches favorisent le MLP. Des configurations CNC ajustées conjointement améliorent certains graphes et en détériorent d'autres. EX11 est décrit comme exploratoire et certaines variantes reposent sur peu de seeds.

EX12 apporte une comparaison confirmatoire HC-RBF/MLP à nombre de paramètres entraînables apparié à ±1 %. Le rapport présente 320 paires candidat-MLP, 640 modèles et 2 560 évaluations sur quatre régimes. Il rapporte des avantages HC-RBF sur les régimes de frontière dans 15/16 contrastes et des gains d'interpolation pour certains cas, mais aucune supériorité générale. Les quatre variantes perdent sur `f1_sin` en interpolation ; l'extrapolation est défavorable sur trois fonctions. La latence p50 à batch 1 est environ 1,82 à 2,25 fois celle du pipeline MLP complet et le temps d'entraînement environ 1,44 à 1,62 fois supérieur. Le résultat intéressant est donc une spécialisation et une couverture parfois utiles, avec des limites nettes en extrapolation et en ressources.

## 6. Adaptation des centres RBF — `arch_up_formalisme_0.tex`

Ce texte étudie une organisation plus réfléchie des centres dans AdaptiveRBF. Il aborde contribution prédictive, résidus, ablations, redondance, sélection progressive, élagage et réentraînement. Une idée est de guider des centres plus faibles à partir de résidus ou de contributions associés à des centres plus forts. Une autre est d'organiser les centres en fonction d'empreintes décrivant position, activation, contribution et redondance.

Les variantes B0 à B5 structurent un programme expérimental allant d'une base de référence à des règles de classement, sélection, guidage, organisation par empreintes et combinaison de ces stratégies. Il s'agit d'hypothèses falsifiables sur l'utilité et la stabilité des centres, non d'une preuve que toute sélection adaptative améliore systématiquement la généralisation.

**Spéculation :** une organisation par empreintes pourrait faciliter l'interprétation de sous-régions fonctionnelles, le diagnostic de redondance ou la construction de réseaux plus spécialisés. Cela pourrait être pertinent pour des modèles scientifiques ou embarqués où l'on souhaite expliquer quels centres portent une contribution. Il faudrait vérifier que les empreintes restent stables entre jeux de données, changements de distribution et seeds.

## 7. Théories sur les cerveaux, les LLM et la mémoire relationnelle

### 7.1 `th_gen_0.tex` et empreintes de modèles de langage

Ces textes explorent l'idée que la compréhension linguistique et certaines formes de généralisation pourraient être distribuées dans des structures relationnelles contextuelles, plutôt que localisées dans un neurone isolé. Une unité peut contribuer à plusieurs motifs ou structures ; cette idée rejoint la question de la poly-sémanticité, mais la coactivation ou une projection de sondes ne suffit pas à démontrer le mécanisme interne réel.

**Spéculation :** des empreintes de contextes pourraient aider à identifier des distinctions sémantiques, des représentations partagées ou des limites de généralisation. En neurosciences, on pourrait comparer ces constructions à des hypothèses sur les représentations distribuées ; en linguistique, à des réseaux de relations entre contextes et sens. Cela ne démontre ni une identité avec le cerveau humain, ni la conscience d'un LLM.

### 7.2 `eGenBrain_1.tex` et le maillage relationnel

La formalisation eGenBrain décrit la construction d'un brain par source, la canonicalisation d'identités, l'ordre des tokens et des relations, puis leur fusion en maillage global et en maillage de contexte de prompt. Les relations inconnues restent inconnues ; la causalité et l'anti-causalité sont explicitées et ne doivent pas être déduites de simples fréquences lexicales. Les états de résultat distinguent notamment FOUND, NO_MATCH et UNKNOWN, avec provenance.

**Spéculation :** un tel maillage pourrait servir de mémoire vérifiable à un agent, à une base de connaissances évolutive ou à un système d'aide à la recherche. Dans les sciences du vivant, il pourrait organiser des relations entre observations, hypothèses et mécanismes, sans assimiler corrélation documentaire et causalité biologique.

### 7.3 Théories eLLM v0 et v1

La version v0 formalise une chaîne de Markov interpolée d'ordre variable, fondée sur des suffixes et des sondes imbriquées. La version v1 étudie des sondes multi-résolution entraînées sur les représentations cachées contextuelles d'un LLM causal préentraîné, puis une correction de logits et des composants de transport appris. Ces deux conceptions doivent rester distinctes.

Les tests de composants et les jeux synthétiques documentés ne démontrent pas un gain de qualité sur un checkpoint réel si ce checkpoint n'a pas été chargé et évalué dans le protocole correspondant. La piste est architecturale : enrichir le contexte par des sondes et une structure de mémoire ou de correction, puis mesurer le résultat face à des références contrôlées.

## 8. Théories de programmation compositionnelle et de synthèse

Les textes de programmation compositionnelle étudient composants, interfaces, types, contrats, effets, ressources, graphes et maillages, transformations, règles de composition, mémoire, provenance et vérification. Des travaux portent sur la synthèse de programmes, la décomposition hiérarchique, le CEGIS et le contrôle de l'exécution.

La vision est de rendre la composition explicite et contrôlable : chaque bloc expose ce qu'il reçoit, ce qu'il produit, ses effets, ses contraintes et son coût. Les règles permettent d'assembler les blocs tout en contrôlant les incompatibilités. Les textes critiques et de refondation examinent aussi les limites des formalismes précédents.

**Spéculation :** ces idées pourraient aider à concevoir des assistants scientifiques qui assemblent des procédures reproductibles, des robots qui doivent respecter des permissions et des ressources, ou des programmes qui s'expliquent au moyen d'un graphe vérifiable. En physique, une bibliothèque d'opérateurs pourrait inclure unités, dimensions et invariants ; toutefois, la correction formelle du programme ne prouve pas la vérité empirique de ses hypothèses.

## 9. ORDER et preuve

Les textes ORDER étudient une recherche itérative et structurée : hiérarchiser un objectif, décomposer, produire des sous-problèmes, chercher des candidats, utiliser l'information acquise et vérifier les certificats au moyen d'un noyau. Les documents et pages web peuvent servir de contexte, mais ne deviennent pas automatiquement des axiomes ou des preuves. Un budget expiré ou une recherche interrompue ne prouve pas l'impossibilité de la proposition visée.

**Spéculation :** une architecture de recherche certifiée pourrait aider en mathématiques, vérification de logiciels, découverte de modèles et planification d'expériences. Dans les sciences physiques, elle pourrait vérifier que des déductions suivent d'un modèle, mais non décider sans données si ce modèle est une description correcte du monde.

## 10. Liens entre les théories et les catégories logicielles

| Théorie ou formalisme | Architecture ou catégorie liée | Question principale |
|---|---|---|
| DDD_Base, empreintes | AAM, eGenBrain, eLLM, sondes | Quelles distinctions l'observation conserve-t-elle ? |
| Formalisme de l'observation | NGeGenBrain, sondes, AAM | Comment séparer objet, contexte, mesure, trace et empreinte ? |
| Théorie des cores | CNG/CNC, AdaptiveRBF, expériences | Comment distribuer et coordonner les transformations ? |
| Mise à niveau AdaptiveRBF | HC-RBF et campagnes EX12 | Quels centres sont utiles, stables ou redondants ? |
| Empreintes LLM/cerveau | NGeGenBrain, eLLM | Comment les représentations internes dépendent-elles du contexte ? |
| eGenBrain relationnel | Mémoire relationnelle | Comment fusionner les connaissances sans inventer les liens ? |
| Programmation compositionnelle | FulleGenBrain | Comment composer des programmes sous contrats et contraintes ? |
| Recherche ORDER | models_order | Comment produire et vérifier des certificats ? |

## 11. Autres textes théoriques et rapports : rôle de chaque pièce

Le dossier `theories/` contient aussi des textes qui complètent les fondements précédents. Ils ne doivent pas être réduits à de simples annexes : plusieurs précisent le statut réel des implémentations, critiquent des résultats expérimentaux ou proposent une architecture générale.

### Empreintes et modèles de langage — `source_th_emp_llm_0.tex` et `source_th_emp_llm_v02.tex`

Le premier texte rassemble le socle observationnel des empreintes et une proposition d'architecture informationnelle pour les modèles de langage. Il examine les activations, états latents et poids d'attention comme observables possibles, puis cherche à décrire leur organisation contextuelle. Il distingue les éléments mathématiques du socle, les choix architecturaux et les hypothèses empiriques. La version v02 approfondit les notions de capacité brute, information et dimension effectives, fermeture observationnelle et mesure empirique des seuils ; elle propose une chaîne de traitement qui va du contexte et des sondes à l'empreinte, au quotient observationnel, au maillage, à la mémoire facultative, au transport et à la prédiction. Ce sont des formalismes et propositions d'ingénierie ; leur efficacité doit être mesurée face à des références sur des modèles réels.

### Extensions cerveau et eGenBrain — `th_gen_0.tex`, `th_brain_gen_0.tex`, `th_eGenBrain_0.tex`, `eGenBrain_1.tex`, `formalisme_eGenBrain_v1.tex`

`th_gen_0.tex` étudie l'hypothèse selon laquelle certaines formes de compréhension, mémoire, connaissance et généralisation d'un modèle de langage dépendent d'organisations informationnelles distribuées, plutôt que de concepts logés individuellement dans une unité unique. `th_brain_gen_0.tex` et `th_eGenBrain_0.tex` sont deux fichiers de théorie apparentés et identiques octet pour octet dans l'instantané examiné ; la comparaison de leurs versions en release reste la référence à citer.

`eGenBrain_1.tex` développe le modèle relationnel : brains par source, identités canoniques, occurrences ordonnées, relations, fusion, contexte, provenance et états de recherche. `formalisme_eGenBrain_v1.tex` rend le modèle opérationnel et lié au code livré : observations source, normalisation, tokenisation, brains individuels durables, maillage global, maillage du prompt, alignement, provenance et statuts `FOUND`, `NO_MATCH`, `UNKNOWN`. `FOUND` signifie que le critère structurel implémenté a accepté un candidat ; ce n'est pas une garantie de vérité factuelle ou de pertinence sémantique. Le formalisme précise aussi que la fréquence d'une relation ne prouve pas une causalité et que le pipeline n'implémente pas l'intégralité de DDD_Base.

### Formalismes eLLM — `formalime_model_eLLM_v0.tex` et `formalise_model_eLLM_v1.tex`

Le formalisme v0 porte sur le modèle effectivement implémenté de type Markov interpolé à ordre variable et sur ses sondes de suffixes emboîtées. Le formalisme v1 décrit une autre architecture : sondes multi-résolution apprises sur les états cachés contextuels d'un LLM causal préentraîné, transport appris et correction des logits. Le texte v1 insiste sur la correspondance entre le formalisme DDD_Base et les composants d'ingénierie réellement revendiqués. Ces documents définissent des architectures et des protocoles ; ils ne garantissent pas un gain de qualité sur un checkpoint réel si l'essai correspondant n'a pas été réalisé.

### Programmation compositionnelle — `theorie_programation_compositionnelle_2.tex`

La version 2 développe la sémantique, les effets, l'ASCRC, l'activation réversible, la mémoire vivante, la synthèse et la vérification en lien avec FulleGenBrain_4. Elle traite la composition de fonctions pures, mais aussi de processus avec état, observation, recherche, récupération et transformation contrôlée. Un composant est décrit par son identifiant et sa version, ses types d'entrée/sortie, ses préconditions et postconditions, ses effets, ses ressources, sa sémantique d'exécution, sa provenance et son mécanisme de vérification.

Le texte sépare **ASCR**, mécanisme existant d'eGenBrain v4, et **ASCRC**, régulation réversible proposée. Il explique que mettre des compositions en veille peut réduire le nombre de candidats actifs en mémoire, mais ne réduit pas par magie le nombre total de candidats possibles : recherche paresseuse, filtrage par contrats, partage, déduplication justifiée et reprise restent nécessaires. Il distingue aussi les faits observés dans les artefacts, les définitions, les invariants de conception, les propriétés prouvées sous hypothèses et les effets qui restent à tester.

### Programmation compositionnelle maillée — versions 3 et NG0

`theorie_programation_compositionnelle_3.tex` propose de relier l'algèbre et la sémantique des programmes à un maillage stratifié inspiré d'eGenBrain : identités canoniques, occurrences, faits typés, règles à plusieurs prémisses, opérateurs, provenance, supports d'observation, certificats et activation. Le maillage n'est pas présenté comme un simple graphe de connaissances : il relie plusieurs couches — données, contrôle, état, effets, ressources, contrats, preuves et cycle de vie — sans les confondre. Le texte vise une composition générale de programmes, avec noyau de calcul, représentation intermédiaire, types et effets, frontières de capacités, compilation, gestion des erreurs et reprise.

`theorie_programation_compositionnelle_NG_0.tex` étend cette orientation vers un noyau général, une sémantique, la vérification, l'évolution et des interfaces accessibles. Les propriétés de correction et de sûreté évoquées sont conditionnelles aux hypothèses, règles et sous-langages spécifiés. Elles ne signifient pas qu'une implémentation arbitraire ou tout programme possible est automatiquement sûr ou correct.

### Critique et refondation de la composition — `rapport_et_proposition_th_PC_0.tex`

Ce rapport compare le cadre compositionnel antérieur et le formalisme eGenBrain v4. Il reconnaît les apports des contrats, effets, mémoire, synthèse et activation réversible, ainsi que ceux des identités canoniques, occurrences, faits typés, hyperrègles, opérateurs et certificats. Il conclut qu'aucun des deux cadres, pris isolément ou simplement juxtaposés, ne remplace encore toute la programmation classique. La refondation proposée cherche donc à faire de la composition un mode général de représentation, de définition, d'exécution, de transformation et d'explication des programmes, tout en préservant l'expressivité du langage cible. Le rapport refuse à la fois de réduire la composition à un DSL d'orchestration et de promettre une garantie universelle non démontrée.

### Rapports EX3–EX10 et EX12

`rapport_analyse_ex3_ex10.tex` est une analyse critique des expériences de sondes RBF, correcteurs OOF, coordinateurs et opérateurs numériques. Elle montre que la réduction du nombre de paramètres a souvent été obtenue et documentée, mais que cette compacité ne s'est pas automatiquement traduite en gain de latence ou de coût d'exécution. Les résultats prédictifs dépendent du domaine ; certaines tâches synthétiques ou de classification sont favorables, tandis que d'autres pénalisent fortement les variantes par rapport au MLP. Ce rapport donne le contexte historique qui explique pourquoi il faut mesurer ensemble précision, nombre de paramètres, entraînement, inférence et coûts de coordination.

`EX12_FINAL_SCIENTIFIC_REPORT.tex` approfondit cette question avec une comparaison confirmatoire HC-RBF/MLP à capacité entraînable appariée. Il rapporte des résultats spécifiques favorables sur les frontières, des pertes d'extrapolation et des latences plus élevées. Le rapport sur les centres examine également leur stabilité et leur utilité : peu d'hypothèses de centres passent simultanément les critères statistiques et d'utilité. La portée du résultat est une caractérisation expérimentale nuancée, non une victoire universelle de HC-RBF.

### Bundle `pack_complet_PC_NG.zip`

Ce bundle regroupe notamment la théorie compositionnelle version 2, le formalisme eGenBrain v4, le rapport de critique/refondation et la théorie compositionnelle maillée NG0, avec les PDF correspondants et un README de livrables. Il permet de lire les textes comme un ensemble de travail coordonné : architecture opératoire, base relationnelle, critique des lacunes et proposition de refondation. Il faut conserver les versions et manifestes du bundle lors de toute citation ou reproduction.

## 12. Comment évaluer une affirmation issue de ces théories

Pour chaque proposition, poser au minimum les questions suivantes :

1. Quel objet mathématique est défini et quelles hypothèses sont nécessaires ?
2. Le résultat est-il démontré dans le texte, ou seulement conjecturé ou illustré ?
3. Existe-t-il une implémentation dans la release correspondante ?
4. Quel protocole expérimental a été exécuté, avec quelles données, seeds, baselines et métriques ?
5. Les résultats négatifs et les limites sont-ils rapportés ?
6. Une validation indépendante ou une réplication est-elle disponible ?
7. La conclusion dépasse-t-elle les données ou le formalisme effectivement présentés ?

Une théorie peut être ambitieuse et utile même si son application physique reste spéculative. La rigueur consiste à préserver cette distinction, non à diminuer l'ambition ni à convertir une hypothèse en fait.

## 13. Sources, releases, langue et licence

Les sources complètes de chaque travail sont accessibles dans la release correspondante. Les bundles théoriques peuvent comprendre sources LaTeX, PDF, fragments, rapports, scripts, manifests et sommes de contrôle ; toute citation ou réplication doit identifier la version précise. Les rapports et la documentation de référence sont rédigés en français. La traduction est la responsabilité personnelle du lecteur qui l'entreprend.

La licence générale de l'auteur est le fichier unique `LICENSE` à la racine de la branche `main`. Elle autorise uniquement les usages de recherche non commerciale dans la mesure des droits détenus ou contrôlés par Bensalem Nassim. Tout usage commercial exige une autorisation préalable, expresse, écrite et signée par l'auteur. Les fichiers de licence internes conservés dans les archives le sont pour préserver les octets et les empreintes SHA-256 ; ils ne constituent pas une seconde licence générale de l'auteur pour ses propres éléments. Cette déclaration ne peut annuler les droits valides de tiers ni les autorisations qui ne peuvent légalement être révoquées. Consulter `LICENSE` pour les conditions intégrales.
