# Les théories expliquées simplement — guide spécial pour les lycéens

**Travaux de Bensalem Nassim, avec assistance d'IA.** Ce guide présente les idées des textes théoriques avec des mots simples. Les documents de référence et rapports sont rédigés en français ; toute traduction faite par un lecteur relève de sa responsabilité personnelle.

## Avant de commencer : à quoi sert une théorie ?

Une théorie est comme un plan détaillé. Elle dit quels objets on étudie, quels mots on utilise, quelles règles relient ces objets et sous quelles conditions ces règles sont vraies. Un programme est ensuite une façon de mettre certaines idées en pratique. Une expérience vérifie ce qui se passe dans un cadre précis.

Il faut donc éviter de confondre une belle idée avec un résultat prouvé. Même un document qui contient beaucoup de formules, de définitions ou de démonstrations doit pouvoir être relu et vérifié par d'autres spécialistes.

## 1. La théorie des empreintes : connaître grâce aux observations

### Une histoire pour comprendre

Imagine deux boîtes fermées. Tu veux savoir si elles contiennent le même objet, mais tu n'as pas le droit de les ouvrir. Tu peux les peser, les secouer doucement, écouter le bruit et mesurer leur température. Tu obtiens une liste de réponses.

Si toutes les réponses sont identiques, tu ne peux pas encore être certain que les objets sont identiques. Tu sais seulement que tes tests n'ont pas réussi à les différencier. Un nouveau test pourrait faire apparaître une différence.

C'est l'idée de base de la **théorie des empreintes** dans `DDD_Base_theorie_des_empreintes_complete_order_5.tex`.

### Les mots importants

- Un **objet** est ce que l'on cherche à étudier.
- Un **contexte** décrit les conditions dans lesquelles on l'observe.
- Une **sonde** est une question ou une mesure que l'on applique à l'objet.
- Une **empreinte** est l'ensemble organisé des réponses obtenues.
- Une **classe d'équivalence** rassemble les objets que les sondes choisies ne savent pas distinguer.

L'empreinte n'est donc pas l'objet lui-même. C'est plutôt une fiche d'identité construite avec les renseignements disponibles. Si la fiche est trop courte, plusieurs objets différents peuvent avoir la même fiche.

### Pourquoi cette idée est-elle puissante ?

Elle oblige un système à respecter les limites de ce qu'il sait. Si deux objets ont la même empreinte, un programme qui n'utilise que cette empreinte ne devrait pas inventer une différence entre eux. Pour les distinguer, il faut obtenir une information supplémentaire.

Le texte étudie aussi les empreintes à plusieurs niveaux de précision. On peut commencer avec quelques questions, puis ajouter des questions plus fines. C'est comme une carte : une carte du pays montre les grandes régions ; une carte de la ville montre les rues ; un plan détaillé montre les portes et les escaliers.

### La spéculation sur le monde réel

On peut imaginer que certaines situations du monde réel se comprennent mieux en séparant ce qui est observé de ce qui ne l'est pas. Cela pourrait être utile avec des caméras, des radars, des instruments médicaux, des robots ou des modèles d'intelligence artificielle. Plusieurs instruments ne voient pas nécessairement les mêmes détails ; les empreintes pourraient aider à comparer leurs informations.

### Le lien possible avec la double fente

En mécanique quantique, l'expérience des deux fentes montre des motifs d'interférence dans certaines conditions. Si l'on cherche à obtenir l'information du chemin suivi par une particule, le résultat expérimental peut changer.

Une question spéculative serait : peut-on décrire les deux situations à l'aide de deux contextes d'observation différents, et représenter les informations disponibles dans chacun par des empreintes ? Peut-on retrouver les nombres mesurés dans l'expérience à partir de règles mathématiques précises ?

Il faut être très clair : **le texte DDD_Base présente la double fente comme une analogie de structure, et indique qu'il n'en déduit aucune conclusion physique.** Il ne démontre pas la mécanique quantique et ne calcule pas les franges d'interférence. Pour devenir une véritable théorie physique, il faudrait retrouver les équations et les résultats quantiques, produire des prédictions chiffrées, puis les tester.

### Le chat de Schrödinger et le chat de Naszimger

Le chat de Schrödinger est une expérience de pensée imaginée pour discuter d'une difficulté de la mesure quantique. Dans le texte sur les empreintes, un exemple porte le nom de « chat de Naszimger ». Il sert à illustrer une classe d'observation : plusieurs possibilités peuvent rester confondues parce que les observations ne les séparent pas.

Ce n'est pas un vrai chat dans un état quantique décrit par une expérience. Ce n'est pas non plus une solution prouvée au problème du chat de Schrödinger. L'idée spéculative est de distinguer trois choses : ce qui se passe dans le système, ce que l'appareil peut mesurer et ce que l'observateur sait. Pour expliquer la physique quantique, il faudrait démontrer un lien précis avec les états, les mesures, les probabilités et les expériences de cette théorie.

## 2. Le formalisme de l'observation : bien distinguer ce que l'on voit

Le bundle `observation_formalisme_full_0_bundle.zip` approfondit la question de l'observation. Il contient un texte principal, des textes complémentaires, des chapitres, des PDF, des fichiers de suivi et des contrôles d'intégrité.

Il insiste sur des mots qui se ressemblent mais qui ne signifient pas la même chose :

1. **L'objet** : la chose étudiée.
2. **Le contexte** : les conditions de l'étude.
3. **La sonde ou le protocole** : la manière de poser une question ou de faire une mesure.
4. **L'observation** : le résultat obtenu.
5. **L'enregistrement** : la trace que l'on garde.
6. **L'empreinte** : le résumé organisé que l'on construit à partir de certaines observations.

Imagine une caméra de surveillance. La scène réelle est l'objet ; la lumière et l'angle de la caméra font partie du contexte ; la caméra est l'instrument ; les images sont les observations ; le fichier vidéo est l'enregistrement ; un résumé décrivant les mouvements est une empreinte. Chaque étape peut perdre des détails.

Le formalisme étudie également les changements dans le temps, les observations complémentaires, les mesures qui aident à distinguer plusieurs explications et les situations où plusieurs causes peuvent produire des observations semblables. Il rappelle qu'un petit nombre de mesures ne permet pas toujours de reconstruire tout ce qui s'est passé entre elles.

**Spéculation quantique :** on pourrait décrire un laboratoire comme un contexte, un appareil comme un ensemble de sondes et les résultats comme des enregistrements. Pour la double fente, il faudrait calculer précisément les résultats selon que l'information du chemin est disponible ou non. Pour le chat de Schrödinger, il faudrait distinguer le système, l'appareil, l'environnement, la trace et l'observateur. Ce vocabulaire peut aider à poser les questions, mais le formalisme ne résout pas actuellement le problème de la mesure.

**Autres domaines possibles :** médecine, astronomie, chimie, contrôle de machines, robotique et observation de la Terre. Dans ces domaines, la question serait de savoir ce que les instruments permettent vraiment de conclure et quelles explications restent possibles.

## 3. Les cores : apprendre, organiser et exécuter

Les textes `th_sondes_core_0.tex` et `th_sondes_core_1.tex` décrivent les sondes et trois sortes de cores.

- Le **core neuronal** apprend à transformer des informations. Il peut utiliser des sondes adaptatives.
- Le **core logique** organise les calculs en étapes et indique quelles étapes dépendent les unes des autres.
- Le **core physique** concerne la machine qui réalise les calculs : puces, mémoire, connexions, énergie et vitesse.

Reprenons l'exemple de la cuisine. Un chef peut connaître une recette ; la recette indique l'ordre des actions ; les fours, les plaques et les ustensiles permettent de réaliser ces actions. Si la cuisine est trop petite, si le four est lent ou si deux personnes attendent le même outil, la recette ne suffit pas à faire gagner du temps.

Les sources décrivent aussi des graphes de calcul et un coordinateur qui peut activer, attendre, transmettre, réutiliser, stocker ou fusionner des résultats.

**Spéculation :** une intelligence artificielle pourrait répartir ses tâches entre plusieurs cores : un noyau apprend, un autre organise les opérations et un troisième exécute le tout sur le matériel. Cela pourrait inspirer des robots, des accélérateurs de calcul ou des systèmes scientifiques. Il faudrait mesurer si cette organisation est réellement plus précise, plus rapide ou moins coûteuse. Les textes ne prouvent pas que le cerveau humain est construit exactement ainsi.

## 4. CNG et CNC : deux familles d'expériences

Le CNG rassemble des sondes qui apprennent ensemble une fonction. On peut comparer cette méthode à une équipe de personnes qui proposent chacune une estimation, puis combinent leurs réponses.

Le CNC utilise des sondes conçues pour des opérations précises : addition, multiplication, division, exponentielle ou logarithme. On les relie pour former un calcul plus long. Cela ressemble à une chaîne de petites machines, chacune chargée d'une étape.

Les expériences comparent ces architectures à des MLP, à des sondes RBF directes ou à des opérations exactes. Les résultats ne sont pas tous identiques : certaines tâches favorisent certaines variantes, d'autres favorisent le MLP. Dans les expériences décrites, le plan du calcul peut être donné à l'avance ; il ne faut donc pas croire que le CNC sait déjà choisir tout seul le plan optimal dans n'importe quelle situation.

**Spéculation :** si ces architectures deviennent plus fiables, un CNG pourrait réunir plusieurs façons d'estimer une situation, tandis qu'un CNC pourrait transformer un calcul compliqué en petites opérations spécialisées. Cela pourrait être étudié dans la robotique, la simulation, le traitement de signaux ou les calculs scientifiques. Il faudrait vérifier que les erreurs ne s'accumulent pas et que la coordination ne coûte pas plus cher que le calcul gagné.

## 5. AdaptiveRBF et HC-RBF : organiser les centres

Un réseau RBF utilise des centres qui réagissent à des entrées proches de leur position. On peut imaginer des balises sur une carte : chacune reconnaît mieux une région particulière.

Les travaux AdaptiveRBF et HC-RBF étudient comment choisir les centres, savoir lesquels apportent une information nouvelle, reconnaître les centres redondants, retirer certains centres et réentraîner le réseau. Ils utilisent aussi l'idée d'empreinte pour décrire la position, l'activation et la contribution d'un centre.

Les rapports EX12 montrent des avantages dans certains cas, notamment certains tests près des frontières des fonctions. Mais ils montrent aussi des pertes en extrapolation pour plusieurs tâches et des coûts de temps supérieurs au MLP. Cela ne rend pas l'architecture sans intérêt : cela indique plus précisément les situations où elle mérite d'être étudiée et celles où elle doit être améliorée.

**Spéculation :** si les centres sont organisés de manière stable, ils pourraient aider à expliquer quelles régions d'un problème sont reconnues par le réseau. Cette idée pourrait être utile pour des modèles scientifiques ou des systèmes embarqués. Il faudrait confirmer cette stabilité sur de nouvelles données et de nouveaux contextes.

## 6. Empreintes dans les modèles de langage et mémoire relationnelle

Certains textes étudient l'idée qu'un modèle de langage peut répartir une information entre plusieurs unités et relations internes. Cela pose une question : le sens d'une phrase est-il toujours localisé dans un seul neurone, ou dépend-il d'un ensemble d'activations et du contexte ?

C'est une piste d'interprétation. Une mesure d'activation ou une expérience de sonde ne suffit pas à expliquer entièrement le mécanisme intérieur d'un grand modèle.

`eGenBrain` explore une mémoire sous forme de réseau de relations. Il relie des mots, des contextes et des informations, mais doit garder la trace de leur origine. Lorsqu'il ne sait pas si un lien existe, il doit pouvoir répondre « inconnu » plutôt que fabriquer une réponse.

**Spéculation :** une mémoire de ce type pourrait soutenir un assistant de recherche ou aider à organiser des connaissances en sciences. En neurosciences, on pourrait comparer certaines idées à des modèles de mémoire associative, mais cela ne prouve pas que le logiciel reproduit le cerveau humain ou possède une conscience.

## 7. Langage, composition de programmes et recherche de preuves

### eLLM

eLLM explore deux chemins : une version utilise un modèle de type Markov avec plusieurs longueurs de contexte ; une autre étudie des sondes apprises à partir des représentations internes d'un LLM préentraîné. L'objectif est de tester si les informations de contexte peuvent être mieux organisées ou utilisées. Les tests de composants ne prouvent pas à eux seuls une amélioration générale de la qualité du langage.

### Programmation compositionnelle et FulleGenBrain

Les théories de composition expliquent comment assembler des blocs de programme avec des règles, des types, des contrats et des limites de ressources. C'est comme construire un objet avec des pièces dont on connaît la forme et les fonctions. Le moteur FulleGenBrain met en pratique une partie de ces idées.

Une bonne vérification peut montrer qu'un programme respecte les règles écrites. Elle ne prouve pas automatiquement que les hypothèses de départ décrivent correctement le monde réel.

### ORDER

ORDER étudie comment découper une question complexe, rechercher des solutions, apprendre des erreurs et vérifier les preuves. Un résultat doit passer par le noyau de vérification. Ne pas trouver de preuve avant la fin du temps disponible ne signifie pas qu'il n'existe aucune preuve.

**Spéculation :** ces méthodes pourraient aider à vérifier des programmes, organiser des expériences scientifiques et contrôler des calculs en mathématiques ou en physique. Elles vérifient les raisonnements à partir des règles données ; elles ne remplacent pas les observations nécessaires pour savoir si une théorie décrit vraiment la nature.

## 8. D'autres théories : construire des programmes et comprendre les relations

### Programmation compositionnelle version 2

La version 2 explique comment construire des programmes à partir de composants qui ont chacun un contrat. Un contrat est comme une fiche qui indique ce qu'un bloc accepte, ce qu'il doit produire, les ressources qu'il peut utiliser et les erreurs possibles. La théorie parle aussi de mémoire, de recherche, de récupération après une interruption et de vérification.

Elle distingue ASCR, un mécanisme d'eGenBrain v4, et ASCRC, une nouvelle proposition de régulation réversible. Mettre une composition en veille peut économiser de la mémoire active, mais ne fait pas disparaître toutes les possibilités de programme. Il faut aussi filtrer les candidats, éviter les répétitions justifiées et organiser la recherche.

### Programmation compositionnelle maillée : versions 3 et NG0

Les versions 3 et NG0 proposent de relier les règles de composition des programmes à un maillage inspiré d'eGenBrain. Ce maillage relie les données, les étapes de contrôle, l'état du programme, les effets, les ressources, les contrats, les preuves et l'historique. Ce n'est pas seulement une carte de mots : il cherche à représenter comment un programme est construit, fonctionne, change et peut être vérifié.

L'objectif est ambitieux : faire de la composition une manière générale de construire des programmes, et pas seulement un petit langage servant à enchaîner quelques tâches. Les garanties de correction présentées restent liées aux hypothèses et aux sous-langages décrits dans les textes.

### Le rapport critique de refondation

`rapport_et_proposition_th_PC_0.tex` compare les travaux de programmation compositionnelle avec le modèle relationnel eGenBrain v4. Il explique ce que chaque approche apporte et ce qui manque encore pour remplacer toute la programmation classique. Il propose une refondation plus générale, mais refuse de prétendre qu'une théorie a déjà prouvé qu'elle pouvait tout programmer de façon automatiquement sûre.

### Les rapports des expériences

`rapport_analyse_ex3_ex10.tex` reprend les expériences plus anciennes sur les sondes RBF, les corrections, les coordinateurs et les calculs spécialisés. Il montre qu'avoir moins de paramètres ne suffit pas à être plus rapide : les calculs supplémentaires et les échanges entre sondes peuvent coûter du temps.

`EX12_FINAL_SCIENTIFIC_REPORT.tex` examine HC-RBF face à des MLP de capacité comparable. Il observe des avantages dans certains tests de frontière, mais aussi des difficultés en extrapolation et une latence plus élevée. Il faut retenir le résultat complet, pas seulement les meilleurs chiffres.

### Les théories des empreintes pour les modèles de langage

`source_th_emp_llm_0.tex` et sa version v02 appliquent les idées d'empreintes aux représentations internes des modèles de langage. Elles proposent d'étudier comment les contextes, les activations et les sondes peuvent former des structures d'information. `th_gen_0.tex` va plus loin en posant l'hypothèse que certaines formes de compréhension et de généralisation peuvent être distribuées dans plusieurs relations, au lieu d'être rangées dans un seul neurone. C'est une hypothèse scientifique à tester, pas une découverte confirmée sur tous les modèles.

### Les deux formalismes eLLM

La version eLLM v0 décrit un modèle de type Markov avec plusieurs longueurs de mémoire. La version v1 étudie des sondes apprises à partir des représentations d'un LLM causal préentraîné et des corrections apportées à ses sorties. Ce sont deux architectures différentes. Il faut mesurer séparément leurs résultats sur de vrais modèles.

### Les archives de travail

`pack_complet_PC_NG.zip` rassemble plusieurs textes de programmation compositionnelle, leur critique et une proposition de refondation, avec des PDF et un README. Le dossier théorique comprend aussi des textes et formalismes eGenBrain qui relient les données, les mots, les occurrences, les relations et les preuves. Ces archives aident à suivre l'évolution des idées et les liens entre elles.

## 9. Comment toutes ces théories se rejoignent-elles ?

On peut dessiner la vision globale comme une boucle :

1. Le système observe une situation avec des sondes.
2. Il construit une empreinte pour résumer ce qu'il sait.
3. Il relie cette information à sa mémoire et à son contexte.
4. Il choisit des opérations et les répartit entre des cores.
5. Il compose une solution ou une action.
6. Il vérifie le résultat et cherche de nouvelles observations si nécessaire.

La boucle peut recommencer lorsque le système découvre une erreur ou une information manquante. Cette image rassemble plusieurs idées des sources ; elle ne signifie pas qu'un système unique réalise déjà parfaitement toutes les étapes.

## 10. Comment lire ces travaux avec un esprit scientifique

Pour chaque idée, demande-toi :

- Est-ce une proposition, une définition ou un résultat démontré ?
- Existe-t-il un programme qui la met en pratique ?
- Quelle expérience a été réalisée ?
- Quels résultats ont été positifs et lesquels ont été négatifs ?
- Est-ce que la conclusion est plus large que ce que l'expérience permet de dire ?

Une vraie recherche ne cache pas les échecs. Elle les décrit, explique leur portée et propose des tests plus précis.

Les sources complètes de chaque travail sont publiées dans les releases correspondantes. Les documents de référence et rapports sont en français ; chaque lecteur qui traduit un document assume personnellement la qualité de sa traduction.

## 11. Auteur et licence

Les travaux sont attribués à **Bensalem Nassim, avec assistance d'IA**. La licence générale unique est `LICENSE`, à la racine de la branche `main`. Elle autorise seulement l'usage de recherche non commerciale sur les éléments dont l'auteur détient les droits. Toute utilisation commerciale exige une autorisation préalable, écrite et signée par Bensalem Nassim.

Les anciennes notices de licence gardées dans certains ZIP n'ont pas été supprimées afin de préserver les octets et les SHA-256 des fichiers. Elles ne forment pas une deuxième licence générale de l'auteur pour ses propres éléments. Les droits valides de tiers restent séparés et ne peuvent pas être supprimés par cette déclaration.

## La grande question à retenir

Et si l'intelligence ne consistait pas seulement à calculer une réponse, mais aussi à savoir comment on l'a obtenue, quelles informations la soutiennent, quelles questions restent ouvertes et comment vérifier le résultat ? C'est l'une des grandes questions qui relient ces travaux. Elle reste ouverte à la recherche, à la critique et à de nouvelles expériences.
