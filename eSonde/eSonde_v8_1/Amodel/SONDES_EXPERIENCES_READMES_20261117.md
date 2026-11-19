

===== EX11_DELIVERABLES_SNAPSHOT_38_OF_65_20261103T125332Z/README_EX11.md =====
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


===== EX12_NEXT_0/EX12_NEXT_0_DELIVERABLES/README_EX12.md =====
# EX12_NEXT_0

Workspace expérimental autonome. Source of truth: `prompt_ex12.json`; rapport directeur: `/mnt/data/rapport_prigramme_expermentale_EX12_NEXT_0.tex`. Les sources historiques sont consultées en lecture seule et ne sont pas copiées dans ce workspace.

Phases séquentielles : P0 audit/gel ; P1 banc informatique ; P2 criblage ; P3 généralisation ; P4 MLP apparié ; P5 qualité/ressources/stabilité ; P6 ablations ; P7 lock/scoring/audit. Voir `00_governance/PRE_REGISTRATION_EX12.md`.

Aucune conclusion de performance n'est présumée. `phase_gate.json` est obligatoire.


===== EX12_NEXT_0/P1_ORIGINAL_SCRIPT_INVESTIGATION/P1_ORIGINAL_SCRIPT_INVESTIGATION/README_EVIDENCE_PACKAGE.md =====
# Evidence package — P1_RUN_001 / P1_RUN_002 source provenance

This package preserves result artifacts, metadata, registries, later canonical scripts, the forensic audit script and the signed declarative investigation report.

## Key finding

The result CSV/JSON artifacts for P1_RUN_001 and P1_RUN_002 exist and their stored timing aggregates recompute from raw measurements. The exact original producer scripts and contemporaneous producer hashes were not found in the accessible environment. The reusable, hash-linked scripts for P1_RUN_003/P1_RUN_004 were created after the first two result sets and are not represented as their originals.

## Layout

- `evidence/P1_RUN_001_FAILED/`: failed prototype result files and failure note.
- `evidence/P1_RUN_001_ROOT_DUPLICATE/`: byte-identical duplicate result artifacts found at P1 root.
- `evidence/P1_RUN_002/`: provisional result files and end-to-end comparison limitation note.
- `evidence/CANONICAL_RUN_003_004_SOURCES/`: later scripts, hashes and run-specific metadata; not original RUN_001/002 sources.
- `evidence/GOVERNANCE_AND_EXISTING_REPORTS/`: run registry, phase gate and P1 report materials.
- `evidence/ENVIRONMENT_AND_AUDIT/`: repeatable forensic audit source and machine-readable output.
- `P1_SOURCE_CHRONOLOGY.csv`: chronology table used in the report.
- `P1_ORIGINAL_SCRIPT_FORENSIC_REPORT.md/.pdf`: signed declarative report.

## Reproduction

Run the audit script from the EX12 workspace's pinned Python environment, or from the path recorded in the JSON report. The script independently checks artifact existence, hashes, raw-to-summary recomputation, available script timestamps, `.pyc` headers, and accessible environment history locations. It does not claim to regenerate the original P1 producer code.

## Limits

The container is `uid=0(root)` but cannot inspect inaccessible host overlay layers or host audit logs. The report therefore states a code-retention/provenance gap and does not infer sabotage, theft or an intentional deletion from missing files alone.


===== EX9_v011_DELIVERABLES/README_EX9.md =====
# EX9 v011 — Sondes adaptatives

Workspace autonome. Les sources EX3–EX8 sont restées à l'extérieur ; aucun ZIP historique, ancien checkpoint ni backup EX3–EX8 n'est livré dans ce dossier.

## Livrables prioritaires

- `prompt_ex9.json` : prompt EX9 final validé ; copie exacte dans `deliverables/prompt_ex9.json`.
- `deliverables/SYNTHESE_EX9_v011.md` : verdict global et état d'achèvement.
- `deliverables/SYNTHETIC_CONFIRMATION_EX9.md` : résultats des deux tests synthétiques gelés.
- `deliverables/th_sondes_core_test_1.tex` et `.pdf` : théorie corrigée CNG/CNC.
- `MODEL_LOCK.json` : verrou historique 45 runs XOR8 avant tentative d'ouverture ; XOR8 est ensuite déclaré compromis/non scoré.
- `MODEL_LOCK_MULTI_DOMAIN.json` : snapshot pré-test de 295 hashes pour concentric2/rotated_moons2, tests synthétiques scorés une fois ; contrôle post-test 294/295, avec une exception de rapport uniquement (voir `reports/PROMPT_EX9_AUDIT_LOCK_EXCEPTION.md`).

## Exécution réellement présente

- Historique EX8 : catalogue A0–A4, B1–B11 ; récupération intégrale B10/B11, checkpoints, traces, prédictions, configurations et contrôles d'intégrité. Voir `reports/EX8_VARIANT_CATALOG.md` et `inputs/AUDIT_SOURCES_EX9.md`.
- Classification XOR8 développement : 45 runs Rev2 B10/B11/A0 + deux MLP par candidate/seed ; audit validation PASS 45/45 ; les candidates perdent contre MLP.
- Ablations B10 : 7 familles × 5 seeds = 35 runs table-only ; audit PASS 35/35 ; exploratoires sur validation réutilisée.
- Deux domaines synthétiques supplémentaires : concentric2 et rotated_moons2, 45 runs par domaine ; audit validation PASS 90/90, historiques MLP conservés.
- Holdouts synthétiques concentric2/rotated_moons2 : 90 scores ; audit post-score PASS 90/90 ; les trois sondes perdent 5/5 face aux deux MLP dans chacun des deux domaines.
- Coeur neuronal : 3 pilotes CNG et 6 spécialistes CNC, audit PASS 9/9 ; pas de graphes CNC complets C1/C2.
- `th_sondes_core_test_1.tex` compile en PDF après correction du prérequis LaTeX.

## Verdict scientifique

Les performances positives EX8 de B10/B11 sur Wisconsin sont historiques et spécifiques au domaine de développement. Elles ne se reproduisent ni sur XOR8 ni sur les deux domaines synthétiques additionnels. Sur concentric2/rotated_moons2, les log-loss test des sondes sont de 0,2009–0,2561 contre 0,0586–0,0649 et 0,1210–0,1223 pour les MLP ; les p50 batch1 CPU des sondes sont environ 12–22× plus élevés. Le ratio de paramètres face au MLP_GE4X est bien ≥4× mais ne compense ni la perte de qualité ni la latence.

Aucune donnée réelle externe vierge n'a été obtenue ; la conclusion n'est donc pas une confirmation générale sur données du monde réel. FLOPs/MAC complets, RSS peak par run et énergie restent non mesurés. Les extensions A0, les ablations de partage/distillation/kernels B10/B11 et la campagne complète CNG/CNC restent partielles.

## Audits

```bash
python -m pytest -q tests
python src/audit_classification.py
python src/audit_checkpoint_deserialization.py
python src/audit_b10_ablations.py
python src/audit_core_pilot.py
python src/audit_multi_domain.py
python src/audit_multi_domain_test_metrics.py
```

Ne pas exécuter `src/score_sealed_test.py` (XOR8 compromis) ni `src/open_score_multi_synth.py --open-test` (les deux tests synthétiques additionnels sont déjà ouverts/scorés). Les scripts d'audit lisent uniquement des artefacts déjà sauvegardés et ne réentraînent pas de modèles.

Voir `reports/EVIDENCE_MATRIX_EX9.md`, `reports/REPORT_EX9_FINAL.md`, `reports/TRACE_CAPTURE_GAP.md` et `FAILURES_AND_DEVIATIONS.md` avant toute reprise.


===== sonde_adapt_1_bundle/adaptive_base/README_experience_sondes_adaptatives.md =====
# Expérience : réseau neuronal vs sondes adaptatives

## Contenu

- `rapport_experience_sondes_adaptatives.pdf` : rapport de résultats.
- `rapport_experience_sondes_adaptatives.tex` : source LaTeX du rapport.
- `experience_sondes_adaptatives.py` : expérience entièrement reproductible.
- `resultats_experience_sondes.csv` : métriques de chaque modèle et de chaque initialisation.
- `synthese_experience_sondes.json` : paramètres du protocole et statistiques récapitulatives.
- `frontieres_decision_sondes.png` : figure des frontières de décision.

## Réexécution

Dépendances : Python 3, `numpy`, `torch`, `scikit-learn`, `matplotlib`.

```bash
python experience_sondes_adaptatives.py
```

Le script réutilise les graines inscrites dans le code et écrit le CSV, le JSON et le PNG dans le même dossier.

## Résumé

- Réseau neuronal MLP : 49 paramètres entraînables ; précision moyenne 95,870 %.
- Sondes radiales adaptatives : 49 paramètres entraînables ; précision moyenne 96,005 %.
- Sondes radiales fixes (ablation) : 13 paramètres entraînables ; précision moyenne 86,230 %.

Les résultats décrivent un banc d'essai synthétique (`two moons`) et ne sont pas une expérience de reconstruction d'un LLM. Les écarts-types rapportés concernent cinq initialisations du modèle sur un jeu de test fixe ; ils ne mesurent pas à eux seuls l'incertitude liée à toutes les données possibles. Les sondes adaptatives sont une architecture apprenable, apparentée aux réseaux à fonctions de base radiales : l'expérience ne prouve pas qu'une sonde est fondamentalement différente d'un neurone.


===== sonde_adapt_1_bundle/adaptive_v1_2/README.md =====
# NGeGenBrain — expérience sur les sondes adaptatives et les neurones

## Objet

Ce dépôt est une expérience exécutée pour examiner, de manière circonscrite, si une sonde RBF adaptative peut (A) apprendre une tâche, (B) apprendre une partie de sa règle d'adaptation, (C1) imiter le comportement entrée-sortie de neurones artificiels simples observés en boîte noire et (C2) remplacer des unités cachées dans une composition de réseau.

Le travail part des deux références originales conservées dans `references/` :
- `NGeGenBrain_observation_formalisme_full_0.tex`
- `rapport_experience_sondes_adaptatives.tex`

La théorie de départ définit une sonde comme un opérateur d'observation spécifié et contrôlé ; elle ne définit pas déjà toute sonde comme un réseau qui apprend. L'adaptation est une extension expérimentale explicitement ajoutée dans `formalisme_sonde_adaptative.tex`. Un complément réel multiclasse sur les chiffres manuscrits a été ajouté séparément avec le protocole gelé `protocole_cas_reel_multiclasse_v1.md`.

## Résultats importants en une page

- Le noyau confirmatoire comprend quatre tâches : `two_moons`, `circles`, `xor_product` et le jeu public Wisconsin Diagnostic Breast Cancer. Un complément distinct préenregistré utilise aussi le jeu `load_digits` à dix classes (1 797 images, graines 1428/2539/3640). Un second supplément séparé filtre ce même jeu à la tâche binaire 3-vs-8 (357 images, 64 pixels, graines 714/825/936), avec son propre protocole et son propre audit.
- Les méthodes comprennent une RBF adaptative A, une RBF à taux par groupe méta-appris B, un contrôle RBF fixe et un MLP à 16 unités tanh.
- L'imitation isolée couvre 9 neurones cibles affines+activation (3 tanh, 3 ReLU, 3 sigmoïdes), 3 budgets (64, 256, 1024 paires entrée-sortie) et 3 initialisations indépendantes de sonde : 81 ajustements. Les sorties de test sont réservées à l'évaluateur.
- La composition remplace 1, 4 ou 16 unités cachées dans deux tâches. L'ancienne exécution de composition v1.1 utilisait par erreur les graines de classification 714/825/936 au lieu des graines de composition prescrites 411/522/633. Elle est préservée dans `audit/superseded_composition_chunks_v1_1/` et **exclue** des synthèses finales. La composition a été relancée avec les graines prévues, selon le correctif v1.2 haché avant la relance.
- L'audit indique `PASS_WITH_LIMITATIONS`. Les hachages de lignes des partitions sont disjoints ; les interfaces d'entraînement ne reçoivent pas les labels de test ni les paramètres des neurones imités. L'orchestration n'est cependant pas un bac à sable OS hostile : l'audit ne prouve pas l'impossibilité de tous les canaux cachés.

## Fichiers principaux

- `rapport_experience_sondes_adaptatives_complet.pdf` : rapport scientifique principal.
- `rapport_experience_sondes_adaptatives_complet.tex` : source LaTeX du rapport.
- `rapport_supplement_cas_reel_digits.pdf` / `.tex` : rapport dédié au supplément binaire 3-vs-8.
- `formalisme_sonde_adaptative.pdf` et `.tex` : formalisation mathématique de l'extension expérimentale.
- `protocole_preregistere.md` : protocole v1.1 pour classification/imitation et intentions de composition.
- `protocole_preregistere_composition_v1_2.md` : correctif versionné de la composition, révélant explicitement la divergence de graines et gelé avant sa relance.
- `protocole_cas_reel_multiclasse_v1.md` : complément préenregistré sur le benchmark réel dix classes.
- `protocole_supplement_digits_v1_0.md` et `protocole_supplement_digits_v1_0_1.md` : protocole déjà exécuté pour 3-vs-8 et correctif du sérialiseur d’audit uniquement.
- `rapport_supplement_cas_reel_digits.pdf/.tex` : rapport autonome du supplément binaire déjà exécuté.
- `protocole_supplement_digits_v1_0.md` et `protocole_supplement_digits_v1_0_1.md` : supplément indépendant 3-vs-8 et correction administrative du sérialiseur.
- `src/` : scripts d'entraînement, d'imitation, de composition, d'audit et de construction de rapport.
- `results/` : résultats par graine, prédictions après gel, tableaux de synthèse, fidélité des activations et résultats de composition.
- `figures/` : graphiques générés par le pipeline.
- `audit/` : gel pré-exécution, empreintes, audits d'intégrité (principal et chiffres), registre des partitions, replay déterministe et anciennes sorties de composition supersédées.
- `manifest_checksums.json` : SHA-256 des fichiers du bundle, hors manifeste lui-même et fichiers intermédiaires de compilation. `audit/audit_integrite_finale.json` agrège les contrôles finaux ; `audit/audit_integrite_digits_3_vs_8_finale.json` valide les résultats binaires déjà produits sans réentraîner les modèles ni modifier les CSV.
- `experience_NGeGenBrain_sondes_adaptatives_bundle.zip` (archive créée à la finalisation, dans le dossier parent) et `checksums_experience_NGeGenBrain_sondes_adaptatives.sha256` (SHA-256 de l’archive).

## Reproduction dans un environnement Python compatible

Versions mesurées lors de cette exécution : Python 3.13 (ou compatible), PyTorch 2.10.0+cpu, NumPy 2.3.5, pandas 2.2.3, scikit-learn 1.8.0, SciPy 1.17.0 et Matplotlib 3.10.8. Les dépendances principales figurent dans `requirements.txt`.

Depuis la racine du dépôt :

```bash
python -m pip install -r requirements.txt
python src/run_classification_stage.py
python src/run_imitation_stage.py
for seed in 411 522 633; do
  python src/run_composition_chunk.py two_moons "$seed"
  python src/run_composition_chunk.py breast_cancer "$seed"
done
python src/finalize_and_audit.py
python src/build_report.py
pdflatex -interaction=nonstopmode rapport_experience_sondes_adaptatives_complet.tex
pdflatex -interaction=nonstopmode rapport_experience_sondes_adaptatives_complet.tex
pdflatex -interaction=nonstopmode formalisme_sonde_adaptative.tex
pdflatex -interaction=nonstopmode rapport_supplement_cas_reel_digits.tex
pdflatex -interaction=nonstopmode rapport_supplement_cas_reel_digits.tex

# Supplément distinct chiffres 3-vs-8 (exécution déjà enregistrée dans les CSV)
python src/run_digits_real_supplement.py

# Complément réel multiclasse (si on veut recalculer les chiffres manuscrits)
python src/run_digits_experiment.py
# Si cette commande atteint une limite de durée après la classification,
# la classification a été sauvegardée avant la composition ; exécuter alors :
python src/run_digits_composition_only.py
python src/build_digits_figures.py
python src/insert_digits_section.py
python src/finalize_delivery.py
```

Les scripts de composition ignorent un chunk déjà présent. Les CSV finaux de chiffres manuscrits ont été contrôlés séparément ; ne relance pas `run_digits_experiment.py` si tu souhaites seulement analyser les résultats existants. Pour une reproduction fraîche, sauvegarder les résultats originaux, puis supprimer seulement les fichiers actifs concernés avant de réexécuter, notamment `results/composition_chunks/*.json`, `results/composition_remplacement_neurones.csv`, `results/fidelite_sondes_par_neurone.csv`, `results/run_manifest.json` et les tableaux de synthèse recalculés. Ne pas supprimer `audit/superseded_composition_chunks_v1_1/` : il documente la divergence historique.

### Analyses secondaires exploratoires

Elles sont distinctes du plan primaire et postérieures à l'analyse confirmatoire. Pour les recalculer :

```bash
python src/run_equal_epoch_control.py
python src/run_ood_imitation.py
for target in 107 110 113 208 211 214 309 312 315; do
  python src/run_parameter_budget_chunk.py "$target"
done
```

`run_parameter_budget_chunk.py` saute les fichiers de chunk existants. Les résultats exploratoires correspondants sont déjà fournis dans `results/`.

## Définition précise des conditions

- **A — Sonde adaptative naturelle :** paramètres RBF ajustés sur la tâche par Adam.
- **B — Mécanisme d'adaptation partiellement appris :** même architecture RBF, avec quatre taux par groupe estimés par hypergradient sur des épisodes train/validation. Le schéma de gradient et l'architecture RBF restent préspécifiés ; ce n'est pas la découverte ex nihilo d'un optimiseur.
- **Contrôle fixe :** centres et largeurs fixes, lecture ajustable seulement. Il a moins de paramètres apprenables (17 au lieu de 65 en 2D ou 513 en 30D), donc la comparaison ne sépare pas parfaitement capacité et adaptation.
- **C1 — Imitation isolée :** régression des sorties d'un neurone cible à partir de couples entrée/sortie autorisés. La fonction de fitting n'accepte ni famille cible, ni graine cible, ni poids cible.
- **C2 — Composition :** sondes entraînées sur les activations cachées observées du MLP, puis remplacement de certaines unités. Le lecteur final original est conservé ; ce n'est pas un étudiant autonome.

## Résultat du complément réel multiclasse (dix classes)

Sur le benchmark `load_digits` complet (1 797 images manuscrites 8×8, dix classes), l'exactitude moyenne sur trois splits est : RBF adaptative 87,31 %, RBF à taux méta-appris 78,33 %, contrôle fixe 76,67 %, MLP de référence 96,76 %. A, B et le MLP ont chacun 1 210 paramètres entraînables ; le contrôle fixe en a 170. Le méta-apprentissage n'apporte donc pas un gain sur cette tâche et la RBF reste sous le MLP. En composition, le remplacement de 1/4/16 unités donne 96,11/95,74/86,57 % d'exactitude composée versus 96,76 % source. Ce résultat négatif est conservé.

## Résultat du supplément distinct 3-vs-8 (binaire, 64 dimensions)

Le supplément `rapport_supplement_cas_reel_digits.pdf` utilise 357 images 8×8 filtrées aux chiffres 3 et 8. Sur trois graines, exactitude moyenne : RBF fixe 91,20 % (17 paramètres), RBF adaptative A 95,37 %, mécanisme partiellement méta-appris B 96,76 %, MLP 99,07 % (A/B/MLP : 1 057 paramètres chacun). B ne dépasse donc pas le MLP. En composition, le MLP source obtient 98,15 % et le remplacement de 1/4/16 unités atteint 98,15/97,22/95,83 %, tandis que l'écart moyen absolu des logits augmente de 0,122 à 1,969. Le lecteur aval source est conservé et chaque sonde possède 529 paramètres contre 65 pour l'unité remplacée : ce n'est pas une reconstruction autonome ni une comparaison à budget égal. L'incident de sérialisation du premier passage et l'identité octet-par-octet des CSV après correction sont consignés dans l'audit.

## Règle rouge : ce que l'audit prouve et ne prouve pas

Les fonctions d'entraînement ne reçoivent pas les labels de test ni les paramètres internes de la cible imitée. Les splits sont enregistrés et audités par hachage de lignes ; les prédictions de test sont exportées après gel. La relance de la classification et de l'imitation a reproduit les artefacts comparés octet par octet ; un lot de composition v1.2 (deux lunes, graine 411) a également été relancé et son JSON reproduit octet par octet.

Cela ne prouve ni une sécurité d'exécution adversariale, ni une équivalence mathématique, ni une généralisation universelle. Le jeu de cancer du sein est un benchmark public, pas une validation clinique. Les intervalles de confiance sont descriptifs et reposent sur peu de graines/cibles.

## Licences et données

Les deux benchmarks réels sont fournis et chargés via l’API scikit-learn : `load_breast_cancer` et `load_digits`. Aucun modèle externe ou dossier médical n'est utilisé. Les documents sources originaux sont inclus à des fins de traçabilité.


## Vérification finale du prompt maître

- `conformite_prompt_maitre.md` et `conformite_prompt_maitre.json` donnent une matrice point par point avec preuves, statut et écarts constatés. Le verdict est `PASS_WITH_LIMITATIONS` et non une validation absolue.
- `audit/audit_integrite_finale.json` rassemble les contrôles de distribution, fichiers, résultats, PDF et archive ; `audit/audit_integrite_digits_3_vs_8_finale.json` vérifie le supplément binaire existant sans relancer l'entraînement ni modifier les CSV.
- Le pipeline historique n'a pas archivé de checkpoints de poids entraînés. Les scripts, versions de dépendances, graines, partitions hachées, prédictions gelées, métriques et rapports sont fournis pour reproduction par réexécution. Aucun checkpoint manquant n'est reconstruit artificiellement.


## Réplication indépendante v1.2 (isolation stricte)

La campagne historique ci-dessus est conservée telle quelle. Une réplication v1.2, avec de nouvelles graines, des répertoires privés par appel et séparation des rôles système, est documentée dans `protocole_isolation_stricte_v1_2.md`. Ses résultats sont conservés séparément dans les fichiers `results/strict_isolation_*_v1_2*.csv`; l'audit de classification, d'imitation et de composition est disponible sous `audit/strict_isolation_*_v1_2_audit.json`.

Le rapport consolidé actualisé est `rapport_experience_sondes_adaptatives_final_v1_2.pdf` et sa source est le `.tex` de même nom. Cette annexe v1.2 ne mélange pas les observations avec celles de la première campagne. Le rejeu de l'inférence gelée a reproduit les 18 fichiers JSON de sortie octet pour octet (`audit/strict_isolation_v1_2_inference_replay.json`). Statut global : `PASS_WITH_LIMITATIONS`, non une garantie absolue d'absence de fuite.

**Point de formalisation à conserver :** `full_0` définit abstraitement une sonde comme opérateur d'observation. La RBF est l'instanciation fonctionnelle déclarée dans `formalisme_sonde_adaptative.tex`; elle n'est pas une architecture imposée directement par le texte source. L'adaptation et le méta-apprentissage sont des extensions expérimentales explicites.


## Rapport consolidé et réplication stricte v1.2

Le rapport de livraison à consulter en premier est `rapport_experience_sondes_adaptatives_final_v1_2.pdf` (source `rapport_experience_sondes_adaptatives_final_v1_2.tex`). Il consolide l'analyse initiale et ajoute une section de réplication indépendante v1.2 sans agréger les graines/protocoles. La formalisation source-to-code est explicitée dans le rapport : `full_0` définit une sonde abstraite comme opérateur d'observation ; la RBF apprenante est une instanciation opérationnelle ajoutée et documentée, pas une architecture imposée par le document source.

Les résultats stricts sont dans `results/strict_isolation_*_v1_2*.csv`; les intervalles descriptifs sont dans les tables `*_ci95_v1_2.csv`. Les comptes et contrôles de la livraison sont enregistrés dans `audit/audit_integrite_livraison_finale_v1_2.json`; la matrice point par point du prompt est dans `conformite_prompt_maitre_v1_2_finale.md` et `.json`. Le PDF final a été rendu sur 17 pages et visuellement contrôlé ; la trace est dans `audit/pdf_visual_review_v1_2_final.md`.

Pour contrôler les fichiers présents sans relancer l'entraînement :

```bash
python src/validate_delivery_v1_2.py
```

Pour reproduire la réplication strictement isolée dans un environnement Linux compatible et avec les permissions administratives nécessaires à la séparation des rôles (prévoir un espace temporaire neuf), les étapes sont `setup`, `classification`, `imitation`, `composition`. Les résultats de cette livraison proviennent des artefacts existants ; ces commandes ne doivent pas être lancées si l'objectif est seulement de vérifier/analyser ces résultats. Après une exécution fraîche, lancer le validateur.

```bash
python src/run_strict_isolated_replication_v1_2.py setup
python src/run_strict_isolated_replication_v1_2.py classification
python src/run_strict_isolated_replication_v1_2.py imitation
python src/run_strict_isolated_replication_v1_2.py composition
python src/validate_delivery_v1_2.py
python src/package_delivery_v1_2.py
```

L'archive livrée dans le dossier parent est `experience_NGeGenBrain_sondes_adaptatives_bundle_final_v1_2.zip`. Le manifeste interne énumère les SHA-256 de tous les fichiers packagés, sauf lui-même ; `manifest_delivery_NGeGenBrain_sondes_adaptatives_final_v1_2.json` et le fichier `.sha256` externes donnent les empreintes de l'archive et du manifeste.


===== sonde_adapt_1_bundle/adaptive_v1_2/frozen_bundle_original/experience_NGeGenBrain_sondes_adaptatives/README.md =====
# NGeGenBrain — expérience sur les sondes adaptatives et les neurones

## Objet

Ce dépôt est une expérience exécutée pour examiner, de manière circonscrite, si une sonde RBF adaptative peut (A) apprendre une tâche, (B) apprendre une partie de sa règle d'adaptation, (C1) imiter le comportement entrée-sortie de neurones artificiels simples observés en boîte noire et (C2) remplacer des unités cachées dans une composition de réseau.

Le travail part des deux références originales conservées dans `references/` :
- `NGeGenBrain_observation_formalisme_full_0.tex`
- `rapport_experience_sondes_adaptatives.tex`

La théorie de départ définit une sonde comme un opérateur d'observation spécifié et contrôlé ; elle ne définit pas déjà toute sonde comme un réseau qui apprend. L'adaptation est une extension expérimentale explicitement ajoutée dans `formalisme_sonde_adaptative.tex`. Un complément réel multiclasse sur les chiffres manuscrits a été ajouté séparément avec le protocole gelé `protocole_cas_reel_multiclasse_v1.md`.

## Résultats importants en une page

- Le noyau confirmatoire comprend quatre tâches : `two_moons`, `circles`, `xor_product` et le jeu public Wisconsin Diagnostic Breast Cancer. Un complément distinct préenregistré utilise aussi le jeu `load_digits` à dix classes (1 797 images, graines 1428/2539/3640). Un second supplément séparé filtre ce même jeu à la tâche binaire 3-vs-8 (357 images, 64 pixels, graines 714/825/936), avec son propre protocole et son propre audit.
- Les méthodes comprennent une RBF adaptative A, une RBF à taux par groupe méta-appris B, un contrôle RBF fixe et un MLP à 16 unités tanh.
- L'imitation isolée couvre 9 neurones cibles affines+activation (3 tanh, 3 ReLU, 3 sigmoïdes), 3 budgets (64, 256, 1024 paires entrée-sortie) et 3 initialisations indépendantes de sonde : 81 ajustements. Les sorties de test sont réservées à l'évaluateur.
- La composition remplace 1, 4 ou 16 unités cachées dans deux tâches. L'ancienne exécution de composition v1.1 utilisait par erreur les graines de classification 714/825/936 au lieu des graines de composition prescrites 411/522/633. Elle est préservée dans `audit/superseded_composition_chunks_v1_1/` et **exclue** des synthèses finales. La composition a été relancée avec les graines prévues, selon le correctif v1.2 haché avant la relance.
- L'audit indique `PASS_WITH_LIMITATIONS`. Les hachages de lignes des partitions sont disjoints ; les interfaces d'entraînement ne reçoivent pas les labels de test ni les paramètres des neurones imités. L'orchestration n'est cependant pas un bac à sable OS hostile : l'audit ne prouve pas l'impossibilité de tous les canaux cachés.

## Fichiers principaux

- `rapport_experience_sondes_adaptatives_complet.pdf` : rapport scientifique principal.
- `rapport_experience_sondes_adaptatives_complet.tex` : source LaTeX du rapport.
- `rapport_supplement_cas_reel_digits.pdf` / `.tex` : rapport dédié au supplément binaire 3-vs-8.
- `formalisme_sonde_adaptative.pdf` et `.tex` : formalisation mathématique de l'extension expérimentale.
- `protocole_preregistere.md` : protocole v1.1 pour classification/imitation et intentions de composition.
- `protocole_preregistere_composition_v1_2.md` : correctif versionné de la composition, révélant explicitement la divergence de graines et gelé avant sa relance.
- `protocole_cas_reel_multiclasse_v1.md` : complément préenregistré sur le benchmark réel dix classes.
- `protocole_supplement_digits_v1_0.md` et `protocole_supplement_digits_v1_0_1.md` : protocole déjà exécuté pour 3-vs-8 et correctif du sérialiseur d’audit uniquement.
- `rapport_supplement_cas_reel_digits.pdf/.tex` : rapport autonome du supplément binaire déjà exécuté.
- `protocole_supplement_digits_v1_0.md` et `protocole_supplement_digits_v1_0_1.md` : supplément indépendant 3-vs-8 et correction administrative du sérialiseur.
- `src/` : scripts d'entraînement, d'imitation, de composition, d'audit et de construction de rapport.
- `results/` : résultats par graine, prédictions après gel, tableaux de synthèse, fidélité des activations et résultats de composition.
- `figures/` : graphiques générés par le pipeline.
- `audit/` : gel pré-exécution, empreintes, audits d'intégrité (principal et chiffres), registre des partitions, replay déterministe et anciennes sorties de composition supersédées.
- `manifest_checksums.json` : SHA-256 des fichiers du bundle, hors manifeste lui-même et fichiers intermédiaires de compilation. `audit/audit_integrite_finale.json` agrège les contrôles finaux ; `audit/audit_integrite_digits_3_vs_8_finale.json` valide les résultats binaires déjà produits sans réentraîner les modèles ni modifier les CSV.
- `experience_NGeGenBrain_sondes_adaptatives_bundle.zip` (archive créée à la finalisation, dans le dossier parent) et `checksums_experience_NGeGenBrain_sondes_adaptatives.sha256` (SHA-256 de l’archive).

## Reproduction dans un environnement Python compatible

Versions mesurées lors de cette exécution : Python 3.13 (ou compatible), PyTorch 2.10.0+cpu, NumPy 2.3.5, pandas 2.2.3, scikit-learn 1.8.0, SciPy 1.17.0 et Matplotlib 3.10.8. Les dépendances principales figurent dans `requirements.txt`.

Depuis la racine du dépôt :

```bash
python -m pip install -r requirements.txt
python src/run_classification_stage.py
python src/run_imitation_stage.py
for seed in 411 522 633; do
  python src/run_composition_chunk.py two_moons "$seed"
  python src/run_composition_chunk.py breast_cancer "$seed"
done
python src/finalize_and_audit.py
python src/build_report.py
pdflatex -interaction=nonstopmode rapport_experience_sondes_adaptatives_complet.tex
pdflatex -interaction=nonstopmode rapport_experience_sondes_adaptatives_complet.tex
pdflatex -interaction=nonstopmode formalisme_sonde_adaptative.tex
pdflatex -interaction=nonstopmode rapport_supplement_cas_reel_digits.tex
pdflatex -interaction=nonstopmode rapport_supplement_cas_reel_digits.tex

# Supplément distinct chiffres 3-vs-8 (exécution déjà enregistrée dans les CSV)
python src/run_digits_real_supplement.py

# Complément réel multiclasse (si on veut recalculer les chiffres manuscrits)
python src/run_digits_experiment.py
# Si cette commande atteint une limite de durée après la classification,
# la classification a été sauvegardée avant la composition ; exécuter alors :
python src/run_digits_composition_only.py
python src/build_digits_figures.py
python src/insert_digits_section.py
python src/finalize_delivery.py
```

Les scripts de composition ignorent un chunk déjà présent. Les CSV finaux de chiffres manuscrits ont été contrôlés séparément ; ne relance pas `run_digits_experiment.py` si tu souhaites seulement analyser les résultats existants. Pour une reproduction fraîche, sauvegarder les résultats originaux, puis supprimer seulement les fichiers actifs concernés avant de réexécuter, notamment `results/composition_chunks/*.json`, `results/composition_remplacement_neurones.csv`, `results/fidelite_sondes_par_neurone.csv`, `results/run_manifest.json` et les tableaux de synthèse recalculés. Ne pas supprimer `audit/superseded_composition_chunks_v1_1/` : il documente la divergence historique.

### Analyses secondaires exploratoires

Elles sont distinctes du plan primaire et postérieures à l'analyse confirmatoire. Pour les recalculer :

```bash
python src/run_equal_epoch_control.py
python src/run_ood_imitation.py
for target in 107 110 113 208 211 214 309 312 315; do
  python src/run_parameter_budget_chunk.py "$target"
done
```

`run_parameter_budget_chunk.py` saute les fichiers de chunk existants. Les résultats exploratoires correspondants sont déjà fournis dans `results/`.

## Définition précise des conditions

- **A — Sonde adaptative naturelle :** paramètres RBF ajustés sur la tâche par Adam.
- **B — Mécanisme d'adaptation partiellement appris :** même architecture RBF, avec quatre taux par groupe estimés par hypergradient sur des épisodes train/validation. Le schéma de gradient et l'architecture RBF restent préspécifiés ; ce n'est pas la découverte ex nihilo d'un optimiseur.
- **Contrôle fixe :** centres et largeurs fixes, lecture ajustable seulement. Il a moins de paramètres apprenables (17 au lieu de 65 en 2D ou 513 en 30D), donc la comparaison ne sépare pas parfaitement capacité et adaptation.
- **C1 — Imitation isolée :** régression des sorties d'un neurone cible à partir de couples entrée/sortie autorisés. La fonction de fitting n'accepte ni famille cible, ni graine cible, ni poids cible.
- **C2 — Composition :** sondes entraînées sur les activations cachées observées du MLP, puis remplacement de certaines unités. Le lecteur final original est conservé ; ce n'est pas un étudiant autonome.

## Résultat du complément réel multiclasse (dix classes)

Sur le benchmark `load_digits` complet (1 797 images manuscrites 8×8, dix classes), l'exactitude moyenne sur trois splits est : RBF adaptative 87,31 %, RBF à taux méta-appris 78,33 %, contrôle fixe 76,67 %, MLP de référence 96,76 %. A, B et le MLP ont chacun 1 210 paramètres entraînables ; le contrôle fixe en a 170. Le méta-apprentissage n'apporte donc pas un gain sur cette tâche et la RBF reste sous le MLP. En composition, le remplacement de 1/4/16 unités donne 96,11/95,74/86,57 % d'exactitude composée versus 96,76 % source. Ce résultat négatif est conservé.

## Résultat du supplément distinct 3-vs-8 (binaire, 64 dimensions)

Le supplément `rapport_supplement_cas_reel_digits.pdf` utilise 357 images 8×8 filtrées aux chiffres 3 et 8. Sur trois graines, exactitude moyenne : RBF fixe 91,20 % (17 paramètres), RBF adaptative A 95,37 %, mécanisme partiellement méta-appris B 96,76 %, MLP 99,07 % (A/B/MLP : 1 057 paramètres chacun). B ne dépasse donc pas le MLP. En composition, le MLP source obtient 98,15 % et le remplacement de 1/4/16 unités atteint 98,15/97,22/95,83 %, tandis que l'écart moyen absolu des logits augmente de 0,122 à 1,969. Le lecteur aval source est conservé et chaque sonde possède 529 paramètres contre 65 pour l'unité remplacée : ce n'est pas une reconstruction autonome ni une comparaison à budget égal. L'incident de sérialisation du premier passage et l'identité octet-par-octet des CSV après correction sont consignés dans l'audit.

## Règle rouge : ce que l'audit prouve et ne prouve pas

Les fonctions d'entraînement ne reçoivent pas les labels de test ni les paramètres internes de la cible imitée. Les splits sont enregistrés et audités par hachage de lignes ; les prédictions de test sont exportées après gel. La relance de la classification et de l'imitation a reproduit les artefacts comparés octet par octet ; un lot de composition v1.2 (deux lunes, graine 411) a également été relancé et son JSON reproduit octet par octet.

Cela ne prouve ni une sécurité d'exécution adversariale, ni une équivalence mathématique, ni une généralisation universelle. Le jeu de cancer du sein est un benchmark public, pas une validation clinique. Les intervalles de confiance sont descriptifs et reposent sur peu de graines/cibles.

## Licences et données

Les deux benchmarks réels sont fournis et chargés via l’API scikit-learn : `load_breast_cancer` et `load_digits`. Aucun modèle externe ou dossier médical n'est utilisé. Les documents sources originaux sont inclus à des fins de traçabilité.


## Vérification finale du prompt maître

- `conformite_prompt_maitre.md` et `conformite_prompt_maitre.json` donnent une matrice point par point avec preuves, statut et écarts constatés. Le verdict est `PASS_WITH_LIMITATIONS` et non une validation absolue.
- `audit/audit_integrite_finale.json` rassemble les contrôles de distribution, fichiers, résultats, PDF et archive ; `audit/audit_integrite_digits_3_vs_8_finale.json` vérifie le supplément binaire existant sans relancer l'entraînement ni modifier les CSV.
- Le pipeline historique n'a pas archivé de checkpoints de poids entraînés. Les scripts, versions de dépendances, graines, partitions hachées, prédictions gelées, métriques et rapports sont fournis pour reproduction par réexécution. Aucun checkpoint manquant n'est reconstruit artificiellement.


## Réplication indépendante v1.2 (isolation stricte)

La campagne historique ci-dessus est conservée telle quelle. Une réplication v1.2, avec de nouvelles graines, des répertoires privés par appel et séparation des rôles système, est documentée dans `protocole_isolation_stricte_v1_2.md`. Ses résultats sont conservés séparément dans les fichiers `results/strict_isolation_*_v1_2*.csv`; l'audit de classification, d'imitation et de composition est disponible sous `audit/strict_isolation_*_v1_2_audit.json`.

Le rapport consolidé actualisé est `rapport_experience_sondes_adaptatives_final_v1_2.pdf` et sa source est le `.tex` de même nom. Cette annexe v1.2 ne mélange pas les observations avec celles de la première campagne. Le rejeu de l'inférence gelée a reproduit les 18 fichiers JSON de sortie octet pour octet (`audit/strict_isolation_v1_2_inference_replay.json`). Statut global : `PASS_WITH_LIMITATIONS`, non une garantie absolue d'absence de fuite.

**Point de formalisation à conserver :** `full_0` définit abstraitement une sonde comme opérateur d'observation. La RBF est l'instanciation fonctionnelle déclarée dans `formalisme_sonde_adaptative.tex`; elle n'est pas une architecture imposée directement par le texte source. L'adaptation et le méta-apprentissage sont des extensions expérimentales explicites.


## Rapport consolidé et réplication stricte v1.2

Le rapport de livraison à consulter en premier est `rapport_experience_sondes_adaptatives_final_v1_2.pdf` (source `rapport_experience_sondes_adaptatives_final_v1_2.tex`). Il consolide l'analyse initiale et ajoute une section de réplication indépendante v1.2 sans agréger les graines/protocoles. La formalisation source-to-code est explicitée dans le rapport : `full_0` définit une sonde abstraite comme opérateur d'observation ; la RBF apprenante est une instanciation opérationnelle ajoutée et documentée, pas une architecture imposée par le document source.

Les résultats stricts sont dans `results/strict_isolation_*_v1_2*.csv`; les intervalles descriptifs sont dans les tables `*_ci95_v1_2.csv`. Les comptes et contrôles de la livraison sont enregistrés dans `audit/audit_integrite_livraison_finale_v1_2.json`; la matrice point par point du prompt est dans `conformite_prompt_maitre_v1_2_finale.md` et `.json`. Le PDF final a été rendu sur 17 pages et visuellement contrôlé ; la trace est dans `audit/pdf_visual_review_v1_2_final.md`.

Pour contrôler les fichiers présents sans relancer l'entraînement :

```bash
python src/validate_delivery_v1_2.py
```

Pour reproduire la réplication strictement isolée dans un environnement Linux compatible et avec les permissions administratives nécessaires à la séparation des rôles (prévoir un espace temporaire neuf), les étapes sont `setup`, `classification`, `imitation`, `composition`. Les résultats de cette livraison proviennent des artefacts existants ; ces commandes ne doivent pas être lancées si l'objectif est seulement de vérifier/analyser ces résultats. Après une exécution fraîche, lancer le validateur.

```bash
python src/run_strict_isolated_replication_v1_2.py setup
python src/run_strict_isolated_replication_v1_2.py classification
python src/run_strict_isolated_replication_v1_2.py imitation
python src/run_strict_isolated_replication_v1_2.py composition
python src/validate_delivery_v1_2.py
python src/package_delivery_v1_2.py
```

L'archive livrée dans le dossier parent est `experience_NGeGenBrain_sondes_adaptatives_bundle_final_v1_2.zip`. Le manifeste interne énumère les SHA-256 de tous les fichiers packagés, sauf lui-même ; `manifest_delivery_NGeGenBrain_sondes_adaptatives_final_v1_2.json` et le fichier `.sha256` externes donnent les empreintes de l'archive et du manifeste.


===== sonde_adapt_1_bundle/adaptive_v1_2/full_bundle/README.md =====
# NGeGenBrain — expérience sur les sondes adaptatives et les neurones

## Objet

Ce dépôt est une expérience exécutée pour examiner, de manière circonscrite, si une sonde RBF adaptative peut (A) apprendre une tâche, (B) apprendre une partie de sa règle d'adaptation, (C1) imiter le comportement entrée-sortie de neurones artificiels simples observés en boîte noire et (C2) remplacer des unités cachées dans une composition de réseau.

Le travail part des deux références originales conservées dans `references/` :
- `NGeGenBrain_observation_formalisme_full_0.tex`
- `rapport_experience_sondes_adaptatives.tex`

La théorie de départ définit une sonde comme un opérateur d'observation spécifié et contrôlé ; elle ne définit pas déjà toute sonde comme un réseau qui apprend. L'adaptation est une extension expérimentale explicitement ajoutée dans `formalisme_sonde_adaptative.tex`. Un complément réel multiclasse sur les chiffres manuscrits a été ajouté séparément avec le protocole gelé `protocole_cas_reel_multiclasse_v1.md`.

## Résultats importants en une page

- Le noyau confirmatoire comprend quatre tâches : `two_moons`, `circles`, `xor_product` et le jeu public Wisconsin Diagnostic Breast Cancer. Un complément distinct préenregistré utilise aussi le jeu `load_digits` à dix classes (1 797 images, graines 1428/2539/3640). Un second supplément séparé filtre ce même jeu à la tâche binaire 3-vs-8 (357 images, 64 pixels, graines 714/825/936), avec son propre protocole et son propre audit.
- Les méthodes comprennent une RBF adaptative A, une RBF à taux par groupe méta-appris B, un contrôle RBF fixe et un MLP à 16 unités tanh.
- L'imitation isolée couvre 9 neurones cibles affines+activation (3 tanh, 3 ReLU, 3 sigmoïdes), 3 budgets (64, 256, 1024 paires entrée-sortie) et 3 initialisations indépendantes de sonde : 81 ajustements. Les sorties de test sont réservées à l'évaluateur.
- La composition remplace 1, 4 ou 16 unités cachées dans deux tâches. L'ancienne exécution de composition v1.1 utilisait par erreur les graines de classification 714/825/936 au lieu des graines de composition prescrites 411/522/633. Elle est préservée dans `audit/superseded_composition_chunks_v1_1/` et **exclue** des synthèses finales. La composition a été relancée avec les graines prévues, selon le correctif v1.2 haché avant la relance.
- L'audit indique `PASS_WITH_LIMITATIONS`. Les hachages de lignes des partitions sont disjoints ; les interfaces d'entraînement ne reçoivent pas les labels de test ni les paramètres des neurones imités. L'orchestration n'est cependant pas un bac à sable OS hostile : l'audit ne prouve pas l'impossibilité de tous les canaux cachés.

## Fichiers principaux

- `rapport_experience_sondes_adaptatives_complet.pdf` : rapport scientifique principal.
- `rapport_experience_sondes_adaptatives_complet.tex` : source LaTeX du rapport.
- `rapport_supplement_cas_reel_digits.pdf` / `.tex` : rapport dédié au supplément binaire 3-vs-8.
- `formalisme_sonde_adaptative.pdf` et `.tex` : formalisation mathématique de l'extension expérimentale.
- `protocole_preregistere.md` : protocole v1.1 pour classification/imitation et intentions de composition.
- `protocole_preregistere_composition_v1_2.md` : correctif versionné de la composition, révélant explicitement la divergence de graines et gelé avant sa relance.
- `protocole_cas_reel_multiclasse_v1.md` : complément préenregistré sur le benchmark réel dix classes.
- `protocole_supplement_digits_v1_0.md` et `protocole_supplement_digits_v1_0_1.md` : protocole déjà exécuté pour 3-vs-8 et correctif du sérialiseur d’audit uniquement.
- `rapport_supplement_cas_reel_digits.pdf/.tex` : rapport autonome du supplément binaire déjà exécuté.
- `protocole_supplement_digits_v1_0.md` et `protocole_supplement_digits_v1_0_1.md` : supplément indépendant 3-vs-8 et correction administrative du sérialiseur.
- `src/` : scripts d'entraînement, d'imitation, de composition, d'audit et de construction de rapport.
- `results/` : résultats par graine, prédictions après gel, tableaux de synthèse, fidélité des activations et résultats de composition.
- `figures/` : graphiques générés par le pipeline.
- `audit/` : gel pré-exécution, empreintes, audits d'intégrité (principal et chiffres), registre des partitions, replay déterministe et anciennes sorties de composition supersédées.
- `manifest_checksums.json` : SHA-256 des fichiers du bundle, hors manifeste lui-même et fichiers intermédiaires de compilation. `audit/audit_integrite_finale.json` agrège les contrôles finaux ; `audit/audit_integrite_digits_3_vs_8_finale.json` valide les résultats binaires déjà produits sans réentraîner les modèles ni modifier les CSV.
- `experience_NGeGenBrain_sondes_adaptatives_bundle.zip` (archive créée à la finalisation, dans le dossier parent) et `checksums_experience_NGeGenBrain_sondes_adaptatives.sha256` (SHA-256 de l’archive).

## Reproduction dans un environnement Python compatible

Versions mesurées lors de cette exécution : Python 3.13 (ou compatible), PyTorch 2.10.0+cpu, NumPy 2.3.5, pandas 2.2.3, scikit-learn 1.8.0, SciPy 1.17.0 et Matplotlib 3.10.8. Les dépendances principales figurent dans `requirements.txt`.

Depuis la racine du dépôt :

```bash
python -m pip install -r requirements.txt
python src/run_classification_stage.py
python src/run_imitation_stage.py
for seed in 411 522 633; do
  python src/run_composition_chunk.py two_moons "$seed"
  python src/run_composition_chunk.py breast_cancer "$seed"
done
python src/finalize_and_audit.py
python src/build_report.py
pdflatex -interaction=nonstopmode rapport_experience_sondes_adaptatives_complet.tex
pdflatex -interaction=nonstopmode rapport_experience_sondes_adaptatives_complet.tex
pdflatex -interaction=nonstopmode formalisme_sonde_adaptative.tex
pdflatex -interaction=nonstopmode rapport_supplement_cas_reel_digits.tex
pdflatex -interaction=nonstopmode rapport_supplement_cas_reel_digits.tex

# Supplément distinct chiffres 3-vs-8 (exécution déjà enregistrée dans les CSV)
python src/run_digits_real_supplement.py

# Complément réel multiclasse (si on veut recalculer les chiffres manuscrits)
python src/run_digits_experiment.py
# Si cette commande atteint une limite de durée après la classification,
# la classification a été sauvegardée avant la composition ; exécuter alors :
python src/run_digits_composition_only.py
python src/build_digits_figures.py
python src/insert_digits_section.py
python src/finalize_delivery.py
```

Les scripts de composition ignorent un chunk déjà présent. Les CSV finaux de chiffres manuscrits ont été contrôlés séparément ; ne relance pas `run_digits_experiment.py` si tu souhaites seulement analyser les résultats existants. Pour une reproduction fraîche, sauvegarder les résultats originaux, puis supprimer seulement les fichiers actifs concernés avant de réexécuter, notamment `results/composition_chunks/*.json`, `results/composition_remplacement_neurones.csv`, `results/fidelite_sondes_par_neurone.csv`, `results/run_manifest.json` et les tableaux de synthèse recalculés. Ne pas supprimer `audit/superseded_composition_chunks_v1_1/` : il documente la divergence historique.

### Analyses secondaires exploratoires

Elles sont distinctes du plan primaire et postérieures à l'analyse confirmatoire. Pour les recalculer :

```bash
python src/run_equal_epoch_control.py
python src/run_ood_imitation.py
for target in 107 110 113 208 211 214 309 312 315; do
  python src/run_parameter_budget_chunk.py "$target"
done
```

`run_parameter_budget_chunk.py` saute les fichiers de chunk existants. Les résultats exploratoires correspondants sont déjà fournis dans `results/`.

## Définition précise des conditions

- **A — Sonde adaptative naturelle :** paramètres RBF ajustés sur la tâche par Adam.
- **B — Mécanisme d'adaptation partiellement appris :** même architecture RBF, avec quatre taux par groupe estimés par hypergradient sur des épisodes train/validation. Le schéma de gradient et l'architecture RBF restent préspécifiés ; ce n'est pas la découverte ex nihilo d'un optimiseur.
- **Contrôle fixe :** centres et largeurs fixes, lecture ajustable seulement. Il a moins de paramètres apprenables (17 au lieu de 65 en 2D ou 513 en 30D), donc la comparaison ne sépare pas parfaitement capacité et adaptation.
- **C1 — Imitation isolée :** régression des sorties d'un neurone cible à partir de couples entrée/sortie autorisés. La fonction de fitting n'accepte ni famille cible, ni graine cible, ni poids cible.
- **C2 — Composition :** sondes entraînées sur les activations cachées observées du MLP, puis remplacement de certaines unités. Le lecteur final original est conservé ; ce n'est pas un étudiant autonome.

## Résultat du complément réel multiclasse (dix classes)

Sur le benchmark `load_digits` complet (1 797 images manuscrites 8×8, dix classes), l'exactitude moyenne sur trois splits est : RBF adaptative 87,31 %, RBF à taux méta-appris 78,33 %, contrôle fixe 76,67 %, MLP de référence 96,76 %. A, B et le MLP ont chacun 1 210 paramètres entraînables ; le contrôle fixe en a 170. Le méta-apprentissage n'apporte donc pas un gain sur cette tâche et la RBF reste sous le MLP. En composition, le remplacement de 1/4/16 unités donne 96,11/95,74/86,57 % d'exactitude composée versus 96,76 % source. Ce résultat négatif est conservé.

## Résultat du supplément distinct 3-vs-8 (binaire, 64 dimensions)

Le supplément `rapport_supplement_cas_reel_digits.pdf` utilise 357 images 8×8 filtrées aux chiffres 3 et 8. Sur trois graines, exactitude moyenne : RBF fixe 91,20 % (17 paramètres), RBF adaptative A 95,37 %, mécanisme partiellement méta-appris B 96,76 %, MLP 99,07 % (A/B/MLP : 1 057 paramètres chacun). B ne dépasse donc pas le MLP. En composition, le MLP source obtient 98,15 % et le remplacement de 1/4/16 unités atteint 98,15/97,22/95,83 %, tandis que l'écart moyen absolu des logits augmente de 0,122 à 1,969. Le lecteur aval source est conservé et chaque sonde possède 529 paramètres contre 65 pour l'unité remplacée : ce n'est pas une reconstruction autonome ni une comparaison à budget égal. L'incident de sérialisation du premier passage et l'identité octet-par-octet des CSV après correction sont consignés dans l'audit.

## Règle rouge : ce que l'audit prouve et ne prouve pas

Les fonctions d'entraînement ne reçoivent pas les labels de test ni les paramètres internes de la cible imitée. Les splits sont enregistrés et audités par hachage de lignes ; les prédictions de test sont exportées après gel. La relance de la classification et de l'imitation a reproduit les artefacts comparés octet par octet ; un lot de composition v1.2 (deux lunes, graine 411) a également été relancé et son JSON reproduit octet par octet.

Cela ne prouve ni une sécurité d'exécution adversariale, ni une équivalence mathématique, ni une généralisation universelle. Le jeu de cancer du sein est un benchmark public, pas une validation clinique. Les intervalles de confiance sont descriptifs et reposent sur peu de graines/cibles.

## Licences et données

Les deux benchmarks réels sont fournis et chargés via l’API scikit-learn : `load_breast_cancer` et `load_digits`. Aucun modèle externe ou dossier médical n'est utilisé. Les documents sources originaux sont inclus à des fins de traçabilité.


## Vérification finale du prompt maître

- `conformite_prompt_maitre.md` et `conformite_prompt_maitre.json` donnent une matrice point par point avec preuves, statut et écarts constatés. Le verdict est `PASS_WITH_LIMITATIONS` et non une validation absolue.
- `audit/audit_integrite_finale.json` rassemble les contrôles de distribution, fichiers, résultats, PDF et archive ; `audit/audit_integrite_digits_3_vs_8_finale.json` vérifie le supplément binaire existant sans relancer l'entraînement ni modifier les CSV.
- Le pipeline historique n'a pas archivé de checkpoints de poids entraînés. Les scripts, versions de dépendances, graines, partitions hachées, prédictions gelées, métriques et rapports sont fournis pour reproduction par réexécution. Aucun checkpoint manquant n'est reconstruit artificiellement.


## Réplication indépendante v1.2 (isolation stricte)

La campagne historique ci-dessus est conservée telle quelle. Une réplication v1.2, avec de nouvelles graines, des répertoires privés par appel et séparation des rôles système, est documentée dans `protocole_isolation_stricte_v1_2.md`. Ses résultats sont conservés séparément dans les fichiers `results/strict_isolation_*_v1_2*.csv`; l'audit de classification, d'imitation et de composition est disponible sous `audit/strict_isolation_*_v1_2_audit.json`.

Le rapport consolidé actualisé est `rapport_experience_sondes_adaptatives_final_v1_2.pdf` et sa source est le `.tex` de même nom. Cette annexe v1.2 ne mélange pas les observations avec celles de la première campagne. Le rejeu de l'inférence gelée a reproduit les 18 fichiers JSON de sortie octet pour octet (`audit/strict_isolation_v1_2_inference_replay.json`). Statut global : `PASS_WITH_LIMITATIONS`, non une garantie absolue d'absence de fuite.

**Point de formalisation à conserver :** `full_0` définit abstraitement une sonde comme opérateur d'observation. La RBF est l'instanciation fonctionnelle déclarée dans `formalisme_sonde_adaptative.tex`; elle n'est pas une architecture imposée directement par le texte source. L'adaptation et le méta-apprentissage sont des extensions expérimentales explicites.


## Rapport consolidé et réplication stricte v1.2

Le rapport de livraison à consulter en premier est `rapport_experience_sondes_adaptatives_final_v1_2.pdf` (source `rapport_experience_sondes_adaptatives_final_v1_2.tex`). Il consolide l'analyse initiale et ajoute une section de réplication indépendante v1.2 sans agréger les graines/protocoles. La formalisation source-to-code est explicitée dans le rapport : `full_0` définit une sonde abstraite comme opérateur d'observation ; la RBF apprenante est une instanciation opérationnelle ajoutée et documentée, pas une architecture imposée par le document source.

Les résultats stricts sont dans `results/strict_isolation_*_v1_2*.csv`; les intervalles descriptifs sont dans les tables `*_ci95_v1_2.csv`. Les comptes et contrôles de la livraison sont enregistrés dans `audit/audit_integrite_livraison_finale_v1_2.json`; la matrice point par point du prompt est dans `conformite_prompt_maitre_v1_2_finale.md` et `.json`. Le PDF final a été rendu sur 17 pages et visuellement contrôlé ; la trace est dans `audit/pdf_visual_review_v1_2_final.md`.

Pour contrôler les fichiers présents sans relancer l'entraînement :

```bash
python src/validate_delivery_v1_2.py
```

Pour reproduire la réplication strictement isolée dans un environnement Linux compatible et avec les permissions administratives nécessaires à la séparation des rôles (prévoir un espace temporaire neuf), les étapes sont `setup`, `classification`, `imitation`, `composition`. Les résultats de cette livraison proviennent des artefacts existants ; ces commandes ne doivent pas être lancées si l'objectif est seulement de vérifier/analyser ces résultats. Après une exécution fraîche, lancer le validateur.

```bash
python src/run_strict_isolated_replication_v1_2.py setup
python src/run_strict_isolated_replication_v1_2.py classification
python src/run_strict_isolated_replication_v1_2.py imitation
python src/run_strict_isolated_replication_v1_2.py composition
python src/validate_delivery_v1_2.py
python src/package_delivery_v1_2.py
```

L'archive livrée dans le dossier parent est `experience_NGeGenBrain_sondes_adaptatives_bundle_final_v1_2.zip`. Le manifeste interne énumère les SHA-256 de tous les fichiers packagés, sauf lui-même ; `manifest_delivery_NGeGenBrain_sondes_adaptatives_final_v1_2.json` et le fichier `.sha256` externes donnent les empreintes de l'archive et du manifeste.


===== sonde_adapt_1_bundle/ngbrain_v2/README.md =====
# NGeGenBrain_v2 — Laboratoire d'étude mécaniste et de reconstruction fonctionnelle

**Version de travail :** `2.0.0.dev0`  
**Date de constitution :** 2026-10-27  
**Langage principal :** Python 3.11+  
**Cœur :** bibliothèque standard Python ; PyTorch optionnel pour l'instrumentation neuronale.

NGeGenBrain_v2 conserve dans `legacy_NGeGenBrain_v1/` le dépôt source complet de la V1 et ajoute un laboratoire d'expérimentation pour modèles neuronaux instrumentables. La V2 est organisée autour d'adapters à capacités déclarées, d'observations sérialisables, d'interventions contrôlées, de registres chaînés par SHA-256, de la découverte de règles dans des classes d'hypothèses explicites, et de la composition/reconstruction de modèles symboliques exécutables.

## Démarrage rapide

```bash
python ngbrain.py init
python ngbrain.py status
python ngbrain.py inspect --model synthetic:parity4
python ngbrain.py observe --model synthetic:parity4 --input '[0,1,1,0]'
python ngbrain.py benchmark --bits 4 --seed 20261027 --max-samples 4096
python ngbrain.py synthetic-ladder --seed 20261027
python ngbrain.py reconstruct --source synthetic --seed 712 --vocab-size 5 --epochs 40 --max-new-tokens 8
python ngbrain.py audit
```

Pour lancer l'interface Web locale :

```bash
python ngbrain.py serve --host 127.0.0.1 --port 8766
```

Ouvrir `http://127.0.0.1:8766/`. Le serveur intégré refuse une écoute sur une adresse non-loopback.

Pour jouer une intervention causale sur le modèle synthétique (structure visible explicitement) :

```bash
python ngbrain.py experiment --model synthetic:parity4 --input '[1,0,0,0]' --target xor_layers.0.positive --mode zero
python ngbrain.py sweep --inputs-file examples/causal_sweep_inputs.json --target xor_layers.0.positive --mode zero
python ngbrain.py plan --inputs-file examples/causal_sweep_inputs.json --target xor_layers.0.positive
python ngbrain.py counterexamples --rows-file examples/discovery_validation_parity3.json --candidate-file examples/affine_candidate_parity3.json
```

## Adapter un LLM Hugging Face local

Le module `src/nggegenbrain_v2/adapters/huggingface.py` offre un adapter optionnel. Installer les extras puis pointer vers un modèle déjà présent localement :

```bash
pip install -e '.[huggingface]'
```

L'adapter est construit avec `trust_remote_code=False` et `local_files_only=True` par défaut. Les capacités sont déclarées explicitement. Le paquet `transformers` n'était pas installé dans l'environnement de validation présent, et l'accès réseau pour l'installer a échoué (résolution DNS indisponible) ; aucun checkpoint LLM externe n'était présent. Aucun LLM externe n'a donc été chargé ni testé dans cette livraison. Le contrat logiciel de l'adapter a été testé avec un faux modèle compatible au protocole (`tests/test_huggingface_adapter_mock.py`), ce qui ne remplace pas un test de checkpoint réel. Le mini-modèle causal synthétique est distinct d'un LLM pré-entraîné.

## Forme de l'architecture

- `adapters/base.py`: contrat du modèle et frontière de capacités.
- `adapters/torch_adapter.py`: capture d'activations par hooks temporaires, interventions scoped, hash de poids et génération autoregressive pour un module déclarant explicitement `is_causal_lm=True`.
- `adapters/huggingface.py`: adapter facultatif pour causal LM local.
- `adapters/synthetic.py`: huit terrains synthétiques progressifs, du réseau linéaire au mini Transformer causal de génération.
- `analysis/causal.py`: expériences appariées baseline/intervention et mesures de delta.
- `analysis/hypotheses.py`: cycle de vie des hypothèses, contre-preuves et historique.
- `discovery/rules.py`: induction GF(2) dans une classe formelle déclarée (parité/XOR booléen affine).
- `discovery/numeric.py`: recherche bottom-up d’expressions arithmétiques exécutables dans une grammaire déclarée, avec budget explicite et statut de troncature.
- `discovery/engine.py`: registre extensible de stratégies d’induction.
- `discovery/circuits.py`: graphe d'influences observées sous intervention, avec portée explicitement limitée.
- `composition.py`: langage déclaratif sûr et exécutable pour mécanismes composés, sans `eval`/`exec`.
- `reconstruction/engine.py`: reconstruction symbolique indépendante à partir de règles découvertes; `reconstruction/causal_lm.py` fournit la découverte d’une règle de prochain token dans une classe finie annoncée et la reconstruction par table de logits sur contextes explicitement interrogés. `reconstruction/synthetic_benchmark.py` entraîne un minuscule Transformer causal synthétique, le met derrière un adaptateur boîte noire et produit des modèles composés indépendants.
- `synthetic_lab.py`: benchmark aveugle avec séparation du répertoire d'analyse et de la vérité d'audit.
- `registry.py`: journal JSONL append-only chaîné par SHA-256, vérification et écriture atomique.
- `web.py`: API locale et interface de laboratoire.

## Échelle synthétique progressive

La commande `synthetic-ladder` exerce huit architectures reproductibles : réseau linéaire, réseau logique/parité, réseau d’interactions, réseau à représentations distribuées, chemins concurrents, réseau hiérarchique, mini-Transformer encodeur et mini-Transformer causal capable de générer des tokens. Le résultat d’exécution officiel se trouve dans `benchmarks/results/20261027_official/synthetic_ladder_results.json`. Cette échelle vérifie l’instrumentation, le comportement boîte noire/instrumentable et la capture/intervention; elle ne prétend pas que les mécanismes internes de ces architectures sont tous reconstruits.

## Échelle synthétique livrée

Le module `adapters/synthetic.py` expose huit niveaux instrumentables via `create_synthetic_level(level, black_box=...)` : (1) réseau linéaire, (2) circuit XOR, (3) interactions, (4) représentation distribuée, (5) voies concurrentes, (6) MLP hiérarchique, (7) mini-Transformer encodeur, (8) mini-Transformer causal génératif. Le protocole `run_synthetic_ladder_smoke()` exécute les huit modèles, enregistre les empreintes, vérifie les captures/interventions et teste la génération du niveau causal. Ces tests valident les adapters, pas la reconstruction mécaniste de chaque architecture.

## Reconstruction d’un modèle causal génératif

La commande `reconstruct --source synthetic` entraîne un petit Transformer causal sur une grammaire synthétique, puis ne fournit à la méthode de découverte qu’un adaptateur de requête sans inspection, capture d’activations ni exposition de paramètres. Le protocole exécute deux chemins indépendants : (1) ajuste une règle modulaire de prochain token dans une classe déclarée, en séparant strictement contextes d’entraînement et holdout ; (2) construit une table autonome des logits pour les contextes expressément interrogés. Les deux artefacts composés exécutent leur propre boucle autoregressive et ne consultent pas la source lors de l’inférence.

```bash
python ngbrain.py --workspace ./workspace_lm reconstruct --source synthetic --seed 712 --vocab-size 5 --epochs 40 --max-new-tokens 8
```

Sorties principales : `public_summary.json`, `rule_reconstruction.json`, `composed_rule_model.json`, `finite_context_lookup_reconstruction.json`, `composed_lookup_model.json` et `auditor_only/hidden_ground_truth.json`. Le dernier fichier est réservé à l’auditeur du benchmark et ne doit pas être transmis au moteur de découverte. Les valeurs du rapport officiel donnent la portée exacte du test effectivement exécuté. Ce cas démontre uniquement une reconstruction comportementale sur un Transformer synthétique minuscule et la classe/domaine précisés ; il ne vaut pas reconstruction interne d’un LLM pré-entraîné de taille réelle.

Un LLM Hugging Face local peut être chargé en mode local-only avec `reconstruct --source huggingface-local --model-path ... --mode lookup|rule|both --contexts-file ... --prompts-file ...`. Le mode `lookup` accepte une liste de contextes token-ID explicitement interrogés. Les modes `rule` et `both` exigent un objet JSON avec des champs séparés `training_contexts` et `validation_contexts` (disjoints) ; `both` exige aussi `lookup_contexts`. Le mode règle utilise par défaut `small_coefficient_modular_affine_v1`, qui examine une classe explicitement restreinte de coefficients `{−1,0,1}` modulo le vocabulaire. Le mode Python `auto` utilise l'énumération exacte `modular_affine_next_token_v1` pour vocabulaire ≤32, et la classe à coefficients réduits au-delà, pour ne pas lancer une recherche cubique déraisonnable. Cette classe réduite est plus scalable, mais n'est pas une recherche universelle de toutes les règles. Les contextes de validation ne sélectionnent jamais la règle. Il faut une couverture suffisante des contextes rencontrés pendant la génération en mode lookup ; un contexte absent n’est pas complété par des logits inventés. Le test avec un vrai checkpoint exige le paquet `transformers` et le checkpoint local ; l’adapter est testé par contrat logiciel séparément.

## Benchmark synthétique livré

Le benchmark `SYNTH-PARITY-n` interroge un petit réseau ReLU déterministe par entrées binaires. L'analyseur ne voit qu'un adapter de requête : il ne voit ni poids, ni couches, ni mécanismes internes. Un sous-ensemble de lignes sert à découvrir une règle candidate ; les autres lignes sont réservées à la validation. L'auditeur conserve séparément la description de construction du benchmark dans `auditor_only/hidden_ground_truth.json`.

Pour `n=4`, le benchmark a découvert une règle XOR des quatre variables, obtenu une exactitude `1.0` sur le holdout de 4 lignes et `1.0` sur la table binaire complète interrogée. C'est une preuve d'exécution utile pour un problème booléen borné et la classe d'hypothèses déclarée. **Ce n'est ni une reconstruction de poids, ni une preuve d'équivalence mécaniste, ni une reconstruction de LLM.**

## Tests

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
python ngbrain.py benchmark --bits 4 --seed 20261027 --max-samples 4096
python ngbrain.py synthetic-ladder --seed 20261027
python ngbrain.py reconstruct --source synthetic --seed 712 --vocab-size 5 --epochs 40 --max-new-tokens 8
python ngbrain.py audit
python ngbrain.py legacy-test
```

Le dépôt V1 est gardé et les tests d'origine s'exécutent à partir de cette copie. Les reçus dans `audit/` donnent les commandes et les résultats réellement observés.

## Environnement et ressources

Le code cœur V2 n'exige aucun paquet tiers. Les adapters PyTorch exigent `torch`; l'adapter Hugging Face exige en plus `transformers`. Les LLM ne sont pas téléchargés automatiquement. Un modèle ouvert particulier n'est pas inclus dans les archives et les expériences sur un LLM externe doivent être lancées sur une machine qui a accès à ce modèle et aux ressources nécessaires.

## Vérification de la version de travail

Le reçu source courant (`audit/validation_receipt.json`) enregistre le résultat du dernier passage de validation ; les comptes finaux exacts sont dans `audit/validation_summary.md` et les journaux bruts `audit/test_runs/`, la compilation Python, la compilation LaTeX, les commandes CLI intégrées, la syntaxe de tous les JSON recensés et les CRC des trois ZIP de référence. L'attestation clean-room de l'archive livrée est distincte et se trouve dans le bundle d'audit/suivi après création de l'archive.

## Terminologie de statut

- **implémenté** : module et contrat présents dans le dépôt.
- **testé** : commande et résultat présents dans un reçu.
- **validé dans un domaine** : résultats hors-échantillon vérifiés dans le domaine nommé.
- **non exécuté** : aucune expérience n'est revendiquée.
- **non démontré** : aucune équivalence ou capacité générale n'est revendiquée.

Les résultats négatifs, ambigus et divergents sont conservés ; l'auditeur de benchmark n'est jamais injecté dans l'interface de découverte.

## V1 conservée

Le code source complet V1 se trouve dans `legacy_NGeGenBrain_v1/`. Pour les détails sur son AST, contrats, maillage, traces, stockage, modèle du monde, CLI/Web et formalismes originaux, consulter son `README.md` et `docs/REPORT_AUDIT_NGeGenBrain_v1.md`.

## Licence

La licence incluse est la licence de recherche/non commerciale personnalisée de V1, conservée sans modification. Consulter `LICENSE`.


===== sonde_adapt_1_bundle/observation/README.md =====
# NGeGenBrain — formalisme unifié de l’observation et de la reconstruction

## Livrables

- `NGeGenBrain_observation_formalisme_full_0.tex` : source LaTeX maître refondue et harmonisée.
- `NGeGenBrain_observation_formalisme_full_0.pdf` : PDF final compilé, 109 pages A4.
- `NGeGenBrain_observation_formalisme_next_1.tex` et `.pdf` : suite autonome sur l’invariance contextuelle, l’information résiduelle, le temps et la décomposition invariant/variant.
- `sources/NGeGenBrain_observation_formalisme.tex` : source fondatrice.
- `sources/NGeGenBrain_observation_formalisme_next_0.tex` : formalisme du problème inverse et de la reconstruction mécaniste.
- `sources/NGeGenBrain_observation_formalisme_next_1.tex` : source corrigée de la suite invariant/variant incluse dans le maître.
- `audit_NGeGenBrain_observation_formalisme_full_0.md` : audit des corrections, validations et limites.
- `traceabilite_NGeGenBrain_observation_formalisme_full_0.csv` : traçabilité de tous les chapitres source.
- `verification_NGeGenBrain_observation_formalisme_full_0.json` : résultats structurels et empreintes.
- `verify_NGeGenBrain_observation_formalisme_full_0.py` : vérificateur structurel.
- `build_NGeGenBrain_observation_formalisme_full_0.py` : génération du maître et des registres depuis les sources archivées.
- `compile_final.log`, `compile_next_1_final.log` : journaux LaTeX finaux.
- `checksums.sha256` : sommes de contrôle internes du bundle, hors ce fichier lui-même.

## Organisation théorique

La théorie distingue l’observation, l’enregistrement, l’empreinte relative à un protocole, l’invariant relatif à une famille de transformations déclarée, la composante variable/résiduelle, la trace temporelle, le dossier d’évidence, le mécanisme candidat, le mécanisme exécutable et la validation indépendante. Elle couvre les échelles de sondes, les vues complémentaires, l’observation continue, les interventions, l’identifiabilité, le problème inverse, la composition hiérarchique récursive, l’incertitude et la provenance.

**Précision sur l’invariance.** Pour un objet, un contexte et une famille de sondes fixés, l’empreinte est une signature bien définie et constante sur les fibres d’indiscernabilité qu’elle induit. Cette constance par définition n’implique pas que la signature soit préservée sous une transformation de l’objet ou un changement de contexte. Une « invariance contextuelle » doit donc déclarer son ensemble de contextes et démontrer l’égalité correspondante.

Une empreinte seule ne permet généralement pas de reconstruire une observation complète si elle a éliminé des variantes pertinentes. Le problème inverse produit alors un ensemble de mécanismes compatibles, sauf si des hypothèses d’identifiabilité explicitement satisfaites permettent d’isoler une classe ou un mécanisme.

## Sources et traçabilité

Les trois sources archivées contiennent respectivement 25, 21 et 12 chapitres, soit 58 chapitres au total. Tous sont affectés au corps argumentatif ou aux annexes, avec une ligne par chapitre dans la matrice CSV. Aucun fichier distinct nommé `NGeGenBrain_observation_formalisme_0.tex` n’a été trouvé; aucun contenu manquant n’a été inventé. `next_1` est inclus parce qu’il formalise l’idée invariant/variant et les échelles d’observation.

## Reproduction

Prérequis : Python 3 et une distribution TeX avec `latexmk`/`pdflatex` et les paquets usuels utilisés par le préambule.

```bash
python build_NGeGenBrain_observation_formalisme_full_0.py
mkdir -p build
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build NGeGenBrain_observation_formalisme_full_0.tex
python verify_NGeGenBrain_observation_formalisme_full_0.py
```

Le script de génération reconstruit le `.tex` maître et les registres depuis les fichiers sous `sources/`. La compilation PDF est une étape distincte.

## Résultats structurels et limites

Le document maître contient 51 chapitres, 8 parties, 94 définitions, 3 environnements d’hypothèse explicite et 81 énoncés de type théorème/proposition/lemme/corollaire avec 81 environnements de démonstration correspondants. Les 58 chapitres source sont tracés. Ces comptes sont structurels; l’égalité du nombre d’énoncés et de preuves ne certifie pas automatiquement les preuves.

La compilation finale réussit sans erreur LaTeX, sans commande indéfinie, référence non résolue ni débordement horizontal; des avertissements `Underfull \\hbox` restent présents dans certains blocs étroits. Cette refondation n’est pas une certification par assistant de preuve ni une revue mathématique indépendante externe. Les hypothèses conditionnelles et les limites d’identifiabilité demeurent explicites.


===== sonde_adapt_global_research_final/README_FINAL.md =====
# NG-ADAPT — livraison finale de recherche

**Campagne :** `NG-ADAPT-2026-10-29-v1`  
**Version de l’audit indépendant :** `NG-ADAPT-INDEPENDENT-AUDIT-v6`
**But :** confronter les architectures de sondes adaptatives locales, coordonnées globalement, activées et dotées d'une boucle observation–empreinte–mise à jour, sans présumer de leur supériorité.

## Lire dans cet ordre

1. [`SYNTHESE_EXECUTIVE.md`](SYNTHESE_EXECUTIVE.md) — conclusions et statut de chaque hypothèse.
2. [`ETAT_DES_PHASES.md`](ETAT_DES_PHASES.md) et [`CONFORMITE_PROMPT_DETAILLEE.md`](CONFORMITE_PROMPT_DETAILLEE.md) — exigences du `prompt.txt`, phase par phase et règle rouge par règle rouge.
3. [`FORMALISME_ADAPTATION_GLOBALE.pdf`](FORMALISME_ADAPTATION_GLOBALE.pdf) — définitions, équations, hypothèses et preuves conditionnelles. Le `.tex` est fourni à côté.
4. [`RESULTATS_COMPLETS.md`](RESULTATS_COMPLETS.md) — tables par tâche, architectures, ablations, boucle et reconstruction.
5. [`PROTOCOLE_PREENREGISTRE.md`](PROTOCOLE_PREENREGISTRE.md), [`docs/PROTOCOLE_FEEDBACK_FINGERPRINT.md`](docs/PROTOCOLE_FEEDBACK_FINGERPRINT.md) et [`docs/PROTOCOLE_BOUCLE_RECONSTRUCTION.md`](docs/PROTOCOLE_BOUCLE_RECONSTRUCTION.md) — protocoles de base et suppléments causaux.
6. [`sites_web_consulte.json`](sites_web_consulte.json) — registre des pages consultées, requêtes, motifs d’utilisation, dispositions et limites de traçabilité historique.
7. [`AUDIT_INDEPENDANT.md`](AUDIT_INDEPENDANT.md) et [`LIMITES_ET_INCERTITUDES.md`](LIMITES_ET_INCERTITUDES.md) — ce que l'audit établit et ce qu'il n'établit pas.
8. [`REPRODUIRE_LES_EXPERIENCES.md`](REPRODUIRE_LES_EXPERIENCES.md) — commandes et reprise par tâche, sans réentraîner les runs déjà calculés.
9. [`INVENTAIRE_SOURCES.md`](INVENTAIRE_SOURCES.md), [`ENVIRONNEMENT.md`](ENVIRONNEMENT.md), [`REGISTRE_DES_AFFIRMATIONS.md`](REGISTRE_DES_AFFIRMATIONS.md), [`JOURNAL_EXECUTION.md`](JOURNAL_EXECUTION.md) — provenance, environnement et statut des affirmations.

## Résultats exécutés

- Vérification de l'intégrité de l'archive source et contrôle récursif de **80 archives ZIP imbriquées**, sans échec d'intégrité ni chemin d'extraction dangereux détecté.
- Rejeu strict du script de référence « two moons » : CSV et JSON reproduits octet par octet.
- **198 entraînements A–K sur six tâches** : 165 entraînements (cinq tâches binaires) + 33 runs digits à dix classes; **38 313 prédictions de test** (29 403 binaires + 8 910 multiclasse). S’ajoutent 60 exécutions d’ablation de coordination, 120 lignes métriques / 16 200 empreintes de robustesse, 390 lignes / 54 000 empreintes dans FBR-1, 148 lignes métriques de reconstruction et RBF-R1 (162 lignes / 23 040 empreintes).
- Audit indépendant v6 : **49/49 contrôles réussis**; cinq contrôles additionnels couvrent l’extension digits10 et l’audit de provenance web est consigné.
- Tests logiciels des projets sources : observation formalisme 109 pages vérifié par son validateur, v1.2 `PASS_WITH_LIMITATIONS` (16/16), v2 117 tests + 10 sous-tests, v3.1 66 tests et test de non-régression V1 65 tests.

Ces succès sont des résultats de reproductibilité et d'ingénierie, pas une preuve de supériorité scientifique universelle. Les six tâches de benchmark (cinq binaires et une multiclasse) utilisent chacune un split fixe et trois graines d'optimisation. L'effet de la coordination et de la boucle varie selon la tâche; une mise à jour en ligne sous labels trompeurs peut provoquer une dérive grave.

## Arborescence

- `code/` — exécuteurs de benchmark, boucle, reconstruction et audit indépendant.
- `configs/` — configuration globale.
- `requirements.txt` et `ENVIRONNEMENT_LOCK.txt` — dépendances épinglées et versions observées.
- `results/` — CSV/JSON de métriques, prédictions, partitions, audits de jeux de données et manifests.
- `figures/` — graphiques finaux des effets FBR-1 et RBF-R1, plus la planche contact des sept pages du PDF contrôlée visuellement; les données à l’origine des figures sont les CSV fournis.
- `logs/` — sorties standard, erreurs et codes de sortie; un run monolithique interrompu est gardé à titre de trace.
- `sites_web_consulte.json` — registre des **40 URL uniques et 28 requêtes** de recherche documentées, avec motifs, dispositions et limites de traçabilité historique.
- `source_copies/` — copies de référence des fichiers sources théoriques prioritaires et du `prompt.txt`; le manifeste exhaustif des fichiers extraits et leurs SHA-256 se trouve dans `results/source_audit/recursive_source_file_manifest.csv`.
- `FORMALISME_ADAPTATION_GLOBALE.{tex,pdf}` — formalisme ajouté.
- `docs/` — protocoles, comparaisons, limites et rapports.

## Intégrité

Le prompt de base est évalué phase par phase dans `CONFORMITE_PROMPT_DETAILLEE.md`. Les phases 1, 4 (couverture complète de toutes les boucles par tâche/architecture) et 8 restent partielles pour les raisons explicites du rapport; la livraison ne les déclare pas satisfaites au-delà des éléments réellement exécutés.

Consulter `SHA256SUMS.txt` pour les empreintes de tous les fichiers livrés, à l'exception du manifeste lui-même. Après extraction, `python3 code/validate_delivery.py` contrôle ce manifeste, les fichiers structurés et le PDF sans modifier la livraison. L’archive distribuée `sonde_adapt_global_research_final.zip` a un SHA-256 externe dans le fichier compagnon `SHA256SUMS_DELIVERY.txt`, livré séparément. L'archive a passé `unzip -t`, puis l'extraction a passé les 8 contrôles de `code/validate_delivery.py`. Les archives originales n'ont pas été modifiées et ne sont pas recopiées intégralement dans la livraison : leurs empreintes, résultats de validation et extractions sont documentés.


===== sonde_adapt_global_research_final/docs/README_FINAL.md =====
# Index documentaire local

Le README final canonique se trouve à [`../README_FINAL.md`](../README_FINAL.md). Il décrit les résultats, commandes de reproduction, contrôles d’intégrité et limites scientifiques.

Documents détaillés conservés dans ce répertoire : `SYNTHESE_EXECUTIVE.md`, `RESULTATS_COMPLETS.md`, `ETAT_DES_PHASES.md`, `CONFORMITE_PROMPT_DETAILLEE.md`, `RED_RULES_AUDIT.md`, `PROTOCOLE_PREENREGISTRE.md`, `PROTOCOLE_FEEDBACK_FINGERPRINT.md`, `PROTOCOLE_BOUCLE_RECONSTRUCTION.md`, `PROTOCOLE_DIGITS_10CLASSES.md` et `LIMITES_ET_INCERTITUDES.md`.


===== sondes_ex4_workspace_20261030/README_EX4.md =====
# Workspace EX4 — sondes adaptatives compactes contre MLP

**Date de gel/livraison :** 30 octobre 2026  
**Dernière version :** `sondes_ex4_v009__2026-10-30`  
**État :** développement Wisconsin + récupération micro-MIXA + un transfert Iris exploratoire achevé ; succès global non démontré.

## Objectif
Trouver une sonde ayant au plus 25 % des coefficients numériques persistants d'un MLP compétitif (P_MLP/P_sonde ≥ 4), sans infériorité en accuracy et log-loss, et avec des coûts inférieurs ou égaux. Paramètres fixes, entraînables et prétraitement partagé sont distingués.

## Conclusion scientifique
Les sondes compactes satisfont le ratio de paramètres mais ne battent pas simultanément les MLP en accuracy, log-loss et ressources. Sur Wisconsin, aucune des 12 familles v006 ne satisfait l'ensemble des conditions. Sur Iris, quatre candidates (adaptatif et trois micro-MIXA) ont été évaluées sur cinq initialisations ; accuracy parfois égale au MLP mais log-loss et latence moins bonnes. L'objectif n'est pas atteint.

## Résultats et livrables
- `prompt_ex4.json` : copie révisée de `prompt_ex3.json`, complétée par la piste micro-MIXA.
- `deliverables/debrit_0_reconstruction.md` : extraction des idées et limites des débris.
- `deliverables/rapport_executif_ex4.md`, `rapport_technique_ex4.md` : conclusions et protocole détaillés.
- `deliverables/rapport_micro_mixa_ex4.md` : hybride micro-MIXA et ablations.
- `deliverables/rapport_transfert_externe_iris.md` : transfert et limites d'isolation.
- `deliverables/AUDIT_V007_MIXED_REGISTRY.md` : séparation du registre mélangeant deux campagnes.
- `deliverables/tableau_conformite_ex4.md` : conformité exigence par exigence.
- `versions/` : v001–v009, scripts, logs, données, prédictions brutes, tables, états modèles, audits et checksums.

## État des preuves
- v005 et v006 : tests d'intégrité PASS, Wisconsin historique.
- v007 : registre brut de 95 lignes mélangeant 70 initiales + 25 add-on ; test historique non filtré échoue par comptage ; audits filtrés séparés passés.
- v008 : récupération micro-MIXA Wisconsin PASS, sans réentraînement, ratios ≥4x.
- v009 : transfert Iris PASS audit technique, 20 sondes, 40 MLP, 60 métriques test, aucun réglage après test. Réserve explicite : loader Iris matérialise le dataset complet et la stratification lit les labels ; pas d'isolation mémoire stricte.

## Non achevé / obstacles
- Workspace/code/checkpoints EX3 et jeux bruts cités dans les débris absents de l'archive.
- Banknote Authentication et MAGIC Gamma Telescope indisponibles au téléchargement à cause de la résolution DNS/réseau de l'environnement.
- Pas de confirmation multi-domaines vierge, pas d'IC de non-infériorité, pas de mesures hardware complètes des FLOPs/MAC, VRAM, énergie ou coût total de recherche.
- Cinq seeds signifient cinq initialisations, pas cinq jeux indépendants.

## Vérifications rapides
```bash
cd versions/sondes_ex4_v006__2026-10-30 && python tests/test_ex4_integrity.py
cd ../sondes_ex4_v008__2026-10-30 && python scripts/audit_micro_mixa_recovery.py
cd ../sondes_ex4_v009__2026-10-30 && python scripts/audit_iris_transfer.py
```

## Continuité finale et intégrité
Le rapport de continuité final est disponible dans `deliverables/rapport_continuite_finale_ex4.md` et le catalogue des artefacts dans `deliverables/manifest_livrables.md`. Lors de la reprise, les copies de `prompt_ex4.json` ont toutes été relues comme JSON et vérifiées identiques (SHA-256 `39471af7dabb7ad80a6379b6c2d2cc53a41d8a35af6369c344b82bd1546b36d4`). Les derniers tests v005, v006, v008 et v009 passent. Le test global historique v007 échoue toujours de façon attendue sur le comptage (95 entrées au lieu de 70) ; les audits filtrés sont la référence pour ce registre mixte. Les journaux et preuves de ces exécutions figurent dans `checksums/`.

**Conclusion ferme :** objectif de réduction des paramètres atteint, mais objectif conjoint performance + ressources non atteint. La campagne reste partielle au sens strict du prompt faute de datasets Banknote/MAGIC récupérables, d'énergie/VRAM mesurées et de démonstration statistique formelle de non-infériorité.


===== sondes_ex5_workspace_20261030/README.md =====
# Workspace de recherche EX5

Workspace dédié à la continuation scientifique EX4 → EX5. Racine canonique : `/mnt/data/sondes_research_workspace_ex5/`.

- `inputs/` conserve les prompts immuables, références et empreintes.
- `versions/sondes_ex5_v001__2026-10-30/` contient la première campagne EX5.
- `reports/` contient les rapports globaux et de continuité.
- `checksums/` contient les inventaires SHA-256 et états de tests.

Règles : pas de modification des sources EX2/EX3/EX4 ; pas d'écrasement de runs terminés ; journaux bruts append-only ; sorties écrites atomiquement ; toute campagne interrompue reste documentée et reprenable. Les données/test restent scellées jusqu'au gel explicite de chaque tâche.


===== sondes_ex5_workspace_20261030/README_EX5_FINAL.md =====
# Workspace EX5 — état consolidé v001–v007 (30 octobre 2026)

EX5 est une campagne versionnée prolongeant EX4 : RETRO/Adam, proportions fixes-adaptatives, correcteur alterné A↔B, micro-MIXA hiérarchique question/réponse, résidus OOF, optimisation du partage encodeur/centres, PCA question-only, transfert Wine/Digits et profilage CPU. Les artefacts historiques, registres bruts, checkpoints et prédictions sont conservés ; les tableaux sont dérivés.

## Conclusion scientifique

Aucune candidate ne démontre simultanément la non-infériorité prédictive pré-enregistrée et la conformité à chacune des dimensions obligatoires mesurées de la règle rouge. Les 437 comparaisons physiques MLP ge4x auditées respectent `P_MLP_total / P_sonde_total >= 4` (minimum 4,000735×). L'OOF est entièrement livré et audité, mais plus lent en entraînement et en latence batch 1 que son MLP ge4x. La règle rouge globale n'est donc pas satisfaite.

## Versions expérimentales

- v001 : RETRO/factoriel, proportions, OOF résiduel et premières topologies Q/A.
- v002 : sémantiques Adam/gel et alternance A↔B.
- v003 : transfert Wine/Digits, gel test et bootstrap apparié.
- v004 : ablations hiérarchiques questions/réponses.
- v005 : partage d'encodeur/centres et optimisation micro-MIXA.
- v006 : PCA question-only, MLP appariés et vectorisation.
- v007 : profilage TorchScript/Numba sans réentraînement ; parité stricte contrôlée.

## OOF — artefacts complets

La famille `TWO_LEVEL_OOF_RESIDUAL` comprend 25 modèles fold (5 folds × 5 graines), 25 états de reprise avec Adam, 25 marqueurs, cinq caches OOF, dix composites finaux (tête fixe/adaptative × cinq graines), dix états de reprise de la tête, dix fichiers de métriques, dix prédictions, et 20 liens MLP matched/ge4x. L'audit spécifique recense 162 artefacts sans manque et vérifie les partitions, les prédictions OOF, la réinférence composite et les métriques (écart maximal 0). Le forward n'accepte que X. Voir `deliverables/oof_artifact_manifest_ex5.csv`, `oof_artifact_audit_ex5.json` et `rapport_oof_mlp_appariement_ex5.md`.

## Nomenclature sans ambiguïté

- `MIXA` (`MIXA_GENERAL`) : famille générale adaptative + banque fixe + mélange appris.
- `micro-MIXA` (`MICRO_MIXA`) : instanciation compacte explorée dans EX4/EX5.
- `MiXA` et `micro-MiXA` : alias de casse uniquement, pas de modèle supplémentaire.
- `mixa_micro_d4_k8` : alias historique de micro-MIXA ; la valeur de 528 coefficients des débris demeure non vérifiable.

Voir `deliverables/NOMENCLATURE_EX5.md`, `nomenclature_registry_ex5.json`, `INDEX_VARIANTS_EX5.md` et `catalogue_campagnes_ex5.csv`.

## Intégrité et limites

Le dernier audit complet couvre 3 951 fichiers non-cache : 1 865 JSON valides, 1 720 lignes JSONL dans 53 fichiers et 60 CSV rectangulaires. Aucun défaut de parsing/forme, aucun hash prompt divergent, aucun lien symbolique sortant. Les audits des versions contrôlent 1 313 références checkpoint, 1 162 références canoniques de prédiction, 826 recalculs et 437 liens ge4x sans divergence/ratio inférieur à 4. Les doublons et pointeurs remplacés sont conservés et documentés.

Banknote/MAGIC sont bloqués par l'échec DNS du runtime ; VRAM et énergie ne sont pas mesurables (CPU-only) ; les MACs complets d'entraînement et une télémétrie RSS uniforme restent non mesurés. EX5 n'est donc pas déclaré complet au sens de la réussite scientifique globale.

## Documents de référence

- `deliverables/rapport_reprise_finale_ex5.md`
- `deliverables/rapport_executif_ex5.md` et `rapport_technique_ex5.md`
- `deliverables/rapport_retro_adam_ex5.md`
- `deliverables/rapport_micro_mixa_ex5.md`
- `deliverables/rapport_alternance_hierarchie_ex5.md`
- `deliverables/rapport_oof_mlp_appariement_ex5.md`
- `deliverables/rapport_generalisation_ex5.md` et `rapport_ressources_ex5.md`
- `deliverables/matrice_conformite_ex5.md`
- `deliverables/audit_integrite_ex5.md` et manifestes SHA-256

Prompt actif : `inputs/prompt_ex5.json` (v1.1), SHA-256 `88f67fc34bf34c5ca0817da42a057ed71dfb092cfb33720be5532da96bab3291`. La version 1.0 et les prompts de référence sont conservés.


===== sondes_ex6_v003_livrables/README.md =====
# Workspace EX6 — sondes adaptatives

Workspace expérimental distinct des sources EX3–EX5.

## Fichiers d'entrée
- `prompt_ex6.json` : prompt d'expérience révision 1.0.1 (également copié dans `inputs/`).
- `inputs/prompt_ex3.json`, `prompt_ex4.json`, `prompt_ex5.json` : prompts de référence.
- `inputs/reference_theory/` : formalismes théoriques utilisés.
- `inputs/reference_code/` : copies des scripts de référence EX5.
- `inputs/data_manifest/` : ledger du split historique.
- `inputs/historical/debrit_0.txt` : notes historiques non probantes.

## Scripts
- `src/ex6_common.py` : adaptation des routines communes utilisées dans les pilotes.
- `src/ex6_mixa_engine.py` : moteur de candidats MIXA.
- `src/run_replica_pilot.py` : pilote Replica inférence-only.
- `src/run_emplica_pilot.py` : pilotes Emplica simple et Orchestra.

## Résultats
- `results/raw/` : JSON bruts par run, prédictions, comparateurs et JSONL.
- `results/models/` : checkpoints et états de reprise.
- `results/metrics/` : recalcul indépendant des métriques, comparaisons par graine et agrégats.
- `reports/` : audits, notes rétrospectives, plan prospectif et rapport final.
- `configs/` : configuration rétrospective des pilotes.
- `checksums/` : manifeste sources et hashes SHA-256.
- `execution_status.json` : statut explicite des expériences et dimensions mesurées.

## Verdict de cette version
`INCOMPLET`. Les quatre familles de pilotes passent le rapport de paramètres 4× vs MLP-ge4x. Les résultats mesurés ne démontrent pas un avantage de vitesse ; les métriques ponctuelles sont généralement inférieures au MLP-ge4x. Les correcteurs OOF inter-couches, certaines familles homogène/spécialiste, le test externe vierge et plusieurs mesures de ressources restent à exécuter.

## Reproduction
Les scripts sont fournis sous `src/`. L'environnement et les graines de cette campagne sont dans `configs/pilot_config_retrospective.json`. Cette configuration est rétrospective, pas un pré-enregistrement. Les résultats bruts ne doivent pas être écrasés ; toute nouvelle campagne doit recevoir un nouvel identifiant de run et une nouvelle version de workspace.


===== sondes_ex7/sondes_ex7_livrables_complets_v002/README_EX7.md =====
# Sondes — expérience EX7 V002

Cette version est un instantané complet réconcilié au 31 octobre 2026. Commencer par `reports/INDEX_LIVRABLES_EX7_V002.md`. Les rapports de conformité distinguent explicitement les expériences terminées des mesures partielles/indisponibles. Aucun succès global n'est revendiqué.


===== sondes_ex7/sondes_ex7_v003/README_EX7_V003.md =====
# EX7 V003 — OuterCoord-Lite-7x1

Cette version teste une architecture simplifiée à sept `AdaptiveRBF` indépendantes et un coordinateur externe `rho` unique. Elle retire les sept gates internes et la cascade 7×5 d'Orchestra Org. Tous les résultats négatifs et limites sont conservés.

## Résultat clé

- Paramètres persistants : 1 341 (contre 6 712 pour Orchestra 7×5).
- Moyenne cinq seeds : accuracy 97,88 %, macro precision 97,34 %, log-loss 0,06806.
- MLP apparié : 98,12 % accuracy, log-loss 0,05136 ; MLP-ge4x : 98,59 %, log-loss 0,05222.
- Latence raw-end-to-end p50 batch 1 : 0,290 ms V003, 1,490 ms Orchestra outer-only, 0,025 ms MLP matched.
- Verdict : gain structurel et contre Orchestra, mais pas de supériorité globale ; marges de log-loss non respectées et inférence plus lente que les MLP.

## Reproduction

Depuis la racine du projet, dans un environnement compatible décrit par `configs/ENVIRONMENT_V003.json` :

```bash
python src/run_outercoord_lite_v003.py
python src/profile_end_to_end_v003.py
python src/audit_v003.py
```

`run_outercoord_lite_v003.py` entraîne la candidate et les deux MLP pour les cinq seeds, vérifie les références, profile le modèle seul et consolide les tableaux. Le profil raw-end-to-end inclut le scaler. Les runs existants ne sont pas écrasés : ils sont réutilisés après contrôle de leur hash.

## Principaux dossiers

- `inputs/` : prompt, données dev-only et références V002 compactes immuables.
- `configs/` : pré-enregistrement, configuration parent, environnement.
- `src/` : entraînement, inférence, profilage, parité et audit indépendant.
- `results/raw/` : prédictions, résultats par seed, historiques.
- `results/models/` : checkpoints et état d'optimiseur.
- `results/metrics/` : agrégats, différences appariées, latence brute et métriques.
- `reports/` : rapports de performance, protocole, conformité, anomalies et audit.
- `logs/` : sorties/stdout/stderr originaux, y compris l'anomalie de consolidation.
- `checksums/` : manifestes finaux SHA-256.

## Limites essentielles

Wisconsin est un split de développement historiquement exposé, non une validation externe vierge. Le test externe n'a pas été ouvert. Les 57 lignes d'adaptation n'ont pas été utilisées. Temps complet d'initialisation/training, RAM isolée comparable, FLOP complets et énergie sont `NON MESURÉ`. Le verdict est développement uniquement.


===== sondes_ex8_v010_B10_ACTION_LANGUAGE_COMPLETE_DOSSIER__2026-11-01/README_B10_COMPLETE.md =====
# Dossier complet B10 — langage d’actions codifiées (EX8 v010)

Ce dossier complémentaire rassemble le code, les configurations, les données d’entraînement/validation autorisées, les checkpoints, les prédictions, les historiques et les comparateurs MLP pour B10 et son contrôle B11. Le paquet global EX8 v010 contient en plus toutes les autres variantes A0–A4 et B1–B9.

## Résultat B10 sur Wisconsin (5 graines)

| Graine | B10 log-loss | B11 gate standard | MLP apparié B10 | MLP ≥4× B10 |
|---:|---:|---:|---:|---:|
| 1501 | 0.04507602 | 0.04639599 | 0.05309571 | 0.05388297 |
| 1607 | 0.03892050 | 0.03918663 | 0.05443205 | 0.05022439 |
| 1717 | 0.03475841 | 0.04361378 | 0.05260622 | 0.05136449 |
| 2029 | 0.04704858 | 0.04824928 | 0.05549038 | 0.05049692 |
| 3037 | 0.04114467 | 0.04468064 | 0.05801149 | 0.04804699 |

Moyennes : B10 **0.04138964**, B11 **0.04442526**, MLP apparié B10 **0.05472717**, MLP ≥4× **0.05080315**. B10 bat son MLP apparié sur **5/5 graines** et le MLP ≥4× sur **5/5 graines**.

## Architecture B10

- Un seul niveau, cinq probes parallèles.
- Dimension latente D=4, K=4 centres par probe.
- 20 évaluations de centres RBF par observation.
- État flou 3×3 construit à partir de la marge OOF et du désaccord inter-probes.
- Une table 9×5 produit des poids continus softmax sur les cinq vecteurs de logits ; le codebook ne décide jamais la classe.
- 45 paramètres d’action ; total déclaré 884 paramètres.
- Les seuils sont estimés uniquement sur les signaux OOF du train.

## Comparaison statistique B10 vs B11

Delta moyen (B10 − B11) = **-0.00303563**. Les cinq différences par graine sont négatives, mais l’IC t apparié à 95 % [-0.00734137, 0.00127012] recouvre zéro ; le test exact de permutation des signes bilatéral donne p=0.0625. L’avantage observé doit donc rester qualifié d’encourageant mais exploratoire.

Latence p50 batch 1 moyenne : B10 0.331801 ms ; B11 0.116289 ms ; ratio B10/B11 **2.853×**. Le mécanisme d’actions est plus lent que le gate standard.

## Fichiers inclus

- `workspace/src/` : scripts d’exécution et moteur partagé.
- `workspace/configs/` : pré-enregistrement B10/B11 et configurations par graine.
- `workspace/inputs/` : code commun et Wisconsin train/validation only.
- `workspace/results/metrics/` : métriques candidates, MLP, comparatif direct et agrégats.
- `workspace/results/models/` : checkpoints B10, B11, backbone et MLP appariés/≥4×.
- `workspace/results/raw/` : prédictions et historiques B10/B11/backbone/MLP disponibles.
- `B10_B11_PAIRED_RESULTS.csv` : table condensée par graine.
- `SHA256SUMS.txt` : manifeste d’intégrité du dossier.

## Limites

Les chiffres sont des résultats de développement sur la partition Wisconsin, pas une validation externe confirmatoire. La réplication SMS est historiquement exposée et B10 n’y bat pas les MLP. Le test indépendant n’a pas été ouvert dans cette campagne. Les checkpoints et prédictions fournis permettent l’inspection et la vérification des métriques ; une reproduction exacte de l’environnement exige les versions de bibliothèques et le matériel documentés dans la configuration système du workspace complet.


===== sondes_ex8_v010__2026-11-01_RESULTS_AND_METHODS/README.md =====
# EX8 v010 — workspace expérimental PCA / V004

Version active : `versions/sondes_ex8_v010__2026-11-01/` (cf. `/mnt/data/EX8/ACTIVE_VERSION.txt`).

Cette branche réunit le contexte EX8 v001/v009, les expériences A0–A4 et B1–B11, les comparateurs MLP, les réplications SMS train/validation et les audits indépendants. Les données sources et snapshots historiques sont conservés en référence ; les runs v010 ne les écrasent pas.

Lire en premier :
1. `reports/RAPPORT_FINAL_V010.md`
2. `reports/AUDIT_PROMPT_EX8.md`
3. `reports/STATISTICAL_ANALYSIS_V010.md`
4. `reports/RESOURCE_ANALYSIS_V010.md`
5. `configs/PRE_REGISTRATION_V010_AB.md` et l’addendum B10/B11.

Les résultats détaillés par run sont dans `results/metrics/`, `results/raw/` et `results/models/`. Les manifestes et vérifications sont sous `deliverables/` et `checksums/`. Les sorties ne doivent pas être écrasées ; toute continuation doit créer une nouvelle version sous `EX8/versions/` et conserver `v010` immuable.


===== sondes_research_workspace_final/README.md =====
# Workspace — recherche sur les sondes adaptatives

Date de création : 2026-10-30

## Objectif

Espace non destructif dédié à l'exécution et à la traçabilité du prompt de recherche révisé (`prompt_ex2.json`). Il sert à reconstruire expérimentalement des sondes adaptatives, étudier l'émergence progressive de la coordination globale, puis vérifier les résultats sur des domaines extérieurs.

## Règles

- Les archives et résultats sources sont conservés dans `versions/sondes_v001__2026-10-30/legacy_reference/` sans modification.
- Chaque campagne substantielle reçoit un nouveau dossier versionné `versions/sondes_vNNN__YYYY-MM-DD/` ; le numéro le plus élevé est la version la plus récente.
- Chaque version possède son propre README, protocole, code, configurations, journaux, résultats bruts/traités, figures, rapports, tests et checksums.
- Aucun dossier abandonné n'est supprimé. Son README indique `ABANDONED`, la date, le motif, les essais, résultats et ressources consommées.
- Les résultats bruts ne sont jamais réécrits silencieusement. Les corrections produisent de nouveaux artefacts versionnés.
- L'exploration ne reçoit aucun plafond arbitraire. Elle dépend des ressources réellement accessibles et des permissions effectives.

## Version courante

Voir [`WORKSPACE_INDEX.md`](WORKSPACE_INDEX.md). La version la plus récente est `sondes_v009__2026-10-30` ; voir `WORKSPACE_INDEX.md`.

## Livrables finaux

- Rapport exécutif : `versions/sondes_v009__2026-10-30/reports/synthese_executive.md`
- Rapport technique : `versions/sondes_v009__2026-10-30/reports/rapport_technique_final.md`
- Audit intégrité/conformité : `versions/sondes_v009__2026-10-30/reports/audit_integrite_et_conformite.md`
- Contrôle reproductible : `versions/sondes_v009__2026-10-30/scripts/audit_delivery.py`
