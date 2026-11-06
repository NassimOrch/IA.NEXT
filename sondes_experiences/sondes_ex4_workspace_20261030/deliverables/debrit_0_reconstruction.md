# Reconstruction méthodique de `debrit_0.txt`

**Objet :** récupérer les éléments scientifiques utiles sans transformer des résumés textuels en résultats bruts vérifiés. Source lue : `last_sources.zip::debrit_0.txt` (68 394 octets ; SHA-256 consigné dans `inputs/source_manifest.json`).

## 1. Échelle de confiance

- **Vérifiable dans les archives EX2 :** code, manifestes, prédictions, métriques et rapports qui sont effectivement présents dans `sondes_research_workspace_final.zip`.
- **Rapporté dans les débris :** nombres et conclusions décrits dans `debrit_0.txt`, mais dont les prédictions, checkpoints, scripts et splits EX3 ne sont pas fournis. Ce sont des éléments de reconstruction, pas des observations qu'EX4 peut certifier.
- **Hypothèse à tester :** mécanisme suggéré par les observations ou par les remarques de recherche ; ne pas le présenter comme une conclusion.

L'archive téléversée ne contient pas les snapshots du workspace EX3 v001–v007 ni les fichiers bruts de ses campagnes. Plusieurs passages de `debrit_0.txt` se répètent et certains statuts sont contradictoires ou décalés par rapport aux dernières activités. Les valeurs EX3 ci-dessous portent donc la marque `rapporté_non_vérifiable`.

## 2. Expériences antérieures récupérables dans les débris

### 2.1 Contrôles de base et importance de la capacité

Le texte distingue plusieurs architectures A–K : MLP conventionnel ; sondes RBF locales ; sondes avec coordination globale ; variantes d'activation `tanh` ; variantes avec boucle d'observation/adaptation ; contrôle RBF fixe K. Le contrôle K ne possède que **17 paramètres** dans le benchmark binaire 2D, contre **65 à 72** pour A–E. Le texte avertit correctement que K teste l'effet de bases fixes et non une supériorité à capacité égale.

**Leçon récupérée :** les comparaisons de qualité doivent être séparées des comparaisons à capacité égale. Le nombre de coefficients et le coût du calcul doivent toujours accompagner accuracy et log-loss.

### 2.2 Reproduction `two_moons`

Le rapport affirme une reproduction exacte du bundle original (CSV/JSON identiques à l'archive) et indique les moyennes suivantes, sur cinq graines et une partition commune :

| Modèle | Accuracy | ROC-AUC | Log-loss |
|---|---:|---:|---:|
| MLP | 95,87 % | 99,19 % | 0,1109 |
| Sondes RBF adaptatives | 96,01 % | 99,06 % | 0,1174 |
| Sondes fixes | 86,23 % | 91,99 % | 0,3550 |

**Interprétation rapportée :** la sonde adaptative gagne légèrement en accuracy (+0,135 point environ), mais perd en log-loss par rapport au MLP. L'apprentissage des paramètres RBF semble utile par rapport au contrôle fixe (+9,78 points d'accuracy), sans isoler à lui seul l'ensemble des mécanismes.

**Leçon :** ne jamais réduire l'objectif à l'accuracy. La log-loss révèle la qualité des probabilités et peut départager des modèles de même accuracy.

### 2.3 Campagne binaire multi-tâches et coordination

Le texte décrit cinq tâches binaires, onze conditions, trois graines par condition (165 entraînements), ainsi qu'une extension multiclasse (33 entraînements). Les moyennes descriptives non pondérées des cinq tâches binaires sont rapportées ainsi :

| Architecture | Accuracy moyenne | Log-loss moyenne |
|---|---:|---:|
| A — MLP | 95,16 % | 0,1628 |
| B — sondes locales | 92,22 % | 0,3961 |
| C — sondes coordonnées | 92,77 % | 0,3655 |

La coordination réduit la log-loss par rapport aux sondes locales mais ne comble pas l'écart avec le MLP dans cette campagne. Les exemples cités :

| Tâche | Log-loss locale B | Log-loss coordonnée C | Variation |
|---|---:|---:|---:|
| two_moons | 0,3390 | 0,3199 | −0,0191 |
| circles | 0,3572 | 0,3352 | −0,0220 |
| xor_product | 0,4753 | 0,4389 | −0,0364 |
| wine_binary | 0,3747 | 0,3440 | −0,0307 |
| digits_3_vs_8 | 0,4344 | 0,3896 | −0,0448 |

Le rapport mentionne aussi un contrôle de coordinateur gelé : sur 2 673 prédictions appariées, ses probabilités sont identiques à B (écart maximal nul). Le coordinateur entraîné baisse la log-loss dans les cinq tâches ; un contrôle avec labels permutés détériore le résultat sur `digits_3_vs_8` (0,4385 contre 0,4344 pour B).

**Leçons récupérées :** (1) la coordination peut améliorer la calibration/log-loss sans gagner en accuracy ; (2) présence d'un coordinateur et apprentissage effectif du coordinateur sont deux conditions différentes ; (3) un contrôle à labels permutés permet de vérifier que le gain vient d'un signal pertinent ; (4) il faut tracer l'effet réel sur les prédictions et les mises à jour.

### 2.4 Extension multiclasse `load_digits`

Le jeu décrit comporte 1 797 images 8×8, 64 variables et dix classes. Les valeurs citées pour les sondes : log-loss coordonnée C = 1,8107 et locale B = 1,8418 ; le texte dit que le MLP domine nettement. La log-loss uniforme de référence est `ln(10) ≈ 2,303`. Le tableau complet par seed et la valeur MLP ne sont pas présents dans l'extrait consulté.

**Leçon :** une log-loss inférieure à la référence uniforme ne signifie pas que la sonde approche le meilleur modèle ; la comparaison directe avec MLP reste essentielle.

### 2.5 Incohérence d'objectif avec `tanh`

Le texte signale que certaines variantes D/E appliquaient `tanh` aux logits tout en envoyant ces valeurs à `BCEWithLogitsLoss`. Cette combinaison est conceptuellement incohérente : cette perte attend des logits non bornés. Les mauvais résultats de cette branche ne permettent donc pas de conclure que `tanh` est mauvais en général.

**Leçon :** les sorties de tête et la fonction de perte doivent être compatibles ; isoler l'activation avec des comparaisons correctement formulées.

### 2.6 Boucle d'observation, empreinte et adaptation en ligne

Une boucle rapportée suit : observation → empreinte/résidu entre prédiction et mesure disponible → décision d'activation → mise à jour ou conservation des paramètres. Le protocole évoque 180 observations d'adaptation sur `two_moons` et des flux propres, manquants, bruités ou décalés.

Résultats MLP avec boucle rapportés :

| Condition | Accuracy | Log-loss |
|---|---:|---:|
| Sans boucle | 91,85 % | 0,2237 |
| Flux propre | 93,09 % | 0,1947 |
| 30 % d'observations manquantes | 91,73 % | 0,2148 |
| 20 % de labels inversés | 85,31 % | 0,4043 |
| 50 % de labels trompeurs | 40,12 % | 0,7633 |
| Flux décalé, test source | 85,43 % | 0,2938 |

Le texte indique que le résidu ne détecte pas nécessairement une erreur de label : anomalie, erreur de supervision et décision de mise à jour sont trois notions différentes. Sous 20 % de corruption, le rappel rapporté est approximativement 0,38–0,67 ; sous 50 %, le rappel du MLP A est proche de 0,07. Certains gates sont fortement dépendants du routage : round-robin abaisse l'accuracy C à environ 72,6 % sur flux propre, tandis que le routage ciblé est rapporté à environ 90,25 % propre et 89,88 % sous labels trompeurs.

**Leçons récupérées :** l'adaptation en ligne peut aider sous données propres mais amplifier les mauvaises observations ; une empreinte n'est pas un oracle anti-erreur ; tester la robustesse aux labels corrompus et au drift ; séparer ce sous-problème d'une sonde statique si la tâche-cible ne comporte pas de boucle de feedback.

## 3. Pistes EX3 les plus directement liées à l'objectif micro

### 3.1 Micro d4/k8 et MIXA

Le texte rapporte pour ModeChoice :

- `micro d4/k8` à **428 coefficients**, seed 2029 : accuracy 95,16 %, log-loss 0,2109 ; MLP ×4 signalés avec log-loss plus élevée dans ce passage, mais les valeurs appariées brutes ne sont pas incluses.
- `mixa_micro_d4_k8` à **528 coefficients**, seed 2029 : accuracy 95,97 %, log-loss 0,1868.
- seed 3037 : MIXA 92,74 % / 0,1900, contre une référence locale indiquée 91,94 % / 0,2109. La différence entre seeds illustre la sensibilité à l'initialisation.

Ces nombres ne sont pas directement interchangeables avec EX4 : les splits, dimensions d'entrée, définitions de paramètres et sources de code ModeChoice sont absents. Ce sont des cibles de reconstruction, pas des performances promises.

### 3.2 Pilote Wine

Le résumé de l'ancien pilote dit : sonde v009 = **3 472 paramètres** ; MLP comparateurs = **13 892** (4,001×) et **27 781** (8,001×). Il ne s'agit que d'une graine et d'un test de 27 observations. La sonde et RETRO n'auraient pas atteint le déclenchement de maturation avant l'arrêt guidé par validation. Malgré beaucoup moins de MACs analytiques, la sonde aurait été plus lente en entraînement et en latence que MLP×4.

**Leçons récupérées :** le ratio paramètres n'est qu'un axe ; moins de MACs analytiques n'implique pas une latence ou un entraînement plus rapides ; un RETRO qui ne déclenche pas sa décroissance locale n'a pas testé son hypothèse ; un petit test et une graine unique sont insuffisants.

### 3.3 État déclaré du workspace EX3 avant l'interruption

Le fil décrit des états de travail v001–v004 : Wine et Star98 auraient des résultats sur cinq graines ; RANDHIE une graine principale ; ModeChoice plusieurs graines (le texte alterne entre deux et trois selon le moment de la reprise) ; ANES96 et Fair sont dits non commencés dans un passage, tandis qu'un `run 072`/test Fair confirmatoire est mentionné plus tard sans tableau brut qui permette de résoudre cette incohérence. Le texte indique que 549 lignes de validation étaient contrôlées, et que deux checkpoints restaient ouverts (ModeChoice fixed_only, seed 1717 ; RANDHIE MIXA égal, seed 1501). Ces statuts ne peuvent pas être audités sans workspace, logs et checkpoints originaux.

Le fil mentionne aussi la nécessité de conserver des splits fixes entre seeds, la reprise de checkpoints au lieu de recommencer, l'absence de tests utilisés pour l'entraînement dans le runner v004 (`Xte=None`) et des comparaisons MLP de différentes profondeurs : sur Wine seed 1607, un MLP mono-couche a un résultat rapporté 100 % / 0,0052, alors qu'un modèle deux couches quasi apparié donne 96,3 % / 0,0365. C'est une raison concrète de ne pas choisir arbitrairement une unique architecture MLP faible.

## 4. Philosophie de recherche que les débris rendent explicite

La proposition méthodologique centrale est de renverser la recherche : choisir un cas réel où le MLP gagne, diagnostiquer précisément l'écart, puis faire évoluer la sonde itérativement sans lui donner d'avantage artificiel jusqu'à ce qu'elle gagne — ou conclure proprement qu'elle ne le fait pas. Les gains doivent ensuite être confirmés sur domaines/sujets extérieurs. La protection contre la triche et le sabotage n'est pas un frein à l'optimisation : c'est ce qui permet de savoir si une amélioration est réelle, reproductible et utilisable dans de futurs systèmes.

Conséquences opérationnelles : conserver les graines défavorables ; ne pas manipuler les splits ; ne pas limiter arbitrairement les architectures/époques/recherche ; ne pas favoriser ni dégrader la sonde ou le MLP ; sauvegarder chaque run et version ; mesurer la ressource au-delà des seuls paramètres ; ouvrir les jeux externes seulement après gel du choix.

## 5. Hypothèses techniques à conserver pour EX4

1. **Réduire le chemin de capacité** : d4/k8 est une piste EX3, mais explorer aussi d2/k4, d8/k4, d4/k16 et les variantes de partage/factorisation.
2. **Séparer croissance structurelle et coordination** : ajouter dynamiquement un expert n'est pas la même chose que faire croître alpha ; journaliser chaque événement.
3. **Faire émerger la coordination** : commencer avec poids uniformes puis interpoler vers un coordinateur appris, en comparant référence historique, aucun coordinateur, immédiat, linéaire et plateau.
4. **RETRO** : `beta_local = 1 - alpha`; vérifier le taux d'apprentissage effectif et la norme des changements de paramètres, car multiplier uniquement le gradient avec Adam peut ne pas produire la baisse voulue.
5. **MIXA** : branche adaptative + branche fixe (projection, centres, largeurs gelés) + gate appris ; compter les états fixes et les octets de déploiement.
6. **Calibration** : suivre log-loss, Brier/ECE en plus de l'accuracy.
7. **Contrôles mécanistiques** : coordinateur gelé, labels permutés, branche fixe seule, adaptatif seul, mélange, ablation gate.
8. **Robustesse de boucle** : si l'apprentissage en ligne est inclus, tester missingness, noise, label flipping et shift ; ne pas confondre anomalie et label erroné.
9. **Comparaison de ressources** : paramètres fixes + entraînables, stockage, MAC/FLOP, temps d'entraînement, latence, débit, RAM/VRAM, énergie si réellement mesurée.
10. **Transfert** : garder l'exposition historique explicite ; ne pas transformer Wine/ModeChoice/Digits historiques en confirmation indépendante.

## 6. Ce qui est définitivement non récupérable depuis cette archive seule

- scripts complets de l'ancien workspace EX3 v001–v007 ;
- fichiers de configuration définitifs de chaque run et versions de code exactes ;
- partitions/splits EX3, identifiants d'observations, snapshots préparés et préprocesseurs ;
- predictions JSONL/CSV par observation permettant de recalculer les métriques ;
- checkpoints, états d'optimiseur et poids de modèle ;
- rapport technique complet, tableaux par seed, mesures de ressources brutes, traces exactes alpha/beta ;
- preuve de statut final pour les tâches nommées.

`prompt_ex3.json` et `debrit_0.txt` suffisent pour récupérer les hypothèses, les pistes et une partie des chiffres narrés, mais pas pour reconstituer les artefacts binaires EX3. La branche EX4 est donc une reconstruction neuve, pas la continuation d'un checkpoint perdu.


## 7. Reconstruction complémentaire : micro-MIXA

La mention `mixa_micro_d4_k8` dans les débris, autour de 528 coefficients sur ModeChoice, peut raisonnablement désigner une architecture hybride micro : branche adaptative très petite + branche fixe (projection et bases persistantes) + mélange/gate. Le texte seul ne permet toutefois pas de reconstituer le graphe ni de vérifier le comptage 528. EX4 formalise donc cette piste en cinq ablations : adaptatif seul, fixe seul, mixage égal, gate global et gate conditionnel à l'entrée. Les poids/projections/centres/largeurs fixes font partie de `P_total`; seuls les coefficients entraînables entrent dans `P_train`.

Les résultats reconstructibles de la campagne micro-MIXA sur Wisconsin et le transfert Iris sont détaillés dans `rapport_micro_mixa_ex4.md`. Le résultat central n'est pas une victoire : les variantes hybrides peuvent améliorer l'accuracy sur un domaine, mais elles n'égalent pas la log-loss du MLP ge4x et leur latence CPU est plus grande. Les 528 coefficients ModeChoice du débris restent un chiffre narré non vérifiable, pas une valeur reproduite.
