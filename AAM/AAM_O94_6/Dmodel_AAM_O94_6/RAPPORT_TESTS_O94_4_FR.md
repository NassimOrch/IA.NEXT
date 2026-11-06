# Rapport complet de tests AAM O94.4 — audit, corrections et résultats

**Version testée :** O94.4, branche incrémentale dérivée d’O94.3  
**Date des essais :** 20 octobre 2026  
**Périmètre :** archive modèle autonome, contrôles de phase, théorie des empreintes incluse, CLI/runtime, GUI sous Xvfb, RAG, modèle local, observation filesystem live, boîte noire, composition et manifestes de livraison.

## 1. Description

L’objectif de l’audit était de vérifier des comportements réellement exécutés plutôt que de considérer les anciennes cases de checklist comme des preuves nouvelles. Les archives O94.3 ont été ouvertes et contrôlées; l’archive `sources_AAM_17.zip` est imbriquée dans `source_material/source_archive/`. La théorie principale `DDD_Base_theorie_des_empreintes_complete_order_5.tex` est présente sous `source_material/theorie_emp/`. Le travail O94.4 reste un correctif descendant et conserve les sources O94.3 comme historique.

Deux défauts reproductibles ont motivé les corrections :

1. Le modèle d’attention local tronquait en silence l’entraînement à 5 000 fenêtres et la validation à 1 000, alors que le corpus d’essai construisait 8 707 et 1 708 fenêtres respectivement.
2. Sur un cas RAG avec deux documents, une source secondaire éloignée était conservée malgré un score beaucoup plus faible et une question de fréquence sélectionnait une phrase d’identification au lieu de la phrase qui précise un intervalle.

## 2. Architecture concernée

Le trajet linguistique analysé est : corpus → partitions train/validation/test → tokenisation en tokens-empreintes → fenêtres contextuelles → réseau à attention compacte Q/K/V → perte de prochain token → capsule sérialisée → sélection du modèle dans le chat. Ce modèle local n’est pas un LLM fondation pré-entraîné.

Le RAG suit : ingestion en lecture seule → chunks observés → espace sémantique et scores → classement → filtre de pertinence → sélection d’extraits → réponse ancrée/citations. Pour les questions qui demandent une fréquence, un bonus ne fait que réordonner les phrases sources contenant un marqueur d’intervalle; il n’injecte pas la réponse et ne génère pas une nouvelle valeur.

Les autres surfaces testées comprennent le runtime autonome, les adaptateurs de modèles, l’observation de filesystem, les capsules de replay, un DSL déclaré pour compositions et l’interface desktop exécutée avec affichage virtuel.

## 3. Pipeline de test et commandes

### Préflight, identité et contrôles

```bash
python -m aam_o93 preflight
python -m aam_o93 status
python -m aam_o93 --help
```

Le préflight O94.4 vérifie les documents de contrôle, les statuts de phases, les reçus et les hashes source/snapshot du savepoint. Le CLI annonce `aam-o94.4`; les lanceurs O94.4 appellent le préflight avant l’UI.

### Suite complète

```bash
xvfb-run -a env PYTHONUNBUFFERED=1 python -m pytest -q --disable-warnings --maxfail=20
```

Résultat final : **374 passed, 5 warnings, 21 subtests passed in 183.52s**, code retour 0. Le journal est `logs/O94_4/pytest_full_xvfb_final.txt`; le reçu machine-readable est `receipts/O94_4/P3_regression_suite.json`. Le premier essai post-correction avait quatre assertions de version héritées, les quatre ont été actualisées et une suite complète ultérieure est passée.

### Couverture train/validation

```bash
python -m aam_o93 --workspace <workspace> train-language-model examples/training_corpus --epochs 1 --max-vocab 48 --dim 8 --context-size 4 --seed 94
python -m aam_o93 --workspace <workspace> train-language-model examples/training_corpus --epochs 1 --max-vocab 48 --dim 8 --context-size 4 --seed 94 --max-steps-per-epoch 5000 --max-validation-windows 1000
```

Dans les deux cas le corpus produit 8 707 fenêtres train et 1 708 validation. Par défaut les traces rapportent 8 707/8 707 et 1 708/1 708. Avec budget explicite, elles rapportent 5 000/8 707 et 1 000/1 708, tandis que les totaux complets restent visibles.

### RAG

```bash
python -m aam_o93 knowledge-ingest ./examples/o944_smoke_corpus/battery_service.md
python -m aam_o93 knowledge-ingest ./examples/o944_smoke_corpus/coastal_weather.md
python -m aam_o93 semantic-search "How often is the Kestrel battery separator inspected?" --top-k 5
```

Dans le scénario de vérification, la source `battery_service.md` est conservée, la source météo secondaire est écartée. Meilleur score : 6,75286; seuil calculé : 5,75286; candidat sous le seuil : 1 sur 2. La réponse extraite indique « every 200 operating hours ». Les hashes des fichiers sources avant/après concordent. Les logs pré-correction (`rag_semantic_search.json` et `rag_chat_answer.json`) sont préservés pour comparer la régression.

### Observation filesystem et boîte noire

Le scénario live ajoute et modifie un fichier dans un répertoire de test contrôlé. La trace contient `session_started`, `filesystem_baseline`, `file_added` et `file_modified`; la chaîne de hash est valide. En boîte noire, 6 exemples autorisés alimentent une capsule; la reproduction exacte fonctionne sur `bonjour` vu dans la trace. Une entrée inconnue retourne `UNRESOLVED`, donc aucune généralisation n’est revendiquée.

### Composition

Le DSL de composition a été enregistré, validé/compilé et exécuté. La trace indique trois nœuds, la règle conditionnelle `min_length`, l’appel de compétence et la création d’une empreinte. Le compilateur livre un graphe JSON déclaratif sûr; ce test ne prétend pas compiler tout programme source arbitraire en exécutable natif.

### Modèle local et UI

Le modèle compact s’entraîne et se sérialise. L’échantillon comporte encore `<unk>` et une génération incohérente est rejetée par le contrôle qualité, qui utilise alors un message de repli. Cette réussite d’intégration ne prouve pas une capacité de dialogue générale. Les surfaces UI/chat et les intégrations runtime/CLI passent les tests automatisés sous Xvfb.

## 4. Résultats et interprétation

| Domaine | Résultat observé | Interprétation bornée |
|---|---|---|
| Tests parent O94.3 | 368 réussites, 5 avertissements, 21 sous-tests | Baseline historisée, pas substitut à O94.4 |
| Tests O94.4 finaux | 374 réussites, 0 échec, 5 avertissements, 21 sous-tests | Suite automatisée passée; les détails de cinq avertissements sont masqués par `--disable-warnings` |
| Entraînement par défaut | 8 707/8 707 train; 1 708/1 708 validation | Plus de plafonds implicites; davantage de calcul par époque |
| Entraînement budgeté | 5 000 train; 1 000 validation | Budgets explicites appliqués et rapportés |
| RAG après correction | Source pertinente seule; intervalle répondu | Amélioration constatée sur le scénario fourni, sans garantie universelle de pertinence |
| Observation live | Événements attendus et chaîne de hash valide | Observe les métadonnées visibles du filesystem autorisé, pas l’intérieur arbitraire d’un programme |
| Boîte noire | Replay exact connu; inconnu `UNRESOLVED` | Capsule déterministe pour les exemples observés; pas de preuve de généralisation |
| Composition | Save/compile/run passé | DSL déclaratif exécuté; pas une compilation native arbitraire |
| Modèle de langage compact | Entraînement/sérialisation passent; génération faible sur l’échantillon | Fonctionne comme prototype local mais qualité de dialogue générale non démontrée |

## 5. Conséquences théoriques, conceptuelles et opérationnelles

**Théoriques.** La théorie des empreintes rapproche les observations via des signatures et des sondes; les classes d’indistinguabilité restent relatives au support examiné. Des traces finies ne prouvent pas une équivalence ou une compétence sur toutes les entrées. Le seuil RAG est une règle expérimentale paramétrique et devrait être étalonné sur un jeu d’évaluation représentatif pour chaque corpus.

**Conceptuelles.** La couverture d’entraînement est maintenant visible et sélectionnable. La question de fréquence influence l’ordre des phrases sources sans forcer une réponse spécifique. Les mécanismes de récompense, l’auto-observation et l’autonomie ne sont pas déclarés « validés entièrement » sur la base d’un test de replay ou d’une suite unitaire.

**Opérationnelles.** Les options `--max-steps-per-epoch` et `--max-validation-windows` autorisent un compromis explicite entre couverture et charge. Le RAG expose les candidats filtrés et le cutoff. Les journaux et reçus facilitent la comparaison avant/après; les sources de test ont été conservées.

## 6. Limites de test et incertitudes

- Les cinq avertissements Pytest sont comptés mais pas individuellement diagnostiqués, car l’option `--disable-warnings` a masqué leurs corps.
- Les endpoints distants Ollama/OpenAI-compatible ne sont pas testés sur un vrai service joignable.
- Aucune caméra, aucun capteur physique et aucune carte réseau physique n’a fait l’objet d’une capture certifiée dans cette campagne.
- Le corpus SMS complet a dépassé la limite d’exécution disponible; l’évaluation bornée aux 300 premiers SMS passe. La non-exécution du corpus entier n’est pas un verdict sur la compétence.
- La recherche lexicale classique peut retourner `NO_MATCH` si son index n’est pas construit dans le workspace; la recherche sémantique finale a été testée.
- Les sorties du modèle compact peuvent être médiocres ou inclure `<unk>`; un adaptateur externe n’est pas considéré testé avant invocation réelle de son backend.

## 7. Conclusions et statut du modèle

La suite automatisée O94.4 passe complètement dans le périmètre couvert. Deux défauts de comportement, entraînement silencieusement sous-échantillonné et alignement RAG insuffisant, ont été corrigés et rejoués. La vérification de l’autonomie et de l’observation complète multimodale exige cependant des campagnes matérielles et réseau spécifiques; aucun résultat ci-dessus ne sert à prédire leur succès ou leur échec.

**Statut :** `COMPLETE_EVIDENCED` pour la non-régression mesurée. La phase P8 a également été close : les trois ZIP passent CRC, chemins sûrs, manifestes internes et extraction propre; le modèle extrait passe `PASS_BOUNDED` au préflight et les huit tests ciblés d’adaptateur. Les hashes exacts et tailles figurent dans `O94_4_delivery_manifest.json`, livré à côté des ZIP pour éviter l’auto-référence cryptographique. Ce statut n’affirme pas l’absence absolue de défauts ni ne préjuge du potentiel théorique de AAM.


## Extension P5 — adaptateur Python générique

### Description / architecture
Le registre de modèles ajoute `python_adapter`, qui utilise un contrat local `load_model(context)` / `generate(model, prompt, options)` et un hook d’entraînement facultatif. L’interface offre la sélection du backend et la génération d’un gabarit. L’adaptateur doit être explicitement approuvé; son SHA-256 est enregistré et toute modification après inscription entraîne un refus.

### Pipeline et commandes exécutées

```bash
python -m pytest -q tests/test_o944_python_adapter.py tests/test_o943_model_adapter_contracts.py --disable-warnings
xvfb-run -a env PYTHONUNBUFFERED=1 python -m pytest -q --maxfail=20
python -m aam_o93 preflight
```

Le premier passage des tests ciblés a échoué sur une assertion de harnais qui attendait le champ `holdout_rows_excluded`; l’API produit `heldout_rows_excluded`. Cette assertion a été corrigée sans modification du comportement du moteur; le retest ciblé a donné 8 réussites. L’incident reste conservé dans `checklist_erreurs_no_model_O94_4.json`.

### Résultats / interprétation
La suite étendue complète a donné **377 tests réussis, 0 échec, 5 avertissements et 21 sous-tests réussis en 190,01 s**. Les cinq avertissements sont visibles dans le journal et correspondent à des dépréciations `torch.jit.trace`, `torch.jit.trace_method` et `torch.jit.load`. Le préflight frais après mise à jour de la sauvegarde a renvoyé `PASS_BOUNDED`.

### Conséquences et statut
L’intégration personnalisée est vérifiée avec un runtime de démonstration, avec consentement explicite et contrôle de hash. Elle permet d’implémenter un protocole non natif, mais ne garantit pas l’autodécouverte de tous les formats ni la qualité d’un modèle non testé. Le code d’adaptateur est exécuté avec les permissions du processus : l’autorisation explicite n’est pas un bac à sable. Les cas métier documentés restent non certifiés jusqu’à leurs bancs de bout en bout.


## Vérification source LaTeX — P8

### Description / architecture
Les sources `formalisme_O94_4.tex` et `laboratoire_O94_4.tex` constituent la spécification et le journal d'expérimentation; elles sont compilées comme test syntaxique des livrables texte. La génération PDF sert ici de vérification de construction, pas de preuve de couverture fonctionnelle du modèle.

### Pipeline complet / commandes
```bash
pdflatex -halt-on-error -interaction=nonstopmode -output-directory=results/latex_compile formalisme_O94_4.tex
pdflatex -halt-on-error -interaction=nonstopmode -output-directory=results/latex_compile laboratoire_O94_4.tex
```

### Résultats / interprétation
Les deux commandes ont terminé avec le code 0. Une première compilation avait exposé des segments de code Markdown non valides en LaTeX, `booktabs` absent dans le préambule du laboratoire et `amssymb` absent pour une notation `\mathbb` déjà employée. Ces défauts de source ont été consignés, corrigés, puis retestés. Les journaux sont conservés dans `logs/O94_4/latex_compile/`; quelques avertissements de boîtes horizontales trop larges demeurent, sans erreur fatale. Aucun audit visuel exhaustif des PDF n'est revendiqué.

### Conséquences / statut
La compilabilité des deux sources est `COMPLETE_EVIDENCED`. L'incident `O944-P8-LATEX-SOURCE-COMPILE-001` est résolu sur preuve de deux codes retour nuls. La phase P8 reste ouverte jusqu'à l'audit indépendant des trois archives.
