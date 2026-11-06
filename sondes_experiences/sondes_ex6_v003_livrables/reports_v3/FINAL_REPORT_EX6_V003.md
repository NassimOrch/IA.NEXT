# Rapport final EX6 — état consolidé v003

**Date :** 31 octobre 2026  
**Statut final :** **INCOMPLET**  
**Prompt :** EX6 révision 1.0.1 — SHA-256 `72744213da2626174e63c45256a6e7a69c6de84c2b810d7a4a94e931c885237c`  
**Campagne additionnelle :** v003, pré-enregistrée avant les runs v003  
**Dataset :** Wisconsin Diagnostic Breast Cancer, split de développement historiquement exposé uniquement.

## 1. Verdict exécutif

Le prompt EX6 a été relu et audité : les 19 sections sont présentes, le JSON est valide et les copies du prompt sont identiques. Toutefois, **le protocole n’est pas exécuté de bout en bout**. La campagne v003 complète les familles homogène/spécialiste, Orchestra input-gated, ablation inter-couches, correcteurs OOF, Replica training-shard et diagnostics de cascade. Les tests externes indépendants, plusieurs architectures/ablations obligatoires, les marges NI, et plusieurs mesures matérielles restent absents.

Le résultat robuste de cette campagne est le suivant : les architectures sondes testées réduisent le nombre de paramètres d’au moins 4× par rapport à leurs MLP-ge4x, mais leurs latences d’inférence et temps de fit sont nettement plus élevés. Les correcteurs OOF ont une log-loss moyenne ponctuellement meilleure que leurs comparateurs sur ce split, mais ce gain est associé à des coûts d’apprentissage et d’inférence beaucoup plus grands et n’est pas une preuve confirmatoire.

**Aucun candidat ne satisfait à ce stade les critères conjoints EX6. Aucun succès global ni non-infériorité ne sont revendiqués.**

## 2. Ce qui a réellement été repris et exécuté

- v001 (pilotes initiaux) reste inchangé ; les quatre pilotes déjà archivés n’ont pas été rejoués.
- v002 conserve l’essai de sélection interrompu par runtime ; il n’est pas compté comme un run achevé ni interprété comme un résultat.
- v003 a introduit un addendum de continuation pré-enregistré : min-delta validation `0,0005`, patience 20, réduction LR aux stades de stagnation 7/14, checkpoints atomiques par époque et reprise déterministe ; même critère de plateau pour candidate et MLP.
- Sélection imbriquée interne : 7 variantes homogènes et 49 candidates spécialistes ; choix gelés avant les runs v003.
- Modèles v003 achevés : 20 piles (4 familles × 5 graines), 10 correcteurs OOF (2 familles × 5 graines), 5 Replica training-shards, plus diagnostics de cascade/préfixe et contrôles calcul noyau/optimiseur.
- Les 105 fichiers de prédictions audités ont été recalculés ; écart métrique maximal vs enregistrement : `0`.

## 3. Résultats v003 — qualité et complexité

Les lignes ci-dessous sont des moyennes sur cinq graines, une validation unique de 85 exemples déjà exposée historiquement. `P_total` inclut les paramètres entraînables, les états fixes/buffers et les 60 coefficients de préprocesseur. Le ratio minimal audité sur les 35 candidates v003 est `4,00047`.

| Architecture | P_total candidate | P_total MLP-ge4x | Ratio min. | Accuracy candidate | Accuracy MLP-ge4x | Log-loss candidate | Log-loss MLP-ge4x |
|---|---:|---:|---:|---:|---:|---:|---:|
| Emplica homogène sélectionnée | 6,705 | 26,825 | 4.0007× | 98.12% | 98.82% | 0.05968 | 0.04566 |
| Emplica spécialiste par couche | 7,340 | 29,366 | 4.0008× | 97.88% | 98.82% | 0.04944 | 0.04891 |
| Orchestra — gate externe conditionné par X | 7,227 | 28,937 | 4.0040× | 97.65% | 98.82% | 0.06299 | 0.04691 |
| Orchestra — ablation sans messages inter-couches | 6,967 | 27,881 | 4.0019× | 97.88% | 98.82% | 0.05995 | 0.04563 |
| Emplica + correcteur OOF | 8,295 | 33,194 | 4.0017× | 98.59% | 98.82% | 0.03637 | 0.04675 |
| Orchestra + correcteur OOF | 8,512 | 34,052 | 4.0005× | 98.12% | 98.82% | 0.03982 | 0.04733 |

### Lecture des résultats qualité

- Emplica spécialiste est proche du MLP-ge4x en log-loss (0,04944 vs 0,04891), mais son accuracy moyenne est plus basse (97,88% vs 98,82%).
- Emplica/Orchestra avec correcteur OOF ont des log-loss ponctuelles moyennes plus faibles que leur MLP-ge4x (0,03637 vs 0,04675 et 0,03982 vs 0,04733). L’accuracy reste légèrement inférieure, l’intervalle bootstrap log-loss inclut zéro, et ce split ne constitue pas une confirmation indépendante.
- Les variantes Emplica homogène et Orchestra sans communication présentent une log-loss moins bonne que le MLP-ge4x.

## 4. Temps d’entraînement et inférence

| Architecture | Fit candidate (s) | Fit MLP-ge4x (s) | Ralentissement fit | p50 batch-1 candidate (ms) | p50 MLP-ge4x (ms) | Ralentissement inférence | p99 batch-1 candidate (ms) | p99 MLP-ge4x (ms) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Emplica homogène sélectionnée | 2.428 | 0.212 | 11.5× | 1.632 | 0.030 | 54.1× | 2.514 | 0.106 |
| Emplica spécialiste par couche | 2.239 | 0.226 | 10.1× | 1.634 | 0.030 | 55.3× | 2.458 | 0.086 |
| Orchestra — gate externe conditionné par X | 2.379 | 0.231 | 10.3× | 1.713 | 0.029 | 59.5× | 3.084 | 0.123 |
| Orchestra — ablation sans messages inter-couches | 2.180 | 0.241 | 9.1× | 1.690 | 0.030 | 56.8× | 3.013 | 0.112 |
| Emplica + correcteur OOF | 11.818 | 0.263 | 45.7× | 1.856 | 0.031 | 59.9× | 3.586 | 0.098 |
| Orchestra + correcteur OOF | 10.677 | 0.260 | 41.3× | 1.871 | 0.027 | 70.4× | 3.475 | 0.098 |

Les temps de fit des piles sont nettement supérieurs à ceux des MLP-ge4x. Les bras OOF incluent la génération des prédictions cross-fitted et le correcteur ; ils représentent donc le coût du pipeline d’apprentissage complet, et non le seul fit final. Les mesures batchées complètes (1/16/64/256), les quantiles p50/p95/p99, throughput et distributions brutes sont conservées dans `EX6_V003_LATENCY_BATCHES.csv` et les JSON bruts.

**Attention à la portée du mot « ressource » :** les bytes des checkpoints sont enregistrés, mais ils ne sont pas une mesure de RAM de pointe ou d’activation. RSS est jugé non fiable pour les comparaisons inter-modèles à cause du cache/allocateur PyTorch dans le même processus. VRAM/activation/énergie sont `NON MESURÉ`. Les MAC sont des estimations analytiques, pas des compteurs hardware.

## 5. Résultats propres à Replica

Deux sens de « partage du calcul » ont été séparés :

1. **Partition noyaux/RBF avec clone exact gelé** : l’encodeur intermédiaire est calculé une fois, puis les deux branches évaluent chacune 4/8 centres et fusionnent les logits. La parité est très bonne (erreur absolue maximale `4,77e-7`). Le coût complet passe de 242 à 424 paramètres. La latence CPU batch-1 p50 passe de 0,0342 ms (baseline) à 0,0656 ms en série et 0,5987 ms en parallèle. En batch 256 : 0,0698 ms baseline, 0,1094 ms série, 0,6507 ms parallèle. Le clone n’apporte pas de gain de vitesse sur ce matériel. Le contrôle parallèle sans clone est lui aussi lent : le parallélisme CPU/ordonnancement domine le calcul.
2. **Training-shard Replica** : la copie est gelée et bit-à-bit inchangée ; seul le head résiduel primaire est optimisé. 2 260 paramètres pour la paire vs MLP-ge4x 9 071 (ratio 4,014). Le temps split-série est ~0,268 s et split-parallèle ~0,293 s, contre ~0,197 s MLP. Cette étude est limitée : la sonde primaire source n’est pas réentraînée de bout en bout et ses experts sont gelés. Il ne faut pas présenter ce run comme une victoire d’entraînement Replica.

Le contrôle de gradient est explicite : un clone gelé ne fournit pas spontanément de gradient au primaire. Les variantes de partition batch n’ont pas été implémentées.

## 6. Emplica Orchestra : communication, OOF et cascade

La pile avec gate externe conditionné par `X` et l’ablation sans messages inter-couches ont toutes deux été évaluées. Le gain de log-loss ponctuel des correcteurs OOF s’accompagne d’un coût de pipeline : ~10,68–11,82 s, contre ~0,26 s pour MLP-ge4x. L’inférence p50 batch-1 reste environ 60–70× plus lente que le MLP.

Les diagnostics préfixe montrent que les premières couches seules ne fournissent généralement pas la qualité de la pile complète. Les seuils 0,90/0,95 pré-déclarés peuvent interrompre trop tôt et dégrader fortement accuracy/log-loss ; le coût du gate et des chemins séquentiels peut même dépasser celui du modèle complet. Aucun gain global de cascade n’est démontré.

## 7. Statistiques : ce qu’elles permettent et ne permettent pas

Bootstrap apparié post-hoc : 10 000 réplications, 85 exemples de validation, cinq graines, seed bootstrap 62031. Il n’est pas ajusté à la multiplicité, et la validation est historiquement exposée. Par exemple, pour Emplica OOF, différence moyenne candidate−MLP de log-loss = −0,01038, IC 95% [−0,05569 ; +0,01905]. L’intervalle contient zéro. Pour Orchestra OOF : −0,00751, IC [−0,06105 ; +0,03035]. Ces intervalles sont exploratoires ; ils n’établissent pas la non-infériorité.

## 8. Audit d’intégrité et absence de corruption détectée

- Archive d’origine `last_sources.zip` : 457 109 554 octets, SHA-256 `5f7a86cb3875f97324f75c46e379b6639673dfe9cc265a173fa8749f1be0f8eb`, contrôle ZIP CRC passé.
- 5 ZIP imbriqués principaux et 12 ZIP historiques internes ont passé les contrôles CRC documentés dans `checksums/source_manifest.json`.
- Copies du prompt EX6 (racine workspace, version v003, `inputs/`) : même SHA-256 `{sha}`.
- Dataset NPZ : SHA-256 `93f7a5f6ef8a5daa090bf83f4a2169a9857893f4aca4b700f7b74566b14be1da`, formes Xtr (341×30), Xva (85×30), Xad (57×30), aucune matrice/label test dans le NPZ.
- 35 comptes de paramètres reconstruits depuis checkpoints ; aucun delta de compte. Ratio minimum : 4,0004699.
- 105 prédictions recalculées depuis les probabilités archivées ; écart maximal des métriques recalculées vs enregistrées : 0,0.
- Aucun fichier checkpoint temporaire `.pt.tmp` résiduel détecté dans `results_v3`. Les résultats v001/v002 n’ont pas été écrasés.

L’audit `PASS_WITH_LIMITATIONS` signifie que les artefacts audités sont cohérents ; il ne prouve pas une absence absolue de corruption dans chaque source brute historique ni une isolation parfaite du test. Le loader sklearn matérialise le dataset complet, même si les tableaux test ne sont pas extraits/serialisés/alimentés aux modèles v003 ; la limite est documentée et le domaine reste développement seulement.

## 9. Matrice de verdict par idée

| Idée | Paramètres ≤ MLP/4 | Qualité | Ressources / vitesse | Verdict actuel |
|---|---|---|---|---|
| Replica | Oui pour les bras contrôlés | Non équivalente sur ce split pour le train-shard | Aucune accélération ; split kernel série/parallèle plus lent | **ÉCHEC SUR CRITÈRE MESURÉ / PARTIELLEMENT ÉTUDIÉ** |
| Emplica simple | Oui (ratio ≥4) | Spécialiste proche du MLP en loss ; OOF loss ponctuelle meilleure | Fit ~10× plus lent ; inférence ~55–60× plus lente | **ÉCHEC SUR CRITÈRE MESURÉ** |
| Emplica Orchestra | Oui (ratio ≥4) | OOF loss ponctuelle meilleure, non confirmatoire | Fit ~41× plus lent ; inférence ~59–70× plus lente | **ÉCHEC SUR CRITÈRE MESURÉ** |
| Généralisation externe | — | Non évaluée | Non évaluée | **INCOMPLET** |

Ce tableau ne transforme pas des dimensions non mesurées en échec mesuré : il indique que l’objectif conjoint EX6 n’est pas démontré et que la vitesse, elle, est défavorablement mesurée sur le matériel testé.

## 10. Liste des non-mesurés / non-exécutés / non-vérifiés

**NON MESURÉ :** VRAM, mémoire d’activation maximale, énergie/joules, RSS comparable inter-modèles, compteurs hardware de FLOP/MAC.

**NON EXÉCUTÉ :** Replica batch sharding dédié ; apprentissage complet des sondes de base avec règle de gradient de partage non triviale ; Orchestra static-global et Orchestra local-global sans externe comme bras indépendants ; Orchestra specialist dédié ; contrôles mono-couche/budget de paramètres strictement apparié et ablations systématiques par couche ; domaine externe vierge et test confirmatoire gelé ; RETRO complet intégré aux nouvelles couches.

**NON VÉRIFIÉ :** généralisation hors Wisconsin ; non-infériorité ; effet multi-domaines ; reproductibilité exacte au niveau des cellules interactives historiques v001 ; bénéfice d’un déploiement sur GPU ou autre matériel ; avantage énergétique.

## 11. Livrables et emplacement

- Prompt final : `prompt_ex6.json` à la racine du workspace, copie identique dans la version et `inputs/`.
- Audit des sources : `reports/AUDIT_SOURCES_EX6.md`.
- Audit structurel du prompt : `reports/AUDIT_PROMPT_EX6.md`.
- Conformité d’exécution section par section : `reports_v3/CONFORMITE_PROMPT_EX6_V003.md`.
- Pré-enregistrement de continuation v003 : `configs/continuation_preregistration_v003.json`.
- Runs/prédictions/poids : `results_v3/raw/`, `results_v3/models/`, `results_v3/deployment/`.
- Comparaisons / latences / paramètres / bootstrap / cascade / opérations / front Pareto exploratoire : `results_v3/metrics/`.
- Front Pareto exploratoire : `reports_v3/FRONT_PARETO_EXPLORATOIRE_V003.md` et `results_v3/metrics/EX6_V003_PARETO_EXPLORATORY.csv`.
- Scripts et snapshots : `src/`.
- Audit indépendant : `reports_v3/AUDIT_INDEPENDANT_V003.json`.
- Audit final d’intégrité : `reports_v3/AUDIT_INTEGRITE_FINALE_V003.md`.
- Manifeste de hashes : `checksums/MANIFEST_SHA256_V003.txt`.

## 12. Verdict final

**INCOMPLET.** Le ratio de paramètres est atteint sur les candidates v003, mais la rapidité n’est pas atteinte : les piles sont beaucoup plus lentes que les MLP-ge4x. Quelques correcteurs OOF ont un meilleur point estimate de log-loss sur la validation historique, sans preuve statistique de non-infériorité/supériorité et avec une pénalité de calcul importante. Des dimensions matérielles et de généralisation sont non mesurées ou non exécutées. La règle rouge interdit de transformer ces résultats partiels en succès ou en échec total préconçu.
