# Audit critique des livrables de la première livraison

## Verdict

La première livraison était **insuffisante au regard du prompt normatif**. Elle contient un formalisme générique et un pilote, mais n'exécute pas plusieurs phases obligatoires. Elle ne doit pas être considérée comme exécution complète de `prompt.txt`.

## Écarts matériels constatés

1. **Portée de la source** — le reçu de la livraison précédente cite l'empreinte d'une archive racine antérieure (`891cf3903f2cf93ac013237b391f53d5feeb2b2002caaee2ae8e13887a5b49f4`, 132 043 934 octets), alors que la source reçue ici a SHA-256 `8fcf82931988a96cdfb1ff5cbe5892142b4b1174385dc87cd9ed0f9e2d7069bb` et 242 262 864 octets. C'est une discordance de provenance des livrables précédents, même si le `sonde_adapt_1_bundle.zip` actuel a été intègre séparément. Le paquet actuel ajoute notamment les matériaux NGeGenBrain v3.1 qu'il fallait inventorier.
2. **Pas de boucle complète et de robustesse** — les variantes F–J n'étaient pas exécutées à 90 epochs; il n'y avait pas les contrôles séparés (mises à jour désactivées, manquants, labels bruités/trompeurs, décalage de distribution) ni de métriques de détection des fingerprints.
3. **Pas de reconstruction sérieuse** — l'expérience `input1 → f → g → output2`, son baseline identité, ses goulots d'étranglement, l'activation, le contrôle de chemin de données et la boucle en ligne n'étaient pas présents.
4. **Coordination insuffisamment isolée** — absence du contrôle où la coordination globale est gelée et du contrôle utilisant des informations volontairement corrompues. La première livraison ne démontrait donc pas la propriété de réduction de façon indépendante.
5. **Sources et données** — aucun audit équivalent de l'ensemble des 80 archives imbriquées, des JSONL malformés/dupliqués et des manifeste/validateurs des versions v2 et v3.1.
6. **Audit indépendant et échecs** — pas d'audit automatique par recalcul des métriques depuis les prédictions test, pas de validation exhaustive des comptes par tâche, et les limites de campagne n'étaient pas assez clairement séparées des résultats acquis.
7. **Formalisme** — le document précédent était un développement très court et n'explicitait pas assez l'accès centralisé aux données, l'ordre causal des updates, l'état d'optimiseur, les conditions précises de convergence et les preuves de réduction/identifiabilité.

## Corrections appliquées à la livraison v2

La livraison actuelle conserve les archives sources immuables et le journal d'interruption/reprise. Elle comporte une reproduction exacte de référence, 165 exécutions principales (A–J+K, cinq tâches, trois graines), 60 exécutions d'ablation globale, 120 lignes de tests de boucle sur cinq architectures, 16 200 événements de fingerprint pour ce test de résistance, une expérience de reconstruction avec contrôle identité, et un audit automatisé final. L'audit de cette version précédente avait 43 contrôles sur 43 (v4). Dans la livraison courante, l'audit v6 recalcule les métriques depuis les prédictions et réussit 49/49 contrôles, dont cinq invariants supplémentaires pour le benchmark digits à dix classes.

Cette correction ne signifie toujours pas que la conclusion scientifique est universelle : le nombre de tâches, de partitions et de graines demeure limité, le coût en FLOPs/mémoire n'est pas strictement égalisé, et `0000.parquet` n'a pas pu être décodé faute de lecteur Parquet installé. Ces points restent déclarés dans les documents de livraison courante.
