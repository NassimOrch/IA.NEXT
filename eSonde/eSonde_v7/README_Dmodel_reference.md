# eSonde v7 — runtime expérimental de dialogue

**Version :** 7.0.0-experimental  
**Fonction utilisateur :** chat/dialogue uniquement  
**Checkpoint :** poids eSonde v6 d'origine, en lecture seule  
**État :** prototype implémenté ; validation conversationnelle sur corpus à poursuivre.

## 1. Ce que fait cette version

eSonde v7 transforme un historique courant facultatif et un prompt en une réponse générée token par token. Il reconstruit un contexte de dialogue local, extrait seize observations par candidat, donne à chaque Obsiss une perspective complète et individualisée sur ces observations, puis utilise les voix individuelles pour classer les continuations.

La population active commence à dix Obsiss. Elle augmente seulement lorsque les critères déclarés de dynamique et de stabilité décisionnelle ne sont pas satisfaits. Le million présent dans le checkpoint est la population maximale disponible, pas une cible obligatoire. Un essai peut donc s'arrêter à dix si les tests réels de cet essai sont satisfaits.

La non-réponse est désactivée par défaut. Le runtime doit générer la meilleure continuation technique disponible ; une abstention n'est possible que par activation volontaire de l'option correspondante.

## 2. Architecture en bref

1. **Contexte de dialogue** : occurrences typées par tour, rôle et position ; liens d'ordre, de succession de tours et de récurrence lexicale ; provenance conservée ; pas de mémoire conversationnelle persistante.
2. **Espace d'observations** : 16 canaux explicites alignés sur les 16 dimensions historiques du checkpoint. Chaque canal mesure un signal particulier, sans prétendre être un sens complet.
3. **Voix des Obsiss** : chaque Obsiss conserve son identité de ligne et combine ses poids d'origine avec son état P propre et une observation croisée. Elle voit les 16 canaux, pas seulement une famille/coordonnée primaire.
4. **Décision collective P/R** : chaque candidat reçoit une activation R propre, conditionnée par le P du préfixe courant et appariée à la même ligne d'Obsiss. Chaque voix combine le rang de ses 16 observations et le rang de sa cohérence P/R. Médiane, IQR et stabilité LOO/partitions conservent l'accord et le désaccord ; les empreintes permettent de recalculer les états sans sérialiser toutes les valeurs.
5. **Génération** : candidats issus des statistiques TRAIN v6 (transitions n-grammes, associations PPMI et retour caractère-trigramme pour formes OOV), classés au moment de chaque continuation du beam.
6. **Convergence** : vérification distincte du point fixe P (absence exacte d'arêtes actives ou répétition SHA-256 d'état de période 1, explicitement qualifiée), de la stabilité des décisions fondées sur les voix P/R et du diagnostic R final. L'atteinte de la limite de longueur de trajectoire n'est pas appelée convergence.

## 3. Fichiers et répertoires

```text
Dmodel_eSonde_v7/
  RUN_CLI.py, RUN_GUI.py, RUN_CLI.sh, RUN_GUI.sh, *.bat
  src/esonde_v6/          opérateurs et modèle source v6 conservés
  src/esonde_v7/          runtime chat et opérateurs v7
  models/eSonde_v6/       poids, métadonnées et statistiques d'origine
  models/eSonde_v7/       configuration de l'architecture v7
  formalism/              formalisme, laboratoire, optimisation technique
  docs/                   architecture, guides CLI/GUI, intégrité, évaluation
  tests/                  tests unitaires ciblés
  runs_v7/                résultats et traces locaux
  control/                checklists, registre des chemins et savepoints en paquet autonome
```

Le dossier `control/` est embarqué dans la livraison Dmodel. En développement, il peut rester frère du runtime. Le CLI détecte les deux structures.

## 4. Installation et prérequis

- Windows 10/11, macOS ou Linux x86-64/ARM64 avec Python 3.10 ou supérieur.
- Le mode de base utilise les bibliothèques standard Python ; aucune installation de poids ou service réseau n'est requise.
- NumPy est facultatif mais recommandé pour accélérer les calculs vectorisés. Sans NumPy, le chemin scalaire de repli est utilisé.
- Tkinter est nécessaire seulement pour la GUI. S'il n'est pas présent dans la distribution Python, utiliser le CLI.

Vérification :

```bash
python --version
python -c "import numpy; print(numpy.__version__)"  # facultatif
python -c "import tkinter; print('Tk OK')"          # GUI seulement
```

Windows peut utiliser `py -3` à la place de `python`.

## 5. Démarrage CLI

Depuis le répertoire du paquet :

```bash
python RUN_CLI.py --help
python RUN_CLI.py verify
python RUN_CLI.py status
python RUN_CLI.py chat --prompt "Bonjour. Présente-toi en une phrase."
```

Le chat démarre à 10 Obsiss puis augmente la population si les critères ne sont pas satisfaits. Pour tester strictement dix lignes, sans autoriser de croissance :

```bash
python RUN_CLI.py chat --prompt "Bonjour" --min-obsiss 10 --n-obsiss 10 --json-out runs_v7/chat_10.json
```

L'option `--n-obsiss` est un plafond pour l'essai. L'absence de cette option laisse la population disponible du checkpoint comme maximum. Pour un historique, fournir un JSON contenant un tableau ordonné d'objets `speaker/text` :

```json
[
  {"speaker": "user", "text": "Je prépare un voyage."},
  {"speaker": "assistant", "text": "Quel type de voyage ?"}
]
```

```bash
python RUN_CLI.py chat --prompt "Plutôt culturel." --history-file history.json
```

Détails complets : `docs/CLI_GUIDE.md`.

## 6. Démarrage GUI

```bash
python RUN_GUI.py
```

Linux/macOS : `./RUN_GUI.sh`. Windows : `RUN_GUI.bat`. La GUI n'offre que le dialogue. L'historique est maintenu dans la session de la fenêtre. Détails : `docs/GUI_GUIDE.md`.

## 7. Contrôles, sauvegardes et sorties

Avant chaque exécution du modèle, le préflight lit les chemins, la checklist de travail, les deux checklists d'incidents, le pointeur de sauvegarde et le manifeste de snapshot. Il vérifie le hash du checkpoint. Après une génération ou une erreur, il enregistre le résultat ou l'incident et tente un snapshot post-exécution.

Fichiers de contrôle :

- `control/suivi_model_eSonde_v7/chemins_eSonde_v7.json`
- `control/suivi_model_eSonde_v7/checklist_de_travail_eSonde_v7.json`
- `control/suivi_model_eSonde_v7/checklist_erreurs_no_model.json`
- `control/suivi_model_eSonde_v7/checklist_erreurs_model.json`
- `control/suivi_model_eSonde_v7/preuves_eSonde_v7.json`
- `control/suivi_model_eSonde_v7/sav_eSonde_v7_reference.json`

Les résultats et traces de dialogue sont écrits sous `runs_v7/`. Ils peuvent contenir des informations sensibles.

## 8. Intégrité du checkpoint

Le fichier original `models/eSonde_v6/weights.bin` doit rester à 64 000 000 octets et porter le SHA-256 suivant :

`8526943d1528418fa8bbbf9128b61b5e1acd90a16eeb7cc062e18864b083dff4`

```bash
python RUN_CLI.py verify --json-out runs_v7/verify.json
```

Ce contrôle atteste uniquement l'identité du fichier, pas la qualité du modèle.

## 9. Tests logiciels

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

Les tests synthétiques couvrent les invariants du runtime, la parité du premier état P/R avec v6 sur fixtures, le plafonnement de population et les mécanismes d'observation. Ils ne sont pas des évaluations humaines de dialogue.

## 10. Ce qui est établi et ce qui reste à mesurer

Le prototype possède un pipeline de chat exécuté localement, une représentation transitoire du contexte, un vote Obsiss individuel sur seize observations, un contrôle de convergence explicite et les instruments de sauvegarde/audit. Cela ne signifie pas que la cohérence conversationnelle générale est déjà démontrée.

Les propositions lexicales reposent encore sur les statistiques TRAIN du checkpoint v6 et le retour caractère. Les Obsiss interviennent réellement dans la sélection via les votes à 16 observations et la cohérence P/R par candidat ; néanmoins, les canaux de polarité, temporalité et modalité restent des observables explicites, pas une compréhension complète de leur portée. Il faut mesurer, sur corpus disjoint et jugement aveugle : cohérence multi-tours, pertinence, contradictions, suivi des consignes, robustesse interlangue, généralisation et comparaison équitable avec les LLM. Aucun classement de supériorité n'est inféré des scores internes.

## 11. Documents de référence

- `formalism/formalisme_eSonde_v7.tex` et `formalism/formalise_eSonde_v7.tex` : architecture et formalisme complet.
- `formalism/laboratoire_eSonde_v7.tex` : décisions architecturales, fiches d'expérience et résultats.
- `formalism/tech_opt_eSonde_v7.tex` : optimisation de calcul et de déploiement.
- `docs/ARCHITECTURE.md` : pipeline et mécanismes.
- `docs/EVALUATION_PROTOCOL.md` : protocole d'évaluation.
- `docs/REPORT_TEMPLATE.md` : format unique des rapports en neuf rubriques.
- `docs/PROVENANCE_AND_INTEGRITY.md` : contrôle des poids et provenances.
