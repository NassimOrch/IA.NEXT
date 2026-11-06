# Guide interface locale — FulleGenBrain_f4_v0

## Démarrage et sécurité locale

Depuis la racine du dépôt :

```bash
PYTHONPATH=src python3 -m fullegenbrain --data-dir ./data serve --host 127.0.0.1 --port 8765
```

Ouvrez ensuite `http://127.0.0.1:8765/`. Le serveur n'accepte que les adresses loopback, refuse les en-têtes Host non locaux, applique un contrôle same-origin aux requêtes POST du navigateur, limite le corps JSON à 16 Mio et applique une Content Security Policy sans CDN. Les appels LLM/RAG externes sont non configurés; les adaptateurs spécialistes sont appelés uniquement par ID et les interfaces transmettent `allow_network=False`.

## Vues principales

### Tâches

La partie supérieure permet d'éditer une enveloppe de programme JSON, d'inspecter ses diagnostics (`Valider sans exécuter`), de l'exécuter localement ou d'enregistrer une observation locale. La partie « tâche structurée » crée un objet de tâche local dans SQLite et permet de le retrouver après rechargement. Une tâche ne signifie pas qu'un agent ou un LLM a effectué le travail demandé.

### Composition

Le programme est un AST JSON fermé. La validation statique vérifie notamment les opérateurs connus, les références, les schémas, les contrats, les effets et les capacités requises. Les résultats affichent statut, diagnostic et trace; le runtime ne lance pas de code Python arbitraire.

### Mémoire

Permet de créer/lister des objets, et d'appliquer explicitement veille, réveil ou révocation. Le statut opérationnel (`ACTIVE`, `HIBERNATED`, `STALE`, `BLOCKED`, `REVOKED`) et le statut épistémique (`UNKNOWN`, `OBSERVED`, `SUPPORTED`, `VERIFIED`, etc.) sont distincts. Un checkpoint d'inspection ne constitue pas automatiquement une preuve sur le contenu du modèle.

### Évaluation

La vue permet :

- d'explorer une grammaire et de reprendre une recherche CEGIS par `search_id`;
- de détecter les collisions d'identifiants/empreintes d'entrée entre partitions;
- de calculer un plan ASCRC sans l'appliquer;
- de comparer deux AST et de conserver la liste des cas non exécutés;
- d'inspecter un dataset JSON et de calculer une empreinte d'un fichier en quarantaine;
- d'exécuter un rapport d'évaluation explicite. Ce dernier n'accepte que `holdout` et `test`, limite la taille, refuse les collisions avant exécution, utilise un magasin mémoire éphémère par cas, et ne sélectionne ni ne promeut de candidat. Il compare les valeurs JSON canoniques et expose des empreintes, statuts et diagnostics.

Un rapport `PASS` signifie que tous les cas explicites de ce rapport ont réussi et correspondu; cela ne démontre pas la correction universelle du programme et ne remplace pas une preuve.

### Sources et spécialistes

Les adaptateurs exposent version, provenance, disponibilité et fichiers manquants. Un élément `AUDIT_ONLY` ou `COMPARISON_ONLY` ne peut pas être traité comme un runtime exécutable. Un fragment historique manquant doit rester visible et ne doit pas être reconstruit par supposition.

### Audit

Le journal local est une chaîne hashée append-only vérifiée avant exposition. L'interface peut exporter le rapport visible, mais les événements runtime n'enregistrent pas le contenu brut des entrées comme champs de trace. Les fichiers exportés restent toutefois des données locales à protéger.

## Limites affichées

Aucun backend d'entraînement de référence, LLM/RAG externe, flux de citations RAG ou procédure de promotion de modèle n'est configuré dans cette version. L'inspection de quarantaine n'exécute ni ne désérialise le fichier. Les états `PARTIAL`, `NOT_CONNECTED`, `INSPECT_ONLY`, `BLOCKED`, `UNRESOLVED` et `NOT_RUN` sont des états explicites et ne sont pas convertis en réussite.

Les tests automatisés contrôlent les labels, assets locaux, routes et petites largeurs CSS déclarées. Ils ne remplacent pas un audit manuel avec lecteur d'écran et appareils réels; les critères UI-16 et UI-17 gardent ce travail restant dans la matrice d'acceptation.
