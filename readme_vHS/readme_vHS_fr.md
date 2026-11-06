# Une invitation à découvrir les travaux de Bensalem Nassim

*Présentation pour les lycéennes et les lycéens*

**Auteur des travaux : Bensalem Nassim, avec assistance d'intelligence artificielle.** L'IA a servi d'aide pour certaines tâches ; elle ne remplace ni l'auteur ni le travail de vérification scientifique.

## 1. Une grande idée : construire une intelligence avec plusieurs outils

Imagine que tu arrives dans une ville inconnue. Tu n'en connais pas tous les habitants, toutes les rues ni toutes les règles. Tu peux regarder une carte, écouter les gens, observer les feux, marcher dans les rues et comparer ce que tu as appris. Chaque moyen te donne une partie de l'information. Aucun ne te montre toute la ville d'un seul coup.

Les travaux présentés ici partent souvent d'une idée semblable : **un système intelligent doit apprendre à observer, organiser ce qu'il observe, relier les informations, choisir quoi examiner ensuite et vérifier ses conclusions.** Il ne suffit pas toujours d'avoir un gros réseau de neurones. On peut aussi construire une architecture composée de plusieurs outils qui coopèrent.

La vision générale ressemble à une équipe : certaines unités apprennent, d'autres organisent les étapes, d'autres gardent la mémoire, et d'autres vérifient le résultat. Les sources explorent ces idées à travers plusieurs projets, théories et expériences.

## 2. Les idées importantes, avec des images simples

### Les empreintes : reconnaître grâce à des indices

Imagine que tu doives reconnaître un animal sans le voir directement. Tu peux poser plusieurs questions : a-t-il des plumes ? Combien de pattes ? Est-ce qu'il vole ? Chaque réponse est un indice. L'ensemble des réponses forme une sorte d'empreinte.

Dans la théorie des empreintes, un objet est étudié grâce à des questions appelées **sondes**. Deux objets peuvent avoir la même empreinte si les questions posées ne permettent pas de les distinguer. Ajouter une question plus précise peut révéler une différence.

Cela apprend une règle importante : on ne doit pas prétendre connaître une information que nos observations ne permettent pas de connaître.

### Les sondes : de petits outils spécialisés

Une sonde est comme un petit outil qui reçoit une information et produit une réponse. Certaines sondes suivent une règle exacte ; d'autres apprennent à partir d'exemples. Plusieurs sondes peuvent se répartir un travail.

### Les réseaux MLP et les réseaux RBF

Un MLP est une famille connue de réseaux de neurones. On peut le comparer à une grande équipe de calcul qui transforme progressivement les informations.

Les RBF fonctionnent autrement : elles utilisent des centres et réagissent davantage à certaines zones de l'espace des entrées. On peut les imaginer comme des points de repère qui reconnaissent les situations proches de leur position.

Les travaux AdaptiveRBF et HC-RBF étudient comment organiser ces centres, mesurer leur utilité, retirer ceux qui sont redondants et combiner les réponses. Le but est d'explorer d'autres architectures que le MLP ou de remplacer certaines parties d'un réseau. Les expériences ne montrent pas que les RBF gagnent toujours : tout dépend du problème et de la manière de mesurer.

### Trois cores : trois métiers différents

Le mot **core** signifie ici un noyau organisé de calcul. Les sources distinguent trois rôles :

- Le **core neuronal** apprend des transformations grâce à des sondes adaptatives. C'est la partie qui apprend à répondre à des situations.
- Le **core logique** organise le travail : quelle opération vient avant l'autre ? Quelles tâches peuvent être faites en même temps ? Quel résultat peut être réutilisé ?
- Le **core physique** concerne la machine réelle qui exécute le travail : processeur, mémoire, communications, énergie et temps de calcul.

Compare cela à une cuisine : les recettes et l'ordre des étapes sont le côté logique ; les cuisiniers et leurs compétences représentent le côté qui réalise les opérations ; la cuisine, les fours, les ustensiles et l'électricité représentent le côté physique. Une bonne recette ne garantit pas que le repas sera prêt vite si le four est lent ou si tout le monde attend le même ustensile.

### CNG et CNC : deux façons de faire coopérer des sondes

Le **CNG** (cœur neuronal général) rassemble plusieurs sondes pour apprendre une fonction. C'est comme demander à plusieurs spécialistes de proposer une réponse, puis de combiner leurs avis.

Le **CNC** (cœur neuronal de calcul) utilise des sondes spécialisées dans des opérations : addition, multiplication, division, exponentielle, logarithme et autres. Elles sont assemblées dans un graphe de calcul, comme des étapes reliées dans une recette.

Le CNG cherche surtout à apprendre une fonction avec plusieurs sondes. Le CNC étudie plutôt comment des opérateurs spécialisés peuvent réaliser un calcul composé. Dans certaines expériences, le plan des opérations est fourni à l'avance : cela ne veut pas encore dire que le système sait toujours inventer seul le meilleur plan.

## 3. Les projets : une équipe de recherches

### `AAM/` — un agent qui observe avant de décider

AAM étudie un agent qui observe une situation, consulte sa mémoire, se demande si les informations suffisent, puis choisit une autre question ou une action. Il peut apprendre de ses erreurs grâce aux contre-exemples. L'idée est de construire un agent organisé sans rendre un grand modèle de langage obligatoire au centre de chaque décision.

### `FulleGenBrain/` — fabriquer des programmes comme des constructions en briques

FulleGenBrain étudie comment construire un programme avec des blocs qui ont chacun un rôle, des entrées, des sorties et des règles. Comme avec des briques de construction, on veut vérifier que les pièces s'emboîtent correctement. Le moteur contient notamment un langage de programme sous forme d'arbre, un vérificateur et un interpréteur de 29 opérateurs dans la version concernée. Il explore aussi la recherche de programmes et la reprise d'une recherche interrompue.

### `NGeGenBrain/` — observer comment des modèles de langage fonctionnent

NGeGenBrain étudie des moyens d'observer plusieurs parties d'un modèle de langage et de combiner certaines informations. C'est un peu comme essayer de comprendre le fonctionnement d'une machine en regardant plusieurs cadrans et en faisant des essais contrôlés.

Une expérience documentée a tenté de recomposer un petit modèle à partir d'informations extraites d'autres modèles. Les résultats publiés dans ce dossier restent limités : la recomposition testée n'a pas dépassé les modèles sources sur la mesure rapportée. L'intérêt est d'étudier la méthode et de savoir précisément où elle fonctionne ou non.

### `eGenBrain/` — une mémoire faite de relations

eGenBrain organise les informations comme un réseau de liens : un mot, un contexte, une idée ou un fait peut être relié à d'autres éléments. Il garde la provenance des informations et distingue trois situations utiles : une réponse trouvée, aucune correspondance, ou une information inconnue. Il vaut mieux dire « je ne sais pas » que d'inventer un lien.

### `eLLM/` — expérimenter d'autres façons de compléter un modèle de langage

eLLM étudie les empreintes et les sondes dans le traitement du langage. Une version explore les modèles de type Markov avec plusieurs tailles de contexte ; une autre étudie l'ajout de sondes apprises aux représentations internes d'un grand modèle de langage. Ces deux approches ne sont pas la même chose et les tests disponibles ne prouvent pas un progrès général sur tous les modèles.

### `models_order/` — chercher une solution et vérifier une preuve

ORDER organise une recherche en plusieurs étapes : découper un grand problème, essayer des pistes, apprendre de ce qui échoue et vérifier les preuves avec un noyau de contrôle. Trouver un texte qui affirme quelque chose ne suffit pas : il faut vérifier le raisonnement. Si le temps manque, cela ne prouve pas que le problème est impossible.

### `sondes_experiences/` — le laboratoire des réseaux et des sondes

Ce dossier contient les expériences sur AdaptiveRBF, HC-RBF, CNG, CNC et leurs comparaisons avec des MLP. On y trouve du code, des protocoles, des mesures et des rapports. Certaines expériences favorisent les nouvelles architectures pour certaines tâches ; d'autres favorisent les MLP. Une étude plus contrôlée montre des avantages HC-RBF dans certains cas de frontière, mais aussi des difficultés en extrapolation et des coûts de calcul plus élevés. C'est exactement ce que doit faire une recherche sérieuse : montrer les réussites et les limites.

### `theories/` — les idées écrites en langage mathématique

Ce dossier rassemble les théories des empreintes et de l'observation, les cores, CNG/CNC, les réseaux RBF adaptatifs, les relations dans eGenBrain, les modèles de langage et la programmation par composition. Ces textes essaient de donner des définitions et des règles précises aux idées étudiées par les logiciels et les expériences.

## 4. Et si ces idées décrivaient aussi certains aspects du monde réel ?

Cette partie est une **spéculation**, c'est-à-dire une piste pour réfléchir et imaginer des expériences. Ce n'est pas une découverte prouvée en physique.

### Les empreintes et la double fente

Dans une expérience à deux fentes, on peut étudier ce qui se passe lorsqu'on cherche à savoir par quelle fente une particule est passée. On pourrait se demander si la théorie des empreintes peut représenter la différence entre un dispositif qui ne distingue pas le chemin et un dispositif qui le mesure. L'idée serait de décrire les informations accessibles dans chaque situation.

Mais le texte DDD_Base dit clairement que sa comparaison avec la double fente est une analogie de structure et qu'elle ne donne pas de conclusion physique sur l'expérience quantique. Pour aller plus loin, il faudrait retrouver les résultats mathématiques de la mécanique quantique et faire des prédictions précises qui pourraient être testées.

### Le chat de Schrödinger et le chat de Naszimger

Le chat de Schrödinger est une expérience de pensée qui montre une difficulté liée à la mesure en physique quantique. DDD_Base présente un exemple appelé « chat de Naszimger ». Ce chat est une classe d'observation dans le modèle, pas un vrai état quantique ni une solution démontrée au problème de Schrödinger.

On peut imaginer que la théorie aide à distinguer ce que contient un système, ce que mesure un appareil et ce que l'observateur sait. C'est une question intéressante, mais elle ne résout pas encore le problème de la mesure.

### D'autres domaines et d'autres théories : pistes spéculatives

Les empreintes pourraient être utiles pour comprendre comment plusieurs caméras observent un même objet, comment des médecins distinguent plusieurs maladies à partir de signes incomplets, comment un robot combine ses capteurs ou comment un modèle de langage utilise le contexte.

Pour les autres familles, on peut imaginer plusieurs questions de recherche :

- **Les cores, le CNG et le CNC :** pourrait-on construire des machines ou des robots où les tâches d'apprentissage, d'organisation logique et d'exécution matérielle coopèrent mieux ? Il faudrait comparer leurs résultats, leur vitesse et leur consommation à des systèmes classiques.
- **AAM :** un agent pourrait-il apprendre à poser de meilleures questions avant de décider, comme un enquêteur qui vérifie ses indices au lieu de deviner ? Cela demanderait de tester sa fiabilité dans des situations nouvelles.
- **FulleGenBrain et la composition :** pourrait-on construire des programmes complexes avec des blocs dont les règles et les limites sont connues, comme on construit un pont avec des pièces contrôlées ? Il faudrait vérifier les programmes et leurs hypothèses.
- **NGeGenBrain et eLLM :** pourrait-on mieux comprendre les modèles de langage en observant plusieurs représentations et en testant de nouveaux moyens de les recomposer ? Il faudrait mesurer si la méthode améliore réellement les réponses sur des modèles réels.
- **eGenBrain :** une mémoire de relations pourrait-elle aider un système à retrouver l'origine d'une information et à reconnaître ce qu'il ne sait pas ? Il faudrait comparer ses réponses à des bases de connaissances de référence.
- **ORDER :** une recherche par petites étapes et preuves vérifiées pourrait-elle aider à résoudre des problèmes de mathématiques ou à contrôler des logiciels ? Il faudrait vérifier chaque preuve et ne pas confondre manque de temps et impossibilité.

Les cores pourraient donc inspirer des machines qui répartissent mieux leurs calculs, et la composition pourrait aider à fabriquer des programmes plus faciles à vérifier. Ce sont des pistes de recherche, pas des résultats garantis.

## 5. Comment reconnaître une vraie avancée scientifique ?

Il faut séparer quatre choses :

1. **Une idée** : une proposition intéressante.
2. **Une théorie** : des définitions et des règles qui expliquent précisément l'idée.
3. **Une implémentation** : un programme qui réalise une partie de cette idée.
4. **Une expérience** : un test qui mesure ce qui se passe dans des conditions précises.

Une expérience positive ne prouve pas que la méthode fonctionne partout. Une expérience négative n'est pas inutile : elle indique où il faut améliorer ou limiter la méthode. Une analogie avec la physique n'est pas une preuve que la théorie décrit la nature.

## 6. Comment lire et apprendre avec ces travaux

Tu peux commencer par les README, puis regarder les rapports expérimentaux, les petites démonstrations et enfin les textes théoriques. Essaie de comprendre une question à la fois : quelle information est observée ? Quelle sonde la mesure ? Comment l'information est-elle mémorisée ? Quelle expérience vérifie la proposition ?

Les sources complètes de chaque travail sont publiées dans les releases correspondantes. L'archive de présentation peut montrer un instantané ou des éléments d'explication ; elle n'est pas le remplacement des releases complètes.

Les documentations et rapports de référence sont rédigés en français. Si tu les traduis, la traduction et sa qualité relèvent de ta responsabilité personnelle. Les versions anglaises des README sont des guides de lecture, pas la traduction officielle de chaque rapport.

## 7. Auteur et licence

Les travaux sont attribués à **Bensalem Nassim, avec assistance d'IA**. La licence générale unique se trouve dans le fichier `LICENSE` à la racine de la branche `main`. Elle autorise uniquement la recherche non commerciale sur les éléments dont l'auteur détient les droits. Un usage commercial nécessite une autorisation préalable, expresse, écrite et signée par Bensalem Nassim.

Les anciens fichiers de licence présents à l'intérieur de certaines archives ZIP ont été conservés afin de ne pas modifier les octets et les empreintes SHA-256 des fichiers distribués. Ils ne constituent pas une deuxième licence générale émise par l'auteur pour ses propres éléments. Cette règle ne peut pas supprimer les droits ou licences valides de tiers. Lis le fichier `LICENSE` avant toute utilisation.

## Pour finir

La grande leçon de ces travaux est simple : une intelligence artificielle peut être étudiée comme une équipe d'outils qui observent, apprennent, organisent, se souviennent, calculent et vérifient. Le défi est de comprendre comment ces outils peuvent coopérer sans inventer ce qu'ils ne savent pas. C'est une question ouverte, exigeante et passionnante — et chacun peut commencer à l'explorer en apprenant les mathématiques, l'informatique et la méthode scientifique.
