# Revue en cinq passes du formalisme eSonde v8

## Description
Revue statique et mathématique du document `Dmodel_eSonde_v8/formalism/formalisme_eSonde_v8.tex`, de la source v7 et du runtime. Les cinq passes sont consignées séparément. Une passe peut révéler des éléments à corriger; la présence de cinq rubriques ne vaut pas validation automatique.

## Passe 1 — Fidélité aux sources et identité des objets
**Vérifications :** checkpoint v6, identité Obsiss, dimension 16, noms des canaux comparés à `semantic_space.py`; code P/R et population comparés aux modules v6/v7; source OASST1 et profils comparés aux manifestes.

**Constat :** la distinction entre seize observations et un million d'identités Obsiss est correctement préservée. Les poids originaux ne sont pas transformés en coordonnées d'observation. Le routage unique `everyday_dialogue` est maintenant spécifié et raccordé au CLI.

**Statut : PASS avec réserves de couverture.** La correspondance exacte de chaque équation avec chaque branche du code doit encore être testée automatiquement sur un lot d'entrées.

## Passe 2 — Cohérence mathématique
**Vérifications :** relation d'équivalence induite par l'empreinte; théorème de factorisation; existence/unicité du minimiseur proximal PCH; formule fermée et constante de contraction.

**Constat :** les preuves de factorisation et de contraction sont cohérentes sous les hypothèses écrites (ensemble convexe fermé non vide en dimension finie, `lambda_r > 0`). La constante de contraction se simplifie bien en `1/(1+2 lambda_r)`. Les rangs, médianes et IQR ne sont pas assimilés à des probabilités ou à la vérité.

**Statut : PASS pour les résultats mathématiques énoncés.** Les propriétés sémantiques du polytope contextuel ne sont pas démontrées par ces théorèmes.

## Passe 3 — Complétude algorithmique de bout en bout
**Vérifications :** entrées/sorties, génération des candidats, observations, PCH, vote, arrêt, sérialisation et gestion des erreurs comparés aux fonctions runtime.

**Constat :** le pipeline général est défini et les fonctions v7 correspondantes existent. Toutefois, certaines règles doivent encore être entièrement figées dans le formalisme : construction exacte de tous les candidats et départages, définition normative des seuils d'arrêt, ordre déterministe de toutes les réductions et contrat d'échec de chaque sous-étape. Le solveur PCH certifié n'est pas encore raccordé au runtime.

**Statut : OPEN — passe non validée.** Ces lacunes sont des tâches d'implémentation/formalisation, pas des raisons d'abandonner les fonctionnalités.

## Passe 4 — Fuites, mémoire et provenance
**Vérifications :** splits par arbre, provenance train/validation/test, absence de paires brutes dans le profil, contexte courant explicitement fourni, poids immuables.

**Constat :** les manifestes OASST1 indiquent zéro chevauchement d'arbres; le profil prévu est agrégé et n'enregistre pas les paires brutes; le contexte de conversation est transitoire. Les fichiers source Parquet restent séparés des dérivés runtime.

**Statut : PASS sur les manifestes et le contrat; revalidation après construction du profil requise.**

## Passe 5 — Exclusion neuronale et falsifiabilité
**Vérifications :** imports et chemins actifs dans `src`, scripts runtime, dépendances et métadonnées; séparation des résultats mesurés, hypothèses et théorèmes.

**Constat :** le code actif inspecté ne référence pas de bibliothèque de réseau neuronal, d'embedding appris, d'optimiseur ou de rétropropagation. Les mentions textuelles de ces mécanismes sont des exclusions contractuelles. Les prototypes historiques incompatibles restent en audit et ne sont pas appelés.

**Statut : PASS statique provisoire.** Une inspection dynamique des dépendances et appels indirects sera faite avant gel de livraison.

## Résultat global des cinq passes
Le formalisme n'est pas déclaré final : la passe 3 reste ouverte et les tests de parité des équations ne sont pas encore exécutés. Les erreurs de compilation LaTeX ont été corrigées; `pdflatex -halt-on-error` réussit sur les trois documents v8. Le statut global est **FORMALISME EN REVUE — NON GELÉ**.

## Template de rapport
Description / architecture / pipeline complet / commandes d'exécution / résultats / interprétation / conséquences théoriques, conceptuelles et opérationnelles / conclusions / statut du modèle.

## Addendum PCH — relecture ciblée du 17 novembre 2026, 13:49 (+01:00)

La lecture intégrale des deux textes de routage PCH (`pch_route_variationnelle_final_v11.tex`, 702 lignes; `pch_routing_theory_extension.tex`, 437 lignes) ajoute les constats suivants à la passe 2 :

- Le noyau proximal et la valeur réduite de Moreau de v11 sont cohérents sous les hypothèses de convexité, fermeture, non-vacuité, dimension finie et paramètres explicites. Le facteur du pré-routage proximal normalisé est `mu/(mu+eta)` quand la fonction normalisée a le module de forte convexité `1/mu`.
- La formule fermée du PCH simplifié eSonde est correcte. La preuve traite désormais explicitement le cas `lambda_ctx=0`, où la fonction réduite en `z` est dégénérée mais le minimiseur `u*` reste unique et indépendant de `z`.
- Le score de gain normalisé de l'extension ne peut atteindre 1 avec `epsilon>0`; au point minimisant le gain est nul. Son égalité prétendue est exclue.
- Le départage via `D Pi_M` n'est pas défini sur toutes les strates d'un polytope. `P0` et la tolérance de quasi-égalité ne sont pas définis de façon autonome. Cette règle est exclue.
- La route par valeurs réduites est ajoutée comme candidat de laboratoire avec paramètres de régularisation communs pour rendre les comparaisons plus identifiables; elle n'est pas implémentée et ne prouve aucune cohérence sémantique.

**Mise à jour du statut :** la passe 2 PCH ciblée est `PASS_WITH_SOURCE_CORRECTIONS`; la passe 3 reste `OPEN` (solveur, partition de contextes et parité avec runtime absents). Les cinq passes globales ne sont donc toujours pas closes et le formalisme reste `UNDER_REVIEW_NOT_FROZEN`.

## Addendum — formalismes connexes et défauts source (17 novembre 2026, 14:xx +01:00)

La revue ciblée des formalismes connexes est archivée dans `P0_FORMALISMES_NONNEURAL_REVIEW_20261117.md` et reliée au laboratoire. Elle ne ferme pas la passe 3. Principales implications : typage/provenance eGenBrain utilisables comme contrat et preuve bornée; toutes les voies PyTorch/MLP/Transformer/Hugging Face de NGeGenBrain et eLLM exclues; FulleGenBrain et AAM ne fournissent pas de validation conversationnelle E2E; la discipline ORDER80.2.2 impose de distinguer synthèse documentée et résolution vérifiée; la théorie des empreintes fournit les fibres et la factorisation conditionnelle, mais ses axiomes ouverts sur mémoire ontologique ne deviennent pas un moteur de réponse.

Le document source `th_emp_observation_formalisme_0.tex` (495 lignes) a été testé sur une copie diagnostique. Compilation originale : conflit de redéclaration de `\\Im` via `\\DeclareMathOperator`; après retrait de cette ligne dans la seule copie de diagnostic, le compilateur expose une expression mathématique mal délimitée menant à `Double subscript` sur `\\Mevo_{t+1}`. L'original source n'a pas été modifié. Le contenu conceptuel demeure exploitable après séparation des définitions, axiomes, conjectures et objets ouverts; il ne peut pas être cité comme un document LaTeX compilable sans correction.

La revue AAM O94.6 révèle une divergence documentaire de comptage (449 réussites dans le reçu/audit, 448 dans une autre description, et 449 ailleurs dans le README); elle est conservée comme point ouvert, à réconcilier depuis les journaux et reçus bruts. La revue FulleGenBrain 4 confirme explicitement `END_TO_END_INTEGRATION_NOT_EVALUATED` et `SPECIFICATION_ONLY_NOT_APPLICATION_IMPLEMENTATION` pour l'interface. Ces statuts ne sont pas extrapolés.

**Registre global :** la passe 3 reste `OPEN`; le formalisme global demeure `UNDER_REVIEW_NOT_FROZEN`. L'ajout de ce mapping théorique n'est ni un passage de phase ni un résultat de génération.
