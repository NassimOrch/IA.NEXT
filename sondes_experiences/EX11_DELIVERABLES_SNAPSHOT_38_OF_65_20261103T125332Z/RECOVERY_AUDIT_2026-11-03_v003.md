# EX11 — addendum de continuité, récupération et campagnes retrouvées

Date : 2026-11-03 (UTC). Ce document complète les audits v001 et v002 sans les réécrire.

## 1. Corrections et hiérarchie des états

- `RECOVERY_AUDIT_2026-11-03.md` (v001) est un faux négatif : il concluait à tort que le workspace était vide.
- `RECOVERY_AUDIT_2026-11-03_v002.md` a correctement retrouvé prompt, scripts, splits et D3Q, mais son état expérimental est devenu obsolète après les exécutions ultérieures. Il affirmait que REPLICA/CNG/CNC étaient absents ; des campagnes complètes ou partielles ont ensuite été retrouvées ou lancées.
- Le présent addendum v003 est la source de vérité de continuité à cette date ; les journaux et artefacts bruts restent prioritaires sur tous les résumés.

## 2. Prompt et protocole

Le prompt historique v1.1.4 annoncé précédemment n'a pas été retrouvé comme fichier original. Le fichier livrable est une reconstruction versionnée à partir des formalismes et prompts EX3–EX9 accessibles.

- `prompt_ex11.json` et `PRE_REGISTRATION_EX11.md` sont synchronisés octet pour octet.
- Révision documentaire actuelle : `2.3.1-reconstructed`; spécification scientifique utilisée au démarrage des runs confirmatoires : `2.3.0-reconstructed`.
- Révision 2.3.1 : correction du numéro de version imprimé (2.2.0 → 2.3.1), correction de `revision.key_design` de liste de caractères en chaîne et recalcul du hash. Aucun changement d'hypothèse, dataset, split, seed, métrique, budget, critère d'arrêt ou règle test.
- Audit structurel prompt : 13 contrôles sur 13 réussis (JSON, copie exacte, hash, six phases, règle anti-triche/anti-sabotage directe et indirecte, test scellé, 13 datasets, seeds, branches, exclusion des archives historiques).

## 3. Sources et données

- SHA-256 des quatre sources utilisateur (`last_sources_3.zip`, `datasets_arff.zip`, rapport TEX/PDF) correspond à `INPUT_SHA256.txt`.
- `unzip -t` : aucune erreur CRC sur les deux archives ZIP d'entrée.
- Les 13 fichiers ARFF d'EX11 sont identiques octet pour octet aux entrées de `datasets_arff.zip`.
- 65 splits / 195 CSV train-validation-test sont présents ; le contrôle indépendant vérifie conservation exacte des lignes, multiplicité, typage, séparation des groupes X, hashes et mode `0440` des 65 fichiers test.
- Aucun contenu des archives EX3–EX10 ni `last_sources_3.zip` n'est copié dans EX11. Les sources historiques sont référencées et hashées à l'extérieur du workspace.

## 4. Campagnes disponibles et statuts

### REPLICA-U
- v003 : 65/65 blocs dataset×seed terminés, checkpoints, OOF, prédictions et métriques présents ; l'auditeur indépendant passe. Qualification : exploratoire/non-confirmatoire, car le refit final v003 utilisait `i_fit` au lieu de tout le train extérieur.
- v004 : campagne corrigée avec five-fold OOF, sélection sur partition interne, preprocessing fit uniquement sur `i_fit`, refit final sur tout le train extérieur, C1 routeur seul, T0 sans loss auxiliaire, students 64/32 et 32/16, MLP appariés, GE4X. Au snapshot de cet addendum : **13/65** blocs complets (German Credit 5/5, Spambase 5/5, Tic-Tac-Toe 3/5). L'auditeur `audit_replica_artifacts_v002.py` passe sur tous les rapports complets présents. Le processus est séquentiel et peut poursuivre la campagne ; un état ultérieur doit relire le registre.

### CNG
- v001 : 18 runs (f1/f2, seed 1501) avec checkpoints/configs/predictions et audit 18/18 ; centres initiaux non-KMeans, donc exploratoires.
- v004 : code confirmatoire prêt avec KMeans train-only, mini-batch order apparié et MLP matched/GE4X par candidate ; non exécuté au snapshot. LOO v004 attend les checkpoints canoniques A3 v004.

### CNC
- v002 a échoué à la persistance car le dossier de sortie manquait ; échec journalisé.
- v003 : un run seed1501 terminé, centres directs initialisés aléatoirement ; exploratoire.
- v004 : un run seed1501 terminé, KMeans train-only ; ordre des mini-batches C3/C4 non apparié, donc partiel/non-confirmatoire.
- v005 : comparaison appariée C3/C4, code et runner testés, non exécuté au snapshot.

### Efficacité D1/D2/D3
- Microbenchmark pré-campagne : CPU mono-thread, 30 échauffements, 200 répétitions par batch 1/16/64/256.
- Équivalence D1/D2 : 40/40 cas (10 graines × 4 batchs) ; erreurs max sorties `1.788e-7`, grad entrée `3.725e-9`, grad paramètres `2.980e-8`, seuil `1e-6`.
- D3Q v001 : 160/160 runs, checkpoints/prédictions/configs réconciliés, mais centres non-KMeans et GE4X insuffisant face à D1/D2 ; campagne exploratoire.
- D3Q v004 : code corrigé préparé, non exécuté au snapshot.

## 5. Ressources et limites réelles

- Environnement CPU : AMD EPYC 9V74, CPU-only (`torch 2.10.0+cpu`), 6.24 GB RAM, 3 CPU logiques exposés ; le runner REPLICA fixe un thread PyTorch.
- La campagne REPLICA v004 observe environ 22–25 s par run German Credit, 112–139 s par run Spambase et 49–55 s par run Tic-Tac-Toe ; 13 blocs complets ont pris un peu plus de 15 minutes cumulées au snapshot. La totalité de 65 blocs, puis les autres branches, dépasse un court budget interactif.
- Les campagnes D3Q v001/REPLICA v003 ont des durées potentiellement perturbées par contention antérieure ; elles ne prouvent pas la vitesse relative.
- Le RSS high-water déjà collecté est un pic global de processus, pas une mesure isolée par variante. Aucun compteur énergétique fiable n'est disponible. Énergie et RAM attribuable par modèle sont `NOT_MEASURED`/`NOT_AVAILABLE`.

## 6. Règles de clôture

- Aucun test tabulaire scellé n'a été ouvert ; P4 reste interdite avant P3 complète et gel.
- Tout run absent est `NOT_RUN`; run partiel/interrompu est conservé avec son état ; quota insuffisant est `INCOMPLETE_QUOTA`.
- Tous les résultats défavorables, historiques non conformes, scripts échoués et corrections restent conservés. Aucun score provenant uniquement d'un message n'est promu en résultat.
- Le statut précis doit être recalculé à partir des registres `logs/append_only/*.jsonl` à chaque snapshot. Le présent v003 décrit le snapshot, pas un état permanent.
