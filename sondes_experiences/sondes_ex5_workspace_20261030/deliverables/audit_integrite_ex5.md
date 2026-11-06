# Audit d'intégrité et de non-corruption EX5

Audit global recalculé après exécution de v006, le 30 octobre 2026.

| Contrôle | Résultat | Statut |
|---|---:|---|
| JSON valides | 1828 | PASS |
| Erreurs JSON | 0 | PASS |
| Fichiers JSONL | 50 | PASS |
| Lignes JSONL valides | 1705 | PASS |
| Erreurs JSONL | 0 | PASS |
| Références checkpoints SHA-256 | 1313 | PASS |
| Hashes checkpoints erronés | 0 | PASS |
| Références prédictions canoniques | 1162 | PASS |
| Hashes prédictions erronés | 0 | PASS |
| Pointeurs historiques superseded | 40 | conservés/documentés |
| Prédictions recalculées | 826 | PASS |
| Divergences métriques | 0 | PASS |
| Ratios MLP ge4x | 437 | PASS |
| Ratios sous 4× | 0 | PASS |
| Ratio minimal | 4.000735294× | PASS |

## V006 PCA-Q : audit spécifique

- PCA recalculée indépendamment sur `X_train` pour 5 graines : True.
- Les 30 métadonnées de checkpoints correspondent aux hashes PCA des manifestes : True.
- Aucun label utilisé au fit PCA (`labels_accessed=false`) ; `fit_rows=341` par graine.
- 20 essais de vectorisation : écart maximal de logits 0,0 et 20/20 ≤ 1e-6.

## Duplications et traces historiques

Certains registres append-only contiennent plusieurs enregistrements d'un même candidat/graine à la suite d'une reprise. Les checkpoints, hashes de prédiction et métriques sont identiques ; les temps wall-clock peuvent différer parce que les reprises/horodatages varient. Les CSV de déduplication donnent le nombre de doublons, la plage des temps et les clés canoniques. Les lignes brutes restent intactes et les doublons ne sont pas traités comme graines supplémentaires.

Le registre RETRO v001 contient aussi une duplication de `retro_linear/1501`, avec mesures de temps contradictoires mais sorties identiques ; une seule ligne canonique est utilisée pour les statistiques de temps et les deux lignes sont conservées.

Un ancien test d'intégrité v001 vérifie des chemins de prédiction partagés historiquement remplacés par des sidecars versionnés ; il échoue sur des chemins obsolètes. Le test canonique `test_ex5_final_integrity.py` passe et valide 495 références canoniques sans erreur. Les 36 pointeurs obsolètes sont explicitement documentés, pas présentés comme des fichiers corrompus.

## Avertissements hérités

- EX4 v007 a un registre mixte (95 entrées pour 70 attendues) ; l'agrégat global est invalidé, mais les résultats filtrés v008 sont audités séparément.
- EX4 v009 Iris est exploration précédente ; il n'est pas inclus comme confirmation indépendante d'EX5.
- Un champ brut v004 a une étiquette trop large pour `SUPERVISED_JOINT_TWOLEVEL` ; correction d'audit sidecar conservée sans réécriture du brut.
- Aucun fichier source ou run historique n'a été supprimé ni réécrit pour faire passer les contrôles.

Conclusion : l'audit global d'intégrité retourne `overall_data_integrity_pass=True`. Cela confirme l'intégrité structurelle et la cohérence des métriques auditées ; cela ne signifie pas que chaque expérience remplit la règle scientifique rouge.

## CSV

Tous les 50 fichiers CSV du workspace ont été analysés avec un parseur indépendant et un contrôle strict du nombre de colonnes : 50 PASS, 0 FAIL. Le détail figure dans `audit_csv_integrity_ex5.csv/json`.
