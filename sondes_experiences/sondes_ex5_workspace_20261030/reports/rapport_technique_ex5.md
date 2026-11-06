# Rapport technique EX5 — méthode, résultats et limites

## 1. Références et protocole

Le prompt actif EX5 v1.1 est hashé et immuable. EX3/EX4 ont été repris en lecture seule ; aucune campagne EX4 déjà vérifiée n’a été réentraînée. Le jeu Wisconsin utilise la partition EX4 v009 pour développement seulement. Seeds : 1501/1607/1717/2029/3037. Les comparateurs MLP sont liés aux sondes par budget réel et seed, avec `P_total` incluant prétraitement/buffers. Les 390 associations candidate-comparateur sont dans le CSV de mapping ; aucune association attendue ne manque.

## 2. MLP matched/ge4x

Les ratios ge4x sont contrôlés par seed. Les journaux de comparaison indiquent des minima : MIXA registry 4,000735× ; RETRO 4,026448× ; Wine v3 4,019164× ; Digits v3 4,036137× ; OOF 4,007759× ; alternance stricte 4,037736×. Les topologies à deux niveaux (P=262/314/564) sont explicitement reliées aux entrées MLP communes ; par exemple 1052/262=4,0153×, 1283/314=4,0860× et 2273/564=4,0301×. Les comparateurs sont parfois réutilisés pour candidats ayant le même P_total et même seed, ce qui évite un réentraînement redondant ; chaque réutilisation est tracée par hash.

## 3. Micro-MIXA

Balayage fixe/adaptatif à quatre unités et capacité constante : 100/0, 75/25, 50/50, 25/75, 0/100. Le ratio 75/25 est le meilleur en log-loss sous gate égal. Les portes globales/input et modes conjoint/gate-only sont ensuite ablatés. Le gate input conjoint est meilleur que le gate global ; la géométrie d4/k4 avec ce gate produit LL 0,06187. Le meilleur OOF adaptatif LL 0,05218 est une architecture résiduelle deux-étages, pas le même modèle micro-MIXA de base.

## 4. RETRO et optimiser

Les triggers et traces alpha/beta sont étudiés ; les checkpoints pre-trigger et post-trigger sont distingués. Les déclencheurs maturation/inverse/gamma ont été atteints, mais la sélection globale retient souvent alpha=0 et les meilleurs checkpoints post-activation sont plus mauvais. Le plan Adam teste garder, réinitialiser, reconstruire, AdamW et absence de gel. Le gel strict saute `optimizer.step()` et garde poids/moments/compteurs inchangés ; un lr=0 ou grad=0 n’est pas une garantie de gel Adam. Aucun régime ne rétablit la log-loss après thaw.

## 5. Deux niveaux et alternance

Le niveau questions ne reçoit que X ; le niveau réponses a Y uniquement comme cible de pertes. Le forward d’inférence est exclusivement `forward(X)`. Les résidus d’étage OOF proviennent de base models qui n’ont pas vu les lignes qu’ils prédisent. L’alternance A/B sépare les partitions train A/B et vérifie les paramètres et états Adam du groupe gelé ; la révision stricte attend deux cycles complets consécutifs sans progrès avant arrêt.

## 6. Généralisation

Wine/Digits sont évalués après gel sur splits test non stratifiés par labels. Les performances sont descriptives. Les tests répliqués par seed ne sont pas indépendants. Aucun test EX4 (Iris/Wisconsin) n’est présenté comme nouveau test vierge. Banknote/MAGIC n’ont pas pu être récupérés via le réseau du conteneur malgré les miroirs UCI/OpenML/DataHub.

## 7. Limites statistique et ressources

Aucune marge numérique de non-infériorité n’était inscrite dans le pré-enregistrement ; les résultats ne peuvent pas être transformés rétrospectivement en test NI. Les moyennes et écarts-types sont rapportés, mais pas d’IC appariés/bootstrap/permutation ni correction de multiplicités. Les matrices de confusion et sous-groupes ne sont pas systématiquement livrés. Les MACs du forward sont analytiques ; backward/step non mesurés. Énergie indisponible ; VRAM indisponible ; RSS partiel. La règle rouge est échouée sur les dimensions mesurées, notamment latence et temps d’entraînement, en plus des performances.
