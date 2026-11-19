# Rapport d'audit — PCH proximal et routage variationnel

## Description

Relecture approfondie du noyau PCH et des propositions de routage à partir des sources présentes dans `theorie_emp/PCH`, en distinguant les textes normatifs, variantes successives, prototypes expérimentaux et variantes incompatibles avec la contrainte non neuronale. Les deux textes centraux lus intégralement pour cette analyse sont `pch_routage/pch_route_variationnelle_final_v11.tex` (702 lignes) et `pch_routage/pch_routing_theory_extension.tex` (437 lignes). L'inventaire PCH plus large est décrit dans `PCH_FILE_BY_FILE_MAP_20261117.md`; il comporte 34 sources TeX de PCH et plusieurs branches/versionnements, qui ne sont pas toutes des preuves indépendantes.

## Architecture

Le noyau PCH local définit, pour un convexe fermé non vide `M_c` et un état `w`, une énergie quadratique associant fidélité à l'entrée, distance au contexte et régularisation ridge. Le minimiseur est unique par forte convexité. La famille v11 formalise ensuite une sélection multi-contextes par les valeurs réduites `V_c(w)=inf_u Jtilde_c(u;w)`, leur enveloppe inférieure, la partition en cellules de dominance, la relaxation entropique et un pré-routage proximal.

L'adaptation eSonde doit vivre dans l'espace `E_O=R^16` des observations explicitement nommées. Les constructions historiques à embeddings pré-entraînés, PCA sur embeddings, `llm_pch` et routeurs appris ne sont pas admissibles pour le runtime cible. La construction d'un catalogue multi-contextes sans apprentissage reste à définir avant toute implémentation de cette branche.

## Pipeline complet analysé

1. Définition des observables `w` dans l'espace des 16 canaux nommés.
2. Construction déterministe et versionnée d'un convexe `M_c` à partir de signatures admissibles, sans données TEST et sans embedding appris.
3. Calcul du minimiseur proximal `u_c*` et de la valeur réduite `V_c`.
4. Sélection exacte `argmin_c V_c`, conservation des ex æquo et de la marge.
5. Option de relaxation entropique `p_c ∝ exp(-beta V_c)` pour une expérience distincte.
6. Option de pré-routage par itérations proximales, avec facteur de contraction explicite et borne d'erreur avant décision.
7. Vérification de la projection par résidus primal, somme, non-négativité et KKT.
8. Comparaison expérimentale avec PCH désactivé et PCH à contexte unique; aucune supériorité n'est présumée.

## Commandes d'exécution

Relecture des sources : `sed -n '120,702p' theorie_emp/PCH/pch_routage/pch_route_variationnelle_final_v11.tex` et `sed -n '1,437p' theorie_emp/PCH/pch_routage/pch_routing_theory_extension.tex`.

Compilation des trois documents v8 : `pdflatex -halt-on-error -interaction=nonstopmode -output-directory=... formalisme_eSonde_v8.tex` (deux passes recommandées pour les références). Aucune exécution de génération du modèle n'a été réalisée pendant cet audit PCH.

## Résultats

### Résultats mathématiques qui tiennent sous les hypothèses explicites

- `J_c(.;w)` est fortement convexe de module `mu_c=1+2 lambda_ridge,c` lorsque `M_c` est convexe fermé non vide et les paramètres admissibles; l'existence et l'unicité du minimiseur suivent.
- La normalisation de v11 donne `Jtilde_c=g_c+||u-w||^2/(2 mu_c)`, donc `u_c*=prox_{mu_c g_c}(w)` et la valeur réduite est l'enveloppe de Moreau correspondante.
- Le routage dur par `argmin_c V_c(w)` est équivalent à la minimisation conjointe sur un ensemble fini de contextes et l'espace latent.
- La relaxation entropique a le minimiseur softmin `p_c=exp(-beta V_c)/sum_j exp(-beta V_j)` et converge vers un contexte unique lorsque celui-ci est strictement optimal.
- Le pré-routage proximal v11 est contractant sous son hypothèse; pour `Jtilde_c` fortement convexe de module `1/mu_c`, le facteur peut être explicité en `mu_c/(mu_c+eta_c)`.
- Le noyau quadratique simplifié eSonde conserve la solution fermée par projection `z*=Pi_C(w/(1+2 lambda_r))` et `u*=(w+2 lambda_c z*)/(1+2 lambda_c+2 lambda_r)`, avec facteur de contraction d'entrée `1/(1+2 lambda_r)`.

### Erreurs et limites du texte d'extension

- La proposition `R=1 iff w est déjà minimiseur` est fausse. Avec `R=Delta/(J(w;w)+epsilon)`, `epsilon>0`, `0<=R<=J(w;w)/(J(w;w)+epsilon)<1`. Si `w` est minimiseur, alors `Delta=0` et `R=0`. Avec epsilon positif, `R=1` est impossible.
- Le départage utilisant `D Pi_M(u*)` n'est pas défini en tout point : la projection sur un polytope peut ne pas être différentiable sur les strates de changement de face. Le projecteur limite `P0` et une règle quantitative pour « quasi-égalité » doivent aussi être spécifiés.
- La définition `T_{eta,alpha}` et l'hypothèse de monotonie du certificat court sont insuffisamment autonomes dans l'extension; la définition opératoire v11 peut être utilisée, mais elle doit être citée explicitement et ses constantes précisées.
- Les contextes historiques sont parfois construits à partir d'embeddings. Cela ne définit pas un catalogue multi-contextes admissible pour eSonde sans réseau appris.
- Les résultats d'optimalité et de contraction ne prouvent ni la qualité sémantique de `M_c`, ni une amélioration de cohérence ou de généralisation dialogique.

## Interprétation

Le noyau PCH proximal possède une base mathématique exploitable. Le routage v11 par valeurs réduites est le candidat de sélection le mieux fondé parmi les textes étudiés. En revanche, le score de gain normalisé et le tie-breaker différentiel de l'extension ne doivent pas être portés au runtime. L'option multi-contextes n'est pas prête à coder tant qu'une construction déterministe et non fuyante de `M_c` n'est pas spécifiée. La variante un seul hull peut être testée séparément, sans confondre contraction numérique et cohérence des réponses.

## Conséquences théoriques, conceptuelles et opérationnelles

- **Théorique :** conserver les preuves de forte convexité, Moreau et contraction avec les hypothèses; corriger l'égalité erronée et exclure la différentiabilité globale de la projection.
- **Conceptuelle :** PCH est un opérateur de purification/routage, pas une preuve de compréhension. Un score énergétique interne ne vaut pas jugement humain de pertinence.
- **Opérationnelle :** aucune dépendance embedding/PCA/routeur appris; solveur simplex déterministe avec certificats; journaliser les marges et les échecs; PCH désactivé tant que les tests appariés ne l'évaluent pas.

## Conclusion

Le noyau mathématique PCH est admissible comme candidat non neuronal sous construction correcte de ses ensembles. La route v11 par valeur réduite est conservée pour expérimentation. Les affirmations défectueuses de l'extension sont explicitement corrigées dans le formalisme v8 et gardées dans l'audit source pour traçabilité. Aucune preuve de gain de cohérence ni décision finale d'intégration multi-contextes n'est disponible à ce stade.

## Statut du modèle

`PCH_CORE_THEORY_REVIEWED`; `PCH_RUNTIME_NOT_IMPLEMENTED`; `MULTICONTEXT_PARTITION_UNRESOLVED`; `NO_FREE_GENERATION_RESULT`. La phase P0 reste `IN_PROGRESS` et n'est pas close.
