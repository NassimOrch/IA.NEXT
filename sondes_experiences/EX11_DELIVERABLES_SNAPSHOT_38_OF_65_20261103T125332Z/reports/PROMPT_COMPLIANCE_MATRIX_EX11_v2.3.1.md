# Matrice de conformité EX11 — prompt v2.3.1-reconstructed (spécification scientifique 2.3.0)

Date de l’état : 2026-11-03, snapshot 2026-11-03 12:45 UTC, après 27/65 runs REPLICA-U v004. Cette matrice distingue la conformité documentaire, les tests du code et les expériences réellement exécutées. Elle ne transforme pas un script préparé en expérience terminée.

| Exigence du prompt | Preuve vérifiée | Statut |
|---|---|---|
| Aucune victoire/défaite présumée ; anti-triche et anti-sabotage directs/indirects | JSON v2.3.1 + préinscription synchronisée ; correction documentaire 2.3.1 | PASS documentaire |
| Workspace EX11 isolé ; pas d'archives historiques embarquées | inventaire EX11 | PASS ; archives EX3–EX10 restent à l'extérieur |
| Hash des sources `last_sources_3.zip`, `datasets_arff.zip`, rapport TEX/PDF | `INPUT_SHA256.txt` | PASS |
| ZIP ARFF CRC et extraction fidèle | `unzip -t`, comparaison binaire | PASS ; 13/13 ARFF identiques |
| Audit des schémas, NA, valeurs non finies, doublons, conflits | `data/metadata/dataset_audit_v002.json` | PASS |
| GINA préserve la frontière Train/Valid source | audit de données + manifestes | PASS documentaire et données |
| 65 splits / 195 CSV | `splits_manifest.json` + `splits_independent_verification.json` | PASS ; couverture exacte et groupes X disjoints |
| Test scellé en lecture seule | modes de `data/sealed_test` | PASS ; 65/65 fichiers CSV `0440` |
| Test scellé non chargé par les scripts d'entraînement | scripts/configs inspectés ; `test_access=false` | PASS pour les campagnes exécutées ; aucun score test produit |
| Prompt JSON et préinscription synchronisés | hash du corps + test octet | PASS ; version documentaire 2.3.1, contenu scientifique 2.3.0 |
| Tests unitaires/intégration | `PYTHONPATH=$PWD pytest -q` | PASS : 24/24 |
| D1/D2 équivalence sorties/gradients | `results/resources/d1d2_equivalence_10seeds.json` | PASS : 40/40 cas, erreur max sous `1e-6` |
| Microbenchmark D1/D2/D3 isolé avant campagne | `results/resources/d1d2d3_microbenchmark.csv/json` | PASS descriptif ; 1 thread, 30 warmups, 200 répétitions, 4 batchs |
| D1/D2/D3 mesure mémoire attribuable au modèle | RSS high-water commun au processus | NON DISPONIBLE ; aucune conclusion par modèle |
| Mesure d'énergie matérielle | aucun compteur valide | NOT MEASURED ; aucune allégation énergétique |
| D3Q v001 qualité (4 fonctions ×10 seeds ×4 variantes) | 160 lignes + 160 checkpoints/prédictions/configs réconciliés | COMPLET mais EXPLORATOIRE : KMeans non conforme et GE4X insuffisant face à D1/D2 ; temps contendus |
| D3Q confirmatoire v004 | script compilé + tests de tailles GE4X | NOT STARTED ; script v004 corrigé prêt, campagne après REPLICA-U v004 |
| REPLICA-U v003 13×5 | registre append-only + audit v002 | TERMINÉ 65/65 ; exploratoire, déviation de refit final (i_fit et non tout le train externe) |
| REPLICA-U v004 full-train refit, C1/T0, matched/GE4X pour les deux étudiants | `replica_u_campaign_v004.jsonl`, checkpoints, prédictions, rapport JSON, audit v002 | EN COURS : 9/65 blocs au snapshot ; 17/17 rapports présents passent l’audit indépendant |
| Ablations top-1/top-2/entrée désaccord | 24 sorties de validation post-hoc | PARTIAL ; aucun gain de calcul prouvé, car les 7 spécialistes sont encore calculés |
| CNG v001 | 18 checkpoints/prédictions/configs audités | COMPLET pour 18 runs, mais EXPLORATOIRE (KMeans absent) |
| CNG confirmatoire v004 | code/test préparé, MLP matched et GE4X par candidate, KMeans train-only, batchs appariés | NOT STARTED |
| CNG LOO F/R | script v004 compilé, dépend des A3 canoniques v004 | NOT STARTED |
| CNC v003/v004 | un run seed1501 par version, résultats conservés | PARTIAL : un seed1501 v003 exploratoire ; un seed1501 v004 KMeans, mais batch-order C3/C4 non apparié |
| CNC v005 comparatif C3/C4 avec batch-order apparié | script + runner compilés, test d'ordre apparié | NOT STARTED |
| Test final scellé après gel | aucun gel complet ; P3 incomplète | NOT STARTED / INTERDIT À CE STADE |
| Rapport final exhaustif et archive CRC | à réaliser après runs et gel | NOT STARTED |

## Limites et décision actuelle

P0/P1 (sources, prompt, données, partitions) sont closes. P2 (implémentation et contrôles logiciels) passe les 24 tests. P3 reste incomplète : REPLICA-U v004 a commencé (33/65), tandis que CNG v004, CNC v005, CNG LOO et D3Q v004 n’ont pas encore commencé. P4 (test scellé) ne doit pas être lancée. P5 (livrables finaux) sera créée à partir des artefacts EX11 effectivement persistés, sans copier `last_sources_3.zip` ni les archives EX3–EX10.

Les mesures de RSS ne permettent pas d'attribuer une consommation mémoire par variante, et aucun instrument d'énergie n'est disponible. Les résultats D3Q/REPLICA/CNC chronométrés pendant des campagnes parallèles sont `CONTENDED_OR_EXPLORATORY`, pas des preuves confirmatoires de vitesse.
