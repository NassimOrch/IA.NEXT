# Tableau de conformité EX5

| Exigence | Statut | Preuve / limite |
|---|---|---|
| Lecture intégrale EX3/EX4/EX5 et cohérence des règles | **RESPECTÉ** | Prompts archivés sous inputs/reference_prompts ; prompt actif v1.1 et config v001. |
| Reprise EX4 sans réentraîner les campagnes validées | **RESPECTÉ** | audit_ex4_reuse.log ; sources EX4 référencées/hashées. |
| Pré-enregistrement, versionnement et addenda append-only | **RESPECTÉ** | configs/EX5_v001_campaign.json et cinq addenda ; rapports/ PRE_REGISTRATION_EX5.md. |
| RETRO post-déclenchement et comparaison pré/post | **RESPECTÉ** | results/raw/retro_runs.jsonl ; results/processed/retro_factorial_summary.csv ; meilleurs post-activation conservés. |
| Adam, moments, gel/dégel strict | **RESPECTÉ** | retro_thaw_v2_runs.jsonl : 20/20 gels stricts ; tests/adam_freeze_semantics.py. |
| Ablation alpha/beta et interaction | **RESPECTÉ** | 12 calendriers/contrôles × cinq graines ; rapport RETRO. |
| Balayage proportions fixe/adaptative à budget constant | **RESPECTÉ** | A4/F0→A0/F4 à P_total 788, cinq seeds ; mixa_proportions_runs.jsonl. |
| Portes globales/conditionnelles et gates gelés/conjoints | **RESPECTÉ** | mixa_gate_refine_runs.jsonl et comparateurs MLP. |
| Optimisation géométrique micro-MIXA | **PARTIEL** | cinq géométries + cinq gate×géométries ; pas d’optimum global ni recherche illimitée démontrée. |
| Alternance A↔B et correcteur résiduel | **RESPECTÉ** | 25 ablations initiales + cinq runs stricts ; 2 cycles complets sans progrès ; gel bitwise. |
| Deux niveaux Q-only X puis réponse supervisée Y | **RESPECTÉ** | 15 runs topologies, 2 reprises Q-only harmonisées ; forward(x) ; tests de cloisonnement. |
| Résidu OOF à deux étages | **RESPECTÉ** | 10 runs, 5-fold OOF; prédictions des lignes hors-fold. |
| Comparaisons MLP matched/ge4x par candidate, seed, dataset | **RESPECTÉ** | mlp_comparator_mapping_all_candidates.csv ; ge4x_ratio_by_candidate_seed.csv ; min >4. |
| Marge formelle de non-infériorité pré-enregistrée | **NON_RESPECTÉ** | Aucune marge delta_accuracy/delta_log_loss numérique n’a été pré-enregistrée ; pas de conclusion NI. |
| Intervalles de confiance/bootstrap/permutation, multiplicité | **PARTIEL** | moyennes/écarts-types sur cinq seeds ; pas d’IC appariés, bootstrap/permutation ni correction multiplicités. |
| Métriques par classe/confusion matrices/calibration complètes | **PARTIEL** | Accuracy, log-loss, macro-F1, balanced accuracy, ECE, Brier/ROC-AUC quand définies ; matrices de confusion/sous-groupes non livrées partout. |
| Ressources : paramètres, temps, batch latence, RSS, taille fichier | **PARTIEL** | mesurées dans plusieurs registres ; pas uniformément sur tous les bras. |
| MACs/FLOPs entraînement backward/step | **NON_MESURÉ** | Seuls MACs analytiques du forward sont présents pour plusieurs bras. |
| Énergie | **NON_MESURÉ** | Aucun wattmètre/instrument fiable. |
| VRAM | **NON_MESURÉ** | CPU-only, CUDA non disponible. |
| Règle rouge performance+ressources | **NON_RESPECTÉ** | Aucune sonde n’égale simultanément MLP en accuracy/log-loss et toutes dimensions mesurables ; latence et/ou coût entraînement dépassent. |
| Transferts externes Wine/Digits label-blind | **RESPECTÉ** | Split test non stratifié sans lecture des features/labels test ; freeze manifest v3 ; résultats descriptifs. |
| Banknote/MAGIC | **BLOQUÉ** | CSV vérifiables via UCI/OpenML/DataHub mais téléchargement échoue par DNS dans conteneur et web ne sert pas text/csv. |
| Iris nouveau transfert EX5 | **NON_RESPECTÉ** | Iris a déjà été utilisé dans EX4 v009 ; prompt l’exclut comme test vierge. |
| Séparation stricte test pour v3 | **RESPECTÉ** | FROZEN_BEFORE_TEST_FEATURE_OR_LABEL_ACCESS ; indices test choisis sans valeurs X/Y. |
| Anomalie registres v3 | **PARTIEL** | 36 anciens pointeurs non uniques conservés et explicitement remplacés par sidecars canoniques corrigés. |
| Audit données/checkpoints/predictions/métriques | **RESPECTÉ** | 1148 JSON, 32 JSONL/829 lignes, 532 checkpoint refs, 495 refs canoniques prédiction, 0 écart métrique. |
| Archive finale et SHA-256 | **EN_COURS** | À produire et tester après génération des rapports. |
