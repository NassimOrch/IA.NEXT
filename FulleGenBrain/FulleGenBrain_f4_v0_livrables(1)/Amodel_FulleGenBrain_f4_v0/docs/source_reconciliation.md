# FulleGenBrain_f4_v0 — réconciliation des sources

**État :** inventaire et lecture des points canoniques effectués ; les adaptations restent soumises aux tests différentiels de leur phase respective.  
**Date de l'audit local :** 26 octobre 2026.  
**Entrée principale :** `source_orderX_0.zip` — 493 682 442 octets, 17 entrées ZIP, intégrité `unzip -tq` : PASS.  
**Règle de gouvernance :** aucune lignée historique n'est considérée comme une implémentation interchangeable de FulleGenBrain. Chaque mécanisme réutilisé possède une provenance et une portée explicites.

## 1. Hiérarchie normative

| Priorité | Source | Autorité | Conséquence d'implémentation |
|---|---|---|---|
| 1 | `formalisme_FulleGenBrain_4.tex` | Architecture métier et pipeline de FulleGenBrain 4 | Le runtime, le cycle de vie, l'épistémique, la recherche, les ressources et la provenance doivent suivre ce document. |
| 2 | `theorie_programation_compositionnelle_2.tex` | Sémantique de composition, AST, contrats, effets, opérateurs et recherche | Les opérateurs sont interprétés selon leurs contrats ; l'absence de code existant ne permet pas d'en supprimer un. |
| 3 | Sources historiques ORDER, AAM, eGenBrain | Implémentations spécialisées et éléments de preuve pour des mécanismes attribués | Réutilisation via adaptateurs à contrat explicite ; différences et versions conservées. Une ressemblance conceptuelle ne constitue pas une preuve d'équivalence. |
| 4 | `interface_FulleGenBrain_4.tex` | Cible UX et 20 critères d'acceptation | Pilote les vues et parcours, sans prévaloir sur l'architecture métier. Un écran ne déclare pas une capacité opérationnelle absente. |
| 5 | `bank_idee_full_models_1.json` | Réservoir d'idées supplémentaire | Source d'hypothèses à examiner, jamais source de vérité ni remplacement du formalisme. Chaque idée retenue requiert motivation, contrat et test. |

## 2. Sources canoniques FulleGenBrain 4

### Architecture

Le formalisme V4 décrit quatre plans coordonnés : structure/catalogue, dynamique/runtime, évolution/découverte, mémoire/ressources. Il distingue statuts épistémiques et opérationnels, et exige provenance complète, validation indépendante, erreurs non effacées, checkpoints et reprise. L'ordre d'autorité ci-dessus évite que la GUI ou une implémentation historique modifie silencieusement les règles architecturales.

### Théorie de composition

La grammaire contient exactement 29 opérateurs racines : `Id`, `Call`, `Seq`, `Par`, `If`, `Map`, `Fold`, `Loop`, `Choose`, `Verify`, `Observe`, `Probe`, `Recover`, `Txn`, `Checkpoint`, `Revoke`, `Compose`, `Transform`, `Fix`, `Select`, `Synthesize`, `Hibernate`, `Wake`, `Compress`, `Summarize`, `Restore`, `EmitWave`, `ReceiveWave`, `ResumeSearch`. Le code livré doit implémenter chaque opérateur ou rendre explicitement `BLOCKED`/`UNSUPPORTED` avec diagnostic ; aucun constructeur muet n'est admissible.

Points de sémantique maintenus : `Choose` expose les alternatives, et ne choisit pas implicitement ; `Select` est une politique de préférence et non un vérificateur ; `UNRESOLVED` ne signifie pas impossible ; `Compress` est sans perte et vérifie la reconstruction ; `Summarize` est dérivé avec perte contrôlée et ne remplace pas la source ; hibernation/réveil ne changent pas le statut épistémique ; les effets externes non idempotents ne peuvent pas être annulés par un simple rollback mémoire ; les checkpoints de recherche conservent signature, versions, grammaire, graines, statistiques et budget.

### Prototype de l'interface

Les critères UI-01 à UI-20 portent notamment sur tâches/objets stables, erreurs/partiels, import contrôlé de données, séparation des partitions, entraînement, import en quarantaine, connecteurs LLM/RAG optionnels, provenance des citations, observation/clonage, édition des compositions, mémoire et ASCRC, audit exportable, accessibilité WCAG 2.2 AA, responsive, disponibilité explicite des adaptateurs et fonctionnement natif hors réseau. Le fichier source dit lui-même qu'il s'agit d'une spécification cible, pas d'une preuve d'implémentation. Tous les critères sont gardés dans la matrice UI du projet ; ceux qui nécessitent un backend d'entraînement ou un audit accessibilité externe restent signalés séparément.

## 3. Réconciliation des modèles historiques

| Lignée / version livrée | Caractéristiques confirmées dans les sources | Usage envisagé dans FulleGenBrain_f4_v0 | Restrictions / preuves requises |
|---|---|---|---|
| **AAM O82_0 / ROCA-D** (`Dmodel_AAM_O82_0`) | Runtime standard-library-first ; observation dégradée, empreintes partielles, retrieval mémoire, suffisance décisionnelle, politique lexicographique, bundles concurrents, correction/CEGIS, capsules de compétences, auto-observation, discovery de probes, décomposition, root-retest, recovery/replay, ledger. CLI `o82`. | Adaptateur de compétences pour observation, acquisition, vérification de suffisance, correction et reprise. Conserver ses contrats et événements comme lignée source. | Exécuter tests en provenance ; ne pas coder une réponse métier spécifique à la place du processus d'observation. Un horizon `max_steps` court est un arrêt de contrôle, non une impossibilité. Vérifier les effets et l'isolation avant exécution intégrée. |
| **AAM O82_2** | Archive d'une version ultérieure et documentation/tests ; `pyproject.toml` indique Python 3.10–3.13 et aucune dépendance de projet déclarée. | Comparaison de contrats/comportements et éclairage des évolutions d'AAM. | Ne pas supposer que l'archive documentation/runtime contient tout O82_0 ; comparer fichiers et versions avant choisir du code. |
| **AAM O94.6** | Dans l'archive fournie, la pièce retrouvée est nommée `Amodel_AAM_O94_6 - Copie.zip` : artefact d'audit, pas le `Dmodel` exécutable attendu. | Source d'audit, preuves et pistes pour des contrôles. | Ne pas présenter la version exécutable O94.6 comme intégrée tant que son paquet Dmodel n'est pas fourni/inspecté. |
| **ORDER O76-1.1** | Moteur mathématique exact spécialisé ; preuves/certificats rejouables par vérificateur indépendant ; états `PROVEN`, `REFUTED`, `UNRESOLVED`; stdlib seulement selon le README. La licence incluse est une note de provenance, pas une licence copyright complète. | Adaptateur spécialisé de vérification mathématique et certificat, exécuté sous contrat isolé. | `UNRESOLVED` signifie qu'aucun certificat n'a été trouvé dans le portefeuille/budget testé ; ne pas le traduire en impossibilité. La base de confiance du vérificateur doit rester documentée. Ne pas réutiliser le calcul pour certifier des domaines hors contrat. |
| **ORDER 80.2.0** | Lignée de référence dans les manifestes des versions suivantes. | Référence historique dans une comparaison versionnée. | Pas sélectionnée par défaut lorsque le correctif 80.2.2 est présent ; conserver le manifeste et pouvoir retracer les différences. |
| **ORDER 80.2.2** | Orchestration hiérarchique observer → résoudre → observer plus → décomposer → retest racine ; distingue `DOCUMENTED_INSIGHT` d'une solution de domaine vérifiée ; stdlib-first selon README. | Orchestration/recherche documentaire comme spécialiste facultatif, avec vérificateurs de domaine explicites. | Une insight multi-source n'est pas une preuve. L'accès au web doit être une permission explicite ; le chemin natif doit fonctionner sans réseau. |
| **ORDER 80.4.7** | Étude de modèle modulaire (spécialistes + maître, probes `surface`/`focused`, acquisition black-box/OIFL, RAG+raisonnement). Rapport documente teacher, données, hash et métriques de campagne. | Inspirer les interfaces d'observation de surface/focalisée et les expériences de spécialisation, sans les imposer à tout problème. | Résultats empiriques limités à ses données et conditions ; l'expérience ne prouve pas la généralisation universelle. Ne pas inclure une dépendance ML lourde dans le noyau pour reproduire uniquement une méthode expérimentale. Les mesures de cette lignée doivent être reproduites avant toute prétention de non-régression. |
| **eGenBrain v4** | Runtime logique et graphe de faits/règles avec stockage SQLite et mesh typé ; chemin principal standard library/SQLite, pas de LLM obligatoire ; démarrage vierge explicitement supporté sans fabriquer de données. `ASCR` et la base MG historique sont distingués. | Adaptateur logique/relations et fallback spécialisé si son bundle et ses données sont valides ; maintenir ASCR séparé d'ASCRC. | Le manifeste déclare une base de 1 648 779 264 octets en deux fragments ; la livraison inspectée ne contient que le premier ZIP de runtime/data et aucune seconde partie correspondante. L'adaptateur doit vérifier manifestes, SHA256, `PRAGMA integrity_check` et FK, et rester `BLOCKED` pour cette base héritée tant que les fragments complets manquent. Le noyau FulleGenBrain ne doit pas dépendre de cette base. |
| **ORDER/AAM/eGenBrain autres archives d'audit** | Des paquets d'audit et dossiers de preuves sont inclus séparément des runtimes. | Référence pour tests, historique, métriques et vérifiabilité. | Les résultats présents dans les audits sont des observations historiques, pas résultats produits par la nouvelle implémentation. Toujours séparer « rapport source » et « re-test local ». |

## 4. Banque d'idées

`bank_idee_full_models_1.json` se déclare comme contenant 190 idées : 88 héritées d'une banque `bank_0` substitutive disponible et 102 nouvelles idées. Le champ source précise que ce fichier ne constitue **pas** une reconstitution de l'original `bank_0` manquant. Les idées servent à proposer des pistes, jamais à remplacer la spécification. Une idée retenue doit être ajoutée à un registre d'évolution avec origine, hypothèse, justification, impact architectural, tests discriminants, mesure, décision (acceptée/rejetée/en attente) et version.

## 5. Gaps de livraison et règles juridiques

1. `Dmodel_eGenBrain_v4_part2.zip` n'est pas trouvé dans l'arbre fourni alors que le manifeste réclame deux fragments de données. Aucun octet de base manquant ne sera synthétisé.
2. `Amodel_AAM_O94_6` est présent en audit ; un runtime Dmodel AAM O94.6 complet n'est pas identifié dans le paquet fourni.
3. Les sources ne portent pas toutes une licence redistributive claire. Le texte `LICENSE.txt` d'ORDER O76 est une note et ne vaut pas automatiquement concession de droits. Le code neuf du projet reçoit une licence non commerciale séparée, tandis que les copies upstream doivent conserver notices/conditions d'origine, être étiquetées provenance, et ne pas être redistribuées sans autorisation suffisante.
4. Les résultats de test inscrits dans les anciens rapports sont des affirmations propres à la source ; leur reproduction dans cette livraison produit des journaux séparés, avec versions, commandes, entrées, sortie, temps, code retour et hashes.

## 6. Règle de validation d'une adaptation

Une adaptation n'est acceptée que si : (a) le mécanisme source est identifié par chemin/version/hash ; (b) un contrat source et un contrat cible sont écrits ; (c) les entrées positives, frontières, erreurs, états partiels et cas non résolus sont comparés sur un corpus fixe ; (d) des vérificateurs indépendants ou tests différentiels sont utilisés là où le domaine le permet ; (e) les métriques et le protocole sont fixés avant l'examen des tests holdout ; (f) toute différence est expliquée ; (g) les résultats restent `PASS`, `FAIL`, `NOT_RUN` ou `BLOCKED` avec preuve. En l'absence de preuve d'équivalence, le composant est étiqueté adaptation exploratoire et ne peut pas prétendre reproduire strictement le modèle source.

## 7. Conclusion de réconciliation

FulleGenBrain_f4_v0 doit être un runtime natif compositionnel autonome avec adaptateurs spécialistes à activation explicite. Le premier incrément ne doit ni dépendre d'une base legacy manquante, ni assimiler une observation à une preuve, ni confondre préférence et certificat, ni laisser l'interface dicter l'architecture. La prochaine étape d'ingénierie autorisée est le noyau AST/contrats et la matrice opérateur–code–test, après clôture des phases formelles et de gouvernance.


## ASCR preservation and ASCRC adaptation
The eGenBrain V4 ASCR-bearing files are checked against the source archive manifest; machine-readable hashes and byte counts are in `spec/evidence/ascr_source_preservation.json`. The historical scalar ASCRC and world-model gate references under `spec/upstream/reference_impl/` are maintained unchanged. The runtime `src/fullegenbrain/runtime/ascrc.py` is a distinct vector-budget adaptation, verified by scalar-projection cases and independent invariant tests; this is not a claim of universal behavioral equivalence.

## P09 — adapters, provenance and licenses

The implemented specialist registry and its source/license inventory are `spec/evidence/specialist_adapter_matrix.json` and `spec/evidence/specialist_source_license_inventory.json`. The checked P09 closure is `spec/evidence/P09_acceptance_gate.json`; detailed results are in `docs/reports/P09_specialist_adapter_validation_report.md`. These records explicitly distinguish executable, partial, comparison-only and audit-only artefacts. Missing `eGenBrain_v4.sqlite3.part02` is surfaced and never synthesized. Upstream license grants are not assumed from the presence of source code or a provenance note.
