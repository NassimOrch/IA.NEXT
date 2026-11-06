# Protocole expérimental et règles d'interprétation

## Enregistrement préalable

Chaque hypothèse doit spécifier une prédiction et une condition de falsification avant l'expérience. Conserver toutes les versions et tous les résultats, y compris ceux qui contredisent la prédiction.

## Contrôles minimaux

1. Enregistrer l'identifiant et le hash du modèle, l'entrée, les données et l'environnement.
2. Capturer une baseline, puis réaliser l'intervention sans changer les poids autrement.
3. Vérifier le rétablissement des hooks/états temporaires.
4. Mesurer les différences de sorties et préserver les sorties brutes.
5. Répéter sur des entrées qui distinguent des hypothèses concurrentes; ajouter des contrôles négatifs.
6. Valider sur des observations indépendantes; séparer la table de vérité secrète du moteur de découverte pour les benchmarks aveugles.
7. Reconstruire dans un runtime distinct qui n'appelle pas le modèle source comme oracle caché.

## Statuts et portée

`SUPPORTEE` signifie que des observations concordent avec la prédiction dans le domaine exécuté; cela ne signifie pas `PROUVEE`. `VALIDATED_ON_SUPPLIED_HOLDOUT` signifie seulement qu'une reconstruction atteint ses métriques sur le holdout fourni. Aucune reconstruction comportementale ne suffit, à elle seule, pour démontrer l'équivalence des poids ou des circuits internes.

## Gestion des budgets

Un budget de recherche est enregistré avec la stratégie et les candidats examinés. Quand le budget est épuisé, produire un statut d'incomplétude avec le périmètre exploré. Ne transformer ni l'absence de résultat dans une exploration limitée en impossibilité, ni un résultat dans une classe limitée en découverte universelle.

## Benchmark synthétique

L'analyseur reçoit des exemples et un adaptateur de requêtes. Le générateur conserve sa vérité cachée dans un répertoire séparé réservé à l'auditeur. L'auditeur compare après coup la règle identifiée à la vérité de référence, sans injecter celle-ci dans la découverte.
