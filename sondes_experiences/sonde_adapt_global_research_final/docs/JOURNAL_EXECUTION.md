# Journal d'exécution et décisions de reprise

**Date de campagne indiquée par l'environnement :** 2026-10-29.  
**Archive source SHA-256 :** `8fcf82931988a96cdfb1ff5cbe5892142b4b1174385dc87cd9ed0f9e2d7069bb`.

| Étape | Opération | Résultat / trace |
|---|---|---|
| 0.1 | Vérification du ZIP source | `zipfile.testzip` réussi; 26 entrées d'archive; copie/source inchangée. |
| 0.2 | Extraction récursive, chemins et intégrité | 80 archives imbriquées; toutes intègres; 0 chemin dangereux et 0 symlink. `logs/recursive_archives.jsonl`. |
| 0.3 | Inventaire et source copies | Manifestes SHA-256 récursifs dans `results/source_audit/`; 14 970 entrées entre deux vues d’extraction (copies en double comptées). Copies prioritaires dans `source_copies/`. |
| 0.4 | Diagnostic environnement | Python 3.13.5, CPU PyTorch, latexmk; absence de décodeur Parquet documentée. |
| 1.1 | Replay « two moons » original | CSV/JSON nouveaux identiques octet par octet aux sorties de référence; logs `base_reproduction.*`. |
| 1.2 | Validateur v1.2 | `PASS_WITH_LIMITATIONS`, 16/16; code 0. |
| 1.3 | Validateur formalisme observation | PDF de 109 pages/structure vérifiés par validateur source; code 0. |
| 1.4 | Manifeste et tests v2/v3.1 | Manifestes v2 417/417 et v3.1 propre 794/794; v2 117 tests + 10 sous-tests; v3.1 66 tests et non-régression V1 65 tests. Les premiers échecs de contexte (PYTHONPATH/manifeste avec `.unpacked`) conservés. |
| 2 | Formel global, preuves conditionnelles et références | `.tex` compilé en PDF 7 pages, rendu contrôlé après inspection des pages initiale, preuve et références. Pas de conclusion universelle. |
| 3 | Préenregistrement des tâches/mesures/conditions | `docs/PROTOCOLE_PREENREGISTRE.md`; amendement explicite de l'état de l'optimiseur reconstruction. |
| 4 | Smoke tests A–K | Scripts valident leur exécution rapide; métriques 8 epochs explicitement exclues des résultats. |
| 5 | Benchmark principal par lots | Un run global a dépassé la limite shell; interruption journalisée; les cinq tâches ont été relancées séparément. 33 runs/tâche, 165 au total, 0 erreur finale. |
| 6 | Ablation coordinateur | 60 runs; poids gelés vs local exactement égaux sur 2 673 prédictions appariées. |
| 7 | Robustesse boucle | 120 lignes, 16 200 empreintes, 0 erreurs; labels manquants, labels bruités/trompeurs, shift et updates désactivés. |
| 7.5 | Audit d'agrégation FBR supplémentaire | Le premier manifeste consolidé indiquait une graine demandée mais fusionnait des chunks de trois graines. Résultats antérieurs quarantinés avec SHA; 15 couples recalculés en espace neuf, 390 métriques, 54 000 événements, zéro erreur. |
| 8 | Reconstruction | 148 lignes de métriques, 2 880 événements d'empreinte; identity, RBF/local/global, activation, bottleneck, MLP AE et loop. Comptage paramètres corrigé puis vérifié. |
| 9 | Audit indépendant | 35/43 contrôles passés avant ajout de l’audit de la boucle de reconstruction; le script final ajoute des contrôles de complétude, intégrité des empreintes et équivalence du contrôle sans mise à jour. Voir les nouveaux nombres dans `results/independent_audit.json/.md`. |
| 10 | Livraison | Archive créée après le gel documentaire, contrôlée par `unzip -t`; inventaire SHA-256 interne et digest du ZIP externe. |

## Échecs conservés et reprise

- Premier outil Python visible : rate limit de l'outil, distinct d'une panne Python; le shell a permis de poursuivre.
- Run principal monolithique : interrompu par limite d'appel. Aucune métrique de cette tentative n'a été traitée comme résultat final; reprise par tâche.
- Tests v2/v3.1 : échecs initiaux d'import causés par chemin d'import; relances documentées avec `PYTHONPATH` correct.
- Extraction non propre de v3 contenant archives internes dépliées : manifeste supplémentaire; contrôle repris dans un répertoire propre depuis le ZIP source.
- Première version du compte de paramètres reconstruction : erreur détectée pendant l'audit et corrigée, valeurs recalculées et résumées dans le rapport.

Aucun contrôle d'accès n'a été contourné. Aucune source d'origine n'a été écrasée. Le travail est limité au périmètre et aux ressources disponibles; les limites de la campagne figurent dans `LIMITES_ET_INCERTITUDES.md`.

| 9.1 | Inventaire final d’audit source | 14 970 entrées hachées, 2 045 chemins Python analysés (0 erreur AST), 106 PDF avec signature correcte; anomalies JSON/JSONL conservées. |
| 9.2 | Compilation/lint final | `compileall` code: exit 0; smoke test A–K à 8 epochs: exécution OK, exclu des résultats scientifiques. |


## Reprise de finalisation — 29 octobre 2026

- Repris à partir des checkpoints existants : aucune campagne de classification, d'ablation ou de reconstruction historique complète n'a été relancée.
- Ajouté un audit indépendant dédié à RBF-R1 : checkpoints de 6 paires, 162 lignes métriques, 23 040 événements; règles pour missingness, décision des quatre politiques, threshold de validation et recomputation des moyennes/écarts-types. Première version d'audit a correctement échoué sur un invariant trop strict pour les événements sans observation; condition corrigée pour exiger au contraire l'absence du résidu et de l'anomalie quand une mesure manque. L'audit intermédiaire corrigé passait 40/40; après ajout des trois derniers invariants de cohérence RBF-R1, la dernière exécution v4 passe 43/43.
- Recompilé le formalisme LaTeX (7 pages A4) puis rendu les 7 pages en PNG; contact sheet et page 4 inspectées visuellement. Une ligne de borne de reconstruction a été mise en display math pour éviter un débordement inutile.
- Documentation mise à jour pour le résultat défavorable RBF-R1, l'état des phases et le crosswalk complet du prompt. La phase 10 a été clôturée après la validation de l’archive ZIP finale, le contrôle de son extraction et la vérification des SHA-256.


## Clôture finale v5 — 2026-10-29

- Ajout du contrôle de provenance web dans l’audit indépendant : 44 contrôles instrumentés réussis sur 44, dont `website_consultation_ledger_complete_and_caveated`.
- Création/vérification de `sites_web_consulte.json` : 33 URL uniques, 16 requêtes documentées, motif et disposition renseignés pour chaque site. La provenance historique non récupérable est signalée; aucune URL manquante n’a été inventée.
- Aucun entraînement ou benchmark existant n’a été relancé pendant cette clôture documentaire; seuls les auditeurs, le validateur de livraison et les contrôles d’intégrité sont exécutés de nouveau.
- Les contrôles de clôture ont été exécutés sur une archive candidate, puis sont répétables après gel des rapports : test ZIP sans erreur, comparaison exacte des membres de l’archive au manifeste (546 fichiers manifestés plus le manifeste SHA lui-même; aucune entrée manquante ni supplémentaire), extraction indépendante et validateur 8/8 PASS. Le hash externe est recalculé à partir du ZIP final et reste en dehors de l’archive. Les phases 1, 4 et 8 restent partiellement couvertes selon `ETAT_DES_PHASES.md`; le succès technique ne les transforme pas en phases scientifiques intégralement satisfaites.


## Clôture de livraison — 29 octobre 2026

- Un contrôle postérieur aux dernières modifications a détecté des SHA-256 obsolètes dans le manifeste; l’archive candidate n’a pas été remise comme finale. Les données structurées étaient lisibles, mais cette divergence empêchait une validation complète.
- L’audit indépendant v6 a d’abord échoué à 48/49 sur l’isolation du flux d’empreintes digits10 (`logs/independent_audit_v6.*` conservés). Après correction du contrôle, la reprise finale `logs/independent_audit_final_release.*` a terminé avec **49/49**, code de sortie **0**. Cette validation couvre des invariants instrumentés, pas une preuve de généralité scientifique.
- Le PDF formel final a été inspecté via `pdfinfo`, extrait avec `pdftotext` et rendu en sept pages A4; les pages 1 et 7 ont été visualisées et ne présentent pas de texte coupé ou de glyphes cassés.
- `sites_web_consulte.json` a été mis à jour avec les requêtes de vérification finale, 40 URL uniques et 28 requêtes documentées. Les identifiants de résultats des anciennes sessions ont été retirés lorsqu’ils ne pouvaient pas être associés de façon fiable; URL, motif et disposition restent la trace durable.
- Clôture technique : manifeste SHA-256 régénéré depuis l’état stabilisé; ZIP reconstruit sans se contenir lui-même; test CRC et extraction dans un répertoire neuf; validateur relancé sur cette extraction. Les valeurs exactes des contrôles, du nombre de fichiers, de la taille et du SHA-256 sont consignées dans `VALIDATION_LIVRAISON_FINALE.md` fourni à côté de l’archive.

## Clôture finale v6 — après mise à jour de la provenance web

- Réexécuté uniquement l'audit indépendant après les corrections documentaires et la consolidation de `sites_web_consulte.json`; aucune campagne de modèle n'a été relancée. Résultat : **49/49 contrôles instrumentés, 0 échec**, code de sortie 0, stderr vide.
- Le registre web final comporte **40 URL uniques et 28 requêtes de recherche identifiées**, avec motif et disposition; les entrées ajoutées lors du dernier contrôle distinguent explicitement les pages éditeur, variantes de résumé, liens PDF indexés et copie secondaire. Les URL historiques irrécupérables ne sont pas inventées.
- Le contrôle de livraison préliminaire a détecté les empreintes SHA périmées causées par les dernières modifications documentaires; il a échoué sur le manifeste seul (7/8), les sept autres contrôles — y compris l'analyse de 116 JSON, 1 JSONL et 165 CSV — réussissant. Le ZIP candidat antérieur a été invalidé et ne constitue pas la livraison finale.
- Le désaccord de somme de probabilité digits10 (maximum `2,40e-7`) provient de l'export softmax float32. Les prédictions brutes n'ont pas été éditées; l'auditeur renormalise seulement une copie en mémoire pour recalculer les métriques, avec écart maximal `2,45e-11`.
- Une note de précision dupliquée a été supprimée du rapport des résultats; aucune donnée expérimentale n'a été modifiée. Les rapports canoniques sont synchronisés avec les copies prévues dans `docs/`.
- **La vérification technique finale n'est déclarée terminée qu'après** régénération du manifeste depuis l'arborescence stabilisée, reconstruction du ZIP, test CRC, comparaison exacte des membres et empreintes, extraction indépendante et réussite des huit contrôles sur cette extraction. Le rapport externe `VALIDATION_LIVRAISON_FINALE.md` publie le digest du ZIP final.
- Les phases scientifiques 1, 4 et 8 restent partielles : la clôture technique ne vaut ni rejeu universel de toutes les anciennes expériences, ni validation de toutes les boucles pour toutes les tâches, ni égalisation des FLOPs/RSS. Les données source tronquées/doublonnées restent signalées et non réparées silencieusement.
