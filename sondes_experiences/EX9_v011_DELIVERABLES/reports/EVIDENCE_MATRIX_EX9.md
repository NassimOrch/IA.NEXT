# Matrice de preuves et de conformité expérimentale — EX9 v011 (état final)

| Branche / exigence | Expériences réellement présentes | Statut probant | État / preuve |
|---|---|---|---|
| Intégrité `last_sources_3.zip` et ZIP imbriqués | CRC shell, extraction, audits sources | `PASS_INTEGRITY` | `inputs/AUDIT_SOURCES_EX9.md`, inventaire SHA source |
| Prompts EX3–EX8 | Prompts et politiques comparés, provenance hashée | `AUDITED` | `reports/PROMPT_EX9_AUDIT.md`, `inputs/source_provenance_manifest.json` |
| Catalogue EX8 v010 | A0–A4, B1–B11, ablations B6 et familles B3–B9 | `HISTORICAL_AUDIT` | `reports/EX8_VARIANT_CATALOG.md` |
| B10/B11 historiques Wisconsin | 5 seeds, comparateurs MLP, prédictions, checkpoints, traces | `HISTORIQUE_INTEGRITY_PASS / DEV` | B10 LL 0,04138964 ; B11 0,04442526 ; gains historiques non confirmatoires |
| B10/B11 réplication EX9 xor8 | 5 seeds + MLP apparié/GE4X | `DEV_NEGATIVE` | 45 JSON/checkpoints ; B10 0,549981 ; B11 0,554089 ; perdent 5/5 |
| A0 réplication EX9 xor8 | 5 seeds + MLP apparié/GE4X | `DEV_NEGATIVE` | A0 0,450060 ; perd 5/5 |
| Ablations B10 table-only | 7 variantes × 5 seeds | `DEV_ABLATION_COMPLETE` | 35/35 audit ; validation déjà utilisée ; pas confirmatoire ; voir `REPORT_B10_ABLATIONS_EX9.md` |
| Parité HARD_3X3 bins | Comparaison `numpy.digitize`/`torch.bucketize` | `PASS_NO_EXACT_THRESHOLD_TIES` | Aucun tie exact train/validation ; 0 mismatch de bins sur cinq seeds |
| Multi-domaines synthétiques de développement | `concentric2`, `rotated_moons2`; B10/B11/A0 + 2 MLP ×5 seeds | `DEV_COMPLETE / AUDITED` | 90 runs ; `MULTI_DOMAIN_INTEGRITY_AUDIT.json` PASS 90/90 |
| Tests synthétiques scellés supplémentaires | `concentric2` seed 61301, `rotated_moons2` seed 62301 ; 1 200 exemples/domaines | `SYNTHETIC_CONFIRMATORY_SCORED` | 90 prédictions ; snapshot pré-test 295 SHA ; métrique PASS 90/90 ; audit post-test 294/295 (exception rapport uniquement) ; aucun modèle modifié après test |
| Holdout synthétique xor8 | Seed test généré avant échec de désérialisation | `OPENED_BUT_NOT_SCORED / COMPROMISED` | Ne pas relancer ; labels générés en mémoire, aucun score/test prédiction écrit |
| Confirmation sur dataset réel vierge | Aucun dataset réel externe neuf disponible/validé | `BLOCKED_REAL_EXTERNAL_DATA` | SMS/Wisconsin/Iris/Breast déjà exposés ; réseau DNS indisponible ; dataset parquet sans PyArrow |
| Série A0 complète | A0 fidèle exécutée sur trois domaines synthétiques ; ablations PCA/local/global/hybrides non achevées | `PARTIAL` | `REPORT_A0_EX9.md`, reports multi-domaines ; pas de victoire MLP |
| B10/B11 efficacité architecturale avancée | Ablations table B10 effectuées ; distillation, sharing RBF, kernels optimisés et gates supplémentaires non exécutés | `PARTIAL` | 35 ablations ; latence encore 12–22× MLP sur domaines 2D, 20× environ sur xor8 |
| CNG | `sin(x)` M1/M2 mean/M2 linear, 1 seed | `PILOT` | 3 runs ; audit PASS |
| CNC spécialistes | ADD/SUB/MUL/DIV/EXP/LOG M1, 1 seed chacune | `PILOT` | 6 runs ; audit PASS ; DIV distribution pas exactement induite |
| CNC graphes C1/C2/C3 | Compositions et fine-tuning conjoint | `NON_EXECUTE` | Core TeX corrigé mais expériences complètes manquantes |
| P_total et budget 4× | 45 runs xor8 + 90 runs 2D, MLP apparié/GE4X | `MEASURED / AUDITED` | Ratio MLP_GE4X ≥4.0 par run |
| Latence CPU et temps fit end-to-end | 135 runs classification + ablations | `MEASURED_WITH_LIMITS` | Warmup 20, 40 répétitions, batches 1/16/64/256 ; CPU only |
| MAC/FLOPs complets | Proxies structurels incomplets uniquement | `NOT_MEASURED_FULL` | Ne pas assimiler les proxies à des FLOPs complets |
| RSS peak / mémoire GPU / énergie | Pas de mesure homogène | `NOT_MEASURED` | CPU-only, pas de wattmètre ; RSS peak non isolé |
| Historiques MLP EX9 xor8 / optimizer states | Historiques MLP manquants dans le script initial ; nouveaux domaines les incluent | `TRACE_GAP_PARTIALLY_CLOSED` | `TRACE_CAPTURE_GAP.md`; aucune trace ancienne inventée |
| Historique ZIP/source dans workspace EX9 | Source archives à l'extérieur ; aucun ZIP historique copié | `PASS_SCOPE` | `find EX9_v011 -name '*.zip'` doit rester vide |

## Verdict global

La spécification EX9, l'audit de source, la récupération B10/B11, les expériences principales, les ablations table, les pilotes CNG/CNC et deux tests synthétiques multi-domaines sont livrés et audités. Les tests synthétiques indépendants confirment que les sondes B10/B11/A0 sont inférieures aux MLP sur les deux tâches 2D ; le coût d'inférence CPU est également beaucoup plus élevé. Les résultats EX8 Wisconsin restent intéressants mais ne se généralisent pas à ces domaines. La confirmation sur données réelles vierges, les mesures complètes de FLOPs/RSS/énergie, les ablations end-to-end avancées et les graphes CNG/CNC demeurent non exécutés. Le travail est donc **partiellement achevé, avec verdict négatif sur les critères de qualité/vitesse dans les nouveaux domaines synthétiques**, sans extrapolation abusive.
