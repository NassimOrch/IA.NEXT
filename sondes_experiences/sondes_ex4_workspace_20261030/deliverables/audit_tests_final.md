# Résultats de vérification finale

Date : 30 octobre 2026.

| Contrôle | Résultat | Détail |
|---|---|---|
| ZIP source principal | PASS | `unzip -tq` + SHA-256 archivé |
| ZIPs imbriqués | PASS | hashes comparés au manifeste source |
| prompt_ex4 JSON | PASS | parse JSON et quatre copies SHA identiques |
| v005 | PASS | 60 sondes, 85 MLP, 120 paires |
| v006 | PASS | 60 sondes, 135 MLP, 120 paires ; 60 ratios ge4x |
| v007 test non filtré | FAIL ATTENDU | 95 lignes au lieu des 70 attendues après ajout de 25 runs micro-MIXA ; voir audit explicatif |
| v007 filtre initial | PASS | 70 runs récupérés |
| v008 micro-MIXA | PASS | 25 runs sonde, 30 MLP, 50 paires ; recalcul des métriques |
| v009 Iris | PASS | 20 sondes, 40 MLP, 40 paires validation, 60 métriques test, 40 paires test, hashes et partitions vérifiés |
| Source materialization v009 | LIMITE DOCUMENTÉE | loader complet et label stratification ; aucun test dans fitting/selection/metrics pré-gel |

Les résultats `FAIL ATTENDU` de v007 ne sont pas supprimés : ils signalent que le registre original a été étendu et ne peut plus être validé avec l'ancien test de comptage. Les deux audits filtrés correspondants passent.
