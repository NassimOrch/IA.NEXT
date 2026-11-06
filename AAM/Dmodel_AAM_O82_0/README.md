# AAM O82 — ROCA-D

## Description
AAM O82 est l'implémentation exécutable de l'architecture ROCA-D formalisée dans `model_AAM_O82.tex`. Le noyau est non-LLM et standard-library-first. Il ne contient aucune table de réponses métier, aucune règle de domaine cachée, ni paramètres de teacher utilisés comme substitut à l'acquisition comportementale.

Le runtime met en œuvre : observation dégradée, empreintes partielles, retrieval mémoire obligatoire, suffisance décisionnelle, politique lexicographique, bundles concurrents, apprentissage par correction/CEGIS, capsules de compétences, auto-observation causale, découverte de probes par composition, décomposition structurelle, root-retest, recovery et replay.

La version est destinée à être lancée localement sur un PC sans service externe obligatoire.

## Runtime horizon semantics
`max_steps` is the maximum number of authoritative control cycles, including `INIT` and subsequent state-machine transitions. A small value may legitimately stop before retrieval or verification; this is a control-horizon outcome, never an impossibility claim. The normative portable examples therefore use a sufficient horizon (typically 32).

## Architecture

## Surfaces héritées O81 conservées
O82_0 conserve et étend les surfaces générales d'O81 0.3 : `StateMachine`/contrats d'action, `RuntimeState`, instruments variables et désaccord, self-health, lifecycle des compétences, re-observation/zoom, RAG comme observateur externe, firewall d'accès, adaptateurs black-box/subprocess, métriques de puissance et protocoles expérimentaux P1-P10. Ces surfaces restent soumises à la gouvernance O82 et ne fournissent aucune réponse métier pré-codée.

## Contrôle de potentiel
La comparaison de versions ne repose pas sur une seule accuracy. Utiliser `reports/P09_validation.json`, `reports/P09_benchmark.json` et les tests P09 pour vérifier fermeture, coût, observation, couverture, vérification, auto-amélioration et régression de capacité.
```text
Problème + Contrat + Budget
          |
          v
   Observation contractuelle
          |
          v
      Empreinte partielle
          |
          v
   Retrieval mémoire obligatoire
          |
          v
  Suffisance décisionnelle ? ---- oui ---> Vérification ---> ACT/DONE
          |
         non
          v
  Policy lexicographique / Pareto
          |
          v
 Probe suivante ou bundle concurrent
          |
          +--> correction / CEGIS / apprentissage
          +--> découverte de probe
          +--> décomposition / root-retest
          +--> auto-observation causale
          |
          v
      Ledger + Raw + Memory
          |
          v
      Replay / Recovery
```

Modules principaux : `governance`, `contracts`, `models`, `state`, `actions`, `runtime_state`, `probes`, `observation`, `fingerprint`, `memory`, `policy`, `controller`, `engine`, `learning`, `cegis`, `self_observer`, `self_health`, `skill_lifecycle`, `discovery`, `decomposition`, `composition`, `verification`, `sufficiency`, `instruments`, `rag`, `firewall`, `power`, `protocols`, `adapters`, `config`, `ledger`, `resources`, `validation`, `benchmark`.

## Pipeline complet
### 1. Préflight et gouvernance
Avant toute exécution, le runtime lit `checklist_erreurs_model.json` et `checklist_erreurs_no_model.json` dans le répertoire indépendant configuré par `AAM_O82_INDEPENDENT_CHECKLIST_DIR`, ou par défaut `~/.aam_o82/checklists`.

Une entrée `open` bloque l'exécution. Les fichiers dans `governance_seed/checklists/` ne sont qu'une graine d'initialisation du répertoire indépendant et ne remplacent pas celui-ci.

### 2. Runtime ROCA-D
1. Charger le contrat et vérifier budget/scope/policy.
2. Commencer par une observation minimale admissible.
3. Archiver le raw avant de dériver l'empreinte.
4. Dériver l'empreinte partielle et ses témoins.
5. Consulter la mémoire immédiatement après l'observation.
6. Calculer la suffisance relative au contrat.
7. Fermer uniquement si une décision unique possède les preuves requises.
8. Sinon sélectionner la prochaine probe selon l'ordre lexicographique et les filtres durs.
9. Utiliser un bundle seulement lorsque les probes sont admissibles et parallélisables.
10. En cas d'échec ou d'insuffisance, corriger, raffiner, découvrir ou décomposer.
11. Toute fermeture reste traçable dans le ledger.
12. Une absence de fermeture produit `UNRESOLVED` scoped sans revendication d'impossibilité globale.

### 3. Acquisition comportementale
```text
train -> observation minimale -> retrieval -> séparation des conflits
      -> correction/CEGIS -> capsule candidate
      -> holdout -> OOD -> vérification -> admission éventuelle
```

`EXPERIMENT` ne promeut jamais automatiquement une compétence. `FINAL` exige une validation séparée et interdit la dépendance active à un teacher.

### 4. Auto-observation et méta-acquisition
Les états auto-observables sont limités aux variables internes autorisées par la spécification. Les déclencheurs prioritaires couvrent notamment échec de vérification, surprise OOD, désaccord instrumental, corrections répétitives, changement de policy, admission de compétence, hausse de coût et dérive mémoire.

Une méta-policy candidate n'est promue que si une intervention causale appariée mesure un effet positif avec ressources comparables. Une prédiction utile ne vaut jamais certificat.

### 5. Découverte, composition et hiérarchie
Les probes nouvelles peuvent être découvertes par composition de probes déjà disponibles. L'artefact porte coût, latence, sécurité, provenance, références d'induction/validation et garde anti-fuite.

Les compétences peuvent être composées seulement lorsqu'elles sont compatibles et vérifiées. Une structure complexe peut être décomposée en sous-tâches parent-enfants sans introduire de règle métier. Toute nouvelle capacité pertinente peut déclencher un root-retest du contrat parent.

## Installation PC
### Pré-requis
Python 3.10, 3.11, 3.12 ou 3.13.

Le noyau n'a aucune dépendance Python externe obligatoire.

### Linux / macOS — voie recommandée sans installation
```bash
export PYTHONPATH="$PWD/src"
python3 -m aam_o82 doctor
```

### Linux / macOS — installation editable (optionnelle)
```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -e .
python -m aam_o82 doctor
```
Cette voie utilise le backend de build Python indiqué dans `pyproject.toml` et peut nécessiter que `setuptools` soit déjà disponible ou téléchargeable sur le PC. La voie « sans installation » reste autonome et ne télécharge aucun composant.

### Linux / macOS — sans installation
```bash
export PYTHONPATH="$PWD/src"
python3 -m aam_o82 doctor
```

### Windows PowerShell — voie recommandée sans installation
```powershell
$env:PYTHONPATH = "$PWD\src"
py -3 -m aam_o82 doctor
```

### Windows PowerShell — installation editable (optionnelle)
```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
py -3 -m pip install -e .
py -m aam_o82 doctor
```
La voie editable peut nécessiter que le backend de build (`setuptools`) soit déjà disponible ou téléchargeable. La voie « sans installation » reste la voie autonome.

### Windows PowerShell — sans installation
```powershell
$env:PYTHONPATH = "$PWD\src"
py -3 -m aam_o82 doctor
```

### Utilisation depuis une archive extraite
Extraire `Dmodel_AAM_O82.zip`, ouvrir un terminal dans le dossier extrait, puis utiliser la procédure « sans installation » correspondant au système d'exploitation. Aucun chemin absolu propre à la machine de développement n'est requis. Au premier lancement, le runtime copie automatiquement `governance_seed/checklists/` vers le répertoire indépendant si les deux checklists obligatoires n'y existent pas.

## Gouvernance des checklists
Répertoire indépendant par défaut :
```text
~/.aam_o82/checklists/
```

Forcer un emplacement différent :
```bash
export AAM_O82_INDEPENDENT_CHECKLIST_DIR=/chemin/vers/checklists
```

PowerShell :
```powershell
$env:AAM_O82_INDEPENDENT_CHECKLIST_DIR = "C:\chemin\vers\checklists"
```

Fichiers obligatoires :
```text
checklist_erreurs_model.json
checklist_erreurs_no_model.json
```

Le plan de phase de cette version est `checklist_O82_0.json`; il décrit les gates P00 à P10 et leurs preuves de clôture.

## Commandes d'exécution
### Diagnostic
```bash
o82 doctor
```
Sans installation :
```bash
PYTHONPATH=src python -m aam_o82 doctor
```

### Runtime
Créer un épisode et exécuter le contrôleur avec la configuration normative :
```bash
PYTHONPATH=src python -m aam_o82 run --problem examples/task.json --contract examples/echo_contract.json --config config/runtime.json --skill <skill.json> --workdir runs/runtime
```

`--skill <skill.json>` est optionnel; lorsqu’il est fourni en FINAL, le fichier est importé avec son statut déclaré et seul un skill VERIFIED compatible peut conduire à une fermeture certifiée.
Les options `--budget`, `--mode` et `--seed` restent disponibles comme surcharges explicites de la configuration. La commande normative sans configuration reste également valide lorsqu'elle fournit `--budget` et `--mode`.

Observer explicitement un épisode existant :
```bash
o82 observe --episode <id> --probe structure --workdir runs/runtime
```

Reprise d'un épisode créé avec une configuration :
```bash
PYTHONPATH=src python -m aam_o82 observe --episode <id> --probe structure --config config/runtime.json --workdir runs/runtime
```

Rejouer et vérifier le ledger :
```bash
o82 replay --episode <id> --workdir runs/runtime
```

### Acquisition
Avec configuration :
```bash
PYTHONPATH=src python -m aam_o82 acquire --dataset examples/demo_dataset.jsonl --contract examples/echo_contract.json --config config/acquisition.json --workdir runs/acquire
```
Surcharge explicite :
```bash
o82 acquire --dataset examples/demo_dataset.jsonl --contract examples/echo_contract.json --mode EXPERIMENT --workdir runs/acquire
```

Promotion conditionnelle :
```bash
o82 acquire --dataset examples/demo_dataset.jsonl --contract examples/echo_contract.json --mode FINAL --workdir runs/acquire_final
```

Évaluer réellement un split :
```bash
o82 evaluate --skill <skill-id> --split holdout --dataset examples/demo_dataset.jsonl --contract examples/echo_contract.json --workdir runs/acquire
```
```bash
o82 evaluate --skill <skill-id> --split ood --dataset examples/demo_dataset.jsonl --contract examples/echo_contract.json --workdir runs/acquire
```

### Compatibilité CLI O81

O82_0 conserve les commandes générales de la branche O81 0.3, ainsi que l’entrée `run --skill`, adaptées aux contrats O82 : `experiment`, `verify-skill`, `transfer`, `compose` et `memory-verify`. Ces commandes ne contournent ni le ledger, ni les preuves, ni les budgets; `compose` refuse les skills non vérifiés et `transfer` renvoie `UNRESOLVED` lorsqu’une empreinte n est pas couverte.

```bash
PYTHONPATH=src python -m aam_o82 experiment --problem examples/task.json --contract examples/echo_contract.json --config config/runtime.json --workdir runs/experiment
PYTHONPATH=src python -m aam_o82 verify-skill --skill <skill.json> --dataset examples/demo_dataset.jsonl --split holdout --contract examples/echo_contract.json
PYTHONPATH=src python -m aam_o82 transfer --skill <skill.json> --input <input.json> --contract examples/echo_contract.json
PYTHONPATH=src python -m aam_o82 compose --skills <skill_a.json> <skill_b.json> --contract examples/echo_contract.json
PYTHONPATH=src python -m aam_o82 memory-verify --memory runs/runtime/memory
```

### Mémoire et probes
```bash
o82 memory review --workdir runs/runtime --contract-id demo.echo
o82 memory search --fingerprint <hash> --contract-id demo.echo --scope demo --workdir runs/runtime
o82 probe list
o82 probe test structure
```

### Configuration déclarative
`config/runtime.json` et `config/acquisition.json` déclarent budget, politique de ressources, allowlist de probes, mémoire, verificateurs, adaptateurs externes, seuils d’auto-observation, seed, mode et rétention.

Validation directe :
```bash
PYTHONPATH=src python -c "from pathlib import Path; from aam_o82.config import load_runtime_config; print(load_runtime_config(Path('config/runtime.json')).to_dict())"
```

`--config` est une extension CLI optionnelle qui ne retire aucune commande normative du document de modèle. Les chemins d’adaptateurs externes doivent appartenir à `path_allowlist`; un chemin hors allowlist est rejeté avant construction du moteur.

### Validation et benchmark
```bash
PYTHONPATH=src python scripts/validate_o82.py --output reports/P11_validation.json
PYTHONPATH=src python scripts/benchmark_o82.py --output reports/P12_benchmark.json
```

Les deux scripts affichent le JSON sur la sortie standard. Avec `--output <path>`, ils écrivent aussi exactement le résultat agrégé à cet emplacement.

### Tests complets
```bash
PYTHONPATH=src python scripts/test_all.py
```

## API Python avancée
### Découverte de probe
```python
from pathlib import Path
from aam_o82.contracts import load_contract
from aam_o82.probes import ProbeRegistry
from aam_o82.discovery import ProbeDiscoveryEngine
from aam_o82.memory import MemoryQuotient
from aam_o82.learning import load_dataset

contract = load_contract({...})
registry = ProbeRegistry()
rows = load_dataset(Path("examples/demo_dataset.jsonl"))
discovery = ProbeDiscoveryEngine(registry)
probe, artifact = discovery.discover(rows, contract, MemoryQuotient(Path("runs/discovery/memory")))
registry.register(probe)
```

### Décomposition et root-retest
```python
from pathlib import Path
from aam_o82.engine import Engine
from aam_o82.contracts import load_contract

contract = load_contract({...})
engine = Engine(Path("runs/hierarchy"), contract, {...})
children = engine.decompose(problem)
result = engine.root_retest(problem, reason="new_verified_capability")
```

### Composition de compétences
```python
from aam_o82.composition import SkillComposer
composer = SkillComposer()
composite = composer.compose(verified_skills, contract)
```

Ces API restent soumises aux mêmes contrats, budgets, vérifications et checklists que le CLI. Lorsqu'un moteur est construit avec `runtime_config`, cette même configuration est propagée aux enfants et root-retests.

## Recovery et intégrité
La mémoire repose sur SQLite plus des journaux JSONL append-only. Les raws sont vérifiés par hash SHA-256. `recover()` reconstruit l'index depuis les journaux puis réapplique les invalidations avant de contrôler les références raw des nœuds actifs.

Le ledger `events.jsonl` est chaîné par hash. `o82 replay --episode <id>` vérifie l'intégrité de la chaîne avant de retourner les événements de l'épisode.

## Modes
### EXPERIMENT
Les nouvelles compétences, probes et méta-policies peuvent rester candidates. Elles ne contaminent pas la voie certifiante de `FINAL`.

### FINAL
Seules les compétences `VERIFIED_SKILL` compatibles avec le contrat sont utilisables pour fermer une décision. Le teacher ne peut pas être une dépendance active du chemin final.

## Structure du projet
```text
src/aam_o82/        code du runtime
examples/           exemples de contrats/datasets
scripts/             tests, validation, benchmark
reports/             rapports de phase et résultats
config/              configuration d'exemple
go​vernance_seed/    graines locales des checklists indépendantes
tests/              tests unitaires et d'intégration
model_AAM_O82.tex   spécification normative
```

## Rapport de version
Tous les rapports utilisent le même template :
1. Description
2. Architecture
3. Pipeline complet
4. Commandes d'exécution
5. Résultats

Le rapport principal est `reports/AAM_O82_implementation_report.md`.

## Ce que le runtime certifie
Le runtime distingue fermeture contractuelle, niveau de vérification, provenance et état de connaissance. `DONE/EXECUTION_CONTRACT_CLOSED` signifie que le contrat logiciel a été fermé selon ses preuves disponibles ; ce n'est pas une affirmation universelle de vérité externe.

## Erreurs récurrentes
Consulter avant toute exécution :
```text
AAM_O82_independent_checklists/checklist_erreurs_model.json
AAM_O82_independent_checklists/checklist_erreurs_no_model.json
```

Toute nouvelle erreur doit être ajoutée au registre correspondant avant sa résolution. Une erreur intrinsèque au modèle va dans `checklist_erreurs_model.json`; une erreur de packaging, d'outil, de ressource ou de banc de contrôle va dans `checklist_erreurs_no_model.json`.

## API services externes optionnels
Le runtime Python expose `Engine.add_rag_document`, `Engine.observe_rag`, `Engine.mark_rag_stale`, `Engine.set_access_manifest`, `Engine.register_external_adapter` et `Engine.query_external_adapter`. Ces interfaces sont facultatives et n'activent aucune source externe par défaut.
