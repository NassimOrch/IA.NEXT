# Rapport de réanalyse technique — eSonde v6

**Date d'audit :** 14 novembre 2026  
**Source :** `rapport_enquete_eSonde_v6.tex`, modules livrés, métadonnées/checkpoints, résultats, traces et journaux de `LIVRAISON_eSonde_v6.zip`.  
**Statut de cette réanalyse :** fondée sur les fichiers présents et relus ; les fichiers binaires sont contrôlés par taille et empreinte, pas interprétés comme du texte.

## 1. Description

La mission de cette réanalyse est d'établir ce qu'eSonde v6 calcule effectivement, ce que les rapports démontrent, ce qu'ils ne démontrent pas et quelles défaillances précises empêchent de conclure à une cohérence de dialogue robuste. L'objet de mesure n'est pas « le nombre d'Obsiss » isolément, mais le pipeline complet : prompt → observations → interactions P/R → propositions → sélection → réponse → mesure postérieure.

Le checkpoint livré déclare 1 000 000 d'Obsiss, 16 coordonnées par Obsiss et un fichier de poids de 64 000 000 octets. Le SHA-256 recalculé de `weights.bin` est `8526943d1528418fa8bbbf9128b61b5e1acd90a16eeb7cc062e18864b083dff4`. Les poids et statistiques sources ont été conservés sans modification dans le runtime v7.

## 2. Architecture

Le code v6 réellement présent comprend les modules `features.py`, `obsiss.py`, `model.py`, `generation.py`, `corpus.py`, `serialization.py` ainsi que les interfaces et outils historiques. La chaîne observée comprend :

1. Tokenisation et construction de caractéristiques locales/globales de dimension 16.
2. Construction d'observations P et R à partir d'un même checkpoint de poids.
3. Application de transformations entières déterministes aux lignes Obsiss.
4. Regroupement des observations exactement équivalentes, en conservant les vérifications exactes des collisions de hash.
5. Construction de voisinages et itérations synchrones de type Jacobi.
6. Publication d'états successifs et d'une trajectoire bornée par le paramètre dimensionnel.
7. Génération de candidats sur support n-grammes et associations PPMI, classement agrégé, puis raffinement MASK.
8. Mesures P/R et diagnostics géométriques postérieurs.

La limite conceptuelle majeure : une trajectoire de 16 coordonnées/états ou un arrêt après un budget fini ne constituent pas, par eux-mêmes, une preuve de point fixe sémantique, de compréhension, de cohérence discursive ou de vérité.

## 3. Pipeline complet observé

- Le texte du prompt est tokenisé ; des caractéristiques locales et globales sont construites.
- Chaque population P/R reçoit des vecteurs et des poids entiers.
- Les transformations et classes d'équivalence sont calculées ; les doublons exacts sont regroupés.
- Les interactions de voisinage produisent des états publiés et des journaux de trajectoire.
- Le générateur exploite des statistiques TRAIN (fréquences, bigrammes/trigrammes, associations) pour proposer les continuations.
- Les candidats sont classés par des signaux internes, puis le raffinement MASK intervient sur la réponse.
- Les observations du prompt et de la réponse peuvent être comparées par une mesure de cosinus.

La séparation des étapes a une conséquence : si les observations P/R ne contrôlent pas la sélection des tokens de manière active, la richesse du mécanisme d'observation peut rester une mesure après coup, au lieu de devenir une capacité effective de génération.

## 4. Commandes d'exécution et sources de preuve

Les commandes archivées sont conservées dans `eSonde_v6_reference/`, les journaux sources dans le registre d'expériences et les hashes détaillés dans `source_file_inventory.json` / `registre_experiences_eSonde_v6_eGenBrain_v4.json`. L'audit courant a effectué :

```bash
unzip -tq /mnt/data/LIVRAISON_eSonde_v6.zip
python suivi_model_eSonde_v7/audit_source_inventory.py
```

Les traces gzip ont été décompressées et leurs lignes JSONL contrôlées. Les résultats JSON ont été analysés avec parseur JSON, taille et empreinte. Les fichiers binaires n'ont pas été « lus » au sens d'une interprétation textuelle ; les données sont identifiées par leur provenance, dimensions, taille et SHA-256.

## 5. Résultats

### Intégrité et périmètre

L'archive actuellement téléversée est de 467 343 383 octets, possède 14 membres ZIP et passe le contrôle CRC. Son SHA-256 : `7af118f5799b0ba428d49aafc2513097fcb0d8da56e185c6e4f3dd911950d312`. Les quatre archives imbriquées présentes passent elles aussi. Les deux archives `suivi_model_eSonde_v6.part1.zip` et `part2.zip` référencées dans le manifeste ne sont pas dans cette livraison ; leur contenu ne peut pas être présenté comme restauré.

L'inventaire contient 650 fichiers issus des cinq racines extraites et 1 636 912 922 octets cumulés. Le registre couvre les 159 résultats JSON, les 72 traces gzip et les journaux/répertoires d'expérience.

### Résultats JSON et traces

- 159 résultats JSON : 148 valides, 10 fichiers de taille nulle et un JSON non analysable.
- 72 traces gzip : 65 complètes/valides et 7 tronquées ou incomplètes.
- Les paires P/R à 1k, 10k et 100k possèdent des traces lisibles de 16 états.
- Les campagnes P/R à 1M recensées sont interrompues ou incomplètes ; la campagne `p_r_1m` ne doit pas être étiquetée réussite.
- Une trace gzip corrompue porte un suffixe `.gz` ordinaire ; l'absence du suffixe `.incomplete` ne la rend pas valide.

### Mesures et génération

Les traces P/R à 100k indiquent environ 115 018 paires candidates/115 009 arêtes côté P et 166 197 paires/166 193 arêtes côté R, avec 26,181 s et 31,111 s respectivement dans les journaux concernés. Ces chiffres sont des mesures de ces exécutions précises ; ils ne préjugent pas de la qualité conversationnelle.

Les exemples générés v4 incluent des sorties multilingues fragmentaires ou génériques (par exemple le français `Ceci: la ministre de l'énergie solaire pour`) alors que certains scores de similarité restent élevés. Il s'agit d'un contre-exemple empirique à l'idée que le score géométrique courant certifie l'adéquation à la question.

Le journal de livraison rapporte 51/51 tests logiciels PASS sous Xvfb. Ces tests établissent des invariants du code et des interfaces couverts ; ils ne démontrent pas la robustesse d'une IA conversationnelle générale.

## 6. Interprétation des résultats

### Ce qui fonctionne, selon les preuves présentes

- Le checkpoint et son format de poids sont reproductibles et vérifiables.
- Les mécanismes d'observation, de transformation, de quotient exact et de trace sont implémentés.
- Les campagnes P/R à 1k/10k/100k produisent des traces exploitables.
- La génération peut produire des chaînes dans plusieurs scripts/langues, même si la pertinence n'est pas garantie.
- La chaîne d'audit du code et les tests de livraison vérifient un ensemble défini d'invariants.

### Ce qui casse pour l'objectif dialogue

1. **Support de propositions borné.** La génération sélectionne dans un ensemble construit à partir de fréquences, n-grammes et cooccurrences. Si le support ne contient pas de formulation adaptée, les mécanismes de classement ne créent pas à eux seuls le contenu absent.
2. **Contexte insuffisamment actif.** Les indices de prompt ne contraignent pas assez fortement chaque continuation. La réponse peut s'éloigner du sujet.
3. **Score non calibré.** La somme/rang de plusieurs signaux peut être élevé pour une sortie manifestement peu pertinente. Un rang n'est ni une probabilité ni un label de vérité.
4. **P/R trop séquentiel.** L'observation R et une partie du score interviennent après que des propositions ont déjà été formulées ; elles ne sont pas nécessairement co-productrices de chaque token.
5. **Sémantique des axes.** Les 16 coordonnées héritées sont des caractéristiques numériques, mais leur interprétation observationnelle explicite et leur contribution indépendante au sens doivent être spécifiées.
6. **Convergence.** Un budget maximal ou une trajectoire de longueur fixe doit être distingué d'une convergence, d'un état stable ou d'un consensus.
7. **Scalabilité à 1M non close.** Les expériences P/R à 1M interrompues sont des incidents/limites de preuve à résoudre, pas des résultats.

Il n'est pas nécessaire d'interpréter négativement ces faits comme une impossibilité théorique. Ils indiquent exactement quelles parties du mécanisme doivent être redessinées, mesurées et ablatées.

## 7. Conséquences théoriques, conceptuelles et opérationnelles

### Théoriques

Un espace de dimension 16 ne devient sémantique que si chaque coordonnée a une définition opératoire, une source, un domaine de validité, une règle de calcul et des cas adverses. L'interaction n'est pas de la compréhension si le résultat ne contraint pas réellement le choix des tokens. L'observation, la qualité de la réponse, la calibration et la vérité doivent être mesurées séparément.

### Conceptuelles

Les Obsiss ne devraient pas être ramenées à un unique vecteur moyen homogénéisant leurs identités. Leur singularité doit participer à des voix d'observation différenciées, avec désaccord observable et une règle collective qui conserve ce désaccord. La cohérence commune doit être une propriété du processus de réponse, pas une suppression de la diversité.

### Opérationnelles

v7 doit garder le checkpoint original intact, activer le contexte à chaque étape de génération, donner un rôle effectif aux Obsiss pendant la proposition/sélection, journaliser la provenance de chaque décision, prévoir des tests de résistance à la négation, au temps, aux changements de référent, aux multi-tours et aux formulations hors vocabulaire, et considérer la terminaison et la convergence comme deux résultats différents.

## 8. Conclusion

Le rapport d'enquête v6 est cohérent avec les sources sur l'architecture de base et les principaux défauts du dialogue. La présente réanalyse rend les preuves traçables : 1M inachevé, dix résultats vides, une trace invalide, des générations hors contexte malgré un signal interne favorable, et absence de preuve de convergence conversationnelle. Ces constats motivent les choix v7 ; ils ne constituent pas un verdict a priori sur le potentiel du modèle.

## 9. Statut du modèle

**eSonde v6 : checkpoint et mécanismes d'observation reproductibles ; génération conversationnelle expérimentale ; preuve de dialogue contextuel robuste non établie ; campagne P/R à 1M incomplète.** Le checkpoint est réutilisable pour v7 sans modification. Aucune conclusion de supériorité/infériorité générale n'est déduite de ces seuls éléments.
