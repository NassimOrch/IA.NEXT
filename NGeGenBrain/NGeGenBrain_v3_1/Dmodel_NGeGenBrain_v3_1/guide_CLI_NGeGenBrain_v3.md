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
ngbrain --workspace ./workspace_lm reconstruct --source synthetic --seed 712 --vocab-size 5 --epochs 40 --max-new-tokens 8
ngbrain --workspace ./workspace_local reconstruct --source huggingface-local --model-path ./local-model --mode lookup --contexts-file contexts_token_ids.json --prompts-file prompts_token_ids.json --vocab-size 32000 --context-window 2 --max-new-tokens 8
ngbrain --workspace ./workspace_local reconstruct --source huggingface-local --model-path ./local-model --mode both --rule-class small_coefficient_modular_affine_v1 --contexts-file rule_and_lookup_contexts.json --prompts-file prompts_token_ids.json --vocab-size 32000 --context-window 2 --max-new-tokens 8
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
- `benchmark`: le benchmark booléen interroge un petit réseau ReLU par l’interface boîte noire, découvre une règle et la valide hors-échantillon.
- `reconstruct --source synthetic`: entraîne un petit Transformer causal synthétique puis (a) découvre une règle de prochain token dans une classe déclarée sur les seules données d’entraînement et la teste sur le holdout et des trajectoires autoregressives, et (b) compose une table de logits indépendante pour le domaine fini explicitement interrogé.
- `reconstruct --source huggingface-local --mode lookup`: charge uniquement un checkpoint local Hugging Face, interroge les contextes token-ID explicitement fournis, compose un modèle table indépendant et compare les logits/générations. La couverture est finie et doit inclure les contextes de génération ; un domaine non couvert n’est pas extrapolé silencieusement.
- `reconstruct --source huggingface-local --mode rule|both`: exige un JSON objet contenant des listes `training_contexts` et `validation_contexts` disjointes ; `both` requiert aussi une liste `lookup_contexts`. Aucun découpage automatique du même fichier de contextes n'est effectué. `--rule-class modular_affine_next_token_v1` énumère exactement une classe affine finie, de coût cubique en vocabulaire; `small_coefficient_modular_affine_v1` explore uniquement `a,b ∈ {-1,0,1}` et en déduit le biais depuis la première observation. La version Python avec `hypothesis_class="auto"` sélectionne la classe exacte pour `vocab_size<=32` et la classe réduite au-delà. Ce choix dépend uniquement du coût de recherche et est rapporté ; ce n'est pas une garantie de trouver une règle hors de la classe sélectionnée.
- `validate` / `audit`: vérifient manifeste et registres.
- `replay`: rerun du protocole synthétique d'après son manifeste et comparaison des métriques.
- `export` / `report`: export structuré et rapport local.
- `legacy-test`: exécute les tests de la V1 conservée.

## Données de découverte

Les JSON de découverte sont des listes d'objets `{"x": [...], "y": ...}`. Pour la découverte booléenne, chaque entrée est binaire et la sortie vaut 0 ou 1. Pour la grammaire numérique, `x` et `y` sont numériques. Le fichier de validation reste séparé du fichier d'apprentissage.

Les options `max_nodes` et `candidate_budget` de la recherche arithmétique sont des budgets d'exploration. Si le budget est atteint, le résultat l'indique ; il ne prétend pas qu'aucune règle n'existe.

## Reconstruction causale générative : protocole

Le modèle synthétique n’expose à la méthode que `forward` via `QueryOnlyAdapter`. La règle du jeu reste dans `auditor_only/hidden_ground_truth.json`. La découverte utilise des contextes séparés par hash ; l’ensemble holdout ne choisit pas de candidat. La classe `modular_affine_next_token_v1` est explicite : un résultat unique signifie uniquement une identité dans cette classe, sur ces observations. Pour les vocabulaires larges, `small_coefficient_modular_affine_v1` fournit un autre espace de recherche déclaré, de complexité `O(9*n)`, sans prétention d’universalité. L’autre voie est une table des logits pour les contextes explicitement interrogés : fidélité locale exacte, sans garantie pour des contextes absents.

Les sorties sont stockées dans le répertoire donné par `--output` ou dans `workspace/synthetic_causal_lm_reconstruction/`. Le code de sortie vaut 0 lorsque les statuts conditionnels prévus sont observés dans ce protocole, 2 sinon ; ce code ne préjuge pas de la réussite d’un LLM externe.

## Modèles locaux V3

```text
ngbrain model list
ngbrain model local --paths <racine_modeles>
ngbrain chat --model-path <dossier_ou_gguf> --prompt "Bonjour"
ngbrain produce-tinylm --corpus research/corpus/public_training_corpus.txt --output research/models/NG-Recomposed-TinyLM-v3
```
