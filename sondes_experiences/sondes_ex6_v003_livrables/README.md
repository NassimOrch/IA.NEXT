# Workspace EX6 — sondes adaptatives

Workspace expérimental distinct des sources EX3–EX5.

## Fichiers d'entrée
- `prompt_ex6.json` : prompt d'expérience révision 1.0.1 (également copié dans `inputs/`).
- `inputs/prompt_ex3.json`, `prompt_ex4.json`, `prompt_ex5.json` : prompts de référence.
- `inputs/reference_theory/` : formalismes théoriques utilisés.
- `inputs/reference_code/` : copies des scripts de référence EX5.
- `inputs/data_manifest/` : ledger du split historique.
- `inputs/historical/debrit_0.txt` : notes historiques non probantes.

## Scripts
- `src/ex6_common.py` : adaptation des routines communes utilisées dans les pilotes.
- `src/ex6_mixa_engine.py` : moteur de candidats MIXA.
- `src/run_replica_pilot.py` : pilote Replica inférence-only.
- `src/run_emplica_pilot.py` : pilotes Emplica simple et Orchestra.

## Résultats
- `results/raw/` : JSON bruts par run, prédictions, comparateurs et JSONL.
- `results/models/` : checkpoints et états de reprise.
- `results/metrics/` : recalcul indépendant des métriques, comparaisons par graine et agrégats.
- `reports/` : audits, notes rétrospectives, plan prospectif et rapport final.
- `configs/` : configuration rétrospective des pilotes.
- `checksums/` : manifeste sources et hashes SHA-256.
- `execution_status.json` : statut explicite des expériences et dimensions mesurées.

## Verdict de cette version
`INCOMPLET`. Les quatre familles de pilotes passent le rapport de paramètres 4× vs MLP-ge4x. Les résultats mesurés ne démontrent pas un avantage de vitesse ; les métriques ponctuelles sont généralement inférieures au MLP-ge4x. Les correcteurs OOF inter-couches, certaines familles homogène/spécialiste, le test externe vierge et plusieurs mesures de ressources restent à exécuter.

## Reproduction
Les scripts sont fournis sous `src/`. L'environnement et les graines de cette campagne sont dans `configs/pilot_config_retrospective.json`. Cette configuration est rétrospective, pas un pré-enregistrement. Les résultats bruts ne doivent pas être écrasés ; toute nouvelle campagne doit recevoir un nouvel identifiant de run et une nouvelle version de workspace.
