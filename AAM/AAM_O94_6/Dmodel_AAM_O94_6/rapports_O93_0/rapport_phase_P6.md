# Rapport de phase P6 — Interface intégrée O93_0

**Version :** AAM O93_0. **État :** `IN_PROGRESS`. **Portée actuelle :** neuf espaces intégrés; tests, smoke Tk/Xvfb et régression locale réalisés; les gates sont en cours de réconciliation avant clôture bornée.

## 1. Description
P6 relie les fonctions déjà séparément testées à une interface cohérente : chat/historique, paramètres, focus, RAG, observer/sondes, compétences, mémoire/observation, entraînement, Internet et réglages généraux. L’interface doit appeler les services réels, conserver l’état nécessaire et rendre visibles erreurs, permissions et limites.

## 2. Architecture
L’interface Tk appelle le runtime, l’observateur multi-format, le Semantic RAG, le moteur de sondes, le registre de compétences/compositions, le gestionnaire d’autonomie/mémoires et les tâches d’entraînement. Les fournisseurs matériels et réseau restent désactivés jusqu’à permission explicite. Le mode local doit fonctionner sans fournisseur Internet.

## 3. Pipeline complet prévu
1. Démarrer le runtime et afficher le chat avec historique et sidebar. 2. Charger/renommer les conversations et lister les sources. 3. Router la sélection automatique/manuelle de compétences et focus. 4. Exposer les actions Observer, RAG, sondes, compositions, mémoire, entraînement et recherche Web. 5. Persister préférences/conversations et journaliser opérations/erreurs. 6. Tester chaque contrôle par callbacks réels, puis intégration bout-en-bout et régression.

## 4. Commandes d’exécution / environnement
Transition validée par `python scripts/o930_transition_p5_to_p6.py`; reçu : `logs/O930_P5_to_P6_transition_receipt.json`. Le développement P6 et ses commandes de test seront ajoutés après chaque sous-étape. Tests headless/mock d’abord; aucun capteur physique, fournisseur réseau ni interface Windows native n’est ouvert par cette transition.

## 5. Résultats bruts
P5 prérequis : 5/5 gates `COMPLETE_LOCAL_TESTED_BOUNDED`, 154/154 tests de régression réussis, audit de clôture `evidence/o930_p5_closure_audit.json`. Transition P5→P6 : PASS; quatre gates P6 restent `PENDING`.

## 6. Interprétation
La dépendance de phase est respectée. La transition n’atteste pas l’implémentation de l’interface demandée; seul l’état de départ de P6 est établi.

## 7. Conséquences
### Théoriques
Le même contrat de tâche/provenance doit traverser l’interface vers les services AAM existants.
### Conceptuelles
Les espaces UI sont des vues de la mission unifiée, et non des fonctionnalités simulées indépendantes.
### Opérationnelles
Les actions requièrent état persistant, gestion d’erreurs et permission lorsque données réseau ou capteurs sont concernées.

## 8. Erreurs, limites et éléments non exécutés
Le rendu GUI natif Windows, l’intégration avec vrai matériel, les fournisseurs Internet/MCP/API et les fonctions multimodales sans décodeur ne sont pas encore validés. Les gates P6 ont depuis été clôturées `PASS_LOCAL_TESTED_BOUNDED` sur le périmètre local testé; les limites externes restent `NOT_RUN`.

## 9. Conclusion
P5 et P6 sont clôturées dans leur portée locale bornée; P7 reste `NOT_STARTED` jusqu’à l’ouverture explicite après préflight.

## 10. Statut du modèle
`P6 = COMPLETE_LOCAL_TESTED_BOUNDED`; `P7 = NOT_STARTED`; `implementation_complete_claimed=false`. Étape suivante : ouvrir P7 uniquement après préflight de transition, puis exécuter et prouver les gates propres aux datasets et à l’entraînement.

## 11. Addendum — inspecteur de sources et candidates de compétence

### Description
Le panneau RAG ajoute un catalogue read-only des sources observées, une inspection bornée des chunks et une commande d'extraction de candidates depuis les structures procédurales trouvées dans le contenu observé.

### Architecture
`AAMRuntime.list_observed_knowledge_sources` vérifie le manifeste, le hash du fichier de chunks, les hashes individuels et l'identité source. `inspect_observed_knowledge_source` expose un aperçu borné sans écriture. `extract_competence_candidates_from_knowledge` écrit des fiches candidates avec références source/chunk et critères d'acceptation; aucune ne contient de code exécutable.

### Pipeline complet
Préflight → lire manifeste → vérifier confinement/hash → cataloguer en lecture seule → sélectionner source → inspecter les chunks validés → extraire uniquement des hypothèses de procédure → sauvegarder candidate, provenance et critères de validation → conserver le statut `CANDIDATE / NOT_EXECUTABLE / NOT_AUTHORIZED`.

### Commandes d'exécution
`python scripts/preflight_O93_0.py --operation P6-source-inspector-candidate-extraction-targeted-tests --output logs/P6_source_inspector_tests_preflight.json`
`python -m py_compile aam_o93/runtime.py aam_o93/ui.py tests/test_p6_source_inspector.py`
`python -m unittest tests.test_p6_source_inspector -v`

### Résultats
Préflight : `PASS_BOUNDED`. `py_compile` : PASS. Tests ciblés : 5/5, zéro échec (`logs/P6_source_inspector_targeted_result.json`). La régression globale antérieure 169/169 est désormais marquée périmée parce que les fichiers runtime/UI ont changé; elle sera rejouée après le smoke UI.

### Interprétation des résultats
Le catalogue et l'inspection garantissent une preuve d'intégrité pour les chunks exposés. Le repérage de procédure sert uniquement à proposer des candidates; il n'affirme pas l'acquisition de la méthode ni sa généralisation.

### Conséquences théoriques, conceptuelles et opérationnelles
Théorique : hashes et provenance relient les vues au contenu observé. Conceptuelle : les propositions restent séparées des compétences exécutables. Opérationnelle : les sources restent en lecture seule et une altération de chunk bloque l'inspection présentée comme valide.

### Erreurs, limites, conclusion et statut du modèle
Ce sous-lot est validé sur corpus textuels temporaires. Les interactions Tk des nouveaux boutons, la régression complète après modification, les grands corpus et les lecteurs multimodaux doivent encore être évalués. `P6 = IN_PROGRESS`, zéro gate P6 clôturé à ce stade; `implementation_complete_claimed=false`.


## Addendum 12 — Inspecteur de sources et candidates (P6)

### Description
Le panneau RAG offre maintenant un catalogue des sources observées, l’inspection en lecture seule de chunks vérifiés et l’extraction de candidates procédurales sans exécution ni promotion.

### Architecture
Le runtime valide les manifestes sources, le confinement des chemins et l’intégrité du fichier de chunks et de chaque ligne; l’interface affiche la provenance puis les candidates.

### Pipeline complet
Préflight normatif → ingestion d’un fichier de test temporaire → catalogue de sources → sélection d’une ligne → inspection bornée read-only → extraction de candidates → contrôle des statuts et de la provenance → vérification d’intégrité mémoire → arrêt runtime.

### Commandes d’exécution
`python scripts/preflight_O93_0.py --operation P6-source-inspector-ui-smoke --output logs/P6_source_inspector_ui_smoke_preflight.json`
`xvfb-run -a python scripts/p6_ui_source_inspector_smoke.py`
`python -m unittest tests.test_p6_source_inspector -v`

### Résultats
Préflight `PASS_BOUNDED`; tests ciblés 5/5; smoke UI `PASS`, code 0. Source hash avant/après identique (`f085de9d01847c1f5b94373b1c75bce1f43e21872bdfb8653cc94ff04aac84ee`), inspection `PASS_BOUNDED` et read-only, candidates: 1, non exécutables et non autorisées; audit et mémoire de raisonnement `PASS`; runtime `STOPPED` et fermé.

### Interprétation
La fonctionnalité UI et la traçabilité de la source sont démontrées dans un environnement local contrôlé. Le détecteur procédural fournit des candidates, non des compétences acquises.

### Conséquences théoriques, conceptuelles et opérationnelles
Théorique: distinction entre empreinte d’une source et statut de compétence. Conceptuelle: candidate ≠ reproduction ≠ généralisation. Opérationnelle: inspection vérifiable sans modification de la source, extraction non exécutable et arrêt confirmé.

### Erreurs, limites, conclusion et statut du modèle
Les essais portent sur un fichier textuel temporaire sous Xvfb. Formats multimodaux avec décodeurs variés, Windows natif, réseau réel et capteurs physiques restent à tester. P6 reste `IN_PROGRESS`; la régression intégrale doit encore être relancée après cette modification. La complétude globale reste non revendiquée.


## Addendum 13 — Compilation et contrôle visuel documentaire

La compilation finale des documents normatifs est PASS (2 passes par document); laboratoire 21 pages et formalisme 19 pages rendus. Les pages P6 (laboratoire p. 17-18 et formalisme p. 14) ainsi que les conclusions finales ont été visuellement inspectées. Le premier échec TeX du chemin inline est résolu après retest.

Preuves : `logs/P6_final_doc_compile_retest_result.json`, `logs/P6_pdf_visual_review_result.json`. La suite complète post-source-inspector reste à exécuter; aucune clôture P6 n’est déduite de la seule validation documentaire.


## Addendum 14 — Régression complète après inspecteur de sources

### Description
La modification de la vue des sources RAG, de l’inspection read-only et de l’extracteur de candidates est intégrée au runtime et au panneau UI. La règle du compteur strict de preuves a été harmonisée avec le test de traçabilité.

### Architecture
Le catalogue s’appuie sur les manifestes et hashes de chunks, l’UI sélectionne une source et appelle le runtime; l’extraction reste une candidate non exécutable et non autorisée. Le registre sépare strictement les statuts vérifiés des statuts implémentés/partiels.

### Pipeline complet
Préflight → inspection normative/checklists → tests ciblés 5/5 → smoke réel Tk/Xvfb → compilation/render PDF → correction du compteur strict → test ciblé du registre 1/1 → régression complète.

### Commandes d’exécution
`python scripts/preflight_O93_0.py --operation P6-full-regression-after-registry-counter-fix --output logs/P6_full_regression_counter_fix_preflight.json`
`python -m unittest discover -s tests -v`

### Résultats
Régression complète : 174/174 tests pass, code 0, aucun échec. Tests ciblés source inspector : 5/5; test du compteur strict : 1/1; smoke UI Xvfb : PASS. Compilation des deux documents deux passes et contrôle visuel des pages P6 passés. Le compteur strict est 4, car seuls les statuts exacts `VERIFIED_LOCAL_TESTED_BOUNDED` entrent dans cette métrique.

### Interprétation
La non-régression locale est établie pour la suite présente. Le compteur n'assimile plus une implémentation bornée ou partielle à une exigence strictement vérifiée. L'extraction candidate est un repérage heuristique, non l'acquisition d'une compétence.

### Conséquences théoriques, conceptuelles et opérationnelles
Théorique : séparation entre observations, hashes et affirmation de compétence. Conceptuelle : statut strict de preuve distinct de l'état d'implémentation. Opérationnelle : catalogue et inspection traçables, extraction non exécutable, test de régression complet enregistré.

### Erreurs, limites, conclusion et statut du modèle
Le test de compteur initial a échoué puis a été corrigé selon une règle stricte, et le retest est vert; les deux résultats restent dans l’historique. Les essais Windows natif, fournisseurs réseau, grands corpus multimodaux et matériels physiques restent non exécutés. `P6 = IN_PROGRESS`; `implementation_complete_claimed=false`; aucune phase suivante n’est ouverte.


## Addendum 15 — Fiches déclaratives et table mémoire causale

### Description
Le panneau Compétences propose maintenant le cycle de vie des fiches déclaratives : ajout, import/export JSON, inspection, modification, validation, test et suppression. Le panneau Observation/Mémoire affiche une table en lecture seule des événements et distingue la chaîne d’intégrité des liens causaux métier déclarés.

### Architecture
`aam_o93/competence_profiles.py` fournit un magasin JSON atomique haché. Une fiche ne référence qu’une compétence enregistrée ou une composition sûre; les champs de code/import/callable sont refusés. `aam_o93/memory.py::recent_events` vérifie la chaîne et expose séparément `prev_hash` et `causal_parent_hashes`.

### Pipeline complet
Préflight → tests store → smoke Tk/Xvfb sur boutons réels → événement parent et enfant causal → vérification mémoire → arrêt → audit statique des boutons → régression complète.

### Commandes
`python -m unittest tests.test_p6_competence_profiles tests.test_p6_memory_event_inspection -v`
`xvfb-run -a python scripts/p6_ui_profile_memory_smoke.py`
`python scripts/audit_ui_button_wiring.py`
`python -m unittest discover -s tests -v`

### Résultats
Tests ciblés : 10/10. Smoke Tk/Xvfb : PASS, opérations de fiches et affichage d’un lien causal validés, journaux audit/raisonnement intègres, runtime fermé. Audit AST : 73 contrôles, zéro sans liaison; les cases à cocher à variable d’état et la portée metadata-only des endpoints sont explicitement rapportées. Régression complète après patch Tk : 184/184, zéro échec (`logs/P6_full_regression_after_profile_memory_smoke.stdout.txt`, code de sortie `0`).

### Interprétation
Le test confirme le cycle technique local, pas la généralisation de compétences référencées. Le hash précédent maintient la chaîne d’audit; seuls des `parent_event_hashes` déclarés expriment une causalité métier. Les imports JSON n’autorisent jamais l’exécution de code embarqué.

### Conséquences théoriques, conceptuelles et opérationnelles
Théorique : événements et relations causales déclarées sont consultables sans mutation. Conceptuelle : fiche déclarative ≠ compétence validée ≠ généralisation. Opérationnelle : les fiches sont persistées/hachées et l’UI ferme sans callback Tk résiduel.

### Erreurs, limites, conclusion et statut
L’assertion UI et les faux positifs de l’audit AST ont été résolus après retest; l’historique des échecs est conservé. MCP/API en direct, caméra/capteurs physiques et UI Windows native restent non exécutés. P6 reste `IN_PROGRESS` jusqu’à compilation/rendu final et réconciliation des gates. `implementation_complete_claimed=false`.


## Addendum 16 — Graphe causal visuel de la mémoire

### Description
L'espace Observation/Mémoire rend en plus de la table une vue Canvas bornée des dix événements récents. Les flèches correspondent uniquement aux parents métier explicitement déclarés.

### Architecture
`O93Desktop._draw_memory_causal_graph` utilise `O93Memory.recent_events`; la chaîne `prev_hash` demeure réservée à l'intégrité. Les parents externes/hors fenêtre et les références invalides sont comptabilisés plutôt que dessinés.

### Pipeline complet
Préflight → 7 tests de contrat du graphe → lancement réel Tk/Xvfb dans un espace temporaire → injection de trois événements de test → rendu Canvas → vérification de l'arête parent-enfant → intégrité des journaux → arrêt/checkpoint.

### Commandes d'exécution
`python scripts/preflight_O93_0.py --operation P6_actual_tk_causal_graph_smoke --output logs/P6_actual_tk_causal_graph_smoke_preflight.json`
`python -m unittest discover -s tests -p test_p6_memory_event_inspection.py -v`
`xvfb-run -a env PYTHONPATH=. python scripts/p6_causal_graph_visual_smoke.py`

### Résultats
Tests ciblés : 7/7 PASS. Smoke Canvas Tk réel : PASS, code 0; 10 nœuds, 1 arête causale déclarée, 10 libellés, aucun lien externe ou invalide sur cet exemple. `prev_hash` n'a pas été interprété comme causalité. Audit et mémoire de raisonnement intègres; autonomie stoppée et checkpoint présent. Voir `logs/P6_causal_graph_contract_targeted_result.json` et `logs/P6_causal_graph_visual_smoke_result.json`.

### Interprétation
Le contrat de rendu et le câblage réel sont vérifiés localement. Les flèches visualisent des liens déclarés dans les événements; elles n'établissent pas une causalité externe.

### Conséquences théoriques, conceptuelles et opérationnelles
Théorique : séparation entre chaîne d'intégrité et causalité déclarée. Conceptuelle : le graphe facilite l'inspection sans transformer une trace en compétence acquise. Opérationnelle : fenêtre de dix événements, comptage des parents absents et absence de mutation des mémoires.

### Erreurs, limites, conclusion et statut du modèle
La recherche initiale d'un helper inexistant est résolue par la création et le retest de ce smoke; l'erreur initiale reste archivée. Windows natif, réseau/MCP réels, caméras/capteurs physiques et très grands journaux ne sont pas validés par ce test. La régression intégrale post-graphe et l'inspection finale des documents restent requises. `P6=IN_PROGRESS`, `P7=NOT_STARTED`, `implementation_complete_claimed=false`.


## Addendum 17 — Régression complète et parcours interactif final après le graphe causal

### Description
Le graphe causal est intégré dans le panneau Observation/Mémoire et les parcours UI complets ont été rejoués après sa modification.

### Architecture
La table d’événements et le Canvas utilisent le journal vérifié de `O93Memory`; le reste du shell garde une file de tâches sérielle, des états visibles, et le focus/réglage réseau persistant.

### Pipeline complet
Préflight normatif → compile/rendu du laboratoire et formalisme → régression complète → smoke réel Canvas → smoke UI interactif complet → contrôle des SHA-256 source et stores mémoire → arrêt autonome/checkpoint → réconciliation des preuves dans la checklist et le registre.

### Commandes
`python scripts/preflight_O93_0.py --operation P6_final_full_ui_interactive_smoke_after_graph --output logs/P6_final_full_ui_interactive_smoke_after_graph_preflight.json`
`xvfb-run -a env PYTHONPATH=. python scripts/p6_ui_interactive_smoke.py`
`python scripts/run_p6_graph_full_regression.py`

### Résultats
Régression complète : 189/189 PASS, zéro échec, code 0. Parcours interactif : PASS, neuf onglets attendus, création/renommage de chat, source inchangée, 31 candidates de sondes distinctes dans le test, compétence et composition exécutées, observation et RAG réussis, gestion des espaces sémantiques passée, commandes pause/reprise/arrêt d’entraînement simulées par contrôleur, permission Internet désactivée respectée, focus (source/mémoire/cadence) persisté, tâche et feedback causaux enregistrés, audit et mémoire de raisonnement intègres, runtime `STOPPED`/fermé. Le graphe Canvas réel est couvert par `logs/P6_causal_graph_visual_smoke_result.json`.

### Interprétation
La suite locale est non régressive pour les 189 tests exécutés et le parcours UI automatisé. Le résultat n’équivaut pas à une certification Windows native, réseau externe, matériel, apprentissage sur grand corpus ou généralisation universelle. L’entraînement réel n’a pas été lancé dans le cadre du smoke P6.

### Conséquences théoriques, conceptuelles et opérationnelles
Théorique : séparation maintenue entre empreinte observable, recherche sémantique empirique, liens causaux déclarés et intégrité du journal. Conceptuelle : candidate, compétence testée et généralisation restent des statuts distincts. Opérationnelle : le shell fonctionne localement en bout en bout; l’accès réseau reste opt-in et les fichiers sources sont non destructifs.

### Erreurs, limites, conclusion et statut du modèle
L’échec initial de chargement des catalogues et l’accès Tk depuis un worker sont conservés comme incidents historiques et résolus par retest positif. Les quatre gates P6 restent à synchroniser après l’inspection finale des deux documents recompilés. `P6=IN_PROGRESS`, `P7=NOT_STARTED`, `implementation_complete_claimed=false`.

## Addendum 18 — Compilation, rendu et revue visuelle finaux du dossier P6

### Description
Le dossier de conception et le laboratoire ont été recompilés en deux passes, rendus page par page, puis revus visuellement avant toute synchronisation finale de phase.

### Architecture
Les sources normatives sont `laboratoire_O93_0.tex` et `formalisme_O93_0.tex`; les PDF compilés, inventaires de pages, SHA-256 et images de rendu sont conservés dans le paquet modèle. L'audit AST séparé recense les contrôles UI sans confondre action locale, métadonnée de connecteur et exécution distante.

### Pipeline complet
Préflight `PASS_BOUNDED` → compilation LaTeX de deux documents (deux passes chacun, codes 0) → rendu PDF de toutes les pages → inspection visuelle des pages de titre, du chapitre graphe causal, des références longues et de la conclusion → comparaison des hashes PDF/registre de compilation → audit statique UI (73 contrôles, aucun non câblé) → rapprochement des checklists et du registre.

### Commandes
`python scripts/preflight_O93_0.py --operation P6_final_docs_render_corrected --output logs/P6_final_docs_render_corrected_preflight.json`
`pdflatex -interaction=nonstopmode -halt-on-error laboratoire_O93_0.tex` (deux passes)
`pdflatex -interaction=nonstopmode -halt-on-error formalisme_O93_0.tex` (deux passes)
`python /home/oai/skills/pdfs/scripts/render_pdf.py laboratoire_O93_0.pdf --out_dir evidence/P6_release_render_laboratoire --dpi 130`
`python /home/oai/skills/pdfs/scripts/render_pdf.py formalisme_O93_0.pdf --out_dir evidence/P6_release_render_formalisme --dpi 130`
`python scripts/audit_ui_button_wiring.py`

### Résultats
Compilation : PASS, deux passes par document. Rendu : PASS; laboratoire 24 pages, formalisme 19 pages. Revue visuelle : PASS sur les pages de titre, page du graphe causal, page de conclusion et page du contrat causal dans le formalisme; aucune troncature/coupure visible sur les pages contrôlées. Les hashes et sorties vérifiables figurent dans `logs/P6_final_docs_compile_result.json`, `logs/P6_release_pdf_render_result.json` et `logs/P6_release_pdf_visual_review_result.json`. L'audit statique est `PASS_WITH_EXPLICIT_SCOPE`, 73 contrôles, zéro non câblé.

### Interprétation
La sortie PDF et la revue des pages contrôlées sont valides dans l'environnement de build. Cela ne valide ni un environnement graphique natif non testé ni les fournisseurs distants et appareils physiques.

### Conséquences théoriques, conceptuelles et opérationnelles
Théorique : les rapports et statuts doivent être traçables sans surinterpréter le périmètre d'essai. Conceptuelle : un document correctement rendu prouve la lisibilité du compte rendu, pas la capacité universelle du modèle. Opérationnelle : les PDF, sources TeX, journaux et hashes sont livrés ensemble.

### Erreurs, limites et statut du modèle
Le premier appel de rendu utilisait l'option invalide `--output_dir`; l'incident `DOC-P6-RENDER-CLI-ARG-001` a été résolu par une exécution correcte avec `--out_dir`. Les quatre gates ont été explicitement évaluées `PASS_LOCAL_TESTED_BOUNDED` et la clôture P6 est inscrite dans la checklist et le registre. Le statut global de complétude reste `false`; P7 n’est pas démarrée par cette clôture et requerra son propre préflight.

## Addendum 19 — Clôture formelle bornée de P6

### Description
P6 clôturée après synchronisation des quatre gates de l’interface dans le périmètre local testé.

### Architecture
La fermeture repose sur l’interface Tk, les services runtime et les journaux persistants déjà reliés; aucun fournisseur distant ou périphérique physique n’est supposé actif.

### Pipeline complet
Préflight de gate → vérification de la régression 189/189 → smoke UI complet et smoke Canvas → audit 73 contrôles / zéro non câblé → compilation en deux passes, rendu complet des deux PDF, revue visuelle → vérification SHA-256 de l’archive originale → statuts des quatre gates écrits dans la checklist et le registre.

### Commandes
`python scripts/preflight_O93_0.py --operation P6_final_gate_review_and_closure --output logs/P6_final_gate_review_and_closure_preflight.json`
`python scripts/close_p6_bounded_after_review.py`

### Résultats
Quatre gates `PASS_LOCAL_TESTED_BOUNDED`; phase `COMPLETE_LOCAL_TESTED_BOUNDED`. La régression locale est 189/189, l’UI présente neuf espaces et le Canvas causal dessine les parents déclarés. Le laboratoire compile en deux passes et produit 27 pages; le formalisme compile en deux passes et produit 19 pages; rendu/revue visuelle PASS. Le hash de l’archive source originale demeure `add72728952cd4ec83b6994a02d28022339fbbed29835d40c01b8f26bca60c38`.

### Interprétation
La clôture signifie uniquement que les gates d’intégration UI locales ont passé les critères définis. Elle ne certifie pas le potentiel universel ni la réussite/échec futur d’AAM.

### Conséquences théoriques, conceptuelles et opérationnelles
Théorique : l’interface expose des observations, espaces sémantiques et liens causaux déclarés. Conceptuelle : le passage d’une phase ne prouve pas que toutes les compétences se généralisent. Opérationnelle : chaque phase reste indépendante, les incidents sont conservés et les paquets doivent reproduire ces preuves.

### Erreurs, limites, conclusion et statut du modèle
L’erreur d’option de rendu `--output_dir` est résolue par retest positif avec `--out_dir`. Windows natif, matériel, exécution MCP/API distante et entraînement réel sur grand corpus restent `NOT_RUN` ou affectés aux phases suivantes. `P6=COMPLETE_LOCAL_TESTED_BOUNDED`; `P7=NOT_STARTED`; complétude globale `false`.
