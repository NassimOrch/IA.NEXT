# Annotations relationnelles explicites

Le fichier `relations.jsonl` est volontairement vide tant qu'aucune annotation de l'utilisateur ou d'un protocole contrôlé n'est disponible. Une ligne admissible suit ce schéma JSON :

```json
{"task":"chat","src_token":"A","dst_token":"B","relation_type":"anticausal","mode":"hard","certified":true,"source_ref":"annotation:identifiant","evidence":"Protocole et élément vérifiable"}
```

`relation_type` vaut `causal_natural` ou `anticausal`; `mode` vaut `hard`, `soft` ou `neutral`. Une relation `hard` doit être explicitement certifiée. Le code ne déduit jamais une relation causale d'un ordre ou d'une cooccurrence. Une annotation doit rester traçable et peut être invalidée par un nouvel événement d'audit plutôt que supprimée silencieusement.
