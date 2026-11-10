# Validation eSonde v3 — registre synthétique des preuves

**Version runtime :** 0.3.0  
**Date du relevé :** 10 novembre 2026 (Africa/Algiers)  
**Périmètre :** conformité architecturale, tests logiciels, interfaces, diagnostic linguistique multilingue, intégrité des checkpoints.  
**Statut global :** implémentation expérimentale et interfaces validées sur les scénarios recensés ; 43 tests passent en groupes isolés ; la suite combinée actuelle conserve une réserve d’orchestration ; évaluation linguistique de démonstration seulement ; potentiel généraliste non tranché.

Ce document distingue les résultats logiciels des mesures de compétence. Un test réussi démontre le contrat qu'il exerce, pas une qualité linguistique générale.

## 1. Description et architecture

Le runtime est constitué de sept familles de sondes explicites (`SEQ`, `SKIP_REL`, `MORPH`, `SEM`, `DISC`, `RETR`, `BYTE`) et d'un coordonnateur `COORD` à mélange convexe. L'état appris est constitué de compteurs, tables creuses, index et structures de provenance. Aucun neurone, MLP, transformeur, embedding dense appris, projection dense ni attention Q/K/V n'est utilisé dans le runtime.

`BYTE` modélise les chaînes ouvertes via des transitions d'octets UTF-8 avec BOS/EOS et backoff. Il est appelé par l'entraînement, le score next-token, la proposition de candidats de génération, COORD et la sérialisation. Le tokenizer v3 effectue un repli CJK/Hangul caractère par caractère ; les checkpoints v2 continuent d'utiliser leur tokenizer 2 historique.

## 2. Pipeline d'évaluation

1. Vérifier les checklists, les chemins canoniques et le dernier snapshot.
2. Vérifier compileall, les tests des groupes cœur/BYTE/avancé/CLI/GUI.
3. Vérifier les commandes d'aide, la version, `info`, l'audit statique de pureté.
4. Vérifier le chargement et les empreintes des checkpoints historiques et actifs.
5. Évaluer MLQA séparément comme diagnostic next-token, sans entraîner sur les splits `dev` ou `test`.
6. Produire les journaux, rapport, manifestes et snapshot avant le packaging.

## 3. Commandes de reproduction

Depuis la racine du paquet Dmodel :

```bash
python --version
python run_esonde.py --version
python run_esonde.py --help
python -m compileall -q src/esonde tests
PYTHONPATH=src python -m unittest discover -s tests -p 'test_core_p2.py' -v
PYTHONPATH=src python -m unittest discover -s tests -p 'test_byte_v3.py' -v
PYTHONPATH=src python -m unittest discover -s tests -p 'test_p6_advanced.py' -v
PYTHONPATH=src python -m unittest discover -s tests -p 'test_cli_p3.py' -v
xvfb-run -a env PYTHONPATH=src python -m unittest discover -s tests -p 'test_gui_p4.py' -v
PYTHONPATH=src python run_esonde.py info --model models/esonde_v3_demo_checkpoint.json
PYTHONPATH=src python run_esonde.py audit --model models/esonde_v3_demo_checkpoint.json
```

Diagnostic MLQA, seulement si l'archive a été obtenue indépendamment et que ses conditions de licence sont respectées :

```bash
PYTHONPATH=src python scripts/evaluate_mlqa_next_token.py \
  --model models/esonde_v3_demo_checkpoint.json \
  --mlqa-zip /chemin/vers/MLQA_V1.zip \
  --output results/mlqa_test_next_token.json \
  --paragraphs-per-language 8
```

Ce script ne copie pas le dataset dans le paquet et ne calcule pas le benchmark officiel QA EM/F1.

## 4. Résultats logiciels

| Groupe | Résultat consigné | Preuve |
|---|---:|---|
| compileall | exit 0 | `results/validation_logs/EXEC-0066-compileall.log` |
| cœur / tokenizer | 16/16 | `EXEC-0067-core-regression-tokenizer3.log` |
| BYTE | 7/7 | `EXEC-0068-byte-regression.log` |
| avancé SEM/DISC/COREF/lots/contexte | 10/10 | `EXEC-0069-advanced-regression.log` |
| CLI | 6/6 | `EXEC-0070-cli-regression.log` |
| GUI après correction de son modèle par défaut | 4/4 | `EXEC-0074-gui-default-and-workflow-regression.log` |
| suite combinée historique | 42/42, `unittest OK`, exit 0 du lanceur contrôlé | `EXEC-0078-full-suite-controlled.log`, avant ajout du quatrième test GUI |
| suite courante par groupes isolés | **43/43**, tous codes 0 | `EXEC-0067` à `EXEC-0074` |
| suite combinée courante | `unittest OK` visible, mais wrapper exit 2 / tentative directe interrompue | `EXEC-0085`, `EXEC-0086`, `EXEC-0088` — réserve maintenue |
| aide CLI et version | exit 0, version `0.3.0` | `EXEC-0079-cli-help.log`, `EXEC-0084-cli-interface-contract.log` |
| audit AST pure-probe | PASS, 21 fichiers, aucun finding | `EXEC-0081-purity-audit.log` |

Les groupes indépendants actuels totalisent 43/43 tests : 16 cœur + 7 BYTE + 10 avancés + 6 CLI + 4 GUI, tous avec code de sortie 0. Les journaux combinés après ajout du quatrième test GUI terminent l’affichage unittest par `OK`, mais le wrapper a retourné 2 ou a été interrompu avant la capture finale ; la tentative combinée actuelle n’est donc pas certifiée avec code global 0. Le résultat combiné contrôlé 42/42 demeure valable pour la version précédant ce test supplémentaire.

## 5. Résultat linguistique MLQA — diagnostic non officiel

**Données :** MLQA_V1, licence CC BY-SA 3.0 ; 49 fichiers `dev`, 49 `test`, aucun split `train`. Aucune donnée `dev` ou `test` n'a été utilisée pour l'entraînement du checkpoint actif. Le modèle a été entraîné sur les huit documents neutres fournis (415 tokens) et calibré sur deux documents (80 cibles).

**Échantillon test :** huit paragraphes par langue, sept langues (`en`, `ar`, `de`, `es`, `hi`, `vi`, `zh`), 56 paragraphes, 4 055 tokens. Les titres exacts entre `dev` et `test` ne se recouvrent pas pour les sept langues dans l'échantillon contrôlé. Il s'agit d'un diagnostic conditionnel next-token context+question, pas de l'évaluation officielle d'extraction de réponses MLQA.

| Mesure | Valeur |
|---|---:|
| Tokens test | 4 055 |
| OOV | 3 510 (86,56 %) |
| NLL COORD avec BYTE | 31,3662 nats/token |
| NLL sans BYTE | 598,4486 nats/token |
| NLL BYTE seul | 30,8303 nats/token |
| Perplexité COORD | environ 4,1895 × 10^13 |
| Baseline unigramme avec classe OOV unique | 6,2438 nats/token (non comparable : tous les OOV sont fusionnés) |

BYTE attribue une probabilité finie aux chaînes OOV de cet échantillon ; la baisse de NLL par rapport à l'ablation sans BYTE est importante dans ce diagnostic. La NLL absolue et la perplexité restent très élevées. Cela ne démontre ni compréhension QA, ni exactitude de génération, ni raisonnement, ni qualité généraliste. Les chiffres sont directement liés au petit checkpoint de démonstration.

Résultat détaillé : `results/p4_mlqa_test_next_token.json`; journal : `analysis/executions/EXEC-0065-mlqa-test-7lang-fullsample.log` dans le dossier de suivi.

## 6. Intégrité des poids et des états

Le checkpoint de démonstration est `models/esonde_v3_demo_checkpoint.json`, SHA-256 fichier `e4a7a2b003931467cb33de416e4954c4813ea4b408d1fc756249219c52a94ab3`, payload `bf9d9f337c86ed5dcdcddf47ff68bda950e5af7dfe1300097345204d26f5eb52` au relevé. Les trois checkpoints v2 de `models/original_v2/` ont été comparés octet par octet aux originaux extraits : leurs SHA-256 sont consignés dans `models/README.md`. La migration v2 attribue un poids BYTE par défaut nul et ne réécrit aucun original.

## 7. Interprétation et conséquences

- **Théorique :** les noyaux conditionnels propres aux familles et le mélange convexe COORD fournissent un formalisme probabiliste cohérent ; la chaîne BYTE offre un support ouvert sur les chaînes UTF-8.
- **Conceptuelle :** une prédiction de chaîne inconnue est distincte d'une simple classe OOV. La distinction entre noyaux d'observation et noyaux linguistiques reste nécessaire.
- **Opérationnelle :** le runtime et ses workflows tests sont disponibles avec Python 3.10+ ; Tkinter est requis seulement pour GUI. La taille des structures et le coût des recherches croissent avec les fenêtres et budgets configurés.
- **Évaluation :** le corpus fourni ne permet pas un pré-entraînement généraliste ; MLQA ne contient pas de train. Aucune conclusion positive ou négative sur le potentiel ultime de l'architecture n'est formulée.

## 8. Conclusion et statut

Les contrats d'architecture, BYTE, sérialisation, compatibilité v2, les tests par groupes et les interfaces ont des preuves. La mesure MLQA est un diagnostic limité et très faible en qualité absolue. La généralisation linguistique à grande échelle n'est pas démontrée faute de corpus d'apprentissage indépendant volumineux et de campagnes pré-enregistrées supplémentaires. Le modèle reste un prototype expérimental pure-sonde, exécutable et extensible ; son potentiel n'est ni présupposé ni déclaré impossible.

## 7.1 Smoke test de génération observé

Commande exacte :

```bash
PYTHONPATH=src python run_esonde.py generate --model models/esonde_v3_demo_checkpoint.json --prompt "Les sondes observent" --max-tokens 5 --strategy greedy --seed 0 --top-k 10
```

Code de sortie : 0 ; statut CLI : `GENERATED` ; nombre de tokens : 5 ; texte retourné : `Les sondes observent.....`. La génération est fonctionnelle au sens du contrat d'exécution, mais cette continuation précise est de faible qualité et répétitive. Elle est conservée comme contre-exemple observé ; aucun filtre ou texte de sortie forcé n'a été ajouté pour la masquer. Le journal est `EXEC-0087-demo-generation-smoke.log` dans le paquet de suivi.
