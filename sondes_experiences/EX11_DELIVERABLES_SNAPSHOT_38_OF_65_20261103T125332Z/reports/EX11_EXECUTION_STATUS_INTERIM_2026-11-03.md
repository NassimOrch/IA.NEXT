# EX11 — état d'exécution intermédiaire vérifié

Date : 2026-11-03 (Africa/Algiers)

Ce document est un instantané des exécutions réellement constatées. Il ne vaut pas rapport final et ne transforme pas les campagnes incomplètes en expériences terminées.

## Intégrité et provenance

- `last_sources_3.zip` SHA-256 : `7fe025ea6adc6581843f6cd8d776eb7399bb5f6849dc53da755a1324beb243c4`, conforme à l'empreinte inscrite dans la reconstruction de `prompt_ex11.json`.
- `datasets_arff.zip` SHA-256 : `a2c5feb334d622fe5197a1a0a8621c5b286947b0693bc05955b990597e44f041`; CRC ZIP valide.
- Les 13 fichiers ARFF extraits d'EX11 sont identiques octet pour octet aux entrées de `datasets_arff.zip`.
- Les 65 fichiers CSV de test sont en mode `0440`; le README du répertoire scellé a été verrouillé également. Aucun script d'entraînement actif ne référence `data/sealed_test`.
- `prompt_ex11.json` est la reconstruction versionnée `2.2.0-reconstructed`, et non une récupération prétendue d'une version antérieure. La préinscription expose la règle de non-succès/non-échec présumé et l'interdiction explicite du sabotage direct ou indirect.

## Implémentation

- `python -m compileall -q src tests` : PASS.
- `PYTHONPATH=/mnt/data/EX11 pytest -q` : 17 tests PASS.
- Audit D3Q au dernier passage : 100 runs alors présents, tous les checkpoints/prédictions rapprochés ; la campagne append-only a continué après cet audit et doit être auditée à nouveau en fin de campagne.
- Audit REPLICA au dernier passage : 21 runs scientifiques vérifiés, le smoke test restant explicitement `SMOKE_ONLY`. La campagne a continué depuis.

## Mesure d'efficacité pré-campagne

Le benchmark D1/D2/D3 a été exécuté à 10:24, avant le lancement du processus D3Q (10:25) et de REPLICA-U (10:46). Matériel/environnement : AMD EPYC 9V74, PyTorch CPU 2.10.0, quota cgroup 2 CPU, mémoire cgroup 4 GiB, un thread, 30 échauffements et 200 répétitions par batch.

- D1/D2 : 819 paramètres chacun ; D3_SHARED : 411 paramètres.
- Erreur absolue maximale D1/D2 : sorties `1.1921e-7`, gradients d'entrée `4.0745e-10`, gradients paramètres `2.9802e-8`; tolérance `1e-6`, test réussi.
- Latence forward p50 D1/D2 (ms) : batch 1 `0.2487/0.0615`; 16 `0.2707/0.0761`; 64 `0.3357/0.1207`; 256 `0.5889/0.3366`.
- Latence train-step p50 D1/D2 (ms) : batch 1 `1.4207/0.4426`; 16 `1.4926/0.5105`; 64 `1.7030/0.6662`; 256 `2.1799/1.1069`.
- Le rapport de mémoire RSS haute-water du processus est identique dans ce fichier et ne permet pas d'attribuer un avantage de mémoire à une architecture. Aucune mesure d'énergie matérielle n'est disponible.

## Exécutions P3 en cours à l'instantané

Les processus actifs identifiés sont `train_efficiency_quality.py` (D3Q v001) et `train_replica_campaign_v003.py` (REPLICA-U v003). Ils utilisent chacun un thread, mais fonctionnent simultanément sur un quota de 2 CPU.

- D3Q v001 : 106 lignes `COMPLETED` dans `d3_quality_runs.jsonl` ; tâches f1 et f2 complètes (10 seeds × 4 variantes), f5 partielle ; f6 non commencé. Objectif de campagne : 160 runs.
- REPLICA-U v003 : 22 blocs `COMPLETED_VALIDATION_ONLY` dans le registre de campagne ; 3 datasets complets et 7 runs GINA/KC1 à l'instantané. Objectif : 65 blocs dataset-seed.
- CNC v004 seed 1501 : terminé, code retour 0, statut `COMPLETED_VALIDATION_AND_HELDOUT_COMPOSITION`; les runs v002 (échec de sauvegarde) et v003 (initialisation antérieure) sont conservés, pas écrasés.
- CNG v001 : 18 runs historiques terminés (f1/f2, seed 1501, initialisation antérieure non-KMeans), classés exploratoires. La campagne confirmatoire `train_cng_suite_v002.py` n'est pas encore lancée.

## Contention et validité des temps

À l'exception du microbenchmark pré-campagne décrit ci-dessus, les mesures `train_seconds` de D3Q v001 et REPLICA-U v003 ont été produites pendant une contention CPU documentée (deux processus intensifs pour un quota de deux CPU, avec des phases de recouvrement). Les métriques de qualité et artefacts de prédiction restent exploitables ; ces durées ne doivent pas servir à une conclusion confirmatoire de vitesse relative. Un profilage end-to-end isolé est requis après la fin des campagnes actives.

## Décision méthodologique

Aucun test scellé n'a été ouvert. Les campagnes en cours ne sont pas arrêtées. Les campagnes confirmatoires et ablations non commencées restent explicitement `NOT_STARTED` ou `INCOMPLETE_QUOTA`, sans extrapolation.
