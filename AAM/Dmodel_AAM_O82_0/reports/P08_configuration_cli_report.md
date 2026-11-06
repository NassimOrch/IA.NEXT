# AAM O82 — Rapport P08 Configuration, CLI et guide PC

## Description
P08 rend la configuration déclarative consommable par le runtime et synchronise le guide PC avec les interfaces réellement exécutables.

## Architecture
`config.py` valide budget, politique de ressources, allowlist de probes, mémoire, verificateurs, adaptateurs, seuils d’auto-observation, seed, mode, rétention et chemins autorisés. `Engine` applique ces paramètres et les transmet aux moteurs enfants/root-retests. Le CLI conserve les commandes normatives du modèle et ajoute `--config` comme option explicite.

## Pipeline complet
`config JSON -> validation typed -> preflight -> construction Engine/Learner -> application des restrictions -> execution -> ledger/replay`. Les rapports sont lintés avant release.

## Commandes d'exécution
```bash
cd Dmodel_AAM_O82_0
cat AAM_independent_governance/checklist_erreurs_no_model.json >/dev/null && cat AAM_independent_governance/checklist_erreurs_model.json >/dev/null
PYTHONPATH=src python -W error::ResourceWarning -m unittest tests.test_config -v
PYTHONPATH=src python scripts/lint_reports.py --output reports/P08_report_lint.json
```

## Résultats
6 tests de configuration passent avec `ResourceWarning` traité comme erreur. Les deux configurations sont complètes. L’allowlist de chemins bloque les adaptateurs externes hors périmètre. Le test d’extraction propre a exécuté le parcours CLI documenté et créé les deux checklists indépendantes depuis les graines.

## Interprétations des résultats
La configuration n’est plus un fichier descriptif : ses valeurs sont des entrées effectives de la construction et de la politique du moteur. Les modes et overrides CLI restent déterministes et traçables.

## Conséquence
### Théorique
Le contrat d’exécution devient paramétrable sans changer les invariants de vérification.
### Conceptuelle
Les politiques de ressources, de visibilité, de mémoire et d’auto-observation sont externalisées sans transformer la configuration en solution métier.
### Opérationnelle
Un PC neuf peut démarrer sans installation Python externe obligatoire et les commandes du README sont testées.

## Conclusions
La phase P08 satisfait le contrat de configuration, de CLI, de documentation et de reporting.

## Statut du model
**P08 = PASS / phase verrouillée.**
