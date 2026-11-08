# eSonde_v0 — Pure-Probe Learning Model

**Version:** 0.1.0-dev (audited release candidate)  
**Date:** November 8, 2026  
**Runtime:** Python 3.10+ and the standard library only. No third-party packages are required.  
**GUI:** Tkinter is optional; the CLI works without a graphical interface.

## 1. Purpose and Status

eSonde_v0 is a supervised tabular regression and classification model whose predictive units consist exclusively of probes. The model contains no neurons, no MLP, no learned affine encoder/head, and no dense or affine residual layers. Probes observe an explicit support, calculate local proximity, carry a consequence, and participate in normalized coordination. This version is an audited functional prototype; no general superiority over any benchmark is claimed.

## 2. Architecture

For a probe `i`, with support `J_i`, anchor `c_i`, positive width `s_i`, consequence `v_i`, and preference `b_i`:

```text
delta_i(x) = mean_j [ ((x_j - c_ij) / s_ij)^2 ]
a_i(x)     = b_i - delta_i(x) / (2 * tau)
w_i(x)     = softmax(a(x))_i
z(x)       = sum_i w_i(x) * v_i
```

Regression: `prediction = z`. Classification: `probabilities = softmax(z)`.

| Family | Support | Anchor | Role |
|---|---|---|---|
| `local` | all variables | adaptive | local response and probe adaptation |
| `coverage` | all variables | geometric, then frozen | support diversity and coverage witness |
| `interaction` | pairs of variables | adaptive | joint observation without an injected symbolic operator |

The preference `b_i` and temperature `tau` adapt the coordination process. All three families can coexist within the same model. Relational/CNC composite graphs remain formalized extensions and are not features of the v0 runtime.

## 3. Training Pipeline

1. Strict CSV parsing: unique headers, present and finite values, numeric variables.
2. Deterministic train/validation/test split (70/15/15 by default; stratified for classification).
3. Fit the normalizer using the training set only.
4. Initialize supports and consequences using the training set only.
5. Calculate probe responses and their coordination.
6. Analytical gradients for MSE or cross-entropy.
7. Adam with individual moments and counters; `coverage` anchors do not evolve, and their moments/counters remain zero.
8. Select the epoch based on validation performance and save the best state.
9. Compute the test score after freezing the model; generate a JSON report, CSV predictions, and coverage diagnostics.

Repeated calls to `fit()` constitute independent new training runs and restore the initial hyperparameters, including the temperature. The JSON file saves the normalizer, probes, Adam state corresponding to the best validated state, random seed, and training history. Exact resumption in the middle of an epoch is not implemented in v0.

## 4. Package Contents

- `run_esonde.py` — direct launcher.
- `run_esonde.sh`, `run_esonde.bat` — convenient POSIX/Windows launchers.
- `src/esonde/model.py` — computation, training, gradients, optimization, JSON model, and diagnostics.
- `src/esonde/data.py` — CSV handling and train/validation/test splitting.
- `src/esonde/metrics.py` — regression/classification metrics.
- `src/esonde/cli.py` — CLI.
- `src/esonde/gui.py` — Tk interface: training, prediction, evaluation, and inspection.
- `tests/` — unit tests and numerical gradient tests.
- `scripts/audit_pure_probe.py` — AST-based audit against prohibited neural/affine layers.
- `examples/` — small, reproducible CSV files.
- `examples/models/` — nine trained and verified JSON model states (index, SHA-256, and guide included): regression, classification, and hybrid examples. These are demonstration snapshots, not universal weights.
- `formalism/formalisme_eSond_v0.tex` — complete mathematical specification.
- `docs/` — detailed guide, scientific protocol, and report template.

## 5. Installation and Getting Started

No `pip install` is required. The archive uses the Python standard library, but requires a Python 3.10+ interpreter to be installed on the PC (the Python distribution is a system prerequisite and is not bundled in the ZIP file).

Linux/macOS:

```bash
chmod +x run_esonde.sh
./run_esonde.sh --help
./run_esonde.sh demo --task regression --output demo.json
```

Windows (PowerShell or CMD):

```bat
run_esonde.bat --help
run_esonde.bat demo --task classification --output demo_cls.json
```

Direct launch on any platform: `python run_esonde.py --help` (or `py run_esonde.py ...` on Windows).

## 6. Full CLI

Help/version:

```bash
python run_esonde.py --help
python run_esonde.py --version
```

Synthetic demo:

```bash
python run_esonde.py demo --task regression --output demo_reg.json --probes 16 --seed 17
python run_esonde.py demo --task classification --output demo_cls.json --probes 16 --seed 17
```

CSV training:

```bash
python run_esonde.py train donnees.csv --target cible --task regression \
  --model modele.json --probes 18 --families local,coverage,interaction \
  --epochs 300 --patience 35 --batch-size 32 --learning-rate 0.025 --seed 17
```

Options: `--task regression|classification`, `--model`, `--probes`, `--families local,coverage,interaction`, `--seed`, `--epochs`, `--patience`, `--batch-size`, `--learning-rate`, `--temperature`, `--coverage-threshold` (optional; defaults to train-only calibration), `--train-fraction`, `--valid-fraction`.

Prediction (CSV without target):

```bash
python run_esonde.py predict --model modele.json --csv nouveaux.csv --output predictions.csv
```

Evaluation (labeled CSV, without retraining) and inspection:

```bash
python run_esonde.py evaluate --model modele.json --csv donnees_labelisees.csv --target cible
python run_esonde.py inspect --model modele.json
```

The model checks column names and order if a manifest has been saved. The output of `evaluate` describes the supplied dataset and does not adjust any parameters.

## 7. Full Graphical Interface

Launch: `python run_esonde.py gui`.

The GUI provides the same main operations as the CLI:

1. Select the CSV file and target column (leave the target empty for prediction).
2. Choose the task type and training/family parameters.
3. Set the JSON model path and output CSV path.
4. **Train**: saves the model, a `.report.json` report, and the metrics for the held-out test set.
5. **Predict CSV**: load the model and write predictions, optional probabilities, and coverage diagnostics.
6. **Evaluate CSV**: calculate metrics on a labeled CSV file, without retraining.
7. **Inspect Model**: display the family registry, dimensions, and parameters.

Long-running operations execute in a worker thread; the widgets are updated by the Tk thread. Interactive cancellation of a training run that has already started is not available in v0. Tkinter requires a graphical environment; on a headless server, use the CLI.

## 8. Tests and Audits

```bash
python -m unittest discover -s tests -v
python -m py_compile run_esonde.py src/esonde/*.py scripts/*.py
python scripts/audit_pure_probe.py
```

The release test suite contains **15 tests**, including finite-difference gradient verification for both tasks, probability checks, exact save/reload, train-only coverage calibration and explicit override, retraining reset, frozen `coverage` anchors, pairwise supports, rejection of empty validation sets and non-finite data, finite predictions for extreme out-of-support inputs, and refusal to load a model declaring an MLP.

The AST audit inspects runtime files and searches for prohibited neural modules/layers. It remains a static audit, complemented by tests and code review.

## 9. Outputs and Diagnostics

The JSON model contains: schema/version, task, hyperparameters, train-only statistics, families and supports, probe parameters, Adam state, classes, training history, and column manifest. The CLI training process also generates a JSON report containing data splits, test metrics, and execution time, as well as a CSV file containing test predictions.

Each prediction exposes the following diagnostics:

- `min_probe_distance`: minimum distance to a probe's support.
- `max_probe_weight`: maximum coordination weight.
- `normalized_entropy`: normalized entropy of the weights.
- `out_of_support`: indicator showing whether the distance exceeds the configured threshold.

By default, the out-of-support threshold is determined before optimization using only the minimum distances between the training observations and the initial anchors: the 95th percentile multiplied by 1.5. The calculation does not use validation or test data.

An explicit threshold can replace this calibration through `--coverage-threshold`. The threshold is a geometric diagnostic, not an error probability; it does not modify the prediction and does not guarantee the detection of all errors.

### Provided Model Snapshots

The `examples/models/` directory contains nine native eSonde_v0 JSON models that have already been trained. To inspect a model:

```bash
python run_esonde.py inspect --model examples/models/release_final_model.json
python run_esonde.py inspect --model examples/models/cli_hybrid_3d.json
```

The `MODELS_INDEX.json` index provides the task, number of probes, families, and SHA-256 fingerprint for each file. The checksums are available in `MODELS_SHA256SUMS.txt`.

These model states make it possible to verify inference and inspection without retraining. They remain specific to their documented tasks and columns.

## 10. Scientific Status and Explicit Limitations

- The runtime core implements the `local`, `coverage`, and `interaction` families, as well as coordination through temperature/priorities.
- Relational graph probes and composite CNC structures are not included in the v0 runtime.
- The real EX3–EX12 datasets are not incorporated into the delivered model. The sealed EX12 tests have not been opened or rescored.
- No paired MLP comparison has been performed by this package using the same splits/configurations; no superiority, non-inferiority, or universal generalization is claimed.
- Standardization does not prevent a lack of support: always inspect the out-of-support diagnostics.
- `Python 3.10+` is required; Tkinter is optional; the ZIP does not include a Python runtime for all operating systems.

## 11. Security, Integrity, and Reproducibility

Models are UTF-8 JSON files, written using atomic replacement. The loader checks dimensions, families, finite parameters, Adam state, and architectural purity flags. `.pt` checkpoints from other experiments are never loaded by the eSonde runtime.

Source archives remain within the audit package and are accompanied by separate SHA-256 manifests.

Keep the random seed, command, CSV file, reports, logs, and checksums. Never select a configuration based on the final test set.



=============================================================================================================================================
=============================================================================================================================================
=============================================================================================================================================
=============================================================================================================================================

# eSonde_v0 — modèle d'apprentissage par sondes pures

**Version :** 0.1.0-dev (release candidate audité)  
**Date :** 8 novembre 2026  
**Runtime :** Python 3.10+ et bibliothèque standard uniquement. Aucun paquet tiers n'est requis.  
**GUI :** Tkinter facultatif ; le CLI fonctionne sans interface graphique.

## 1. Objet et statut

eSonde_v0 est un modèle supervisé tabulaire de régression et de classification dont les unités prédictives sont exclusivement des sondes. Le modèle ne contient ni neurones, ni MLP, ni encodeur/tête affine appris, ni couche dense ou résidu affine. Les sondes observent un support explicite, calculent une proximité locale, portent une conséquence et participent à une coordination normalisée. La version est un prototype fonctionnel audité ; aucune supériorité générale sur un comparateur n'est affirmée.

## 2. Architecture

Pour une sonde `i`, de support `J_i`, ancre `c_i`, largeur positive `s_i`, conséquence `v_i` et préférence `b_i` :

```text
delta_i(x) = mean_j [ ((x_j - c_ij) / s_ij)^2 ]
a_i(x)     = b_i - delta_i(x) / (2 * tau)
w_i(x)     = softmax(a(x))_i
z(x)       = sum_i w_i(x) * v_i
```

Régression : `prediction = z`. Classification : `probabilities = softmax(z)`.

| Famille | Support | Ancre | Rôle |
|---|---|---|---|
| `local` | toutes les variables | adaptative | réponse locale et adaptation de la sonde |
| `coverage` | toutes les variables | géométrique puis gelée | diversité du support et témoin de couverture |
| `interaction` | paires de variables | adaptative | observation conjointe sans opérateur symbolique injecté |

La préférence `b_i` et la température `tau` adaptent la coordination. Les trois familles peuvent coexister dans un même modèle. Les graphes relationnels/CNC composés restent des extensions formalisées et non des fonctions du runtime v0.

## 3. Pipeline d'apprentissage

1. Lecture stricte du CSV : en-têtes uniques, valeurs présentes et finies, variables numériques.
2. Séparation train/validation/test déterministe (70/15/15 par défaut ; stratifiée en classification).
3. Ajustement du normaliseur sur train uniquement.
4. Initialisation des supports et conséquences sur train uniquement.
5. Calcul des réponses de sondes et de leur coordination.
6. Gradients analytiques pour MSE ou cross-entropy.
7. Adam avec moments et compteur individuels ; les ancres `coverage` n'évoluent pas et leurs moments/compteurs restent nuls.
8. Sélection de l'époque sur validation, sauvegarde du meilleur état.
9. Score test après gel ; rapport JSON, prédictions CSV et diagnostics de couverture.

L'appel répété à `fit()` constitue un nouvel entraînement indépendant et restaure les hyperparamètres initiaux, dont la température. Le JSON sauvegarde le normaliseur, les sondes, l'état Adam du meilleur état validé, la graine et l'historique. La reprise exacte au milieu d'une époque n'est pas implémentée dans v0.

## 4. Contenu du package

- `run_esonde.py` — lanceur direct.
- `run_esonde.sh`, `run_esonde.bat` — lanceurs pratiques pour POSIX/Windows.
- `src/esonde/model.py` — calcul, apprentissage, gradients, optimisation, modèle JSON et diagnostics.
- `src/esonde/data.py` — CSV et split train/validation/test.
- `src/esonde/metrics.py` — métriques régression/classification.
- `src/esonde/cli.py` — CLI.
- `src/esonde/gui.py` — interface Tk : entraînement, prédiction, évaluation, inspection.
- `tests/` — tests unitaires et tests numériques des gradients.
- `scripts/audit_pure_probe.py` — audit AST anti-couches neuronales/affines.
- `examples/` — petits CSV reproductibles.
- `examples/models/` — neuf états JSON entraînés et vérifiés (index, SHA-256 et guide inclus) : exemples de régression, classification et hybride. Ce sont des snapshots de démonstration, pas des poids universels.
- `formalism/formalisme_eSond_v0.tex` — spécification mathématique complète.
- `docs/` — guide détaillé, protocole scientifique et modèle de rapport.

## 5. Installation et démarrage

Aucun `pip install` n'est nécessaire. L'archive utilise la bibliothèque standard Python, mais nécessite un interpréteur Python 3.10+ installé sur le PC (la distribution Python est un prérequis système, elle n'est pas embarquée dans le ZIP).

Linux/macOS :

```bash
chmod +x run_esonde.sh
./run_esonde.sh --help
./run_esonde.sh demo --task regression --output demo.json
```

Windows (PowerShell ou CMD) :

```bat
run_esonde.bat --help
run_esonde.bat demo --task classification --output demo_cls.json
```

Lancement direct partout : `python run_esonde.py --help` (ou `py run_esonde.py ...` sur Windows).

## 6. CLI complet

Aide/version :

```bash
python run_esonde.py --help
python run_esonde.py --version
```

Démo synthétique :

```bash
python run_esonde.py demo --task regression --output demo_reg.json --probes 16 --seed 17
python run_esonde.py demo --task classification --output demo_cls.json --probes 16 --seed 17
```

Entraînement CSV :

```bash
python run_esonde.py train donnees.csv --target cible --task regression \
  --model modele.json --probes 18 --families local,coverage,interaction \
  --epochs 300 --patience 35 --batch-size 32 --learning-rate 0.025 --seed 17
```

Options : `--task regression|classification`, `--model`, `--probes`, `--families local,coverage,interaction`, `--seed`, `--epochs`, `--patience`, `--batch-size`, `--learning-rate`, `--temperature`, `--coverage-threshold` (facultatif ; par défaut calibrage train-only), `--train-fraction`, `--valid-fraction`.

Prédire (CSV sans cible) :

```bash
python run_esonde.py predict --model modele.json --csv nouveaux.csv --output predictions.csv
```

Évaluer (CSV étiqueté, sans réentraînement) et inspecter :

```bash
python run_esonde.py evaluate --model modele.json --csv donnees_labelisees.csv --target cible
python run_esonde.py inspect --model modele.json
```

Le modèle vérifie les noms/ordre des colonnes si le manifeste a été enregistré. Le résultat de `evaluate` décrit le jeu fourni et n'ajuste aucun paramètre.

## 7. Interface graphique complète

Lancement : `python run_esonde.py gui`.

Le GUI propose les mêmes opérations principales que le CLI :

1. Sélectionner le CSV et la colonne cible (laisser la cible vide pour une prédiction).
2. Choisir le type de tâche et les paramètres d'entraînement/familles.
3. Définir le chemin du modèle JSON et celui du CSV de sortie.
4. **Entraîner** : sauvegarde le modèle, un rapport `.report.json` et les métriques du test réservé.
5. **Prédire CSV** : charger le modèle et écrire les prédictions, probabilités éventuelles et diagnostics de couverture.
6. **Évaluer CSV** : calculer les métriques sur un CSV étiqueté, sans réentraînement.
7. **Inspecter modèle** : afficher le registre des familles, dimensions et paramètres.

Les opérations longues tournent dans un thread de travail ; les widgets restent mis à jour par le thread Tk. L'annulation interactive d'un entraînement déjà engagé n'est pas disponible en v0. Tkinter nécessite un environnement graphique ; sur serveur headless, utilisez le CLI.

## 8. Tests et audits

```bash
python -m unittest discover -s tests -v
python -m py_compile run_esonde.py src/esonde/*.py scripts/*.py
python scripts/audit_pure_probe.py
```

La suite de release compte **15 tests**, dont vérification de gradients par différences finies pour les deux tâches, probabilités, save/reload exact, calibration de couverture train-only et override explicite, réinitialisation d'un réentraînement, ancrages coverage gelés, supports pairwise, rejet de validation vide et de données non finies, prédiction extrême hors-support finie et refus de charger un modèle déclarant un MLP. L'audit AST inspecte les fichiers runtime et recherche modules/couches neuronaux interdits ; il reste un audit statique, complété par tests et lecture de code.

## 9. Sorties et diagnostics

Le modèle JSON contient : schéma/version, tâche, hyperparamètres, statistiques train-only, familles et supports, paramètres des sondes, état Adam, classes, historique et manifeste de colonnes. Le train CLI produit aussi un rapport JSON avec partitions, métriques test et temps, ainsi qu'un CSV des prédictions test.

Chaque prédiction expose les diagnostics :
- `min_probe_distance` : distance minimale au support d'une sonde ;
- `max_probe_weight` : poids maximal de coordination ;
- `normalized_entropy` : entropie normalisée des poids ;
- `out_of_support` : indicateur de distance supérieure au seuil configuré.

Par défaut, le seuil hors-support est déterminé avant l'optimisation à partir des distances minimales des seules observations train aux ancres initiales : quantile 95 % multiplié par 1,5. Le calcul n'utilise ni validation ni test. Un seuil explicite peut remplacer cette calibration avec `--coverage-threshold`. Le seuil est un diagnostic géométrique, non une probabilité d'erreur ; il ne modifie pas la prédiction et n'est pas une garantie de détection de toutes les erreurs.

### Snapshots de modèles fournis

Le dossier `examples/models/` contient neuf modèles JSON natifs entraînés par eSonde_v0. Pour inspecter un modèle :

```bash
python run_esonde.py inspect --model examples/models/release_final_model.json
python run_esonde.py inspect --model examples/models/cli_hybrid_3d.json
```

L'index `MODELS_INDEX.json` donne la tâche, le nombre de sondes, les familles et l'empreinte SHA-256 de chaque fichier. Les checksums sont dans `MODELS_SHA256SUMS.txt`. Ces états permettent de vérifier l'inférence et l'inspection sans réentraînement ; ils restent spécifiques à leurs tâches et colonnes documentées.

## 10. Statut scientifique et limites explicites

- Le cœur runtime implémente les familles `local`, `coverage`, `interaction` et la coordination par température/priorités.
- Les sondes relationnelles en graphe et CNC composés ne sont pas dans le runtime v0.
- Les données réelles EX3–EX12 ne sont pas incorporées dans le modèle livré. Les tests EX12 scellés n'ont pas été ouverts/resscorés.
- Aucune comparaison MLP appariée n'a été exécutée par ce package sur les mêmes splits/configurations ; aucune supériorité, non-infériorité ou généralisation universelle n'est revendiquée.
- La standardisation n'empêche pas le manque de support : toujours inspecter les diagnostics hors-support.
- `Python 3.10+` est requis ; Tkinter est facultatif ; le ZIP n'embarque pas un runtime Python pour tous systèmes.

## 11. Sécurité, intégrité et reproductibilité

Les modèles sont JSON UTF-8, écrits par remplacement atomique. Le chargeur vérifie dimensions, familles, paramètres finis, état Adam et drapeaux de pureté architecturale. Les checkpoints `.pt` issus d'autres expériences ne sont jamais chargés par le runtime eSonde. Les archives source restent dans le package d'audit et sont accompagnées de manifestes SHA-256 distincts. Conserver la graine, la commande, le CSV, les rapports, les logs et les checksums ; ne jamais choisir une configuration à partir du test final.

