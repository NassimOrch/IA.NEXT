# Conformité du prompt EX7 — état consolidé V002

## Héritage EX6

Le champ `prompt` de `prompt_ex7.json` commence par le texte intégral EX6, caractère par caractère (`prompt_ex7.startswith(prompt_ex6) = true`). Les 19 sections héritées, y compris règles rouges, interdictions de fuite, anti-triche/anti-sabotage, règles de gel et de conservation des échecs, sont conservées sans modification.

## Matrice EX7 A–L

| Section | Exigence / contrôle | État V002 | Preuve / limite |
|---|---|---|---|
| A | Portée, héritage, objectif de calcul complet | PASS | Prompt parent identique ; résultats analysés séparément en paramètres, temps, qualité et ressources. |
| B | Audit lignée micro-MIXA → OOF → Emplica/Orchestra | PASS AVEC LIMITES | `LINEAGE_MAP_EX7.md`, audit des scripts et résultats ; historique volumineux ciblé, pas relecture binaire manuelle exhaustive de chaque archive. |
| C | Hypothèses falsifiables, seuils qualité, comparaison appariée | PARTIEL | Comparaisons par graine et agrégats ; marge de développement documentée ; pas d'IC bootstrap appariés systématiques ni validation populationnelle. |
| D | REF/CAL-LOGIT/LIN-CONTEXT/RBF-LITE/DISTILLED/NO-CORR, coûts | PASS EXÉCUTION, MESURES PARTIELLES | 50/50 correcteurs légers, 20/20 distillation et base seule ; Brier/ECE/AUC et mémoire/latence correcteur séparée incomplets pour tous les bras. |
| D | Cross-fitting 2/3/5 plis sans fuite | PASS EXÉCUTION | 3-fold référence, 2-fold 10/10, 5-fold 10/10 ; 10-fold/repeats non exécutés (optionnels, coût élevé). Les 2/5-fold ne sont pas non-infériorité confirmée. |
| E | Vectorisation et parité | PASS PARITÉ, PERF PARTIELLE | Écart max 4.77e-7 ; gains dépendants des batchs. |
| E | Processus/threading CPU | PASS TEST NÉGATIF | 27.34 s parallèle folds vs 16.11 s séquentiel ; threads inter-couches plus lents. |
| E | GPU / ONNX / compile / export | PARTIEL / INDISPONIBLE | CUDA absent, ONNX absent, compile non exécuté ; TorchScript parité exacte et amélioration vs eager, mais pas vs MLP. |
| E | Cache, mutualisation, activation / communication | PARTIEL | Artefacts OOF/logits et sorties d'étage réutilisés dans les runs ; coût mémoire, bytes de communication et économies end-to-end non profilés intégralement. |
| E | Quantification, low-rank, centre-sharing, pruning | PASS EXPÉRIMENTAL PARTIEL | qint8 testée mais plus lente ; low-rank/centre-sharing testés (60/60), qualité non uniformément conservée ; pruning non exécuté distinctement. |
| F | Variantes de la lignée, capacités/profondeurs, correcteurs | PASS EXÉCUTION AVEC RÉSERVES | 60/60 correcteurs structurels ; 25/25 capacité ; balayage historique micro-MIXA réutilisé ; les nouveaux bras restent exploratoires. |
| G | Orchestra Org originale récursive | PASS IMPLÉMENTATION ET EXÉCUTION | 7×5, `pi` interne, `rho` externe, objectifs séparés/détachés, cascade, modulation LR, 5/5 graines ; audit dédié. |
| G | Ablations causales et communication | PASS EXÉCUTION, MESURE PARTIELLE | 6×5=30 ablations ; 5/5 couches indépendantes ; mesure bytes/communication et temps de synchronisation pas exhaustive. |
| H | Confirmation externe intègre | PASS DÉCISION D'INTÉGRITÉ | Aucune donnée existante n'est déclarée vierge ; aucun test externe ouvert ; validation externe non établie. |
| I | Coûts OOF complets, mémoire, énergie | PARTIEL | Temps OOF+base+correcteur reconstruit pour plusieurs bras ; RSS contaminée par allocateur/cache, mémoire activation/DRAM/énergie non mesurée de façon fiable. |
| J | Version, scripts, checkpoints, données, rapports, hashes, archive | PASS V002 | Snapshot complet, manifestes SHA-256, contrôle de tous fichiers et ZIP CRC/hash. |
| K | Séquence complète, audit adversarial, livraison | PASS AVEC LIMITES | Séquence suivie ; aucune fuite identifiée ; critères de mesure non exécutables déclarés, aucun score confirmatoire externe. |
| L | Verdict multidimensionnel sans succès global indu | PASS | Verdict séparé ci-dessous ; aucun succès global revendiqué. |

## Contrôles d'intégrité V002

- Données de développement : `Xtr` 341×30, `Xva` 85×30, `Xad` 57×30 ; labels et scaler dimensionnés/finis ; SHA-256 du fichier NPZ de données `93f7a5f6ef8a5daa090bf83f4a2169a9857893f4aca4b700f7b74566b14be1da`.
- OOF récursif : cinq graines ; trois folds par graine ; couverture exacte de chaque ligne train une fois ; index folds et logits vérifiés.
- Audit dédié : 5 entraînements racine, 5 campagnes OOF, 15 fits fold, 15 correcteurs récursifs ; 25 capacités et 60 correcteurs structurels ; aucun avertissement/erreur dans l'audit machine.
- Analyse de l'ensemble du workspace source v001 : 626 JSON, 54 CSV, 70 NPY, 6 NPZ, 468 `.pt` (checkpoints et exports), 38 scripts Python ; parsing/chargement effectué sans erreur. Deux avertissements PyTorch de compatibilité/TypedStorage sont non bloquants.
- Archive V001 antérieure : CRC valide mais 306 fichiers présents dans le workspace n'étaient pas inclus dans cette archive ; V002 corrige cette omission et est construite depuis le snapshot complet réconcilié.

## Verdict EX7

**DÉVELOPPEMENT UNIQUEMENT — VALIDATION EXTERNE NON ÉTABLIE — SUCCÈS GLOBAL NON DÉMONTRÉ.**

Les branches d'expérimentation prévues sur CPU et Wisconsin sont exécutées, notamment la récursion originale et les essais `centers_k4`. Toutefois, les réductions de paramètres n'ont pas créé d'accélération globale : les pipelines OOF restent largement plus lents que les MLP ; les parallélismes testés ralentissent sur le CPU disponible ; l'énergie et la mémoire de pointe ne sont pas mesurées de façon fiable ; aucune donnée externe vierge n'est disponible. Le prompt est respecté dans sa règle de transparence : les éléments non mesurés/indisponibles restent explicitement PARTIELS ou NON EXÉCUTÉS, pas convertis en réussites.
