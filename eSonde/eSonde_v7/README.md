
# eSonde v7 — Experimental Dialogue Runtime

**Runtime version:** 7.0.0-experimental  
**Public function:** chat prompt/response with optional current dialogue history  
**Checkpoint:** original eSonde v6 checkpoint, 1,000,000 Obsiss, dimension 16  
**Weights:** `models/eSonde_v6/weights.bin`, 64,000,000 bytes, SHA-256 `8526943d1528418fa8bbbf9128b61b5e1acd90a16eeb7cc062e18864b083dff4`

> The v7 runtime is an experimental dialogue prototype built on the original v6 checkpoint. It implements a token-by-token contextual decoder and cross-voting across 16 Obsiss families. It does not yet claim general conversational competence, equality with, or superiority over LLMs. Its capabilities must be established through independent and comparative testing.

## 1. Functional Scope

The sole user-facing task is chat: a prompt, optionally preceded by `user`/`assistant`/`system` turns, produces a response. The public CLI exposes only `chat`, `status`, and `verify` (the latter two are administrative operations). The GUI provides only a conversation interface. The retained v6 computational modules are internal compatibility components required by the checkpoint; the previous CLI/GUI/evaluation interfaces are not exposed: no translation, infill, classification, search, or separate QA mode.

Non-response is **disabled by default**. The model attempts the best available continuation. The `--allow-no-response` option (CLI) or the GUI checkbox explicitly enables it.

## 2. Architecture Overview

1. **Inherited Checkpoint:** The `weights.bin` weights, linguistic statistics, and training manifest are preserved identically. No v7 training or weight overwriting is claimed.
2. **Transient Context:** Each token occurrence retains its turn, role, and position. Turn-order and succession relationships are typed; no causality is inferred from order alone. The framework is reconstructed from the current conversation and the generated prefix, without a persistent knowledge base.
3. **16-Observation Space:** Local transition, prompt association, dialogue association, lexical recurrence, morphological affinity, response role, discursive continuity, polarity, temporality, boundary, TRAIN support, subword feedback, referential continuity, modality, speaker alignment, and informational novelty.
4. **Obsiss Voices:** Each checkpoint row remains identified by its index. Each Obsiss combines a primary channel `a_i = i mod 16` and a secondary channel `b_i = (7i+3) mod 16`, with a gain derived from its original parameters. The quantiles of each family preserve dispersion instead of masking all voices within an average.
5. **Generation:** Each beam prefix reactivates the context, produces n-gram/PPMI candidates, triggers TRAIN character-level feedback when local lexical support is rare, computes observations, and selects continuations through Obsiss votes. P observes the prompt; R observes the generated response afterward as a complementary diagnostic.

The complete specifications are available in `formalism/formalisme_eSonde_v7.tex`, `formalism/laboratoire_eSonde_v7.tex`, and `formalism/tech_opt_eSonde_v7.tex`.

## 3. Requirements and Installation

- Python 3.10 or later.
- Python standard libraries.
- NumPy is optional and accelerates vectorized calibration. A fallback scalar path is provided.
- Tkinter is required for the GUI; it may be distributed separately in some Linux distributions.
- No model download is required: the weights and statistics are located in `models/eSonde_v6/`.

On a fresh system, check:

```bash
python --version
python -c "import tkinter; print('Tk OK')"   # GUI only
python -c "import numpy; print(numpy.__version__)"  # optional acceleration
```

The portable distribution folder may contain `control/suivi_model_eSonde_v7/` and `control/sav_eSonde_v7/` alongside the runtime so that an independently extracted Dmodel includes its checklists and initial snapshot. In the development directory structure, these elements are sibling folders of Dmodel. The CLI detects both layouts.

## 4. Quick Start — CLI

From the package root directory:

```bash
python RUN_CLI.py --help
python RUN_CLI.py verify
python RUN_CLI.py status
python RUN_CLI.py chat --prompt "Hello. Introduce yourself in one sentence."
```

For a JSON history:

```json
[
  {"speaker": "user", "text": "I'm planning a trip."},
  {"speaker": "assistant", "text": "What kind of trip?"}
]
```

```bash
python RUN_CLI.py chat --prompt "More of a cultural trip." --history-file history.json
```

By default, the entire available checkpoint population is used. `--n-obsiss 10000` is an explicit reduction useful for ablation or latency testing; it does not modify the checkpoint and does not become the default value.

## 5. Quick Start — GUI

```bash
python RUN_GUI.py
```

Linux/macOS: `./RUN_GUI.sh`; Windows: `RUN_GUI.bat`. The interface allows users to enter a prompt, continue turns, and explicitly enable the non-response policy. Session exchanges are retained in the temporary dialogue history; there is no search or recall of previous conversations.

## 6. Backups, Checks, and Evidence

Before each generation, the runtime reads the files `chemins_eSonde_v7.json`, `checklist_de_travail_eSonde_v7.json`, `checklist_erreurs_no_model.json`, `checklist_erreurs_model.json`, and the savepoint registry. It checks the presence of the snapshot, its manifest, the manifest SHA-256, and the active checkpoint hash. If a critical check fails, generation is blocked rather than continuing without a trace.

After a generation or generation error, the runtime writes a result or incident report, updates the evidence, and attempts a post-execution snapshot. The paths are specified in `chemins_eSonde_v7.json`. Dialogue and log files may contain sensitive content; protect the output directory and apply the desired local retention policy.

## 7. Checkpoint Integrity Verification

```bash
python RUN_CLI.py verify --json-out runs_v7/verify.json
sha256sum models/eSonde_v6/weights.bin
```

The expected hash for `weights.bin` is:

`8526943d1528418fa8bbbf9128b61b5e1acd90a16eeb7cc062e18864b083dff4`

The hash check guarantees that the file is identical to the delivered version; it does not guarantee generation quality or the truthfulness of a response.

## 8. Currently Verified Limitations and Open Questions

- The generator relies on v6 TRAIN statistics: n-gram transitions, PPMI associations, and characters. It is not a trained Transformer, and the learned lexical support conditions its proposals.
- Negation, temporality, and modality markers are explicitly lexical; they do not constitute a complete semantic parser.
- The context preserves occurrences, roles, order, and provenance, but does not fully resolve coreference or causality.
- The ranking score and disagreement are not calibrated probabilities.
- Software tests are not sufficient to demonstrate dialogue coherence; blind, multilingual, multi-turn, comparative human evaluation is still required.
- The v6 P/R campaign at 1M is incomplete. v7 latency and memory usage across the entire population must be measured on a target machine.

These findings are not absolute theoretical limitations: they are the limitations demonstrated or not yet overcome by the currently available sources and tests.

## 9. Document References

- `formalism/formalisme_eSonde_v7.tex`: end-to-end architecture formalization.
- `formalism/formalise_eSonde_v7.tex`: requested copy using the alternative naming spelling.
- `formalism/laboratoire_eSonde_v7.tex`: experiments, comparisons, results, and decisions.
- `formalism/tech_opt_eSonde_v7.tex`: optimization and instrumentation.
- `docs/CLI_GUIDE.md`: detailed CLI contracts.
- `docs/GUI_GUIDE.md`: GUI guide.
- `docs/REPORT_TEMPLATE.md`: single report template with nine sections.






======================================================================================================================================
# eSonde v7 — Runtime de dialogue expérimental

**Version du runtime :** 7.0.0-experimental  
**Fonction publique :** chat prompt/réponse avec historique de dialogue courant facultatif  
**Checkpoint :** checkpoint original eSonde v6, 1 000 000 d'Obsiss, dimension 16  
**Poids :** `models/eSonde_v6/weights.bin`, 64 000 000 octets, SHA-256 `8526943d1528418fa8bbbf9128b61b5e1acd90a16eeb7cc062e18864b083dff4`

> Le runtime v7 est un prototype expérimental de dialogue construit sur le checkpoint original v6. Il implémente un décodeur contextuel token par token et un vote croisé de 16 familles d'Obsiss. Il ne revendique pas encore une compétence conversationnelle générale, une égalité ou une supériorité face aux LLM. Les capacités doivent être établies par essais indépendants et comparatifs.

## 1. Périmètre fonctionnel

L'unique tâche utilisateur est le chat : un prompt, éventuellement précédé de tours `user`/`assistant`/`system`, mène à une réponse. Le CLI public expose uniquement `chat`, `status` et `verify` (les deux dernières sont des opérations d'administration). L'interface graphique ne propose qu'une conversation. Les modules de calcul v6 conservés sont des composants internes de compatibilité nécessaires au checkpoint ; les anciennes interfaces CLI/GUI/évaluation ne sont pas exposées : pas de traduction, d'infill, de classification, de recherche ou de mode QA séparé.

La non-réponse est **désactivée par défaut**. Le modèle tente la meilleure continuation disponible. L'option `--allow-no-response` (CLI) ou la case GUI l'active explicitement.

## 2. Architecture résumée

1. **Checkpoint hérité** : les poids `weights.bin`, les statistiques linguistiques et le manifeste d'entraînement sont conservés à l'identique. Aucun entraînement v7 ou écrasement des poids n'est prétendu.
2. **Contexte transitoire** : chaque occurrence de token conserve son tour, son rôle et sa position. Les relations d'ordre et de succession des tours sont typées ; aucune causalité n'est inférée par le seul ordre. Le cadre est reconstruit depuis la conversation courante et le préfixe généré, sans base de connaissances persistante.
3. **Espace de 16 observations** : transition locale, association au prompt, association au dialogue, récurrence lexicale, affinité morphologique, rôle de réponse, continuité discursive, polarité, temporalité, frontière, support TRAIN, retour sous-mot, continuité référentielle, modalité, alignement de locuteur et nouveauté informationnelle.
4. **Voix des Obsiss** : chaque ligne du checkpoint reste identifiée par son index. L'Obsiss combine un canal primaire `a_i = i mod 16` et un canal secondaire `b_i = (7i+3) mod 16`, avec un gain dérivé de ses paramètres originaux. Les quantiles de chaque famille conservent la dispersion au lieu de masquer toutes les voix dans une moyenne.
5. **Génération** : chaque préfixe de faisceau réactive le contexte, produit des candidats n-grammes/PPMI, déclenche le retour caractère TRAIN si le support lexical local est rare, calcule les observations et sélectionne les continuations par les votes d'Obsiss. P observe le prompt ; R observe la réponse générée après coup comme diagnostic complémentaire.

Les spécifications complètes figurent dans `formalism/formalisme_eSonde_v7.tex`, `formalism/laboratoire_eSonde_v7.tex` et `formalism/tech_opt_eSonde_v7.tex`.

## 3. Prérequis et installation

- Python 3.10 ou supérieur.
- Les bibliothèques standard Python.
- NumPy est facultatif et accélère la calibration vectorisée. Un chemin scalaire de repli est fourni.
- Tkinter est requis pour l'interface graphique ; il peut être livré séparément dans certaines distributions Linux.
- Aucun téléchargement de modèle n'est nécessaire : les poids et statistiques sont dans `models/eSonde_v6/`.

Sur un système neuf, vérifier :

```bash
python --version
python -c "import tkinter; print('Tk OK')"   # GUI seulement
python -c "import numpy; print(numpy.__version__)"  # accélération facultative
```

Le dossier de livraison portable peut contenir `control/suivi_model_eSonde_v7/` et `control/sav_eSonde_v7/` à côté du runtime afin qu'un Dmodel extrait seul ait ses checklists et son snapshot initial. Dans l'arborescence de développement, ces éléments sont des dossiers frères du Dmodel. Le CLI repère les deux dispositions.

## 4. Démarrage rapide — CLI

Depuis le dossier racine du paquet :

```bash
python RUN_CLI.py --help
python RUN_CLI.py verify
python RUN_CLI.py status
python RUN_CLI.py chat --prompt "Bonjour. Présente-toi en une phrase."
```

Pour un historique JSON :

```json
[
  {"speaker": "user", "text": "Je prépare un voyage."},
  {"speaker": "assistant", "text": "Quel type de voyage ?"}
]
```

```bash
python RUN_CLI.py chat --prompt "Plutôt culturel." --history-file history.json
```

Par défaut, toute la population disponible du checkpoint est utilisée. `--n-obsiss 10000` est une réduction explicite utile pour une ablation ou un test de latence ; elle ne modifie pas le checkpoint et ne devient pas la valeur par défaut.

## 5. Démarrage rapide — interface graphique

```bash
python RUN_GUI.py
```

Linux/macOS : `./RUN_GUI.sh`; Windows : `RUN_GUI.bat`. L'interface permet de saisir le prompt, d'enchaîner les tours, et d'activer explicitement la politique de non-réponse. Les échanges de la session sont conservés dans l'historique temporaire du dialogue ; il n'existe pas de recherche ou de rappel d'anciennes conversations.

## 6. Sauvegardes, contrôles et preuves

Avant chaque génération, le runtime lit les fichiers `chemins_eSonde_v7.json`, `checklist_de_travail_eSonde_v7.json`, `checklist_erreurs_no_model.json`, `checklist_erreurs_model.json` et le registre de savepoint. Il vérifie la présence du snapshot, son manifeste, le SHA-256 du manifeste et le hash du checkpoint actif. Si un contrôle critique échoue, la génération est bloquée plutôt que de continuer sans trace.

Après une génération ou une erreur de génération, le runtime écrit un résultat ou un incident, met à jour les preuves et tente un snapshot post-exécution. Les chemins sont indiqués dans `chemins_eSonde_v7.json`. Les fichiers de dialogue et de logs peuvent contenir du contenu sensible ; protéger le dossier de sorties et appliquer la rétention locale voulue.

## 7. Vérification de l'intégrité du checkpoint

```bash
python RUN_CLI.py verify --json-out runs_v7/verify.json
sha256sum models/eSonde_v6/weights.bin
```

Le hash attendu pour `weights.bin` est :

`8526943d1528418fa8bbbf9128b61b5e1acd90a16eeb7cc062e18864b083dff4`

Le contrôle du hash garantit que le fichier est identique à celui livré ; il ne garantit ni la qualité de génération ni la véracité d'une réponse.

## 8. Limites actuellement vérifiées et questions ouvertes

- Le générateur s'appuie sur les statistiques TRAIN v6 : transitions n-grammes, associations PPMI et caractères. Il ne s'agit pas d'un Transformer entraîné et le support lexical appris conditionne les propositions.
- Les marqueurs de négation, temporalité et modalité sont explicitement lexicaux ; ils ne constituent pas un parseur sémantique complet.
- Le contexte préserve les occurrences, les rôles, l'ordre et la provenance, mais ne résout pas complètement la coréférence ni les causes.
- Le score de rang et le désaccord ne sont pas des probabilités calibrées.
- Les tests logiciels ne suffisent pas à démontrer la cohérence de dialogue ; une évaluation humaine aveugle, multilingue, multi-tours et comparative reste nécessaire.
- La campagne P/R v6 à 1M est incomplète. La latence et la mémoire v7 sur toute la population doivent être mesurées sur une machine cible.

Ces constats ne sont pas des limites théoriques absolues : ce sont les limites démontrées ou non encore levées par les sources et essais actuellement disponibles.

## 9. Référence des documents

- `formalism/formalisme_eSonde_v7.tex` : formalisation d'architecture de bout en bout.
- `formalism/formalise_eSonde_v7.tex` : copie demandée sous l'autre orthographe de nommage.
- `formalism/laboratoire_eSonde_v7.tex` : expériences, comparaisons, résultats et décisions.
- `formalism/tech_opt_eSonde_v7.tex` : optimisation et instrumentation.
- `docs/CLI_GUIDE.md` : contrats détaillés CLI.
- `docs/GUI_GUIDE.md` : guide de la GUI.
- `docs/REPORT_TEMPLATE.md` : modèle unique des rapports en neuf rubriques.
