# Index d'audit des sources — eSonde v3

L'audit et les inventaires de provenance détaillés sont fournis dans le paquet `Amodel_eSonde_v3`. Les deux archives originales et leurs extractions sont volontairement exclues de Dmodel, Amodel et suivi.

| Archive | Taille source | SHA-256 | Vérification |
|---|---:|---|---|
| `liverables_eSonde_v2.zip` | 341 535 837 octets | `8c555730195eef334889e5e6d67c4470fefa6bc8b955309abf856e3cdebfd99a` | ZIP CRC validé |
| `last_sources_3.zip` | 514 707 606 octets | `b118cb1f81f375997694646ff19c2632f8c901eb571cd1b93bca9688d841ee02` | ZIP CRC validé |

Le manifeste récursif des extractions contient 34 623 fichiers avec SHA-256, total de 6 538 517 720 octets. Les ZIP imbriqués ont également été inventoriés récursivement : 12 128 entrées pour le paquet v2 (4 100 172 824 octets décompressés cumulés) et 23 266 entrées pour le paquet d'expériences (1 946 769 414 octets décompressés cumulés), sans erreur CRC/parsing au relevé.

Consulter dans Amodel : `SOURCE_AUDIT.md`, `EXPERIMENT_MATRIX.md`, `source_inventory/`, `gates/` et `quantum/`. Les inventaires fournissent chemins, tailles et empreintes, pas le contenu des pièces sources. Cela respecte l'exclusion des archives attachées et de leurs extractions brutes des livrables.
