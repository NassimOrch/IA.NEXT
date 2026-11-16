# Modèle obligatoire des rapports eSonde v7

Tous les rapports d'architecture, d'expérience, d'incident et d'optimisation doivent conserver les neuf rubriques ci-dessous, dans cet ordre. Si une rubrique est non applicable, l'expliquer ; ne pas la supprimer.

1. **Description** — but, hypothèse, périmètre, source et version.
2. **Architecture** — composants, données et relations.
3. **Pipeline complet** — opérations dans l'ordre, entrées et sorties.
4. **Commandes d'exécution** — commandes exactes, environnement, options et graine. Indiquer `NON EXECUTE` si aucune exécution n'a eu lieu.
5. **Résultats** — sorties brutes, logs, métriques, hashes et incidents. Ne jamais remplacer un résultat absent par une estimation.
6. **Interprétation des résultats** — portée exacte, biais, incertitudes et explications alternatives.
7. **Conséquences théoriques, conceptuelles et opérationnelles** — distinguer les trois niveaux.
8. **Conclusions** — décisions étayées et questions ouvertes.
9. **Statut du modèle/expérience** — `SOURCE_OBSERVEE`, `CALCUL_REPRODUIT`, `TEST_LOGICIEL`, `ESSAI_MODELE`, `INCOMPLET`, `NON_EXECUTE` ou `BLOQUE`, avec critères d'entrée/sortie.

Chaque exécution doit être précédée d'un préflight et d'une sauvegarde vérifiée, puis suivie d'un résultat, d'un registre d'erreurs, d'une mise à jour des checklists et d'un snapshot post-exécution.
