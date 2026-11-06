# NGeGenBrain_v2 — Laboratoire d'étude mécaniste et de reconstruction fonctionnelle

**Version de travail :** `2.0.0.dev0`  
**Date de constitution :** 2026-10-27  
**Langage principal :** Python 3.11+  
**Cœur :** bibliothèque standard Python ; PyTorch optionnel pour l'instrumentation neuronale.

NGeGenBrain_v2 conserve dans `legacy_NGeGenBrain_v1/` le dépôt source complet de la V1 et ajoute un laboratoire d'expérimentation pour modèles neuronaux instrumentables. La V2 est organisée autour d'adapters à capacités déclarées, d'observations sérialisables, d'interventions contrôlées, de registres chaînés par SHA-256, de la découverte de règles dans des classes d'hypothèses explicites, et de la composition/reconstruction de modèles symboliques exécutables.

## Démarrage rapide

```bash
python ngbrain.py init
python ngbrain.py status
python ngbrain.py inspect --model synthetic:parity4
python ngbrain.py observe --model synthetic:parity4 --input '[0,1,1,0]'
python ngbrain.py benchmark --bits 4 --seed 20261027 --max-samples 4096
python ngbrain.py synthetic-ladder --seed 20261027
python ngbrain.py reconstruct --source synthetic --seed 712 --vocab-size 5 --epochs 40 --max-new-tokens 8
python ngbrain.py audit
```

Pour lancer l'interface Web locale :

```bash
python ngbrain.py serve --host 127.0.0.1 --port 8766
```

Ouvrir `http://127.0.0.1:8766/`. Le serveur intégré refuse une écoute sur une adresse non-loopback.

Pour jouer une intervention causale sur le modèle synthétique (structure visible explicitement) :

```bash
python ngbrain.py experiment --model synthetic:parity4 --input '[1,0,0,0]' --target xor_layers.0.positive --mode zero
python ngbrain.py sweep --inputs-file examples/causal_sweep_inputs.json --target xor_layers.0.positive --mode zero
python ngbrain.py plan --inputs-file examples/causal_sweep_inputs.json --target xor_layers.0.positive
python ngbrain.py counterexamples --rows-file examples/discovery_validation_parity3.json --candidate-file examples/affine_candidate_parity3.json
```

## Adapter un LLM Hugging Face local

Le module `src/nggegenbrain_v2/adapters/huggingface.py` offre un adapter optionnel. Installer les extras puis pointer vers un modèle déjà présent localement :

```bash
pip install -e '.[huggingface]'
```

L'adapter est construit avec `trust_remote_code=False` et `local_files_only=True` par défaut. Les capacités sont déclarées explicitement. Le paquet `transformers` n'était pas installé dans l'environnement de validation présent, et l'accès réseau pour l'installer a échoué (résolution DNS indisponible) ; aucun checkpoint LLM externe n'était présent. Aucun LLM externe n'a donc été chargé ni testé dans cette livraison. Le contrat logiciel de l'adapter a été testé avec un faux modèle compatible au protocole (`tests/test_huggingface_adapter_mock.py`), ce qui ne remplace pas un test de checkpoint réel. Le mini-modèle causal synthétique est distinct d'un LLM pré-entraîné.

## Forme de l'architecture

- `adapters/base.py`: contrat du modèle et frontière de capacités.
- `adapters/torch_adapter.py`: capture d'activations par hooks temporaires, interventions scoped, hash de poids et génération autoregressive pour un module déclarant explicitement `is_causal_lm=True`.
- `adapters/huggingface.py`: adapter facultatif pour causal LM local.
- `adapters/synthetic.py`: huit terrains synthétiques progressifs, du réseau linéaire au mini Transformer causal de génération.
- `analysis/causal.py`: expériences appariées baseline/intervention et mesures de delta.
- `analysis/hypotheses.py`: cycle de vie des hypothèses, contre-preuves et historique.
- `discovery/rules.py`: induction GF(2) dans une classe formelle déclarée (parité/XOR booléen affine).
- `discovery/numeric.py`: recherche bottom-up d’expressions arithmétiques exécutables dans une grammaire déclarée, avec budget explicite et statut de troncature.
- `discovery/engine.py`: registre extensible de stratégies d’induction.
- `discovery/circuits.py`: graphe d'influences observées sous intervention, avec portée explicitement limitée.
- `composition.py`: langage déclaratif sûr et exécutable pour mécanismes composés, sans `eval`/`exec`.
- `reconstruction/engine.py`: reconstruction symbolique indépendante à partir de règles découvertes; `reconstruction/causal_lm.py` fournit la découverte d’une règle de prochain token dans une classe finie annoncée et la reconstruction par table de logits sur contextes explicitement interrogés. `reconstruction/synthetic_benchmark.py` entraîne un minuscule Transformer causal synthétique, le met derrière un adaptateur boîte noire et produit des modèles composés indépendants.
- `synthetic_lab.py`: benchmark aveugle avec séparation du répertoire d'analyse et de la vérité d'audit.
- `registry.py`: journal JSONL append-only chaîné par SHA-256, vérification et écriture atomique.
- `web.py`: API locale et interface de laboratoire.

## Échelle synthétique progressive

La commande `synthetic-ladder` exerce huit architectures reproductibles : réseau linéaire, réseau logique/parité, réseau d’interactions, réseau à représentations distribuées, chemins concurrents, réseau hiérarchique, mini-Transformer encodeur et mini-Transformer causal capable de générer des tokens. Le résultat d’exécution officiel se trouve dans `benchmarks/results/20261027_official/synthetic_ladder_results.json`. Cette échelle vérifie l’instrumentation, le comportement boîte noire/instrumentable et la capture/intervention; elle ne prétend pas que les mécanismes internes de ces architectures sont tous reconstruits.

## Échelle synthétique livrée

Le module `adapters/synthetic.py` expose huit niveaux instrumentables via `create_synthetic_level(level, black_box=...)` : (1) réseau linéaire, (2) circuit XOR, (3) interactions, (4) représentation distribuée, (5) voies concurrentes, (6) MLP hiérarchique, (7) mini-Transformer encodeur, (8) mini-Transformer causal génératif. Le protocole `run_synthetic_ladder_smoke()` exécute les huit modèles, enregistre les empreintes, vérifie les captures/interventions et teste la génération du niveau causal. Ces tests valident les adapters, pas la reconstruction mécaniste de chaque architecture.

## Reconstruction d’un modèle causal génératif

La commande `reconstruct --source synthetic` entraîne un petit Transformer causal sur une grammaire synthétique, puis ne fournit à la méthode de découverte qu’un adaptateur de requête sans inspection, capture d’activations ni exposition de paramètres. Le protocole exécute deux chemins indépendants : (1) ajuste une règle modulaire de prochain token dans une classe déclarée, en séparant strictement contextes d’entraînement et holdout ; (2) construit une table autonome des logits pour les contextes expressément interrogés. Les deux artefacts composés exécutent leur propre boucle autoregressive et ne consultent pas la source lors de l’inférence.

```bash
python ngbrain.py --workspace ./workspace_lm reconstruct --source synthetic --seed 712 --vocab-size 5 --epochs 40 --max-new-tokens 8
```

Sorties principales : `public_summary.json`, `rule_reconstruction.json`, `composed_rule_model.json`, `finite_context_lookup_reconstruction.json`, `composed_lookup_model.json` et `auditor_only/hidden_ground_truth.json`. Le dernier fichier est réservé à l’auditeur du benchmark et ne doit pas être transmis au moteur de découverte. Les valeurs du rapport officiel donnent la portée exacte du test effectivement exécuté. Ce cas démontre uniquement une reconstruction comportementale sur un Transformer synthétique minuscule et la classe/domaine précisés ; il ne vaut pas reconstruction interne d’un LLM pré-entraîné de taille réelle.

Un LLM Hugging Face local peut être chargé en mode local-only avec `reconstruct --source huggingface-local --model-path ... --mode lookup|rule|both --contexts-file ... --prompts-file ...`. Le mode `lookup` accepte une liste de contextes token-ID explicitement interrogés. Les modes `rule` et `both` exigent un objet JSON avec des champs séparés `training_contexts` et `validation_contexts` (disjoints) ; `both` exige aussi `lookup_contexts`. Le mode règle utilise par défaut `small_coefficient_modular_affine_v1`, qui examine une classe explicitement restreinte de coefficients `{−1,0,1}` modulo le vocabulaire. Le mode Python `auto` utilise l'énumération exacte `modular_affine_next_token_v1` pour vocabulaire ≤32, et la classe à coefficients réduits au-delà, pour ne pas lancer une recherche cubique déraisonnable. Cette classe réduite est plus scalable, mais n'est pas une recherche universelle de toutes les règles. Les contextes de validation ne sélectionnent jamais la règle. Il faut une couverture suffisante des contextes rencontrés pendant la génération en mode lookup ; un contexte absent n’est pas complété par des logits inventés. Le test avec un vrai checkpoint exige le paquet `transformers` et le checkpoint local ; l’adapter est testé par contrat logiciel séparément.

## Benchmark synthétique livré

Le benchmark `SYNTH-PARITY-n` interroge un petit réseau ReLU déterministe par entrées binaires. L'analyseur ne voit qu'un adapter de requête : il ne voit ni poids, ni couches, ni mécanismes internes. Un sous-ensemble de lignes sert à découvrir une règle candidate ; les autres lignes sont réservées à la validation. L'auditeur conserve séparément la description de construction du benchmark dans `auditor_only/hidden_ground_truth.json`.

Pour `n=4`, le benchmark a découvert une règle XOR des quatre variables, obtenu une exactitude `1.0` sur le holdout de 4 lignes et `1.0` sur la table binaire complète interrogée. C'est une preuve d'exécution utile pour un problème booléen borné et la classe d'hypothèses déclarée. **Ce n'est ni une reconstruction de poids, ni une preuve d'équivalence mécaniste, ni une reconstruction de LLM.**

## Tests

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
python ngbrain.py benchmark --bits 4 --seed 20261027 --max-samples 4096
python ngbrain.py synthetic-ladder --seed 20261027
python ngbrain.py reconstruct --source synthetic --seed 712 --vocab-size 5 --epochs 40 --max-new-tokens 8
python ngbrain.py audit
python ngbrain.py legacy-test
```

Le dépôt V1 est gardé et les tests d'origine s'exécutent à partir de cette copie. Les reçus dans `audit/` donnent les commandes et les résultats réellement observés.

## Environnement et ressources

Le code cœur V2 n'exige aucun paquet tiers. Les adapters PyTorch exigent `torch`; l'adapter Hugging Face exige en plus `transformers`. Les LLM ne sont pas téléchargés automatiquement. Un modèle ouvert particulier n'est pas inclus dans les archives et les expériences sur un LLM externe doivent être lancées sur une machine qui a accès à ce modèle et aux ressources nécessaires.

## Vérification de la version de travail

Le reçu source courant (`audit/validation_receipt.json`) enregistre le résultat du dernier passage de validation ; les comptes finaux exacts sont dans `audit/validation_summary.md` et les journaux bruts `audit/test_runs/`, la compilation Python, la compilation LaTeX, les commandes CLI intégrées, la syntaxe de tous les JSON recensés et les CRC des trois ZIP de référence. L'attestation clean-room de l'archive livrée est distincte et se trouve dans le bundle d'audit/suivi après création de l'archive.

## Terminologie de statut

- **implémenté** : module et contrat présents dans le dépôt.
- **testé** : commande et résultat présents dans un reçu.
- **validé dans un domaine** : résultats hors-échantillon vérifiés dans le domaine nommé.
- **non exécuté** : aucune expérience n'est revendiquée.
- **non démontré** : aucune équivalence ou capacité générale n'est revendiquée.

Les résultats négatifs, ambigus et divergents sont conservés ; l'auditeur de benchmark n'est jamais injecté dans l'interface de découverte.

## V1 conservée

Le code source complet V1 se trouve dans `legacy_NGeGenBrain_v1/`. Pour les détails sur son AST, contrats, maillage, traces, stockage, modèle du monde, CLI/Web et formalismes originaux, consulter son `README.md` et `docs/REPORT_AUDIT_NGeGenBrain_v1.md`.

## Licence

La licence incluse est la licence de recherche/non commerciale personnalisée de V1, conservée sans modification. Consulter `LICENSE`.
