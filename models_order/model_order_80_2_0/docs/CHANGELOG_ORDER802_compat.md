# Changelog ORDER80.2

## 8.0.2

### Boucle de recherche

- Passage de l'observation principalement globale à une boucle complète propre à chaque séquent `Γ ⊢ G`.
- Observation après chaque échec avant décomposition.
- Niveaux `bootstrap → focused → expanded → broad`.
- Observation formelle au niveau théorème.
- Observation documentaire au niveau chunk.

### Propagation

- Fermeture et vérification indépendante de chaque sous-problème résolu.
- Sauvegarde immédiate de la mémoire.
- Retest racine immédiat après chaque mise à jour.
- `peer_probe` immédiat des nœuds en attente.

### Observation étendue

- RAG local incrémental.
- Bibliothèques locales importables.
- Observer web avec références, recherche, domaines autorisés, profondeur de liens et journal des erreurs.
- Les URLs du corpus ne deviennent disponibles pour le web qu'après observation effective de leur chunk, sauf référence explicitement configurée.

### Vérification

- Noyau indépendant avec comptage des hypothèses ouvertes.
- Revalidation récursive des lemmes `apply_lemma`.
- Détection des chaînes de dépendances circulaires.
- Trace détaillée du noyau dans les résultats.
- Séparation explicite de `resolution_status` et `novelty_status`.

### Audit

- Conservation du contenu exact des observations locales et web.
- Journal JSONL des transitions.
- Mémoire persistante et événementielle.
- Tests web et bibliothèque ajoutés à la suite automatisée.


## ORDER80.2 correction

Fixed a proof-closure defect in `_projection`: when the requested projection equals its source, the original assumption proof is preserved instead of replacing it by a bare `exact` node. This prevents a global sequent assumption from remaining open in otherwise valid certificates. A focused regression test covers the case.


## ORDER80.2 verified-lemma reuse

Added the kernel/synthesizer rule `reuse_lemma`. It can only reuse an already observed and independently re-verified complete certificate whose statement is exactly the current goal. It introduces no new mathematical premise.
