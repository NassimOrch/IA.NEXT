# Mémoire et provenance ORDER80.2

Une entrée mémorisée est un certificat fermé, pas une note libre :

```text
statement
statement fingerprint
schema fingerprint
proof tree
proof fingerprint
dependencies
source
revision
metadata
```

## Cycle d'une entrée

```text
preuve candidate
→ vérification indépendante
→ fermeture du séquent si nécessaire
→ admission
→ persistance
→ revalidation au chargement
→ activation seulement si le certificat et ses dépendances repassent le noyau
```

Une entrée `pending` n'est pas utilisable tant que ses dépendances ne sont pas présentes et vérifiables.

La mémoire conserve les dépendances d'`apply_lemma`, ce qui permet à l'audit de reconstruire l'arbre de provenance.

Après un succès local, la mémoire est sauvegardée avant le retest racine. Le fichier `memory.json` de chaque exécution correspond donc à l'état réellement utilisé par la suite de l'expérience.


## ORDER80.2 verified-lemma reuse

Added the kernel/synthesizer rule `reuse_lemma`. It can only reuse an already observed and independently re-verified complete certificate whose statement is exactly the current goal. It introduces no new mathematical premise.
