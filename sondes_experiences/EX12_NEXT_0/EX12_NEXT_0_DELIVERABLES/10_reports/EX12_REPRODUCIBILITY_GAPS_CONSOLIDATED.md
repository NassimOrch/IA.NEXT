# Lacunes de provenance et de reproduction — inventaire consolidé EX12

Ce document ne qualifie aucune lacune de sabotage ou de vol : il décrit uniquement ce que les artefacts disponibles permettent ou non de reproduire.

1. **P1_RUN_001 et P1_RUN_002 :** les mesures brutes et logs existent, mais les scripts sources exacts de ces deux prototypes ne sont pas présents. Les runs 003/004 sont les reproductions canoniques avec scripts et hashes. Voir `10_reports/RAPPORT_LACUNES_REPRODUCTIBILITE_P1_RUN001_RUN002.md`.
2. **P5 V2 historique :** 13 416 cellules historiques référencent un script V2 exact indisponible. La reproduction V3 est fournie, hashée et auditée sur 13 440 cellules. Voir `10_reports/RAPPORT_LACUNE_REPRODUCTIBILITE_P5_V2.md` et `10_reports/P5_RESOURCE_REPORT_V3.md`.
3. **P6 v1 :** 123 terminal records ne contiennent pas le hash du script exécuté. Le fichier v1 est présent dans le workspace, mais l'identité octet-pour-octet au moment historique de ces exécutions n'est pas attestable depuis le registre terminal. Voir `10_reports/P6_SCRIPT_PROVENANCE_CAVEAT.md`.
4. **Sources historiques absentes :** `prompt_ex10.json` et `arch_up_test_0.zip` étaient absents de l'archive fournie. EX10 a été reconstruit à partir des rapports, scripts et audits disponibles ; aucune conclusion n'est inventée pour arch_up_test_0.
5. **Prompts :** les prompts EX3/4/5/6/7/8/9/11 ont été audités ; EX10 est une lacune de fichier et non un prompt déclaré lu.

Les scripts réellement disponibles, y compris les versions fautives/abandonnées, sont inclus dans `04_code/` et les registres conservent les tentatives échouées et interrompues.
