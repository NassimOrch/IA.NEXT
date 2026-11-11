# eSonde v4 — README complet / Complete README

**Version / Version:** 4.0.0  
**Release reviewed / Livraison examinée:** 11 November 2026  
**Architecture target / Cible architecturale:** sondes discrètes, compteurs clairsemés, index et coordination explicite — zéro neurone artificiel, zéro MLP.  
**Nature du livrable / Release type:** prototype logiciel expérimental, reproductible et audité — pas un LLM généraliste dont les performances seraient déjà établies.

---

# PARTIE I — FRANÇAIS

## 1. Vue d'ensemble et avis synthétique

eSonde v4 est un modèle de langage statistique à sondes explicites, associé à un moteur de recherche documentaire et à des fonctions de réponse extractive. Il apprend des régularités de séquences, de formes, de cooccurrences et de documents sous forme de compteurs et de tables clairsemées. Les familles de sondes produisent des distributions ou des propositions, puis COORD les combine à l'aide de coefficients scalaires calibrés sur un corpus de validation.

Le runtime livré n'utilise pas de neurones artificiels, de MLP, de Transformer, d'attention Q/K/V, d'embeddings denses appris ni de framework neuronal. Le code déployable audité est fondé sur Python standard, des dictionnaires/compteurs, des signatures déterministes, un modèle de Markov d'octets et un index documentaire.

**Avis technique :** eSonde v4 est une réalisation logicielle concrète et intéressante de l'approche « sondes uniquement ». La séparation des familles, la traçabilité, la sérialisation vérifiable, le CLI/GUI et l'ingestion multi-format constituent une base d'expérimentation utile. En revanche, les résultats actuels ne démontrent pas une compétence sémantique généraliste ni une égalité/supériorité face aux LLM classiques. Sur MLQA, la vraisemblance next-token est nettement moins bonne qu'une baseline unigramme lissée ; le score QA extractif est faible. Plusieurs familles portent actuellement des mécanismes plus simples que les constructions riches décrites dans le formalisme. Cette évaluation porte sur le checkpoint et le code livrés, pas sur une impossibilité théorique ni sur le potentiel futur de l'approche.

## 2. Les trois livrables

| Paquet | Contenu | Usage |
|---|---|---|
| `Dmodel_eSonde_v4.zip` | Runtime, checkpoint v4 de démonstration, sauvegardes du checkpoint, exemples train/validation/test, CLI, GUI, formalisation, tests et guides | Exécuter et utiliser eSonde v4 |
| `Amodel_eSonde_v4.zip` | Audit des sources et expériences, formalisation, rapports P0–P8, logs, résultats JSON, scripts d'évaluation et d'audit, checkpoint v4, poids historiques v2/v3 avec provenance | Comprendre, auditer et reproduire les expériences |
| `suivi_model_eSonde_v4` | Checklists, chemins, preuves, incidents, outils de sauvegarde/préflight et snapshots historiques | Traçabilité et restauration du travail |

### 2.1 Intégrité vérifiée

Les empreintes SHA-256 ci-dessous correspondent aux fichiers de livraison contrôlés :

```text
22022cf589a3645425edb729c7246c4a5dfe0d1ad4b5c832d06e4a38b356e42f  Dmodel_eSonde_v4.zip
d6b0c035c72da54b49f9a80b42699004ced6be54578d476a5e857955253358e0  Amodel_eSonde_v4.zip
4d195e6437006a608dbcbf3e7a98296ada573b1652968c7f68426c0bdfef5745  suivi_model_eSonde_v4.z01
e071433459cd3cbd98893bd328a4446b6409b0277982d0f35ec51272897b982a  suivi_model_eSonde_v4.zip
95671a18e1ce098a14f05ad721dc905cbae69ea4f0c326c5449cfa3fe4138e93  suivi_model_eSonde_v4_assembled.zip
```

| Fichier | Taille exacte | Contrôle |
|---|---:|---|
| Dmodel | 5 968 668 octets | CRC ZIP + 78 fichiers du manifeste SHA-256 |
| Amodel | 4 585 616 octets | CRC ZIP + 333 fichiers du manifeste SHA-256 |
| Suivi volume `.z01` | 110 100 480 octets | Empreinte SHA-256 du volume |
| Suivi volume `.zip` | 96 447 915 octets | Empreinte SHA-256 du volume |
| Suivi réassemblé | 206 548 391 octets | CRC ZIP + 9 242 fichiers du manifeste SHA-256 |

Dmodel et Amodel contiennent chacun deux fichiers de métadonnées de manifeste en plus des fichiers comptés dans leur manifeste (`PACKAGE_MANIFEST.json` et `MANIFEST.sha256`). Suivi contient lui aussi ces deux fichiers supplémentaires. Les manifestes internes ont été vérifiés fichier par fichier ; aucun fichier attendu ne manque et aucune divergence SHA-256 n'a été observée.

**Important — archive Suivi fractionnée :** `suivi_model_eSonde_v4.z01` et `suivi_model_eSonde_v4.zip` sont deux volumes d'une seule archive Info-ZIP. Le fichier `.zip` final n'est pas une archive autonome et ne doit pas être testé ou extrait isolément. Il faut conserver les deux volumes dans le même répertoire et les réassembler, ou utiliser l'archive complète `suivi_model_eSonde_v4_assembled.zip` lorsqu'elle est disponible.

Depuis le dossier qui contient les deux volumes :

```bash
python reassembler_suivi_model_eSonde_v4.py \
  --archive suivi_model_eSonde_v4.zip \
  --output suivi_model_eSonde_v4_assembled.zip
```

Le script s'appuie sur la commande système `zip` d'Info-ZIP (`zip -s 0`). Il faut donc que cette commande soit installée et accessible dans `PATH`. Le réassemblage contrôlé a produit une archive byte-identique à l'archive complète de référence, avec le SHA-256 `95671a18...e4138e93`.

### 2.2 Périmètre des sources et données

Les trois paquets ne contiennent ni l'archive source brute `eSonde_v3_sources.zip`, ni le dataset MLQA brut. Ils contiennent les rapports, empreintes, manifestes et résultats utiles à leur audit. Amodel conserve quatre checkpoints historiques v2/v3 ; leurs quatre SHA-256 concordent avec les sidecars de provenance présents dans les sources examinées.

Une réserve d'audit doit rester visible : le rapport P0 note que deux archives historiques référencées par un manifeste de 34 623 fichiers (`liverables_eSonde_v2.zip` et `last_sources_3.zip`) n'étaient pas présentes dans l'archive téléversée. Leur contenu n'a donc pas pu être réinspecté indépendamment. Ce n'est pas une perte déclarée pendant la construction de v4 ; c'est une limite du matériel source effectivement fourni.

## 3. Qu'est-ce qu'une sonde dans eSonde v4 ?

Une sonde est un opérateur explicite qui observe une partie du contexte ou de la mémoire et consulte les régularités enregistrées. Contrairement à un neurone artificiel, elle n'est pas une unité cachée dont les paramètres seraient appris par rétropropagation. Dans le runtime v4, les états sont principalement des compteurs entiers, des tables signature→cible, des profils de cooccurrence, des documents indexés et des coefficients scalaires.

À chaque position, le contexte causal est constitué des unités précédentes. Les familles applicables construisent des distributions conditionnelles ou des scores. COORD combine les distributions actives :

\[
P(y\mid h,M)=\sum_{f\in F(h)}\widetilde{\lambda}_f Q_f(y\mid h,M),\qquad
\widetilde{\lambda}_f=\frac{\lambda_f}{\sum_{g\in F(h)}\lambda_g}.
\]

Les coefficients \(\lambda_f\) sont des scalaires non négatifs normalisés sur le simplexe. La calibration les ajuste sur le split validation par mise à jour exponentielle. Cette optimisation utilise une dérivée analytique sur dix poids scalaires ; ce n'est pas une rétropropagation dans un réseau de neurones.

### 3.1 Les dix familles réellement implémentées

| Famille | Fonction dans le runtime livré | Ce que cela ne signifie pas encore |
|---|---|---|
| **SEQ** | Compte les continuations associées aux suffixes normalisés des 1 à 8 dernières unités. | Ne construit pas encore un modèle syntaxique ou discursif complet. |
| **SKIP** | Compte les continuations associées aux unités observées aux offsets 1, 2, 3, 5 et 8. | Ne réalise pas une inférence arbitraire sur des dépendances longues. |
| **MORPH** | Utilise la forme Unicode du dernier token, le script, la casse, la longueur et des préfixes/suffixes de 1 à 4 caractères. | N'apprend pas encore des paradigmes morphologiques complets ni des n-grammes de caractères généralisés. |
| **BYTE** | Modèle de Markov d'ordre 4 sur les octets UTF-8, avec BOS/EOS et lissage ; permet de donner une vraisemblance à des chaînes hors vocabulaire. | Dans cette version, il est essentiellement un prior de forme de token : sa probabilité ne dépend pas directement du contexte linguistique précédent. Il ne comprend donc pas le sens d'un mot OOV à partir de la phrase. |
| **SEM** | Profils clairsemés de cooccurrence des termes dans une fenêtre locale de quatre termes de contenu et similarité cosinus entre profils. | N'est pas un embedding dense, un graphe conceptuel universel ou une compréhension compositionnelle profonde. |
| **REL** | Compteurs de continuations indexés par le dernier terme de contenu, la dernière paire et le dernier triplet. | Ne construit pas encore de propositions typées A–relation–B ni de règles de composition relationnelle. |
| **SLOT** | Compteurs de continuations indexés par les formes des 1 à 4 unités précédentes. | Ne constitue pas encore une grammaire, un parseur syntaxique ou un système de remplissage de slots syntaxiques. |
| **DISC** | Résume les termes de contenu les plus fréquents dans les 100 derniers termes de contenu, en conservant jusqu'à 12 thèmes. | Ne résout pas encore la coréférence, les alias, les mentions d'entités ou les rôles discursifs. |
| **RETR** | Fournit à la fois des signatures prédictives sur les derniers termes et un index documentaire sparse avec un score de type BM25. | Le volet prédictif REL/RETR est actuellement redondant pour ses signatures unaires/binaires/ternaires ; le retrieval documentaire reste une fonction distincte. |
| **TRACE** | Calcule des empreintes SHA-256 de contextes de profondeur 2, 4 et 6 et associe des continuations observées. | Ne gère pas encore les trajectoires d'état, les quotients observationnels ou le raffinement formel décrits dans les parties ambitieuses du formalisme. |

**COORD** n'est pas une onzième sonde prédictive : c'est le mécanisme de combinaison des dix familles.

### 3.2 Une nuance architecturale importante

Le formalisme `formalisme_eSonde_v4.tex` contient des objectifs plus riches que le code livré : composition relationnelle, cadres syntaxiques gauche/droite, mémoire de mentions et de coréférence, trajectoires et raffinement observationnel. Le document est une spécification de direction et de critères ; il ne faut pas présenter ces fonctions comme déjà réalisées lorsque le runtime n'en implémente qu'une version réduite. Le statut précis est donc : dix opérateurs/count tables existent et sont testés, mais plusieurs constructions théoriques du formalisme restent à développer.

Autre observation concrète : REL et RETR prédictives utilisent les mêmes contextes lexicaux récents (un terme, une paire, un triplet), avec des noms de signatures distincts. Sur le checkpoint livré, leurs NLL et statistiques de support sont identiques dans les tableaux d'évaluation. Pour le prochain cycle, il serait utile de dédupliquer leur signal prédictif ou de donner à REL une véritable structure relationnelle composée.

## 4. Apprentissage, calibration et inférence

### 4.1 Apprentissage

1. Le lecteur résout un fichier, un dossier récursif ou une archive ZIP de corpus.
2. Il extrait le texte, conserve les identifiants de source et applique le nettoyage propre au format.
3. Le tokenizer segmente le texte en unités Unicode de surface ; espaces et ponctuation sont eux aussi des tokens.
4. Chaque cible est associée au contexte antérieur du même document et met à jour les compteurs des sondes.
5. SEM construit en parallèle des profils de cooccurrence distributionnelle.
6. RETR conserve les documents et des sacs de termes pour la recherche.
7. Le checkpoint JSON est mis à jour de façon atomique et accompagné d'un sidecar SHA-256 ; une sauvegarde est faite avant les actions CLI concernées.

Le modèle livré a été entraîné sur **13 documents et 1 903 tokens**, pour un vocabulaire de **709 unités**. C'est un corpus de démonstration minuscule à l'échelle de l'apprentissage du langage. La validation comprend **243 positions** ; le test interne, après lecture avec le parseur réel, comprend **248 positions**.

### 4.2 Calibration COORD

Le modèle a été calibré sur les 243 positions de validation, avec 40 itérations et un taux d'apprentissage de 0,08. La NLL moyenne mesurée sur ce petit ensemble passe de 15,0108 à 14,5203 nats/token. Le poids BYTE obtenu est d'environ 0,5128 ; les autres poids sont distribués entre SEQ, SKIP, MORPH, SEM, REL, SLOT, DISC, RETR et TRACE.

Pour la vraisemblance ouverte, les familles non-BYTE sont catégorielles sur le vocabulaire fixé par l'entraînement ; BYTE score la séquence UTF-8 complète suivie d'EOS. Une cible de validation/test n'est pas ajoutée artificiellement au vocabulaire. Ce protocole est préférable à une évaluation qui injecterait la réponse dans la liste des candidats.

### 4.3 Prédiction et génération

Le modèle peut classer des unités candidates et produire une continuation autoregressive. Les stratégies exposées sont : greedy, échantillonnage, top-k et nucleus. Les candidats proviennent du vocabulaire d'entraînement, de candidats explicitement fournis et d'un beam BYTE qui propose des chaînes UTF-8 valides.

Cette capacité de génération est une génération statistique locale. La présence d'une commande `generate` ne signifie pas que le système sait suivre des instructions complexes, raisonner sur plusieurs étapes ou rédiger des réponses fiables comme un LLM moderne.

### 4.4 Recherche et QA

- `search` classe les documents appris avec un score lexical de type BM25 et peut étendre les termes par les voisins SEM.
- `ask` récupère les documents et retourne une phrase de preuve quand un recouvrement lexical est disponible.
- `answer` reçoit un contexte explicite et tente d'en extraire un petit span contigu avec offsets et provenance.

Il s'agit d'une recherche documentaire et d'une extraction heuristique, non d'une génération libre de réponse. Le système peut s'abstenir lorsque le support est absent. Il ne faut pas confondre cette abstention et une compréhension sémantique profonde.

## 5. Formats acceptés

Le CLI `python esonde.py formats` expose 24 extensions de fichiers, plus les archives ZIP de corpus :

- Texte et markup : `.txt`, `.md`, `.rst`, `.text`, `.log`, `.org`, `.tex`, `.rtf`.
- Web/XML : `.html`, `.htm`, `.xhtml`, `.xml`.
- Données structurées : `.json`, `.jsonl`, `.csv`, `.tsv`.
- Courriels et documents : `.eml`, `.docx`, `.pptx`, `.xlsx`, `.odt`, `.ods`, `.odp`, `.epub`.
- Conteneur : `.zip`, contenant un niveau de fichiers acceptés.

Le même lecteur est partagé par `train`, `calibrate` et `evaluate`. Les fichiers PDF, les anciens fichiers Office binaires `.doc`, `.xls`, `.ppt` et les formats non listés sont rejetés explicitement. Ils doivent être convertis vers un format accepté avant ingestion. Les formats Office modernes sont extraits depuis leurs parties XML ; il ne s'agit pas d'un rendu sémantique complet de chaque mise en page ou objet incorporé.

Le runtime ne fait pas automatiquement de séparation train/validation/test. Il appartient à l'utilisateur de fournir des répertoires séparés et de ne pas entraîner le modèle sur un dossier parent qui inclurait validation ou test.

## 6. Installation et prérequis

- CPython **3.10 ou plus récent**.
- Aucun paquet Python tiers requis pour le runtime ; bibliothèque standard uniquement.
- GUI : `tkinter` / Tk-Tcl doit être disponible. Sur Linux, le paquet système Tk peut devoir être installé séparément.
- Windows, Linux et macOS avec une version compatible de Python.

Dmodel est autonome vis-à-vis des bibliothèques Python tierces ; ce n'est pas un exécutable natif incluant Python. Il faut donc installer Python avant de l'utiliser.

### Décompression

Décompresser `Dmodel_eSonde_v4.zip`. Toutes les commandes ci-dessous sont à exécuter depuis le dossier `Dmodel_eSonde_v4/`.

### Vérification initiale

```bash
python --version
python esonde.py --help
python esonde.py formats
python esonde.py verify --model models/esonde_v4_checkpoint.json
python scripts/check_runtime.py
```

Le checkpoint fourni est déjà entraîné et calibré. Éviter d'utiliser `init --force` dessus sans avoir conservé une copie. Pour une expérience depuis zéro, choisir un nouveau chemin de modèle.

## 7. Guide CLI complet

### 7.1 Initialiser un nouveau checkpoint

```bash
python esonde.py init --model models/mon_experience.json
```

### 7.2 Entraîner sur un corpus

```bash
python esonde.py train \
  --model models/mon_experience.json \
  --corpus examples/demo_corpus/train \
  --batch-id mon-lot-001
```

`--corpus` peut pointer vers un fichier pris en charge, un dossier ou un ZIP. L'entraînement est incrémental ; il ajoute les documents qui ne sont pas déjà présents, selon l'identifiant source+texte.

### 7.3 Calibrer sur validation

```bash
python esonde.py calibrate \
  --model models/mon_experience.json \
  --validation examples/demo_corpus/validation \
  --epochs 40 \
  --max-positions 5000
```

La calibration modifie les poids COORD ; elle ne doit être exécutée que sur le split validation, jamais sur le test.

### 7.4 Vérifier et inspecter le modèle

```bash
python esonde.py verify --model models/mon_experience.json
python esonde.py info --model models/mon_experience.json
python esonde.py audit --model models/mon_experience.json
```

`verify` vérifie le checkpoint et son empreinte. `info` affiche les volumes d'état et les poids COORD. `audit` examine les imports du runtime et le checkpoint selon les règles de pureté livrées.

### 7.5 Prédire et générer

```bash
python esonde.py predict \
  --model models/mon_experience.json \
  --context "Les sondes observent" \
  --top-k 12

python esonde.py generate \
  --model models/mon_experience.json \
  --prompt "Les sondes observent" \
  --strategy nucleus \
  --top-p 0.92 \
  --temperature 0.8 \
  --max-new-tokens 50
```

Stratégies disponibles : `greedy`, `sample`, `top_k`, `nucleus`. La graine de génération est configurable par `--seed`.

### 7.6 Rechercher et poser une question

```bash
python esonde.py search \
  --model models/mon_experience.json \
  --query "sparse document index" \
  --top-k 5

python esonde.py ask \
  --model models/mon_experience.json \
  --question "What is a hash function?"
```

`ask` interroge les documents déjà ingérés dans le modèle.

### 7.7 Répondre à partir d'un contexte fourni

Fournir exactement l'un des deux arguments `--context` ou `--context-file` :

```bash
python esonde.py answer \
  --model models/mon_experience.json \
  --question "What can a checksum detect?" \
  --context-file examples/demo_corpus/test/01_test.txt
```

### 7.8 Évaluer sur un split test indépendant

```bash
python esonde.py evaluate \
  --model models/mon_experience.json \
  --corpus examples/demo_corpus/test \
  --max-positions 5000
```

Le classement top-k est fait sur le vocabulaire fixe d'entraînement. La NLL ouverte peut scorer une cible OOV par BYTE. Lire attentivement la couverture et les tokens OOV ; ne pas considérer top-k seul comme un indicateur complet de qualité linguistique.

### 7.9 Sauvegarde

Les opérations du CLI créent une sauvegarde pré-exécution dans `.esonde_backups/` à côté du checkpoint et vérifient son SHA-256 avant l'opération. Les mutations du checkpoint passent par une écriture atomique et un sidecar SHA-256. Conserver régulièrement une copie externe du dossier `models/` et de `.esonde_backups/`.

## 8. Guide GUI

Lancer depuis la racine Dmodel :

```bash
python gui/esonde_gui.py
```

Ou utiliser les lanceurs fournis :

- Windows : `RUN_GUI.bat` et `RUN_CLI.bat`.
- Linux/macOS : `./RUN_GUI.sh` et `./RUN_CLI.sh` (rendre les scripts exécutables si nécessaire : `chmod +x RUN_GUI.sh RUN_CLI.sh`).

La GUI Tkinter permet de choisir le checkpoint, sélectionner un fichier/dossier/ZIP pour le corpus, sélectionner un fichier de contexte pour `answer`, et déclencher les fonctions train, calibrate, evaluate, predict, generate, search, ask, answer, info, verify et audit. Elle délègue au CLI commun ; elle ne possède pas un second moteur de génération. Une file thread-safe relaie les sorties du worker vers le thread Tk principal.

Pour les détails de champs et de boutons, consulter `docs/GUI_GUIDE.md` et `docs/GUIDE_UTILISATION_CLI_GUI.md`. L'interface graphique nécessite un affichage disponible ; le CLI fonctionne sans environnement graphique.

## 9. Tests et reproduction logicielle

Depuis la racine de Dmodel :

```bash
python -m compileall -q src gui scripts
PYTHONPATH=src python -m unittest discover -s tests -v
python scripts/check_tex_structure.py formalism/formalisme_eSonde_v4.tex
python esonde.py verify --model models/esonde_v4_checkpoint.json
```

Sur Windows PowerShell, définir temporairement le chemin du module avant les tests :

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

La révision livrée a passé **26/26 tests** dans une extraction fraîche de Dmodel, ainsi que `compileall`, l'aide CLI, la liste des formats et la vérification du checkpoint. Les rapports enregistrent également un smoke test GUI sous Xvfb. Les tests établissent les contrats des chemins exécutés ; ils ne démontrent pas à eux seuls une compétence linguistique générale.

## 10. Résultats expérimentaux et leur interprétation

### 10.1 Checkpoint et séparation des données

- Train : 13 documents, 1 903 tokens.
- Vocabulaire : 709 unités.
- Validation : 243 positions ; 84 OOV dans l'échantillon de calibration.
- Calibration : 40 itérations ; NLL validation de 15,0108 à 14,5203 nats/token.
- Checkpoint final : 2 526 102 octets ; SHA-256 `49d48a48c4a86eca75916c0e7d02c087f668c3ff95df874e2ec6a347b6ad9905`.

### 10.2 Holdout interne de démonstration

Sur 248 positions du split test :

| Mesure | Résultat |
|---|---:|
| NLL ouverte | 12,5525 nats/token |
| Perplexité | 282 810 |
| Top-1 | 41,13 % |
| Top-5 | 54,84 % |
| OOV | 26,61 % |

**Diagnostic complémentaire par catégorie de tokens, recalculé lors de la revue du paquet :**

| Catégorie | Positions | Top-1 | Top-5 | NLL moyenne |
|---|---:|---:|---:|---:|
| Tokens de contenu (mots/nombres) | 125 | 0,00 % | 12,00 % | 23,3857 |
| Espaces | 108 | 94,44 % | 100,00 % | 1,1875 |
| Ponctuation | 15 | 0,00 % | 86,67 % | 4,1043 |

Cela signifie que le top-1 agrégé de 41,13 % donne une image trop optimiste si on l'interprète comme une prédiction correcte des mots : il est fortement tiré par la prédiction du token espace. Les futures évaluations devraient publier systématiquement les mesures séparées pour espaces, ponctuation et tokens de contenu, ainsi que des métriques par caractère/octets.

### 10.3 MLQA — diagnostic next-token personnalisé

Le test custom a sélectionné 8 paragraphes par langue dans 7 langues, soit 56 paragraphes et 4 581 positions. Les contextes/questions sont concaténés selon le protocole décrit dans le rapport ; cette mesure n'est **pas** la métrique officielle de QA extractif MLQA.

| Mesure | Résultat |
|---|---:|
| NLL moyenne | 17,3065 nats/token |
| Perplexité | 32 818 446 |
| OOV | 49,62 % |
| BYTE seul NLL | 17,4110 |
| Sans BYTE : NLL sur les seuls tokens in-vocabulary | 2,3292 sur 2 307 positions |
| Sans BYTE : positions non couvertes | 2 274 / 4 581 (49,64 %) |
| Baseline unigramme lissée | 5,06545 nats/token (perplexité ≈ 158,45) |

La baseline unigramme est meilleure que le modèle complet sur ce diagnostic : l'écart est de 12,241 nats/token, soit un rapport de perplexité d'environ 207 120. La voie sans BYTE affiche une NLL beaucoup plus basse, mais elle ne couvre qu'environ la moitié des positions ; il serait incorrect de comparer sa NLL conditionnelle aux résultats complets sans mentionner les positions OOV non prises en charge. BYTE procure une couverture ouverte, mais sa probabilité de chaîne est encore peu informative sur ce corpus et son poids COORD est élevé (~51,28 %).

### 10.4 MLQA — QA extractif sur 49 paires de langues

L'évaluation a pris un échantillon déterministe de 50 questions par paire/fichier, soit 2 450 questions au total. Ce n'est pas une évaluation exhaustive de toutes les questions MLQA et ce score n'est pas présenté comme un score leaderboard officiel.

| Portée | EM | F1 | Taux de réponse |
|---|---:|---:|---:|
| 49 paires globales | 0,204 % | 3,084 % | 32,12 % |
| 7 paires diagonales (même langue) | 0,857 % | 10,429 % | 96,00 % |
| 42 paires croisées | 0,095 % | 1,859 % | 21,48 % |

Le taux d'abstention global est de 67,88 % (1 663 questions). La différence entre paires diagonales et croisées suggère que les signaux appris sur le petit corpus ne transfèrent pas efficacement entre langues. Le faible EM/F1 global confirme que la fonction de QA est encore un prototype extractif très limité.

### 10.5 Comparaison v3/v4

Les expériences ont sélectionné les mêmes 56 paragraphes/questions pour v3 et v4. Toutefois, les tokenizers produisent respectivement 4 055 et 4 581 positions. Les unités cibles et les dénominateurs NLL ne sont donc pas identiques. Les NLL v3/v4 ne constituent **pas** une comparaison directe valide ; il faut un protocole avec tokenizer commun, même séquence cible ou une métrique de vraisemblance normalisée en octets/caractères.

## 11. Analyse critique : forces, faiblesses et prochaines étapes

### Forces constatées

1. Le contrat « sondes explicites uniquement » est réellement représenté dans le runtime audité : compteurs, signatures, profils sparse, index et poids scalaires.
2. Les familles sont observables et inspectables ; l'apport et la couverture peuvent être mesurés séparément.
3. Le pipeline de checkpoint est traçable : sauvegardes avant opérations, sérialisation atomique, sidecars SHA-256 et snapshots.
4. Le runtime n'exige pas de dépendance Python tierce ; le même lecteur multi-format alimente train, validation et test.
5. Le paquet d'audit garde les résultats faibles, les incidents corrigés et les réserves au lieu de les cacher.

### Faiblesses mesurées ou structurelles

1. **Échelle de données :** 1 903 tokens d'entraînement sont insuffisants pour conclure à une compétence généraliste et rendent la calibration sur 243 positions fragile.
2. **NLL et OOV :** la NLL MLQA de 17,3065 et la perplexité de 32,8 millions sont très défavorables face à la baseline unigramme de 5,06545 nats/token ; presque la moitié des tokens sont OOV.
3. **Métriques de tokens :** les espaces et la ponctuation gonflent le top-1/top-5 agrégé. Le top-1 des tokens de contenu est nul sur le holdout interne.
4. **BYTE non conditionnel :** BYTE modélise la chaîne du token via un Markov d'octets, mais ne conditionne pas réellement la forme sur le contexte linguistique antérieur.
5. **Redondance REL/RETR :** les tables prédictives utilisent des signatures recent-term pratiquement identiques ; le signal prédictif est donc dupliqué.
6. **Portée de la sémantique :** SEM détecte des cooccurrences ; les autres familles ne constituent pas encore une analyse syntaxique, une résolution d'entités ou un raisonnement relationnel composé.
7. **Formalisme/runtime :** plusieurs fonctions théoriques (coréférence, relations composées, slots syntaxiques, trajectoires/quotients) ne sont pas matérialisées dans le code courant.
8. **QA :** la sélection de spans est heuristique et lexicale ; le score F1 MLQA est de 3,084 % seulement.
9. **Mesures opérationnelles :** la livraison n'établit pas encore les coûts mémoire/latence à grande échelle, sur de gros corpus multilingues.

### Axes de travail recommandés, sans abandonner l'identité eSonde

1. Conserver l'architecture sans neurones et faire évoluer les sondes par opérateurs vérifiables, pas par remplacement MLP/Transformer.
2. Définir pour chaque sonde sa représentation mathématique, son support, son coût, ses règles de mise à jour, sa calibration et ses preuves de provenance ; séparer explicitement les fonctions implémentées des extensions de recherche.
3. Faire de BYTE un mécanisme contextuel si les expériences le justifient : par exemple, conditionner les transitions de bytes à des signatures de contexte ou à des classes de forme, puis mesurer son apport OOV sans sacrifier les tokens connus.
4. Dédupliquer le signal prédictif REL/RETR ou donner à REL une vraie extraction de relations avec vérificateurs et témoins ; garder retrieval comme moteur documentaire distinct.
5. Implémenter progressivement les cadres SLOT, les entités/coréférences DISC et les trajectoires TRACE décrits dans le formalisme, chacun avec tests isolés et benchmarks.
6. Augmenter le corpus de façon substantielle et représentative, avec données autorisées, splits au niveau document/source et validation multilingue indépendante.
7. Refaire les comparaisons avec tokenisation contrôlée, baseline unigramme, n-gram, byte-level et retrieval-only ; publier les métriques par contenu/espaces/ponctuation, langue, domaine et OOV.
8. Évaluer la QA avec un protocole exhaustif ou un échantillon préenregistré plus large, des contrôles de citations et une comparaison retrieval/extractive stricte.
9. Publier les ablations appariées, intervalles d'incertitude, consommation mémoire, latence, taille du checkpoint et comportement sur données hors domaine.

## 12. Sécurité des données et exploitation

Le checkpoint contient les compteurs, les index et les textes des documents ingérés pour permettre la recherche et la traçabilité. Il peut donc contenir des données confidentielles. Ne pas distribuer un checkpoint entraîné sur des documents privés sans contrôler les obligations de confidentialité et de conservation. Le SHA-256 garantit l'intégrité des octets, pas la confidentialité ni l'authenticité d'un auteur.

Les opérations du modèle peuvent écrire une sauvegarde dans `.esonde_backups/`. Prévoir un espace disque suffisant et des sauvegardes externes. Les fichiers ZIP de corpus sont contrôlés CRC et les chemins dangereux sont refusés ; ce contrôle ne constitue pas une protection complète contre toutes les archives malveillantes ou les ZIP bombs. N'ingérer que des archives provenant de sources fiables.

## 13. Arborescence des paquets

```text
Dmodel_eSonde_v4/
  README.md
  esonde.py
  src/esonde_v4/          # moteur, sondes, tokenizer, corpus, sérialisation
  gui/                    # GUI Tkinter
  models/                 # checkpoint v4 + sauvegardes
  examples/demo_corpus/   # train / validation / test séparés
  tests/                  # tests unitaires et intégration
  formalism/              # formalisme TeX
  docs/                   # architecture et guides d'exploitation
  scripts/                # audits et vérifications

Amodel_eSonde_v4/
  formalism/              # formalisme
  docs/                   # audits et rapports complets
  logs/                   # journaux d'exécution
  results/                # métriques et audits JSON
  provenance/             # poids historiques v2/v3 et preuves de hash
  scripts/                # reproduction des évaluations/audits

suivi_model_eSonde_v4/
  checklists/             # checklist travail et incidents
  chemins_eSonde_v4.json
  preuves_eSonde_v4.json
  sav_eSonde_v4/          # snapshots, manifestes et checkpoints sauvegardés
  tools/                  # préflight, savepoint, reassembly
```

## 14. Références internes

- `formalism/formalisme_eSonde_v4.tex` : spécification mathématique, algorithmique et opérationnelle.
- `docs/ARCHITECTURE.md` : architecture réellement câblée.
- `docs/CLI_GUIDE.md`, `docs/GUI_GUIDE.md`, `docs/API_GUIDE.md` : modes d'utilisation.
- `docs/RAPPORT_P6_EVALUATION.md` : métriques internes et MLQA.
- `docs/RAPPORT_P7_AUDIT_FINAL.md` : audits statiques/dynamiques et tests.
- `docs/RAPPORT_P8_LIVRAISON.md` : packaging et intégrité.
- `Amodel_eSonde_v4/docs/RAPPORT_AUDIT_SOURCES.md` : périmètre et réserves de provenance des sources.
- `Amodel_eSonde_v4/docs/RAPPORT_AUDIT_EXPERIENCES.md` : expériences EX4–EX11 et résultats historiques v0–v3.

---

# PART II — ENGLISH

## 1. Overview and concise assessment

eSonde v4 is a discrete-probe statistical language model combined with document retrieval and extractive question-answering functions. It learns sequence, surface-form, co-occurrence and document patterns as counters and sparse tables. Probe families produce distributions or candidate evidence; COORD combines active families using scalar coefficients calibrated on a validation corpus.

The shipped runtime does not use artificial neurons, MLPs, Transformers, Q/K/V attention, learned dense embeddings or neural frameworks. The audited deployable code relies on the Python standard library, dictionaries/counters, deterministic signatures, a byte Markov model and a document index.

**Technical assessment:** eSonde v4 is a concrete and useful software implementation of the “probes only” direction. Its modular probe families, observability, provenance tracking, verifiable checkpoint serialization, CLI/GUI and multi-format corpus ingestion provide a practical experimental foundation. However, the current results do not establish general-purpose semantic competence or parity/superiority against conventional LLMs. On MLQA, next-token likelihood is substantially worse than a smoothed unigram baseline, and extractive QA scores are low. Several probe names currently represent simpler mechanisms than the richer concepts described in the formal specification. This assessment concerns the shipped code and checkpoint; it is neither a proof of theoretical impossibility nor a prediction about future versions.

## 2. The three deliverables

| Package | Contents | Purpose |
|---|---|---|
| `Dmodel_eSonde_v4.zip` | Runtime, demonstration v4 checkpoint, checkpoint backups, separated train/validation/test examples, CLI, GUI, formal specification, tests and guides | Run and use eSonde v4 |
| `Amodel_eSonde_v4.zip` | Source/experiment audits, formal specification, P0–P8 reports, logs, JSON results, evaluation/audit scripts, v4 checkpoint and historical v2/v3 weights with provenance | Inspect, audit and reproduce experiments |
| `suivi_model_eSonde_v4` | Checklists, paths, proofs, incidents, savepoint/preflight tools and historical snapshots | Traceability and restoration |

### 2.1 Verified integrity

The SHA-256 digests below match the delivered files that were checked:

```text
22022cf589a3645425edb729c7246c4a5dfe0d1ad4b5c832d06e4a38b356e42f  Dmodel_eSonde_v4.zip
d6b0c035c72da54b49f9a80b42699004ced6be54578d476a5e857955253358e0  Amodel_eSonde_v4.zip
4d195e6437006a608dbcbf3e7a98296ada573b1652968c7f68426c0bdfef5745  suivi_model_eSonde_v4.z01
e071433459cd3cbd98893bd328a4446b6409b0277982d0f35ec51272897b982a  suivi_model_eSonde_v4.zip
95671a18e1ce098a14f05ad721dc905cbae69ea4f0c326c5449cfa3fe4138e93  suivi_model_eSonde_v4_assembled.zip
```

| File | Exact size | Verification |
|---|---:|---|
| Dmodel | 5,968,668 bytes | ZIP CRC + 78 payload files in SHA-256 manifest |
| Amodel | 4,585,616 bytes | ZIP CRC + 333 payload files in SHA-256 manifest |
| Suivi `.z01` volume | 110,100,480 bytes | Volume SHA-256 |
| Suivi `.zip` volume | 96,447,915 bytes | Volume SHA-256 |
| Reassembled Suivi | 206,548,391 bytes | ZIP CRC + 9,242 payload files in SHA-256 manifest |

Each Dmodel and Amodel archive contains two manifest metadata files in addition to the payload files counted by its package manifest (`PACKAGE_MANIFEST.json` and `MANIFEST.sha256`). Suivi also contains these two metadata files. The internal manifests were checked file by file; no expected file was missing and no SHA-256 mismatch was found.

**Important — split Suivi archive:** `suivi_model_eSonde_v4.z01` and `suivi_model_eSonde_v4.zip` are two volumes of one Info-ZIP archive. The final `.zip` volume is not a standalone ZIP and must not be tested or extracted by itself. Keep both volumes in the same directory and reassemble them, or use the complete `suivi_model_eSonde_v4_assembled.zip` archive when available.

From the directory containing both volumes:

```bash
python reassembler_suivi_model_eSonde_v4.py \
  --archive suivi_model_eSonde_v4.zip \
  --output suivi_model_eSonde_v4_assembled.zip
```

The script invokes the system Info-ZIP `zip` command (`zip -s 0`), so that command must be installed and available in `PATH`. The verified reassembly was byte-identical to the complete reference archive and had SHA-256 `95671a18...e4138e93`.

### 2.2 Source and data scope

The three packages do not include the raw `eSonde_v3_sources.zip` source archive or the raw MLQA dataset. They contain the reports, hashes, manifests and results needed for auditing. Amodel preserves four historical v2/v3 checkpoint files; all four hashes match their provenance sidecars from the inspected sources.

An audit-scope reservation must remain visible: the P0 report notes that two historical archives referenced by a 34,623-file manifest (`liverables_eSonde_v2.zip` and `last_sources_3.zip`) were not present in the uploaded source archive. Their contents could therefore not be independently re-inspected. This is not a loss that occurred while building v4; those archives were simply absent from the supplied source materials.

## 3. What is a probe in eSonde v4?

A probe is an explicit operator that observes part of the context or memory and consults recorded regularities. Unlike an artificial neuron, it is not a hidden unit whose parameters are learned by backpropagation. In the shipped v4 runtime, the state mainly consists of integer counters, signature-to-target tables, co-occurrence profiles, indexed documents and scalar coefficients.

At each position, the causal context consists of preceding units. Active families build conditional distributions or scores. COORD combines them:

\[
P(y\mid h,M)=\sum_{f\in F(h)}\widetilde{\lambda}_f Q_f(y\mid h,M),\qquad
\widetilde{\lambda}_f=\frac{\lambda_f}{\sum_{g\in F(h)}\lambda_g}.
\]

The \(\lambda_f\) coefficients are non-negative scalar weights normalized on the simplex. Calibration adjusts them on the validation split by exponentiated updates. This optimization uses an analytical derivative over ten scalar mixture weights; it is not backpropagation through a neural network.

### 3.1 The ten families implemented in the runtime

| Family | Actual function in the shipped runtime | What it does not yet mean |
|---|---|---|
| **SEQ** | Counts continuations associated with normalized suffixes of the previous 1–8 units. | It is not yet a complete syntactic or discourse model. |
| **SKIP** | Counts continuations associated with units at offsets 1, 2, 3, 5 and 8. | It does not perform arbitrary long-range dependency inference. |
| **MORPH** | Uses the previous token's Unicode shape, script, casing, length and 1–4 character prefixes/suffixes. | It does not yet learn complete morphological paradigms or generalized character n-grams. |
| **BYTE** | An order-4 Markov model over UTF-8 bytes, with BOS/EOS and smoothing; it can assign likelihood to out-of-vocabulary strings. | In this version it is essentially a token-form prior: its probability does not directly depend on the preceding linguistic context. It therefore does not infer the meaning of an OOV word from its sentence. |
| **SEM** | Sparse term co-occurrence profiles in a local window of four content terms and cosine similarity between profiles. | It is not a dense embedding, universal concept graph or deep compositional understanding. |
| **REL** | Continuation counters indexed by the last content term, last pair and last triple. | It does not yet build typed A–relation–B propositions or composition rules. |
| **SLOT** | Continuation counters indexed by the shapes of the previous 1–4 units. | It is not yet a grammar, syntactic parser or syntactic slot-filling system. |
| **DISC** | Summarizes the most frequent content terms in the previous 100 content terms, retaining up to 12 topics. | It does not yet resolve coreference, aliases, entity mentions or discourse roles. |
| **RETR** | Provides predictive signatures over recent terms and a sparse document index with BM25-like scoring. | Its predictive part is currently redundant with REL for the unary/binary/ternary signatures; document retrieval remains a separate function. |
| **TRACE** | Computes SHA-256 fingerprints of contexts at depths 2, 4 and 6 and associates observed continuations. | It does not yet implement state trajectories, observational quotients or formal refinement as described in the richer formal specification. |

**COORD** is not an eleventh predictive probe; it is the combination mechanism for the ten families.

### 3.2 An important architecture nuance

The `formalisme_eSonde_v4.tex` document contains goals richer than the shipped code: relational composition, left/right syntactic frames, mention and coreference memory, trajectories and observational refinement. The document is a normative research direction and a set of criteria; these functions must not be described as already implemented when the runtime currently contains only a reduced version. The accurate status is therefore: ten probe/count-table operators exist and are tested, but several theoretical constructions remain to be developed.

A second concrete observation is that REL and predictive RETR use the same recent lexical contexts (one term, a pair and a triple), with different signature labels. On the shipped checkpoint, their NLL and support statistics are identical in the evaluation tables. A next development cycle should deduplicate their predictive signal or give REL a genuine compositional relational structure.

## 4. Training, calibration and inference

### 4.1 Training

1. The reader resolves an individual file, a recursive directory or a corpus ZIP archive.
2. It extracts text, keeps source identifiers and applies format-specific cleanup.
3. The tokenizer segments the text into Unicode surface units; whitespace and punctuation are also tokens.
4. Each target is associated with the preceding context in the same document and updates probe counters.
5. SEM builds distributional co-occurrence profiles in parallel.
6. RETR stores documents and term bags for search.
7. The JSON checkpoint is written atomically with a SHA-256 sidecar; the relevant CLI operations create a backup first.

The shipped model was trained on **13 documents and 1,903 tokens**, with a vocabulary of **709 units**. This is a very small demonstration corpus for language learning. Validation contains **243 positions**; the internal test contains **248 positions** after the actual corpus reader processes it.

### 4.2 COORD calibration

The model was calibrated on the 243 validation positions, using 40 iterations and a learning rate of 0.08. Mean validation NLL decreased from 15.0108 to 14.5203 nats/token on this small sample. The resulting BYTE weight is approximately 0.5128; the remaining weights are distributed across SEQ, SKIP, MORPH, SEM, REL, SLOT, DISC, RETR and TRACE.

For open-string likelihood, non-BYTE families are categorical over the training vocabulary fixed by training; BYTE scores the complete UTF-8 sequence followed by EOS. A validation/test target is not artificially inserted into the vocabulary. This is preferable to an evaluation that inserts the answer into the candidate list.

### 4.3 Prediction and generation

The model can rank candidate units and produce an autoregressive continuation. Exposed strategies are greedy, sampling, top-k and nucleus. Candidates come from the training vocabulary, explicitly supplied candidates and a BYTE beam that proposes valid UTF-8 strings.

This is local statistical generation. The existence of a `generate` command does not mean that the system can follow complex instructions, reason through multiple steps or produce reliable answers like a modern LLM.

### 4.4 Search and QA

- `search` ranks learned documents using BM25-like lexical scoring and may expand terms using SEM neighbors.
- `ask` retrieves documents and returns an evidence sentence when lexical overlap is available.
- `answer` receives an explicit context and tries to extract a short contiguous span with offsets and provenance.

These are document retrieval and heuristic extraction functions, not free-form answer generation. The system can abstain when support is absent. Abstention should not be confused with deep semantic understanding.

## 5. Supported file formats

The `python esonde.py formats` command lists 24 file extensions, plus ZIP corpus archives:

- Text and markup: `.txt`, `.md`, `.rst`, `.text`, `.log`, `.org`, `.tex`, `.rtf`.
- Web/XML: `.html`, `.htm`, `.xhtml`, `.xml`.
- Structured data: `.json`, `.jsonl`, `.csv`, `.tsv`.
- Email and documents: `.eml`, `.docx`, `.pptx`, `.xlsx`, `.odt`, `.ods`, `.odp`, `.epub`.
- Container: `.zip`, containing one level of supported files.

The same reader is shared by `train`, `calibrate` and `evaluate`. PDF files, legacy binary Office files `.doc`, `.xls`, `.ppt` and unlisted formats are explicitly rejected. Convert them to a supported format before ingestion. Modern Office files are extracted from their XML parts; this is not a complete semantic rendering of every layout or embedded object.

The runtime does not automatically split train/validation/test. Users must provide separate directories and must not train on a parent directory that also includes validation or test data.

## 6. Installation and requirements

- CPython **3.10 or newer**.
- No third-party Python packages are required for the runtime; Python standard library only.
- GUI: `tkinter` / Tk-Tcl must be available. On Linux, the system Tk package may need to be installed separately.
- Windows, Linux and macOS with a compatible Python release.

Dmodel is self-contained with respect to third-party Python libraries; it is not a native executable that embeds Python. Python must be installed before running it.

### Extract

Extract `Dmodel_eSonde_v4.zip`. Run all commands below from the `Dmodel_eSonde_v4/` directory.

### Initial checks

```bash
python --version
python esonde.py --help
python esonde.py formats
python esonde.py verify --model models/esonde_v4_checkpoint.json
python scripts/check_runtime.py
```

The supplied checkpoint is already trained and calibrated. Do not run `init --force` against it without preserving a copy. To start a fresh experiment, choose a new model path.

## 7. Complete CLI guide

### 7.1 Initialize a new checkpoint

```bash
python esonde.py init --model models/my_experiment.json
```

### 7.2 Train on a corpus

```bash
python esonde.py train \
  --model models/my_experiment.json \
  --corpus examples/demo_corpus/train \
  --batch-id my-batch-001
```

`--corpus` may point to a supported file, a directory or a ZIP. Training is incremental; documents not already present are added according to their source+text identifier.

### 7.3 Calibrate on validation

```bash
python esonde.py calibrate \
  --model models/my_experiment.json \
  --validation examples/demo_corpus/validation \
  --epochs 40 \
  --max-positions 5000
```

Calibration changes COORD weights. It must only use the validation split, never the test split.

### 7.4 Verify and inspect the model

```bash
python esonde.py verify --model models/my_experiment.json
python esonde.py info --model models/my_experiment.json
python esonde.py audit --model models/my_experiment.json
```

`verify` checks the checkpoint and its digest. `info` displays state sizes and COORD weights. `audit` inspects runtime imports and the checkpoint against the delivered purity rules.

### 7.5 Predict and generate

```bash
python esonde.py predict \
  --model models/my_experiment.json \
  --context "The probes observe" \
  --top-k 12

python esonde.py generate \
  --model models/my_experiment.json \
  --prompt "The probes observe" \
  --strategy nucleus \
  --top-p 0.92 \
  --temperature 0.8 \
  --max-new-tokens 50
```

Available strategies: `greedy`, `sample`, `top_k` and `nucleus`. The generation seed is configurable through `--seed`.

### 7.6 Search and ask a question

```bash
python esonde.py search \
  --model models/my_experiment.json \
  --query "sparse document index" \
  --top-k 5

python esonde.py ask \
  --model models/my_experiment.json \
  --question "What is a hash function?"
```

`ask` queries documents already ingested into the model.

### 7.7 Answer from a supplied context

Provide exactly one of `--context` or `--context-file`:

```bash
python esonde.py answer \
  --model models/my_experiment.json \
  --question "What can a checksum detect?" \
  --context-file examples/demo_corpus/test/01_test.txt
```

### 7.8 Evaluate on an independent test split

```bash
python esonde.py evaluate \
  --model models/my_experiment.json \
  --corpus examples/demo_corpus/test \
  --max-positions 5000
```

Top-k ranking is over the fixed training vocabulary. Open NLL can score an OOV target through BYTE. Read coverage and OOV rates carefully; top-k alone is not a complete measure of language quality.

### 7.9 Backups

CLI model operations create a pre-execution backup in `.esonde_backups/` next to the checkpoint and verify its SHA-256 before the operation. Checkpoint mutations use atomic writes and a SHA-256 sidecar. Keep an external backup of `models/` and `.esonde_backups/` regularly.

## 8. GUI guide

Launch from the Dmodel root:

```bash
python gui/esonde_gui.py
```

Or use the included launchers:

- Windows: `RUN_GUI.bat` and `RUN_CLI.bat`.
- Linux/macOS: `./RUN_GUI.sh` and `./RUN_CLI.sh` (make scripts executable if needed: `chmod +x RUN_GUI.sh RUN_CLI.sh`).

The Tkinter GUI lets users choose a checkpoint, select a file/directory/ZIP as a corpus, select a context file for `answer`, and invoke train, calibrate, evaluate, predict, generate, search, ask, answer, info, verify and audit. It delegates to the shared CLI; it does not contain a second generation engine. A thread-safe queue relays worker output to the main Tk thread.

For control and button details, see `docs/GUI_GUIDE.md` and `docs/GUIDE_UTILISATION_CLI_GUI.md`. A graphical display is required for the GUI; the CLI works without a desktop environment.

## 9. Tests and software reproduction

From the Dmodel root:

```bash
python -m compileall -q src gui scripts
PYTHONPATH=src python -m unittest discover -s tests -v
python scripts/check_tex_structure.py formalism/formalisme_eSonde_v4.tex
python esonde.py verify --model models/esonde_v4_checkpoint.json
```

In Windows PowerShell, set the module path temporarily before running tests:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

The delivered revision passed **26/26 tests** in a fresh Dmodel extraction, as well as `compileall`, CLI help, the format listing and checkpoint verification. The reports also record a GUI smoke test under Xvfb. Tests establish the contracts of the paths executed; they do not by themselves demonstrate general language competence.

## 10. Experimental results and interpretation

### 10.1 Checkpoint and data separation

- Training: 13 documents, 1,903 tokens.
- Vocabulary: 709 units.
- Validation: 243 positions; 84 OOV positions in the calibration sample.
- Calibration: 40 iterations; validation NLL from 15.0108 to 14.5203 nats/token.
- Final checkpoint: 2,526,102 bytes; SHA-256 `49d48a48c4a86eca75916c0e7d02c087f668c3ff95df874e2ec6a347b6ad9905`.

### 10.2 Internal demonstration holdout

On 248 test positions:

| Metric | Result |
|---|---:|
| Open NLL | 12.5525 nats/token |
| Perplexity | 282,810 |
| Top-1 | 41.13% |
| Top-5 | 54.84% |
| OOV | 26.61% |

**Supplementary token-category diagnostic, recomputed during package review:**

| Category | Positions | Top-1 | Top-5 | Mean NLL |
|---|---:|---:|---:|---:|
| Content tokens (words/numbers) | 125 | 0.00% | 12.00% | 23.3857 |
| Whitespace | 108 | 94.44% | 100.00% | 1.1875 |
| Punctuation | 15 | 0.00% | 86.67% | 4.1043 |

The aggregate top-1 of 41.13% gives an overly optimistic impression if interpreted as correct word prediction: it is heavily driven by prediction of the whitespace token. Future evaluations should always publish separate whitespace, punctuation and content-token results, as well as character/byte-level metrics.

### 10.3 MLQA — custom next-token diagnostic

The custom test selected 8 paragraphs per language in 7 languages, totalling 56 paragraphs and 4,581 positions. Contexts/questions are concatenated as described in the report; this is **not** the official MLQA extractive QA metric.

| Metric | Result |
|---|---:|
| Mean NLL | 17.3065 nats/token |
| Perplexity | 32,818,446 |
| OOV | 49.62% |
| BYTE-only NLL | 17.4110 |
| Without BYTE: NLL on in-vocabulary tokens only | 2.3292 over 2,307 positions |
| Without BYTE: unsupported positions | 2,274 / 4,581 (49.64%) |
| Smoothed unigram baseline | 5.06545 nats/token (perplexity ≈ 158.45) |

The smoothed unigram baseline outperforms the full model on this diagnostic: the gap is 12.241 nats/token, or a perplexity ratio of approximately 207,120. The no-BYTE path has a much lower NLL but only covers about half the positions; it would be misleading to compare that conditional NLL with the full model without reporting unsupported OOV positions. BYTE provides open-vocabulary coverage, but its string probabilities are still uninformative on much of this corpus and its COORD weight is high (~51.28%).

### 10.4 MLQA — extractive QA on 49 language pairs

The evaluation used a deterministic sample of 50 questions per pair/file, or 2,450 questions total. It is not an exhaustive evaluation of all MLQA questions and is not presented as an official leaderboard result.

| Scope | EM | F1 | Answer rate |
|---|---:|---:|---:|
| All 49 pairs | 0.204% | 3.084% | 32.12% |
| 7 diagonal pairs (same language) | 0.857% | 10.429% | 96.00% |
| 42 cross-language pairs | 0.095% | 1.859% | 21.48% |

The overall abstention rate is 67.88% (1,663 questions). The diagonal/cross-language gap suggests the signals learned from the small corpus do not transfer effectively across languages. The low global EM/F1 confirms that the current QA function is a very limited extractive prototype.

### 10.5 v3/v4 comparison

The experiments selected the same 56 paragraphs/questions for v3 and v4. However, the tokenizers produced 4,055 and 4,581 positions respectively. The target units and NLL denominators therefore differ. The v3/v4 NLL values are **not a valid direct comparison**; a common-tokenizer protocol, identical target sequence or byte/character-normalized likelihood is needed.

## 11. Critical analysis: strengths, weaknesses and next steps

### Observed strengths

1. The “explicit probes only” contract is actually represented in the audited runtime: counters, signatures, sparse profiles, indexes and scalar weights.
2. Probe families are observable and inspectable; their contribution and coverage can be measured separately.
3. Checkpoint handling is traceable: pre-operation backups, atomic serialization, SHA-256 sidecars and snapshots.
4. The runtime needs no third-party Python dependency; the same multi-format reader feeds training, validation and testing.
5. The audit package preserves weak results, corrected incidents and reservations rather than hiding them.

### Measured or structural weaknesses

1. **Data scale:** 1,903 training tokens are insufficient to establish general competence and make calibration on 243 positions fragile.
2. **NLL and OOV:** MLQA NLL of 17.3065 and perplexity of 32.8 million are very poor relative to the 5.06545-nat smoothed unigram baseline; almost half the tokens are OOV.
3. **Token metrics:** whitespace and punctuation inflate aggregate top-1/top-5. Content-token top-1 is zero on the internal holdout.
4. **Unconditional BYTE:** BYTE models token strings through a byte Markov chain but does not truly condition token form on preceding linguistic context.
5. **REL/RETR redundancy:** predictive tables use practically identical recent-term signatures; the predictive signal is duplicated.
6. **Semantic scope:** SEM detects co-occurrences; other families do not yet implement syntactic parsing, entity resolution or compositional relational reasoning.
7. **Formalism/runtime gap:** several theoretical functions (coreference, composed relations, syntactic slots, trajectories/quotients) are not materialized in current code.
8. **QA:** span selection is heuristic and lexical; MLQA F1 is only 3.084%.
9. **Operational measurements:** large-scale memory/latency costs have not yet been established on large multilingual corpora.

### Recommended development directions while preserving eSonde's identity

1. Preserve the non-neural architecture and evolve probes through verifiable operators rather than replacing them with MLPs/Transformers.
2. Define each probe's mathematical representation, support, cost, update rules, calibration and provenance; clearly separate implemented functions from research extensions.
3. Make BYTE context-sensitive if experiments support it: for example, condition byte transitions on context signatures or shape classes, then measure OOV gains without sacrificing known-token likelihood.
4. Deduplicate REL/RETR predictive signals or give REL a genuine relation-extraction mechanism with verifiers and witnesses; keep document retrieval as a separate engine.
5. Progressively implement the SLOT frames, DISC entity/coreference memory and TRACE trajectories described in the formal specification, each with isolated tests and benchmarks.
6. Increase corpus size substantially with representative, permitted data, document/source-level splits and independent multilingual validation.
7. Re-run comparisons with controlled tokenization, unigram, n-gram, byte-level and retrieval-only baselines; publish metrics by content/whitespace/punctuation, language, domain and OOV.
8. Evaluate QA with exhaustive or larger pre-registered samples, citation checks and strict retrieval/extractive baselines.
9. Publish paired ablations, uncertainty intervals, memory use, latency, checkpoint size and out-of-domain behaviour.

## 12. Data security and operations

The checkpoint stores counters, indexes and ingested document texts for retrieval and traceability. It may therefore contain confidential data. Do not distribute a checkpoint trained on private documents without reviewing confidentiality and retention requirements. SHA-256 verifies byte integrity, not confidentiality or author authenticity.

Model operations may write backups to `.esonde_backups/`. Provide sufficient disk space and keep external backups. Corpus ZIP files are CRC-checked and dangerous paths are rejected; this is not comprehensive protection against every malicious archive or ZIP bomb. Ingest only archives from trusted sources.

## 13. Package layouts

```text
Dmodel_eSonde_v4/
  README.md
  esonde.py
  src/esonde_v4/          # engine, probes, tokenizer, corpus, serialization
  gui/                    # Tkinter GUI
  models/                 # v4 checkpoint and backups
  examples/demo_corpus/   # separated train / validation / test
  tests/                  # unit and integration tests
  formalism/              # TeX formal specification
  docs/                   # architecture and operational guides
  scripts/                # local audits and checks

Amodel_eSonde_v4/
  formalism/              # formal specification
  docs/                   # audits and detailed reports
  logs/                   # execution logs
  results/                # metrics and audit JSON
  provenance/             # historical v2/v3 weights and hash evidence
  scripts/                # evaluation and audit reproduction

suivi_model_eSonde_v4/
  checklists/             # work and incident checklists
  chemins_eSonde_v4.json
  preuves_eSonde_v4.json
  sav_eSonde_v4/          # snapshots, manifests and backed-up checkpoints
  tools/                  # preflight, savepoint and reassembly tools
```

## 14. Internal references

- `formalism/formalisme_eSonde_v4.tex`: mathematical, algorithmic and operational specification.
- `docs/ARCHITECTURE.md`: architecture actually wired into the runtime.
- `docs/CLI_GUIDE.md`, `docs/GUI_GUIDE.md`, `docs/API_GUIDE.md`: usage modes.
- `docs/RAPPORT_P6_EVALUATION.md`: internal and MLQA metrics.
- `docs/RAPPORT_P7_AUDIT_FINAL.md`: static/dynamic audits and tests.
- `docs/RAPPORT_P8_LIVRAISON.md`: packaging and integrity.
- `Amodel_eSonde_v4/docs/RAPPORT_AUDIT_SOURCES.md`: source scope and provenance reservations.
- `Amodel_eSonde_v4/docs/RAPPORT_AUDIT_EXPERIENCES.md`: EX4–EX11 and historical v0–v3 results.

---

**End of README. / Fin du README.**
