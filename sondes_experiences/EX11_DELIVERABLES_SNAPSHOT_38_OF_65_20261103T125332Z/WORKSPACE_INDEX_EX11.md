# Index du workspace EX11

## Contrôle d'accès et provenance
- `prompt_ex11.json`, `PRE_REGISTRATION_EX11.md` : protocole reconstruit v2.3.1 (correction documentaire uniquement).
- `INPUT_SHA256.txt`, `checksums/`, `data/metadata/` : empreintes d'entrées, données, splits et versions du prompt.
- `AUDIT_SOURCES_EX11.md`, `RECOVERY_AUDIT_2026-11-03*.md` : provenance, sources historiques, récupération et limites.

## Données
- `data/raw/datasets_arff/` : 13 ARFF du nouveau lot, en lecture seule.
- `data/train_val/`, `data/splits/` : partitions et manifestes de validation.
- `data/sealed_test/` : holdouts tabulaires en lecture seule ; ne pas ouvrir avant gel P4.
- `data/metadata/` : audits de données, provenance et vérification indépendante des 65 splits.

## Code
- `src/data/` : audit ARFF, génération des splits, prétraitement.
- `src/models/` : AdaptiveRBF, CNG/CNC, REPLICA-U.
- `src/training/` : scripts d'entraînement versionnés et runners de campagnes.
- `src/evaluation/` : audits d'artefacts, réconciliation et synthèse.
- `src/profiling/` : benchmark et coûts structurels.
- `tests/` : tests unitaires et d'intégration.

## Preuves expérimentales
- `configs/` : configurations par run.
- `logs/append_only/` : registres append-only complets.
- `logs/runs/`, `logs/stdout/`, `logs/stderr/` : journaux et codes retour.
- `results/checkpoints/`, `results/predictions/`, `results/replica_u/`, `results/cnc/` : checkpoints, prédictions et rapports de run.
- `results/metrics/`, `results/resources/`, `results/audits/`, `results/ablations/`, `results/quarantine/` : résultats dérivés, profils, audits, ablations et artefacts invalidés/quarantainés.

## Rapports
- `reports/` : préenregistrements versionnés, matrice de conformité, corrections, états et rapports par branche.
- `theory/EX11_PROTOCOL.tex` : formalisation mathématique compacte d'EX11.
- `deliverables/` : emplacement réservé à l'archive finale et à son manifeste ; aucun test scellé ne peut y être inclus avant P4.

## Exclusions
Aucune archive `last_sources_3.zip` ou archive/historique/checkpoint EX3–EX10 n'est copiée dans EX11. Les sources historiques restent à l'extérieur ; seuls les nouveaux ARFF remis pour EX11 sont copiés et hashés.
