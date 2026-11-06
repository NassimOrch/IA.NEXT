# Tableau de conformité EX4 — état final du 30 octobre 2026

| Exigence du prompt | Statut | Preuve / réserve |
|---|---|---|
| Inventaire/hash des archives sources | Respecté | `inputs/archive_integrity.json`; ZIP original et ZIPs imbriqués testés |
| Extraction rigoureuse de `debrit_0.txt` | Partiel mais réalisé | `debrit_0_reconstruction.md`; chiffres narrés restent non vérifiables faute de données brutes |
| Workspace EX3 complet récupéré | Bloqué par absence | Code, checkpoints, états optimiseur, partitions et prédictions EX3 absents |
| Copie EX3 vers EX4 et correction du prompt | Respecté | `prompt_ex4.json`, JSON parsé ; objectif P_total harmonisé ; micro-MIXA ajouté |
| Candidate EX2/v009 reconstruite | Partiellement respecté | d16/k32 référencée sur Wisconsin ; pas de reconstitution intégrale du pipeline EX2 externe |
| Sondes micro / croissance dynamique | Respecté en développement | v005/v006, cinq seeds et géométries ; croissance instancie les experts actifs uniquement |
| RETRO `beta_local=1-alpha` | Partiel | `retro_linear` activé mais dégrade les résultats/ressources ; RETRO par plateau s'active après checkpoint retenu |
| MIXA adaptatif + fixe + gate | Respecté (implémenté) | v007/v008 et transfert v009 ; aucune supériorité complète démontrée |
| Micro-MIXA (hybride) | Respecté comme reconstruction expérimentale | v008 cinq bras, 25 runs ; v009 adaptatif + trois modes MIXA ; pas identité revendiquée avec prototype EX3 |
| Comparaisons fixe-only/adaptatif-only/mixa et ablations | Partiel | fixe-only mesuré sur Wisconsin ; adaptatif et trois MIXA sur Wisconsin/Iris ; deux pré-vol fixed-only Iris quarantinés |
| P_train et P_total fixes + appris + scaler | Respecté dans audits v006/v008/v009 | scaler ajouté aux deux côtés ; comptes vérifiés |
| MLP comparateurs ≥4× P_total | Respecté dans les campagnes auditées | v006 60/60 ; v008 25/25 ; v009 toutes comparaisons ge4x ≥4,015625× |
| Accuracy et log-loss non inférieures | Non respecté / non démontré | Les log-loss sonde/MIXA restent supérieures aux MLP ; aucune non-infériorité formelle |
| Temps d'entraînement ≤ MLP | Non respecté sur MIXA mesurées | v006/v009 plus lents ; cinq fit-times adaptatifs Iris indisponibles, pas imputés |
| Latence ≤ MLP | Non respecté | Latence médiane sonde sensiblement supérieure aux MLP sur Wisconsin et Iris |
| Comptage MAC/FLOPs matériel complet | Partiellement mesuré | v009 estimate analytique incomplet, pas de compteur matériel ; v006 non mesuré |
| RSS | Partiel | v008 RSS global du processus échantillonné ; pas allocation isolée |
| VRAM | Non mesuré | PyTorch CPU / CUDA indisponible |
| Énergie | Non mesuré | Aucun compteur fiable disponible |
| Taille sérialisée | Partiellement respecté | `state_dict` + scaler mesurés ; package complet et runtime non profilés |
| Test final v006 Wisconsin | Non ouvert | Données historiquement exposées ; pas de métrique test pour ne pas requalifier l'historique |
| Transfert externe indépendant | Partiel | Iris exploratoire exécuté (30 test, 5 initialisations), un seul dataset |
| Isolation test stricte v009 | Partiel avec réserve explicite | Aucun test dans fit/prétraitement/sélection/metrics avant gel ; `load_iris` charge tout et stratification lit labels ; pas d'isolation mémoire absolue |
| Banknote/MAGIC | Bloqué par accès données | Téléchargements UCI échoués (DNS/réseau indisponible) ; aucun résultat inventé |
| Métriques réconciliées avec prédictions brutes | Respecté | tests v005/v006, audits v008/v009 recalculent métriques |
| Test d'intégrité v005 | PASS | `versions/...v005/tests/test_ex4_integrity.py` |
| Test d'intégrité v006 | PASS | `versions/...v006/tests/test_ex4_integrity.py` |
| Test global v007 | FAIL ATTENDU SUR REGISTRE MÉLANGÉ | 95 lignes réelles vs 70 attendues ; les audits filtrés initial/micro-MIXA passent |
| Audit micro-MIXA v008 | PASS | 25 sondes, 30 MLP, 50 paires, no test access |
| Audit transfert Iris v009 | PASS | JSONL, predictions, metrics, hashes, partitions, ratios, checkpoints, isolation caveat |
| Livrables et archive de reprise | Respecté pour les artefacts disponibles | `manifest_livrables.md`, `rapport_continuite_finale_ex4.md`, ZIP final vérifié et SHA-256 ; limites restantes listées explicitement |

## Conclusion de conformité
Le prompt EX4 a été exécuté jusqu'aux comparaisons micro-MIXA et à un premier transfert externe ; il n'est pas satisfait au sens fort de tous les domaines et de toutes les mesures de ressources. Le résultat scientifique final est négatif quant au succès complet : compacité démontrée, avantage simultané de log-loss et de ressources non démontré. Les blocages et données non récupérables sont explicitement identifiés ; aucune métrique ou expérience absente n'est inventée.
