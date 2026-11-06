# AAM O82 — Rapport P04 Socle exécutable PC

## Description
Validation du socle portable, du CLI normatif, du journal d'épisodes, de la gouvernance et du diagnostic local sans dépendance externe obligatoire.

## Architecture
`CLI -> governance preflight -> contracts -> Engine -> EventLedger -> persistent workdir`. Le package utilise uniquement la bibliothèque standard Python à l'exécution.

## Pipeline complet
`checklists -> doctor -> contract load -> episode create/resume -> run -> observe -> replay -> integrity check`.

## Commandes d'exécution
```bash
PYTHONPATH=src python -m aam_o82 doctor
PYTHONPATH=src python -m aam_o82 run --problem examples/task.json --contract examples/echo_contract.json --budget '{"time":5,"compute":5,"memory":5,"energy":5,"parallelism":1,"external_quota":5}' --mode EXPERIMENT --workdir runs/runtime
PYTHONPATH=src python -m aam_o82 replay --episode <id> --workdir runs/runtime
```

## Résultats
`doctor`, création d'épisode, exécution, observation et replay ont fonctionné. La reprise a été corrigée et validée par le test d'épisode : un seul `INIT`, réhydratation des observations, de l'étape et du budget, puis `RESUME`. Gate P04: PASS.
