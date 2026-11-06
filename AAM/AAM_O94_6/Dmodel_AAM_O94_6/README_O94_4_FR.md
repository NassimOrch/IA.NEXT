# AAM O94.4 — correction incrémentale, couverture d’entraînement et pertinence RAG

O94.4 prolonge O94.3 avec deux corrections observées et testées :

1. **Couverture du modèle de langue local** : plus de plafond silencieux à 5 000 fenêtres d’entraînement et 1 000 de validation. Par défaut, toutes les fenêtres disponibles sont traitées; les limites facultatives sont explicites dans le CLI et la trace.
2. **Pertinence RAG et intention de fréquence** : un seuil relatif transparent filtre les chunks de score faible; les diagnostics exposent le score, le seuil et les candidats écartés. Pour une question de fréquence, le classement favorise une phrase source contenant un intervalle, sans inventer ni réécrire le texte source.

## Résultat de validation

La suite complète finale sous affichage virtuel donne **377 tests réussis, 21 sous-tests réussis, 5 avertissements et 0 échec** (190,01 s). Les preuves détaillées sont dans `receipts/O94_4/` et `logs/O94_4/`; les 5 avertissements sont visibles dans le journal complet et concernent les API TorchScript dépréciées `torch.jit.trace`, `torch.jit.trace_method` et `torch.jit.load`.

La correction RAG a été testée sur deux vrais fichiers de scénario : le résultat batterie pertinent est conservé, la source météo secondaire est filtrée au seuil explicite, et « How often ...? » obtient la phrase indiquant « every 200 operating hours ». Les fichiers d’entrée ont été vérifiés inchangés. L’entraînement du corpus livré traite 8 707/8 707 fenêtres train et 1 708/1 708 validation par défaut, et exactement 5 000/1 000 quand les deux budgets sont fournis.

## Démarrage

Après extraction complète, lancer `run_AAM_O94_4.bat` (Windows), `run_AAM_O94_4.ps1` (PowerShell) ou `run_AAM_O94_4.sh` (Linux/macOS). Les anciens lanceurs O94.3 sont conservés pour la compatibilité. Python 3.11+ est recommandé et Tk/Tcl est requis pour l’interface de bureau.

```bash
python -m aam_o93 preflight
python -m aam_o93 status
python -m aam_o93 ui
```

## Entraînement

```bash
python -m aam_o93 train-language-model ./corpus --epochs 5 --max-vocab 128 --dim 16 --context-size 5 --seed 94
```

Par défaut toutes les fenêtres disponibles sont utilisées. Pour limiter volontairement la charge :

```bash
python -m aam_o93 train-language-model ./corpus --epochs 3 --max-steps-per-epoch 5000 --max-validation-windows 1000
```

Un backend `python_adapter` permet aussi de raccorder un runtime/protocole personnalisé via un contrat local explicite; l’interface crée un gabarit indépendant de PyTorch. Le fichier adaptateur est du code exécutable : n’autorisez que le code inspecté, et isolez au niveau du système d’exploitation tout adaptateur non fiable.

Le modèle interne est un petit modèle à attention sur tokens-empreintes, pas un modèle fondation pré-entraîné. Les essais ont montré un entraînement/sérialisation fonctionnels, mais une génération pauvre sur l’échantillon contenant `<unk>`; la sortie incohérente est rejetée par le filtre qualité. Ce résultat n’est ni une preuve d’impossibilité ni une preuve de qualité générale.

## RAG et fonctionnalités

```bash
python -m aam_o93 knowledge-ingest ./document.md
python -m aam_o93 rag-spaces
python -m aam_o93 semantic-search "question précise" --top-k 5
python -m aam_o93 search "question précise" --top-k 5
python -m aam_o93 rag-rebuild
python -m aam_o93 rag-cleanup
```

`semantic-search` lit l’espace sémantique final. `search` est la compétence de recherche lexicale classique et peut nécessiter l’index lexical explicite; l’ingestion en mode `observe_first` ne garantit pas cet index. Voir `GUIDE_UTILISATEUR_O94_4.md` pour Observer, boîte noire, modèles locaux, composition et GUI. Le contrat de l’objectif intégral et la matrice honnête des capacités figurent dans `cible_fonctionnelle_AAM_O94_4.tex` et la section ajoutée au laboratoire.

## Portée et limites de certification

Les essais couverts incluent tests automatisés, entraînement local, RAG sur fichiers, capture filesystem live, replay boîte noire, composition DSL et UI virtuelle. Les services Ollama / endpoints externes, les caméras/capteurs physiques et une capture NIC réelle n’ont pas été certifiés ici. Le backend `python_adapter` est vérifié sur runtime factice de test; son adaptateur réel doit être qualifié individuellement. Une réplique boîte noire exacte sur une entrée observée n’implique pas une généralisation; les entrées inconnues restent `UNRESOLVED`. Le corpus SMS complet dépasse le budget d’exécution dans cette session, même si le test limité à 300 messages passe.


## Adaptateur Python personnalisé

Le backend `python_adapter` fournit un point d’extension pour un runtime ou protocole non natif. Le gabarit `examples/model_adapters/python_model_adapter_template.py` est volontairement non productif. Le module d’adaptateur est du code exécutable, pas un fichier modèle universel : son approbation et son SHA-256 sont vérifiés, mais cette approbation ne constitue pas un bac à sable. Consultez `examples/model_adapters/README_O94_4_FR.md`.
