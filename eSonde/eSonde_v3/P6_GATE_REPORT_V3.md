# Rapport de phase P6 v3 — tests, pureté et intégrité

**Phase :** P6 — vérification logicielle/intégrité  
**Statut :** PASS_WITH_DOCUMENTED_LIMITATIONS  
**Version runtime :** 0.3.0

## 1. Description

P6 rassemble les tests unitaires et fonctionnels, compileall, commandes publiques, intégrité des checkpoints et audit statique de pureté. Il sépare la correction logicielle des mesures de compétence linguistique.

## 2. Architecture

Les tests couvrent les familles de sondes, tokenizer v2/v3, BYTE, COORD, SEM/DISC/COREF, mise à jour/retrait de lots, CLI et GUI. Le runtime apprend des compteurs, tables creuses, graphes et index explicites. Le scan AST porte sur les 21 fichiers runtime identifiés.

## 3. Pipeline complet

1. Lire les chemins, checklists et preuves.
2. Vérifier le snapshot S18 avant la campagne.
3. Compiler tous les modules et tests.
4. Exécuter la suite complète sous Xvfb dans un processus détaché, avec fichier de log et marqueur de code de sortie.
5. Vérifier `--version`, `--help`, commandes principales et chargement du modèle.
6. Vérifier les hashes v2 et l'audit de pureté.
7. Conserver le smoke test de génération avec sa sortie exacte.

## 4. Commandes d'exécution

```bash
python -m compileall -q src/esonde tests
xvfb-run -a env PYTHONPATH=src python -m unittest discover -s tests -v
python run_esonde.py --version
python run_esonde.py --help
PYTHONPATH=src python run_esonde.py info --model models/esonde_v3_demo_checkpoint.json
PYTHONPATH=src python run_esonde.py audit --model models/esonde_v3_demo_checkpoint.json
PYTHONPATH=src python run_esonde.py generate --model models/esonde_v3_demo_checkpoint.json --prompt "Les sondes observent" --max-tokens 5 --strategy greedy --seed 0 --top-k 10
```

## 5. Résultats

| Contrôle | Résultat | Référence |
|---|---:|---|
| compileall | exit 0 | EXEC-0066 |
| cœur/tokenizer | 16/16 | EXEC-0067 |
| BYTE | 7/7 | EXEC-0068 |
| avancé SEM/DISC/COREF/lots/contexte | 10/10 | EXEC-0069 |
| CLI | 6/6 | EXEC-0070 |
| GUI avec test du checkpoint par défaut | 4/4 | EXEC-0074 |
| suite combinée actuelle | **43/43, `OK`, exit 0, 41,369 s** | EXEC-0086 |
| version et aide CLI | exit 0, `eSonde 0.3.0` | EXEC-0079 / EXEC-0084 |
| audit AST de pureté | PASS, 21 fichiers, aucun finding | EXEC-0081 |
| smoke génération | exit 0, statut `GENERATED`, 5 tokens | EXEC-0087 |

L'essai direct EXEC-0085 s'est arrêté sur la limite du wrapper au début du scénario GUI, sans code de sortie final. Il a été enregistré comme timeout du wrapper, ni comme succès ni comme échec du test. EXEC-0086 est la relance détachée contrôlée et complète.

## 6. Interprétation

Les contrats logiciels couverts ont passé dans l'arborescence source. Le smoke test a produit `Les sondes observent.....` avec cinq tokens de ponctuation. Il est fonctionnel du point de vue du contrat d'exécution mais de faible qualité pour ce prompt. Ce contre-exemple est conservé ; aucun filtre de sortie ou réponse attendue n'a été ajouté. La qualité linguistique doit rester évaluée séparément.

## 7. Conséquences

- **Théoriques :** les tests vérifient les invariants explicitement codés ; ils ne prouvent pas que les sondes sont optimales.
- **Conceptuelles :** la correction d'un pipeline n'est pas synonyme de compréhension ou de génération fluide.
- **Opérationnelles :** tests, logs, version, interface et pureté ont des preuves reproductibles ; le contrôle depuis les archives ZIP extraites reste une obligation P7.

## 8. Conclusion

P6 est fermée sur l'arborescence courante. Le contrôle post-extraction et l'intégrité des trois paquets relèvent de P7 ; tout défaut découvert à cette phase rouvre le critère correspondant.

## 9. Statut du modèle

Le runtime 0.3.0 passe 43 tests combinés. Le checkpoint de démonstration reste petit et son smoke test montre une sortie répétitive. Aucun verdict global sur le potentiel de l'architecture n'est formulé.
