# AAM O94.3 — guide de démarrage

## Démarrage

Extraire intégralement `Dmodel_AAM_O94_3.zip`, puis lancer `run_AAM_O94_3.bat` sous Windows, `run_AAM_O94_3.sh` sous Linux/macOS, ou `run_AAM_O94_3.ps1` depuis PowerShell. Les journaux de préflight et du lanceur sont conservés sous `logs/O94_3/`.

## Observation live

Dans l’onglet **Observer**, choisir une source autorisée :

- **filesystem** : observer les ajouts, modifications et suppressions dans un dossier choisi par l’utilisateur; le JSONL est créé par AAM dans son workspace (ou à un chemin choisi).
- **process** : collecter les instantanés accessibles d’un PID (état, ressources et descripteurs permis par le système). Nécessite les permissions du système et `psutil`.
- **network** : capturer les métadonnées/paquets accessibles via TShark et une interface sélectionnée. Nécessite TShark et les privilèges de capture du système. Les payloads sont désactivés par défaut; TLS demeure chiffré.

La session a un budget configurable de durée, nombre d’événements et octets, crée un fichier JSONL et un rapport d’arrêt. Elle ne requiert pas un JSONL préconstruit. Les traces JSONL préexistantes restent admises comme mode séparé d’apprentissage/rejeu.

Exemple CLI :

```bash
python -m aam_o93 observe-live --source-kind filesystem --authorize-source --root ./dossier_a_observer --seconds 10 --max-events 5000
```

Pour observer un processus, fournir `--pid PID`; pour le réseau, utiliser `--interface ID` et éventuellement `--capture-filter`. Vérifier les permissions et respecter l’autorisation de la source. AAM ne lit pas arbitrairement la mémoire d’un processus ni ne déchiffre le trafic TLS.

## Modèles locaux et externes

L’onglet **Models local/PyTorch** expose :

- **Transformers local** : chemin vers un répertoire de modèle/tokenizer local; le chargement peut être configuré pour rester hors ligne.
- **PyTorch TorchScript** : charge directement un module local exporté par `torch.jit.trace` / `torch.jit.script`; l’entrée est JSON tensorielle (`{"input":[...]}`, `{"inputs":[...]}` ou `{"kwargs":{...}}`) et la sortie est sérialisée en JSON. CPU par défaut; pas de désérialisation pickle arbitraire.
- **PyTorch adapter** : un fichier `.pt`/`.pth` de poids n’indique pas l’architecture. Copier et compléter `examples/model_adapters/pytorch_state_dict_adapter_template.py` pour déclarer `load_model`, `generate` et, si approprié, `train_model`.
- **Ollama** : endpoint local et identifiant de modèle.
- **OpenAI-compatible** : endpoint compatible et identifiant; la clé API est saisie à l’exécution et ne doit pas être écrite dans les fichiers de configuration/rapports.
- **AAM workspace** : utilisation d’un workspace AAM comme source de données/artefacts via les contrats documentés.

Un modèle externe réel exige que ses fichiers, dépendances et/ou serveur existent. TorchScript n’est pas équivalent à un chargeur de state_dict : ce dernier exige un adaptateur dont l’architecture est connue.

## Programmation par composition

L’onglet **Composition** répertorie les briques de base, permet de composer le DSL supporté et de compiler vers un artefact JSON versionné. **Apprendre depuis une trace** ajoute des candidats : les règles/méthodes dérivées d’observations restent en revue manuelle; les paires entrée-sortie non ambiguës de l’ensemble train créent un lookup exact, qui répond `UNRESOLVED` pour une entrée inconnue. Les lignes holdout/test ne servent pas à l’apprentissage.

## Données/RAG

Les composants historiques `aam_o93/semantic_rag.py`, `aam_o92/retrieval.py` et les tests historiques référencés dans `rapport_O94_3/rag_parity_O94_0_O94_1_O94_2.json` sont conservés byte-à-byte depuis les versions parentes. Les tests RAG sont exécutés séparément dans la validation O94.3.

## Limites de portée

La capture dépend des sources accessibles et autorisées. Une interface graphique opaque, la mémoire arbitraire d’un processus, le déchiffrement TLS, ou la reconstruction universelle d’un programme exigent un adaptateur ou une instrumentation adaptés; ils ne sont pas déclarés obtenus par une simple trace. Les rapports distinguent toujours capture, compilation, reproduction sur entrées vues et généralisation.
