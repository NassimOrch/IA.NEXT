# NG-ADAPT — livraison finale de recherche

**Campagne :** `NG-ADAPT-2026-10-29-v1`  
**Version de l’audit indépendant :** `NG-ADAPT-INDEPENDENT-AUDIT-v6`
**But :** confronter les architectures de sondes adaptatives locales, coordonnées globalement, activées et dotées d'une boucle observation–empreinte–mise à jour, sans présumer de leur supériorité.

## Lire dans cet ordre

1. [`SYNTHESE_EXECUTIVE.md`](SYNTHESE_EXECUTIVE.md) — conclusions et statut de chaque hypothèse.
2. [`ETAT_DES_PHASES.md`](ETAT_DES_PHASES.md) et [`CONFORMITE_PROMPT_DETAILLEE.md`](CONFORMITE_PROMPT_DETAILLEE.md) — exigences du `prompt.txt`, phase par phase et règle rouge par règle rouge.
3. [`FORMALISME_ADAPTATION_GLOBALE.pdf`](FORMALISME_ADAPTATION_GLOBALE.pdf) — définitions, équations, hypothèses et preuves conditionnelles. Le `.tex` est fourni à côté.
4. [`RESULTATS_COMPLETS.md`](RESULTATS_COMPLETS.md) — tables par tâche, architectures, ablations, boucle et reconstruction.
5. [`PROTOCOLE_PREENREGISTRE.md`](PROTOCOLE_PREENREGISTRE.md), [`docs/PROTOCOLE_FEEDBACK_FINGERPRINT.md`](docs/PROTOCOLE_FEEDBACK_FINGERPRINT.md) et [`docs/PROTOCOLE_BOUCLE_RECONSTRUCTION.md`](docs/PROTOCOLE_BOUCLE_RECONSTRUCTION.md) — protocoles de base et suppléments causaux.
6. [`sites_web_consulte.json`](sites_web_consulte.json) — registre des pages consultées, requêtes, motifs d’utilisation, dispositions et limites de traçabilité historique.
7. [`AUDIT_INDEPENDANT.md`](AUDIT_INDEPENDANT.md) et [`LIMITES_ET_INCERTITUDES.md`](LIMITES_ET_INCERTITUDES.md) — ce que l'audit établit et ce qu'il n'établit pas.
8. [`REPRODUIRE_LES_EXPERIENCES.md`](REPRODUIRE_LES_EXPERIENCES.md) — commandes et reprise par tâche, sans réentraîner les runs déjà calculés.
9. [`INVENTAIRE_SOURCES.md`](INVENTAIRE_SOURCES.md), [`ENVIRONNEMENT.md`](ENVIRONNEMENT.md), [`REGISTRE_DES_AFFIRMATIONS.md`](REGISTRE_DES_AFFIRMATIONS.md), [`JOURNAL_EXECUTION.md`](JOURNAL_EXECUTION.md) — provenance, environnement et statut des affirmations.

## Résultats exécutés

- Vérification de l'intégrité de l'archive source et contrôle récursif de **80 archives ZIP imbriquées**, sans échec d'intégrité ni chemin d'extraction dangereux détecté.
- Rejeu strict du script de référence « two moons » : CSV et JSON reproduits octet par octet.
- **198 entraînements A–K sur six tâches** : 165 entraînements (cinq tâches binaires) + 33 runs digits à dix classes; **38 313 prédictions de test** (29 403 binaires + 8 910 multiclasse). S’ajoutent 60 exécutions d’ablation de coordination, 120 lignes métriques / 16 200 empreintes de robustesse, 390 lignes / 54 000 empreintes dans FBR-1, 148 lignes métriques de reconstruction et RBF-R1 (162 lignes / 23 040 empreintes).
- Audit indépendant v6 : **49/49 contrôles réussis**; cinq contrôles additionnels couvrent l’extension digits10 et l’audit de provenance web est consigné.
- Tests logiciels des projets sources : observation formalisme 109 pages vérifié par son validateur, v1.2 `PASS_WITH_LIMITATIONS` (16/16), v2 117 tests + 10 sous-tests, v3.1 66 tests et test de non-régression V1 65 tests.

Ces succès sont des résultats de reproductibilité et d'ingénierie, pas une preuve de supériorité scientifique universelle. Les six tâches de benchmark (cinq binaires et une multiclasse) utilisent chacune un split fixe et trois graines d'optimisation. L'effet de la coordination et de la boucle varie selon la tâche; une mise à jour en ligne sous labels trompeurs peut provoquer une dérive grave.

## Arborescence

- `code/` — exécuteurs de benchmark, boucle, reconstruction et audit indépendant.
- `configs/` — configuration globale.
- `requirements.txt` et `ENVIRONNEMENT_LOCK.txt` — dépendances épinglées et versions observées.
- `results/` — CSV/JSON de métriques, prédictions, partitions, audits de jeux de données et manifests.
- `figures/` — graphiques finaux des effets FBR-1 et RBF-R1, plus la planche contact des sept pages du PDF contrôlée visuellement; les données à l’origine des figures sont les CSV fournis.
- `logs/` — sorties standard, erreurs et codes de sortie; un run monolithique interrompu est gardé à titre de trace.
- `sites_web_consulte.json` — registre des **40 URL uniques et 28 requêtes** de recherche documentées, avec motifs, dispositions et limites de traçabilité historique.
- `source_copies/` — copies de référence des fichiers sources théoriques prioritaires et du `prompt.txt`; le manifeste exhaustif des fichiers extraits et leurs SHA-256 se trouve dans `results/source_audit/recursive_source_file_manifest.csv`.
- `FORMALISME_ADAPTATION_GLOBALE.{tex,pdf}` — formalisme ajouté.
- `docs/` — protocoles, comparaisons, limites et rapports.

## Intégrité

Le prompt de base est évalué phase par phase dans `CONFORMITE_PROMPT_DETAILLEE.md`. Les phases 1, 4 (couverture complète de toutes les boucles par tâche/architecture) et 8 restent partielles pour les raisons explicites du rapport; la livraison ne les déclare pas satisfaites au-delà des éléments réellement exécutés.

Consulter `SHA256SUMS.txt` pour les empreintes de tous les fichiers livrés, à l'exception du manifeste lui-même. Après extraction, `python3 code/validate_delivery.py` contrôle ce manifeste, les fichiers structurés et le PDF sans modifier la livraison. L’archive distribuée `sonde_adapt_global_research_final.zip` a un SHA-256 externe dans le fichier compagnon `SHA256SUMS_DELIVERY.txt`, livré séparément. L'archive a passé `unzip -t`, puis l'extraction a passé les 8 contrôles de `code/validate_delivery.py`. Les archives originales n'ont pas été modifiées et ne sont pas recopiées intégralement dans la livraison : leurs empreintes, résultats de validation et extractions sont documentés.
