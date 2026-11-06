# Tests ORDER80.2

## Suite automatisée

La validation locale comprend :

1. preuve fermée minimale et fermeture des hypothèses ;
2. rejet d'une branche mal fermée ;
3. observation documentaire par chunks ;
4. observation formelle par théorèmes ;
5. scénario réel `échec → observation supplémentaire → résolution` ;
6. cycle d'observation propre aux sous-problèmes et décomposition imbriquée ;
7. propagation immédiate vers la racine et les pairs ;
8. mémoire persistante et revalidation ;
9. recherche web configurée sur une référence HTTP locale ;
10. import d'une bibliothèque locale ;
11. scan de source contre l'injection d'une solution cible spécifique.

Commande :

```bash
python3 self_test.py
pytest -q
```

Résultat de la release : **ORDER80.2 SELF-TEST PASS** et **5 tests pytest passés** dans l'environnement de construction.

## Test de la cible structurée Riemann

Une exécution complète de la cible structurée présente dans le paquet a également été réalisée sans web externe :

- statut du modèle : `UNRESOLVED` ;
- `resolution_status` : `NO_COMPLETE_PROOF_VERIFIED_IN_THIS_EXECUTION` ;
- observations formelles : 15 unités ;
- observations documentaires : 36 chunks ;
- observations web : 0 ;
- tours d'observation globaux : 10 ;
- tentatives de nœuds : 10 ;
- mémoire de sortie : 0 certificat admis.

Ce résultat est uniquement le résultat de cette exécution du modèle. Le rapport ne l'interprète pas comme une impossibilité, une falsité ni une preuve de difficulté de la conjecture.

## Reproductibilité

La commande exacte et les journaux bruts de cette exécution sont inclus dans `audit_order_8_0_2.zip` sous `runtime/riemann_order801/`.
