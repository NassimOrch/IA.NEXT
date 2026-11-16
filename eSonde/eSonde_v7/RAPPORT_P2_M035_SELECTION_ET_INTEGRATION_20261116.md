# Rapport M-035 — sélection de la fusion dialogique et intégration runtime

**Date :** 16 novembre 2026  
**Phase :** P2 — laboratoire expérimental, non clôturée  
**Architecture :** Obsiss/sondes uniquement ; aucun neurone, MLP, GRU, embedding appris ou rétropropagation.

## Objet

Sélectionner la contribution des associations contexte→réponse et des transitions de réplique pour le profil `screenplay_dialogue`, puis intégrer la règle retenue dans les canaux Obsiss existants sans ajouter de dimension. La sélection est faite sur VALIDATION ; TEST n'est utilisé qu'une fois après gel de la règle.

## Résultats mesurés

Le jeu dérivé comprend 346 segments TRAIN (13 scènes sources), 30 segments VALIDATION (1 scène) et 49 segments TEST (3 scènes). Les segments d'une scène restent dans une seule partition.

- VALIDATION : transition seule (poids association 0, transition 1) = **0,62218** de rang normalisé moyen ; association seule = **0,51870** ; fusion 50/50 = **0,57044**. Le critère choisit le maximum parmi les règles testées.
- Référence de fréquence globale sur VALIDATION : **0,91988**, supérieure à toutes les variantes apprises testées.
- TEST, règle gelée évaluée une seule fois : transition seule = **0,62004** sur 770 tokens cibles couverts sur 967 (couverture 0,79628), trois scènes ; référence de fréquence globale = **0,91353**.
- La fusion M-032 50/50 avait obtenu **0,55418** sur le même TEST. M-035 améliore ce rang relatif au modèle M-032, mais reste nettement sous le prior global.

**Sens de la métrique :** le rang normalisé est meilleur lorsqu'il est plus élevé. Ces scores mesurent un classement teacher-forced de tokens cibles, pas la qualité d'une réponse libre, la cohérence globale ou la généralisation ouverte. Les 770 tokens ne sont pas 770 dialogues indépendants.

## Intégration technique

Pour `screenplay_dialogue`, le runtime ne propose plus les candidats de l'association contextuelle entraînée ; les transitions apprises alimentent le canal `local_transition` existant. Le canal `dialogue_association` historique reste présent, normalisé par rang. Les profils d'autres domaines conservent leur comportement antérieur jusqu'à une sélection propre à leur domaine. Aucun canal, Obsiss ou paramètre neuronal n'est ajouté.

La suite de tests Dmodel passe à **51/51**. Le test dédié vérifie que le profil scénario suit bien la règle sélectionnée et que l'ensemble des 16 canaux est conservé.

## Provenance et intégrité

Le fichier profil utilisé au moment du scoring avait SHA-256 `50ee62059b8d4a6e0cc936f92372a4a0b15c59646f2a322f7f4ae65480886998`. Après le scoring, seule la métadonnée top-level `fusion.M035_validation_selected_screenplay` a été ajoutée ; le sous-arbre `profiles` qui contient les données apprises est resté identique (empreinte canonique `ca1678432fc1134b5ccf8762a99a7b58d51de64d3766f84bdd483960612e01ea`). Le rapport n'a pas relancé le TEST.

Le JSON de résultat est `experiments/P2_M035_CONTEXT_FUSION_SELECTION_20261116.json`, SHA-256 `8d03e9d26776bd4bc68eab88e17e81cbd413afcf81ab4d938eb68b2d62adcda2`.

## Conclusion et statut

M-035 fournit une règle d'intégration définie par VALIDATION et un TEST gelé reproductible. Elle améliore l'ancienne fusion M-032 sur le classement des tokens scénarios, mais n'améliore pas le prior de fréquence globale. La qualité conversationnelle libre et la généralisation ne sont donc pas démontrées. P2 demeure ouverte ; aucune architecture n'est promue comme solution générale sur ces mesures seules.
