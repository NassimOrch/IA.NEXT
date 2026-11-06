# Synthèse exécutive

## Question étudiée

Le travail confronte, sans présumer la réponse, les familles prévues par le prompt original : sonde adaptative locale, coordination globale, option d'activation, combinaison coordination + activation, boucle causale observations → empreintes → mises à jour, et composition `input → f → g ≈ input`. Les comparateurs incluent un MLP classique et une RBF à sorties fixes avec readout appris.

## Résultats principaux

1. **Le protocole historique prioritaire est reproduit exactement.** Le script « two moons » a été ré-exécuté à partir de sa copie source ; les fichiers CSV et JSON générés correspondent octet par octet aux sorties archivées. Les valeurs archivées donnent MLP : accuracy moyenne 0,9587, AUC 0,9919, log-loss 0,1109 ; sondes RBF adaptatives : 0,9601, 0,9906, 0,1174 ; sonde fixe témoin : 0,8623, 0,9199, 0,3550. Ce sont des résultats sur le split et protocole d'origine, pas une preuve de généralité.

2. **La coordination globale a des effets dépendants de la tâche.** Sur les cinq tâches binaires, la coordination trainée réduit la log-loss par rapport aux sondes locales dans ce protocole fixe, mais les changements d'accuracy sont petits ou non uniformes. Une ablation vérifie l'assertion mécanistique la plus utile : lorsque le coordinateur est gelé avec poids uniformes, les probabilités des sondes locales et de la condition globale gelée sont exactement égales pour 2 673 prédictions appariées (différence maximale 0). Cette égalité est un invariant du code expérimental contrôlé, non une preuve que tout système global doit se réduire ainsi.

3. **L'activation n'est pas gratuite.** L'option testée est tanh appliqué après le logit scalaire de chaque sonde, et non une activation dans les fonctions de base ou un réseau MLP. Dans l'implémentation utilisant `BCEWithLogitsLoss`, la double interprétation logit/activation produit une log-loss plus défavorable pour certaines conditions. Il faut comparer les emplacements d'activation et leurs pertes cohérentes avant de tirer une conclusion architecturale générale.

4. **La boucle observations–empreintes peut aider ou dégrader.** Sur deux lunes, la mise à jour en ligne du MLP avec observations propres améliore ce split/seed illustratif (accuracy 0,9185 → 0,9309; log-loss 0,2237 → 0,1947), mais sous 20 % de labels inversés elle tombe à 0,8531/0,4043, et sous 50 % de labels trompeurs à 0,4012/0,7633. Les sondes ne réagissent pas toutes comme le MLP; le détecteur de résidu n'est ni parfait ni universel. Ces chiffres ne sont pas à généraliser au-delà du protocole ciblé.

5. **La reconstruction non triviale est possible sur la tâche synthétique, mais la boucle peut dériver.** L'identité directe atteint RMSE 0 par définition puisque la cible est l'entrée; c'est un contrôle trivial, pas un système appris. L'autoencodeur MLP latent 2 obtient RMSE ≈0,0349; RBF à deux cartes libre, ≈0,0982. Les boucles de reconstruction peuvent dégrader fortement les résultats et afficher une variance importante entre graines. La reconstruction et le débruitage sont des objectifs différents; le protocole n'autorise pas à présenter le premier comme une preuve du second.

6. **Le contrôle indépendant est positif mais borné.** 49 contrôles instrumentés sur 49 passent (audit v6), avec recalcul des métriques, contrôle du registre web, contrôle de précision numérique et audit propre à digits 10 classes. Les tests des sources NGeGenBrain v2 et v3.1 ont été exécutés avec leurs chemins de paquet requis. Deux problèmes de données ont été signalés : la dernière ligne de `batch_dataset.jsonl` est tronquée; `Screenplay_dataset.jsonl` a 4 000 lignes valides mais 2 000 objets distincts (chacun répété deux fois). Le contenu de `0000.parquet` n'a pas pu être décodé car aucune bibliothèque Parquet pertinente n'était installée.

## Traçabilité des sources web

`sites_web_consulte.json` décrit les 40 URL uniques et les 28 requêtes documentées de la reprise actuelle, avec leur utilité et leur statut d’accès. Les historiques précédents ne conservaient pas toutes les URL; cette limitation est indiquée explicitement.

## Résultat complémentaire RBF-R1 — gate de reconstruction défavorable

Le complément causal RBF-R1 (6 couples modèle–graine, 162 métriques, 23 040 événements) active réellement le gate d'empreinte au moment de l'update. Sur le test source, les RMSE moyennes sont 0,0982 sans update, 0,4804 après 240 updates inconditionnelles et 1,4298 avec le gate q90 pour `RBF2_free_global`; pour la variante tanh, respectivement 0,0864, 0,7521 et 1,3659. Les résultats restent mauvais sous bruit de mesure et décalage de distribution. **La conclusion opérationnelle est négative pour cette règle de mise à jour et ces deux modèles : une empreinte de résidu à seuil q90 n'assure pas la stabilité.** Une mise à jour en ligne pourrait nécessiter clipping, pas borné et/ou un redémarrage d'optimiseur; ce sont des pistes d'expérience future, non un correctif appliqué après observation des résultats.

## Verdict par hypothèse

| Hypothèse | Statut | Interprétation |
|---|---|---|
| Les sondes locales apprennent une fonction utile | Soutenue dans le domaine testé | Reproduction deux lunes et benchmark contrôlé; pas une affirmation universelle. |
| La coordination globale améliore uniformément l'accuracy | Non soutenue dans le domaine testé | Effets modestes et dépendants de la tâche; pas « démontrée fausse » dans tous les contextes. |
| La coordination globale peut réduire la log-loss dans cette implémentation | Partiellement soutenue | Gains descriptifs sur cinq tâches binaires, un split chacune, trois graines; digits10 est une extension séparée. |
| L'activation tanh améliore toujours les sondes | Non soutenue dans le domaine testé | L'effet dépend de la position de l'activation et de la perte utilisée. |
| La boucle d'observation améliore toujours le modèle | Non soutenue dans le domaine testé | Propre : parfois utile; corruption ou décalage : dégradation possible. |
| Les empreintes détectent toutes les données trompeuses | Non soutenue dans le domaine testé | Précision/rappel varient; plusieurs faux négatifs demeurent. |
| Une chaîne de deux sondes peut reconstruire l'entrée | Soutenue dans le domaine testé | Oui avec les paramètres appris; l'identité triviale ne compte pas comme solution apprise. |
| La boucle en ligne est stable pour la reconstruction | Non soutenue dans le domaine testé | Dérive et performance très variable observées. |
| La théorie d'empreintes identifie unique­ment la structure interne | Non testée / impossible à conclure | Les données finies identifient au mieux les sorties échantillonnées; les paramètres peuvent être non identifiables. |

## Portée et prochaines expériences

Le résultat le plus défendable n'est pas une victoire d'architecture, mais une décomposition plus nette des mécanismes : la coordination centrale modifie les poids et les taux d'apprentissage locaux; l'activation a un emplacement exact; la boucle est une règle de mise à jour supervisée non anticipative; et la reconstruction se juge contre un contrôle identité ainsi qu'un modèle appris. Pour une conclusion solide, il faut davantage de splits indépendants, un choix d'activation/loss cohérent et préenregistré, des budgets FLOPs/mémoire appariés, des intervalles au niveau de jeux indépendants, et au moins une tâche observationnelle non synthétique avec provenance vérifiable.


### Supplément reconstruction RBF-R1

Une boucle en ligne distincte a été testée sur deux auto-encodeurs RBF, trois graines, quatre conditions de flux et quatre politiques. Elle produit 162 lignes métriques et 23 040 événements. Le contrôle sans mise à jour reproduit la baseline exactement, mais l’adaptation et surtout le gate q90 dégradent fortement la reconstruction sur ce problème. Ce résultat négatif est conservé et ne doit pas être extrapolé à d’autres tâches.
