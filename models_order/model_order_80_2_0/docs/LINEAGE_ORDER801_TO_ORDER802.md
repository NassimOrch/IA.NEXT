# Lignée ORDER80.1 → ORDER80.2

ORDER80.2 est une correction issue d’un test boîte noire strict sur un théorème de distributivité à quatre cas.

## Défauts détectés dans ORDER80.1

- perte du certificat du contexte global lors d’une projection de séquent ;
- manque d’import de `FImp` sur la voie de fermeture de séquent ;
- gestion insuffisamment identifiée des hypothèses de branches `or_elim` ;
- réutilisation inefficace des certificats déjà vérifiés ;
- activation trop tardive des dépendances d’une mémoire persistante.

## Corrections ORDER80.2

- comptabilité par tokens pour les hypothèses ;
- `initial_context` explicite dans le noyau ;
- marqueurs `context:`, `global:` et `branch:` ;
- règle stricte `reuse_lemma` ;
- récupération provenance-driven des dépendances de mémoire avant activation ;
- tests de non-régression et test de persistence par rechargement.

Aucune information spécifique permettant de reconstruire la cible de test n’a été ajoutée au moteur.
