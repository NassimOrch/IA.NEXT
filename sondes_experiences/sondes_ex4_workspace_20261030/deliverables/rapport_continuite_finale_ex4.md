# Rapport de continuité et d'audit final EX4

**Date :** 30 octobre 2026  
**Workspace :** `sondes_research_workspace_ex4`  
**Dernière campagne exécutée :** v009 — transfert exploratoire Iris

## 1. Point de reprise et règle de non-répétition

La reprise a commencé par la vérification des artefacts déjà présents dans le workspace. Les campagnes v005 et v006 n'ont pas été relancées. Le registre v007 n'a pas été réutilisé comme agrégat homogène : il contient 70 lignes de la campagne initiale et 25 lignes additionnelles micro-MIXA. Les audits filtrés distinguent ces deux blocs. Les 25 runs de sondes micro-MIXA, les 30 MLP et les 50 paires v008 ont été récupérés et réaudités sans nouvel entraînement. Dans v009, les cinq checkpoints adaptatifs Iris déjà terminés ont été restaurés sans réentraînement ; les temps et historiques non enregistrés sont laissés `ND`.

## 2. Vérification du prompt de base

Le fichier `prompt_ex4.json` est un JSON valide de 73 879 octets. Il est identique octet pour octet dans les cinq emplacements de livraison et d'exécution :

- `/mnt/data/prompt_ex4.json`
- `prompt_ex4.json`
- `inputs/prompt_ex4.json`
- `versions/sondes_ex4_v008__2026-10-30/inputs/prompt_ex4.json`
- `versions/sondes_ex4_v009__2026-10-30/inputs/prompt_ex4.json`

SHA-256 commun : `39471af7dabb7ad80a6379b6c2d2cc53a41d8a35af6369c344b82bd1546b36d4`.

Le prompt couvre bien l'objectif P_total, les comparateurs MLP matched/ge4x, les variantes maturation/croissance/RETRO/MIXA, l'hybride micro-MIXA, les partitions, le gel avant test, les mesures de ressources et les livrables. La piste micro-MIXA est définie comme hypothèse reconstructive (branche adaptative micro d4/k8 + branche RBF fixe d4/k8 + mélange égal/gate global/gate conditionnel + ablations branche seule) ; elle n'est pas présentée comme reproduction identique du prototype EX3 absent.

La finalité n'est pas satisfaite : la conformité protocolaire et l'objectif de performance/ressources sont évalués séparément. Les expériences exécutées ne démontrent pas la non-infériorité simultanée de la sonde en accuracy/log-loss et en ressources.

## 3. Résultats expérimentaux consolidés

### Wisconsin développement (v006)

Le ratio de paramètres corrigé du scaler atteint au moins 4x pour les comparaisons ge4x auditées. Aucune des 12 familles ne passe simultanément accuracy, log-loss, temps d'entraînement et latence médiane. Pour d8/k4 croissance, P_total moyen vaut 356, contre 1 448 pour le MLP ge4x (ratio 4,067x) ; accuracy moyenne 97,65 % des deux côtés ; log-loss 0,05952 sonde contre 0,05394 MLP ; fit 0,352 s contre 0,263 s ; latence médiane batch-1 0,07432 ms contre 0,01390 ms.

Wisconsin est historiquement exposé dans EX2/EX3 : ces résultats sont développementaux et ne constituent pas une confirmation indépendante.

### Micro-MIXA Wisconsin (v008)

25 runs de sondes (5 seeds × 5 bras), 30 MLP uniques et 50 comparaisons appariées. Le plus petit ratio ge4x après scaler est 4,01878x. Résultats moyens : adaptive-only P_total=242, accuracy=96,71 %, log-loss=0,07579 ; fixed-only 242, 94,12 %, 0,17291 ; mélange égal 424, 97,18 %, 0,08456 ; gate global 426, 96,94 %, 0,07516 ; gate conditionnel 486, 97,18 %, 0,08707. Les MLP ge4x ont une log-loss de 0,05121–0,05439 et une accuracy de 97,88–98,35 %. Le mélange égal gagne en accuracy mais perd en log-loss par rapport à l'adaptatif seul. Aucun bras ne rattrape le MLP en log-loss.

Le code micro-MIXA n'utilise pas la partition adaptation comme contrôleur, contrairement à un drapeau générique présent dans les données sources v007. Ce drapeau original a été conservé ; l'audit v008 porte une correction séparée attestant la lecture du code. Il n'y a pas de fuite test constatée dans cette campagne.

### Transfert Iris (v009)

Quatre bras (adaptatif seul et trois micro-MIXA), cinq initialisations ; 20 sondes, 40 MLP uniques, 40 paires validation et 60 métriques test après gel. Le test contient 30 observations communes aux cinq graines. Le ratio ge4x minimal est 4,015625x. En test, accuracy sonde/MLP : adaptatif 95,33/96,67 %, mélange égal 96,00/96,67 %, gate global 96,67/96,67 %, gate conditionnel 96,67/96,67 %. Log-loss sonde/MLP : 0,16466/0,09761 ; 0,12062/0,09633 ; 0,14282/0,09331 ; 0,17272/0,09420. Les MLP ont une meilleure log-loss dans les quatre comparaisons.

Les latences batch-1 sonde sont 0,03890 à 0,08966 ms contre 0,01384 à 0,01468 ms pour les MLP. Les trois MIXA entraînés sur Iris ont un fit de 1,34 à 2,28 s contre 0,26 à 0,28 s pour les MLP correspondants. Les temps fit des cinq checkpoints adaptatifs récupérés sont indisponibles et marqués ND. Les cinq initialisations réutilisent les mêmes 30 observations de test ; elles ne constituent pas 150 cas indépendants. Aucun test de non-infériorité formelle n'est revendiqué.

**Réserve d'isolation :** `load_iris()` matérialise le tableau complet ; le partitionnement stratifié lit les labels pour assigner les partitions ; le CSV/NPZ source entier est conservé. Aucun exemple test ne sert au scaler, aux gradients, à l'arrêt, aux métriques ni à la sélection avant gel. L'expérience ne revendique toutefois pas l'isolation mémoire/processus absolue.

## 4. Audit de l'intégrité et des artefacts

### Sources immuables

- `last_sources.zip` : 376 130 193 octets ; SHA-256 `f7226d7bef28145279aeebd074e4838ae5512639e15ed3b7801961a2eaeb0a42` ; 6 membres ; `testzip=null`.
- `sondes_research_workspace_final.zip` : 1 113 membres ; SHA-256 `729a06a8356e3fefd521cb72c3812b96ad36d9efe4f73e4329d112baaca28b26` ; `testzip=null`.
- `sonde_adapt_global_research_final.zip` : 567 membres ; SHA-256 `b49e6f5bd67fb61262dd9fed6a1f4f86c526c6cbe9d7bd2b9c9e1ce0defb3b1a` ; `testzip=null`.
- `sources_ng_adapt_0.zip` : SHA-256 `8fcf82931988a96cdfb1ff5cbe5892142b4b1174385dc87cd9ed0f9e2d7069bb` ; test ZIP passé.
- `debrit_0.txt` et `prompt_ex3.json` ont été copiés en lecture seule dans `inputs/source_recovery/` avec les mêmes tailles et empreintes que les originaux.

### Tests exécutés sur cette reprise

| Bloc | Résultat | Détail |
|---|---|---|
| JSON workspace | PASS | 47 fichiers JSON analysés |
| Copies `prompt_ex4.json` | PASS | 5 copies identiques, SHA-256 commun |
| v005 | PASS | 60 sondes, 85 MLP, 120 paires, 60 comparaisons ge4x |
| v006 | PASS | 60 sondes, 135 MLP, 120 paires, 60 comparaisons ge4x |
| v007 ancien test global | FAIL attendu | le test historique attend 70 lignes, registre réel 95 (70 + 25 add-on) ; voir audit dédié |
| v008 micro-MIXA | PASS filtré | 25 sondes, 30 MLP, 50 paires, test Wisconsin non ouvert |
| v009 Iris | PASS | prédictions/métriques recalculées, checkpoints et ratios vérifiés, test post-gel |

Le FAIL v007 n'est pas masqué ni présenté comme PASS : c'est une incompatibilité du test de comptage ancien face à un registre ajouté. Les audits filtrés séparent les deux campagnes. Aucun signe de corruption des ZIPs sources, des JSON, des prédictions ou des métriques n'a été détecté dans les contrôles exécutés. La présence d'un champ source incorrect et d'un registre mixte est une anomalie de provenance/métadonnées, pas une corruption binaire ; les originaux sont conservés et les corrections sont en sidecar.

## 5. Travaux non terminés et obstacles exacts

1. Workspace EX3 complet, scripts et états EX3 cités dans les débris : absents de l'archive. Les 528 coefficients de `mixa_micro_d4_k8` restent non vérifiables.
2. Banknote Authentication (1 372 lignes, 4 variables) et MAGIC Gamma Telescope (19 020 lignes, 10 variables) : les pages officielles UCI sont accessibles, mais la récupération des archives de données a échoué (erreur de téléchargement/décodage navigateur et résolution DNS côté conteneur). Aucun benchmark n'est revendiqué.
3. Ressources matérielles complètes : CUDA/VRAM et énergie non mesurées ; MACs disponibles seulement comme estimation analytique pour Iris ; RSS partiel au niveau processus ; runtime complet non profilé.
4. Wisconsin est historiquement exposé ; Iris est un transfert exploratoire de petite taille, pas une réplication multi-domaines confirmatoire.
5. La non-infériorité statistique formelle demandée par le prompt n'est pas établie.

## 6. Conclusion de reprise

La reprise a récupéré et audité le travail présent sans réexécuter les campagnes déjà achevées. Elle a ajouté l'analyse micro-MIXA et le transfert Iris, puis vérifié les copies du prompt, les sorties brutes, les prédictions, les ratios, les tests et les empreintes. Le résultat scientifique reste négatif par rapport à l'objectif complet : les sondes réduisent fortement le nombre de paramètres et parfois les MACs analytiques, mais la log-loss et la latence restent moins bonnes que celles des MLP ; les temps de fit sont aussi supérieurs sur les branches MIXA transférées à Iris. Le protocole EX4 est substantiellement exécuté, mais pas intégralement confirmé : deux datasets externes restent indisponibles, des mesures matérielles manquent et la non-infériorité n'est pas démontrée.
