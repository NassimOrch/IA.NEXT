# Audit scientifique des sources EX3–EX10 et fondements EX11

Date de l'audit : 2026-11-03 (Africa/Algiers)  
Périmètre : archives en lecture seule fournies dans `last_sources_3.zip`, formalismes extraits et rapport `rapport_analyse_ex3_ex10.tex`. Les sources historiques ne sont pas recopiées dans le livrable EX11.

## 1. Chaîne de provenance et hiérarchie des preuves

Les quatre entrées utilisateur et leurs SHA-256 sont consignés dans `INPUT_SHA256.txt` :

- `last_sources_3.zip` : archive historique qui contient les ZIP EX4–EX10, les prompts EX3–EX9, les formalismes et références `sources_ng_adapt_0.zip` ;
- `datasets_arff.zip` : les 13 jeux de données nouveaux pour EX11 ;
- `rapport_analyse_ex3_ex10.tex` et son PDF : analyse secondaire.

La source de vérité pour un chiffre expérimental est l'association données + code exécuté + configuration + checkpoint + prédictions + registre. Un rapport ou un message de suivi n'est pas un substitut à ces artefacts. Les résultats historiques sont utilisés pour formuler des hypothèses, jamais comme preuve d'un résultat EX11.

## 2. Fondations théoriques générales : empreinte et observation

Les deux textes fournis dans `sources_ng_adapt_0.zip` sont traités comme les fondements conceptuels du projet, distincts des formalismes directement exécutés dans EX11.

### 2.1 `DDD_Base_theorie_des_empreintes_complete_order_5.tex`

Le socle définit une empreinte non comme une essence intrinsèque de l'objet, mais comme le résultat d'un protocole d'observation : pour un contexte `P`, un objet `x` et une famille de sondes finie `F_K`, l'observation associe le tuple des réponses des sondes. L'égalité des empreintes induit une relation d'indiscernabilité, dont les classes sont les fibres observationnelles ; le quotient identifie les objets qui ne peuvent être distingués par la famille de sondes considérée. Le théorème de factorisation exprime qu'une représentation qui est constante sur ces fibres passe au quotient.

La théorie introduit aussi une échelle croissante de familles de sondes, une filtration des partitions et des seuils de séparation. Une sonde supplémentaire n'apporte donc une distinction nouvelle que si elle raffine effectivement les fibres (et pas simplement parce qu'elle ajoute des coordonnées ou paramètres). Cette distinction motive, dans EX11, les contrôles d'équivalence D1/D2, l'ablation LOO des sondes et l'attention portée aux sondes redondantes.

Le texte distingue les statuts épistémiques (définition, hypothèse, conjecture, théorème démontré, observation, résultat expérimental, interprétation, piste et contre-exemple). EX11 reprend explicitement cette discipline : les performances mesurées ne sont pas converties en propositions théoriques, et un résultat local n'est pas promu en généralité sans preuve.

### 2.2 `NGeGenBrain_observation_formalisme_full_0.tex`

Le formalisme d'observation approfondit le contrat entre objets, contextes, mesures et sondes. Il sépare explicitement empreinte informationnelle, observation complète et état interne ; observation exacte, bruitée et stochastique ; état et trajectoire ; stabilité, stationnarité et invariance ; équivalence observationnelle et équivalence mécaniste. Il insiste sur le fait que des observations finies compatibles n'identifient pas nécessairement un mécanisme unique et n'impliquent pas une généralisation universelle.

Il formalise les vues multiples, la complémentarité des sondes, la sélection active de sondes et les interventions. Une intervention est distincte d'une observation passive : ses effets ne sont interprétables causalement que si les conditions d'identifiabilité, les contrôles appariés, la provenance et les éventuels facteurs de confusion sont explicités. Il sépare les niveaux d'ajustement, de sélection et de test indépendant ; les métriques de qualité, de ressources et de fidélité ne sont pas substituables.

### 2.3 Traduction opérationnelle et limite d'interprétation

Dans EX11, les `AdaptiveRBF` sont des mécanismes paramétriques concrets destinés à approximer des fonctions et des tâches. Ils sont utilisés comme sondes au sens opérationnel du projet, mais leurs sorties ne sont pas automatiquement des « empreintes sémantiques certifiées » au sens du traité. EX11 mesure la qualité, les coûts, l'équivalence et la contribution des composants ; il ne démontre pas à lui seul les théorèmes de factorisation/identifiabilité du cadre général. Les deux niveaux restent reliés conceptuellement, mais leurs statuts de preuve demeurent séparés.

## 3. Lignée des prompts méthodologiques

Les prompts EX3–EX9 convergent sur les règles suivantes, reprises dans `prompt_ex11.json` :

1. ne présumer ni réussite ni échec ;
2. comparaison appariée sur données, partitions, seeds et prétraitement comparables ;
3. compter les paramètres réellement présents à l'inférence, y compris routeur, centres, largeurs, projections, buffers persistants et prétraitement ;
4. comparer à un MLP apparié et à un MLP dont le nombre de paramètres est effectivement supérieur ou égal à quatre fois celui de la variante testée ;
5. mesurer la performance et les ressources, pas seulement le nombre de paramètres ;
6. ajuster transformations, imputation, encodage, KMeans et centres sur train uniquement ;
7. utiliser des prédictions OOF pour tout méta-apprentissage supervisé évitant l'auto-prédiction ;
8. sceller le test jusqu'au gel du code, du modèle, du checkpoint et du scorer ;
9. conserver les runs défavorables, échoués, interrompus, invalides ou sous quota ;
10. fournir scripts réellement exécutés, configs, logs, artefacts, prédictions et hashes ;
11. interdire manipulation, sélection opportuniste, falsification, omission et sabotage direct ou indirect ;
12. ne pas présenter une estimation analytique de FLOPs ou une mesure CPU comme une consommation d'énergie.

Les exigences se renforcent au fil des expériences. EX4–EX5 insistent sur le coût total, l'état des optimiseurs, les ablations et le partage adaptatif/fixe. EX6–EX7 mettent l'accent sur OOF strict, composition en couches, coût complet des spécialistes et reproductibilité des variantes. EX8 formalise les familles récursives/hybrides, les comparateurs et les mesures de ressources ; EX9 pousse les validations sur domaines distincts ; EX10 impose la traçabilité de holdout et une séparation explicite des mesures de ressources fiables, contestées et absentes.

## 4. Formalisme `th_sondes_core_test_1.tex` : CNG et CNC

### 4.1 Sonde AdaptiveRBF

Pour une entrée `x` et une sonde `i` :

\[
 z_i(x)=\tanh(W_i x+b_i),\qquad
 \phi_{ik}(x)=\exp\!\left(-\frac{\|z_i(x)-c_{ik}\|_2^2}{2\sigma_{ik}^2}\right),
\]
\[
 P_i(x)=V_i\phi_i(x)+a_i.
\]

La dimension latente spécifiée est `d=4`, avec `K=8` centres. Les centres sont initialisés par KMeans sur les représentations train seulement et restent entraînables ; les largeurs doivent être strictement positives (paramétrisation softplus). La comptabilité doit distinguer paramètres entraînables, buffers et taille totale du chemin d'inférence.

### 4.2 CNG multi-sondes

Pour `M` sondes :

\[
 h(x)=[P_1(x);\ldots;P_M(x)],\quad
 f_{\mathrm{mean}}(x)=\frac1M\sum_iP_i(x),\quad
 f_{\mathrm{learned}}(x)=W_ch(x)+b_c.
\]

Familles : A1 (M=1), A2 (M=2,4,7, moyenne fixe), A3 (M=2,4,7, composeur linéaire appris), MLP apparié et MLP GE4X. A6 est une sonde directe ; elle ne doit pas être recomptée comme réplication distincte si elle est mathématiquement identique à A1.

Fonctions :

- `f1(x)=sin(x)`, `x∈[-π,π]` ;
- `f2(x1,x2)=x1*x2`, `[-2,2]^2` ;
- `f3(x1,x2)=x1^2+x2`, `[-2,2]^2` ;
- `f4(x1,x2,x3)=sin(x1*x2)+x3`, `[-2,2]^3` ;
- `f5(x1,x2)=sin(x1)+0.5*cos(2*x2)`, `[-π,π]^2` ;
- `f6(x1,x2,x3)=x1*x2+0.25*x3^2`, `[-2,2]^3`.

Le protocole formel exige 4096 points train, 1024 validation et 8192 test scellé par fonction et seed. Le profil d'extrapolation/boundary est séparé de la sélection in-domain. Les seeds principales sont `[1501,1607,1717,2029,3037,4099,4517,5003,6011,7013]`.

Les ablations leave-one-probe-out (LOO) doivent distinguer : (F) sondes restantes gelées et composeur réappris ; (R) système réduit réentraîné depuis une initialisation indépendante. Sans ces ablations, les contributions individuelles et la coopération ne peuvent pas être déclarées établies.

### 4.3 CNC par composition

Un graphe `G=(V,E)` applique des approximations neuronales d'opérateurs aux sorties de prédécesseurs. Les opérateurs sont `ADD`, `SUB`, `MUL`, `DIV`, `EXP`, `LOG`, avec domaines :

- ADD/SUB/MUL : opérandes dans `[-2,2]` ;
- DIV : numérateur `[-4,4]`, dénominateur `[-1,-0.25] ∪ [0.25,3]` ;
- EXP : entrée `[-2,2]` ;
- LOG : entrée `[0.1,9]`.

Graphes de réplication : `g1=ab+exp(c)`, `g2=ab/(c+1)` avec `|c+1|≥0.25`, `g3=log(a²+b²+1)+exp(c)`. Compositions inédites : `g4=exp(ab)+c`, `g5=log(ab+5)+c²`. Les graphes g1–g3 servent à apprendre/sélectionner ; g4–g5 ne sont générés/scorés qu'après gel.

Variantes : C1 (spécialistes gelés), C2 (ajustement conjoint depuis les spécialistes), C3 (MLP direct), C4 (AdaptiveRBF directe), C5 (oracle natif exact, pas un modèle appris). Le pipeline doit tracer l'erreur par nœud et sa propagation jusqu'à la sortie.

## 5. Formalisme `Replica_U_0.tex` : REPLICA-U

REPLICA-U constitue une expérience séparée du CNG/CNC. Il définit une chaîne :

1. backbone résiduel compact ;
2. banque de spécialistes RBF entraînés sur train uniquement ;
3. teacher conjoint et routeur dense utilisant la représentation du backbone, les résidus des spécialistes et leur désaccord ;
4. apprentissage du student autonome par distillation à partir de logits teacher OOF, avec les labels réels ;
5. mesure du chemin d'inférence du student sans spécialistes, routeur ou teacher.

La forme du teacher est `z_T=z_B+Σ_i α_i r_i`, et chaque sortie spécialiste auxiliaire `z_i=z_B+r_i`. Les poids `α_i` sont normalisés ; les spécialistes doivent être owner-excluded lorsqu'ils produisent les cibles de distillation du train. La comparaison doit comprendre backbone seul, teacher, students, MLP apparié et MLP GE4X. Le coût de production du teacher doit être séparé du coût d'inférence du student.

## 6. Résultats historiques qui motivent EX11 (sans préjuger des résultats)

### EX8 v010

Le rapport historique B10 donne une log-loss moyenne de `0.04138964`, B11 `0.04442526` et le MLP apparié `0.05473` sur Wisconsin ; B10 gagne face au MLP sur les cinq seeds de cette campagne. Cette observation est intéressante mais ne constitue pas à elle seule une preuve de généralisation externe. Le profil historique indique que B10 est plus lent que B11 à batch 1 (ordre de grandeur rapporté : 0.332 ms contre 0.116 ms). La qualité et la vitesse pointent donc dans des directions différentes.

### EX9

Les domaines synthétiques XOR8, concentric2 et rotated_moons2 ne reproduisent pas l'avantage Wisconsin de façon générale ; les MLP dominent les sondes sur les holdouts observables. L'évaluateur XOR8 a échoué avant prédiction : aucun score XOR8 ne doit être inventé. Les mesures de latence rapportées montrent également des candidates plus lentes que les MLP sur ce protocole. Les conclusions de ressources restent limitées quand mémoire/énergie n'ont pas été mesurées de façon isolée.

### EX10

Le rapport final annonce 460 runs CNG, 90 runs CNC et 1 695 évaluations holdout, avec un état de conformité des ressources non uniforme. CNG a des succès localisés (notamment f2 dans certains régimes) mais pas de supériorité uniforme ; l'extrapolation reste un point faible. B10 reproduit un résultat positif sur Wisconsin, mais perd sur SMS. Les lignes de ressources comportent des mesures déclarées `CONTENDED_OR_UNVERIFIED` : elles ne peuvent pas être traitées comme des preuves matérielles propres.

## 7. Choix scientifique EX11

Les trois branches ne sont pas fusionnées :

- REPLICA-U teste si un teacher assisté par spécialistes produit un student autonome performant ;
- CNG/CNC testent la capacité des sondes à approximer des fonctions et à composer des opérations ;
- D1/D2/D3 testent si la vectorisation exacte et le partage d'encodeur réduisent effectivement le coût logiciel.

La troisième expérience répond directement au décalage révélé par EX8–EX10 : peu de paramètres ne signifie ni peu d'opérations, ni peu d'accès mémoire, ni faible latence. D1 et D2 doivent être fonctionnellement équivalents ; D3 est une variante architecturale qui doit être comparée en qualité et en ressources, sans présumer qu'elle est équivalente.

## 8. Limites explicites

Le corpus historique ne permet pas de prouver l'absence d'exposition humaine des 13 nouveaux jeux. La famille PROMISE contient des recouvrements de vecteurs entre jeux et ne fournit pas cinq domaines statistiquement indépendants. GINA préserve sa frontière historique Train/Valid et dérive de la reconnaissance de chiffres. Les résultats EX11 sont rapportés au niveau de complétion réellement atteint ; les runs manquants portent le statut `NOT_RUN` ou `INCOMPLETE_QUOTA`. Le test scellé ne sera ouvert qu'après gel.
