# EX11 — état vérifié au 2026-11-03 12:20 UTC

## Prompt et intégrité
- Prompt scientifique : 2.3.0-reconstructed ; version documentaire actuelle : 2.3.1-reconstructed.
- Corps JSON = `PRE_REGISTRATION_EX11.md` octet pour octet ; SHA-256 du corps : `a39cd3ca1d4d772670b96fe4c7ebff0aa594ea1ef098caeb23f18fd48cb65258`.
- `revision.key_design` est maintenant une chaîne et non une liste de caractères.
- Correction 2.3.1 limitée à l'étiquette de version et aux métadonnées ; pas de changement scientifique.

## Données et tests
- 13/13 ARFF originaux présents et identiques aux entrées.
- 65/65 splits et 195 CSV : vérification indépendante antérieure passée.
- Fichiers de test : mode 0440.
- Tests logiciels : 24 passed.

## Campagnes
| Branche | Version | Statut | Qualification |
|---|---|---|---|
| REPLICA-U | v003 | 65/65 | Exploratoire, déviation refit final |
| REPLICA-U | v004 | 6/65 | En cours, confirmatoire selon protocole |
| CNG | v001 | 18 runs | Exploratoire, centres non-KMeans |
| CNG | v004 | 0 runs | Script préparé, non commencé |
| CNG LOO | v004 | 0 runs | En attente des checkpoints A3 v004 |
| CNC | v003 | 1 seed | Exploratoire |
| CNC | v004 | 1 seed | KMeans oui, permutations C3/C4 non appariées |
| CNC | v005 | 0 seeds | Runner apparié préparé |
| D3Q | v001 | 160/160 | Exploratoire, géométrie GE4X / centres / contention non conformes |
| D3Q | v004 | 0/160 | Script corrigé préparé |

## Ressources
- Microbenchmark pré-campagne D1/D2/D3 proprement isolé ; équivalence D1/D2 40/40.
- Pas de mesure énergétique matérielle fiable. RSS par variante non attribuable dans les mesures déjà faites.
- Les temps de campagnes sous concurrence CPU ne sont pas des preuves confirmatoires de vitesse.

## Décision
P0/P1/P2 clôturées avec les réserves versionnées. P3 incomplète. Aucun accès au test scellé. Aucune conclusion de supériorité globale n'est permise.
