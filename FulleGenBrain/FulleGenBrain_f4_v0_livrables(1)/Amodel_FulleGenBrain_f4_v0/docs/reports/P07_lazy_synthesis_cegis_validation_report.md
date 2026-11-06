# Rapport de validation — P07 : synthèse paresseuse et CEGIS

**Modèle :** `FulleGenBrain_f4_v0`  
**Version du protocole de front :** `3.0.0`  
**Version AST :** `1.3.0`  
**Date :** 26 octobre 2026  
**Statut de phase :** `PASS` après le contrôle complet documenté ci-dessous; la validation globale P08–P13 reste ouverte.

## 1. Description

P07 transforme la synthèse de programmes d'une liste matérialisée de candidats en une recherche finie, versionnée, paresseuse et reprenable. La boucle combine validation du programme, filtres de types/contrats/effets, exécution sur les exemples permis, conservation des contre-exemples, interrogation optionnelle d'un oracle indépendant et checkpoint durable. Elle préserve les distinctions épistémiques : un candidat sélectionné n'est pas une preuve.

## 2. Architecture

- `runtime/synthesis.py` : grammaire historique en liste ou grammaire `slot_product`, normalisation des coûts, front best-first borné et hashé, validation de reprise.
- `runtime/interpreter.py` : synthèse CEGIS, checkpoint de recherche, budgets, isolation des partitions, persistance du candidat et du journal des contre-exemples.
- `runtime/oracles.py` : contrat d'un oracle de contre-exemples enregistré par l'hôte, identifié par ID/version/portée/plafond de requêtes.
- `runtime/ast.py` et `spec/schemas/fullegenbrain_ast_v1.json` : opérateurs et champs versionnés, dont `oracle_id` et `max_oracle_queries`.
- `runtime/sqlite_services.py` : stockage durable de la recherche, hash, checkpoint et intégrité.

## 3. Pipeline complet

1. Valider l'enveloppe de grammaire et les données JSON canoniques.
2. Normaliser les coûts (coût absent = indice d'origine), trier chaque slot par coût puis indice, et vérifier les limites.
3. Créer le front à partir de la combinaison initiale; conserver l'identité de grammaire par SHA-256.
4. Extraire le candidat minimal disponible par coût total puis tuple d'indices, sans matérialiser le produit entier.
5. Rejeter avant exécution tout candidat invalide au niveau AST, type, contrat, effet, permissions ou budget.
6. Évaluer seulement sur les exemples de construction et CEGIS disponibles.
7. Appeler, si configuré, l'oracle d'hôte avec l'AST et l'identifiant de requête opaque; ne pas transmettre d'exemples `holdout`/`test`.
8. Valider à l'exécution un témoin retourné par l'oracle; l'ajouter à CEGIS uniquement si le candidat est réellement réfuté.
9. Persister traces, tentatives, coûts, contre-exemples, hash et front après chaque transition; reprendre uniquement si l'identité/version/portée correspond.
10. Retourner un candidat sous statut `HYPOTHESIS` ou un résultat `PARTIAL` reprenable si le budget est épuisé. Aucun succès partiel n'est converti en preuve universelle.

## 4. Commandes d'exécution

Exécution ciblée, depuis la racine du dépôt :

```sh
python scripts/preflight.py --read-only-check
python scripts/run_checked.py --label p07-oracle-budget-and-integrity-retest --kind model -- env PYTHONPATH=src python3 -W error::ResourceWarning -m unittest tests.test_p07_cegis tests.test_p07_synthesis_engine tests.test_p04_parser_contracts tests.test_p04_schema_artifact -v
python scripts/run_checked.py --label p07-full-suite-after-oracle-integration --kind model -- env PYTHONPATH=src python3 -W error::ResourceWarning -m unittest discover -s tests -v
```

Le runner relit les quatre fichiers de contrôle, lance le préflight, conserve stdout/stderr et reçu horodaté, journalise une erreur en cas d'échec et crée le point de sauvegarde. Ne pas contourner ce wrapper pour les exécutions vérificatrices du projet.

## 5. Résultats

- Suite ciblée : **50 tests réussis**, code retour 0, reçu `logs/executions/P07/20261026T111631277506+0000_p07-oracle-budget-and-integrity-retest.receipt.json`.
- Suite complète : **168 tests réussis**, code retour 0, durée rapportée 2,387 s pour `unittest`, reçu `logs/executions/P07/20261026T111852909946+0000_p07-full-suite-after-oracle-integration.receipt.json`.
- Les avertissements `ResourceWarning` ont été configurés comme erreurs; aucune alerte ressource n'a fait échouer la suite.
- Couverture du catalogue : les 29 opérateurs sont présents et testés dans le catalogue du runtime.
- Ordre du front : 50 grammaires finies pseudo-aléatoires ont été comparées à un ordre de référence exhaustif; l'ordre coût/indices concorde.
- Persistance : le front et les éléments CEGIS survivent à fermeture/réouverture SQLite, et un identifiant de recherche ne peut être réaffecté à une autre grammaire.
- Oracle : les tests couvrent témoin valide, témoin qui ne réfute pas le candidat, budget de requêtes reprenable, reprise après persistance et absence de fuite des partitions `holdout`/`test`.

Les reçus et leurs empreintes sont les pièces de preuve principales; ce rapport ne substitue pas un résumé aux journaux complets.

## 6. Interprétation des résultats

Les résultats établissent le comportement testé du front borné et de la boucle CEGIS sur les scénarios couverts. Ils n'établissent pas que chaque tâche du monde réel dispose d'une grammaire adéquate, que tout oracle possible est correct, ni qu'un produit immense sera terminé sous une limite de temps donnée. La génération paresseuse réduit la matérialisation du produit, mais ne supprime pas la taille combinatoire de l'espace logique. Le budget explicite et la reprise garantissent un état rapportable/reprenable selon le contrat, pas une vitesse universelle.

Une réponse nulle de l'oracle dit seulement qu'aucun témoin n'a été trouvé dans sa portée annoncée. Les adaptateurs d'oracle sont des frontières de confiance fournies par l'hôte; ils ne sont ni sandboxés ni rendus sûrs simplement par leur conformité structurelle. L'intégrateur doit contrôler leurs effets et leurs données externes.

## 7. Conséquences théoriques, conceptuelles et opérationnelles

### Théoriques

- Le front adopte un ordre total déterministe fondé sur le coût normalisé et les indices.
- Les checkpoints sont liés à la grammaire, au protocole et à l'identité de l'oracle.
- Une hypothèse sélectionnée est distinguée d'une preuve; un budget épuisé est distingué d'une impossibilité.

### Conceptuelles

- La recherche compositionnelle est une boucle falsifiable qui retient les contre-exemples.
- L'oracle externe a un contrat de données étroit et ne peut pas utiliser `holdout`/`test` via l'API de synthèse.
- Le processus ne guide pas le candidat vers une réponse codée en dur : il évalue le programme candidat sur les exemples et témoins disponibles.

### Opérationnelles

- Les limites de grammaire, de front, de candidats et de requêtes sont explicites.
- Toute nouvelle version de grammaire ou d'oracle impose une reprise compatible, sinon le checkpoint est refusé.
- Les journaux d'exécution et snapshots fournissent une piste d'audit.

## 8. Conclusions

Les critères de sortie P07 sont satisfaits dans la portée des contrats et tests cités : grammaire versionnée et génération paresseuse; pruning statique; front borné; checkpoints/reprise; contre-exemples conservés; oracle host-registered; contrôle de fuite `holdout`/`test`; budgets et résultats partiels explicites. La phase peut donc être marquée `PASS`.

## 9. Statut du modèle

**P07 : `PASS` dans le périmètre testé.** P00–P06 restent validées. P08–P13 ne sont pas déclarées terminées ici; la validation globale de `FulleGenBrain_f4_v0` demeure en cours jusqu'à la fin de l'intégration ASCRC, des adaptateurs spécialisés, du CLI/GUI, de la robustesse/performance, de la documentation, du packaging et de l'audit final.
