# Contrat du moteur de solution généraliste

ORDER80.2.1 sépare quatre objets : problème, observation, synthèse candidate et vérification.

Le problème est une demande libre. Les références constituent uniquement la frontière documentaire dans laquelle le moteur a le droit de chercher. La synthèse candidate est construite à partir des données observées et porte toujours une provenance. La vérification décide si l'artefact respecte le contrat demandé.

Dans cette release, le synthétiseur général intégré est extractif et déterministe. Il peut fournir une réponse documentée lorsque les références contiennent les éléments nécessaires. Il ne constitue pas un moteur sémantique universel et il ne prétend pas prouver une propriété de domaine par simple corroboration textuelle.

Pour un domaine à forte garantie, le contrat recommandé est :

```text
problème
→ références allowlistées
→ observation incrémentale
→ synthèse candidate
→ vérificateur de domaine explicite
→ PASS
→ mémoire + news/
```

Le cœur généraliste n'embarque pas de solution particulière. Une extension de domaine doit être fournie comme composant explicite et séparé, avec son propre vérificateur.

## Réutilisation de mémoire

Les artefacts `PASS` sont présentés au synthétiseur comme des connaissances marquées `memory:<fingerprint>`. Ils restent distingués des documents bruts. Une mémoire n'est jamais admise uniquement parce qu'elle existe dans un fichier ; ses propres métadonnées de vérification sont conservées.
