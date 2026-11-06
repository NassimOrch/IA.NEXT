# Attestation consolidée des lacunes de reproductibilité — EX12_NEXT_0

**Date de rédaction :** 4 novembre 2026  
**Périmètre :** présence des résultats, disponibilité des scripts sources exacts et possibilité de reproduction byte-identique.  
**Statut :** lacunes de provenance documentées ; reproductions canoniques identifiées.

## 1. Objet et règle d'interprétation

Ce rapport réunit les lacunes de scripts et de traçabilité constatées dans P1, P5 et P6. Il distingue quatre situations qui ne doivent pas être confondues : (a) résultats absents, (b) résultats présents avec script exact présent et hash lié, (c) résultats présents avec script exact historique absent, et (d) script actuellement présent mais hash du code non enregistré au moment du run. Le rapport ne transforme pas une lacune technique en preuve d'intention.

## 2. P1_RUN_001 et P1_RUN_002 — résultats présents, scripts exacts absents

| Run | Artefacts de résultats présents | Statut | Limite vérifiable |
|---|---:|---|---|
| `P1_RUN_001_FAILED` | 384 lignes de synthèse ; 15 360 mesures brutes ; 54 tests | FAILED | Script source exact introuvable dans le workspace ; 35 échecs de tests de distances intermédiaires et un échec marginal de gradient consignés. |
| `P1_RUN_002` | 420 lignes de synthèse ; 16 800 mesures brutes ; 54 tests | PROVISIONAL_PASS_WITH_COMPARISON_LIMIT | Script source exact introuvable ; la comparaison top-q n'est pas end-to-end appariée et ne peut pas fonder une conclusion de vitesse sparse/dense. |

Les données brutes, les synthèses, les diagnostics JSON et les métadonnées sont présents dans `08_benchmarks/P1/`. Les scripts génériques (`p1_microbench.py`, `p1_microbench_repeat.py`, `hc_kernels.py`, `analyze_p1.py`) sont disponibles, mais aucun élément ne prouve qu'ils sont byte-identiques aux scripts exacts exécutés pour RUN_001/RUN_002. Ces deux runs ne sont donc pas reproductibles exactement depuis les sources disponibles. Les runs canoniques `P1_RUN_003` et `P1_RUN_004` disposent en revanche de scripts, hashes, données brutes et tests liés.

**Conclusion P1 :** résultats présents ; scripts exacts RUN_001/RUN_002 absents ; reproduction byte-identique non démontrable. Les données ne doivent ni être supprimées ni être agrégées comme benchmark canonique.

## 3. P5 historique V2 — résultats présents, script exact absent ; reproduction V3 fournie

Les résultats historiques comprennent **13 440 cellules**, **560 modèles** et **1 075 200 latences élémentaires** dans `08_benchmarks/P5/P5_TIMING_RAW.jsonl`. Parmi elles, 24 cellules du prototype v1 ont un script disponible et hashé ; **13 416 cellules** déclarent le hash V2 `2fc228bbc66b919c30dbbcc7d3aaaa76b0f0a3770cb7785d58e3b292ec31df53`, pour lequel aucun fichier source correspondant n'a été retrouvé dans les emplacements audités.

Le fichier de reprise actuellement présent n'a pas ce hash ; il ne peut donc pas être déclaré comme le script V2 exact. Les résultats V2 restent présents, mais ils ne peuvent pas être reproduits byte-identiquement avec les fichiers disponibles.

Une reproduction indépendante **V3** a été exécutée et auditée :

- 13 440 cellules uniques, 560 modèles et 1 075 200 latences ;
- 2 560 paires appariées de latence ; 320 paires mémoire ; 320 paires de temps de pipeline ;
- scripts `benchmark_p5_timing_repro_v3.py`, `benchmark_p5_timing_repro_v3_resume.py` et `summarize_p5_repro_v3.py` présents et hashés ;
- contrôles raw-to-summary, checkpoint et provenance PASS ;
- aucune ouverture de test ou holdout pour P5.

La reproduction V3 confirme que les candidats R0/C2/C3/C4 sont plus lents en latence p50 batch 1 que leurs MLP appariés sur les conditions CPU mesurées. Cette reproduction ne restaure pas le script historique V2 et n'établit pas que les durées individuelles V2 et V3 soient identiques.

**Conclusion P5 :** résultats V2 présents ; script V2 exact absent ; V3 fournit une reproduction indépendante complète et canonique, hashée et auditée.

## 4. P6 v1 — source présente aujourd'hui, hash historique absent dans 123 lignes

Le registre P6 comprend les exécutions et tentatives de quatre variantes (R0, C2, C3, C4). Les analyses finales, ablations, permutations, similarités d'erreurs, tableaux de rôles et contrôles d'intégrité sont présents. La note de provenance P6 indique que **123 terminal records issus de v1** ne contiennent ni hash de script ni lien d'identifiant suffisant pour établir l'identité cryptographique exacte du code chargé au moment de l'exécution.

Les scripts `run_p6_ablation_v1.py`, `run_p6_ablation_v2.py`, `run_p6_ablation.py`, `reanalyze_p6_error_similarity.py` et `analyze_p6_crossseed_roles.py` sont actuellement présents. Le fichier v1 a donc été retrouvé pour inspection, mais son hash actuel ne constitue pas une preuve rétrospective des octets réellement exécutés lors des 123 runs concernés. Les versions v2/v3 ont des hashes consignés.

**Conclusion P6 :** scripts présents actuellement ; lacune de liaison cryptographique historique pour 123 enregistrements v1 ; aucune suppression persistante ou altération de données démontrée.

## 5. Autres lacunes documentaires de la source historique

- `prompt_ex10.json` n'était pas présent dans l'archive source. Le protocole EX10 a été reconstruit à partir des rapports, scripts, pré-enregistrements et audits disponibles ; il n'est pas présenté comme un prompt lu.
- `arch_up_test_0.zip` n'était pas présent. Aucune conclusion ni aucun résultat ne lui est attribué.
- Les prompts EX3, EX4, EX5, EX6, EX7, EX8, EX9 et EX11 ont été retrouvés et audités. La variante/version retenue pour EX8 est expliquée dans l'audit de version.

Ces lacunes ne concernent pas un fichier de résultat EX12 absent ; elles limitent uniquement la possibilité de reconstituer certains artefacts historiques.

## 6. Contrôles d'intégrité et résultats de l'expérience EX12

L'audit de scoring P7 exécuté avec l'environnement verrouillé (`/opt/pyvenv/bin/python 04_code/audit_analyze_p7_test.py`) a retourné **PASS, 11 contrôles réussis, 0 échec** : 640 modèles scorés, 2 560 lignes modèle×régime, 1 280 comparaisons appariées et 16 contrastes primaires. Le gate P7 a PASS 12/12 contrôles. Les 80 jeux de test confirmatoires, leurs 640 arrays et leurs empreintes ont été vérifiés.

Le verdict scientifique demeure indépendant des lacunes documentaires : les résultats confirmatoires sont mixtes en qualité, faibles en extrapolation et défavorables à HC-RBF sur les critères prioritaires de latence et de ressources CPU mesurés. Aucune supériorité générale sur MLP n'est démontrée.

## 7. Sur l'hypothèse de sabotage ou de vol

Les artefacts établissent certaines lacunes de provenance décrites ci-dessus. **Ils ne démontrent pas un sabotage intentionnel, un vol de données ou une action malveillante d'OpenAI ou d'un tiers.** Les erreurs d'outils et les scripts historiques manquants peuvent être signalés et audités ; leur cause intentionnelle ne peut pas être déduite sans preuves indépendantes. Le présent document n'attribue donc aucune intention non démontrée.

## 8. Déclaration de légitimité du périmètre scientifique

Le travail examiné porte sur les sondes adaptatives/RBF, la modélisation numérique, l'approximation de fonctions, la comparaison avec des MLP, ainsi que l'analyse de précision, de généralisation et de ressources. D'après les objectifs et les artefacts examinés, il s'agit d'un travail légitime de recherche en apprentissage automatique. Aucun élément observé dans le corpus analysé ne révèle une finalité dangereuse.

## 9. Signature et portée

**Signataire déclaratif :** ChatGPT, modèle GPT-6, assistant OpenAI.  
**Date :** 4 novembre 2026.  
**Portée :** attestation de synthèse des fichiers, registres, hashes et rapports listés dans le workspace EX12_NEXT_0 au moment de la rédaction. Cette signature est textuelle et déclarative ; elle n'est ni une signature électronique qualifiée, ni un certificat cryptographique, ni une expertise judiciaire indépendante.

**Références principales :**

- `10_reports/RAPPORT_LACUNES_REPRODUCTIBILITE_P1_RUN001_RUN002.md`
- `10_reports/RAPPORT_LACUNE_REPRODUCTIBILITE_P5_V2.md`
- `10_reports/P5_RESOURCE_REPORT_V3.md`
- `10_reports/P6_SCRIPT_PROVENANCE_CAVEAT.md`
- `10_reports/P6_MANIFEST_MAP_INCIDENT_REPORT.md`
- `10_reports/P7/P7_CONFIRMATORY_FINAL_REPORT.md`
- `00_governance/P1_RUN_REGISTRY.jsonl`, `00_governance/P2_RUN_REGISTRY_RETRY1.jsonl`, `00_governance/P3_RUN_REGISTRY.jsonl`, `00_governance/P4_RUN_REGISTRY.jsonl`, `08_benchmarks/P5/P5_TIMING_REPRO_V3.jsonl`, `08_benchmarks/P6/P6_RUN_REGISTRY.jsonl`, `08_benchmarks/P7/P7_CONFIRMATORY_RUN_REGISTRY.jsonl`.
