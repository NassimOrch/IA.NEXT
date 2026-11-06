# P13 — Audit final de livraison FulleGenBrain_f4_v0

## 1. Description

P13 vérifie les archives réellement distribuées après extraction propre. L’objectif de clôture est l’intégrité des trois paquets, le fonctionnement du noyau inclus, l’interface locale, la relocalisation des chemins, la fusion sans conflit et la reproductibilité des tests intégrés. Cette phase prépare la publication éventuelle par l’auteur; elle ne publie rien.

## 2. Architecture

- `Dmodel_FulleGenBrain_f4_v0.zip` : runtime Python standard-library, CLI, GUI loopback, exemples, schémas et code/configuration minimum pour les adaptateurs spécialistes actuellement branchés.
- `Amodel_FulleGenBrain_f4_v0.zip` : rapports normalisés P00–P13, reçus, journaux, preuves de provenance, inventaires de hachage et attestations.
- `suivi_model_FulleGenBrain_f4_v0.zip` : checklists, chemins, scripts, tests, benchmarks, formalismes et preuves JSON reproductibles.

Les sources historiques complètes, l’archive d’entrée, les anciens snapshots, les corpus d’entraînement et les fragments de base absents sont exclus selon la politique de livraison minimale. Chaque ZIP porte un `PACKAGE_MANIFEST.json` interne; les hashes exacts des ZIP sont détachés dans `release_manifest.json` et les sidecars `.sha256` pour éviter une référence circulaire.

## 3. Pipeline complet

1. Lire les chemins, la checklist, les deux registres d’erreurs et le dernier manifeste de sauvegarde avant exécution.
2. Vérifier CRC, taille, hash extérieur et hash de chaque membre des trois archives.
3. Extraire Dmodel dans un répertoire propre et exécuter 13 commandes de smoke test natives.
4. Démarrer la GUI sur `127.0.0.1`, vérifier la route `/` en HTML et `/api/health` en JSON, puis arrêter le processus proprement.
5. Extraire les trois paquets, les fusionner en refusant les conflits, puis relocaliser les chemins sans les dépôts historiques.
6. Exécuter la suite intégrée complète avec `ResourceWarning` traité comme une erreur.
7. Écrire la preuve P13 détachée, le rapport de clôture, la checklist et l’état courant; construire les archives finalisées et vérifier la nouvelle génération après extraction.

## 4. Commandes d'exécution

Depuis la racine du projet :

```bash
python scripts/run_checked.py --label p13-final-clean-extraction --kind model -- python -u scripts/p13_clean_extraction_validation.py --deliverables-dir ../deliverables --source-archive /mnt/data/source_orderX_0.zip
python scripts/run_checked.py --label p13-final-package-verification --kind no_model -- python scripts/p13_rebuild_and_verify_manifest.py
```

Pour une vérification manuelle du paquet livré :

```bash
unzip -t Dmodel_FulleGenBrain_f4_v0.zip
unzip -t Amodel_FulleGenBrain_f4_v0.zip
unzip -t suivi_model_FulleGenBrain_f4_v0.zip
```

## 5. Résultats

Le reçu de clôture `logs/executions/P13/20261026T173648246635+0000_p13-clean-extraction-after-sqlite-sidecar-race-fix.receipt.json` est `PASS`, avec code retour 0 et snapshot post-exécution `PASS`. La preuve détachée est `spec/evidence/P13_clean_extraction_validation.json`; le reçu du retest final est `logs/executions/P13/20261026T173648246635+0000_p13-clean-extraction-after-sqlite-sidecar-race-fix.receipt.json`.

- **Trois archives :** CRC, manifestes internes, inventaire des membres et SHA-256 vérifiés; les tailles exactes de la génération finale figurent dans `release_manifest.json`, et chaque archive est sous la limite de 200 000 000 octets.
- **13 commandes natives :** toutes terminées avec code retour 0, dont `doctor`, autotest, liste des composants/adaptateurs, inspection, validation/exécution d’un programme, synthèse/reprise, mémoire et ASCRC.
- **GUI :** HTML de la route `/` et statut JSON `PASS` de `/api/health`, serveur arrêté proprement.
- **Fusion/relocalisation :** zéro conflit de contenu, policy de chemins relocalisés `PASS`.
- **Suite intégrée après extraction et fusion :** **264 tests, 174 sous-tests réussis** en 25,44 secondes avec `ResourceWarning` traité comme erreur.
- **Suites sources isolées :** 175 tests cumulés dans les quatre suites ORDER/AAM/eGenBrain consignées séparément en P11.
- **Historique des erreurs :** les incidents historiques restent présents avec leurs preuves; les anciens échecs de construction/validation et la dernière interruption du wrapper sont explicitement résolus à partir de retests indépendants concordants. L’essai interrompu n’est pas compté comme un PASS. Aucune entrée historique n’a été supprimée.

L’archive source `source_orderX_0.zip` a également été contrôlée. Son SHA-256 observé est `e423f5f207eba4b38ed5606da81e00eb74504410f77c251a82dcef23a1ee3303`.

## 6. Interprétation des résultats

Ces résultats vérifient l’intégrité et le fonctionnement du périmètre livré sur les scénarios ci-dessus; ils ne constituent pas une preuve de correction de toute exécution possible. Les statuts `PARTIAL` et `NOT_RUN` restent visibles pour les sous-parties auxquelles manquent des artefacts exécutables d’origine. Aucun comportement manquant n’a été remplacé par une sortie simulée.

## 7. Conséquences : théoriques, conceptuelles et opérationnelles

- **Théoriques :** `formalisme_FulleGenBrain_5.tex`, `theorie_programation_compositionnelle_3.tex` et le formalisme opérationnel restent fournis; leurs sources V4/V2 restent conservées dans l’espace de travail source, mais les dépôts historiques complets ne sont pas redistribués.
- **Conceptuelles :** le formalisme FulleGenBrain garde l’autorité architecturale; la théorie compositionnelle définit le fondement; le prototype d’interface reste une référence d’ergonomie, pas une autorité sur le runtime.
- **Opérationnelles :** le runtime de base ne requiert que la bibliothèque standard Python; les composants spécialistes actuellement branchés sont fournis avec leur fermeture de fichiers/configurations minimale et les notices de provenance/licence. La publication reste une décision manuelle de l’auteur.

## 8. Conclusions

Les trois paquets finalisés sont prêts à être examinés, téléchargés et éventuellement publiés par l’utilisateur. Aucun dépôt distant n’a été créé, aucun push n’a été fait, et aucun service de publication n’a été appelé. Les manifestes SHA-256 détachés permettent de vérifier l’identité exacte des fichiers livrés.

## 9. Statut du modèle

**P13 : PASS pour le périmètre de livraison validé.** Les phases P00–P13 sont enregistrées `PASS` selon leurs critères de sortie. Les limites de données/source ci-dessous restent décrites explicitement et ne sont pas interprétées comme une prédiction générale de faisabilité ou d’échec.

- **eGenBrain base historique MG : `PARTIAL`.** `part01` a été haché et vérifié; `part02` n’était pas présent dans l’archive fournie. Le reassemblage de cette base n’a donc pas été exécuté et aucun octet de remplacement n’a été fabriqué. L’adaptateur mesh distinct est fourni et passé les contrôles.
- **AAM O94.6 et ORDER 80.4.7 : `NOT_RUN` comme runtimes autonomes.** Les artefacts fournis sont d’audit/comparaison, non des runtimes exécutables autoportants. Leur statut est documenté dans l’inventaire de provenance.
- **Publication publique : non effectuée.** Avant publication, l’auteur doit effectuer la revue humaine de la licence non commerciale et des notices tierces, comme décrit dans `release/READY_TO_PUBLISH.md`.
