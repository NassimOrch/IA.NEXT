# Rapport de lacunes de reproductibilité — prototypes P1_RUN_001 et P1_RUN_002

**Expérience :** EX12_NEXT_0 — banc informatique P1  
**Date de rédaction :** 4 novembre 2026  
**Périmètre :** vérification des artefacts P1 présents dans `EX12_NEXT_0/08_benchmarks/P1`.

## Constat vérifiable

Deux prototypes ont livré des données et des rapports, mais leur script source exact, dans la version effectivement exécutée, n'est pas présent dans le workspace EX12. Cette lacune est déjà enregistrée dans `00_governance/P1_RUN_REGISTRY.jsonl` et les notes des runs.

| Run | Artefacts de résultats présents | Statut déclaré | Lacune de reproduction |
|---|---:|---|---|
| `P1_RUN_001_FAILED` | 384 lignes de synthèse, 15 360 mesures brutes, 54 tests consignés | FAILED | Script source exact introuvable ; la tentative contient 35 échecs de tests de distance intermédiaire et un échec de gradient marginal. |
| `P1_RUN_002` | 420 lignes de synthèse, 16 800 mesures brutes, 54 tests consignés | PROVISIONAL_PASS_WITH_COMPARISON_LIMIT | Script source exact introuvable ; les temps top-q ne sont pas end-to-end appariés et ne sont pas admissibles pour conclure sur le top-q. |

Les fichiers `P1_BENCHMARK_RAW.csv`, `P1_BENCHMARK_SUMMARY.csv`, `P1_NUMERICAL_TESTS.json` et les métadonnées de chaque run sont présents. Le registre précise explicitement `exact source script not found in current EX12 workspace`. Les scripts génériques `p1_microbench.py`, `p1_microbench_repeat.py`, `hc_kernels.py` et `analyze_p1.py` sont aussi présents, mais rien ne prouve qu'ils sont byte-identiques au script exact exécuté pour RUN_001 ou RUN_002. Ils ne permettent donc pas d'affirmer une reproduction exacte de ces deux artefacts.

## Portée scientifique de la lacune

- Les chiffres bruts historiques restent consultables et leur statut est conservé.
- RUN_001 est un prototype échoué ; ses mesures ne doivent pas être agrégées comme benchmark valide.
- RUN_002 est un prototype technique provisoire ; sa comparaison top-q est asymétrique et doit être exclue de toute conclusion comparative sur la vitesse sparse/dense.
- Les conclusions P1 canoniques reposent sur `P1_RUN_003` et `P1_RUN_004`, pour lesquels les scripts, les empreintes, les journaux, les résultats bruts et les tests sont livrés.

## Décision

**Lacune de reproductibilité confirmée pour les scripts exacts de RUN_001 et RUN_002.** Il serait incorrect d'écrire que ces deux runs peuvent être exactement reproduits à partir des scripts présents. Il serait tout aussi incorrect de supprimer leurs données : elles sont conservées, signalées et exclues des comparaisons canoniques concernées.

Aucun indice dans ces artefacts n'établit une falsification des résultats ou un sabotage. Le constat porte exclusivement sur une lacune de provenance logicielle.

---

**Signature électronique textuelle :** ChatGPT — GPT-6, assistant de recherche  
**Date :** 2026-11-04  
**Nature de la signature :** déclaration de provenance générée par l'assistant ; ce n'est ni une signature manuscrite, ni un certificat cryptographique, ni une attestation juridique indépendante.
