# EX11 — workspace expérimental dédié

EX11 est isolé sous `/mnt/data/EX11/`. Les archives historiques EX3–EX10 et `last_sources_3.zip` restent hors de ce workspace. Les seules données tabulaires réelles copiées ici sont les 13 données ARFF jointes pour EX11. Les tâches CNG/CNC synthétiques sont générées par les scripts EX11.

## Protocole courant

- `prompt_ex11.json` : prompt reconstruit et versionné **2.3.1-reconstructed**. Ce fichier est une reconstruction contrôlée à partir des sources accessibles ; il n'est pas présenté comme une récupération d'une ancienne version introuvable.
- `PRE_REGISTRATION_EX11.md` : corps du prompt, strictement identique au champ `prompt` du JSON au niveau octet.
- `reports/PROMPT_COMPLIANCE_MATRIX_EX11_v2.3.1.md` : matrice de conformité courante, avec statut réel de chaque branche.
- `AUDIT_SOURCES_EX11.md` : analyse des sources et formalismes EX3–EX10 sans copie des archives historiques.
- `INPUT_SHA256.txt`, `checksums/` et les manifestes sous `data/metadata/` : provenance et intégrité.

## Données

- `datasets_arff.zip` passe le test CRC ; SHA-256 comparé à la pièce jointe.
- Les 13 ARFF présents sous `data/raw/datasets_arff/` sont identiques octet pour octet aux fichiers correspondants dans l'archive.
- Les 65 splits (13 jeux × 5 seeds) et 195 CSV train/validation/test ont passé une vérification indépendante : toutes les lignes source une fois, groupes X disjoints, schémas/hashes conformes.
- Les 65 CSV de test sont en mode `0440`. Aucun entraînement ni réglage n'utilise ces fichiers.
- Les doublons X, conflits de labels et chevauchements inter-jeux PROMISE sont documentés ; ils n'ont pas été supprimés.

## Code et tests

- Scripts réellement utilisés conservés dans `src/`, configs dans `configs/`, sorties dans `results/`, journaux append-only dans `logs/`.
- Test courant : `PYTHONPATH=$PWD pytest -q` → **24/24 PASS**.
- Les scripts confirmatoires préparés sont compilés : REPLICA-U v004, CNG v004, CNC v005, D3Q v004 et LOO CNG v004. Une compilation ou un test unitaire ne vaut pas exécution scientifique.

## État expérimental

L'instantané détaillé le plus récent est `reports/EX11_PROGRESS_ADDENDUM_2026-11-03_1249UTC.md`. Au moment de cet addendum, REPLICA-U v004 était à 31/65 blocs confirmatoires, tous audités ; le runner séquentiel PID 11597 était actif. Les campagnes confirmatoires CNG v004, CNC v005, CNG LOO v004 et D3Q v004 n'avaient pas encore inscrit de runs. Les branches historiques v001/v003/v004 sont conservées avec leurs statuts exploratoire ou partiel explicités.

La révision documentaire du prompt 2.3.1 corrige uniquement le numéro affiché dans le corps et le type du champ `key_design`; elle ne modifie aucune règle ou aucun budget scientifique. La version 2.3.0 est la spécification scientifique appliquée par les premiers runs v004.

La livraison finale et l'archive CRC restent à produire après consolidation. Si les budgets confirmatoires ne peuvent pas être achevés dans ce quota d'exécution, les blocs manquants seront explicitement `INCOMPLETE_QUOTA`, jamais extrapolés.

La présence d'un script ou d'un checkpoint partiel n'est jamais présentée comme une expérience complète. Tous les runs défavorables, échoués, interrompus, exploratoires ou non conformes restent conservés et identifiés.
