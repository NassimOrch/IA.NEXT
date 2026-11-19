

===== SOURCE: eGenBrain/Dmodel_eGenBrain_v4/README.md =====
# eGenBrain v4 — runtime autonome

Version du moteur : **4.0.0**. eGenBrain v4 préserve la base MG héritée, ajoute un maillage inférentiel typé et certifié, et conserve le retrieval/reconstruction v3 comme fallback traçable.

## Fichiers de livraison et installation

Il faut les deux archives `Dmodel_eGenBrain_v4.zip` et `Dmodel_eGenBrain_v4_part2.zip`, ainsi que `reassemble_packages_eGenBrain_v4.py`. Python 3.11+ est recommandé. Le chemin normal du moteur utilise la bibliothèque standard Python et SQLite; certains formats d'import facultatifs (par exemple Parquet) peuvent demander un module additionnel.

Placez les deux ZIP et le script externe dans un même dossier puis exécutez :

```bash
python reassemble_packages_eGenBrain_v4.py --archive-dir . --destination ./eGenBrain_v4_installed
```

L'installateur contrôle les CRC et chemins des ZIP, la taille et SHA-256 des deux fragments, reconstitue atomiquement `model/eGenBrain_v4.sqlite3`, vérifie l'empreinte finale et exécute `PRAGMA integrity_check` et `PRAGMA foreign_key_check`. Il refuse d'écraser une destination non vide.

## Lancement

Depuis le dossier installé :

```bash
python -m egenbrain serve --model model/eGenBrain_v4.sqlite3
python -m egenbrain chat --model model/eGenBrain_v4.sqlite3 --message "Tim buys 3 dozen eggs. Eggs cost $.50 each. How much did he pay for eggs?"
python -m egenbrain mesh4 --help
```

Le serveur local est destiné à l'usage local; l'interface v4 expose les opérations sur faits, règles, inférence et requêtes et conserve les traces. La base maillée v4 est un sidecar distinct de la base MG historique.

## Démarrage volontairement vierge

Pour démarrer l'interface sans charger le MG livré, donnez un chemin SQLite inexistant :

```bash
python -m egenbrain serve --model model/eGenBrain_v4_fresh.sqlite3 --empty-start
```

Cette option refuse le remplacement d'une base existante et crée un schéma vide sans réponses synthétiques. Il faut importer des données et déclarer les primitives/règles souhaitées. Elle ne promet pas de capacité d'apprentissage ou de généralisation non mesurée.

## Interprétation scientifique

Les tests de livraison prouvent l'intégrité et l'exécution des chemins testés. La campagne d'ablation est contenue dans l'archive d'audit, séparée du runtime. Le score 8/8 de composition vaut pour les huit micro-cas positifs finis de la campagne; il ne démontre ni induction autonome d'opérateurs ni intelligence générale. Le facteur `dozen=12` est une primitive fournie; les opérateurs arithmétiques sont des opérateurs typés génériques.


===== SOURCE: eGenBrain/Amodel_eGenBrain_v4/README_AUDIT.md =====
# Amodel eGenBrain v4 — audit du modèle

Cette archive regroupe le code source auditable, les tests, les sorties brutes, les résultats de scoring post-hoc, les traces, les journaux de correction et les formalismes. Les échecs/interruption de harnais et les résultats négatifs ont été conservés; une exécution PASS ne signifie pas nécessairement que le résultat du modèle est exact.

## Résultats principaux vérifiés

- Suite complète: 136/136 tests sur le code source, `ResourceWarning` élevé au rang d'erreur.
- Campagne aveugle: 66 inférences brutes (11 cas × 6 modes), persistées avant scoring, avec 8 cas positifs demandant une composition et 3 cas où une abstention était attendue. Le mode complet a 8/8 dérivations positives et 3/3 abstentions attendues dans ces micro-mondes finis.
- Intégration réelle au MG historique: problème des œufs -> `18`, certificat `PASS`, sans fallback v3. Le hash du MG historique est inchangé.
- Installation à partir des ZIP runtime finaux: taille et SHA-256 de la base reconstituée conformes, SQLite integrity check `ok`, zéro violation FK. Le test runtime à froid est aussi conservé.

Les réponses de référence sont dans `experiments/references_sealed.json`, utilisé uniquement par le scorer après les inférences; il ne fait pas partie du paquet Dmodel runtime. Les empreintes finales des archives sont consignées dans `manifest_livraison_eGenBrain_v4.json` et l'archive de suivi.

Le score de 8/8 ne vaut que pour les 8 cas positifs construits. Les opérateurs arithmétiques sont des primitives déterministes génériques; le facteur `dozen=12` est une primitive explicitement fournie. L'induction autonome des opérateurs/règles et l'intelligence générale restent des questions ouvertes.


===== SOURCE: eGenBrain/Dmodel_eGenBrain_v1/formalisme_eGenBrain_v1.tex =====
\documentclass[11pt,a4paper,openany]{book}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[french]{babel}
\usepackage{lmodern}
\usepackage[a4paper,margin=2.3cm]{geometry}
\usepackage{amsmath,amssymb,mathtools}
\usepackage{booktabs,longtable,tabularx,array}
\usepackage{hyperref}
\usepackage{enumitem}
\setlength{\parindent}{0pt}\setlength{\parskip}{5pt}\sloppy
\title{Formalisation opérationnelle d'eGenBrain\_v1\\\large Conforme au code et au modèle livré}
\author{Dossier de formalisation et de traçabilité}
\date{22 octobre 2026}
\begin{document}\maketitle\tableofcontents
\chapter*{Statut et règle de lecture}
Ce document formalise le système effectivement présent dans le dépôt de livraison. Il distingue (i) une définition mathématique opérationnelle, (ii) une propriété testée, (iii) un comportement empirique observé et (iv) une hypothèse restant ouverte. Une fonction de code ou un test fini n'est pas une preuve de vérité factuelle. Le registre \texttt{preuves\_eGenBrain\_v1.json} associe les sections de la source \texttt{eGenBrain\_1.tex} aux références de code et aux résultats disponibles. Les éléments de la théorie DDD qui ne sont pas codés restent expressément marqués comme non revendiqués.

\chapter{Objets, données et conventions}
\section{Observations source et paires canoniques}
Une observation source est notée $o_i=(s_i,t_i,q_i,a_i,m_i)$, où $s_i$ est le fichier et l'identifiant de provenance, $t_i$ la tâche, $q_i$ le prompt, $a_i$ la réponse observée et $m_i$ les métadonnées. Le corpus brut est $\mathcal{D}_{raw}=\{o_i\}_{i=1}^{N}$. À l'entraînement, les observations de même signature canonique peuvent être regroupées en un exemple $e_j$, mais leur multiplicité $\mu_j$ et leurs références source demeurent conservées. Le modèle livré contient $N=134\,759$ observations/br ains et $112\,992$ paires canoniques; par construction, $\sum_j\mu_j=N$.

La signature de regroupement est définie par le code avec tâche, prompt et réponse normalisés; le groupe de split, lui, dépend de la tâche et du prompt normalisé, et non de la réponse :
\[
\sigma(t,q,a)=\operatorname{SHA256}(t\Vert 0\Vert NFC(q)'\Vert 0\Vert NFC(a)'),\qquad
\gamma(t,q)=\operatorname{SHA256}(t\Vert 0\Vert NFKC(q)_{casefold,espaces}).
\]
Ces expressions décrivent les séparateurs NUL et les normalisations effectivement utilisées; elles ne sont pas des identifiants sémantiques universels.

\section{Tokenisation, identité et occurrences}
Pour une chaîne $x$, le tokenizeur renvoie $\tau(x)=(u_1,\ldots,u_m)$ avec position, surface, forme canonique, offsets $[b_i,e_i)$ et indicateur lexical. La forme canonique des occurrences est la normalisation Unicode NFKC suivie de \texttt{casefold}. Les runs de lettres/chiffres/underscore sont lexicaux; les autres caractères non blancs apparaissent comme occurrences de ponctuation/symbole. On conserve les offsets originaux et les positions répétées. L'identité lexicale canonique n'assimile pas synonymes, paraphrases ni concepts.

\section{Brain individuel durable}
Chaque observation garde un brain durable $B_i=(id_i,task_i,Q_i,A_i,O_i,R_i,P_i,H_i)$ où $Q_i$ et $A_i$ sont les textes prompt/réponse, $O_i$ les occurrences ordonnées, $R_i$ les relations locales, $P_i$ la provenance et $H_i$ une empreinte calculée. Les occurrences restent distinctes même quand plusieurs occurrences partagent le même token canonique. Le brain est une structure de données, pas un agent autonome.

\chapter{Construction hors ligne : fusion et maillage global}
\section{Identités fusionnées et provenance conservée}
On définit les tokens canoniques observés $V=\{c(u):u\in O_i, i\in train\}$. Des occurrences différentes peuvent pointer vers la même identité lexicale $c$, sans perdre leur position dans leur brain. Une relation globale est une arête dirigée $(u,v,\rho,w,S,\kappa)$ contenant type, support/poids, références de support et statut relationnel $\kappa$. Le graphe global opérationnel est $G=(V,E)$. Les arêtes d'ordre proviennent des séquences dans les brains du split \texttt{train}; les splits de validation/test ne doivent pas alimenter ce maillage.

La multiplicité brute d'une paire aide à préserver les occurrences et le support, mais la fréquence ne prouve pas une causalité. Le modèle actuellement livré contient 125\,453 identités de tokens, 1\,811\,636 lignes d'indexation occurrence-token et 756\,568 arêtes globales. Le contrôle d'intégrité atteste les compteurs et les références de support, pas la véracité du corpus.

\section{Relations causales et anti-causales}
Le statut relationnel appartient à $\{unknown,causal\_natural,anticausal\}$. Une relation inconnue ne devient pas naturelle par cooccurrence ni par fréquence. Le moteur applique les annotations explicites, avec contraintes dures ou pénalités souples selon le modèle de règle configuré. Une violation anti-causale dure rend le candidat inadmissible; une règle souple intervient comme pénalité, non comme interdiction absolue. Le corpus livré contient zéro annotation causale et zéro annotation anti-causale. Le mécanisme est testé sur annotations explicites synthétiques, mais son bénéfice empirique sur un corpus causalement annoté reste non évalué.

\chapter{Recherche en ligne et maillage contextuel}
\section{Brain du prompt et alignement ordonné}
Pour le prompt $q$, le moteur construit un contexte local $C_q$ à partir des occurrences réelles du prompt. Les occurrences du prompt demeurent distinctes; le code représente leurs relations contextuelles dirigées pour toute paire distincte. Ce maillage contextuel est conceptuellement séparé du graphe global d'apprentissage. Les répétitions sont des occurrences distinctes et une ancre requise doit être alignée sur une occurrence/position compatible.

\section{Alignement et orientation}
Une correspondance admissible doit respecter l'ordre des ancres et les règles d'alignement implémentées. L'existence individuelle des tokens dans $G$ ne suffit pas : une trajectoire ordonnée admissible est nécessaire. Les relations intermédiaires sont permises dans certaines configurations du modèle; les contraintes anti-causales dures peuvent bloquer un candidat. Le code peut retourner $NO\_MATCH$ si la trajectoire structurelle est absente, et $UNKNOWN$ quand la preuve lexicale exploitable est insuffisante. La distinction entre échec de recherche et preuve que la réponse n'existe pas doit être maintenue.

\section{Réponse, provenance et états}
La recherche renvoie un résultat structuré $(status,task,answer,trace)$ et expose les références source quand un candidat est trouvé. Les états opérationnels comprennent \texttt{FOUND}, \texttt{NO\_MATCH} et \texttt{UNKNOWN}. \texttt{FOUND} signifie que le critère structurel codé a accepté un candidat; il ne veut pas dire que la réponse est factuellement ou sémantiquement juste. Les résultats du test web montrent d'ailleurs qu'une réponse \texttt{FOUND} peut être sémantiquement inadéquate sur un prompt personnalisé.

\chapter{Empreintes opérationnelles imbriquées}
\section{Sondes finies}
Pour une requête et un candidat, le profil observé est composé de quatre couches déclarées :
\begin{enumerate}[label=\arabic*.]
\item \textbf{identité lexicale}: fréquences des tokens de requête et fréquences de présence dans le candidat;
\item \textbf{alignement ordonné}: positions de requête, token, position cible et offsets; complétude de l'alignement;
\item \textbf{écosystème relationnel}: arêtes d'ordre/support, hits causaux/anti-causaux, violations et règles d'intermédiaires;
\item \textbf{provenance}: hashes des références sources et métadonnées (ou déclaration que la sonde de provenance est désactivée).
\end{enumerate}
Chaque couche plus fine incorpore la charge utile de la couche précédente. Si $F_{k+1}(x)=F_{k+1}(y)$ pour l'égalité de charge utile avant hash, alors l'égalité des sous-objets antérieurs est préservée; des tests vérifient cette monotonie sur les objets opérationnels utilisés. Le hash SHA-256 est une empreinte de sérialisation JSON canonique, non une distance sémantique. Cette construction ne représente pas toute la théorie DDD d'ordre 5 : notamment, le pipeline ne met pas en oeuvre un système universel de seuils, d'ultramétrique, d'imagination, de promotion certifiée ou de transfert.

\chapter{Invariants et frontières épistémiques}
\section{Invariants vérifiables}
Les invariants vérifiés sur le modèle gelé sont : (1) intégrité SQLite; (2) aucune violation de clé étrangère; (3) aucune fuite de groupe de prompt entre splits; (4) aucun index de token de document provenant de validation/test; (5) hashes d'observations source concordants lors de l'audit P3; (6) la somme des multiplicités vaut 134\,759; (7) l'évaluation laisse inchangé le SHA-256 du modèle. Ces points concernent l'intégrité et la procédure, non la qualité globale des réponses.

\section{Propriétés non démontrées}
Aucune de ces vérifications ne prouve que (a) toutes les réponses sont exactes, (b) l'architecture génère une compréhension sémantique générale, (c) toute requête peut être résolue, (d) les relations causales sont fiables, ou (e) les mécanismes théoriques hors code existent implicitement. Les résultats empiriques doivent être interprétés selon la tâche, l'effectif et la latence observée.

\chapter{Algorithme de construction et algorithme de recherche}
\section{Construction hors ligne}
\begin{enumerate}
\item découvrir les sources permises et calculer leurs hashes;
\item lire chaque format, convertir les lignes valides en observations normalisées et enregistrer les erreurs de parsing;
\item calculer les signatures canoniques et conserver les références/multiplicités;
\item former les groupes de split par tâche et prompt normalisé avec la graine déterministe;
\item écrire les exemples canoniques et le brain durable pour chacune des observations;
\item indexer les occurrences du split train et agréger les arêtes globales ordonnées;
\item écrire les annotations explicites sans promotion implicite de \texttt{unknown};
\item vérifier les relations, les contraintes, les clés étrangères et l'intégrité SQLite;
\item publier atomiquement la nouvelle base et produire le manifeste SHA-256.
\end{enumerate}

\section{Recherche en ligne}
\subsection{Contrat de routage par tâche}
Soit $h$ l'indication explicite fournie par l'appelant. Si $h\in\{\texttt{chat},\texttt{math\_qa},\texttt{sms\_classification}\}$, la tâche $t$ utilisée par la recherche est $t=h$; une valeur explicite non autorisée est rejetée. Si aucune indication n'est fournie, le code applique uniquement les règles de repli définies dans \texttt{route\_task}. Cette règle évite de substituer silencieusement un autre index au sous-graphe demandé. Elle est vérifiée par \texttt{test\_explicit\_math\_task\_hint\_routes\_to\_math\_index} et \texttt{logs/math\_task\_route\_regression.log}. Le routage est un prérequis d'une mesure valide, mais ne garantit pas l'exactitude sémantique de la réponse.

\begin{enumerate}
\item déterminer la tâche depuis l'indication explicite ou le routeur opérationnel;
\item tokeniser le prompt en conservant les offsets et les répétitions;
\item construire le contexte local de la requête;
\item retrouver des candidats via l'index lexical et le maillage global;
\item vérifier la trajectoire et l'alignement ordonné; tester les contraintes explicites;
\item éliminer les candidats inadmissibles et ordonner ceux qui restent par le score codé;
\item produire \texttt{FOUND} et la provenance lorsqu'un candidat est admis, sinon \texttt{NO\_MATCH} ou \texttt{UNKNOWN};
\item enregistrer la trace d'observation. L'inférence est testée sans mutation de la base.
\end{enumerate}

\chapter{Interfaces et commandes}
Le serveur local expose chat, statistiques, exemples train, inventaire/inspection de datasets, upload, entraînement asynchrone vers une nouvelle base, activation explicite du modèle, évaluation, interrogation de job et console applicative. La console applique une liste blanche de commandes (aide, stats, vérification, chat, inspection, entraînement, évaluation); elle n'exécute pas un shell arbitraire. CLI : \texttt{python -m egenbrain --help}; commandes principales : \texttt{train}, \texttt{serve}, \texttt{chat}, \texttt{evaluate}, \texttt{inspect-dataset}. L'accès web par défaut est local sur \texttt{127.0.0.1:8765}.

\chapter{Référence d'implémentation}
\begin{longtable}{p{.25\linewidth}p{.37\linewidth}p{.26\linewidth}}
\toprule Concept & Point d'entrée code & Test/log décisif\\\midrule
Tokenisation et offsets & \texttt{egenbrain/core.py:canonicalize, tokenize} & \texttt{tests/test\_core.py}\\
Brain durable & \texttt{egenbrain/core.py:build\_local\_brain}; \texttt{egenbrain/train.py:\_insert\_model} & \texttt{logs/p3\_structural\_audit.json}\\
Données / Parquet & \texttt{egenbrain/datasets.py:read\_rows}; \texttt{egenbrain/parquet\_flat.py} & \texttt{logs/parquet\_reader\_probe\_v1.log}\\
Maillage / recherche & \texttt{egenbrain/core.py:EGenBrain.search} & \texttt{tests/test\_core.py}\\
Empreintes & \texttt{egenbrain/observations.py:candidate\_observation\_profile} & \texttt{tests/test\_observations.py}\\
Évaluation & \texttt{egenbrain/evaluate.py:run\_evaluation} & \texttt{logs/p5\_test\_evaluation\_extended.json}\\
API / studio & \texttt{egenbrain/server.py} et \texttt{web/} & \texttt{logs/p4\_live\_http\_smoke.json}\\
Intégrité / empaquetage & \texttt{scripts/verify\_integrity.py}, \texttt{scripts/reassemble\_model.py} & \texttt{logs/p6\_prepackage\_integrity.json}\\
\bottomrule
\end{longtable}
Les lignes exactes et hashes des sources sont dans le JSON de preuves, qui recense chaque rubrique de la source eGenBrain_1 et chaque rubrique de DDD ordre 5.

\chapter{Routage corrigé et résultats empiriques mis à jour}
Le routage explicite est vérifié par une régression ciblée. Les évaluations corrigées (\texttt{logs/p5\_test\_routed\_v2.json}, \texttt{logs/p5\_validation\_routed\_v2.json}) conservent le hash de la base avant/après et vérifient intégrité et non-fuite. Les résultats sont : math 57/100 FOUND au test, 47/100 en validation, mais 0/100 exact-match math dans chaque split; SMS 5/10 et 7/10 exacts; chat 0/3 et 0/1 FOUND. FOUND représente l'admissibilité structurelle, non une preuve de réponse exacte. Les anciennes métriques math sont conservées comme historiques invalidées par l'erreur de routage.

\chapter{Routage corrigé et résultats empiriques mis à jour}
Le routage explicite est vérifié par une régression ciblée. Les évaluations corrigées (\texttt{logs/p5\_test\_routed\_v2.json}, \texttt{logs/p5\_validation\_routed\_v2.json}) conservent le hash de la base avant/après et vérifient intégrité et non-fuite. Les résultats sont : math 57/100 FOUND au test, 47/100 en validation, mais 0/100 exact-match math dans chaque split; SMS 5/10 et 7/10 exacts; chat 0/3 et 0/1 FOUND. FOUND représente l'admissibilité structurelle, non une preuve de réponse exacte. Les anciennes métriques math sont conservées comme historiques invalidées par l'erreur de routage.

\chapter{Routage corrigé et résultats empiriques mis à jour}
Le routage explicite est vérifié par une régression ciblée. Les évaluations corrigées (\texttt{logs/p5\_test\_routed\_v2.json}, \texttt{logs/p5\_validation\_routed\_v2.json}) conservent le hash de la base avant/après et vérifient intégrité et non-fuite. Les résultats sont : math 57/100 FOUND au test, 47/100 en validation, mais 0/100 exact-match math dans chaque split; SMS 5/10 et 7/10 exacts; chat 0/3 et 0/1 FOUND. FOUND représente l'admissibilité structurelle, non une preuve de réponse exacte. Les anciennes métriques math sont conservées comme historiques invalidées par l'erreur de routage.

\chapter{Statut formel du modèle livré}
Le système implémente un pipeline déterministe de brains persistants, fusion lexicale, maillage d'ordre global, contexte local, alignement, contraintes explicites, traçabilité, interfaces et mesures reproductibles. Les résultats initiaux sur les petits échantillons sont conservés mais leurs métriques math sont invalidées par un défaut de routage désormais corrigé. Après correction, le test donne 57/100 réponses math FOUND et la validation 47/100; l'exact-response-match math est 0/100 dans les deux splits et le F1-token moyen est 0,126596/0,106234. Le chat reste à 0/3 FOUND au test et 0/1 en validation; SMS obtient 5/10 labels exacts au test et 7/10 en validation. Les annotations causales/anti-causales d'entraînement sont absentes. Ainsi, le statut est : implémentation exécutée et structurellement auditée; qualité empirique mixte, avec accès au bon sous-graphe réparé mais justesse des réponses math non démontrée; couverture DDD partielle plutôt qu'intégrale.
\end{document}


===== SOURCE: NGeGenBrain/Amodel_NGeGenBrain_v2/rapport_audit_NGeGenBrain_v2.md =====
# Rapport d’audit — NGeGenBrain_v2

- Date : `2026-10-27`.
- Version : `2.0.0.dev0` (version de développement instrumentable).
- Exécution officielle : `20261027T153351Z`.
- Espace d'expérience actif : `benchmarks/results/20261027_official/workspace_20261027T153351Z`.
- Origine : sources/tests V1 conservés dans `legacy_NGeGenBrain_v1/`; archives de référence conservées dans `references/`.

## 1. Portée de l'audit

Audit de la structure V1, conservation des capacités de l'ancienne suite, formalisme V2, code, tests, CLI, interface Web locale, laboratoire synthétique, journaux chaînés, intégrité JSON/ZIP, rapport LaTeX et préparation de livraison. Aucune architecture V1 n'a été remplacée silencieusement. La cartographie formalisme→modules→tests→preuves se trouve dans `NGeGenBrain_v2_mise_en_oeuvre.json`, `chemins_NGeGenBrain_v2.json` et `preuves_NGeGenBrain_v2.json`.

## 2. Vérifications logicielles exécutées

- Compilation Python (`compileall`) : PASS.
- Compilation du formalisme LaTeX avec `pdflatex -halt-on-error` dans un répertoire temporaire : PASS.
- Tests V2 : **52/52 passés**, journal `audit/test_runs/v2_unit_integration_tests_final.log` (exécution indépendante enregistrée).
- Tests de régression V1 : **65/65 passés**, journal `audit/test_runs/v1_preserved_regression_tests_final.log`.
- CLI : initialisation, benchmark aveugle, audit des registres, composition, découverte numérique, planification, contre-exemples, balayage causal, ladder synthétique : PASS.
- JSON du projet : **83/83 fichiers JSON parsés sans erreur** au contrôle source de cette version; la liste détaillée est dans `audit/validation_receipt.json`.
- Les trois archives V1 de référence embarquées ont passé `zipfile.testzip()` (**3/3 CRC valides**).
- Registres de l'expérience officielle : tous les hash-chains sont valides.

Reçu détaillé : `audit/validation_receipt.json`; reçu des contrôles par composants : `audit/component_validation_receipt.json`; résumé : `audit/validation_summary.md`. Les 17 contrôles composants documentés ont passé individuellement. La génération du package et le contrôle clean-room des archives restent des étapes séparées. Les tests V1/V2 ont été exécutés séparément avec sorties brutes rattachées par hash. Une tentative d'exécution globale dépassait le budget temporel du superviseur d'outil; cet arrêt n'est pas codé ni interprété comme un résultat de test.

- Un défaut de résolution d’imports entre `reconstruction.py` et le paquet `reconstruction/` a été détecté par la vérification CLI clean-room, corrigé en déplaçant l’implémentation publique vers `reconstruction/engine.py` et en exportant explicitement l’API du paquet. Deux tests de non-régression couvrent désormais cet import ; la CLI a été relancée après correction.

## 3. Évidence expérimentale principale

- Benchmark : `SYNTH-PARITY-4`.
- Lignes discovery : `12` ; holdout : `4`.
- Exactitude holdout : `1.0` ; exactitude de la table finie interrogée : `1.0`.
- Échelle d'instrumentation : `8` architectures synthétiques, dont mini-Transformer encodeur et mini-Transformer causal génératif. Cette échelle teste forward/capture/intervention/génération, elle ne prouve pas la reconstruction de chaque modèle.
- Intervention locale `zero` sur `xor_layers.0.positive`, entrée `[1,0,0,0]` : delta L2 `2.0`.
- Balayage : `8` entrées, `2` effets non nuls, `6` effets nuls.
- Contrôle négatif positif : candidat incomplet détecté comme erroné sur `8` lignes, avec `4` contre-exemples.

## 4. Réserve concernant un véritable LLM

Aucun modèle pré-entraîné Hugging Face n'a été chargé : `transformers` et un checkpoint local n'étaient pas disponibles, et l'installation de dépendances distantes n'a pas été possible dans cet environnement. L'adapter local Hugging Face est livré, mais non validé ici sur un checkpoint réel. **L'analyse et la recomposition d'un LLM externe sont donc NON EXÉCUTÉES**; ce constat ne démontre ni réussite ni échec de la méthode.

## 5. Risques et périmètre

- Les méthodes de découverte opèrent dans des classes/grammaires déclarées, pas dans une classe universelle de toutes les fonctions possibles.
- L'intervention causale est limitée aux capacités effectivement fournies par l'adapter et aux entrées testées.
- La reconstruction actuelle valide une fonction booléenne finie et symbolique; elle ne récupère pas les poids et ne prouve pas l'équivalence causale d'un réseau.
- Le graphe de circuits est un graphe d'influences observées et de dépendances; il ne constitue pas à lui seul une ontologie causale exhaustive.
- L'interface Web est volontairement locale (loopback) et l'adapter HF a `trust_remote_code=False`, `local_files_only=True` par défaut.
- Les archives finales et leur clean-room verification sont documentées dans `cleanroom_archive_validation_receipt.json` dans le bundle d'audit/suivi final; le dépôt de travail contient le reçu source ci-dessus.

## 6.1 Recherche affine sur vocabulaire large

La suite de tests comprend deux contrôles dédiés à la recherche sur des vocabulaires plus grands : une recherche sur un vocabulaire synthétique de 32 000 tokens dans la classe `small_coefficient_modular_affine_v1`, puis un test du sélecteur `auto` avec vocabulaire 257. La première vérifie une règle cible dans la classe de coefficients déclarée `{−1,0,1}` (9 paires de coefficients, puis calcul du biais depuis les données d'entraînement), avec une complexité annoncée `O(9*n)`. Ces essais valident l'implémentation et la recherche sur les données synthétiques du test ; ils ne démontrent pas la découverte d'une règle arbitraire dans un LLM réel.

## 7. Conclusion d'audit

Les éléments livrés étayent les fonctionnalités explicitement testées, dans leur domaine exact. Ils n'étayent aucune affirmation de reconstruction complète d'un LLM pré-entraîné. Les systèmes de validation et de traçabilité ne préprogramment ni réussite ni échec : ils enregistrent les résultats obtenus, les limites de portée, les contre-exemples et les expériences non exécutées.


===== SOURCE: NGeGenBrain/Amodel_NGeGenBrain_v2/rapport_experimentation_NGeGenBrain_v2.md =====
# Rapport d’expériences officiel — NGeGenBrain_v2

- Date UTC : `2026-10-27T15:33:59Z`
- Environnement : `Linux-6.18.55-x86_64-with-glibc2.41` / Python `3.13.5`
- Intégrité des registres : **VALIDE**

## 1. Reconstruction synthétique aveugle

- Benchmark : `SYNTH-PARITY-4`
- Classe d’hypothèses : affine booléenne / XOR
- Lignes découverte : 12
- Lignes holdout : 4
- Exactitude holdout : 1.0
- Exactitude sur la table complète observée : 1.0
- Domaine exhaustif : `True`
- Reconstruction : `VALIDATED_ON_SUPPLIED_HOLDOUT`

Interprétation : le candidat a reproduit la fonction binaire étudiée sur les 16 entrées observées, dont 4 réservées au holdout. Cela valide ce cas fonctionnel borné uniquement. Cela n’établit ni l’équivalence causale du réseau, ni la reconstruction de ses poids, ni la reconstruction d’un LLM.

## 2. Échelle de modèles synthétiques

Le banc de test a exercé huit niveaux de modèles synthétiques : fonction linéaire, parité logique, interactions, représentations distribuées, voies concurrentes, composition hiérarchique, mini-Transformer encodeur et mini-modèle causal génératif. Pour chaque niveau, le moteur a exécuté une requête boîte noire et une capture/intervention sur le modèle instrumentable. Le modèle causal a aussi généré des tokens. Ce sont des tests de l’infrastructure d’observation/instrumentation ; seul le cas parité 4 bits ci-dessus est une reconstruction fonctionnelle aveugle évaluée.

## 3. Intervention causale instrumentée

- Hypothèse enregistrée avant test : `HYP-a41ec984b018`
- Expérience : `EXP-c98bcb46b7a9`
- Cible : `xor_layers.0.positive`
- Intervention : `zero` sur l’entrée `[1,0,0,0]`
- Delta L2 observé : `2.0`
- Statut de l’hypothèse après le test : `SUPPORTEE`

Ce résultat soutient uniquement l’effet local prédit dans cette configuration ; d’autres entrées, contrôles et interventions sont nécessaires pour identifier une fonction générale.

## 4. Balayage causal et contrôle négatif

- Entrées balayées : `8`
- Effets comparables : `8`
- Effets non nuls : `2`
- Minimum / maximum du delta L2 : `0.0` / `2.0`

Le balayage inclut des cas avec effet nul et des cas avec effet non nul. Il ne représente que les huit entrées prédéfinies et ne justifie pas une généralisation à toutes les entrées.

## 5. Contrôle adversarial par contre-exemples

- Candidat volontairement incomplet : `{'features': [0, 1], 'bias': 0, 'complexity': 2}`
- Lignes évaluées : `8`
- Contre-exemples détectés : `4`

Ce contrôle positif confirme que le chemin de détection peut signaler un candidat insuffisant sur les observations fournies ; il ne mesure pas la couverture des contre-exemples hors échantillon.

## 6. Découverte numérique

- Classe : `numeric_expression_grammar_v1`
- Statut : `CANDIDATE_FOUND`
- Candidat : `{"op": "add", "args": [{"op": "var", "index": 0}, {"op": "var", "index": 1}]}`
- Validation indépendante : `{"evaluated": true, "count": 3, "correct": 3, "accuracy": 1.0, "errors": [], "tolerance": 1e-09}`

## 7. Composition déclarative

- Sortie : `{"y": 1}`

## 8. Périmètre non exécuté

Aucun modèle LLM externe n’a été chargé ; l’adapter Hugging Face n’a pas été exercé sur des poids réels, car `transformers` et un checkpoint local n’étaient pas disponibles. Cette absence d’expérience n’est ni une preuve de réussite, ni une preuve d’échec du protocole sur les LLM.
## 9. Reconstruction d’un Transformer causal synthétique entraîné

- Statut découverte-règle : `VALIDATED_GREEDY_BEHAVIOR_ON_HELDOUT_AND_COMPOSED_TRAJECTORIES`
- Contextes train/holdout : `20` / `5`
- Exactitude holdout : `1.0`
- Concordance des trajectoires générées après composition : `1.0`
- Reconstruction table/logits : `VALIDATED_ON_QUERIED_FINITE_CONTEXT_DOMAIN_AND_COMPOSED_TRAJECTORIES`
- Concordance exacte des logits observés : `1.0`
- Concordance des générations composées : `1.0`

Portée : le système a produit deux implémentations indépendantes à partir des sorties d’un minuscule Transformer causal synthétique dont l’inspection interne était désactivée : un modèle par règle découvert sur les contextes de découverte et validé sur des contextes réservés, ainsi qu’un modèle de table reproduisant exactement les logits des contextes interrogés et leurs trajectoires composées. Ce résultat n’établit pas l’équivalence des circuits internes et ne se généralise pas automatiquement à un LLM de taille réelle.


## 10. Recherche de prochain-token sur vocabulaire large

Les tests de contrat de la recherche affine modulaire utilisent un jeu synthétique à vocabulaire `V = 32 000`, avec huit contextes d'entraînement. Dans la classe explicitement déclarée `small_coefficient_modular_affine_v1`, le moteur trouve une candidate unique de coefficients `(previous=0, current=1, bias=1)` et vérifie les huit lignes d'entraînement. La classe examine neuf paires de coefficients `(a,b) ∈ {-1,0,1}²`, puis calcule les biais compatibles ; la complexité annoncée est `O(9*n)` pour cette classe, pas pour toutes les fonctions possibles. Un autre test vérifie la sélection automatique de cette stratégie pour `V=257` et la généralisation sur les observations réservées. Ces résultats sont des tests synthétiques de l'algorithme, pas une expérience sur les poids d'un LLM réel.


===== SOURCE: NGeGenBrain/Dmodel_NGeGenBrain_v2/README.md =====
# NGeGenBrain_v2 — Laboratoire d'étude mécaniste et de reconstruction fonctionnelle

**Version de travail :** `2.0.0.dev0`  
**Date de constitution :** 2026-10-27  
**Langage principal :** Python 3.11+  
**Cœur :** bibliothèque standard Python ; PyTorch optionnel pour l'instrumentation neuronale.

NGeGenBrain_v2 conserve dans `legacy_NGeGenBrain_v1/` le dépôt source complet de la V1 et ajoute un laboratoire d'expérimentation pour modèles neuronaux instrumentables. La V2 est organisée autour d'adapters à capacités déclarées, d'observations sérialisables, d'interventions contrôlées, de registres chaînés par SHA-256, de la découverte de règles dans des classes d'hypothèses explicites, et de la composition/reconstruction de modèles symboliques exécutables.

## Démarrage rapide

```bash
python ngbrain.py init
python ngbrain.py status
python ngbrain.py inspect --model synthetic:parity4
python ngbrain.py observe --model synthetic:parity4 --input '[0,1,1,0]'
python ngbrain.py benchmark --bits 4 --seed 20261027 --max-samples 4096
python ngbrain.py synthetic-ladder --seed 20261027
python ngbrain.py reconstruct --source synthetic --seed 712 --vocab-size 5 --epochs 40 --max-new-tokens 8
python ngbrain.py audit
```

Pour lancer l'interface Web locale :

```bash
python ngbrain.py serve --host 127.0.0.1 --port 8766
```

Ouvrir `http://127.0.0.1:8766/`. Le serveur intégré refuse une écoute sur une adresse non-loopback.

Pour jouer une intervention causale sur le modèle synthétique (structure visible explicitement) :

```bash
python ngbrain.py experiment --model synthetic:parity4 --input '[1,0,0,0]' --target xor_layers.0.positive --mode zero
python ngbrain.py sweep --inputs-file examples/causal_sweep_inputs.json --target xor_layers.0.positive --mode zero
python ngbrain.py plan --inputs-file examples/causal_sweep_inputs.json --target xor_layers.0.positive
python ngbrain.py counterexamples --rows-file examples/discovery_validation_parity3.json --candidate-file examples/affine_candidate_parity3.json
```

## Adapter un LLM Hugging Face local

Le module `src/nggegenbrain_v2/adapters/huggingface.py` offre un adapter optionnel. Installer les extras puis pointer vers un modèle déjà présent localement :

```bash
pip install -e '.[huggingface]'
```

L'adapter est construit avec `trust_remote_code=False` et `local_files_only=True` par défaut. Les capacités sont déclarées explicitement. Le paquet `transformers` n'était pas installé dans l'environnement de validation présent, et l'accès réseau pour l'installer a échoué (résolution DNS indisponible) ; aucun checkpoint LLM externe n'était présent. Aucun LLM externe n'a donc été chargé ni testé dans cette livraison. Le contrat logiciel de l'adapter a été testé avec un faux modèle compatible au protocole (`tests/test_huggingface_adapter_mock.py`), ce qui ne remplace pas un test de checkpoint réel. Le mini-modèle causal synthétique est distinct d'un LLM pré-entraîné.

## Forme de l'architecture

- `adapters/base.py`: contrat du modèle et frontière de capacités.
- `adapters/torch_adapter.py`: capture d'activations par hooks temporaires, interventions scoped, hash de poids et génération autoregressive pour un module déclarant explicitement `is_causal_lm=True`.
- `adapters/huggingface.py`: adapter facultatif pour causal LM local.
- `adapters/synthetic.py`: huit terrains synthétiques progressifs, du réseau linéaire au mini Transformer causal de génération.
- `analysis/causal.py`: expériences appariées baseline/intervention et mesures de delta.
- `analysis/hypotheses.py`: cycle de vie des hypothèses, contre-preuves et historique.
- `discovery/rules.py`: induction GF(2) dans une classe formelle déclarée (parité/XOR booléen affine).
- `discovery/numeric.py`: recherche bottom-up d’expressions arithmétiques exécutables dans une grammaire déclarée, avec budget explicite et statut de troncature.
- `discovery/engine.py`: registre extensible de stratégies d’induction.
- `discovery/circuits.py`: graphe d'influences observées sous intervention, avec portée explicitement limitée.
- `composition.py`: langage déclaratif sûr et exécutable pour mécanismes composés, sans `eval`/`exec`.
- `reconstruction/engine.py`: reconstruction symbolique indépendante à partir de règles découvertes; `reconstruction/causal_lm.py` fournit la découverte d’une règle de prochain token dans une classe finie annoncée et la reconstruction par table de logits sur contextes explicitement interrogés. `reconstruction/synthetic_benchmark.py` entraîne un minuscule Transformer causal synthétique, le met derrière un adaptateur boîte noire et produit des modèles composés indépendants.
- `synthetic_lab.py`: benchmark aveugle avec séparation du répertoire d'analyse et de la vérité d'audit.
- `registry.py`: journal JSONL append-only chaîné par SHA-256, vérification et écriture atomique.
- `web.py`: API locale et interface de laboratoire.

## Échelle synthétique progressive

La commande `synthetic-ladder` exerce huit architectures reproductibles : réseau linéaire, réseau logique/parité, réseau d’interactions, réseau à représentations distribuées, chemins concurrents, réseau hiérarchique, mini-Transformer encodeur et mini-Transformer causal capable de générer des tokens. Le résultat d’exécution officiel se trouve dans `benchmarks/results/20261027_official/synthetic_ladder_results.json`. Cette échelle vérifie l’instrumentation, le comportement boîte noire/instrumentable et la capture/intervention; elle ne prétend pas que les mécanismes internes de ces architectures sont tous reconstruits.

## Échelle synthétique livrée

Le module `adapters/synthetic.py` expose huit niveaux instrumentables via `create_synthetic_level(level, black_box=...)` : (1) réseau linéaire, (2) circuit XOR, (3) interactions, (4) représentation distribuée, (5) voies concurrentes, (6) MLP hiérarchique, (7) mini-Transformer encodeur, (8) mini-Transformer causal génératif. Le protocole `run_synthetic_ladder_smoke()` exécute les huit modèles, enregistre les empreintes, vérifie les captures/interventions et teste la génération du niveau causal. Ces tests valident les adapters, pas la reconstruction mécaniste de chaque architecture.

## Reconstruction d’un modèle causal génératif

La commande `reconstruct --source synthetic` entraîne un petit Transformer causal sur une grammaire synthétique, puis ne fournit à la méthode de découverte qu’un adaptateur de requête sans inspection, capture d’activations ni exposition de paramètres. Le protocole exécute deux chemins indépendants : (1) ajuste une règle modulaire de prochain token dans une classe déclarée, en séparant strictement contextes d’entraînement et holdout ; (2) construit une table autonome des logits pour les contextes expressément interrogés. Les deux artefacts composés exécutent leur propre boucle autoregressive et ne consultent pas la source lors de l’inférence.

```bash
python ngbrain.py --workspace ./workspace_lm reconstruct --source synthetic --seed 712 --vocab-size 5 --epochs 40 --max-new-tokens 8
```

Sorties principales : `public_summary.json`, `rule_reconstruction.json`, `composed_rule_model.json`, `finite_context_lookup_reconstruction.json`, `composed_lookup_model.json` et `auditor_only/hidden_ground_truth.json`. Le dernier fichier est réservé à l’auditeur du benchmark et ne doit pas être transmis au moteur de découverte. Les valeurs du rapport officiel donnent la portée exacte du test effectivement exécuté. Ce cas démontre uniquement une reconstruction comportementale sur un Transformer synthétique minuscule et la classe/domaine précisés ; il ne vaut pas reconstruction interne d’un LLM pré-entraîné de taille réelle.

Un LLM Hugging Face local peut être chargé en mode local-only avec `reconstruct --source huggingface-local --model-path ... --mode lookup|rule|both --contexts-file ... --prompts-file ...`. Le mode `lookup` accepte une liste de contextes token-ID explicitement interrogés. Les modes `rule` et `both` exigent un objet JSON avec des champs séparés `training_contexts` et `validation_contexts` (disjoints) ; `both` exige aussi `lookup_contexts`. Le mode règle utilise par défaut `small_coefficient_modular_affine_v1`, qui examine une classe explicitement restreinte de coefficients `{−1,0,1}` modulo le vocabulaire. Le mode Python `auto` utilise l'énumération exacte `modular_affine_next_token_v1` pour vocabulaire ≤32, et la classe à coefficients réduits au-delà, pour ne pas lancer une recherche cubique déraisonnable. Cette classe réduite est plus scalable, mais n'est pas une recherche universelle de toutes les règles. Les contextes de validation ne sélectionnent jamais la règle. Il faut une couverture suffisante des contextes rencontrés pendant la génération en mode lookup ; un contexte absent n’est pas complété par des logits inventés. Le test avec un vrai checkpoint exige le paquet `transformers` et le checkpoint local ; l’adapter est testé par contrat logiciel séparément.

## Benchmark synthétique livré

Le benchmark `SYNTH-PARITY-n` interroge un petit réseau ReLU déterministe par entrées binaires. L'analyseur ne voit qu'un adapter de requête : il ne voit ni poids, ni couches, ni mécanismes internes. Un sous-ensemble de lignes sert à découvrir une règle candidate ; les autres lignes sont réservées à la validation. L'auditeur conserve séparément la description de construction du benchmark dans `auditor_only/hidden_ground_truth.json`.

Pour `n=4`, le benchmark a découvert une règle XOR des quatre variables, obtenu une exactitude `1.0` sur le holdout de 4 lignes et `1.0` sur la table binaire complète interrogée. C'est une preuve d'exécution utile pour un problème booléen borné et la classe d'hypothèses déclarée. **Ce n'est ni une reconstruction de poids, ni une preuve d'équivalence mécaniste, ni une reconstruction de LLM.**

## Tests

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
python ngbrain.py benchmark --bits 4 --seed 20261027 --max-samples 4096
python ngbrain.py synthetic-ladder --seed 20261027
python ngbrain.py reconstruct --source synthetic --seed 712 --vocab-size 5 --epochs 40 --max-new-tokens 8
python ngbrain.py audit
python ngbrain.py legacy-test
```

Le dépôt V1 est gardé et les tests d'origine s'exécutent à partir de cette copie. Les reçus dans `audit/` donnent les commandes et les résultats réellement observés.

## Environnement et ressources

Le code cœur V2 n'exige aucun paquet tiers. Les adapters PyTorch exigent `torch`; l'adapter Hugging Face exige en plus `transformers`. Les LLM ne sont pas téléchargés automatiquement. Un modèle ouvert particulier n'est pas inclus dans les archives et les expériences sur un LLM externe doivent être lancées sur une machine qui a accès à ce modèle et aux ressources nécessaires.

## Vérification de la version de travail

Le reçu source courant (`audit/validation_receipt.json`) enregistre le résultat du dernier passage de validation ; les comptes finaux exacts sont dans `audit/validation_summary.md` et les journaux bruts `audit/test_runs/`, la compilation Python, la compilation LaTeX, les commandes CLI intégrées, la syntaxe de tous les JSON recensés et les CRC des trois ZIP de référence. L'attestation clean-room de l'archive livrée est distincte et se trouve dans le bundle d'audit/suivi après création de l'archive.

## Terminologie de statut

- **implémenté** : module et contrat présents dans le dépôt.
- **testé** : commande et résultat présents dans un reçu.
- **validé dans un domaine** : résultats hors-échantillon vérifiés dans le domaine nommé.
- **non exécuté** : aucune expérience n'est revendiquée.
- **non démontré** : aucune équivalence ou capacité générale n'est revendiquée.

Les résultats négatifs, ambigus et divergents sont conservés ; l'auditeur de benchmark n'est jamais injecté dans l'interface de découverte.

## V1 conservée

Le code source complet V1 se trouve dans `legacy_NGeGenBrain_v1/`. Pour les détails sur son AST, contrats, maillage, traces, stockage, modèle du monde, CLI/Web et formalismes originaux, consulter son `README.md` et `docs/REPORT_AUDIT_NGeGenBrain_v1.md`.

## Licence

La licence incluse est la licence de recherche/non commerciale personnalisée de V1, conservée sans modification. Consulter `LICENSE`.


===== SOURCE: eLLM/Dmodel_eLLM_v0/README_FR.md =====
# eLLM_v0 — modèle local expérimental fondé sur les empreintes

## Description et statut

Cette distribution contient un modèle probabiliste autorégressif à n-grammes interpolés, ajusté par comptages de corpus, avec un pipeline d’empreintes exactes multi-résolution. Elle fournit un tokenizer, un modèle prédictif sérialisable, des partitions et seuils d’empreinte, une fermeture empirique sur univers fini, un graphe relationnel, une mémoire locale optionnelle, une recherche de faisceau et une imagination de trajectoires reproductibles, six diagnostics observationnels distincts (proxies, non vérités latentes), des contrôles de factorisation/transport, une API HTTP et une interface Web de chat. Le prédicteur livré est un modèle statistique compact, pas un Transformer ni un LLM de grande échelle. Cette description porte sur l’artefact livré ; elle ne préjuge pas de développements ultérieurs.

## Prérequis et autonomie

- Python 3.10 ou plus récent.
- Aucun paquet Python tiers nécessaire à l’exécution, au service Web ou aux tests.
- Pas d’accès Internet requis : les ressources Web sont locales au package.
- Un navigateur moderne est nécessaire pour l’interface.

## Démarrage

Depuis le répertoire `Dmodel_eLLM_v0` :

```bash
python run_eLLM_v0.py serve --host 127.0.0.1 --port 8765
```

Puis ouvrir `http://127.0.0.1:8765`. Sous Linux/macOS, `./start_unix.sh` lance le serveur. Sous Windows, double-cliquer `start_windows.bat` ou l’exécuter depuis un terminal. Arrêt par `Ctrl+C`. Le serveur écoute sur loopback par défaut. Ne l’exposez pas à un réseau public sans ajouter authentification, TLS et une politique de sécurité adaptée.

## Entraînement reproductible livré

Le checkpoint distribué a été entraîné sur `data/corpus_fr.txt`, 80 paragraphes, split déterministe 64/8/8 avec graine 2025. La sélection compare 25 configurations sur validation uniquement, fixe le contexte maximal testé (5 tokens) afin que le prompt utilisateur puisse contribuer à l’état prédictif, puis choisit le lissage par NLL de validation. Le test réservé a été évalué après gel du choix.

Pour reproduire la sélection :

```bash
python scripts/tune_and_train.py --corpus data/corpus_fr.txt --checkpoint checkpoints/model.json --metrics checkpoints/training_metrics.json --seed 2025 --contexts 1,2,3,4,5 --alphas 0.35,1,3,10,30 --max-vocab 5000 --selection-policy max_context_then_validation_nll
```

Cette commande est la procédure recommandée. La commande générique `train` enregistre et évalue une configuration explicitement demandée ; elle ne fait pas la recherche d’hyperparamètres. Le script de sélection est volontairement séparé. Pour utiliser un autre corpus, conservez son hash, séparez les données par document et ne réutilisez pas le test pour choisir les hyperparamètres.

## Commandes de travail

```bash
python run_eLLM_v0.py chat
python run_eLLM_v0.py footprint "une phrase d’exemple"
python run_eLLM_v0.py search "Une empreinte observe les données" --max-new-tokens 8
python run_eLLM_v0.py imagine "Une empreinte observe les données" --count 3 --max-new-tokens 12 --seed 17
python run_eLLM_v0.py diagnose "Une requête à examiner" --search-depth 3
python run_eLLM_v0.py transport-check "une fleur verte" "une route verte" --resolution 1 --output-mode token_count
python run_eLLM_v0.py evaluate --corpus chemin/vers/test.txt
python -m unittest discover -s tests -v
node --check web/app.js
```

Le format du corpus est UTF-8, les paragraphes étant séparés par une ligne vide. `evaluate` doit recevoir un corpus de test distinct si l’on veut une mesure non contaminée.

## API locale

- `GET /api/status` : état et paramètres du checkpoint actif.
- `GET /api/metrics` : rapport métrique d’entraînement.
- `GET /api/memory` : statistiques de la mémoire relationnelle locale.
- `POST /api/chat` : génération ; JSON avec `message`, `session_id`, `use_memory`, `max_new_tokens`, `temperature`, `top_k`.
- `POST /api/search` : recherche déterministe par faisceau ; paramètres `message`, `max_new_tokens`, `beam_width`, `branch_top_k`.
- `POST /api/imagine` : échantillonnage reproductible de trajectoires internes ; paramètres `message`, `count`, `max_new_tokens`, `temperature`, `top_k`, `seed`.
- `POST /api/diagnostics` : calcule `D_obs`, `D_cap`, `D_res`, `D_search`, `D_transfer` et `D_constraint`, avec périmètre et avertissements explicites. Plusieurs valeurs sont des proxies opérationnels, pas des déficits latents établis.
- `POST /api/transport-check` : vérifie la constance d'une sortie sur les fibres d'un univers fini fourni et la restriction inter-résolutions `r_{high→low}`.
- `POST /api/reset` : effacer l’historique serveur d’une session.
- `POST /api/memory/clear` : effacer la mémoire relationnelle.

L’API accepte une demande de génération jusqu’à 2048 tokens comme garde-fou opérationnel du serveur local ; le modèle lui-même n’impose plus de maximum arbitraire dans sa méthode de génération. Un token de fin peut arrêter la génération avant la longueur demandée.

## Définition opérationnelle des empreintes

Pour une suite de tokens `x`, la sonde `suffix_k` renvoie ses `k` derniers tokens. La signature au niveau `k` contient les réponses `suffix_1, …, suffix_k`. Les familles sont emboîtées et produisent des partitions exactes. Le seuil entre deux séquences est la longueur de leur suffixe commun, bornée par le niveau d’observation calculé. Les signatures servent aux quotients ; la distribution de probabilités du prédicteur reste une observable numérique distincte.

La fermeture, la capacité effective, la dimension effective, le seuil et la factorisation sont calculés sur des domaines finis explicites : ils ne sont pas automatiquement établis pour l’ensemble infini de toutes les séquences possibles.

## Résultat de l’évaluation actuellement livrée

La sélection seed 2025 a retenu `max_context=5` et `alpha=10`. Sur le test réservé de 8 documents (328 tokens scorés), la perplexité est 217.039 et l’exactitude top-1 21.04 %. Le baseline unigramme évalué sur les mêmes documents obtient une perplexité 449.916 et une exactitude top-1 5.79 %. Ce résultat est descriptif pour ce petit corpus et ce split ; il ne prouve ni une performance générale, ni la factualité, ni la validité empirique de la théorie. Des générations observées peuvent être incohérentes, très courtes ou incorrectes.

## Confidentialité, logs et sécurité

L’historique de session et la mémoire optionnelle sont écrits dans le répertoire local `memory/`; les erreurs sont journalisées dans `logs/`. Aucun contenu n’est envoyé à une API distante. Supprimez les fichiers locaux si les données sont sensibles. La limite de 4000 caractères par prompt et celle de 2048 tokens par requête HTTP sont des contrôles d’entrée de l’application, pas des propriétés mathématiques du modèle.

## Validation interface

La suite automatisée valide les API HTTP sur le vrai serveur. Le rendu DOM Chromium a aussi été testé en chargeant les fichiers HTML/CSS/JavaScript réels avec un `fetch` simulé, car la politique de l’environnement de développement bloquait la navigation du navigateur vers loopback. Ce test ne remplace pas un essai manuel sur chaque navigateur et chaque système d’exploitation.

## Recherche et imagination internes

Depuis le composeur Web, **Explorer** lance une recherche déterministe de continuations (beam search), **Imaginer** échantillonne plusieurs trajectoires avec graines reproductibles, et **Diagnostiquer** expose les six familles de proxies observables. Les opérations correspondantes sont également disponibles par les routes locales `/api/search`, `/api/imagine` et `/api/diagnostics`. Le contrôle de transport fini est accessible via `/api/transport-check` et la CLI `transport-check`. Elles explorent les probabilités apprises du checkpoint, sans réponse-cible codée en dur. La trace renvoie les niveaux d'empreinte associés.

CLI : `python run_eLLM_v0.py search "Utilisateur : exemple Assistant :"` et `python run_eLLM_v0.py imagine "Utilisateur : exemple Assistant :"`.


===== SOURCE: eLLM/Amodel_eLLM_v0/README_AUDIT_FR.md =====
# Audit de eLLM_v0 — version 0.2.0

Ce dossier regroupe les scripts de vérification, les résultats de tests et d'expériences, les captures Chromium, le smoke du serveur/CLI, les incidents historiques conservés et les rapports/formalismes LaTeX.

## Lecture recommandée

1. `reports/rapport_eLLM_v0.tex` décrit l'ensemble du processus selon le format demandé : description, architecture, pipeline complet, commandes, résultats, interprétations, conséquences, conclusions et statut.
2. `reports/formalime_model_eLLM_v0.tex` détaille les équations réellement instanciées dans le code. Le nom `formalisme_model_eLLM_v0.tex` est fourni comme alias orthographique identique.
3. `final_integration_smoke.json`, `browser_ui_test.json` et `experiments/` contiennent les résultats agrégés ; le dossier `logs/` contient les journaux correspondants.
4. `incidents/` conserve les erreurs rencontrées, leurs corrections et leur statut, au lieu de les effacer de l'historique.
5. `MANIFEST_SHA256.json` permet de vérifier les fichiers de l'archive après extraction.

## Résultats importants

- Le checkpoint du modèle contient un prédicteur probabiliste interpolé à n-grammes variables, pas un Transformer.
- Corpus de démonstration : 80 paragraphes ; split de livraison 64/8/8 ; checkpoint SHA-256 `3e42677b469937ba688022c30d968752c412c09eaabe3d826d2712f6e84590dc`.
- Perplexité du test réservé : 217.0393 contre 449.9162 pour le baseline unigramme sur le même split.
- Suite finale : 38 tests unitaires/HTTP ; smoke serveur/CLI : 17 contrôles ; Chromium DOM avec API mockée : PASS.
- Invariants structurels : 80 états, 512000 triplets, zéro violation dans le domaine fini enregistré.
- Validation de portabilité après extraction propre : 38/38 tests et routes locales principales PASS; détails dans `experiments/clean_extraction_portability.json`.

Ces résultats ne certifient pas une compréhension générale ni une performance sur des corpus externes. Le rapport documente leur portée précise.

## Rejouer les contrôles

En extrayant les trois archives dans un même dossier, lancer les commandes du rapport depuis `Dmodel_eLLM_v0/`. Les scripts d'audit résolvent leur racine relativement à leur propre fichier et peuvent être exécutés depuis `Amodel_eLLM_v0/`. Certaines expériences nécessitent Playwright/Chromium pour le test navigateur ; cela concerne l'audit seulement, pas l'application livrée.


===== SOURCE: models_order/model_order_80_2_2_CORRIGE_HIERARCHICAL_STRICT/README.md =====
# ORDER80.2.2 — moteur généraliste hiérarchique corrigé

Cette release est la correction d’ORDER80.2.1 après benchmark RAG. Elle rétablit la logique de contrôle hiérarchique au niveau de l’entrypoint général et sépare explicitement une **synthèse documentaire vérifiée** d’une **solution du problème**.

## Cycle

```text
problème
→ observer
→ résoudre
→ échec
→ observer davantage
→ résoudre
→ …
→ décomposer
→ sous-problèmes
→ chaque sous-problème : observer → résoudre → observer davantage → décomposer encore
→ nouveauté vérifiée
→ mémoire
→ news/
→ retest racine
→ peer-probes
→ poursuivre
```

Le cycle est enregistré dans `events.jsonl` et `subproblem_tree.json`. Une nouvelle tentative ne constitue pas un progrès si l’état documentaire est identique.

## Sens des statuts

Le moteur ne considère plus une réponse provenant de plusieurs sources comme une « solution » universellement vérifiée. Une `DOCUMENTED_INSIGHT` peut être mémorisée et placée dans `news/`, mais la résolution complète d’un problème exige un vérificateur de domaine explicite. Sans celui-ci, la fin de run est `NO_DOMAIN_VERIFIED_COMPLETE_SOLUTION_IN_THIS_EXECUTION`.

## Installation

Python 3.10+ et bibliothèque standard uniquement.

```bash
unzip model_order_8_0_2_2.zip -d model_order_8_0_2_2
cd model_order_8_0_2_2/model
python3 -m pytest -q
python3 self_test_order8022.py
```

## Lancement

```bash
python3 run_order_8_0_2_2.py --task task.json --references references.json --output run --duration 1h
python3 run_order_8_0_2_2.py --task task.json --references references.json --output run --duration 24h
```

`--no-web` coupe le réseau. Les références locales sont limitées au manifeste. Le RAG dynamique accepte les nouveaux documents dans `run/rag_inbox/documents/` et `run/rag_inbox/formal/`. Quand aucun nouveau contenu n’est disponible, `run/rag_inbox/requests/CURRENT_REQUEST.json` est écrit.

## Nouveautés

Les connaissances documentaires nouvellement vérifiées comme couvrant le contrat sont mémorisées comme `DOCUMENTED_INSIGHT`. Elles ne sont jamais promues automatiquement en axiome ou en certificat mathématique. Un vrai certificat doit passer le vérificateur correspondant au domaine.

## Sécurité

Les règles web de la branche 8.0.2.1 sont conservées : HTTPS par défaut, allowlist des domaines, validation DNS/public IP, ports autorisés, redirections contrôlées, taille/type bornés, contenu non exécuté, hashes optionnels et journalisation.

## Audit

Chaque run produit `events.jsonl`, `observation_ledger.json`, `memory.json`, `subproblem_tree.json`, `checkpoint.json`, `news/` et `rag_inbox/`.


===== SOURCE: models_order/model_math_order_O76_CORRIGE_O76_1_1/README.md =====
# MODEL mathématique O76 — version corrigée O76-1.1

O76 est un moteur mathématique exact orienté preuve. Il n'utilise ni modèle de langage, ni oracle de benchmark, ni solveur symbolique externe dans son chemin de décision. La production d'un statut `PROVEN` ou `REFUTED` exige un certificat rejouable par un vérificateur indépendant.

## Exécution en une commande

```bash
python3 run_math_O76.py examples/prove_groebner.json
```

Sous Windows :

```text
py run_math_O76.py examples/prove_groebner.json
```

Le fichier de configuration `config/o76.json` permet de régler temps, nombre de trajectoires, paires Buchberger, cas d'énumération, mémoire et stratégie. Les mêmes paramètres sont surchargeables par la ligne de commande.

## Contrat de sortie

- `PROVEN` : certificat présent et accepté par le vérificateur exact.
- `REFUTED` : contre-certificat exact, par exemple contre-exemple exhaustif ou contre-modèle propositionnel.
- `UNRESOLVED` : aucune conclusion certifiée n'a été obtenue dans le portefeuille et les ressources déclarées. Ce statut ne signifie pas « impossible ».

## Familles natives

Arithmétique rationnelle exacte; identités polynomiales; conséquences linéaires; systèmes linéaires; idéaux polynomiaux avec Buchberger et certificat d'identité explicite; tours polynomiales triangulaires avec contradiction exacte; racines univariées rationnelles et réelles par Sturm; matrices sur Q; équations diophantiennes linéaires; CRT; Pell x^2-D y^2=1; logique propositionnelle; énumération exacte de domaines finis.

## Architecture émergente

Le noyau applique une boucle observée et récursive : empreinte structurelle → portefeuille de trajectoires → transformation exacte → certificat → vérification indépendante → mémoire évolutive de faits/échecs → nouvelle sélection. La théorie des empreintes sert à observer et ordonner; elle n'est jamais un oracle de réponse.

## Ce que signifie « preuve »

La garantie est opérationnelle et rejouable : le vérificateur recalcule l'objet mathématique et l'identité du certificat. Le runtime Python et le code du vérificateur constituent toutefois la base de confiance; O76 n'est pas lui-même une implémentation formellement vérifiée dans Lean/Coq/Isabelle.

## Correction O76-1.1 et test décisif

Les corrections décisives et de régression observées pendant le test externe ont été intégrées :

1. `TRIANGULAR_TOWER_EXACT` ajoute une preuve algébrique exacte par élimination arrière pour toute tour structurelle `x1^k-c=0`, `x(i+1)^k-xi=0`, `xn-r=0`, sans dépendre de la réussite de Buchberger. Les coefficients du certificat sont rejoués indépendamment.
2. `UNSUPPORTED_FORM` valide la relation entière avant de l'accepter comme mathématique : une prose contenant des signes `=` internes, comme l'énoncé de Collatz, reste hors contrat. Les `UNRESOLVED` portent maintenant les stratégies tentées et la raison `portfolio_exhausted` lorsque le portefeuille ne conclut pas.

Sur l'instance de stress profondeur 12, la version O76-1.0 n'a pas produit de certificat dans le délai de l'expérience et a dépassé le watchdog externe; O76-1.1 produit un certificat `TRIANGULAR_TOWER_CONTRADICTION` vérifié indépendamment en environ 1 seconde sur la machine de test.

Les problèmes ouverts Riemann/Collatz restent `UNRESOLVED`/`UNSUPPORTED_FORM` : le modèle ne transforme pas une question mathématique ouverte en pseudo-preuve.

La procédure complète et les résultats détaillés sont dans `rapport_experience_decisive_O76.tex`.


===== SOURCE: sondes_experiences/sondes_ex8_v010__2026-11-01_RESULTS_AND_METHODS/README.md =====
# EX8 v010 — workspace expérimental PCA / V004

Version active : `versions/sondes_ex8_v010__2026-11-01/` (cf. `/mnt/data/EX8/ACTIVE_VERSION.txt`).

Cette branche réunit le contexte EX8 v001/v009, les expériences A0–A4 et B1–B11, les comparateurs MLP, les réplications SMS train/validation et les audits indépendants. Les données sources et snapshots historiques sont conservés en référence ; les runs v010 ne les écrasent pas.

Lire en premier :
1. `reports/RAPPORT_FINAL_V010.md`
2. `reports/AUDIT_PROMPT_EX8.md`
3. `reports/STATISTICAL_ANALYSIS_V010.md`
4. `reports/RESOURCE_ANALYSIS_V010.md`
5. `configs/PRE_REGISTRATION_V010_AB.md` et l’addendum B10/B11.

Les résultats détaillés par run sont dans `results/metrics/`, `results/raw/` et `results/models/`. Les manifestes et vérifications sont sous `deliverables/` et `checksums/`. Les sorties ne doivent pas être écrasées ; toute continuation doit créer une nouvelle version sous `EX8/versions/` et conserver `v010` immuable.


===== SOURCE: sondes_experiences/sondes_ex8_v010_B10_ACTION_LANGUAGE_COMPLETE_DOSSIER__2026-11-01/README_B10_COMPLETE.md =====
# Dossier complet B10 — langage d’actions codifiées (EX8 v010)

Ce dossier complémentaire rassemble le code, les configurations, les données d’entraînement/validation autorisées, les checkpoints, les prédictions, les historiques et les comparateurs MLP pour B10 et son contrôle B11. Le paquet global EX8 v010 contient en plus toutes les autres variantes A0–A4 et B1–B9.

## Résultat B10 sur Wisconsin (5 graines)

| Graine | B10 log-loss | B11 gate standard | MLP apparié B10 | MLP ≥4× B10 |
|---:|---:|---:|---:|---:|
| 1501 | 0.04507602 | 0.04639599 | 0.05309571 | 0.05388297 |
| 1607 | 0.03892050 | 0.03918663 | 0.05443205 | 0.05022439 |
| 1717 | 0.03475841 | 0.04361378 | 0.05260622 | 0.05136449 |
| 2029 | 0.04704858 | 0.04824928 | 0.05549038 | 0.05049692 |
| 3037 | 0.04114467 | 0.04468064 | 0.05801149 | 0.04804699 |

Moyennes : B10 **0.04138964**, B11 **0.04442526**, MLP apparié B10 **0.05472717**, MLP ≥4× **0.05080315**. B10 bat son MLP apparié sur **5/5 graines** et le MLP ≥4× sur **5/5 graines**.

## Architecture B10

- Un seul niveau, cinq probes parallèles.
- Dimension latente D=4, K=4 centres par probe.
- 20 évaluations de centres RBF par observation.
- État flou 3×3 construit à partir de la marge OOF et du désaccord inter-probes.
- Une table 9×5 produit des poids continus softmax sur les cinq vecteurs de logits ; le codebook ne décide jamais la classe.
- 45 paramètres d’action ; total déclaré 884 paramètres.
- Les seuils sont estimés uniquement sur les signaux OOF du train.

## Comparaison statistique B10 vs B11

Delta moyen (B10 − B11) = **-0.00303563**. Les cinq différences par graine sont négatives, mais l’IC t apparié à 95 % [-0.00734137, 0.00127012] recouvre zéro ; le test exact de permutation des signes bilatéral donne p=0.0625. L’avantage observé doit donc rester qualifié d’encourageant mais exploratoire.

Latence p50 batch 1 moyenne : B10 0.331801 ms ; B11 0.116289 ms ; ratio B10/B11 **2.853×**. Le mécanisme d’actions est plus lent que le gate standard.

## Fichiers inclus

- `workspace/src/` : scripts d’exécution et moteur partagé.
- `workspace/configs/` : pré-enregistrement B10/B11 et configurations par graine.
- `workspace/inputs/` : code commun et Wisconsin train/validation only.
- `workspace/results/metrics/` : métriques candidates, MLP, comparatif direct et agrégats.
- `workspace/results/models/` : checkpoints B10, B11, backbone et MLP appariés/≥4×.
- `workspace/results/raw/` : prédictions et historiques B10/B11/backbone/MLP disponibles.
- `B10_B11_PAIRED_RESULTS.csv` : table condensée par graine.
- `SHA256SUMS.txt` : manifeste d’intégrité du dossier.

## Limites

Les chiffres sont des résultats de développement sur la partition Wisconsin, pas une validation externe confirmatoire. La réplication SMS est historiquement exposée et B10 n’y bat pas les MLP. Le test indépendant n’a pas été ouvert dans cette campagne. Les checkpoints et prédictions fournis permettent l’inspection et la vérification des métriques ; une reproduction exacte de l’environnement exige les versions de bibliothèques et le matériel documentés dans la configuration système du workspace complet.


===== SOURCE: sondes_experiences/EX11_DELIVERABLES_SNAPSHOT_38_OF_65_20261103T125332Z/README_EX11.md =====
# EX11 — workspace expérimental dédié

EX11 est isolé sous `/mnt/data/EX11/`. Les archives historiques EX3–EX10 et `last_sources_3.zip` restent hors de ce workspace. Les seules données tabulaires réelles copiées ici sont les 13 données ARFF jointes pour EX11. Les tâches CNG/CNC synthétiques sont générées par les scripts EX11.

## Protocole courant

- `prompt_ex11.json` : prompt reconstruit et versionné **2.3.1-reconstructed**. Ce fichier est une reconstruction contrôlée à partir des sources accessibles ; il n'est pas présenté comme une récupération d'une ancienne version introuvable.
- `PRE_REGISTRATION_EX11.md` : corps du prompt, strictement identique au champ `prompt` du JSON au niveau octet.
- `reports/PROMPT_COMPLIANCE_MATRIX_EX11_v2.3.1.md` : matrice de conformité courante, avec statut réel de chaque branche.
- `AUDIT_SOURCES_EX11.md` : analyse des sources et formalismes EX3–EX10 sans copie des archives historiques.
- `INPUT_SHA256.txt`, `checksums/` et les manifestes sous `data/metadata/` : provenance et intégrité.

## Données

- `datasets_arff.zip` passe le test CRC ; SHA-256 comparé à la pièce jointe.
- Les 13 ARFF présents sous `data/raw/datasets_arff/` sont identiques octet pour octet aux fichiers correspondants dans l'archive.
- Les 65 splits (13 jeux × 5 seeds) et 195 CSV train/validation/test ont passé une vérification indépendante : toutes les lignes source une fois, groupes X disjoints, schémas/hashes conformes.
- Les 65 CSV de test sont en mode `0440`. Aucun entraînement ni réglage n'utilise ces fichiers.
- Les doublons X, conflits de labels et chevauchements inter-jeux PROMISE sont documentés ; ils n'ont pas été supprimés.

## Code et tests

- Scripts réellement utilisés conservés dans `src/`, configs dans `configs/`, sorties dans `results/`, journaux append-only dans `logs/`.
- Test courant : `PYTHONPATH=$PWD pytest -q` → **24/24 PASS**.
- Les scripts confirmatoires préparés sont compilés : REPLICA-U v004, CNG v004, CNC v005, D3Q v004 et LOO CNG v004. Une compilation ou un test unitaire ne vaut pas exécution scientifique.

## État expérimental

L'instantané détaillé le plus récent est `reports/EX11_PROGRESS_ADDENDUM_2026-11-03_1249UTC.md`. Au moment de cet addendum, REPLICA-U v004 était à 31/65 blocs confirmatoires, tous audités ; le runner séquentiel PID 11597 était actif. Les campagnes confirmatoires CNG v004, CNC v005, CNG LOO v004 et D3Q v004 n'avaient pas encore inscrit de runs. Les branches historiques v001/v003/v004 sont conservées avec leurs statuts exploratoire ou partiel explicités.

La révision documentaire du prompt 2.3.1 corrige uniquement le numéro affiché dans le corps et le type du champ `key_design`; elle ne modifie aucune règle ou aucun budget scientifique. La version 2.3.0 est la spécification scientifique appliquée par les premiers runs v004.

La livraison finale et l'archive CRC restent à produire après consolidation. Si les budgets confirmatoires ne peuvent pas être achevés dans ce quota d'exécution, les blocs manquants seront explicitement `INCOMPLETE_QUOTA`, jamais extrapolés.

La présence d'un script ou d'un checkpoint partiel n'est jamais présentée comme une expérience complète. Tous les runs défavorables, échoués, interrompus, exploratoires ou non conformes restent conservés et identifiés.
