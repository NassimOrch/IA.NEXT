# EX11 — addendum de récupération et correction du premier constat

Date : 2026-11-03 (Africa/Algiers)

## 1. Correction explicite

Le rapport `RECOVERY_AUDIT_2026-11-03.md` concluait à tort que `/mnt/data/EX11` ne contenait qu'un README vide et qu'aucun prompt, script ou manifeste EX11 n'avait été retrouvé. Une recherche complémentaire par inventaire exhaustif des fichiers a invalidé ce constat. Les artefacts existaient déjà dans le workspace avec des horodatages antérieurs à ce rapport. Le premier audit a donc produit un faux négatif ; il ne doit pas être utilisé comme état de vérité actuel.

Le rapport v001 est conservé pour préserver l'historique. Le présent addendum constitue la correction et l'état de récupération à retenir.

## 2. Artefacts EX11 retrouvés et vérifiés

- `prompt_ex11.json`, révision `2.2.0-reconstructed`, et `PRE_REGISTRATION_EX11.md` (corps synchronisé après normalisation de la terminaison de ligne).
- Sources formelles conservées dans `/tmp/ex11_audit` : `Replica_U_0.tex`, `th_sondes_core_test_0.tex`, `th_sondes_core_test_1.tex`, prompts EX3–EX9 et archives imbriquées EX4–EX10.
- 13 ARFF extraits sous `data/raw/datasets_arff/`, avec provenance SHA-256.
- 65 splits (13 datasets × 5 seeds), matérialisés en 195 CSV train/validation/test. Vérification indépendante relancée : `n_datasets=13`, `n_splits=65`, `all_pass=true`; lignes sources conservées exactement, schémas typés, multiplicité, empreintes et absence de chevauchement des groupes X contrôlés ; tests scellés mode 0440.
- Modèles `AdaptiveRBF`, CNG/CNC et REPLICA-U sous `src/models/`.
- Tests logiciels : 5/5 réussis lors du dernier run `p2_tests_final_2026-11-03.log`.
- Benchmark D1/D2/D3 d'équivalence et microperformance sous `results/resources/`, avec sortie et gradient D1/D2 équivalents dans la tolérance 1e-6.
- Campagne de qualité D3Q sur `f1`, seed 1501 : quatre checkpoints, quatre prédictions, journal append-only et script source `src/training/train_efficiency_quality.py`. Le SHA-256 du script correspond exactement au `code_sha256` des quatre lignes de registre.

## 3. Artefacts absents / limites de récupération

Aucun run complet REPLICA-U, CNG général, CNC général n'a été retrouvé : pas de checkpoint, prédiction ou métrique correspondante dans le workspace inspecté. Le code modèle existe, mais les scripts d'entraînement/évaluation complets REPLICA-U et CNC ne sont pas encore livrés. Les valeurs REPLICA-U/CNC annoncées dans des messages d'étape (log-loss sur cinq datasets, MAE C1/C2) ne disposent donc pas d'artefacts bruts correspondants et restent **non vérifiées**.

Le run D3Q f1/1501 est une seule graine sur une seule tâche ; ce n'est pas une campagne complète confirmatoire. Le MLP de D3Q v001 possède 1441 paramètres : il dépasse 4× D3_SHARED (359 paramètres), mais pas 4× D1/D2 (407 paramètres). Il ne vaut donc pas comme GE4X à l'égard de toutes les variantes.

## 4. Intégrité vérifiée à la reprise

- `sha256sum -c /mnt/data/EX11/INPUT_SHA256.txt` : les quatre entrées utilisateur passent.
- `last_sources_3.zip` et `datasets_arff.zip` présents et CRC vérifié dans les contrôles antérieurs ; les empreintes sont conservées dans le manifeste de provenance.
- Vérification indépendante des splits : 13/13 datasets, 65/65 splits, succès.
- Tests logiciels relancés : 5/5 passent.

Le fichier `checksums/phase1_sha256.txt` conserve un checksum antérieur de `splits_independent_verification.json`; ce dernier a été enrichi par la vérification détaillée et son checksum doit être recalculé dans le manifeste final. Ce décalage est un historique de version, pas une corruption des données.

## 5. Décision

Conserver tous les artefacts trouvés. Ne pas supprimer ni écraser les résultats v001. Les nouveaux essais auront des identifiants/versionnements distincts. Les campagnes REPLICA-U et CNC encore absentes doivent être soit implémentées et exécutées avec preuves, soit déclarées `NOT_RUN`/`INCOMPLETE_QUOTA`; aucune valeur issue d'un message d'étape ne peut être promue en résultat.
