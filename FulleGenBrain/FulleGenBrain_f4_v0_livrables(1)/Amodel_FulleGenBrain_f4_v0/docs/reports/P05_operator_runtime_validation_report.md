# Rapport de validation — Phase P05 : interpréteur des 29 opérateurs

## 1. Description

P05 audite l’interpréteur réel déjà présent dans le projet et clôture les écarts de sémantique identifiés pendant les essais. Le runtime exécute exclusivement un AST JSON fermé; aucun `eval`, `exec`, import dynamique ou appel réseau implicite n’a été ajouté.

## 2. Architecture

- `src/fullegenbrain/runtime/ast.py` : catalogue fermé des 29 opérateurs, validation de forme et limites de base.
- `src/fullegenbrain/runtime/program.py` : parseur d’enveloppe, résolution de variables lexicales, contrats, analyse statique des effets et capacités.
- `src/fullegenbrain/runtime/interpreter.py` : interprétation bornée, statuts d’exécution/épistémiques, validation des sorties et trace.
- `src/fullegenbrain/runtime/services.py` : adaptateur mémoire process-local pour P05; l’adaptateur persistant relève de P06.
- `TraceJournal` : journal append-only chaîné par hashes, réouvert et vérifié à la lecture.

## 3. Pipeline complet

1. Valider l’enveloppe JSON et la version de schéma.
2. Valider l’AST fermé, les champs et les limites.
3. Vérifier les contrats entrée/sortie des composants, les références lexicales, les effets et les capacités.
4. Exécuter l’AST sous budget de pas, profondeur, éléments, itérations, sortie et temps.
5. Préserver les statuts `PARTIAL` et `UNRESOLVED`; n’émettre `SUCCESS` que lorsque les obligations du chemin exécuté sont satisfaites.
6. Valider le schéma de sortie déclaré et la sérialisabilité JSON.
7. Conserver diagnostics, métriques, traces et reçus du test dans les journaux.

## 4. Commandes d'exécution

Depuis la racine du projet :

```bash
env PYTHONPATH=src python3 -m unittest discover -s tests -v
python3 scripts/check_operator_matrix.py
python3 -m py_compile src/fullegenbrain/runtime/*.py
```

Les commandes de livraison doivent être lancées via `scripts/run_checked.py`, après lecture des chemins et des trois checklists de contrôle.

## 5. Résultats

- Suite complète : **102 tests réussis**, code retour 0, durée enregistrée dans le reçu P05.
- Matrice : **29/29 opérateurs**, 29 branches de dispatch, 29 associations de test, aucune entrée manquante/extra/dupliquée.
- Contrôles négatifs : champ inconnu pour chacun des 29 opérateurs; champ obligatoire manquant pour les 27 formes qui en ont; limites négatives/nulles et politiques invalides rejetées.
- Tests de sémantique ajoutés : propagation de `PARTIAL` dans `Seq`; `Map` avec `skip`/`collect` reste partiel; `Recover` restaure l’état mémoire local avant repli et refuse de démarrer un effet irréversible; `Txn` refuse l’atomicité si le backend ne fournit pas snapshot/rollback; contrat de sortie vérifié; capacités manquantes rejetées.
- Les erreurs intermédiaires de commande/import/matrice/tests sont conservées et marquées résolues avec reçus référencés; aucune entrée historique n’a été effacée.

## 6. Interprétation des résultats

Les tests démontrent le comportement des chemins couverts par les fixtures locales et les contrats simulés. Ils ne démontrent pas, à eux seuls, l’absence universelle de défauts, ni la correction sur toutes compositions, toutes charges ou toutes versions d’environnement. Le service mémoire courant est process-local; ce point est explicitement réservé à P06.

## 7. Conséquences théoriques, conceptuelles et opérationnelles

- **Théorique :** le statut agrégé de `Seq` ne peut plus transformer silencieusement un résultat partiel en succès; les contrats de sortie sont exécutés.
- **Conceptuelle :** `Recover` ne tente plus une récupération après un effet non prouvé réversible; un rollback confirmé est distingué d’un repli ordinaire.
- **Opérationnelle :** les mutations mémoire sous `Txn`/`Recover` exigent un adaptateur capable de snapshot/rollback/fermeture du snapshot; les sorties et statuts sont testés.

## 8. Conclusions

Les critères de sortie documentés de P05 sont satisfaits sur la suite et la matrice actuelles. La phase P05 est `PASS`. La mémoire process-local n’est pas présentée comme durable; le projet passe à P06 pour la persistance SQLite et les tests de reprise après redémarrage.

## 9. Statut du modèle

**FulleGenBrain_f4_v0 : développement en cours.** P00–P05 sont marquées `PASS`; P06 est `IN_PROGRESS`. Aucun statut de complétude globale, aucune promesse d’absence absolue de défauts et aucune prédiction de succès/échec futur ne sont revendiqués à ce stade.
