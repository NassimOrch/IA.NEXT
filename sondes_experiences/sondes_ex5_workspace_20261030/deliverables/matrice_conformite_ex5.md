# Matrice de conformité EX5 — état consolidé v001–v007

L’état est attribué à l’exigence, pas à la seule présence d’un fichier. `RESPECTÉ` signifie que la procédure ou le contrôle a été exécuté ; cela ne signifie pas que la candidate a obtenu une victoire prédictive. `NON_RESPECTÉ` signale que le critère de réussite n’est pas satisfait, `PARTIEL` qu’une partie des mesures ou expériences reste incomplète, `BLOQUÉ` qu’une contrainte externe empêche l’exécution, et `NON_MESURÉ` qu’aucune mesure instrumentée n’existe.

| Exigence | Statut | Preuve / limite |
|---|---|---|
| Lire EX5/EX4/EX3, cohérence et inventaire | **RESPECTÉ** | prompts relus; inventaire versions v001–v007; audits globaux |
| Préserver les sources et résultats EX2/EX3/EX4 | **RESPECTÉ** | versions et archives historiques non modifiées; EX5 versionné |
| Hashes et intégrité JSON/JSONL | **RESPECTÉ** | 1 850 JSON valides dans v001–v007; 1 720 lignes JSONL valides; 0 erreur parse |
| Hashes checkpoints | **RESPECTÉ** | 1 313 références; 0 échec |
| Hashes prédictions canoniques | **RESPECTÉ** | 1 162 références; 0 échec; 40 pointeurs superseded documentés |
| Recalcul métriques à partir prédictions | **RESPECTÉ** | 826 fichiers recalculés; 0 divergence |
| Paramètres MLP ge4x | **RESPECTÉ** | 437 liens; min 4.000735; 0 inférieur à 4 |
| RETRO maturation post-activation | **PARTIEL** | triggers/rampes/checkpoints pré/post conservés; checkpoint choisi souvent pré-activation; aucun gain stable post-activation |
| Facteur alpha×beta | **PARTIEL** | contrastes et variantes réalisés; preuve formelle/statistique limitée par petit jeu développemental |
| Audit Adam/gel strict | **PARTIEL** | 25 essais v2; 20/20 gels stricts; moments/steps/scheduler par époque incomplets sur les vieilles expériences |
| Proportion fixe/adaptative budget constant | **RESPECTÉ** | cinq ratios d’ancrage, cinq seeds; rho/branch counts/P_total fournis |
| Optimisation micro-MIXA | **PARTIEL** | gates, centres/encodeurs partagés, PCA-Q et vectorisation; recherche ouverte non exhaustive et règle rouge échoue |
| Alternance A↔B correcteur | **RESPECTÉ** | 7 bras ×5 seeds; contrôles stricts de gel; MLP matched/ge4x |
| Hiérarchie questions→réponses | **PARTIEL** | hybride/hybride, fixe→adaptatif, adaptatif→fixe, Q-only, answer-side, OOF et contrôles; ressources complètes et non-infériorité non atteintes |
| Cloisonnement X/Y à l’inférence | **RESPECTÉ** | forward(X) seulement; PCA Q-only fit X_train; hashes de PCA recalculés |
| MLP matched/ge4x nouvelles candidates | **RESPECTÉ** | comparaisons appariées; MLP réutilisés uniquement par budget exact et seed; liens traçables |
| Statistiques non-infériorité externe | **RESPECTÉ** | pré-enregistrement avant test; bootstrap apparié 20k et Bonferroni; résultats indiquent aucun pass conjoint |
| Généralisation multi-domaines | **PARTIEL** | Wine et Digits exécutés; tous NI conjoints échouent; Banknote/MAGIC bloqués DNS; Iris antérieur exploratoire |
| Ressources : forward MACs | **RESPECTÉ** | mesurés/analytiques et comparés; sonde ≤ MLP sur tous les liens documentés |
| Ressources : temps entraînement | **NON_RESPECTÉ** | mesuré; généralement supérieur au MLP (par ex. 16/235 seulement au plus égal en V1/V2; 1/30 en V6); training MACs complets non mesurés |
| Ressources : latence batch1 p50/p95 | **NON_RESPECTÉ** | mesurée; généralement plus élevée que MLP (0/235 V1/V2 p50, 0/30 V3, 0/30 V6); quelques exceptions V4 insuffisantes pour satisfaire globalement la règle rouge |
| Ressources : RAM/RSS | **PARTIEL** | mesures RSS disponibles mais variables; instrumentation RSS peak not complete for all pipelines |
| Ressources : bytes déployés/checkpoint | **PARTIEL** | bytes de déploiement mesurés et souvent inférieurs; tailles checkpoint/états optimiseur pas uniformes dans chaque branche historique |
| Ressources : énergie | **NON_MESURÉ** | aucun instrument énergétique |
| Ressources : VRAM | **NON_MESURÉ** | environnement CPU-only, pas de GPU |
| Banknote/MAGIC externes | **BLOQUÉ** | téléchargement UCI échoue DNS; datasets non matérialisés |
| Règle rouge de réussite globale | **NON_RESPECTÉ** | aucune candidate n’égale simultanément MLP en prédiction et chaque dimension de ressources |
| Anti-triche / test scellé V3 | **RESPECTÉ** | manifest freeze avant test; test pas utilisé pour sélection |
| Archive et SHA final | **RESPECTÉ** | ZIP créé, unzip -t vérifié, SHA externe |
| Non-infériorité prédictive externe (résultat des candidates) | **NON_RESPECTÉ** | 6/6 comparaisons conjointes Wine/Digits échouent aux marges pré-enregistrées après bootstrap et Bonferroni |
| Appariement MLP matched/ge4x des deux correcteurs OOF | **RESPECTÉ** | 20 liens candidate×seed×type ; MLP réutilisés par P_total exact 1160 et seed ; 10 modèles physiques partagés ; ge4x 4649/1160=4.007759 ; hashes et métriques recalculés |
| Profilage compilation CPU v007 avec parité stricte | **PARTIEL** | TorchScript trace exact 5/5 mais 7.75× plus lent en batch1 ; optimize_for_inference exclu (différence probe/MLP >1e-6) ; Numba v2 parité sonde 1/5 ; Numba v1 invalide ; aucun gain de latence conforme |
| RETRO : séparation checkpoint sélectionné / snapshots post-activation | **RESPECTÉ** | retro_post_activation_summary_ex5.csv ; 12 familles ×5 seeds ; pre/post/select séparés ; 1 doublon retro_linear/1501 conservé et audit timing conservateur |
| Correcteur résiduel OOF : appariement et coût pipeline complet | **PARTIEL** | OOF 5 plis, 5 seeds, résidus de train OOF et forward X-only ; ratios ge4x validés ; log-loss/latence/temps restent derrière MLP ge4x |
| Audit final v007 des exports compilés | **RESPECTÉ** | 25 exports (20 modules + 5 scalers) SHA-256 vérifiés ; trois fonctions de test passées individuellement ; aucun test accédé |
| Mesure training MAC / énergie / VRAM | **NON_MESURÉ** | MAC forward disponibles analytiquement ; MAC complets de training non instrumentés ; CPU-only sans VRAM ; aucun capteur énergie |
| Données Banknote/MAGIC | **BLOQUÉ** | Tentatives UCI/OpenML ; résolution DNS indisponible dans le runtime, aucun fichier ni résultat synthétique créé |

| Nomenclature MIXA/micro-MIXA et variantes/artefacts | **RESPECTÉ** | `NOMENCLATURE_EX5.md`, `nomenclature_registry_ex5.json`, catalogues campagnes/variantes ; MiXA et micro-MiXA sont alias de casse, pas des modèles distincts |
| Complétude des artefacts OOF | **RESPECTÉ** | 162 entrées, 0 manquante ; 25 folds, 10 composites, 20 liens MLP ; parité des prédictions/logits et métriques exactement 0 |


### Portée exacte des tests v007

Les trois fonctions de test de `v007/tests/test_profile_integrity.py` ont été importées et appelées individuellement ; elles passent. La collecte pytest globale a dépassé la fenêtre d’exécution disponible et n’est pas déclarée PASS. Les backends `torch.jit.optimize_for_inference` et Numba non conformes restent exclus selon le seuil de parité pré-enregistré.
