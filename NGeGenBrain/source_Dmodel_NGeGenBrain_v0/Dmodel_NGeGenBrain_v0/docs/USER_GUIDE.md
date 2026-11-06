# Guide utilisateur complet — NGeGenBrain_v0

## 1. Installation et premier lancement

Le projet est fourni en code source Python, sans dépendance PyPI. Installez Python 3.11+ puis extrayez l'archive dans un dossier permanent. N'exécutez pas le projet depuis un dossier temporaire. Les fichiers `.bat` utilisent `%LOCALAPPDATA%\NGeGenBrain_v0` pour les données persistantes. Sur Linux/macOS, choisissez explicitement un dossier permanent avec `NGEGB_HOME`.

### Linux/macOS

```sh
python3 ngbrain.py init
python3 ngbrain.py status
python3 ngbrain.py serve --host 127.0.0.1 --port 8765
```

Ouvrir `http://127.0.0.1:8765/`. `Ctrl+C` arrête le serveur. Ne configurez pas une adresse publique : le serveur intégré est volontairement lié à loopback.

### Windows

- `launch_NGeGenBrain_v0.bat` : démarre le serveur et ouvre le navigateur.
- `run_web_NGeGenBrain_v0.bat` : démarre uniquement le serveur.
- `ngbrain_NGeGenBrain_v0.bat <commande...>` : transmet les commandes au CLI.
- `test_NGeGenBrain_v0.bat` : lance la suite de tests avec les avertissements de ressources transformés en erreurs.

Les scripts préfèrent `runtime\python314\python.exe` lorsqu’il existe, puis vérifient `py -3` et `python` (version 3.11+). Ils ne téléchargent rien au lancement. Pour un Windows x64 sans Python global, exécutez une fois `powershell -ExecutionPolicy Bypass -File tools\bootstrap_python_windows.ps1` avec accès Internet : le script télécharge l’archive officielle Python 3.14.10, vérifie le SHA-256 officiel puis la configure. Ce script n’a pas pu être exécuté dans ce conteneur Linux sans accès DNS à python.org ; son fonctionnement Windows reste à vérifier sur une machine Windows réelle. En environnement hors-ligne, Python 3.11+ doit déjà être installé.

## 2. Architecture de l'interface web

L'interface est composée de panneaux navigables, d'un espace conversationnel, d'un inspecteur de résultats et d'un explorateur de toutes les actions. Les sections couvrent le chat, les programmes/AST, les composants, le maillage, les certificats et traces, la mémoire/checkpoints, l'exploration/recherche, la synthèse, ASCRC, les modèles du monde, les intentions/langage et l'état du système.

L'explorateur charge le catalogue canonique `ACTION_DESCRIPTORS` depuis `/api/actions`. Toute action listée peut être envoyée via le même endpoint `/api/action`. Ce mécanisme fournit la parité des opérations métier : le CLI `action ACTION_ID` et l'interface web appellent le même `ActionService`. Les commandes de contrôle de processus telles que `serve` restent des commandes de démarrage, pas des actions métier à exécuter depuis une page Web.

## 3. CLI : commandes de contrôle

```text
python ngbrain.py init
python ngbrain.py status
python ngbrain.py actions
python ngbrain.py verify
python ngbrain.py test
python ngbrain.py demo
python ngbrain.py serve --host 127.0.0.1 --port 8765
python ngbrain.py run --program FILE.json [--input JSON] [--capabilities JSON] [--budget JSON]
python ngbrain.py action ACTION_ID [--data JSON | --file PAYLOAD.json]
```

- `init` : crée/met à jour le schéma et le registre natif de façon idempotente.
- `status` : santé, compteurs et informations de base.
- `actions` : catalogue exhaustif d'actions, avec identifiants, descriptions et exemples.
- `verify` : intégrité SQLite, clés étrangères et chaîne des événements.
- `test` : suite `unittest` livrée avec le code.
- `demo` : démonstration isolée, sans utiliser la base principale pour ses données de démonstration.
- `serve` : serveur HTTP local.
- `run` : exécution d'un AST JSON, avec capacités et budgets explicites.
- `action` : invocation d'une fonction du registre partagé par CLI/API/web.

Sélectionner la même base de données dans les interfaces est nécessaire pour partager les mêmes données. CLI accepte `--db PATH`; les scripts Windows définissent `NGEGB_HOME`.

## 4. Actions métier disponibles

Les noms exacts sont générés depuis le registre du runtime ; utilisez `python ngbrain.py actions` plutôt qu'une copie possiblement périmée de la liste. Le registre est partagé et groupé par domaine :

- **Système/données** : initialisation, santé, statistiques, auto-test, démonstration, vérification SQLite, baux et déploiements staged.
- **Composants/programmes** : lister/enregistrer les composants et compositions, exécuter une composition, exécuter un AST, transformation structurelle.
- **Maillage** : ajouter/interroger des faits typés, ajouter/lister des règles multi-prémisses, clôture d'inférence bornée et validation de certificat.
- **Traces/preuves** : lister et inspecter les événements, vérifier la chaîne append-only.
- **Mémoire** : ajouter/lire/lister des objets, veille/réveil, cycle de vie, checkpoints et révocation transitive.
- **Événements** : émettre/recevoir des vagues typées, déduplication et TTL.
- **ASCR-NG/ASCRC** : recherche de candidats, admission, classement, ordonnanceur persistant et métriques d'attente.
- **Synthèse** : chercher des programmes candidats et reprendre une session enregistrée.
- **Modèles du monde** : enregistrer une transition pure, simuler un pas et évaluer une politique contre une baseline sur un holdout séparé.
- **Intentions/chat** : définir des motifs/slots typés, lister les intentions et soumettre un message au résolveur contrôlé.

Pour voir les champs exigés d'une action, ouvrez le catalogue JSON de `ngbrain actions`, consultez sa valeur `example`, ou sélectionnez-la dans l'explorateur web. Les payloads sont des objets JSON. Pour les payloads volumineux, préférez `--file` plutôt qu'un argument de shell.

## 5. Exemples de programmes

### Addition exacte via un opérateur enregistré

Fichier `examples/add.json` :

```json
{"op":"Call","component":"add","args":[2,4]}
```

Exécution :

```sh
python ngbrain.py run --program examples/add.json --input null --capabilities '[]' --budget 1000
```

### Séquence de deux étapes

```json
{
  "op":"Seq",
  "steps":[
    {"op":"Call","component":"add","args":[2,4]},
    {"op":"Call","component":"multiply","args":[{"var":"input"},3]}
  ]
}
```

La portée exacte des variables et les chemins attendus sont définis par le constructeur. Pour un programme métier non trivial, vérifiez d'abord l'exemple via `program.run` et l'AST dans un fichier JSON. Le runtime n'interprète pas de fragment Python arbitraire.

## 6. Faits, règles et certificats

Ajouter un fait :

```sh
python ngbrain.py action mesh.fact.add --data '{"subject":"A","predicate":"edge","object":"B","status":"observed","type_subject":"Entity","type_object":"Entity","provenance":{"source":"manual"}}'
```

Ajouter une règle de transitivité explicite :

```json
{
 "rule": {
   "id":"transitive-edge", "version":"1.0.0",
   "premises":[
     {"subject":{"var":"x"},"predicate":"edge","object":{"var":"y"}},
     {"subject":{"var":"y"},"predicate":"edge","object":{"var":"z"}}
   ],
   "conclusions":[{"subject":{"var":"x"},"predicate":"edge","object":{"var":"z"}}]
 }
}
```

Enregistrer ce contenu dans `rule.json`, puis lancer `python ngbrain.py action mesh.rule.add --file rule.json`, suivie de `python ngbrain.py action mesh.infer --data '{}'` et `mesh.fact.query`. La transitivité n'est pas implicite. Les faits `observed`, `derived` et `assumed` restent distincts. Les certificats sont reconstruits à partir des prémisses/règles actives, et pas seulement validés par un hash.

## 7. Mémoire, veille et révocation

`memory.put`, `memory.get`, `memory.list`, `memory.state`, `memory.hibernate`, `memory.wake`, `checkpoint.create`, `checkpoint.get`, `memory.revoke` sont les opérations principales. Les payloads exacts gardent leur hash et leurs dépendances. Les résumés approximatifs doivent référencer la source ; la veille ne certifie pas un objet et le réveil ne rend pas une donnée périmée automatiquement valide. Une révocation met les descendants connus à revalider/invalidés avant leur réutilisation certifiée.

## 8. Recherche ASCR-NG et régulation ASCRC

`ascr.search` classe des candidats à partir d'indices de récupération. Cette réimplémentation prend le rôle de retrieval décrit dans les références disponibles, mais n'affirme pas l'équivalence exacte avec le runtime historique absent. Ses scores ne sont jamais une preuve de vérité.

`ascrc.evaluate`, `ascrc.order`, `ascrc.schedule`, `ascrc.candidates.list` contrôlent l'admission opérationnelle. Les conditions dures de type, contrat, capacités, fraîcheur et coût précèdent le score heuristique. L'état épistémique n'est pas changé par une priorité, une mise en attente ou une veille. Les budgets CPU/mémoire/I/O du planificateur sont des unités déclarées et non des mesures physiques OS ; les journaux les nomment comme estimations/allocation.

## 9. Synthèse et reprise

`synthesis.run` reçoit un objectif structuré, des exemples d'entrée/sortie et un budget ; `synthesis.resume` reprend la session persistée. Les candidats sont étiquetés `EXAMPLE_CONSISTENT_NOT_UNIVERSALLY_PROVED`. La recherche n'accède pas à un oracle de scoring caché ni ne transforme l'accord avec des exemples en certificat universel. Reprise déterministe et budget sont enregistrés avec la session.

## 10. Modèles du monde

Enregistrer une transition pure :

```json
{
  "definition": {
    "id":"increment-model", "version":"1.0.0",
    "transition_program":{"op":"Call","component":"add","args":[{"path":["state"]},{"path":["action"]}]},
    "state_type":"Number", "action_type":"Number", "output_type":"Number",
    "activation_policy":{"min_samples":5,"min_gain":0.05,"z_score":1.96}
  }
}
```

Prédiction : `world_model.predict` avec `id`, `state`, `action`. Résultat marqué `SIMULATED`, `is_observed=false`, `is_certified=false`. L'évaluation (`world_model.evaluate`) impose baseline et holdout ; la cible `observed_next_state` n'est pas fournie aux prédicteurs avant leur exécution. La porte d'activation est statistique et descriptive, dépend de l'indépendance/représentativité de l'holdout, et n'est pas une preuve générale de validité.

## 11. Intentions et langage conversationnel

Une intention est un motif littéral avec slots typés (`Number`, `Integer`, `Word`, `Text`, `Bool`, `Rest`) et un AST déclaratif. Exemple :

```json
{"definition":{"id":"add-words","pattern":"add {left:Number} and {right:Number}","program":{"op":"Call","component":"add","args":[{"path":["slots","left"]},{"path":["slots","right"]}]}}}
```

Enregistrer via `intents.register`. Ensuite envoyer `{"message":"add 2 and 4"}` à `chat.submit` ou dans le chat web. C'est un résolveur extensible et typé de motifs ; ce n'est pas une affirmation que toute phrase en langage naturel est automatiquement comprise. Les ambiguïtés restent non résolues et sont présentées avec leurs candidats ; les capacités ne sont pas octroyées par l'interprétation d'un message.

## 12. Erreurs, statuts et diagnostic

Les statuts `Success`, `Partial`, `Unresolved`, `Rejected`, `Failed` et `Cancelled` doivent être lus tels quels. Une sortie partielle/inconnue/rejetée n'est pas un succès. `NOT_RUN`, budget épuisé, objet `STALE`, ou candidat de synthèse non prouvé ne signifie ni capacité absente ni réfutation du modèle.

Diagnostic :

```sh
python ngbrain.py status
python ngbrain.py verify
python ngbrain.py action system.actions
python ngbrain.py action trace.list --data '{"limit":50}'
python ngbrain.py action mesh.certificate.verify --file certificate.json
python ngbrain.py test
```

Le dossier `logs/` de l'archive de suivi conserve également les défaillances de construction et de test historiques, y compris celles corrigées. Le rapport d'audit ne supprime pas un échec antérieur : il indique sa résolution et son test de non-régression.

## 13. Limites d'environnement et sauvegarde

Le serveur web intégré n'expose qu'un service loopback et n'est pas un serveur multi-utilisateur durci pour Internet. Les actions composables n'exécutent pas arbitrairement du code natif ; de telles capacités nécessitent des adaptateurs/plugins explicites dans la frontière de confiance. Le runtime d'origine ASCR/AAM n'était pas présent dans les sources disponibles : le rôle retrieval est reconstruit avec traçabilité, pas annoncé comme identique à une ancienne version inconnue.

Sauvegarder la base en arrêtant les écritures puis en copiant le fichier SQLite, ou utiliser une procédure SQLite cohérente ; ne copier pas seulement le `.sqlite3` pendant qu'un WAL est actif sans vérifier les journaux associés. Conserver séparément la clé d'identité si une extension cryptographique future en introduit une.


## 14. Bootstrap Windows

Si aucun Python 3.11+ n'est installé, exécuter `powershell -NoProfile -ExecutionPolicy Bypass -File tools\bootstrap_python_windows.ps1`. Le script récupère l'embeddable Python 3.14.10 x64 officiel, vérifie son SHA-256 avant extraction et l'installe dans `%LOCALAPPDATA%\NGeGenBrain_v0\runtime`. L'opération nécessite Internet et PowerShell. Les scripts Windows ont été validés statiquement mais pas exécutés nativement dans l'environnement Linux de génération.
