# Amodel_eSonde_v8_1 — audit et recherche

Cette archive contient l'audit de l'archive source fournie, la revue eSonde v7/v8, les registres `theorie_emp`, PCH, formalismes, eGenBrain/NGeGenBrain, les contrôles non neuronaux, les rapports d'expériences et le rapport de situation courant. Les fichiers sources attachés et les poids du modèle ne sont pas dupliqués dans Amodel; les poids/artefacts runtime sont dans Dmodel.

## Organisation

- `reports/P0_*`: inventaire, analyses approfondies, réconciliation et synthèses des sources. Les niveaux DEEP_READ, STRUCTURAL_ONLY et METADATA_ONLY sont conservés séparément; le dossier `theorie_emp` est inventorié sur 2 018 chemins mais seulement 160 chemins étaient enregistrés en lecture approfondie dans la checklist source héritée. P0 reste donc IN_PROGRESS.
- `reports/PCH_*`: audit de 34 sources TeX PCH, comparaison des versions, revue mathématique et décision de portée.
- `reports/P0_ESONDE_V7_DEEP_REVIEW_20261117.md` et `P0_OBSISS_SOURCE_AUDIT_20261117.md`: diagnostic v7/Obsiss.
- `reports/FORMALISMES_*`: apport, exclusions et points d'attention des architectures/formalismes historiques.
- `reports/V81_*` et `RAPPORT_V81_*`: génération libre, ablations, erreurs, intégration contextuelle et état des sorties.
- `reports/ETAT_LIVRAISON_ET_AUDIT_eSonde_v8_1_20261118.md`: état courant et prochaine étape.
- `experiments/`: outils d'audit, scripts et registres.

## État des preuves

Le runtime v8.1 présente 131 tests logiciels réussis et trois fichiers TeX v8.1 compilables. Des générations complètes ont été enregistrées, mais plusieurs réponses sont incohérentes ou hors sujet. Les tests logiciels et la stabilité des classements ne prouvent pas la cohérence conversationnelle ni la généralisation. La dernière politique `initial_only` a passé les tests mais n'a pas encore été évaluée par une génération libre.

Les rapports respectent le modèle : description, architecture, pipeline, commandes, résultats, interprétations, conséquences, conclusion et statut. Les incidents de construction partielle et d'exécution interrompue sont conservés comme tels. Aucune hypothèse de réussite ou d'échec global n'est posée.

## Source et données

L'archive source utilisateur et les Parquet OASST1 bruts ne sont pas inclus dans cet audit. Les chemins, empreintes, résultats de décodage et registres de revue sont fournis. Les composants entraînés explicitement neuronaux (RNN/TinyLM/MLP/Transformer/embeddings appris) sont exclus du moteur v8.1.

