# Rapport de validation P04 — AST, schémas, contrats et validation de types/effets

- **Projet :** `FulleGenBrain_f4_v0`
- **Phase :** P04
- **Statut :** PASS pour le périmètre défini ci-dessous
- **Version du schéma :** `1.0.0`
- **Autorités :** `formalisme_operationnel_FulleGenBrain_f4_v0.tex`, `spec/upstream/formalisme_FulleGenBrain_4.tex`, `spec/upstream/theorie_programation_compositionnelle_2.tex`

## 1. Description

P04 met en place un parseur fermé pour les programmes JSON FulleGenBrain, la grammaire versionnée de ses 29 opérateurs canoniques, un validateur de contrats/types/effets/capacités, un évaluateur d'expressions borné sans `eval`/`exec`, et un journal de traces append-only à chaîne de hachage.

Le statut PASS porte sur ces mécanismes et les tests listés. Il ne prétend pas que l'interpréteur des 29 opérateurs ou l'application complète soit déjà achevée : cela relève des phases suivantes.

## 2. Architecture

- `src/fullegenbrain/runtime/ast.py` : définitions canoniques et parsing de l'AST.
- `src/fullegenbrain/runtime/contracts.py` : sous-ensemble JSON Schema accepté, validation des valeurs, formes d'expressions.
- `src/fullegenbrain/runtime/expressions.py` : évaluation fermée des expressions (`$literal`, `$ref`, `$var`, `$op`).
- `src/fullegenbrain/runtime/program.py` : enveloppe de programme, inférence d'effets/capacités, validation statique.
- `src/fullegenbrain/runtime/registry.py` : registre explicite des composants et de leurs contrats.
- `src/fullegenbrain/runtime/tracing.py` : événements JSONL séquencés, hash-chain, idempotence et détection d'altération.
- `spec/schemas/fullegenbrain_ast_v1.json` : export machine-lisible de la grammaire, vérifié contre `ast.py`.

Le parseur rejette les opérateurs/champs inconnus, les champs requis absents, les versions non prises en charge, les références invalides détectables statiquement, les variables hors portée, les effets interdits dans `Par`/`Txn`, les capacités manquantes et les expressions de forme/type invalide avant de démarrer l'exécution.

## 3. Pipeline complet

1. Lire et valider les fichiers de gouvernance/checklists et le pointeur de sauvegarde.
2. Parser l'enveloppe JSON et vérifier `schema_version`.
3. Valider les schémas d'entrée/sortie avec le sous-ensemble supporté.
4. Parser l'AST avec limites de profondeur/taille et fermeture des champs.
5. Analyser les références, les portées lexicales, les formes d'expression, les contrats, les effets et les capacités.
6. Rejeter les programmes statiquement invalides avant tout effet.
7. Évaluer uniquement les expressions de la liste blanche, sans exécuter du code arbitraire.
8. Écrire les événements avec identifiants idempotents et chaîne SHA-256 ; refuser les collisions, les lignes finales partielles et les altérations.
9. Enregistrer résultat, erreurs et point de sauvegarde.

## 4. Commandes d'exécution

Depuis la racine du projet :

```bash
python3 scripts/preflight.py --read-only-check
python3 scripts/run_checked.py --label p04-export-versioned-ast-schema --kind no_model -- python3 scripts/export_ast_schema.py
python3 scripts/run_checked.py --label p04-complete-test-suite-retest --kind model -- python3 -m unittest discover -s tests -v
python3 scripts/savepoint.py verify --restore-smoke
```

`run_checked.py` lit au préalable les chemins, checklist de travail et deux registres d'erreurs, conserve sorties/codes de retour, ajoute une ligne au journal d'exécution et crée un point de sauvegarde après chaque commande.

## 5. Résultats

- **59 tests réussis, 0 échec** lors de `p04-complete-test-suite-retest`.
- Couverture de parsing : les 29 noms d'opérateurs sont présents, distincts et parsés.
- Artefact de grammaire : version `1.0.0`, les 29 opérateurs et toutes les listes de champs concordent avec la source runtime.
- Expressions : tests positifs et négatifs sur les références, variables, opérations, arité, arithmétique non finie, division par zéro et clés réservées.
- Contrats et sécurité statique : tests des schémas, capacités, effets, variables et références fermées.
- Journal : tests d'ajout, vérification de hash-chain, idempotence, collision d'identifiant, détection d'altération et refus d'une fin de fichier partielle.
- Les deux exécutions de test historiques en échec restent conservées et sont marquées RÉSOLUES avec preuves ; leur cause provenait des attentes/tests, non du code runtime final.

Preuves détaillées : `logs/executions/P04/20261026T100946769064+0000_p04-complete-test-suite-retest.receipt.json`, ses sorties jumelles, `spec/schemas/fullegenbrain_ast_v1.json` et `tests/test_p04_*.py`.

## 6. Interprétation des résultats

Les tests démontrent les propriétés contrôlées dans le périmètre P04 sur l'environnement local d'exécution. Ils ne démontrent ni la correction sémantique de tous les opérateurs pendant l'exécution, ni des garanties universelles, ni l'absence absolue de bogues. Les tests d'interpréteur par opérateur, de mémoire persistante, de reprise, de concurrence et les tests intégrés restent les critères de P05 et des phases suivantes.

## 7. Conséquences théoriques, conceptuelles et opérationnelles

### Théoriques

La syntaxe des programmes est versionnée et fermée ; la validation statique est séparée de l'exécution. La trace possède un mécanisme local de détection d'altération, sans prétendre être une signature cryptographique externe ni une garantie contre un acteur contrôlant simultanément code et stockage.

### Conceptuelles

Les états épistémiques ne sont pas assimilés à des états opérationnels. `UNRESOLVED` n'est pas interprété comme une impossibilité. La sélection par politique ne constitue pas une preuve. Ces principes seront vérifiés à l'exécution en P05/P08.

### Opérationnelles

Le pipeline peut refuser un programme invalidé avant d'appeler ses composants. Les expressions sont évaluées selon une grammaire limitée ; aucune dépendance réseau ou import dynamique n'est autorisé par cette couche.

## 8. Conclusions

**Conclusion P04 : PASS.** La gate de phase autorise le démarrage de P05; ce rapport ne déclare pas que le système global est achevé.

## 9. Statut du modèle

**P04 : PASS dans le périmètre des contrats AST/schéma/typage/effets et des tests consignés.** Le modèle global est en cours de validation par phases.
