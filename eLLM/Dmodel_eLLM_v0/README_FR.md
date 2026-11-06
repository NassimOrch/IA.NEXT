# eLLM_v0 — modèle local expérimental fondé sur les empreintes

## Description et statut

Cette distribution contient un modèle probabiliste autorégressif à n-grammes interpolés, ajusté par comptages de corpus, avec un pipeline d’empreintes exactes multi-résolution. Elle fournit un tokenizer, un modèle prédictif sérialisable, des partitions et seuils d’empreinte, une fermeture empirique sur univers fini, un graphe relationnel, une mémoire locale optionnelle, une recherche de faisceau et une imagination de trajectoires reproductibles, six diagnostics observationnels distincts (proxies, non vérités latentes), des contrôles de factorisation/transport, une API HTTP et une interface Web de chat. Le prédicteur livré est un modèle statistique compact, pas un Transformer ni un LLM de grande échelle. Cette description porte sur l’artefact livré ; elle ne préjuge pas de développements ultérieurs.

## Prérequis et autonomie

- Python 3.10 ou plus récent.
- Aucun paquet Python tiers nécessaire à l’exécution, au service Web ou aux tests.
- Pas d’accès Internet requis : les ressources Web sont locales au package.
- Un navigateur moderne est nécessaire pour l’interface.

## Démarrage

Depuis le répertoire `Dmodel_eLLM_v0` :

```bash
python run_eLLM_v0.py serve --host 127.0.0.1 --port 8765
```

Puis ouvrir `http://127.0.0.1:8765`. Sous Linux/macOS, `./start_unix.sh` lance le serveur. Sous Windows, double-cliquer `start_windows.bat` ou l’exécuter depuis un terminal. Arrêt par `Ctrl+C`. Le serveur écoute sur loopback par défaut. Ne l’exposez pas à un réseau public sans ajouter authentification, TLS et une politique de sécurité adaptée.

## Entraînement reproductible livré

Le checkpoint distribué a été entraîné sur `data/corpus_fr.txt`, 80 paragraphes, split déterministe 64/8/8 avec graine 2025. La sélection compare 25 configurations sur validation uniquement, fixe le contexte maximal testé (5 tokens) afin que le prompt utilisateur puisse contribuer à l’état prédictif, puis choisit le lissage par NLL de validation. Le test réservé a été évalué après gel du choix.

Pour reproduire la sélection :

```bash
python scripts/tune_and_train.py --corpus data/corpus_fr.txt --checkpoint checkpoints/model.json --metrics checkpoints/training_metrics.json --seed 2025 --contexts 1,2,3,4,5 --alphas 0.35,1,3,10,30 --max-vocab 5000 --selection-policy max_context_then_validation_nll
```

Cette commande est la procédure recommandée. La commande générique `train` enregistre et évalue une configuration explicitement demandée ; elle ne fait pas la recherche d’hyperparamètres. Le script de sélection est volontairement séparé. Pour utiliser un autre corpus, conservez son hash, séparez les données par document et ne réutilisez pas le test pour choisir les hyperparamètres.

## Commandes de travail

```bash
python run_eLLM_v0.py chat
python run_eLLM_v0.py footprint "une phrase d’exemple"
python run_eLLM_v0.py search "Une empreinte observe les données" --max-new-tokens 8
python run_eLLM_v0.py imagine "Une empreinte observe les données" --count 3 --max-new-tokens 12 --seed 17
python run_eLLM_v0.py diagnose "Une requête à examiner" --search-depth 3
python run_eLLM_v0.py transport-check "une fleur verte" "une route verte" --resolution 1 --output-mode token_count
python run_eLLM_v0.py evaluate --corpus chemin/vers/test.txt
python -m unittest discover -s tests -v
node --check web/app.js
```

Le format du corpus est UTF-8, les paragraphes étant séparés par une ligne vide. `evaluate` doit recevoir un corpus de test distinct si l’on veut une mesure non contaminée.

## API locale

- `GET /api/status` : état et paramètres du checkpoint actif.
- `GET /api/metrics` : rapport métrique d’entraînement.
- `GET /api/memory` : statistiques de la mémoire relationnelle locale.
- `POST /api/chat` : génération ; JSON avec `message`, `session_id`, `use_memory`, `max_new_tokens`, `temperature`, `top_k`.
- `POST /api/search` : recherche déterministe par faisceau ; paramètres `message`, `max_new_tokens`, `beam_width`, `branch_top_k`.
- `POST /api/imagine` : échantillonnage reproductible de trajectoires internes ; paramètres `message`, `count`, `max_new_tokens`, `temperature`, `top_k`, `seed`.
- `POST /api/diagnostics` : calcule `D_obs`, `D_cap`, `D_res`, `D_search`, `D_transfer` et `D_constraint`, avec périmètre et avertissements explicites. Plusieurs valeurs sont des proxies opérationnels, pas des déficits latents établis.
- `POST /api/transport-check` : vérifie la constance d'une sortie sur les fibres d'un univers fini fourni et la restriction inter-résolutions `r_{high→low}`.
- `POST /api/reset` : effacer l’historique serveur d’une session.
- `POST /api/memory/clear` : effacer la mémoire relationnelle.

L’API accepte une demande de génération jusqu’à 2048 tokens comme garde-fou opérationnel du serveur local ; le modèle lui-même n’impose plus de maximum arbitraire dans sa méthode de génération. Un token de fin peut arrêter la génération avant la longueur demandée.

## Définition opérationnelle des empreintes

Pour une suite de tokens `x`, la sonde `suffix_k` renvoie ses `k` derniers tokens. La signature au niveau `k` contient les réponses `suffix_1, …, suffix_k`. Les familles sont emboîtées et produisent des partitions exactes. Le seuil entre deux séquences est la longueur de leur suffixe commun, bornée par le niveau d’observation calculé. Les signatures servent aux quotients ; la distribution de probabilités du prédicteur reste une observable numérique distincte.

La fermeture, la capacité effective, la dimension effective, le seuil et la factorisation sont calculés sur des domaines finis explicites : ils ne sont pas automatiquement établis pour l’ensemble infini de toutes les séquences possibles.

## Résultat de l’évaluation actuellement livrée

La sélection seed 2025 a retenu `max_context=5` et `alpha=10`. Sur le test réservé de 8 documents (328 tokens scorés), la perplexité est 217.039 et l’exactitude top-1 21.04 %. Le baseline unigramme évalué sur les mêmes documents obtient une perplexité 449.916 et une exactitude top-1 5.79 %. Ce résultat est descriptif pour ce petit corpus et ce split ; il ne prouve ni une performance générale, ni la factualité, ni la validité empirique de la théorie. Des générations observées peuvent être incohérentes, très courtes ou incorrectes.

## Confidentialité, logs et sécurité

L’historique de session et la mémoire optionnelle sont écrits dans le répertoire local `memory/`; les erreurs sont journalisées dans `logs/`. Aucun contenu n’est envoyé à une API distante. Supprimez les fichiers locaux si les données sont sensibles. La limite de 4000 caractères par prompt et celle de 2048 tokens par requête HTTP sont des contrôles d’entrée de l’application, pas des propriétés mathématiques du modèle.

## Validation interface

La suite automatisée valide les API HTTP sur le vrai serveur. Le rendu DOM Chromium a aussi été testé en chargeant les fichiers HTML/CSS/JavaScript réels avec un `fetch` simulé, car la politique de l’environnement de développement bloquait la navigation du navigateur vers loopback. Ce test ne remplace pas un essai manuel sur chaque navigateur et chaque système d’exploitation.

## Recherche et imagination internes

Depuis le composeur Web, **Explorer** lance une recherche déterministe de continuations (beam search), **Imaginer** échantillonne plusieurs trajectoires avec graines reproductibles, et **Diagnostiquer** expose les six familles de proxies observables. Les opérations correspondantes sont également disponibles par les routes locales `/api/search`, `/api/imagine` et `/api/diagnostics`. Le contrôle de transport fini est accessible via `/api/transport-check` et la CLI `transport-check`. Elles explorent les probabilités apprises du checkpoint, sans réponse-cible codée en dur. La trace renvoie les niveaux d'empreinte associés.

CLI : `python run_eLLM_v0.py search "Utilisateur : exemple Assistant :"` et `python run_eLLM_v0.py imagine "Utilisateur : exemple Assistant :"`.
