# Guide CLI — eSonde v7

## 1. Fonction et commandes

Le CLI expose une seule fonction conversationnelle : `chat`. `status` et `verify` sont des commandes administratives destinées à inspecter le checkpoint et les contrôles locaux.

```text
python RUN_CLI.py chat --prompt TEXT [options]
python RUN_CLI.py chat --prompt-file FILE [options]
python RUN_CLI.py status [options]
python RUN_CLI.py verify [options]
```

Aucune commande de traduction, de classification, de résumé, de recherche, d'infill ou de traitement de tâches supplémentaires n'est incluse.

## 2. Installation

Prérequis : Python 3.10+. Le chemin de base utilise les bibliothèques standard Python. NumPy est facultatif et accélère les calculs vectorisés. Pas de téléchargement de poids : le checkpoint original se trouve sous `models/eSonde_v6/`.

Linux/macOS :

```bash
python3 --version
./RUN_CLI.sh --help
```

Windows :

```powershell
py -3 --version
RUN_CLI.bat --help
```

## 3. Préflight obligatoire avant chaque chat

Avant de charger et exécuter le modèle, le runtime lit les fichiers suivants dans `suivi_model_eSonde_v7/` (ou `control/suivi_model_eSonde_v7/` en paquet autonome) :

- `chemins_eSonde_v7.json` ;
- `checklist_de_travail_eSonde_v7.json` ;
- `checklist_erreurs_no_model.json` ;
- `checklist_erreurs_model.json` ;
- `sav_eSonde_v7_reference.json` et le manifeste du snapshot référencé.

Il vérifie le statut de phase qui autorise les essais, la présence du snapshot, le hash du manifeste et l'identité SHA-256 du checkpoint actif. En cas d'anomalie critique, l'exécution est bloquée ; la bonne action est de réparer le chemin ou le manifeste puis de relancer le contrôle, jamais de supprimer le garde-fou.

## 4. Options de chat

| Option | Défaut | Description |
|---|---:|---|
| `--prompt TEXT` | — | Prompt UTF-8 direct |
| `--prompt-file FILE` | — | Prompt lu depuis un fichier UTF-8 |
| `--history-file FILE` | aucun | Tableau JSON ordonné de messages `{ "speaker": "user", "text": "..." }` |
| `--min-obsiss N` | `10` | Population de départ pour mesurer la convergence |
| `--n-obsiss N` | population disponible | Plafond maximal de lignes que cette exécution peut activer ; les poids ne sont pas changés |
| `--max-tokens N` | `80` | Longueur maximale de continuation |
| `--beam-width N` | `6` | Nombre maximum de continuations concurrentes |
| `--candidate-limit N` | `16` | Taille visée du pool candidat |
| `--allow-no-response` | désactivé | Active explicitement la politique de non-réponse |
| `--no-char-backoff` | désactivé | Désactive le retour caractère TRAIN |
| `--no-trace` | désactivé | Désactive les traces d'activation détaillées |
| `--output-dir DIR` | `runs_v7/` | Répertoire des traces |
| `--json-out FILE` | stdout | Copie le JSON final dans un fichier |
| `--plain` | JSON | Affiche uniquement la réponse |
| `--model-dir DIR` | checkpoint livré | Répertoire du modèle |
| `--workspace DIR` | détecté | Racine avec checklists et savepoints |

La population démarre à `min(--min-obsiss, population disponible)`. Pour chaque continuation candidate, le moteur calcule P sur le contexte et R sur la continuation candidate, conditionné par P, puis associe les deux états par la même ligne d'Obsiss. Les voix combinent le rang de leurs seize observations et le rang de leur cohérence P/R. La dynamique P et la stabilité de la décision sont contrôlées séparément. Si un critère manque, la population double jusqu'à la satisfaction des critères ou jusqu'au plafond. Un million de lignes n'est pas une cible : `--n-obsiss 10` permet un test strictement limité à dix lignes, tandis que l'absence de l'option laisse le plafond disponible ouvert.

## 5. Exemples

Chat simple, départ à dix avec croissance adaptative autorisée jusqu'au checkpoint disponible :

```bash
python RUN_CLI.py chat --prompt "Explique ce que tu comprends de ma demande."
```

Test explicitement limité à dix Obsiss :

```bash
python RUN_CLI.py chat --prompt "Bonjour" --min-obsiss 10 --n-obsiss 10 --json-out runs_v7/chat_10.json
```

Prompt depuis un fichier :

```bash
python RUN_CLI.py chat --prompt-file prompt.txt --max-tokens 100 --json-out runs_v7/chat.json
```

Dialogue multi-tours avec `history.json` contenant un tableau ordonné d'objets `speaker/text` :

```bash
python RUN_CLI.py chat --prompt "Que devrais-je faire ensuite ?" --history-file history.json
```

Activer volontairement la non-réponse :

```bash
python RUN_CLI.py chat --prompt "Bonjour" --allow-no-response
```

Contrôle d'intégrité :

```bash
python RUN_CLI.py verify --json-out runs_v7/verify.json
```

## 6. Champs du JSON résultat

Le résultat comprend les champs `model`, `version`, `task`, `status`, `prompt`, `response`, `non_response`, `context`, `obsiss`, `generation`, `interpretation`, `preflight`, `execution_evidence` et `savepoint_after_execution`.

`obsiss.convergence` distingue les mesures de stabilité par décision, la dynamique P, l'historique de croissance de population et le statut final. Chaque candidat retenu expose les 16 observations, ses témoins et une empreinte des voix individuelles, plutôt que de sérialiser un million de valeurs flottantes. L'empreinte peut être recalculée de manière déterministe depuis le checkpoint et la trace du candidat. Les scores sont des rangs, pas des probabilités.

## 7. Codes de sortie et erreurs

- `0` : commande terminée et résultat JSON écrit.
- `2` : préflight, chargement, validation ou génération en erreur.

Une erreur est inscrite dans `checklist_erreurs_model.json` et un snapshot post-incident est tenté. Un fichier de sortie vide, une trace interrompue ou un processus terminé par un signal externe doit rester marqué incomplet ; il ne devient pas une réponse valide.

## 8. Sauvegardes, chemins et confidentialité

Les chemins actifs sont indiqués dans `chemins_eSonde_v7.json`. Les snapshots référencés dans `sav_eSonde_v7_reference.json` contiennent les fichiers du runtime et le checkpoint. Les prompts, historiques, réponses et traces peuvent être sensibles : conserver ces fichiers localement et contrôler leur contenu avant partage.

## 9. Dépannage

- `PREFLIGHT_BLOCKED` : lire la cause, les checklists, les chemins et le manifeste ; ne pas désactiver le préflight.
- `FileNotFoundError` : vérifier `--workspace` et `--model-dir`.
- `verify` en échec : comparer les empreintes avec `docs/PROVENANCE_AND_INTEGRITY.md`.
- GUI indisponible : Tkinter ne concerne que la GUI ; le CLI reste autonome.
- Temps d'exécution élevé : commencer par un test plafonné à dix Obsiss, conserver la trace, puis augmenter uniquement sur justification expérimentale.
