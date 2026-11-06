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
