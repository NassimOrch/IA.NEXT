# eLLM_v1 — LLM préentraîné + empreintes observationnelles apprises

## Fonction réelle du système

eLLM_v1 n'est pas le n-gramme d'eLLM_v0. Il enveloppe un checkpoint causal préentraîné compatible Transformers (par défaut `HuggingFaceTB/SmolLM2-135M-Instruct`) et apprend conjointement un adaptateur d'observation multi-résolution. Les sondes prennent les états cachés contextualisés; leurs familles sont emboîtées; une correction dérivée de leurs empreintes entre dans les logits et reçoit une perte prédictive multi-résolution. Les signatures quantifiées définissent un protocole d'indiscernabilité explicite, distinct des réponses continues.

Le code ne remplace jamais un checkpoint manquant par des poids aléatoires, un n-gramme ou un modèle de substitution. Les poids externes ne sont pas inclus dans le ZIP; ils doivent être téléchargés sur le PC de l'utilisateur. L'environnement de construction qui a produit cette archive ne disposait pas d'une résolution DNS fonctionnelle vers le dépôt de modèle; cette absence est enregistrée dans l'audit. Le téléchargement, le chargement et l'entraînement réels doivent être exécutés sur une machine disposant des dépendances et de l'accès au dépôt choisi.

## Installation

Nécessite Python 3.10+ et une connexion réseau pour installer les dépendances et télécharger les poids. Sous Windows, macOS ou Linux, depuis ce répertoire :

```bash
python setup_eLLM_v1.py
python run_eLLM_v1.py status
python run_eLLM_v1.py download-model --model-id HuggingFaceTB/SmolLM2-135M-Instruct --revision ee72e5415c002e8fc0566a191a07c0b2b708875a
python run_eLLM_v1.py serve --host 127.0.0.1 --port 8765
```

Ouvre `http://127.0.0.1:8765`. Le serveur écoute sur loopback par défaut; ne l'expose pas à un réseau partagé sans ajouter une authentification et une politique d'accès adaptées.

### SmolLM2 déjà présent localement

Si le checkpoint est déjà sur ce PC, tu peux éviter un nouveau téléchargement :

1. Lance le serveur sur **le même PC qui contient les poids**.
2. Ouvre **Réglages → Checkpoint préentraîné**.
3. Garde `HuggingFaceTB/SmolLM2-135M-Instruct` et le commit épinglé si ton dossier correspond exactement à cette révision officielle.
4. Saisis le chemin absolu du dossier contenant `config.json`, le tokenizer et les poids, puis clique **Importer le checkpoint local**.
5. L’import vérifie les fichiers, écrit un manifeste SHA-256 et copie le modèle par staging. Un remplacement différent exige la case de confirmation; l’ancienne copie est conservée.

Pour le modèle officiel épinglé, le fichier `model.safetensors` doit avoir le SHA-256 publié attendu. Un checkpoint quantifié, shardé différemment ou provenant d’une autre révision ne sera pas présenté comme la révision officielle épinglée. Pour un autre modèle compatible, modifie explicitement l’identifiant et la révision; le manifeste attestera alors l’intégrité locale, pas l’authenticité auprès d’un registre externe. Si l’interface indique que le checkpoint est importé mais non chargé, exécute `python setup_eLLM_v1.py`, actualise l’état puis relance le chargement; aucun backend de substitution n’est utilisé.

### Vérification réelle sur le PC qui contient SmolLM2 (gate P07)

Le conteneur de construction ne peut pas lire le disque de ton PC. Pour enregistrer une preuve de l'inférence réelle, utilise le script `tools/validate_local_checkpoint_eLLM_v1.py` sur le même ordinateur que le checkpoint. Il ne télécharge pas les poids et n'installe rien en silence; il écrit un rapport JSON même en cas de manque de dépendances ou d'erreur de provenance.

D'abord, installe les dépendances une fois :

```bash
python setup_eLLM_v1.py
```

Smoke test de l'inférence réelle, en remplaçant le chemin par le dossier qui contient `config.json`, les poids et le tokenizer :

```bash
python tools/validate_local_checkpoint_eLLM_v1.py \
  --checkpoint-dir "C:/Models/SmolLM2-135M-Instruct" \
  --root "./ellm_v1_data"
```

Le script vérifie le checkpoint local, contrôle son manifeste et son identité, charge le vrai modèle, génère une réponse déterministe courte et enregistre le résultat sous `ellm_v1_data/outputs/`. Il ne marque pas l'inférence comme réussie si le modèle n'a pas effectivement été chargé.

Pour exécuter ensuite le fine-tuning et l'évaluation réservée sur le Parquet fourni :

```bash
python tools/validate_local_checkpoint_eLLM_v1.py \
  --checkpoint-dir "C:/Models/SmolLM2-135M-Instruct" \
  --root "./ellm_v1_data" \
  --train \
  --dataset "training_data/provided_sources/0000.parquet" \
  --config "examples/training_config_lora_1epoch.json" \
  --mapping "examples/mapping_question_answer.json"
```

Ce profil à une époque constitue un run initial de vérification du pipeline, pas un plafond imposé : modifie les paramètres JSON pour tes expériences complètes, en conservant les résultats précédents. Le rapport contient l'identité du checkpoint, le hash du dataset avant/après, la configuration, les événements, la sélection validation, les métriques du test réservé et la comparaison empreinte activée/désactivée. Les quatre fichiers sources fournis sont inclus byte-identiques dans `training_data/provided_sources/`; leur manifeste SHA-256 y est joint.

## Entraînement

Dans l'écran **Entraîner le modèle** : sélectionne ou importe un dataset, inspecte le rapport d'import, mappe explicitement les champs conversation/texte/prompt/cible/label/ID, règle le modèle et les hyperparamètres, puis lance le job. L'historique d'entraînement, les partitions, les erreurs et les checkpoints sont persistés sous `logs/` et `checkpoints/`. La sélection du meilleur epoch est fondée sur validation; le test réservé est évalué une fois la sélection terminée. La comparaison empreinte activée/désactivée utilise les mêmes poids sélectionnés.

Les formats pris en charge sont JSONL, JSON, CSV, TSV, TXT, Markdown, ZIP et Parquet. Si une ligne est invalide, elle est comptée et reportée par numéro de ligne et hash; le fichier brut n'est jamais réécrit automatiquement. Le zip SMS d'origine contient un membre historique sans extension, traité comme TSV sans en-tête (label, texte).

## Chat et historique

Le chat est local et sauvegardé en SQLite dans `sessions/history.sqlite3`. Les conversations peuvent être recherchées, renommées, supprimées et exportées en JSON. Si le checkpoint est absent, l'interface garde le message utilisateur dans l'historique mais n'invente pas de réponse de modèle.

## CLI

```bash
python run_eLLM_v1.py status
python run_eLLM_v1.py inspect-model
python run_eLLM_v1.py chat
python run_eLLM_v1.py train --dataset training_data/raw/dataset/Screenplay_dataset.jsonl
python run_eLLM_v1.py selftest -v
```

`train --dataset` utilise les valeurs par défaut si aucun `--config` ou `--mapping` JSON n'est fourni; pour des sources hétérogènes, définir le mapping explicitement. En mode complet, la consommation RAM/VRAM et le temps dépendent du checkpoint, de la séquence, du batch et du matériel. Aucun paramètre ne prétend lever les limites physiques du matériel; on expose des réglages, des erreurs et des checkpoints de reprise au lieu de substituer silencieusement un autre modèle.

## Preuves théoriques et portée

Le source `reference/DDD_Base_theorie_des_empreintes_complete_order_5.tex` est conservé sans modification. `ellm_v1/theory.py` implémente des constructions sur domaines finis et signatures quantifiées : partitions, raffinement, seuil et statut de bord, ultramétrique dérivée corrigée avec diagonale nulle, fermeture, facteurisation, capacité effective, dimension affine, compatibilité de transition et contraintes déclarées. Ces tests prouvent seulement les propriétés définies sur les objets fournis; ils ne certifient pas une sémantique universelle.

## Dépendances et tests

```bash
python setup_eLLM_v1.py --check-only
python run_eLLM_v1.py selftest -v
node --check web/app.js
```

Les tests unitaires des composants peuvent tourner sans télécharger le checkpoint; les tests de génération, fine-tuning et UI reliée à un vrai modèle nécessitent les poids locaux. Cette distinction est volontaire et documentée.
