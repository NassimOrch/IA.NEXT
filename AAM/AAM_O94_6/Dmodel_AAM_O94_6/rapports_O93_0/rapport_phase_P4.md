# Rapport de phase P4 — Compétences, composition et routage

## Description

P4 intègre la qualification documentée du socle de compétences, la sélection automatique/manuelle/focus, la composition persistante de compétences dans un graphe déclaratif sûr, et l’acquisition supervisée avec séparation des partitions et rejeu sans source. Statut : `COMPLETE_LOCAL_TESTED_BOUNDED`.

## Architecture

`CompetenceRegistry` décrit/exécute les compétences et décide le routage. `CompositionRepository` gère les graphes `step`/`sequence`/`condition` avec prédicats fermés, hash d’intégrité et traces persistantes. `AAMRuntime` expose la sélection, l’exécution et le rejeu. `O93AcquisitionService` lit JSON, JSONL, CSV et TSV, construit un artefact candidat et mesure validation/holdout/OOD sur des exemples contrôlés. L’interface dispose de l’onglet Compétences, d’un choix manuel dans le chat et d’un éditeur déclaratif de compositions; sa fenêtre native n’a pas été lancée pendant cette phase.

## Pipeline complet

1. Préflight des quatre documents normatifs et des dépendances P0–P3.
2. Compilation de l’implémentation et des tests.
3. Vérification du socle général et de ses frontières.
4. Test de sélection auto/manuelle/focus et de la trace de décision.
5. Sauvegarde/rechargement/exécution d’un graphe conditionnel et séquentiel.
6. Mutation volontaire du hash et contraintes invalides pour s’assurer du refus.
7. Lecture de quatre formats structurés; acquisition sur partitions TRAIN/VALID/HOLDOUT/OOD contrôlées.
8. Rejeu source-off après retrait du dataset et contrôle du contenu de capsule.
9. Tests ciblés, régression complète, construction/render du formalisme et du laboratoire.
10. Mise à jour du registre de preuves, des checklists d’erreurs et de phase.

## Commandes d’exécution

```bash
python -m compileall -q aam_o93 tests/test_p4_competence_graph.py tests/test_p4_acquisition.py
python -m unittest tests.test_p4_competence_graph tests.test_p4_acquisition tests.test_p3_competencies tests.test_p4_ui_integration -v
python -m unittest discover -s tests -v
pdflatex -interaction=nonstopmode -halt-on-error -output-directory evidence formalisme_O93_0.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory evidence laboratoire_O93_0.tex
python /home/oai/skills/pdfs/scripts/render_pdf.py evidence/formalisme_O93_0.pdf --out_dir evidence/render_formalisme_final --dpi 120
python /home/oai/skills/pdfs/scripts/render_pdf.py evidence/laboratoire_O93_0.pdf --out_dir evidence/render_laboratoire_final2 --dpi 120
```

Les commandes ont été exécutées via `scripts/o930_phase_exec.py`, qui enregistre le préflight, code retour, sorties et met à jour l’historique avant/après chaque commande.

## Résultats bruts

- Tests ciblés P4/P3 : **27 réussis, 0 échec** (`logs/O930_P4_targeted_regression_reverified_result.json`; stdout/stderr associés dans le même répertoire de logs).
- Régression intégrale : **143 réussis, 0 échec** en 18,004 s (`logs/O930_P4_full_regression_reverified_result.json`).
- Lecture JSON/JSONL/CSV/TSV : 1 test de contrat réussi.
- Form alisme : 17 pages; laboratoire : 17 pages; rendus de chaque page produits et pages critiques inspectées visuellement.
- Archive source `sources_AAM_17.zip` : SHA-256 `add72728952cd4ec83b6994a02d28022339fbbed29835d40c01b8f26bca60c38`, taille 39758574 octets, 220 membres, CRC ZIP `PASS`.
- Trois incidents de maintenance (décodage de sortie TeX, accent dans un bloc listings, apostrophe de script) sont conservés dans la checklist puis marqués `RESOLVED_RETEST_PASS` avec références de retest; aucune erreur n’a été supprimée.

## Interprétation des résultats

Les contrats du graphe, la sélection de compétences, la persistance et le chemin d’acquisition passent les tests contrôlés. Le statut d’une acquisition reste `CANDIDATE_PENDING_INDEPENDENT_ACCEPTANCE`: ni un succès logiciel, ni une répétition sur un petit exemple ne démontrent une compétence universelle. L’interface a été auditée statiquement et par un round-trip de la CLI/workspace, mais l’interaction GUI native n’a pas été exécutée.

## Conséquences — théoriques, conceptuelles et opérationnelles

- **Théoriques :** la généralité reste une propriété à vérifier sur tâches/données indépendantes; les champs de métadonnées déclarent le contrat, pas une preuve universelle.
- **Conceptuelles :** une compétence peut être un mécanisme reproduit ou un composite conditionnel; le composite garde la provenance et n’est pas promu automatiquement.
- **Opérationnelles :** les graphes et prédicats hors DSL, regex invalides, intervalles incohérents et hashes modifiés sont refusés. Les lignes brutes du dataset ne sont pas conservées dans la capsule. Les formats non structurés se dirigent vers observation/RAG sans étiquettes inventées.

## Conclusions

P4 est fermée dans la portée locale testée. La gate d’acquisition s’appuie sur des fixtures synthétiques; l’évaluation de transfert sur datasets réels reste à faire. La suite complète inclut des tests hérités P5–P9, mais ceux-ci ne remplacent pas la revue/fermeture séquentielle des phases O93_0.

## Statut du modèle

`P4 = COMPLETE_LOCAL_TESTED_BOUNDED`. Prochaine phase autorisable : P5, autonomie persistante/mémoire/feedback causal, après enregistrement de cette clôture. État global O93_0 : **pas déclaré complet**; interface native, ressources Internet/matériel, validation indépendante de généralisation et acceptation externe restent non certifiées.
