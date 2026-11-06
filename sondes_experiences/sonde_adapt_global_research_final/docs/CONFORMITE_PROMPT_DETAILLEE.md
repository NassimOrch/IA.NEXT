# Matrice de conformité détaillée avec `source_copies/prompt.txt`

Cette matrice vérifie la réalisation observable du prompt source, pas l'intention déclarée. `SATISFAIT` signifie que les éléments énumérés ont un artefact ou une vérification. `PARTIEL` signifie qu'une exigence plus large du prompt n'a été couverte que dans le périmètre indiqué. `NON SATISFAIT / EXPLICITE` signale un écart conservé dans le rapport au lieu d'être masqué.

## Identité et intégrité de la consigne

| Objet | Résultat vérifiable |
|---|---|
| Archive racine | `/mnt/data/sources_ng_adapt_0.zip`; SHA-256 `8fcf82931988a96cdfb1ff5cbe5892142b4b1174385dc87cd9ed0f9e2d7069bb`; test ZIP réussi; 26 entrées racine. |
| Prompt extrait | `source_copies/prompt.txt`; SHA-256 `ef4f007a968908209427b894e5aafcd9a453cf61a1d5925f02334b03fe9b188a`; 35 706 octets / 1002 lignes. |
| Bundle principal `sonde_adapt_1_bundle.zip` | SHA-256 `0825554aeaac3f570f052fca43806be133f1dc0e49d836bf0fcecc5190cb5465`; 110 206 894 octets; 1265 membres; test d'intégrité réussi. |
| Archives imbriquées | 80 contrôlées récursivement; intégrité passante pour chacune; aucun chemin d'extraction dangereux ou lien symbolique détecté dans le journal d'audit. |
| Copies non destructives prioritaires | `etude_et_formalisme_sonde_adaptative_1.tex`, `rapport_th_emp_vs_obs_1.tex`, `DDD_Base_theorie_des_empreintes_complete_order_5.tex`, `NGeGenBrain_observation_formalisme_full_0.tex`, `prompt.txt` dans `source_copies/`. |
| Manifeste extrait | `results/source_audit/recursive_source_file_manifest.csv`: 14 970 entrées; contenu et hashes enregistrés. Ce total est un inventaire des vues extraites et peut inclure des fichiers représentés dans plus d'une arborescence de bundle. |

## Phase par phase

| Phase du prompt | Statut | Preuve / écart explicite |
|---|---|---|
| 0 — Espace, inventaire, environnement, intégrité | **SATISFAIT avec réserves binaires** | Inventaire récursif, hashes, vérification ZIP, environnement et journal; 2045 fichiers Python passés par l'analyse AST sans erreur. Les quatre JSON invalides, le JSONL tronqué, la signature Parquet sans décodage et les doublons textuels ont été conservés et signalés. La source originale n'a pas été altérée. |
| 1 — Reproduction des expériences précédentes | **PARTIEL** | L'expérience historique `two_moons` a été exécutée indépendamment avec CSV/JSON reproduits exactement octet par octet. Validateurs source exécutés : v1.2 16/16 `PASS_WITH_LIMITATIONS`; formalisme d'observation, manifests v2/v3.1 et suites de tests consignés. Tous les essais historiques de remplacement, toutes les compositions et le scénario complet 10 classes digits n'ont pas été rejoués strictement; ils ne sont pas présentés comme reproduits. |
| 2 — Formalisme de l'adaptation globale | **SATISFAIT pour le modèle effectivement étudié; pas de théorème universel** | `.tex` et PDF accessibles sans le code; définitions d'état local/global, communications, objectifs, activation, état persistant, ordre d'update, réductions, non-identifiabilité et preuve de stabilité pour un objectif quadratique strictement convexe sous pas approprié. Les garanties sont conditionnelles. Comparaisons référencées : RBF approximation [Park & Sandberg, 1991](https://doi.org/10.1162/neco.1991.3.2.246), MAML [Finn et al., 2017](https://proceedings.mlr.press/v70/finn17a.html), optimisation bi-niveau [Franceschi et al., 2018](https://proceedings.mlr.press/v80/franceschi18a.html), FedAvg [McMahan et al., 2017](https://proceedings.mlr.press/v54/mcmahan17a.html), approximation à deux temps [Borkar, 1997](https://doi.org/10.1016/S0167-6911(97)90015-3). |
| 3 — Protocole et préenregistrement | **SATISFAIT avec dérogations documentées** | `PROTOCOLE_PREENREGISTRE.md` et protocoles séparés FBR-1/RBF-R1. Graines, splits, métriques primaires/secondaires, actions contrôlées et seuils décrits. La taille d'échantillon reste trois graines d'optimisation sur un split par tâche; pas d'analyse de puissance confirmatoire, d'égalisation stricte FLOPs/RSS ou de calibration sur de nombreux splits. |
| 4 — Cinq familles d'architecture | **PARTIEL en largeur; exécuté dans des sous-périmètres traçables** | A–K totalise 165 entraînements sur cinq tâches binaires, auxquels s'ajoutent 33 runs digit10 (198 au total, six tâches); ablation coordination 60 runs. La robustesse de base porte sur A–E et `two_moons`. Dans les anciens F–J, l'empreinte était journalisée mais n'influençait pas la décision; FBR-1 ajoute une vraie politique causale de gate/routage sur A–E pour `two_moons`, cinq flux et trois graines. Ce supplément n'étend pas cette boucle à chaque architecture sur chaque tâche.
| 5 — Composition `input1 → f → g → output2` | **SATISFAIT pour la tâche synthétique déclarée; généralité non établie** | 148 lignes métriques, trois graines, identity directe, composition RBF locale/globale, activation, bottleneck, MLP autoencoder, bruit/décalage et boucle. Pas de skip connection; `g` n'a pas directement accès à `x`. Supplément RBF-R1 : 6 paires, 162 lignes métriques, 23 040 événements; l'empreinte pilote réellement le gate. Résultat négatif conservé : les updates et le gate q90 peuvent déstabiliser deux modèles RBF de reconstruction. |
| 6 — 25 règles rouges | **PASS / PARTIEL règle par règle** | Voir `RED_RULES_AUDIT.md` et le détail ci-dessous. Les audits instrumentés sont positifs; ils ne peuvent pas établir l'absence de toutes les fuites sémantiques possibles. |
| 7 — Audit et reproductibilité | **49/49 contrôles déterministes PASS (audit v6)** | `results/independent_audit.json`, `results/independent_audit.md`, script `code/audit_independent.py`; inclut hashes, runs complets, métriques recalculées, isolation des partitions, ablations, boucles, reconstruction, registre web et extension digits10.
| 8 — Métriques et interprétation | **PARTIEL** | Classification: accuracy, précision/rappel/F1, ROC/PR-AUC, log-loss, Brier, ECE, confusion; reconstruction: MAE, RMSE, R², quantiles/max d'erreur; résultats par graine, dispersions/IC descriptifs, temps et nombre d'updates. Il manque FLOPs calibrés, RSS de pointe, latence réseau, coût mémoire exhaustif et un protocole confirmatoire multi-split. |
| 9 — Décision scientifique | **SATISFAIT comme bilan limité** | `RESULTATS_COMPLETS.md`, `SYNTHESE_EXECUTIVE.md`, `REGISTRE_DES_AFFIRMATIONS.md`, `LIMITES_ET_INCERTITUDES.md`; aucune supériorité universelle n'est déclarée. Les effets négatifs d'activation, d'updates en ligne et de gate de reconstruction restent visibles. |
| 10 — Livraison | **PASS technique (archive finale validée)** | Archive finale `livraison_recherche_finale.zip` testée avec `unzip -t`, membre par membre comparés au manifeste, extraction propre et 8/8 contrôles de `code/validate_delivery.py` réussis. Cette validation technique ne complète pas les réserves scientifiques des phases 1, 4 et 8.

## Audit des 25 règles rouges

| # | Règle exigée | Statut | Preuve, ou limite concrète |
|---:|---|---|---|
| 1 | Aucun test pour sélectionner une architecture/hyperparamètre | **PASS** | Les API de fit/updates reçoivent les partitions de train/adaptation; les tests sont post-hoc. Une partition par tâche reste une limite statistique. |
| 2 | Aucun transfert caché de labels de test | **PASS dans les chemins instrumentés** | Les labels de test sont conservés dans les CSV d'audit seulement après prédiction et ne sont pas passés aux API d'update. |
| 3 | Pas de chevauchement de données non déclaré | **PASS pour les hashes exacts** | Aucun hash exact des caractéristiques ne traverse deux partitions dans les six ledgers du benchmark (cinq tâches binaires et digits10); les quasi-doublons sémantiques ne sont pas exhaustivement audités.
| 4 | Repérer doublons/quasi-doublons | **PARTIEL** | Doublons exacts de certaines partitions contrôlés; `Screenplay_dataset.jsonl` comporte 2000 objets uniques pour 4000 lignes, et le JSONL `batch_dataset.jsonl` a une dernière ligne tronquée. Pas de déduplication sémantique globale. |
| 5 | Les métriques ne proviennent pas des prédictions d'entraînement | **PASS** | Prédictions de test ont leurs propres lignes et recalcul indépendant. |
| 6 | Aucun résultat inventé ou extrapolé comme calculé | **PASS dans le rapport** | Tous les résultats rapportés ont un artefact source ou sont marqués comme résultats archivés/non reproduits. |
| 7 | Aucun échec remplacé silencieusement | **PASS** | Logs d'interruptions, d'import, de smoke test et reprises par lots archivés; seules les campagnes complètes sont agrégées comme résultats finaux. |
| 8 | Pas de modification silencieuse du protocole après test | **PARTIEL** | Les modifications de trace/agrégation et état d'optimiseur sont documentées; ces amendements n'ont pas tous un nouveau split externe indépendant. |
| 9 | Baseline classique non volontairement sous-entraînée | **PARTIEL** | Le MLP a 90 epochs, budget de paramètre d'ordre comparable à A–E et même données; pas de sweep de tuning égalisé complet pour toutes les architectures. |
| 10 | Pas de budget caché supérieur | **PARTIEL** | Nombre de paramètres et temps mesurés; FLOPs/RSS strictement appariés manquants. Les tours centralisés donnent au coordinateur une passe globale déclarée. |
| 11 | Pas d'information inaccessible à une sonde | **PASS sous contrat déclaré** | Le coordinateur central est explicitement autorisé à voir les sorties et labels train complets; le système n'est pas décrit comme fédéré ou privé. |
| 12 | Pas de filtrage des résultats défavorables | **PASS** | Toutes les tâches/architectures/graines prévues sont présentes; effets négatifs conservés. |
| 13 | Pas de sélection de graines ou runs favorable | **PASS pour le protocole principal** | Graines prévues fixes; les anciennes erreurs et runs incomplets restent dans les journaux. Un split par tâche reste faible. |
| 14 | Pas de changement de métrique après résultats | **PASS dans le protocole documenté** | Accuracy et log-loss primaires; métriques secondaires annoncées et conservées. |
| 15 | Réussite de reproduction avec journaux/configs | **PASS pour le replay two-moons strict** | CSV et JSON de référence identiques octet par octet; les expériences non rejouées sont étiquetées partielles. |
| 16 | Pas de cache/poids pré-entraînés non déclarés | **PASS pour la campagne nouvelle** | Modèles et générateurs déclarés; les modèles historiques NGeGenBrain sont séparés et attribués à leur propre artefact. |
| 17 | Paramètres, état d'optimiseur et calcul distingués | **PARTIEL** | Paramètres stockés/mis à jour/gelés comptés dans reconstruction; état Adam tracé, mais mémoire complète des buffers et coût exact ne sont pas mesurés partout. |
| 18 | Pas d'accès implicite au futur/historique interdit | **PASS dans les boucles déclarées** | predict-before-reveal pour les flux; labels test hors update. Les données d'adaptation simulées sont un flux supervisé explicitement déclaré. |
| 19 | Pas de résultat positif basé seulement sur accuracy | **PASS** | Log-loss, AUC, Brier, ECE, F1/PR-AUC et erreurs de reconstruction rapportées selon le cas. |
| 20 | Reconstruction pas évaluée seulement sur train / solution triviale identifiée | **PASS avec contrôle trivial explicite** | Test séparé, identité RMSE=0 marquée comme contrôle direct non appris; pas de skip connection. |
| 21 | Aucun échec technique supprimé des journaux | **PASS** | Les logs d'interruption/retentatives et les codes de sortie sont conservés. |
| 22 | Ne pas confondre validité technique/scientifique | **PASS** | Les textes précisent que les 49/49 contrôles vérifient des invariants instrumentés, pas une hypothèse universelle.
| 23 | Pas de supériorité universelle à partir de quelques tâches | **PASS** | Conclusions limitées à six tâches (cinq binaires et une multiclasse), trois graines d'optimisation et un split chacune.
| 24 | Sources originales non modifiées | **PASS opérationnel** | Extraction dans des espaces de travail dédiés; hash racine vérifié. |
| 25 | Pas d'hypothèse favorable non déclarée | **PASS avec limites explicites** | Centralisation, shards, seuil q90, corruption, identité, données cassées, budget non égalisé et split unique sont signalés. |

## Contrôles finaux de livraison requis

Contrôles finaux de phase 10 consignés dans le journal :

1. Tous les scripts sont syntaxiquement valides (`python -m compileall code`).
2. Le formalisme PDF a été rendu en PNG et inspecté visuellement après la dernière compilation.
3. Tous les résultats sont immuables jusqu'au hash de livraison; les métriques des suppléments sont recalculées sans réentraîner les modèles.
4. Le manifeste SHA couvre chaque fichier livré sauf lui-même; l'archive ZIP est ensuite testée avec `unzip -t`.
5. Le hash SHA-256 de l'archive est livré à côté, et les liens pointent vers les chemins réels.

- Archive ZIP finale testée avec `unzip -t` et extraite dans un répertoire temporaire indépendant; `code/validate_delivery.py` exécuté sur l’extraction. La présence du prompt, du formalisme PDF/TeX, des scripts, des résultats, de la matrice de conformité et de `sites_web_consulte.json` a été vérifiée. Le SHA-256 de l’archive est fourni dans `SHA256SUMS_DELIVERY.txt` à côté de l’archive.
