# Intégrité, reproductibilité et limites de données — EX8 v010

## Comptages vérifiés

- 90 runs candidates nouveaux, 18 bras × 5 seeds ; 160 runs MLP uniques appariés, réutilisés seulement quand deux candidates ont exactement le même budget déclaré.
- 20 candidates SMS et 40 MLP SMS, soit 60 result JSONs complets.
- 60 références historiques v001 reprises sans réentraînement.
- 10 archives ZIP imbriquées testées CRC : 10/10 PASS.
- Audit indépendant en lecture seule : 1 177 fichiers JSON générés/manifestes strictement parsés, 155 événements JSONL parsés ; 5 paires de tables d’actions inspectées.
- Écart maximal entre log-loss recalculée depuis les probabilités et celle du résultat : 1,34×10⁻⁸ Wisconsin ; 3,60×10⁻⁹ SMS.
- Les probabilités sont finies, non négatives, lignes normalisées ; les labels de validation sont strictement identiques entre candidates et MLPs appariés.

## Checksums et versions

Les résultats sont stockés sous la version fixe `EX8/versions/sondes_ex8_v010__2026-11-01/`; `ACTIVE_VERSION.txt` désigne la version. `checksums/SHA256SUMS.txt` liste tous les artefacts hors manifeste et archive de livraison. Un hash du ZIP de livraison est fourni séparément. Les sources v001/v009 et archives source restent inchangées.

## Statut des données

Wisconsin : le loader v010 n’indexe que `Xtr/ytr/Xva/yva` et les paramètres du scaler ; les clés d’adaptation présentes physiquement dans l’archive NPZ n’ont pas été chargées en valeurs. Test non présent dans le NPZ de développement.

SMS : le NPZ préparé ne matérialise que train (3 102) et validation (775). Le corpus source brut a été streamé pour déduplication/empreintes ; les labels des lignes cachées ont été parcourus pour le contrôle de format, mais ni textes/features ni labels cachés n’ont servi au fit, à la sélection ou aux métriques. Le test et l’adaptation ne sont pas évalués. Cependant la source et le split ont été utilisés historiquement dans EX5/V007/V009 : SMS n’est pas un holdout vierge.

## OOF et initialisations non supervisées

L’entraînement supervisé OOF masque les labels des folds tenus à l’écart. Toutefois, certaines initialisations K-means de couches supérieures voient la matrice de features train complète sans étiquette avant les mises à jour OOF. Le pipeline est donc sans fuite de label mais transductif du point de vue de l’initialisation non supervisée. Cette limite est documentée et doit être éliminée dans une validation confirmatoire strictement fold-isolée.

## Données historiques

Certains anciens JSON dans les snapshots source immuables contiennent des tokens non standards `NaN`. Les snapshots sont passés CRC et n’ont pas été modifiés. Les nouveaux artefacts v010 générés (1 177 JSON actifs) sont strictement parsables sans NaN/Infinity.
