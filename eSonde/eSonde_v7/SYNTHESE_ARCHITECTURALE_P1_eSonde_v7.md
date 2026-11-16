# SYNTHÈSE ARCHITECTURALE P1 — choix d'une voie conditionnelle eSonde v7

**Statut :** décision conceptuelle retenue pour formalisation P2 ; non encore validée en qualité de réponse.

## 1. Contrainte fonctionnelle
La seule fonction publique est le chat prompt/réponse. La non-réponse est désactivée pendant les travaux. Le modèle ne recherche pas une ancienne réponse : toute relation prompt→réponse doit être portée par les paramètres appris et l'état transitoire du dialogue, pas par une table de paires consultée à l'inférence.

## 2. Options étudiées

| Option | Description | Avantage démontrable | Risque / défaut | Décision |
|---|---|---|---|---|
| A — associatif actuel | Statistiques de texte, candidats n-grammes/PPMI, vote Obsiss | Réutilise le checkpoint intact ; baseline rapide | Pas de fonction conditionnelle paramétrique ; deux runs restent hors cible malgré de nombreuses décisions stables | Gardé comme baseline et ablation |
| B — récupération Q/R | Recherche des prompts proches et restitution des réponses stockées | Contrôle utile sur exemples déjà vus | C'est une mémoire/lookup et ne satisfait pas le but | Exclu du runtime livré |
| C — seq2seq conventionnel | Modèle neuronal conditionnel appris sur Q/R | Objectif direct, baseline paramétrique comparable | Les Obsiss peuvent devenir des features périphériques et perdre leur voix | Baseline concurrente à mesurer |
| D — transducteur conditionnel d'état-observation | Séquence d'états 16 canaux, voix Obsiss individuelles, dynamique P/R, opérateur de continuation partagé appris | Associe apprentissage conditionnel, identité des Obsiss, 16 observations et contexte actif ; pas de table de réponses à l'inférence | Nouveau noyau à entraîner ; capacité et généralisation à mesurer | Choisi comme hypothèse centrale |
| D+ — panel sentinelle | Petit sous-ensemble d'Obsiss diversifiées compare ses votes à ceux des travailleurs | Peut signaler un consensus fragile ou une contamination du pool | Accord ne prouve pas la justesse | Hypothèse optionnelle de laboratoire |

## 3. Architecture D proposée

### 3.1 Séquence d'observations
Chaque occurrence du prompt et de l'historique produit un vecteur de 16 signaux explicitement nommés. Les canaux restent attachés à chaque occurrence et à son rôle, tour, position et provenance ; le prompt n'est pas réduit à un vecteur moyen.

### 3.2 Voix Obsiss
Chaque Obsiss conserve son identité issue du checkpoint v6 et observe l'ensemble des seize canaux. Elle calcule ses activations P/R et fournit une perspective de continuation. Les voix restent auditables ; l'agrégat collectif conserve médiane, dispersion et désaccords. Le checkpoint original reste immuable.

### 3.3 Transducteur paramétrique conditionnel
Un opérateur partagé appris transforme l'état d'observation du prompt et le contexte local en état de continuation, token par token. Le décodeur est entraîné par teacher forcing uniquement pendant l'apprentissage sur réponses TRAIN. À l'inférence, seules les séquences de paramètres apprises sont utilisées. Aucun index de réponses, nearest-neighbour ou lookup prompt/réponse n'est présent. Les nouveaux paramètres sont stockés séparément dans un checkpoint dérivé. La forme concrète (état récurrent compact, transition d'état structurée ou encodeur-décodeur de référence) est comparée au laboratoire.

### 3.4 Objectifs séparés
- `chat`: 13 paires TRAIN eGenBrain ; mêmes 17 contenus uniques que V6, partitions différentes.
- `math_qa`: 5 978 paires TRAIN, domaine mathématique rapporté séparément ; pas une preuve de dialogue général.
- Textes autonomes: éventuellement objectif de langue séparé, jamais un prior assistant sans provenance de rôle.
- `sms_classification`: exclu du chat.

Toutes les sources sont dédupliquées par groupe de prompt avant le split ; TRAIN seul optimise, VALIDATION sélectionne, TEST reste gelé jusqu'au gel final.

## 4. Rôle du contexte eGenBrain
Transfert retenu : occurrence-level context, speaker, ordre, provenance, témoins et graphe local temporaire reconstruit par tour et préfixe. Ordre observé ne signifie pas causalité. Le contexte n'est pas persisté comme base de réponses ; le sous-graphe actif est reconstruit à partir des messages fournis.

## 5. Panel sentinelle minimal
La proposition M-015 reste une expérience : panel de 2 à 8 Obsiss existantes, choisies selon la diversité de leurs signatures ; il observe l'écart panel/travailleurs. Désaccord = réévaluation du pool/context et éventuellement extension de population. Il ne choisit pas de token ni ne certifie la vérité.

## 6. Convergence et critères
Séparer (1) terminaison de la dynamique P/R ; (2) stabilité de rangs/candidats ; (3) robustesse panel/travailleurs ; (4) qualité contextuelle évaluée indépendamment. Un système peut satisfaire 1–3 et échouer à 4, comme l'illustre le run français à 128 Obsiss archivé. Départ 10 ; croissance seulement si un critère le demande. Un million n'est ni cible ni condition de réussite.

## 7. Critères de poursuite
Formaliser D, l'objectif conditionnel, les splits et le panel ; implémenter un entraînement séparé sans écrire dans le checkpoint v6 ; valider les pertes train/validation et l'absence de fuite ; effectuer les ablations ; créer un savepoint et un preflight avant le premier entraînement. Les sorties TEST restent gelées.

**Décision P1 :** D comme voie centrale à formaliser ; A comme baseline ; C comme baseline paramétrique concurrente ; B contrôle négatif hors runtime ; D+ comme hypothèse de diagnostic. Ce choix expérimental ne prédit pas l'issue.
