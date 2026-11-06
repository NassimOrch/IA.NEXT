# AAM O82 — Rapport P12 Benchmark

## Description
Mesure de l'expérience PC, des budgets scarce/rich, de la latence murale, de la taille du store mémoire et de la répétabilité logique.

## Architecture
Le benchmark exécute le même `Engine` avec des budgets différents, contrôle le statut/les étapes/coûts, mesure le store mémoire et lance les smoke-tests `doctor` et `probe list` dans un sous-processus isolé.

## Pipeline complet
`benchmark -> scarce -> rich -> repeated logical runs -> memory size -> CLI smoke -> aggregate PASS/FAIL`.

## Commandes d'exécution
```bash
PYTHONPATH=src python scripts/benchmark_o82.py
```

## Résultats
Le benchmark P12 a retourné `PASS`. Le mode restreint s'arrête proprement avec budget faible; le mode riche peut observer plus avant. Deux exécutions identiques ont conservé le même statut logique et le même nombre d'étapes. `doctor` et `probe list` ont retourné code 0.

Les mesures de temps murales sont instrumentales et peuvent varier d'une machine à l'autre; le gate porte sur les invariants logiques, les coûts du budget et la réussite des commandes normatives.
