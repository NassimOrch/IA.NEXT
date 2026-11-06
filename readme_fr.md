# Travaux de recherche de Bensalem Nassim

## Vue d'ensemble

Ce dépôt rassemble un programme de recherche autour de l'observation, des empreintes informationnelles, des architectures d'intelligence artificielle, de la mémoire relationnelle, de la composition de programmes, de la recherche adaptative et de la vérification. Il ne s'agit pas seulement d'une collection de logiciels : les dossiers réunissent des formalismes mathématiques, des propositions architecturales, des prototypes exécutables, des modèles, des campagnes expérimentales, des rapports d'audit et des outils de reproductibilité.

La vision émergente est celle de systèmes capables de **construire une représentation à partir d'observations**, de la raffiner à plusieurs niveaux, de relier les informations, de faire coopérer des unités spécialisées, de réutiliser une mémoire traçable, de composer des opérations et de vérifier les résultats avant de conclure ou d'agir. Cette synthèse traverse plusieurs familles ; elle ne signifie pas qu'un unique système livré réunit déjà toutes ces capacités de bout en bout.

**Auteur : Bensalem Nassim, avec assistance d'intelligence artificielle.** L'IA a soutenu certaines tâches de rédaction, d'analyse, de programmation ou de mise en forme ; l'attribution scientifique et la responsabilité des travaux présentés reviennent à l'auteur dans les limites des droits qu'il détient.

## Comment lire le dépôt

Le dossier source fourni est un instantané de référence. Il contient des sources, des sous-ensembles, des rapports, des preuves de validation, des historiques et des archives de distribution. La présence d'un sous-ensemble dans cet instantané ne signifie pas que le travail concerné n'a pas de source complète : **la source complète de chaque travail est publiée dans la release correspondante**. Pour reproduire un résultat, il faut utiliser la release ciblée, ses instructions, ses manifestes, ses dépendances et ses empreintes de fichiers.

Les documentations, rapports scientifiques et documents de référence sont rédigés en français. Les lecteurs qui souhaitent les traduire dans une autre langue assument personnellement la responsabilité de leur traduction, de sa fidélité, de sa terminologie et de sa diffusion. Une traduction de lecteur n'est pas automatiquement officielle ni validée par l'auteur. Le README anglais est un guide de présentation ; il ne remplace pas la traduction intégrale des rapports français.

## Architecture IA : les idées centrales

### Observation et empreintes

Un système ne connaît pas nécessairement un objet dans son intégralité. Il dispose d'observations faites selon un contexte, une famille de sondes et une résolution. Une **empreinte informationnelle** est le profil des réponses de l'objet aux sondes retenues. Deux objets qui produisent la même empreinte sont indiscernables pour ce protocole précis ; ajouter des sondes ou augmenter la résolution peut séparer cette classe en distinctions plus fines.

Ce cadre permet d'étudier les invariants, les différences observables, les classes d'équivalence, les trajectoires, les seuils de séparation et les transformations qui ne dépendent que de l'information effectivement conservée. L'empreinte reste relative au protocole : elle n'est pas une photographie absolue de la réalité et ne reconstruit pas ce qui n'a pas été observé.

### Sondes adaptatives, RBF et alternatives aux MLP

Une sonde est une unité de calcul qui réalise une transformation entre une entrée et une sortie. Certaines sondes sont exactes ou symboliques ; d'autres sont apprises. La famille **AdaptiveRBF** transforme l'entrée dans un espace latent, évalue des bases radiales gaussiennes autour de centres appris, puis combine leurs activations. Les textes décrivent notamment un encodage latent de type `tanh`, des activations gaussiennes et une couche de lecture paramétrée.

L'intérêt architectural est de ne pas traiter tout le calcul comme un unique réseau dense. Des sondes spécialisées peuvent être inspectées, composées, organisées et comparées selon leur contribution. Cela ouvre une alternative expérimentale aux MLP, ou un remplacement ciblé de certaines parties d'un réseau. Cela ne signifie pas que les RBF sont systématiquement meilleures : les résultats dépendent des fonctions, des régimes de généralisation, de la capacité et des coûts mesurés.

Le formalisme EX12 introduit **HC-RBF (Hybrid Coverage-Adaptive RBF)** et étudie la sélection progressive des centres, leur contribution prédictive, les résidus, la redondance et leur organisation par empreintes. Le but est d'identifier les centres réellement utiles et stables plutôt que de supposer qu'ils contribuent tous de la même façon.

### Cores : neuronal, logique et physique

Les sources distinguent trois formes de réalisation qui ne doivent pas être confondues :

- **Core neuronal** : groupe de sondes adaptatives qui apprend collectivement une transformation. Il peut être évalué comme candidat pour remplacer un MLP ou une partie d'un réseau.
- **Core logique** : organisation fonctionnelle des sondes sous forme de graphe de dépendances. Il indique quelles opérations doivent être exécutées, leur ordre, les opérations indépendantes qui peuvent être parallélisées et les résultats réutilisables. Il ne suppose pas un matériel particulier.
- **Core physique** : réalisation matérielle potentielle de l'organisation logique, avec unités de calcul, mémoire locale, communications, contrôleur, latence, bande passante, énergie et surface. Une architecture logique parallélisable n'est pas automatiquement plus rapide : le bénéfice matériel doit être mesuré.

Un core est structuré autour d'un ensemble de sondes, d'un graphe de dépendances et d'une mémoire ou d'un état. Plusieurs cores peuvent former une hiérarchie. Un coordinateur gère l'activation, l'attente, le transfert, le stockage, la fusion et la réutilisation des résultats. Le langage de coordination et les contrats d'exécution rendent la coopération explicite.

### CNG et CNC : deux architectures expérimentales distinctes

- **CNG — Cœur neuronal général** : plusieurs sondes coopèrent pour approximer une fonction générale. Les configurations étudiées incluent une sonde unique, des groupes agrégés par moyenne fixe et des compositions apprises, notamment avec composeur linéaire. L'expérience mesure l'approximation, la complémentarité et la généralisation à capacité contrôlée.
- **CNC — Cœur neuronal de calcul** : les sondes sont spécialisées par opération (addition, soustraction, multiplication, division, exponentielle, logarithme, etc.), puis assemblées dans un graphe de calcul. L'étude porte sur l'erreur de chaque opération, sa propagation et l'effet de la composition sur un calcul plus complexe.

CNG et CNC ne sont pas synonymes : le premier étudie la coopération multi-sondes pour apprendre une fonction ; le second, une bibliothèque d'opérateurs neuronaux spécialisés et leur composition en calcul. Dans les protocoles documentés, le graphe peut être fourni à l'avance ; cela ne prouve pas que le CNC choisit déjà seul toute la structure d'opérations.

### Vision IA transversale

Les travaux permettent d'explorer une architecture en couches : observer au moyen de sondes ; construire des empreintes multi-résolution ; relier observations et contextes en graphes ou maillages ; mobiliser des cores neuronaux et des opérations logiques ; coordonner leur activation selon les contrats, ressources et dépendances ; utiliser une mémoire traçable et les contre-exemples ; enfin, vérifier les sorties et s'abstenir lorsque les preuves sont insuffisantes.

Cette vue est une synthèse intellectuelle du corpus, pas la description d'un produit unique déjà intégré de bout en bout.

## Les grandes catégories du dépôt

### `AAM/` — AAM, ROCA-D et acquisition comportementale

AAM étudie une architecture d'agent et de raisonnement fondée sur l'observation contractuelle, les empreintes partielles, la mémoire, la suffisance décisionnelle, la sélection de sondes et la vérification. La lignée O82 formalise **ROCA-D** comme un runtime non-LLM : observation minimale, archivage du brut, construction d'une empreinte, consultation de la mémoire, contrôle de suffisance, puis sélection d'une autre sonde, d'un bundle parallèle ou d'une action de correction. Elle inclut CEGIS (synthèse guidée par contre-exemples), découverte et composition de sondes, décomposition hiérarchique, auto-observation causale, replay et récupération.

Les itérations O94.x approfondissent composition, programmation par contrats, adaptateurs et diagnostics. Les tests établissent des comportements dans des périmètres définis ; ils ne prouvent pas une intelligence générale. AAM explore une voie d'agentification structurée qui ne rend pas le LLM obligatoire au centre de la décision.

### `FulleGenBrain/` — programmation compositionnelle et moteur de composition

FulleGenBrain associe une théorie de programmation compositionnelle à un moteur local. La théorie traite les composants, types, valeurs, effets, contrats, ressources, maillages de programmes et de connaissances, règles de composition, synthèse, vérification, provenance, mémoire vivante, reprise et sécurité d'exécution.

La branche documentaire FulleGenBrain_4 décrit l'architecture et une interface cible ; une spécification d'interface ne doit pas être confondue avec son implémentation intégrale. Le livrable `FulleGenBrain_f4_v0` fournit un noyau opérationnel avec AST JSON fermé, validation statique, interpréteur explicite de 29 opérateurs, mémoire SQLite versionnée, journal d'audit, recherche paresseuse reprenable, boucle CEGIS et contrôleur **ASCRC**. ASCRC règle l'admission opérationnelle, l'allocation des ressources, la veille et le réveil des candidats ; il ne décide pas de leur vérité. Un candidat endormi n'est ni rejeté ni réfuté. Le modèle du monde reste conditionnel à une utilité décisionnelle démontrée.

### `NGeGenBrain/` — observation et reconstruction multi-vues des modèles

NGeGenBrain explore l'observation interne de modèles de langage, l'instrumentation de leurs états, la collecte de plusieurs vues et la possibilité de reconstruire des structures fonctionnelles à partir de ces observations. La lignée comprend versions successives, modèles locaux, interfaces, instrumentation et comparaisons entre modèles sources et modèles étudiants.

La version v3.1 documente le chargement et l'interrogation de checkpoints locaux, l'instrumentation de couches, les observations multi-vues et un modèle étudiant compact. Les résultats ne démontrent pas une reconstruction mécaniste complète d'un LLM réel ; le modèle étudiant reste nettement inférieur aux modèles sources dans les comparaisons rapportées. Cette limite précise ce qui a été observé, ce qui a été reconstruit et ce qui reste à établir.

### `eGenBrain/` — mémoire et maillage relationnel contextuel

eGenBrain étudie une mémoire construite à partir d'observations et de relations. Un brain est construit pour chaque observation source ; les identités canoniques et relations sont fusionnées dans un maillage global. À la requête, un maillage contextuel est dérivé du prompt complet, de ses ancrages, de son ordre et des relations pertinentes. La provenance est conservée et les états `FOUND`, `NO_MATCH` et `UNKNOWN` empêchent de transformer une absence de réponse en réponse inventée.

La théorie couvre tokenisation, identité, occurrences, fusion, redondance utile, directions naturelles, relations causales ou anti-causales lorsqu'elles sont explicitement annotées, construction du contexte et recherche de trajectoires compatibles. La cohérence relationnelle ne vaut pas automatiquement vérité factuelle ou causalité démontrée.

### `eLLM/` — modèles de langage fondés sur des empreintes

Deux voies sont distinctes. **eLLM_v0** est un modèle de langage à n-grammes de Markov d'ordre variable avec interpolation ; ce n'est pas un Transformer. Les suffixes du contexte jouent le rôle de sondes emboîtées et le modèle étudie mémoire et diagnostics d'imagination.

**eLLM_v1** utilise un LLM causal préentraîné et ajoute des sondes apprises à plusieurs résolutions sur ses états cachés contextualisés. Les sondes apprennent des transports et des corrections des logits afin d'influencer la prédiction, pas seulement de visualiser le modèle. Les tests des composants ne suffisent pas à affirmer une amélioration sur un vrai checkpoint : l'audit précise les conditions de disponibilité des poids et les expériences qui restent nécessaires.

### `models_order/` — recherche adaptative, ordre et preuve

La famille ORDER étudie un moteur où les problèmes sont observés progressivement, décomposés récursivement, puis traités par synthèse de candidats et vérification dans un noyau de preuve indépendant. Les observateurs formels, documentaires et web sont séparés : une page apporte du contexte, mais ne devient pas un axiome. Seuls les certificats validés par le noyau entrent en mémoire comme preuves. Une preuve locale peut fermer un sous-problème, déclencher un nouveau test de la racine et guider d'autres branches.

Les versions persistantes ajoutent reprise, budgets temporels, prévention de stagnation par signatures de nouveauté et expansion documentaire. `VERIFIED_COMPLETE`, `TIME_BUDGET_EXPIRED` et `INTERRUPTED` décrivent une exécution ; un temps écoulé n'est pas une preuve d'impossibilité. ORDER80.4.7 étudie aussi le transfert d'artefacts appris d'un enseignant vers des spécialistes et un micro-maître, puis vers un moteur final utilisant les artefacts acquis. Ce n'est pas un LLM général.

### `sondes_experiences/` — expériences AdaptiveRBF, CNG, CNC et HC-RBF

Ce dossier rassemble les expériences sur les sondes adaptatives, depuis les premières campagnes jusqu'à EX9, EX10, EX11 et EX12 : protocoles, scripts, jeux de données, journaux, métriques, ablations, tests de généralisation et audits de provenance.

CNG compare sondes seules, groupes et composeurs ; CNC teste opérateurs neuronaux spécialisés et composition. Les résultats antérieurs varient selon les fonctions et conditions. EX11 conserve un statut exploratoire, avec limites de graines et campagnes non clôturées dans l'instantané.

EX12 spécifie HC-RBF et réalise une campagne confirmatoire contre des MLP appariés en nombre de paramètres entraînables. Sur quatre tâches synthétiques confirmatoires, 11 des 16 contrastes d'interpolation satisfont la non-infériorité ajustée et 7/16 rejettent l'égalité après correction statistique ; aucune variante ne gagne partout. Les régimes de frontière favorisent souvent HC-RBF, mais l'extrapolation est fortement défavorable sur trois tâches sur quatre. Sur le matériel mesuré, le pipeline HC-RBF est plus lent et l'entraînement coûte davantage que le MLP. L'analyse P6 détecte des cas de spécialisation stable et utile, mais seulement 7 hypothèses de rôle sur 1 024 passent simultanément les deux critères dans le cas documenté. Ces résultats fournissent des pistes d'amélioration sans valider une supériorité générale.

### `theories/` — fondements scientifiques et formalismes

Ce dossier contient théorie des empreintes, formalisme de l'observation, théorie des cores, formalismes CNG/CNC, architecture AdaptiveRBF/HC-RBF, théorie du maillage eGenBrain, théories des empreintes pour LLM, formalismes eLLM, programmation compositionnelle et rapports critiques de refondation. Les sources `.tex` doivent être lues en respectant le statut de chaque énoncé : définition, hypothèse, proposition, théorème, conjecture, résultat expérimental ou piste de recherche.

À noter : `th_brain_gen_0.tex` et `th_eGenBrain_0.tex` sont identiques octet par octet dans l'instantané ; il s'agit de deux copies, pas de confirmations indépendantes.

### `readme_vHS/` — vulgarisation

Ce dossier contient des lettres et textes destinés aux lecteurs plus jeunes. Les README `readme_vHS_*.md` poursuivent cet objectif avec des mots simples et des métaphores, sans effacer les distinctions entre hypothèse, expérience et résultat.

## Théories principales : explication et spéculation

### Théorie des empreintes — DDD_Base, ordre 5

La théorie définit un domaine d'objets, des contextes, une famille de sondes et un protocole d'observation. L'empreinte est le profil des réponses. Elle induit indiscernabilité, fibres et quotient ; une famille de sondes plus riche peut raffiner les classes. L'ordre 5 traite aussi seuils de séparation, ultramétrique dérivée sous hypothèses, fermeture observationnelle, factorisation des transformations, trajectoires, identité, généralisation, contraintes, transformations certifiées et limites d'une observation incomplète.

**Spéculation :** si la réalité était en partie décrivable par des niveaux d'observation emboîtés, les empreintes pourraient exprimer ce qu'un observateur distingue à une résolution donnée et ce qui reste confondu. En physique quantique, on pourrait explorer une représentation des classes observationnelles dépendantes du dispositif. DDD_Base contient un exemple géométrique appelé « chat de Naszimger », une reconstruction de structure de type Schrödinger et une analogie interne à la double fente. On pourrait interpréter une observation grossière comme une classe contenant plusieurs possibilités, puis un raffinement comme une séparation de ces possibilités. **Mais le texte précise qu'il ne reconstruit pas le formalisme quantique de Schrödinger et ne déduit aucune conclusion physique de l'analogie de la double fente.** Il ne dérive ni la règle de Born, ni les amplitudes complexes, ni l'équation de Schrödinger, ni l'intrication ou la décohérence. Le chat de Naszimger est une classe observationnelle du modèle, pas un état physique établi du chat de Schrödinger. Il faudrait définir une correspondance avec le formalisme quantique, établir des prédictions quantitatives et les soumettre à des tests indépendants avant toute prétention explicative.

Hors quantique, cette idée pourrait être étudiée en vision par ordinateur, fusion de capteurs, robotique, diagnostic, sciences du vivant, linguistique et interprétabilité des réseaux : plusieurs instruments donnent des vues partielles, et la représentation doit indiquer quelles distinctions sont établies ou invisibles.

### Formalisme de l'observation

Le bundle `observation_formalisme_full_0_bundle.zip` rassemble un texte principal et trois sources articulées, 58 chapitres tracés, README, audit, CSV de traçabilité, manifestes, sommes de contrôle et scripts. L'audit recense 8 parties, 51 chapitres, 94 définitions, 3 hypothèses explicites et 81 énoncés de type théorème/proposition/lemme/corollaire avec environnements de preuve. La compilation et l'existence d'environnements de preuve ne remplacent pas une revue mathématique indépendante ou une vérification par assistant de preuve.

Le formalisme distingue l'objet, le contexte, le protocole, l'observation, l'enregistrement et l'empreinte ; les invariants sous transformations déclarées ; les composantes variables, résidus et traces temporelles ; l'incertitude, l'identifiabilité, les problèmes inverses et les interventions. Il rappelle qu'une empreinte ne reconstitue pas les composantes perdues, qu'un problème inverse peut avoir plusieurs mécanismes compatibles, qu'une intervention isolée ne démontre pas une causalité complète et qu'un signal échantillonné ne révèle pas nécessairement ce qui se passe entre les échantillons.

**Spéculation :** en quantique, le formalisme pourrait permettre de décrire les dispositifs comme des contextes et les mesures comme des sondes. Pour la double fente, il faudrait montrer que les règles proposées prédisent quantitativement l'apparition ou la disparition des franges. Pour le chat de Schrödinger, il aide à distinguer description, dispositif, enregistrement et empreinte, mais ne résout pas à lui seul le problème de la mesure. En biologie, médecine, contrôle, télédétection, astronomie ou chimie, il pourrait clarifier l'identifiabilité des mécanismes et les limites des données.

### Théorie des cores, CNG/CNC et AdaptiveRBF

`th_sondes_core_0.tex` et `th_sondes_core_1.tex` formalisent les sondes, cores, graphes de calcul, composition hiérarchique, mémoire temporaire, coordinateur et cores neuronal/logique/physique. Les textes de test établissent les protocoles CNG/CNC. `arch_up_formalisme_0.tex` étudie l'organisation adaptative des centres AdaptiveRBF.

**Spéculation :** des cores coordonnés pourraient aider en robotique, simulation scientifique, systèmes temps réel, processeurs spécialisés et IA multimodale. Une sonde pourrait approximer un opérateur coûteux, un core logique gérer le graphe et un core physique réaliser son exécution. Ce n'est ni une théorie des constituants de la matière, ni la preuve d'une vitesse supérieure aux architectures conventionnelles. Les mesures de précision, latence, énergie et coût de coordination sont nécessaires.

### Empreintes, LLM, maillages relationnels et eGenBrain

`th_gen_0.tex` et les sources sur les empreintes de LLM avancent l'hypothèse que la signification et certaines formes de généralisation pourraient être distribuées dans des structures relationnelles formées par des contextes et des empreintes internes. Une unité neuronale peut participer à plusieurs structures ; la poly-sémanticité est une piste interprétative, pas une cause démontrée par coactivation seule. `eGenBrain_1.tex` formalise le maillage des brains, la fusion, le contexte, la recherche et la provenance.

**Spéculation :** une IA pourrait organiser des connaissances comme structures relationnelles multi-résolution plutôt que comme activations isolées. On pourrait comparer cette idée aux mémoires associatives, à la formation de concepts et à la généralisation en sciences cognitives, linguistique et neurosciences. Aucune équivalence avec le cerveau humain ou la conscience n'est établie par les sources.

### Programmation compositionnelle et contraintes

Les théories de programmation compositionnelle définissent composants typés, contrats, effets, budgets, maillages de programmes/connaissances, règles d'inférence, transformations, mémoire, synthèse et vérification. Elles visent à rendre visibles la correction, les ressources, les permissions et la provenance. Le rapport critique de programmation compositionnelle analyse les formalismes antérieurs et propose une refondation.

**Spéculation :** ces outils pourraient soutenir des systèmes autonomes auditables, des chaînes de calcul scientifiques reproductibles, des décisions certifiables et des robots respectant des contraintes. Des composants de simulation physique pourraient porter unités, invariants et domaines de validité. Un programme bien typé n'est toutefois pas automatiquement un modèle vrai du monde.

### eLLM et génération de langage

Les formalismes eLLM explorent un modèle Markovien d'ordre variable dans v0 et l'ajout de sondes multi-résolution à un LLM préentraîné dans v1.

**Spéculation :** les empreintes contextuelles pourraient améliorer le contrôle de génération, la mémoire structurée ou la détection de contextes où le modèle distingue mal deux cas. Cela doit être mesuré sur de vrais checkpoints et comparé à des références ; aucune conscience, compréhension humaine ou supériorité générale n'en découle.

### ORDER et recherche de preuve

ORDER développe une recherche progressive : observer, synthétiser, apprendre de l'échec, décomposer, obtenir des preuves locales, les vérifier et retester la racine. Les sources documentaires et web restent distinctes des preuves formelles.

**Spéculation :** cette architecture pourrait aider en mathématiques, vérification de logiciels, recherche scientifique et planification expérimentale. En physique, elle pourrait examiner les conséquences formelles d'un modèle et vérifier les calculs, sans décider seule si le modèle décrit l'univers. L'absence de certificat ne prouve pas l'impossibilité d'un résultat.

## Discipline scientifique : ce qui est établi et ce qui reste ouvert

Il faut distinguer :

- **défini** : les objets, termes, règles et l'architecture sont spécifiés ;
- **implémenté** : le code correspondant existe dans la release ;
- **testé** : un scénario a été exécuté avec mesures et journaux ;
- **confirmé dans le périmètre** : le résultat tient au protocole et aux répétitions annoncés ;
- **hypothétique ou spéculatif** : une proposition à formaliser et à falsifier.

Un test logiciel vérifie un scénario ; une expérience évalue une hypothèse dans un protocole ; une preuve mathématique vaut sous ses hypothèses ; une analogie inspire une question mais ne démontre rien à elle seule. Les rapports conservent résultats défavorables, cas limites et lacunes de provenance : c'est indispensable pour comprendre la portée réelle des architectures.

## Releases, langues et sources

Chaque travail possède sa source complète dans la release correspondante. Les README propres aux versions indiquent prérequis, commandes, dépendances, données et limites. Les documentations et rapports de référence sont en français ; la traduction vers une autre langue est la responsabilité personnelle de chaque lecteur qui l'entreprend.

## Auteur et licence

**Bensalem Nassim, avec assistance d'IA.** La licence générale unique de l'auteur est le fichier `LICENSE` à la racine de la branche `main`. Elle limite les droits détenus par l'auteur à la recherche non commerciale ; tout usage commercial exige un accord préalable, exprès, écrit et signé par Bensalem Nassim. Les notices internes aux ZIP sont conservées pour préserver les octets distribués et les SHA-256, mais ne constituent pas une seconde licence générale de l'auteur pour les éléments dont il détient les droits. Cette règle n'annule pas les droits de tiers ni les droits antérieurs irrévocables. Voir `LICENSE` pour le texte complet.

## Carte rapide

| Dossier | Sujet | Contribution |
|---|---|---|
| `AAM/` | Agent non-LLM, observation, mémoire | ROCA-D, CEGIS, sondes, décision sous contrat |
| `FulleGenBrain/` | Programmation compositionnelle | AST typé, 29 opérateurs, synthèse, ASCRC |
| `NGeGenBrain/` | Observation de modèles | Instrumentation multi-vues, reconstruction expérimentale |
| `eGenBrain/` | Mémoire relationnelle | Maillage contextuel, provenance, abstention |
| `eLLM/` | Langage et empreintes | Markov variable, sondes apprises sur LLM causal |
| `models_order/` | Recherche et preuve | Décomposition, synthèse, noyau de preuve |
| `sondes_experiences/` | Expériences neuronales | AdaptiveRBF, HC-RBF, CNG, CNC |
| `theories/` | Fondements | Empreintes, observation, cores, LLM, composition |
| `readme_vHS/` | Vulgarisation | Lettres pédagogiques |
