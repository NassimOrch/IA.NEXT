# Bibliothèque d'outils : choix et justification

## Principe

Le cœur de NGeGenBrain_v3 ne dépend pas d'une seule bibliothèque de réseau neuronal. Une interface `ModelAdapter` forme une frontière entre le laboratoire et le modèle. Chaque adapter expose une matrice de capacités ; le protocole expérimental ne doit pas appeler une opération qui n'est pas déclarée.

## Outils déjà présents dans le code

| Outil | Rôle | Statut dans l'environnement livré |
|---|---|---|
| Python standard library | CLI, HTTP loopback, JSON, hashing, stockage fichiers, tests | Présent, utilisé par le cœur |
| PyTorch | Chargement de `nn.Module`, hooks d'activations, interventions sur sorties de modules, hash des poids | Présent dans l'environnement de validation (2.10.0+cpu) ; dépendance optionnelle du projet |
| Hugging Face Transformers | Chargement de causal LM local et tokenization | Adapter écrit, mais paquet absent dans l'environnement de validation ; non testé sur vrai LLM |
| safetensors | Stockage de poids compatible avec l'écosystème HF | Présent dans l'environnement mais non nécessaire au cœur |
| NumPy | Option pratique pour analyses numériques plus larges | Présent, non obligatoire pour le cœur livré |
| NetworkX | Graphes avancés si la taille le justifie | Présent mais non obligatoire ; graphe actuel stocké dans un schéma JSON simple |

## Pourquoi une bibliothèque propriétaire complète n'a pas été ajoutée

Le protocole demande de ne pas réécrire ce qui existe déjà sans nécessité. La bibliothèque spécialisée est donc le paquet `nggegenbrain_v3.adapters` et les services de découverte/expérimentation. Les opérations génériques s'appuient sur des bibliothèques existantes lorsque présentes ; le cœur reste installable sans dépendances additionnelles.

## Capacités présentes dans l'adapter PyTorch

- `forward`, `inspect`, `capture` ;
- capture par hooks temporaires sur les modules nommés ;
- intervention scoped : zéro/ablation, mise à l'échelle, remplacement, permutation ;
- empreinte des paramètres ;
- sérialisation/restauration de l'état des poids.

L'intervention est appliquée sur la sortie du module ciblé. Pour intervenir sur une unité/feature, il est possible de passer `unit_index` lorsque la sortie est indexable. Cela n'autorise pas l'adapter à comprendre automatiquement la sémantique du neurone : l'effet doit être mesuré et interprété expérimentalement.

## Capacités optionnelles Hugging Face

L'adapter charge des modèles locaux avec `trust_remote_code=False`; `local_files_only=True` est la valeur par défaut. Les sorties observables incluent logits/hidden states et génération ; les interventions fines sur chaque module seront développées à travers les mêmes hooks que l'adapter PyTorch lorsqu'elles seront exposées et validées pour une architecture donnée. La capacité actuellement déclarée de capture de génération et hidden states ne doit pas être confondue avec une garantie d'intervention causale universelle sur toutes les architectures HF.

## Outils supplémentaires à envisager selon l'expérience

Les outils suivants seront ajoutés quand les expériences en ont besoin : stockage d'activations volumineux avec chunking/memmap, contrôle de versions et dataset fingerprints, capture d'attention adaptée à l'architecture, gradient attribution, patching inter-séquences, hooks spécifiques aux blocs Transformers, interpretability probes, recherche sparse autoencoder / features, calcul d'information d'acquisition, métriques de similarité de représentations, et sandbox de processus pour modèles non fiables. Chaque extension devra avoir un test isolé et une expérience vérifiable, et ne devra pas prétendre être universelle si elle ne fonctionne que sur certaines architectures.
