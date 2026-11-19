# Audit du profil OASST1 v8 — structure, provenance et hypothèses

## 1. Provenance et splits

- Source OASST1 : 88 838 messages source, révision `fdf72ae0827c1cda404aff25b6603abec9e3399b`.
- Source train : 84 437 lignes; source validation : 4 401 lignes.
- Arbres source : 9 846 TRAIN et 518 validation.
- Dérivés après construction des paires de contexte/réponse et isolement d'arbres : 48 557 lignes TRAIN, 2 495 VALIDATION, 2 653 TEST; aucun arbre ne traverse les splits.
- Profil construit uniquement depuis 48 557 lignes TRAIN, 48 549 exemples non vides; VALIDATION et TEST ne sont ni utilisés pour entraîner ni pour sélectionner.
- Checkpoint V6 d'origine : 64 000 000 octets, SHA-256 `8526943d1528418fa8bbbf9128b61b5e1acd90a16eeb7cc062e18864b083dff4`, non modifié.

## 2. Structure du profil

`dialogue_profiles.json` (178 134 753 octets, SHA-256 `24780eea05de8cb8c77a772f8d03776adc33dc497fcb7d6e896690f8e99ce0e6`) contient un seul profil `everyday_dialogue` :
- 57 884 ancres contextuelles et leurs distributions agrégées de tokens réponse;
- 57 884 compteurs de fréquence/document et de total réponse;
- 252 793 unigrammes/tokens réponse distincts;
- 256 débuts de réponse retenus;
- 252 103 clés bigrammes et 1 762 580 clés trigrammes;
- 6 950 298 tokens de réponse agrégés;
- hashes d'identité des 48 471 exemples utilisés pour déduplication/provenance.

Le profil ne stocke pas les paires brutes prompt/réponse, ni des réponses complètes à retrouver. Il stocke des statistiques agrégées ancre→token et des transitions n-grammes internes à chaque réponse. Cela le classe comme modèle statistique de comptage, non comme mémoire épisodique de réponses. Cette propriété structurelle n'établit toutefois pas à elle seule une généralisation intelligente : il faut mesurer la génération libre et la couverture généralisée.

## 3. Hypothèses de construction encore ouvertes

Le script `train_oasst1_chat_profile_sqlite.py` fixe :
- `K=16` ancres distinctes prises dans les 16 derniers tokens contextuels uniques;
- top 128 arêtes réponse par ancre;
- top 64 continuations bigrammes et trigrammes par clé;
- top 256 débuts de réponse;
- support minimal de deux ancres indépendantes avant injection d'une association.

Ces bornes sont des choix de construction, pas des résultats validés. Elles peuvent exclure des signaux rares utiles ou surpondérer la fin du prompt. Les ablations K, top-K, seuils et politique de sélection d'ancres sont nécessaires.

## 4. Mélange multilingue

Le dérivé TRAIN comporte au moins 20 tags de langue : en 21 954; es 14 294; ru 3 739; zh 1 730; de 1 699; fr 1 380; th 786; ca 765; pt-BR 691; it 370; uk-UA 293; ja 200; pl 169; eu 168; vi 133; et d'autres langues. Le constructeur ne lit pas `row.lang` dans `chunk()` et agrège tout dans le même profil `everyday_dialogue`. Le sélecteur linguistique V6 n'isole donc pas les associations OASST1 par langue.

Il faut comparer profil mixte et profils/conditionnements par langue, tout en gardant le périmètre « chat » : aucune fonction de traduction séparée n'est ajoutée. Les mesures doivent inclure code-switching, prompt en langue rare, réponse dans la langue du prompt et contamination interlangue.

## 5. Risques de génération à mesurer

- longue traîne lexicale (252 793 tokens distincts sur 6,95M occurrences);
- tokens rares, noms propres, chiffres et ponctuation qui peuvent produire des pseudo-mots ou sorties incohérentes;
- transitions de réponse apprises indépendamment du prompt;
- associations qui peuvent refléter des cooccurrences plutôt qu'une pertinence;
- perte de contraintes anciennes due à la sélection des 16 dernières ancres;
- mélange des langues dans un seul profil;
- réduction de couverture par top-K et seuil de deux ancres.

## 6. Évaluation requise

Comparer sans profil, profil OASST1 mixte, profil conditionné par langue, transitions seules, associations seules et fusion. Mesurer exact-match séparément de generalized coverage, réponses inédites, pertinence prompt, continuité multi-tour, répétition, diversité, pseudo-mots, contradictions et ancrage de contraintes. Le modèle de génération doit réaliser les réponses; aucune réponse cible ou phrase de référence n'est injectée dans le runtime. Non-réponse désactivée pour toutes les expériences principales.

## 7. Statut

Le profil est construit, parseable, traçable et chargé par le CLI v8. Sa contribution à la cohérence et à la généralisation n'est pas encore démontrée par une génération libre terminée. Le diagnostic v7 précédent a expiré avant génération; ce timeout ne vaut ni échec ni réussite du modèle.

## 8. Distribution de la longue traîne

Le profil contient 252 793 tokens distincts pour 6 950 298 occurrences; 129 927 sont hapax, 163 809 apparaissent au plus deux fois et 199 888 au plus cinq fois. Les 256 débuts de réponse conservés ont une fréquence minimale de 18, mais les tables de transitions/associations conservent beaucoup d'arêtes rares : 2 294 528 hapax dans 5 843 389 arêtes contexte→token; 712 882 hapax dans 1 080 236 bigrammes; 2 908 353 hapax dans 3 624 138 trigrammes. Les filtres de support/rang interviennent ensuite, mais les transitions ne possèdent pas actuellement de seuil de support minimal.

Cette longue traîne peut être utile pour les noms propres et le vocabulaire rare, ou produire des pseudo-mots/continuations fragiles. Elle doit être évaluée par ablation de fréquence, support et backoff, sans supprimer arbitrairement les tokens rares.

## 9. Clarification exacte de la politique de split

Le manifeste dérivé précise : le TRAIN source (84 437 lignes) est séparé 95/5 par `message_tree_id` en TRAIN dérivé (9 362 arbres, 48 557 exemples) et VALIDATION dérivée (484 arbres, 2 495 exemples); le split source VALIDATION (4 401 lignes, 518 arbres) est réservé comme TEST dérivé (2 653 exemples). Les contrôles `train/validation`, `train/test` et `validation/test` rapportent zéro chevauchement d'arbres. Le profil n'utilise que le TRAIN dérivé.

La politique exclut des cibles et du contexte les nœuds supprimés, `review_result=False` et synthétiques; un ancêtre signalé tronque le contexte et un parent immédiat signalé exclut la cible assistant. Les valeurs `review_result=null` ne sont pas explicitement exclues. Ces règles doivent rester dans le manifeste et être auditées par langue/longueur de conversation, car elles changent la distribution d'apprentissage.

## 10. Filtrage source et contexte d'entraînement

Le constructeur dérivé `prepare_oasst1_parquet.py` conserve le champ `lang` dans chaque exemple mais le profil ne l'utilise pas. Il n'exclut que `deleted=True`, `review_result=False` et `synthetic=True`; les valeurs `review_result=null` restent admissibles. Les données décodées comptent `synthetic_true=0` dans les deux splits, donc ce filtre n'a actuellement aucun effet. Les arbres non `ready_for_export` sont exclus en entier; les ancêtres signalés tronquent le contexte; le parent immédiat signalé exclut la cible assistant. Les IDs utilisateur, ratings et detoxify sont exclus.

Le contexte de chaque exemple est limité à `MAX_CONTEXT_MESSAGES=8`, puis tronqué aux huit derniers messages propres. Cette borne est un choix de préparation, pas une propriété du runtime. Il faut comparer 8, 16 et contexte complet sur validation, surtout pour la cohérence multi-tour et les contraintes anciennes. Le runtime `context_tokens()` n'applique pas nécessairement la même limite; la différence entre contexte vu à l'entraînement et contexte vu à l'inférence doit être mesurée.
