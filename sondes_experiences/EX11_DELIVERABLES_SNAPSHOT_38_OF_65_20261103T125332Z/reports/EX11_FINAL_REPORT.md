# Rapport EX11 — état finalisable et résultats vérifiables

## Statut d’ensemble au snapshot

**EX11 n’est pas encore entièrement terminée.** P0/P1/P2 sont vérifiées ; P3 reste en cours ; P4 (ouverture du test tabulaire scellé) n’a pas été exécutée et doit rester fermée tant que P3 et le gel ne sont pas achevés.

### Portes

| Phase | Statut | Justification |
|---|---|---|
| P0 provenance/intégrité | PASS | hashes et CRC des sources ; 13 ARFF binaires conformes |
| P1 protocole | PASS documentaire | prompt JSON/Markdown identiques ; 13 contrôles de cohérence |
| P2 code/tests | PASS tests | 24/24 tests automatisés |
| P3 expériences | INCOMPLETE | REPLICA v004 en cours ; CNG v004, CNC v005, CNG LOO et D3Q v004 pas exécutés |
| P4 gel/test scellé | NOT STARTED | test scellé demeure en lecture seule et non consulté |
| P5 rapports/archive | PARTIAL | rapports par branche établis ; manifeste/ZIP final à achever |

## Résultats centraux

- Le contrôle D1/D2 est le résultat positif le plus solide : même fonction, mêmes paramètres, équivalence numériques et gradients vérifiée 40/40 ; gain de latence microbenchmark 1,75–4,0× selon batch.
- Le modèle partagé D3 a environ moitié moins de paramètres, mais n’a pas encore une preuve confirmatoire de qualité sur la grille f1/f2/f5/f6.
- REPLICA-U v003 termine 65/65 runs, mais il n’est pas conforme à l’étape de réentraînement complet du train extérieur ; ses résultats restent exploratoires. REPLICA-U v004 est la branche corrigée, commencée et auditée partiellement.
- CNG v001 a 18 runs exploratoires audités. La campagne KMeans v004 et les ablations LOO n’ont pas encore été exécutées.
- CNC v004 (seed1501) donne des résultats mixtes : C2 réduit beaucoup l’erreur sur g3 mais pas sur g1/g2/g5 ; C4 est très compact mais nettement moins précis que C3 sur graphes connus.
- Pas de mesure énergétique fiable. La mémoire RSS disponible est un pic de processus partagé et ne peut pas être attribuée par variante.

## Règle de vérité

Tous les nombres sont des mesures de validation ou de holdout de composition synthétique. Aucun score sur les 13 holdouts tabulaires scellés n’est publié. Tout run non exécuté est `NOT_RUN`; les quotas insuffisants sont `INCOMPLETE_QUOTA`. Les succès locaux ne sont pas extrapolés en supériorité générale.

## Limite d’exécution

REPLICA-U v004 : 11/65 blocs complets au snapshot et 0 échecs explicites. Le runner est séquentiel et chaque bloc inclut cinq folds OOF et les variantes préenregistrées ; les durées observées (≈22 s pour German Credit, ≈112–139 s pour Spambase) rendent la campagne complète coûteuse dans le quota CPU disponible. Les runs terminés sont conservés ; la campagne ne sera pas déclarée terminée par extrapolation.

## Livrables

Le workspace comporte prompt/préinscription, code versions, données et manifestes, journaux, checksums, tests, checkpoints, prédictions, rapports spécifiques aux branches et audit de récupération. La ZIP finale doit inclure seulement les artefacts EX11 et sera CRC-testée après stabilisation des registres.
