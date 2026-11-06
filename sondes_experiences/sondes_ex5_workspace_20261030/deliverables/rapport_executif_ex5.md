# EX5 — Rapport exécutif consolidé v001–v007

**État : campagne expérimentale exécutée sur les axes réalisables ; réussite scientifique globale non atteinte.**

EX5 a prolongé les travaux EX4 sans réentraîner les campagnes historiques déjà validées. Sept versions incrémentales contiennent RETRO et ses contrôles factoriels, les sémantiques Adam/gel, la correction alternée A↔B, les proportions fixe/adaptative, les topologies hiérarchiques question/réponse, les résidus OOF, l'optimisation par partage de centres/encodeurs et PCA question-only, le transfert Wine/Digits et le profilage de déploiement CPU.

## Résultats déterminants

- **Capacité :** 437 lignes de comparateurs MLP ge4x auditées ; aucun ratio inférieur à 4 ; minimum 4,000735×. Les deux bras OOF ont en plus 20 liens explicites (10 modèles physiques réutilisés) ; ge4x = 4,007759×.
- **RETRO :** les variantes maturation et inverse déclenchent sur 5/5 graines, mais le checkpoint global choisi reste pré-activation ; les meilleurs snapshots post-activation ont une log-loss nettement dégradée. Les autres couplages ne révèlent pas de gain stable.
- **Optimiseurs :** 25 essais Adam/AdamW ; 20/20 gels stricts passent. LR=0 ou gradient nul avec `step()` n'équivalent pas à un gel de l'état Adam.
- **OOF :** correcteur adaptatif, 1 160 paramètres, accuracy 97,65 %, log-loss 0,05218 ; MLP ge4x, 4 649 paramètres, accuracy 98,59 %, log-loss 0,05037. Temps pipeline 2,138 s contre 0,268 s ; latence p50 batch1 0,341 ms contre 0,0166 ms.
- **Hiérarchie Q/A :** le Q-only hybride à gate global est proche du MLP en log-loss de validation (0,05219 contre ≈0,05261), mais son pré-entraînement et sa latence sont beaucoup plus coûteux.
- **Transfert externe :** Wine et Digits évalués après gel ; aucune des six comparaisons ne démontre la non-infériorité conjointe pré-enregistrée.
- **v006 PCA-Q :** aucun des six candidats n'égale le MLP en accuracy et log-loss ; 30/30 ont moins de MACs forward, mais 0/30 ont une latence p50/p95 batch1 plus faible et 1/30 seulement un temps de pipeline au plus égal.
- **v007 compilation :** TorchScript trace exact 5/5, mais 7,75× plus lent en batch1 ; optimize-for-inference échoue au seuil de parité ; Numba v2 passe pour la sonde sur 1/5 seulement.

## Intégrité

1 850 JSON (périmètre v001–v007), 1 720 lignes JSONL, 1 313 références de checkpoints, 1 162 références canoniques de prédictions, 826 recalculs de métriques et 437 ratios ge4x ont été audités ; aucune erreur de hash, de parsing, de métrique recalculée ou de ratio inférieur à 4 n'est détectée. Les doublons et pointeurs superseded restent documentés et les originaux préservés.

## Audit intégral du workspace

L’audit final a contrôlé 3 951 fichiers non-cache : 1 865 JSON, 1 720 lignes JSONL et 60 CSV ; aucun problème de parsing ou de structure. Les deux copies de `prompt_ex5.json` sont identiques au hash attendu et aucun lien symbolique ne sort du workspace. Le manifeste SHA-256 complet se trouve dans `deliverables/sha256_manifest_workspace_final.csv`.

## Limites et verdict

Banknote/MAGIC n'ont pas pu être téléchargés à cause de l'indisponibilité DNS du runtime. L'environnement est CPU-only, sans instrument d'énergie ni VRAM ; les MACs complets d'entraînement et une télémétrie RSS uniforme restent indisponibles. Les ressources de latence et de temps d'entraînement restent généralement supérieures au MLP. **Aucune candidate ne satisfait ensemble la qualité prédictive et toutes les dimensions obligatoires de la règle rouge.** EX5 n'est pas déclaré complet au sens de la réussite scientifique globale.

Voir `rapport_reprise_finale_ex5.md` pour le diagnostic détaillé, les exceptions et les chemins de preuve.


## 10. Complétude OOF et canonicalisation MIXA

La variante OOF est livrée avec son code et ses dépendances, 25 checkpoints fold, 25 checkpoints de reprise avec états optimiseurs, 25 marqueurs, cinq caches OOF, dix checkpoints composites, dix reprises de tête, dix fichiers métriques, dix prédictions et 20 liens MLP. L'audit dédié recense 162 artefacts, 0 manquant ; chaque ligne train est prédite par le fold qui ne l'a pas vue, les logits OOF/validation/composite et métriques se reproduisent avec écart maximal 0, et `forward(self, x)` ne reçoit que X.

La nomenclature canonique est `MIXA` pour la famille générale et `micro-MIXA` pour la reconstruction compacte. `MiXA` et `micro-MiXA` sont des alias de casse uniquement ; `mixa_micro_d4_k8` est un identifiant historique rattaché à micro-MIXA, mais son nombre de coefficients de 528 dans les débris n'est pas vérifiable depuis un checkpoint source.

L'audit final du workspace compte 3 951 fichiers non-cache : 1 865 JSON valides, 1 720 lignes dans 53 JSONL, 60 CSV rectangulaires ; prompt externe/interne identique au SHA-256 attendu, aucun lien symbolique sortant et aucune erreur de parsing/forme. Les audits globaux de versions donnent 1 850 JSON valides, 1 313 références checkpoint sans échec, 1 162 références canoniques de prédiction sans échec, 826 recalculs de métriques sans divergence et 437 comparaisons MLP ge4x, minimum 4,000735×.
