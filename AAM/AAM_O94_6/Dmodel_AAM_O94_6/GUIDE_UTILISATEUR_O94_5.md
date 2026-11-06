# Guide d'utilisation AAM O94.5 — ligne de commande et interface graphique

**Version du guide : 20 octobre 2026**

## 1. Préparer et vérifier

Extraire l'intégralité du ZIP modèle dans un dossier d'écriture. Le modèle garde dans ce dossier sa configuration, ses checklists, ses scripts, sa mémoire de travail et son point de sauvegarde incrémental. Utiliser Python 3.11+ compatible avec les dépendances du paquet; disposer de Tk/Tcl pour la GUI. Les outils d'observation facultatifs doivent être installés localement : Tesseract OCR, Poppler (`pdftotext`, `pdfinfo`, `pdftoppm`) et FFmpeg/FFprobe. Le rapport indique quelles voies ont réellement été détectées.

```bash
python scripts/preflight_o945.py
python -m aam_o93 status
python -m aam_o93 --help
```

`preflight` vérifie les documents de phase, registres, hashes et sauvegarde. Ne contournez pas un statut `BLOCKED` : lisez la sortie et consultez `checklist_erreurs_no_model_O94_5.json` ou `checklist_erreurs_model_O94_5.json`.

### Lancer l’application

Linux/macOS : `./run_AAM_O94_5.sh` (à partir du dossier extrait ou en lui donnant le chemin complet). Windows : lancer `run_AAM_O94_5.bat` ou `run_AAM_O94_5.ps1`. Les scripts exécutent le préflight avant de démarrer la GUI. À défaut :

```bash
python -m aam_o93 ui
```

Le chat permet de choisir la compétence et le générateur selon ce que le registre contient, de joindre des fichiers, d'utiliser le RAG et de consulter les diagnostics disponibles. Un modèle qui a échoué à générer doit rester signalé en erreur; le runtime ne doit pas substituer un autre modèle sans l'indiquer.

## 2. Chat et résolution continue

```bash
python -m aam_o93 solve "Résume les différences entre ces deux fichiers" --mode auto --attachment ./document.pdf
python -m aam_o93 solve "Explique le comportement de cette fonction" --mode chat --retrieval-policy auto
python -m aam_o93 resolve-continuously "Corrige et teste le parseur JSON" --max-iterations 12 --seconds 90
```

Pour déclarer un succès *vérifié*, fournir un fichier vérificateur JSON contenant `expected` ou `constraints` via `--verifier-json`. Sans vérificateur explicite, la résolution peut produire une proposition, mais ne doit pas l'étiqueter comme résultat objectivement vérifié. Le budget d'itérations et le timeout limitent une exécution donnée; ils ne sont pas une affirmation sur le potentiel général.

## 3. Observation multimodale et RAG

```bash
python -m aam_o93 observe ./document.pdf
python -m aam_o93 observe ./image.png --modality image
python -m aam_o93 observe ./video.mp4 --modality video
python -m aam_o93 knowledge-ingest ./sources --no-learn
python -m aam_o93 rag-spaces
python -m aam_o93 semantic-search "périodicité de maintenance" --top-k 5
python -m aam_o93 rag-inspect <space_id>
python -m aam_o93 rag-cleanup
```

`observe` écrit des diagnostics et des empreintes; l'extraction OCR est réalisée uniquement si l'outil est disponible. Pour PDF sans couche texte, la voie testée est `pdftoppm → Tesseract` avec limite explicite de pages par passage. Pour l'audio, FFprobe/FFmpeg calculent les métadonnées et caractéristiques acoustiques; une transcription est déclarée seulement si un moteur ASR et ses poids locaux sont configurés. La source est lue sans modification; l'envoi d’un dérivé au RAG est une action distincte et doit être demandé explicitement. `search` est la voie lexicale classique; `semantic-search` lit l'espace sémantique final pondéré.

### Observer un processus ou le système de fichiers en direct

```bash
python -m aam_o93 observe-live --source-kind filesystem --root ./workspace --seconds 20 --interval 1 --max-events 500 --trace-out ./traces/workspace.jsonl
python -m aam_o93 observe-live --source-kind process --pid 1234 --seconds 10 --interval 0.5 --authorize-source
```

Remplacer `1234` par un PID autorisé sur la machine. Le type `network` nécessite `tshark`/`dumpcap` et les autorisations système adaptées. N'inclure ni contenu de fichiers ni charge utile réseau par défaut; activer `--include-file-content`, `--include-packet-payload` ou `--include-raw-pcap` uniquement avec une autorisation précise, un budget et une politique de données appropriée.

## 4. Charger SmolLM2 ou un modèle Transformers local

L'unité de chargement est un *bundle* complet, pas le nom du modèle ni le fichier de poids seul. Le dossier doit notamment contenir une configuration `config.json`, des poids compatibles (`model.safetensors`, shards/index ou format pris en charge), et les métadonnées/tokenizer nécessaires. Le registre accepte la sélection du fichier `model.safetensors`, résout son dossier parent, inventorie les fichiers et calcule leurs SHA-256. Il refuse une génération si des fichiers manquent ou si leur contenu change après enregistrement.

1. Copier `examples/model_integration/transformers-local.json` vers un fichier de configuration personnel.
2. Définir `model_id` de manière unique et remplacer `local_path` par le dossier réel de SmolLM2 (ou son fichier de poids dans ce dossier).
3. Installer les dépendances optionnelles dans l'environnement Python voulu; installer la roue PyTorch correspondant au CPU/CUDA/MPS de la machine séparément si nécessaire.
4. Enregistrer et inspecter le statut :

```bash
python -m pip install -r requirements-transformers.txt
python -m aam_o93 model-register ./smollm2-local.json
python -m aam_o93 models-list
python -m aam_o93 model-generate smollm2-local "Écris une phrase de test" --tokens 96
python -m aam_o93 solve "Réponds en français" --mode chat --language-model smollm2-local
```

Adapter le nom `smollm2-local` à la valeur exacte de `model_id` déclarée. `model-register` peut conserver un bundle incomplet comme brouillon diagnostique; seul `READY_LOCAL_BUNDLE` est chargeable. Un checkpoint `.pt`/`.pth` contenant seulement un `state_dict` n’est pas universel : l’architecture et la configuration compatibles doivent être connues; le chargeur strict refuse les clés manquantes ou inconnues et ne permet pas le chargement pickle arbitraire. TorchScript suit un backend séparé. Les adaptateurs Python/PyTorch lancent du code exécutable; n’approuver qu'un fichier inspecté et isoler au niveau OS tout code non fiable. `trusted_local_code_confirmed=true` n’est pas un bac à sable.

**Portée testée de cette livraison :** la résolution de bundle, le registre, les contrôles de hash, les paramètres de chargement local et les contrats de génération ont 15 tests ciblés réussis. Les poids SmolLM2 réels n'étaient pas disponibles dans l'environnement de construction et Transformers ne pouvait pas être installé faute d'accès à l’index. La génération sur ton dossier réel reste donc à exécuter sur la machine qui détient les vrais fichiers; cette limite est ouverte dans le registre d'incidents.

## 5. Entraînement des modèles et apprentissage de compétences

Pour un modèle compact interne/capsule linguistique :

```bash
python -m aam_o93 train-language-model ./corpus --epochs 5 --max-vocab 256 --dim 64 --context-size 5
```

Par défaut toutes les fenêtres disponibles sont traitées. Pour un modèle Transformers enregistré avec une `training_policy` de type `transformers_lora`, utiliser un dataset supervisé avec champs réels et splits train/validation/holdout explicités :

```bash
python -m aam_o93 model-train smollm2-local ./train.jsonl --input-key input --target-key target --split-key split --epochs 2
```

La méthode dépend de `training_policy` et de l’architecture déclarée. Les politiques `inference_only` ne modifient pas les poids; `export_supervised_pairs` prépare un export mais ne constitue pas un entraînement; LoRA requiert une configuration modèle compatible et les modules cibles correspondants. Une exécution d'entraînement n’est pas déclarée concluante sans évaluation sur le holdout. Le mécanisme `acquire-skill` d'AAM et l’entraînement des poids LLM sont des opérations différentes.

## 6. Programmer par composition et compiler

L'exemple versionné est `examples/compositions/O94_5/project_compilation_audit.json`. Il utilise uniquement les composants inscrits au catalogue : validation de requête, opérations de l'atelier, branches/itérations autorisées et scellement de résultat.

```bash
python -m aam_o93 composition-save o945_project_audit examples/compositions/O94_5/project_compilation_audit.json
python -m aam_o93 composition-list
```

Pour exécuter la composition, créer un fichier JSON d'entrée dont les champs correspondent au DSL, notamment `workspace` pointant vers un projet jetable ou autorisé; consulter le manifeste et les fichiers de spécification du projet avant de lancer `composition-run`. La chaîne de compilation valide le JSON, émet du Python déterministe, compile le source/bytecode CPython et écrit des hashes/manifeste; l’exécution contrôle l'autorisation, le délai et la sortie. Les fragments Python arbitraires sont refusés. Un composant d'exécution de programme projet ne doit pas être appelé sans consentement.

L'éditeur intégré offre ouverture multi-onglets, coloration, sauvegarde atomique, détection des conflits externes, recherche/remplacement, création/édition de fichiers, compilation de projet, diagnostics ligne/colonne et test autorisé. Le test de projet compile le vrai code du répertoire. Le compilateur LaTeX appelle un moteur réel (si `pdflatex`/`latexmk` est installé), vérifie le PDF et conserve le hash de la source avant/après.

## 7. Récompense/punition, mémoire et autonomie

```bash
python -m aam_o93 feedback <task_id> satisfied --comment "réponse vérifiée et utile"
python -m aam_o93 feedback <task_id> partial --comment "bonne structure, source manquante"
python -m aam_o93 feedback <task_id> unsatisfied --comment "la solution ne passe pas le test"
python -m aam_o93 autonomy --help
```

Le système distingue préférence utilisateur, fiabilité d'exécution et résultat vérifié indépendant. Un timeout ou une exception peut diminuer la fiabilité de la compétence effectivement utilisée; il ne prétend pas prouver que sa réponse est fausse. Un signal `UNRESOLVED` n’est pas une punition automatique. Les événements sont rattachés à une tâche, hashés et dédupliqués pour éviter d'appliquer deux fois le même feedback. L'autonomie est orchestrée par le runtime et peut être configurée; l'enregistrement de mémoire et son contenu peuvent être inspectés/limités selon les réglages de confidentialité.

## 8. Diagnostics, preuves, restauration

- `checklist_de_travail_O94_5.json` : ordre séquentiel et critères de sortie.
- `checklist_erreurs_model_O94_5.json` : défauts de comportement du modèle.
- `checklist_erreurs_no_model_O94_5.json` : incidents d'environnement, harnais, preuves ou données absentes.
- `registre_prouves_O94_5.json` et `O94_5_TEST_MATRIX.json` : traçabilité fonction → source → test → reçu → statut.
- `sav_AAM_O94_5/savepoint_manifest.json` : manifeste SHA-256 du delta O94.5 et lien avec le parent O94.4 figé.

Vérifier la sauvegarde sans modifier le projet :

```bash
python scripts/restore_o945_savepoint.py
```

La restauration n’est pas automatique. Pour remplacer les fichiers suivis à partir du snapshot après avoir fait une copie de sûreté :

```bash
python scripts/restore_o945_savepoint.py --restore
```

Le script refuse les chemins absolus, `..`, les répertoires de sauvegarde internes et toute entrée de manifeste non sûre. Les fichiers remplacés sont copiés dans `restore_backups/` avant la restauration.

## 9. Statut et limites restantes

P0–P6 disposent de reçus; P7 traite la documentation/la restauration; P8 contrôle les archives finales. La réussite de la suite complète est établie pour les tests présents (419 passés, 0 échec, 5 avertissements). Elle ne certifie pas tous les modèles distants, toutes les architectures PyTorch, la transcription sans modèle ASR, le réseau physique ou la reproduction exacte/générale de tout objet. Ces voies ont des contrats explicites, budgets, états non résolus et critères de qualification; aucune limite d'environnement n’est transformée en conclusion sur le potentiel futur du modèle.
