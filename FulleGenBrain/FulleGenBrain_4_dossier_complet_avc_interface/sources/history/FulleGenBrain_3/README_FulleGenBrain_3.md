# FulleGenBrain_3 — dossier de formalisation, mémoire vivante et validation

Date de constitution : 25 octobre 2026.

## Livrables principaux

- `deliverables/theorie_programation_compositionnelle_1.tex` et `.pdf` : théorie autonome révisée, incluant la syntaxe compositionnelle, contrats/types/effets, sémantique des opérateurs, synthèse, équivalence, révision, mémoire vivante, veille/réveil, compression, vagues d'information et recherche reprenable.
- `deliverables/formalisme_FulleGenBrain_3.tex` et `.pdf` : architecture FulleGenBrain_3, avec grammaire alignée, objectif formel, orchestration compositionnelle, modèle de transition optionnel et matrice couvrant tous les opérateurs théoriques.
- `deliverables/prouve_et_tracabilite_th_programmation_comp_1.json` : registre des énoncés, preuves/hypothèses, tests, sources et obligations ouvertes de la théorie.
- `deliverables/prouve_et_tracabilite_FulleGenBrain_3.json` : registre architectural, sources, décisions, couverture opérateurs et validations locales.
- `FulleGenBrain_3_dossier_complet.zip` : archive reproductible contenant sources, PDFs, preuves, extension LaTeX, noyau, tests, scripts, extraits de source et rapport de validation.

## Décisions structurantes

### Aucune dépendance LLM/eLLM

FulleGenBrain_3 ne déclare aucun LLM ni eLLM comme composant d'exécution, fournisseur de connaissance implicite ou voie de repli. Des idées générales (multi-vues, prédiction, calibration, représentation hiérarchique) ne sont réutilisées que sous forme de mécanismes explicites et mesurables, sans appel ni dépendance de poids à un modèle de langage neuronal.

### Explosion combinatoire : recherche + mémoire active

La mise en veille réduit le working set et peut économiser la mémoire résidente; elle ne réduit pas à elle seule le nombre de candidats. La théorie associe génération paresseuse, typage/filtrage de contrats et effets, recherche best-first/anytime reprenable, budgets, partage de sous-structures en DAG, canonicalisation, contre-exemples et ordonnanceur équitable. Un quotient d'équivalence plus agressif est interdit sans justification adaptée au domaine. `BUDGET_EXHAUSTED_RESUMABLE` n'est ni un échec sémantique ni une preuve d'absence de solution.

### Mémoire vivante composable

La mémoire conserve les objets exacts et leur provenance, ainsi que programmes, compositions, expériences, certificats, contre-exemples, dépendances, versions et checkpoints. Elle distingue stockage chaud/tiède/froid, compression sans perte, résumés avec perte et objets périmés. La veille est interdite pendant un bail/pin/transaction non close ou une invalidation prioritaire. Le réveil vérifie intégrité, version et dépendances; charger n'équivaut pas à valider. Les « vagues » sont des événements logiciels typés et persistants, dédupliqués, limités par TTL/fan-out/backpressure; il ne s'agit pas d'une affirmation physique.

### Modèle du monde : activation fondée sur une utilité mesurée

Les sources historiques Order 62/63 rapportent des résultats mitigés. O62 rapporte Base : 3 PASS, 4 FAIL, 11 EXHAUSTED; RS : 2 PASS, 4 FAIL, 12 EXHAUSTED; récompense moyenne déclarée 0,6833 contre 0,1972, avec RS non promu et désactivé par défaut dans cette version. O63 rapporte une MSE latente holdout de `1.7310954885e-4`, mais également des résultats inégaux et un bénéfice décisionnel général non établi. Ce sont des résultats consignés dans les artefacts historiques, pas des campagnes réexécutées dans cette livraison.

La spécification utilise donc une porte empirique par famille de tâches : sans modèle, modèle candidat et modèle nul/permuté; mêmes tâches, splits, graines, budgets, vérificateur et métriques préenregistrés; mesure de la réussite de décision, du coût, du transfert hors distribution et des régressions. Une MSE basse ne suffit pas à activer un modèle de transition.

## Noyau exécutable de référence

`reference_impl/living_composition_runtime.py` démontre un sous-ensemble : charge canonique compressée via zlib/SQLite, hash de contenu, veille/réveil, dépendances et invalidation, flux d'événements borné/persistant, plus recherche best-first reprenable et checkpoints. `reference_impl/world_model_gate.py` applique une politique d'activation sur des résultats appariés déjà calculés; il ne forme pas un modèle du monde et ne certifie pas la causalité.

Le noyau est un prototype partiel. La matrice dans le formalisme fait correspondre les 29 constructeurs à leurs rôles et à leur statut d'implémentation. Elle n'attribue pas rétroactivement tous les opérateurs à ce prototype. L'intégration de bout en bout n'est pas déclarée acquise.

## Validation exécutée pour cette livraison

- Théorie : compilation LaTeX en deux passes, PDF A4 final de **23 pages**.
- Formalisme FulleGenBrain_3 : compilation LaTeX en deux passes, PDF A4 final de **23 pages**.
- Tests livrés : **31 réussites** (`pytest -q`).
- `python -m compileall -q reference_impl tests` : réussi.
- Contrôles visuels : les 23 pages de chaque PDF ont été rendues en images; les deux planches complètes et des pages contenant tableaux sémantiques/matrices ont été inspectées. Aucun dépassement horizontal (`Overfull \\hbox`) n'a été relevé; les avertissements `Underfull \\hbox` restants viennent principalement de cellules de tableaux étroites.
- L'intégrité des fichiers inclus est enregistrée dans `MANIFEST_SHA256.txt` (tous les fichiers empaquetés sauf le manifeste lui-même). L'empreinte du ZIP complet est fournie dans le fichier compagnon `FulleGenBrain_3_dossier_complet.zip.sha256`, placé à côté du ZIP et en dehors de celui-ci pour éviter l'auto-référence cryptographique.
- Les tests sont locaux et ciblés : ils ne constituent pas une évaluation complète de FulleGenBrain_3.

Les preuves formelles présentes dans le texte sont des preuves mathématiques sous hypothèses explicites, non des preuves-machines Lean/Coq/Isabelle. La correspondance générale compilateur/interpréteur, la sémantique de tous les effets et l'intégration de bout en bout demeurent des obligations de construction/vérification clairement enregistrées; aucune capacité n'est retirée de la spécification pour cette raison.

## Reproduction

Depuis la racine de ce dossier :

```bash
bash validation/reproduce.sh
```

Environnement : Python 3, `pytest`, `pdflatex`, `pdfinfo`, et les dépendances standard Python. Le script reconstruit les `.tex` depuis les entrées amont embarquées, applique les extensions idempotentes, recompile les PDFs et relance tests et `compileall`.
