# Index des livrables V003

| Fichier | Contenu |
|---|---|
| `README_EX7_V003.md` | Point d'entrée, commande de reproduction, résumé |
| `configs/PRE_REGISTRATION_V003.json` | Protocole gelé avant entraînement |
| `configs/ENVIRONMENT_V003.json` | Runtime et matériel visible |
| `src/run_outercoord_lite_v003.py` | Entraînement candidate et MLP |
| `src/predict_v003.py` | Inférence sur entrées brutes avec scaler inclus |
| `src/profile_end_to_end_v003.py` | Profil raw-end-to-end |
| `src/verify_deployment_v003.py` | Contrôle de parité déploiement |
| `src/audit_v003.py` | Audit indépendant reproductible |
| `results/metrics/AGGREGATES_V003.csv` | Métriques agrégées cinq seeds |
| `results/metrics/PER_SEED_COMPARISON_V003.csv` | Résultats par graine et bras |
| `results/metrics/PAIRED_DIFFERENCES_V003.json` | Différences appariées et IC descriptifs |
| `results/metrics/LATENCY_AGGREGATES_V003.csv` | Latence modèle seul |
| `results/metrics/LATENCY_AGGREGATES_RAW_END2END_V003.csv` | Latence avec scaler |
| `reports/FINAL_REPORT_V003.md` | Rapport détaillé |
| `reports/PROTOCOL_AUDIT_V003.md` | Périmètre et protocole |
| `reports/CONFORMITE_V003.md` | Matrice conformité |
| `reports/ANOMALIES_V003.md` | Échecs/anomalies consignés |
| `reports/AUDIT_INDEPENDENT_V003.md/.json` | Audit 91/91 |
| `checksums/SHA256SUMS_V003.txt` | Hash de tous les fichiers du package (hors lui-même) |
| `checksums/FILE_MANIFEST_V003.csv` | Tailles et hashes |
