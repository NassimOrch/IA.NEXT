# Index des versions

| Version | Dossier | Date | Statut | Objet |
|---|---|---|---|---|
| 001 | `versions/sondes_v001__2026-10-30/` | 2026-10-30 | ABANDONED | Pilote borné à 160 époques ; résultats exploratoires conservés, non confirmatoires. |
| 002 | `versions/sondes_v002__2026-10-30/` | 2026-10-30 | ABANDONED | Reconstruction RBF latente ; 3/105 runs, arrêt dû à la limite réelle d'exécution par invocation. |
| 003 | `versions/sondes_v003__2026-10-30/` | 2026-10-30 | ABANDONED | Campagne ciblée incomplète : 2/30 runs après contraintes réelles de calcul. |
| 004 | `versions/sondes_v004__2026-10-30/` | 2026-10-30 | COMPLETED — diagnostic | Diagnostic d'optimiseur sur une configuration, pas confirmatoire ; deux fichiers JSON contiennent NaN pour SD indéfinie. |
| 005 | `versions/sondes_v005__2026-10-30/` | 2026-10-30 | COMPLETED | Effet experts full-data vs sharded, quatre politiques alpha, 5 graines, Wisconsin. |
| 006 | `versions/sondes_v006__2026-10-30/` | 2026-10-30 | COMPLETED | Transfert SMS de la candidate v005 ; split désormais historiquement exposé. |
| 007 | `versions/sondes_v007__2026-10-30/` | 2026-10-30 | COMPLETED | Reconstruction d=16, k=32 ; 35 runs Digits ; candidate maturation gelée. |
| 008 | `versions/sondes_v008__2026-10-30/` | 2026-10-30 | ABANDONED | Évaluation Wisconsin invalidée : prétraitement incohérent entre validation et test. |
| 009 | `versions/sondes_v009__2026-10-30/` | 2026-10-30 | COMPLETED | Réévaluation externe corrigée Wisconsin/SMS, nouveaux splits, audit d'intégrité et livraison. |

**Version la plus récente : `sondes_v009__2026-10-30` (v009).**

Les versions abandonnées ne sont pas supprimées ; leur README et leur `ABANDONMENT.md` expliquent les motifs et les résultats conservés.
