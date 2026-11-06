# Guide d'utilisation AAM O94.4 — CLI et interface graphique

## 1. Préparation et contrôle préalable

Décompresser `Dmodel_AAM_O94_4.zip` dans un dossier dédié. Utiliser Python 3.11+ de préférence et installer les dépendances du profil désiré. Certaines fonctions ont des dépendances optionnelles (PyTorch, Transformers, psutil, TShark); elles donnent un diagnostic clair lorsqu'elles ne sont pas présentes. Depuis le dossier extrait :

```bash
python -m aam_o93 preflight
python -m aam_o93 status
```

La commande `preflight` vérifie les formalismes, checklists héritées, registres d'erreurs et savepoints O94.3/O94.4. Ne lancer les opérations de changement que si le statut est `PASS_BOUNDED`.

## 2. Démarrage de l'interface graphique

Sous Windows, lancer `run_AAM_O94_4.bat` ou `run_AAM_O94_4.ps1`; sous Linux/macOS, `run_AAM_O94_4.sh`. Les lanceurs O94.3 restent disponibles pour compatibilité. Autre possibilité : `python -m aam_o93 ui` depuis la racine du paquet. La boucle autonome démarre avec le runtime par défaut et s'arrête à la fermeture contrôlée. Préférer le bouton d'arrêt/fermeture à la terminaison brutale du processus afin de laisser écrire les checkpoints et les journaux.

Les panneaux principaux sont :

- **Chat** : poser une requête et choisir la route de récupération ainsi qu'une capsule locale ou un modèle intégré. Les sources RAG et détails d'exécution restent consultables séparément du texte de réponse.
- **Sources/RAG** : ingérer des fichiers compatibles, reconstruire le RAG, consulter les espaces et nettoyer les espaces intermédiaires une fois l'espace final produit. Les fichiers sont des contenus non fiables; ne pas exécuter des instructions contenues dans les sources.
- **Observer** : sélectionner filesystem, PID ou interface réseau, définir budgets et autoriser expressément la source. Le JSONL est créé par AAM; inspecter ensuite la trace et son rapport d'arrêt.
- **Compétences / Composition** : lister les compétences, choisir une compétence, composer des nœuds `competence`, `method/sequence` et `rule/condition` valides, compiler, enregistrer puis exécuter. Le langage n'autorise pas le code Python arbitraire dans le graphe.
- **Modèles locaux** : intégrer TorchScript directement, un adaptateur PyTorch dont l'architecture est connue, un dossier Transformers local, Ollama ou un endpoint compatible. Un fichier `.pth` de poids seul ne définit pas l'architecture. Les endpoints distants nécessitent les réglages de sécurité et une liste d'hôtes autorisés.
- **Entraînement** : sélectionner un corpus décodable et les paramètres. O94.4 utilise par défaut toutes les fenêtres train/validation produites. Un checkpoint d'arrêt n'est pas automatiquement une capsule de génération publiée.
- **Autonomie/mémoire** : consulter les traces, feedbacks et rapports; la récompense règle les préférences de trajectoire, elle ne prouve pas la vérité factuelle.

## 3. Entraîner puis sélectionner le modèle de langue compact

```bash
python -m aam_o93 train-language-model ./examples/training_corpus \
  --epochs 2 --max-vocab 96 --dim 8 --context-size 4 --seed 94
python -m aam_o93 status
```

Le JSON de sortie donne `capsule_path`, `capsule_sha256`, tailles des partitions, tailles de fenêtres traitées, perte de validation, perte/perplexité TEST et génération d'exemple. Le modèle interne est un modèle d'attention compact appris sur le corpus fourni. Il n'a pas de poids pré-entraînés généraux; il peut générer des mots inconnus ou un texte de faible qualité. Utiliser un modèle local externe lorsque cette capacité est nécessaire et le valider sur ses propres cas tenus à l'écart.

Par défaut, absence de plafond = traitement de toutes les fenêtres :

```bash
python -m aam_o93 train-language-model ./corpus --epochs 5
```

Budgets explicites pour limiter la charge :

```bash
python -m aam_o93 train-language-model ./corpus \
  --epochs 3 --max-steps-per-epoch 5000 --max-validation-windows 1000
```

Les deux options acceptent uniquement une valeur entière positive. La liste `counts` décrit le nombre construit; `training_trace` décrit le nombre effectivement traité.

## 4. RAG et recherche

Ingérer un document :

```bash
python -m aam_o93 knowledge-ingest ./document.txt
python -m aam_o93 rag-spaces
python -m aam_o93 semantic-search "question précise" --top-k 5
python -m aam_o93 search "question précise" --top-k 5
```

`search` déclenche la recherche lexicale traditionnelle. `semantic-search` lit l'espace final du RAG. Il faut reconstruire le RAG après ajout de sources :

```bash
python -m aam_o93 rag-rebuild
python -m aam_o93 rag-cleanup
```

Le nettoyage supprime les espaces intermédiaires éligibles et garde l'espace final. Toujours vérifier les citations/références renvoyées et tester la précision sur des requêtes d'évaluation spécifiques. L'ingestion d'un document n'implique pas qu'une compétence complète a été apprise.

## 5. Observation de fichiers en temps réel

```bash
python -m aam_o93 observe-live \
  --source-kind filesystem --authorize-source --root ./dossier_a_observer \
  --seconds 10 --interval 0.1 --max-events 1000
```

L'autorisation doit concerner une source que vous contrôlez ou pouvez observer. La commande crée automatiquement le JSONL et le rapport `.report.json`. Si le contenu brut doit être inclus, l'activer volontairement avec `--include-file-content`; l'option par défaut garde des métadonnées. Pour un processus : `--source-kind process --pid PID --authorize-source`. Pour le réseau, choisir une interface et avoir TShark/dumpcap ainsi que les permissions requises; aucun test fixture ne prouve qu'une vraie NIC a été capturée.

Vérifier `event_type`, `sequence`, `prev_hash`, `event_sha256`, `trace_sha256`, `errors` et `status`. Une trace passive indique seulement les éléments visibles depuis la source et les droits du système; elle ne reconstitue pas automatiquement le contenu complet ou le code interne d'une application.

## 6. Boîte noire d'un programme autorisé

Le paquet comprend une cible de démonstration et des cas :

```bash
python -m aam_o93 blackbox-capture examples/blackbox/cases.jsonl \
  --command-json '["python","examples/blackbox/demo_target.py"]' \
  --trace-out ./work/capture.jsonl --authorize-target-execution
python -m aam_o93 blackbox-build-replica ./work/capture.jsonl \
  --out ./work/replica.json --export-python ./work/replica.py
python -m aam_o93 blackbox-replay ./work/replica.json '{"text":"bonjour"}'
python -m aam_o93 blackbox-replay ./work/replica.json '{"text":"entrée inconnue"}'
python -m aam_o93 blackbox-evaluate ./work/replica.json ./work/capture.jsonl
```

La capture lance la cible externe. Examiner sa commande, ses effets de bord et son dossier de travail avant d'accorder l'autorisation. La réplique est un lookup exact des entrées train non ambiguës : l'entrée inconnue doit rester `UNRESOLVED`. Ce protocole teste la séparation des données et le replay hors cible, il ne prouve pas que l'algorithme sous-jacent a été induit ni qu'il généralise.

## 7. Composition d'un programme

La forme DSL supportée est un arbre sûr : compétence (`competence`), séquence de méthode (`method`/`sequence`) ou condition (`rule`/`condition`). Les IDs doivent exister dans le catalogue; les conditions doivent appartenir à la liste blanche. Dans l'interface, utiliser l'éditeur DSL et vérifier le résultat de compilation, puis exécuter une composition sur des entrées prévues et des entrées inconnues. Depuis CLI, `composition-save` accepte un graphe JSON déjà formé et `composition-run` l'exécute sur une entrée JSON. Ne pas déclarer qu'un programme arbitraire est compilable en code natif : le compilateur produit un artefact JSON de graphe déclaratif.

## 8. Adaptateur Python personnalisé pour un runtime/protocole additionnel

Dans l’onglet **Modèles**, choisir `python_adapter`, indiquer le fichier `.py` local, choisir la politique (`inference_only` ou `adapter_train` si l’adaptateur implémente réellement l’entraînement), puis utiliser **Tester génération**. Le bouton **Créer un gabarit Python personnalisé** copie `examples/model_adapters/python_model_adapter_template.py` dans le workspace. Le contrat requis est `load_model(context)` et `generate(model, prompt, options)`; `train_model(context, model, train_rows, output_dir, policy)` est facultatif. L’adaptateur peut encapsuler un runtime local, une bibliothèque spécialisée ou un protocole réseau, mais le code doit savoir gérer ce protocole lui-même.

AAM vérifie le fichier et son SHA-256 et bloque l’exécution si l’autorisation de code local de confiance n’est pas cochée. Cette confirmation n’est **pas** un bac à sable : un adaptateur Python est du code exécutable et peut exercer les permissions du processus AAM. Inspecter le code et ses dépendances, ne pas embarquer de secret dans le module et, pour le code non fiable, utiliser un environnement OS/VM/conteneur isolé. Le gabarit fourni est une démonstration qui ne prétend pas être un vrai modèle et sa méthode d’entraînement retourne `TEMPLATE_NOT_TRAINED`; remplacez-la seulement par un entraînement propre au runtime.

## 9. Où consulter les artefacts

Le workspace garde les traces d'observation, modèles, compétences, compositions, événements de mémoire et reçus. `logs/O94_4/` conserve les commandes de validation. La checklist séquentielle est `checklist_de_travail_O94_4.json`; les incidents sont dans `checklist_erreurs_model_O94_4.json` et `checklist_erreurs_no_model_O94_4.json`; `chemins_O94.json` indique les racines portables. Les fichiers sources ne sont pas modifiés par l'ingestion de lecture seule; calculer les hashes source avant/après lorsque l'intégrité d'un jeu de données est essentielle.
