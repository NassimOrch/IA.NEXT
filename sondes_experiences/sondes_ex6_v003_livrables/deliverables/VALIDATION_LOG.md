# Journal de validation — EX6 v001

Date : 2026-10-31

| Contrôle | Résultat | Détail |
|---|---|---|
| Archive source externe | PASS | 457 109 554 octets ; SHA-256 `5f7a86cb3875f97324f75c46e379b6639673dfe9cc265a173fa8749f1be0f8eb` |
| ZIP principaux | PASS | 5 archives ; `testzip()` sans erreur |
| ZIP imbriqués sous `sources_ng_adapt_0.zip` | PASS | 12 fichiers ZIP ; CRC sans erreur |
| JSON prompts EX3–EX5 | PASS | Les trois fichiers se pars ent sans erreur |
| JSON prompt EX6 | PASS | Révision 1.0.1 ; 19 sections |
| Copies EX6 | PASS | Racine, version, inputs et deliverables identiques |
| Manifeste des copies sources | PASS | 28 fichiers contrôlés par SHA-256 |
| Recalcul des prédictions | PASS | 62 fichiers ; Δ accuracy max 0 ; Δ log-loss max 8.459e-09 |
| Recompte des paramètres | PASS | 20 paires candidate/MLP-ge4x ; state_dict + 60 coefficients scaler = P_total |
| Clone Replica | PASS | États primaire/clone identiques tenseur par tenseur pour 5 graines |
| Ratio paramétrique | PASS | Ratio minimum mesuré 4.000856 |
| Exports d'inférence | PASS | 20 paires weights+scaler exportées et tailles enregistrées |
| Compilation scripts | PASS | Scripts Python dans `src/` compilés |
| Smoke test CLI/imports | PASS | `--help`, chargement source Replica, forwards Emplica/Orchestra |
| Isolation confirmatoire des données | NON | Dataset historique et chargeur matérialisant la source complète |
| Campagne complète EX6 | INCOMPLET | Plusieurs bras OOF/spécialiste/cascade et mesures de ressources restent à faire |

## Exécution et traçabilité

- Les cellules interactives déterminantes sont archivées dans `logs/pilot_execution_trace_cells.md`.
- Les scripts actuels sont dans `src/`; leurs versions compilent et sont importables.
- Les scripts autonomes ont été sauvegardés/ajustés après les runs initiaux : leur SHA exact au moment des runs n'est pas prouvé. Voir `reports/REPRODUCIBILITY_GAP_EX6.md`.
- Le script `src/audit_ex6.py` a été exécuté avec le statut `PASS` ; sortie dans `results/metrics/audit_ex6_run.json`.

## Réserve importante

Les contrôles PASS valident l'intégrité, la cohérence des prédictions et les comptes sauvegardés. Ils ne changent pas les verdicts scientifiques : les quatre pilotes échouent sur la rapidité mesurée face au MLP-ge4x et les conclusions restent descriptives sur données historiques.
