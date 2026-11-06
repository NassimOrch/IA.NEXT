# Lignée ORDER80.2.0 → ORDER80.2.1

ORDER80.2.1 est construit à partir du modèle `model_order_8_0_2_0`.

## Conservé

- budgets temporels ;
- observation incrémentale ;
- anti-stagnation ;
- mémoire persistante ;
- archivage `news/` ;
- checkpoints ;
- demande RAG ;
- journalisation événementielle ;
- provenance et fingerprints.

## Généralisé

- problème : texte libre plutôt que cible mathématique ;
- références : fichiers, dossiers, URLs et moteurs de recherche ;
- observation : chunks documentaires arbitraires ;
- planification : requêtes dérivées du problème, des observations et des lacunes ;
- sortie : synthèse générale avec provenance ;
- vérification : contrat générique de couverture/provenance ;
- réseau : nouvelle couche de sécurité dédiée.

## Séparation de la lignée historique

Les anciens artefacts spécifiques O80.2 et leurs tests restent sous `legacy_order8020/` afin de conserver la traçabilité. Le point d'entrée actif `run_order_8_0_2_1.py` ne charge aucun corpus ni résultat spécifique à une cible par défaut.
