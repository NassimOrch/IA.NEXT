# Configuration ORDER80.2

`run_order802.py` charge par défaut `data/observation_config.json` puis applique les options CLI fournies explicitement.

## Observation

```json
{
  "initial_formal_batch": 1,
  "initial_research_batch": 2,
  "formal_batch": 2,
  "research_batch": 4,
  "research_chunk_size": 3200
}
```

Ces tailles contrôlent le nombre d'unités ramenées par tour, pas le nombre total d'unités observables.

## Web

```json
{
  "web": {
    "enabled": false,
    "search_enabled": true,
    "reference_urls": [],
    "allow_domains": [],
    "search_engines": [
      "https://html.duckduckgo.com/html/?q={query}",
      "https://www.google.com/search?q={query}"
    ]
  }
}
```

Le web devient actif avec `--web` ou avec `"enabled": true`. Les références peuvent aussi être ajoutées par `--web-reference`.

## Bibliothèques

Les racines de bibliothèque sont ajoutées avec plusieurs `--library` ou dans `library_paths`.

## Plafonds optionnels

```json
{
  "max_observation_rounds_per_node": 0,
  "max_node_depth": 0,
  "max_node_attempts": 0,
  "max_search_states": 0
}
```

Dans ORDER80.2, `0` signifie qu'aucun plafond artificiel n'est appliqué par ce paramètre. Les contraintes du système d'exécution (mémoire, temps CPU du processus, etc.) restent extérieures au modèle.
