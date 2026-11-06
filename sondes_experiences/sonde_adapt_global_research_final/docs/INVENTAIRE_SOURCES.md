# Inventaire des sources — livraison v2

## Archive reçue

- Fichier : `sources_ng_adapt_0.zip`
- Taille comprimée : 242 262 864 octets
- SHA-256 : `8fcf82931988a96cdfb1ff5cbe5892142b4b1174385dc87cd9ed0f9e2d7069bb`
- `zipfile.testzip()` : PASS, aucun membre corrompu
- 26 entrées dans le ZIP, 22 fichiers non-répertoire, 261 469 222 octets non comprimés cumulés
- `prompt.txt` : 35 706 octets, 1 002 lignes; copie non modifiée dans `source_copies/prompt.txt`
- Archives ZIP imbriquées : 80 archives répertoriées dans `logs/recursive_archives.jsonl`; 80 contrôlées/extraites, 0 échec d'intégrité, 0 chemin dangereux détecté, 0 membre symlink. Somme des tailles décompressées déclarées par ces archives : environ 607 226 190 octets (non dédupliquée).

Le script `code/recursive_archive_audit.py` effectue les contrôles en flux, refuse les chemins de traversal et conserve les résultats par archive. Il s'agit d'une extraction séparée; les sources originales n'ont pas été modifiées.

## Inventaire complet des fichiers extraits

En complément des 80 contrôles ZIP, tous les fichiers réguliers présents dans deux vues d'extraction ont été hachés :

- Arbre de travail extrait : **10 838 fichiers**, **869 746 379 octets** cumulés.
- Extraction récursive dédiée : **4 132 fichiers**, **378 456 251 octets** cumulés.
- Total des deux vues (les fichiers répliqués entre les arbres sont comptés dans chaque vue) : **14 970 entrées**, **1 248 202 630 octets**.

Manifestes complets : `results/source_audit/recursive_source_file_manifest.csv` (chemin relatif, taille, SHA-256, suffixe, type et résultat de validation) et `results/source_audit/recursive_source_inventory.json` (synthèse machine-lisible). Dans le corpus combiné apparaissent notamment 3 636 fichiers `.json`, 1 378 fichiers `.jsonl`, 2 045 fichiers `.py`, 349 fichiers `.tex`, 106 fichiers `.pdf` et 1 226 poids/checkpoints `.pt`. Ces nombres comptent les copies entre les deux arbres, pas des éléments uniques dédupliqués.

Contrôles syntaxiques automatisés : **0 erreur AST Python parmi les fichiers `.py`** et **0 signature PDF non conforme** (test de l'en-tête `%PDF-`; ce dernier n'est pas une validation complète de chaque PDF). Quatre chemins `.json` ont échoué au parseur, mais ils ne représentent que deux journaux stdout vides (`composition.stdout.json` et `imitation.stdout.json`), recopiés dans les deux arbres. Un fichier JSONL contient une ligne invalide supplémentaire : `batch_dataset.jsonl`, ligne 784 tronquée. Ces erreurs ont été conservées et documentées; aucune correction n'a été injectée dans les sources.

Le manifeste hache aussi les fichiers binaires; cela prouve leur identité, pas leur contenu sémantique. Les poids de modèle `.pt` ne sont pas interprétés comme de la théorie ou comme preuve d'une propriété du modèle.

## Niveaux prioritaires

| Source | Nature | Traitement de cette livraison |
|---|---|---|
| `sonde_adapt_1_bundle.zip` | Formalisme original et études expérimentales | ZIP SHA-256 `0825554aeaac3f570f052fca43806be133f1dc0e49d836bf0fcecc5190cb5465`, 110 206 894 octets, 1 265 membres, intégrité PASS; document source prioritaire copié vers `source_copies/etude_et_formalisme_sonde_adaptative_1.tex`, et rapport de comparaison théorie/observation également copié. |
| `th_emp/DDD_Base_theorie_des_empreintes_complete_order_5.tex` | Théorie générale des empreintes | Copie conservée sous `source_copies/`; SHA-256 dans le manifeste des sources utiles. |
| `th_emp/observation_formalisme_full_0_bundle.zip` | Formalisme observationnel et dossier de preuve | Validateur fourni exécuté : code 0; PDF interne de 109 pages, SHA et contrôles internes vérifiés, pas de référence LaTeX non résolue. |
| `sondes_adaptatives/experience_NGeGenBrain_sondes_adaptatives_bundle_final_v1_2.zip` | Expérience, protocole et validation | Validateur `validate_delivery_v1_2.py` exécuté dans une copie de travail : `PASS_WITH_LIMITATIONS`, 16/16 contrôles, code 0. La validation est un audit de paquet, pas une preuve de supériorité scientifique. |
| `sondes_adaptatives/experience_sondes_adaptatives_bundle.zip` | Expérience historique | Archives et scripts recensés; résultats référencés dans les documents de reproduction lorsque scripts et configuration étaient exécutables. |
| `NGeGenBrain/Amodel_NGeGenBrain_v1.zip`, `Dmodel_NGeGenBrain_v1.zip`, `suivi_model_NGeGenBrain_v1.zip` | V1 / code et suivi | Présence et archives contrôlées dans l'inventaire récursif; sources et reçus antérieurs pris en compte sans prétendre re-exécuter toutes les commandes Windows. |
| `NGeGenBrain/Amodel_NGeGenBrain_v2.zip`, `Dmodel_NGeGenBrain_v2.zip`, `suivi_model_NGeGenBrain_v2.zip` | V2 / modèle et suivi | Manifest du paquet Dmodel v2 vérifié sur une extraction propre : 417 entrées, 417 présentes, 0 inattendue, 0 manquante. |
| `NGeGenBrain/NGeGenBrain_v3.zip` | V3.1 et matériaux étendus | Archives récursives auditées; extraction Dmodel v3.1 à la demande; manifeste propre valide (794/794), 66 tests Pytest et 65 tests de non-régression V1 exécutés avec succès. Les mesures du rapport interne (BPB/router/checkpoints) restent des observations consignées par ce projet, distinctes de notre nouvelle campagne de probes. |
| `dataset/Screenplay_dataset.jsonl` | Dataset JSONL | 4 000 lignes syntaxiquement valides, 2 000 objets distincts et 2 000 duplications excédentaires (chaque objet distinct apparaît deux fois). |
| `dataset/batch_dataset.jsonl` | Dataset JSONL | 784 lignes, 783 objets JSON valides, dernière ligne 784 tronquée; conservée et signalée, non réparée silencieusement. |
| `dataset/smsspamcollection.zip` | Dataset SMS | ZIP valide, 3 membres; contenu audité séparément. |
| `dataset/0000.parquet` | Dataset Parquet | Fichier reconnu comme Apache Parquet, magique `PAR1` en tête et en fin, 2 306 545 octets; contenu tabulaire non décodé, car `pyarrow`, `duckdb`, `polars`, `fastparquet` et `parquet-tools` ne sont pas installés. Ne pas considérer les lignes de ce fichier comme analysées. |

## Traçabilité et fichiers de référence

- Liste des 22 fichiers de premier niveau : `results/source_audit/source_manifest.csv` et `.json`; manifeste exhaustif des deux arbres d’extraction : `results/source_audit/recursive_source_file_manifest.csv` et `recursive_source_inventory.json`.
- Audit de 80 archives imbriquées : `logs/recursive_archives.jsonl`.
- SHA-256 des artefacts de livraison : `SHA256SUMS.txt` (après génération finale).
- Inventaire de datasets : `results/dataset_audit/dataset_inventory.json`.
- Source théorique de l'observation et preuve de validation : `logs/observation_bundle_validator.stdout.log`.

## Limites d'étendue

Toutes les archives du paquet ont été inventoriées et testées au niveau archive. Les sources mathématiques prioritaires et scripts expérimentaux pertinents ont été lus / exécutés selon le registre de phase. Cela ne signifie pas que chaque fichier binaire, chaque document historique et chaque checkpoint NGeGenBrain a été reproduit expérimentalement; ceux-ci ont leurs propres limites et statuts déclarés dans `ETAT_DES_PHASES.md` et `LIMITES_ET_INCERTITUDES.md`.


## Suppléments expérimentaux ajoutés à partir du prompt

- `results/fingerprint_feedback_loop/`: expérience FBR-1 (15 paires modèle/graine, 390 métriques, 54 000 événements); ancienne agrégation incohérente conservée en quarantaine et non utilisée pour les résultats finaux.
- `results/reconstruction_feedback_gate/`: expérience causale RBF-R1 (6 paires, 162 métriques, 23 040 événements); checkpoints atomiques individuels par modèle/graine.
- `figures/fbr1_archC_clean_vs_misleading.png` et `figures/rbf_r1_reconstruction_policy_rmse.png`: graphiques calculés directement à partir des CSV finaux par graine.
- `CONFORMITE_PROMPT_DETAILLEE.md`: crosswalk des dix phases et vingt-cinq règles rouges du prompt extrait.
- Le PDF de formalisme est compilé à 7 pages A4 et rendu après la dernière modification; les images de contrôle et le journal LaTeX sont dans `logs/`.
