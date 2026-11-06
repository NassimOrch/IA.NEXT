# FulleGenBrain_4 — dossier de formalisation

Release documentaire et prototypes de référence — 25 octobre 2026.

## Livrables principaux

- `deliverables/formalisme_FulleGenBrain_4.tex` et `.pdf` : formalisation de l'architecture FulleGenBrain_4.
- `deliverables/theorie_programation_compositionnelle_2.tex` et `.pdf` : théorie autonome de programmation compositionnelle intégrée à l'architecture.
- `deliverables/prouve_et_tracabilite_FulleGenBrain_4.json` : registre des preuves, sources, décisions et validations de l'architecture.
- `deliverables/prouve_et_tracabilite_th_programmation_comp_2.json` : registre des preuves et obligations de la théorie.

- `interface_FulleGenBrain_4.tex` : spécification complète de l’interface UX/UI cible (chat, modèles, datasets, entraînement, LLM/RAG optionnels, observation, clonage, composition, mémoire, ASCRC, évaluation, audit et sécurité).
- `deliverables/interface_FulleGenBrain_4.pdf` : version compilée de la spécification d’interface (23 pages A4).

## Statut de l’interface

Le document d’interface décrit le produit cible et ses contrats d’intégration; il ne prétend pas qu’une application graphique complète est déjà implémentée. La compilation LaTeX et la vérification visuelle du PDF ont réussi. Les critères `UI-01` à `UI-20` sont des critères d’acceptation à tester pendant la construction de l’application. Les services de datasets, d’entraînement, de catalogue complet de modèles, de clonage et d’interface LLM/RAG nécessitent encore leur raccordement et une validation intégrée.

La navigation prévue utilise un chat comme point d’entrée, avec des espaces dédiés et des objets persistants reliés à leurs versions, traces et provenances. ASCR reste inchangé; ASCRC dispose d’une console opérationnelle séparée.

## ASCR et ASCRC : contrat de non-interférence

**ASCR d'eGenBrain v4 est conservé sans changement dans la formalisation** : le texte de sa sous-section dans le formalisme V4 est vérifié identique au texte d'origine V3. ASCRC est un mécanisme séparé, ajouté à FulleGenBrain_4 ; il consomme des descripteurs candidats via un adaptateur non destructif et ne modifie ni la définition d'ASCR ni son statut épistémique.

ASCRC régule l'admission opérationnelle, l'allocation, l'activation, la veille et le réveil. Il ne décide pas de la vérité d'un candidat. **Le budget de ressources reste un plafond dur** ; ASCRC est une politique d'allocation, pas un substitut au budget. Un candidat dormant n'est ni supprimé, ni rejeté, ni réfuté.

## Traitement de l'explosion combinatoire

La mise en veille réduit la population active, mais ne réduit pas à elle seule le nombre théorique de compositions. La spécification combine donc :

1. génération paresseuse et continuation/versionnement du générateur ;
2. filtrage précoce par syntaxe, types, contrats, effets et permissions ;
3. indexation par signatures, dépendances et cache ;
4. partage des sous-compositions ;
5. canonicalisation uniquement lorsqu'une équivalence pertinente est justifiée ;
6. allocation ASCRC avec budgets physiques, quotas éventuels d'exploration/vérification/maintenance, vieillissement et rotation ;
7. veille/réveil, checkpoint, révalidation des versions et invalidation des dépendances ;
8. utilisation des contre-exemples pour réorienter la recherche.

Les garanties d'anti-famine sont explicitement conditionnelles : ensemble fini et continuellement admissible, capacité suffisante, service continu et reprise sans perte. Aucune prétention de complétude pour tout espace infini n'est déduite de ces hypothèses.

## Modèle du monde

Le modèle du monde est **conditionnel à l'utilité décisionnelle mesurée**, pas un composant obligatoire par dogme. Les extraits O62/O63 fournis sont des résultats historiques rapportés : ils montrent pourquoi une erreur de prédiction ou une bonne métrique latente ne suffit pas à justifier son rôle dans le contrôleur. La promotion doit utiliser des expériences appariées, des baselines sans modèle, des modèles nuls/permutés, des ablations et un budget comparable. Ces campagnes historiques ne sont pas relancées par ce paquet.

## Absence de LLM/eLLM

La spécification n'introduit pas de dépendance d'exécution à un LLM ou eLLM. Toute idée reprise d'approches neuronales doit être reformulée en un mécanisme indépendant, explicite, auditable et évalué.

## Prototype et validation

- `reference_impl/ascrc_controller.py` : prototype local ASCRC, à budget scalaire, sans import/appel/modification d'ASCR.
- `reference_impl/living_composition_runtime.py` : prototype de mémoire vivante, veille/réveil, vagues, continuation et recherche reprenable.
- `reference_impl/world_model_gate.py` : porte de décision pour l'activation conditionnelle d'un modèle du monde.
- `tests/` : tests locaux pour ces prototypes.

Commande depuis la racine du dossier :

```bash
python -m pytest -q
python -m compileall -q reference_impl tests
python build_v4.py
bash scripts/build_v4_pdfs.sh
python scripts/verify_release_v4.py
```

La chaîne complète de reconstruction est `bash scripts/reproduce_v4.sh`.

## Lecture correcte du statut

La théorie et l'architecture sont formalisées et leurs documents compilés. Les prototypes locaux sont testés sur leur périmètre. Cela ne signifie pas que tous les 29 opérateurs syntaxiques sont implémentés dans un runtime unifié, que les théorèmes sont vérifiés par Lean/Coq/Isabelle, ni que l'intégration complète de FulleGenBrain_4 a été évaluée de bout en bout. Les registres séparent preuves sous hypothèses, invariants de spécification, observations de source, tests locaux et obligations ouvertes. Le statut ne préjuge ni succès ni échec futur.

## Reproductibilité et provenance

- Sources V3 exactes : `sources/upstream/`.
- Artefacts de l'ancienne release et journaux V3 : `sources/history/FulleGenBrain_3/`.
- Extensions V4 : `sources/extensions/`.
- Extraits historiques O62/O63 : `sources/evidence/`.
- Journal de tests, compilation, matrice, rendus et vérifications : `validation/` et `renders/`.
- `MANIFEST_SHA256.txt` couvre les fichiers de la release empaquetée, à l'exception du manifeste lui-même et de l'archive qui le contient. L'empreinte SHA-256 de l'archive est dans le sidecar distribué à côté du ZIP.
