# Guide CLI — NGeGenBrain_v3

Dans les exemples, `python ngbrain.py` doit être exécuté depuis la racine du projet. Utiliser `--workspace /chemin` avant la commande pour isoler les registres et résultats.

## Commandes principales

```text
ngbrain init
ngbrain status
ngbrain model list
ngbrain model inspect --name synthetic:parity4
ngbrain inspect --model synthetic:parity4
ngbrain observe --model synthetic:parity4 --input '[1,0,1,1]'
ngbrain experiment --model synthetic:parity4 --input '[1,0,0,0]' --target xor_layers.0.positive --mode zero
ngbrain hypothesis propose --description 'C influence Y dans le contexte X' --origin 'EXP-123' --falsification 'l ablation ne change pas Y'
ngbrain hypothesis update --id HYP-... --status EN_TEST --note 'plan de test enregistré'
ngbrain discover --train-file examples/discovery_train_parity3.json --validation-file examples/discovery_validation_parity3.json
ngbrain discover --train-file train_numeric.json --validation-file valid_numeric.json --hypothesis-class numeric_expression_grammar_v1 --max-nodes 5 --candidate-budget 100000
ngbrain compose --file examples/compose_xor.json
ngbrain benchmark --bits 4 --seed 20261027 --max-samples 4096
ngbrain synthetic-ladder --seed 20261027 --output benchmarks/results/ladder.json
ngbrain validate
ngbrain replay
ngbrain audit
ngbrain export --registry experiments --output exports/experiments.json
ngbrain report --output rapport_NGeGenBrain_v3.md
ngbrain serve --host 127.0.0.1 --port 8766
ngbrain legacy-test
```

## Sens des familles

- `model`: catalogue d'adapters intégrés et inspection de modèles synthétiques.
- `observe`: interroge le modèle sans intervention et inscrit l'observation.
- `experiment`: mesure un baseline et le résultat d'une intervention sur un modèle dont la structure est volontairement exposée.
- `hypothesis`: crée et met à jour un objet versionné, avec preuves et contre-preuves.
- `discover`: recherche une règle dans une classe d'hypothèses explicite. Les classes présentes sont `affine_boolean_parity` et `numeric_expression_grammar_v1`.
- `compose`: exécute un mécanisme déclaratif enregistré dans un fichier JSON sans interpréter de code arbitraire.
- `benchmark` / `reconstruct`: le benchmark interroge un petit réseau ReLU par l'interface boîte noire, découvre une règle, puis valide hors-échantillon.
- `validate` / `audit`: vérifient manifeste et registres.
- `replay`: rerun du protocole synthétique d'après son manifeste et comparaison des métriques.
- `export` / `report`: export structuré et rapport local.
- `legacy-test`: exécute les tests de la V1 conservée.

## Données de découverte

Les JSON de découverte sont des listes d'objets `{"x": [...], "y": ...}`. Pour la découverte booléenne, chaque entrée est binaire et la sortie vaut 0 ou 1. Pour la grammaire numérique, `x` et `y` sont numériques. Le fichier de validation reste séparé du fichier d'apprentissage.

Les options `max_nodes` et `candidate_budget` de la recherche arithmétique sont des budgets d'exploration. Si le budget est atteint, le résultat l'indique ; il ne prétend pas qu'aucune règle n'existe.
