# Manifeste de références — spécification complète

```json
{
  "local": ["./docs", "./manual.md"],
  "local_sha256": {"./manual.md": "..."},
  "web": {
    "references": [{"url": "https://trusted.example/manual", "query_hints": ["official manual"]}],
    "allow_domains": ["trusted.example"],
    "search_allow_domains": ["search.example"],
    "search_engines": ["https://search.example/?q={query}"],
    "search_queries": ["initial query"],
    "query_hints": ["context"],
    "enabled": true,
    "search_enabled": true,
    "require_https": true,
    "allowed_ports": [443],
    "max_bytes": 2000000,
    "max_pages_per_round": 3,
    "max_redirects": 0,
    "follow_links": false,
    "link_depth": 0
  },
  "engine": {
    "duration": "1h",
    "local_batch": 4,
    "rag_batch": 6,
    "chunk_size": 5000,
    "max_solution_sentences": 14,
    "max_local_bytes": 5000000
  }
}
```

`local` accepte des fichiers ou dossiers. Les chemins relatifs sont résolus par rapport au dossier du manifeste. Un fichier dépassant `max_local_bytes` ou sortant des racines configurées via un lien symbolique est rejeté.

`web.references` permet de déclarer des URL de référence précises. Elles deviennent autorisées par leur hôte exact tout en restant soumises aux autres contrôles réseau.

`allow_domains` définit les hôtes de contenu. `search_allow_domains` définit uniquement les hôtes des moteurs de recherche. Une URL issue d'un résultat de recherche doit encore être validée par `allow_domains` avant d'être récupérée.

`sha256` local/web permet de verrouiller un contenu attendu. En cas de différence, le document est rejeté et l'événement de sécurité est conservé.

`max_redirects=0` est le défaut recommandé. Lorsque les redirections sont activées, chaque hop est revalidé.
