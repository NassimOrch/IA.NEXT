# Référence CLI — eSonde v3

## 1. Prérequis et exécution

Python 3.10+ ; bibliothèque standard seulement pour le runtime. Depuis la racine du dossier livré :

```bash
python run_esonde.py --version
python run_esonde.py --help
python run_esonde.py <commande> --help
```

Alternative : `PYTHONPATH=src python -m esonde --help`. L'installation `pip install .` est facultative. Les wrappers sont `run_esonde_cli.sh` et `run_esonde_cli.bat`.

## 2. Corpus et règles de séparation

Les dossiers sont parcourus récursivement et de façon déterministe. Les suffixes reconnus sont `.txt`, `.text`, `.md`, `.rst`, `.csv`, `.tsv`, `.jsonl`. Les chemins de fichier donnés directement sont lus en UTF-8. Un document est identifié par identifiant, étiquette de chemin et SHA-256 du texte. Train, validation et test doivent être disjoints par identifiant et contenu. La validation calibre uniquement COORD ; `score` est read-only et refuse les contenus déjà connus.

## 3. Création et entraînement

```bash
python run_esonde.py train \
  --corpus ./corpus/train \
  --validation ./corpus/validation \
  --config ./examples/training_config.json \
  --output ./models/model.json
```

`--validation` est facultatif ; sans validation, le modèle est marqué non calibré. `--config` doit être un objet JSON dont les clés appartiennent au schéma du runtime. Le résultat JSON décrit le nombre de documents/tokens, les supports par famille, la calibration et les empreintes écrites (`model.json` et `model.json.sha256`).

La commande `demo` entraîne sur les petits textes neutres livrés :

```bash
python run_esonde.py demo --output ./models/demo.json
```

Cette démo valide l'exécution ; elle ne constitue pas un entraînement généraliste.

## 4. Mise à jour, calibration et retrait exact

```bash
python run_esonde.py update --model ./models/model.json \
  --corpus ./corpus/new_batch --batch-id batch-2026-01 \
  --validation ./corpus/validation --output ./models/model_updated.json

python run_esonde.py calibrate --model ./models/model_updated.json \
  --validation ./corpus/validation --output ./models/model_calibrated.json

python run_esonde.py remove-batch --model ./models/model_updated.json \
  --batch-id batch-2026-01 --output ./models/model_without_batch.json
```

Les lots ajoutés doivent être nouveaux par ID et SHA-256. Le retrait exact reconstruit l'état en rejouant les lots conservés depuis le registre source embarqué. Les checkpoints historiques v2 sans historique complet refusent le retrait exact. Les checkpoints récents stockent les textes nécessaires à la reconstruction : protégez-les comme les corpus d'origine.

## 5. Génération

```bash
python run_esonde.py generate --model ./models/model.json \
  --prompt "Les observations indiquent" --max-tokens 32 \
  --strategy greedy --seed 0 --top-k 40

python run_esonde.py generate --model ./models/model.json \
  --prompt-file ./prompt.txt --max-tokens 64 --strategy sample --seed 11 --plain
```

`--prompt` et `--prompt-file` sont mutuellement exclusifs et l'un est requis. `greedy` choisit le candidat en tête ; `sample` échantillonne avec la graine donnée. Sans `--plain`, la CLI affiche la trace JSON. La recherche BYTE peut proposer des chaînes hors vocabulaire lexical ; le beam est une recherche de candidats approximative, alors que le score de chaque chaîne évaluée utilise la loi BYTE normalisée.

## 6. Évaluation

```bash
python run_esonde.py score --model ./models/model.json \
  --corpus ./corpus/test --top-k 5 --output ./results/score.json
```

Sorties : statut, cibles évaluées, log-loss/perplexité, précision top-k, résultats par document et diagnostics de contexte tronqué. Il s'agit d'une évaluation next-token, pas automatiquement d'un benchmark QA/EM/F1.

Le script distinct `scripts/evaluate_mlqa_next_token.py` utilise l'archive MLQA fournie par l'utilisateur via `--mlqa-zip` ; le dataset brut n'est pas inclus dans le paquet Dmodel. L'expérience actuelle est explicitement diagnostique et rapportée dans `docs/VALIDATION_V3.md`.

## 7. Récupération et sémantique composée

```bash
python run_esonde.py retrieve --model ./models/model.json \
  --query "solar energy storage" --top-k 5

python run_esonde.py relations --model ./models/model.json \
  --left "solar cells" --relation "produce" --right "electricity" --top-k 20

python run_esonde.py coref --model ./models/model.json \
  --text "Alice met Bob. Alice returned." --top-k 20
```

`retrieve` retourne les contextes mémorisés avec provenance disponible. `relations` expose les motifs observés sous forme A–relation–B. `coref` expose des candidats de mention/alias avec preuves et ne marque pas une résolution unique (`resolved=false`). Ni l'une ni l'autre fonction n'est un parseur sémantique complet ou un résolveur pronominal général.

## 8. Inspection, audit et informations

```bash
python run_esonde.py inspect --model ./models/model.json --family BYTE
python run_esonde.py inspect --model ./models/model.json --family COORD
python run_esonde.py audit --model ./models/model.json --output ./results/audit.json
python run_esonde.py info --model ./models/model.json
```

Familles admises : `SEQ`, `SKIP_REL`, `MORPH`, `SEM`, `DISC`, `RETR`, `BYTE`, `COORD`. `--key` d'`inspect` sélectionne une clé sérialisée exacte. `audit` exécute l'audit statique de pureté et l'inspection d'état ; un résultat d'audit avec finding retourne le code `3`.

## 9. Paramètres de configuration

`examples/training_config.json` donne les valeurs versionnées. Les paramètres admis sont :

| Paramètre | Rôle |
|---|---|
| `max_context` | plafond global ; `0` désactive ce plafond additionnel |
| `seq_max_order`, `seq_decay` | ordre et décroissance SEQ |
| `skip_patterns` | paires d'offsets positives SKIP_REL |
| `morph_recent_words` | fenêtre MORPH |
| `sem_window` | fenêtre SEM |
| `disc_window`, `disc_recent_cutoff` | mémoire DISC et exclusion du suffixe récent |
| `retrieval_context_window`, `retrieval_budget`, `retrieval_top_k` | contexte et budget RETR |
| `coordinator_smoothing`, `calibration_sample_limit` | lissage et budget de calibration COORD |
| `byte_order`, `byte_alpha`, `byte_max_bytes`, `byte_candidate_count` | ordre/backoff, lissage, longueur UTF-8 maximale et propositions BYTE |
| `tokenizer_version` | tokenizer 2 historique ou 3 (repli CJK/Hangul par caractère) |

Toute clé inconnue, valeur booléenne utilisée comme entier, valeur non finie ou motif invalide est refusé.

## 10. Intégrité et sauvegardes

Chaque checkpoint est un JSON canonique avec SHA-256 du payload et du fichier, plus un sidecar `.sha256`. Ne supprimez pas un sidecar invalide et ne le recréez pas à partir d'un JSON non fiable. Avant une mise à jour, copiez le modèle et ses sidecars. Le runtime écrit atomiquement le JSON de sortie et son sidecar.

## 11. Codes de retour

- `0` : opération terminée.
- `2` : erreur d'argument, chemin, encodage, configuration, split ou état.
- `3` : l'audit détecte un finding de pureté.

Les erreurs sont écrites sur stderr. Un code `0` prouve seulement l'exécution de la commande, pas la qualité linguistique du texte produit.
