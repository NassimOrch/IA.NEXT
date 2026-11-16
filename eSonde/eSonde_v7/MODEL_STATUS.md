# Statut du modèle eSonde v7

**Révision :** 7.0.0-experimental  
**Périmètre :** chat/dialogue uniquement.  
**Checkpoint :** eSonde v6 d'origine, utilisé en lecture seule.

## 1. Architecture implémentée

- Contexte de dialogue transitoire, occurrence-level, typé par tour, rôle et position ; provenance et ordre sont conservés, sans inférence automatique de causalité ni mémoire persistante.
- Seize canaux d'observation explicites, alignés sur les seize coordonnées historiques. Chaque Obsiss garde son identité de ligne et sa perspective complète sur les seize observations ; aucune assignation permanente à une dimension primaire ou secondaire.
- Vote individuel calculé depuis les poids originaux de la ligne, son état P et une permutation croisée déterministe des observations. Les voix individuelles sont agrégées par rang médian ; l'IQR conserve le désaccord.
- **Couplage P/R au moment de la proposition :** pour chaque continuation candidate, une activation R est calculée avec l'état P du préfixe courant et la même ligne d'Obsiss. La cohérence P/R de chaque ligne entre dans le vote du token avant son choix. L'état R complet de la réponse finale reste aussi publié comme diagnostic.
- Propositions issues des statistiques TRAIN v6 (n-grammes, associations PPMI et retour caractère-trigramme en cas de pool lexical rare). Aucune table de réponses prompt/cible n'est injectée.
- Population de départ dix. Elle croît seulement si la dynamique P/R ou la stabilité décisionnelle ne satisfait pas les critères. Le million est un plafond de checkpoint, pas une cible obligatoire.
- Non-réponse désactivée par défaut ; `--allow-no-response` et la case GUI l'activent explicitement.

## 2. Distinction des convergences

La dynamique d'interaction de v6 est exécutée exactement sur une vue en lecture seule des lignes actives. `NO_ACTIVE_NEIGHBORS`, répétition d'état SHA-256 de période 1, oscillation et borne de trajectoire ont des statuts séparés. Le hash constitue une évidence cryptographique, non une preuve mathématique sans collision.

La stabilité de la décision est mesurée séparément : leave-one-Obsiss-out pour 2 à 128 unités, huit partitions déterministes au-delà ; seuils de rétention top-1 0,90, Jaccard top-k moyen 0,90, Spearman moyen 0,95. Un pool d'un seul candidat ne démontre pas la stabilité. Ni l'un ni l'autre critère ne prouve la vérité factuelle.

## 3. Tests logiciels exécutés

**16/16 tests PASS** au 14 novembre 2026. La compilation Python des modules runtime, lanceurs et tests passe. Les tests couvrent notamment : 16 canaux ; rangs ex-aequo ; contexte/provenance ; perspective 16D individualisée ; dix Obsiss synthétiques stables ; parité exacte du premier état P/R avec v6 sur fixture ; lecture strictement bornée du checkpoint ; séparation des statuts de dynamique ; non-réponse désactivée ; CLI chat-only ; hash original ; vote P/R candidate-spécifique, hachage int16 des états dynamiques, et replis sans NumPy.

Ces résultats sont des tests logiciels. Le cas synthétique de dix Obsiss n'est pas un résultat de convergence sur le checkpoint réel.

## 4. Intégrité du checkpoint

`models/eSonde_v6/weights.bin` : 64 000 000 octets. SHA-256 attendu et vérifié :

`8526943d1528418fa8bbbf9128b61b5e1acd90a16eeb7cc062e18864b083dff4`

Le checkpoint n'a pas été modifié.

## 5. Essai réel et incident M-010

Le premier chat réel plafonné à dix Obsiss s'est arrêté avant de produire une réponse : `KeyError: 'published_sha256'` dans le contrat de statistiques de l'activation dynamique. L'incident M-010 est documenté dans l'audit ; la trace P correspondante est un gzip valide, mais elle ne constitue ni une réponse ni une preuve de convergence. Le défaut est corrigé ; le contrat expose désormais les empreintes `published_sha256` et `q_context_sha256` (P uniquement). La suite de tests est à 16/16.

## 6. Expériences encore nécessaires

- Refaire un chat réel plafonné à dix Obsiss, non-réponse désactivée, après nouveau snapshot complet et préflight ; enregistrer séparément dynamique P, stabilité décisionnelle, latence et réponse.
- Si l'une des conditions échoue, effectuer une campagne adaptative avec plafond supérieur, sans imposer le million.
- Tests multi-tours, langues, longueurs, négation, temporalité, contradictions, OOV et références.
- Mesures RSS, CPU, latence/token, ablations et évaluation humaine aveugle.
- Comparaison reproductible avec v6, baselines et LLM à protocoles identiques.

Le statut n'anticipe aucun de ces résultats. La stabilité d'un vote n'est ni compréhension universelle ni preuve de qualité générale.
