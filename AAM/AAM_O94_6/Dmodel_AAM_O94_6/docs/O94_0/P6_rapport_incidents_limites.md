# Rapport O94_0 — incidents, interprétation et limites

## Description
Ce rapport complète `laboratoire_O94_0.tex` et `formalisme_O94_0.tex`. Il suit le modèle de rapport exigé : description, architecture, pipeline, commandes, résultats, interprétation, conséquences théoriques/conceptuelles/opérationnelles, conclusion et statut.

## Architecture concernée
La version O94_0 sépare les responsabilités : (1) conservation/ingestion des enregistrements, (2) routage RAG maître → micro-RAG → feuilles, (3) génération avec question et preuves dans des champs distincts, (4) contrôle de candidate et repli extractif, (5) rendu réponse et détails, (6) arbre hiérarchique de mémoire construit depuis le journal canonique, (7) graphe causal métier séparé de l'intégrité cryptographique, (8) reçus de test/checklists/sauvegarde.

## Pipeline opérationnel
1. La question est observée et normalisée sans remplacer sa sémantique par une réponse attendue.
2. Le RAG est tenté en mode normal même si l'index est vide ; `NO_INDEX`, `NO_MATCH` et `NOT_RUN` restent distincts.
3. Les signatures/résumés du maître acheminent vers un nombre borné de micro-RAG. Les enregistrements complets ne sont lus qu'après sélection et vérification d'intégrité.
4. Le générateur sélectionné reçoit question et preuves séparément. Une instance AAM peut être sélectionnée explicitement ; aucune bascule silencieuse ni délégation récursive n'est autorisée.
5. Si la candidate est inutilisable, le système choisit un champ réponse d'un enregistrement pertinent ou produit une absence de preuve lisible ; il ne concatène pas les records voisins.
6. Le corps de réponse contient le texte de réponse ; sources, scores, hashes, statut, moteur et détails de résolution se trouvent dans l'inspecteur « Détails ».
7. La mémoire utilise maître → micro-branche → événement, avec profondeur de lecture, budget et intégrité. Le journal canonique reste la source de vérité.

## Commandes et reproductibilité
Depuis la racine `Dmodel_AAM_O94_0`, lire d'abord `chemins_O94_0.json`, `checklist_de_travail_O94_0.json` et les deux `checklist_erreurs_*.json`. Les modules représentatifs sont exécutables via `python -m pytest -q tests/test_o940_rag_resolution.py`, `tests/test_o931_chat_pipeline.py`, `tests/test_o940_memory_resolution.py`, `tests/test_o940_ui_resolution_details.py`, `tests/test_o940_real_sms_corpus_sample.py` et `tests/test_o940_real_sms_retrieval.py`. Sur Linux sans écran, les tests Tk doivent être exécutés par le runner sous Xvfb. Pour les phases contrôlées, utiliser `python scripts/o940_phase_test_runner.py --help` et conserver le reçu.

## Résultats observés
- P2 : revalidation d'ingestion TSV SMS, 16 tests et 5 sous-tests ; échantillon de 300 lignes issu d'un corpus de 5 574 lignes, enregistrements préservés et récupération ciblée. Le corpus complet n'a pas été interrogé intégralement.
- P3 : les routes RAG→générateur local, RAG→instance AAM explicitement sélectionnée et `rag_direct` ont des tests distincts. Les réponses structurées longues sont extraites sans couper le payload de référence. Une évaluation Screenplay bornée obtient 10/10 correspondances post-hoc sur 32 enregistrements.
- P4 : mémoire hiérarchique 11/11 ; panneau Détails/depth UI 2/2 sous Xvfb ; inspection d'événements mémoire 7/7 ; graphe causal 4/4 ; régression réponse/chat 30/30 ; récompense/traçabilité 3/3 ; résolution continue UI 1/1.
- P5 : la matrice consolidée rapporte 54/54 modules, 316 tests et 21 sous-tests réussis. Ces reçus sont une preuve locale bornée et n'impliquent pas que les cas inconnus sont tous résolus ou que la vérité factuelle est garantie.

Les reçus bruts et les hashes des sources figurent dans `logs/O94_0/`, notamment `P5_matrix_consolidated_001.json`, `P5_closure_001.json`, `P2_sms_tsv_retest_004.json`, les reçus P3 de réponses longues et les reçus P4 mémoire/UI. Les échecs initiaux ne sont pas effacés des deux checklists d'incidents ; lorsqu'un retest les résout, le statut pointe vers la preuve correspondante. Les interruptions de groupe/timeout ne comptent pas comme PASS en l'absence d'un retest isolé.

## Incidents et limites
1. **Ingestion SMS TSV** : le parseur CSV strict rejetait des guillemets ordinaires dans le corps de message et produisait zéro chunk. La ligne physique est désormais traitée comme une unité et le premier tabulateur sépare étiquette et corps. Le retest 300 lignes passe ; cela ne vaut pas une interrogation exhaustive de 5 574 messages.
2. **Réponses structurées longues** : le champ réponse complet a été séparé du contexte borné envoyé au générateur ; les tests longs et l'évaluation Screenplay échantillonnée passent. Les tests ne prouvent pas une exactitude universelle.
3. **Ordre RAG/génération** : la route normale exécute le RAG avant génération, y compris pour signaler un index vide. Les preuves sont envoyées à part de la requête. Le backend AAM est validé avec adaptateur contrôlé, pas avec tous les services AAM possibles.
4. **Mémoire/affichage** : l'accès progressif conserve le journal canonique et ne charge les payloads qu'après sélection. L'UI a été testée sous Xvfb/Linux, pas sur un Windows natif réel.
5. **Outils de validation** : des problèmes de chemins d'import, de statuts de phase, de schémas de manifeste, d'assertions héritées et de timeouts sont gardés dans les journaux. Les tests retestés individuellement ont des reçus distincts ; les tentatives originales restent conservées.
6. **Limites externes** : aucun endpoint LLM distant vivant, service Internet/MCP réel, appareil caméra/capteur physique ou OS Windows natif n'est réputé validé sans reçu spécifique. Les hashes vérifient l'intégrité des octets contre un état attendu, non leur vérité.

## Interprétation et conséquences
- **Théorique** : la hiérarchie exprime une filtration de classes observationnelles avec raffinement contextuel ; la signature n'est pas un oracle de vérité.
- **Conceptuelle** : RAG, génération, rendu et mémoire deviennent des étapes distinctes. L'arbre permet de demander davantage de détail progressivement au lieu de charger toute la mémoire.
- **Opérationnelle** : l'index est dérivé et doit être resynchronisé après mutation. Chaque paquet final doit passer CRC, extraction indépendante, hash-manifest et smoke test CLI ; les hashes finaux des ZIP sont consignés dans un manifeste externe pour éviter la circularité d'auto-hash.

## Conclusion et statut du modèle
O94_0 contient des correctifs testés pour R1–R3 dans des périmètres explicitement documentés. Le statut n'est pas « complétude universelle » : c'est `LOCAL_TESTED_BOUNDED`, avec limites externes et corpus partiellement évalués. Les phases P6 (documents/registre/sauvegarde) et P7 (construction et vérification finale des archives) ne peuvent être déclarées achevées qu'après les reçus structurels, synchronisation du snapshot et contrôles CRC/hashes des livrables.
