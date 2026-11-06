# Rapport complet de tests AAM O94.5 — audit, corrections, résultats et statut

**Date : 20 octobre 2026.** La version est documentée comme un incrément descendant d'O94.4; le manifeste parent O94.4 reste figé, tandis que le delta O94.5 est couvert par `sav_AAM_O94_5`.

## 1. Description

Cette campagne a vérifié les défauts concrets notés sur O94.4 : bundle local Transformers choisi via le fichier de poids, observation outillée, compilation compositionnelle effective, feedback causal et intégration de ces voies dans la chaîne du chat. Elle inclut des tests unitaires, d'intégration, UI sous Xvfb, CLI et scénarios réels locaux générés par les outils installés. Les poids SmolLM2 de l’utilisateur n'étaient pas présents dans les archives fournies.

## 2. Architecture auditée

- `aam_o93/model_integration.py` : inspecteur de bundle, registre, génération locale, policy d'entraînement et intégrité SHA-256.
- `aam_o93/observation_tools.py` et `runtime.py` : Tesseract, Poppler, FFprobe/FFmpeg, empreinte des octets bruts, privacy/redaction du rapport, dérivés RAG et mémoire.
- `aam_o93/composition_compiler.py`, `composition_runtime.py`, `code_workbench.py`, `code_editor_app.py` : DSL JSON validé, émission Python, compilation CPython/bytecode, manifeste, atelier de code et diagnostics.
- `aam_o93/reward_policy.py`, `memory.py`, `autonomy.py` : préférences, fiabilité opérationnelle, résultats vérifiés, journal causal et idempotence.
- `aam_o93/cli.py`, `ui.py`, `rag.py` : routage chat, sélection modèle/compétence, contexte RAG, pièces jointes, résolution continue et interface.

## 3. Pipeline complet et commandes

### Contrôle séquentiel et sauvegarde

Avant l’exécution, le runner a consulté `chemins_O94_5.json`, `checklist_de_travail_O94_5.json`, les deux checklists d'erreurs, `sav_AAM_O94_5/savepoint_manifest.json` et le manifeste parent O94.4. Le gate final pré-campagne a rendu `PASS_BOUNDED`; 49 fichiers parent et 143 fichiers O94.5 étaient vérifiés.

```bash
python scripts/refresh_o945_savepoint.py
python scripts/preflight_o945.py
python -m aam_o93 status
```

### Suite complète

```bash
python scripts/run_o945_full_suite.py --timeout-seconds 420
```

Le runner vérifie le gate séquentiel, force une session Xvfb neuve si disponible, écrit des chemins de log/reçu uniques pendant l’exécution, puis ne met à jour les alias stables qu'après la sortie de pytest. Reçu final : `receipts/O94_5/P6_full_suite_regression_20261020T114952Z_19680.json`; journal : `logs/O94_5/P6_full_suite_regression_20261020T114952Z_19680.log`.

### Batteries ciblées exécutées

```bash
pytest -q tests/test_o945_observation_multimedia_ffmpeg.py tests/test_o945_observation_reward.py
pytest -q tests/test_o945_composition_compiler_workbench.py tests/test_o945_compiled_project_audit.py tests/test_o945_chat_composition_dispatch.py
pytest -q tests/test_o945_transformers_bundle.py tests/test_o943_model_adapter_contracts.py
pytest -q tests/test_o945_causal_reward_routing.py tests/test_o945_reward_runtime_integration.py tests/test_o943_runtime_integration.py tests/test_o943_learned_blocks_and_composition.py
pytest -q tests/test_o943_passive_observation.py tests/test_o943_cli_live_e2e.py
pytest -q tests/test_o940_rag_resolution.py tests/test_o940_memory_resolution.py tests/test_o943_ui_contracts.py tests/test_o940_real_sms_corpus_sample.py
```

Les exécutions correspondantes sont consignées sous `receipts/O94_5/` et `logs/O94_5/`. Les commandes ci-dessus résument les batteries; les reçus contiennent les commandes exactes exécutées (avec Xvfb/timeout là où requis).

## 4. Résultats et interprétation

### 4.1 Résultat final global

| Mesure | Résultat final |
|---|---:|
| Tests réussis | **419** |
| Échecs | **0** |
| Sous-tests réussis | **21** |
| Avertissements | **5** |
| Durée pytest | **199,38 s** |
| Timeout | Non |
| Display UI | Xvfb |
| Statut du reçu | `PASS_BOUNDED` |

Le code retour du runner est 0; son reçu lie le résultat au SHA-256 du log. Une tentative précédente a produit 419 lignes de progression mais n’a pas finalisé de reçu à cause de l'interruption de l'orchestrateur : elle est conservée dans l'historique mais n’est pas utilisée comme preuve de clôture. La campagne détachée suivante a écrit son propre reçu final et clôturé cette incertitude.

### 4.2 Preuves ciblées principales

| Domaine | Reçu | Résultat | Interprétation |
|---|---|---:|---|
| Observation Tesseract/PDF/FFmpeg/FFprobe | `P6_real_tool_observation_regression.json` | 7 réussis, 0 échec | Outils réellement invoqués sur images, PDF scanné et médias locaux synthétiques; l'ASR reste conditionnel à un modèle local. |
| Composition, compilateur, éditeur et dispatch chat | `P6_composition_compiler_editor_dispatch.json` | 10 réussis, 0 échec | DSL compilé, projet Python analysé et exécuté, diagnostics ligne/colonne, compilation LaTeX réelle et chemin de composition exercés. |
| Bundles de modèles/adaptateurs | `P6_local_model_adapter_regression.json` | 15 réussis, 0 échec | Résolution de fichier de poids vers bundle, validation, refus des bundles incomplets, intégrité et contrat de génération testés. Les poids SmolLM2 réels ne sont pas certifiés. |
| Feedback causal, autonomie et composition | `P6_reward_autonomy_composition_regression.json` | 11 réussis, 0 échec | Distinction préférence/fiabilité/vérification, événements et routage causal testés. |
| Observation live + CLI | `P6_passive_live_observation_cli.json` | 8 réussis, 0 échec | Capture filesystem/processus autorisée et appels CLI couverts. |
| RAG, mémoire, UI, échantillon SMS | `P6_rag_memory_ui_real_corpus.json` | 34 réussis, 0 échec | Recherche sémantique, mémoire et échantillon réel du corpus SMS couverts. |
| Contrat de statut des décodeurs | `P6_status_contract_fix_targeted_20261020T114506Z_18578.json` | 2 réussis, 0 échec | Deux attentes de test ont été mises en accord avec `PASS_BOUNDED`, statut déjà défini pour un décodeur local réussi à couverture bornée; aucun contrôle d'intégrité n’a été retiré. |

Les nombres des batteries ciblées se recouvrent avec la suite globale; ils ne doivent pas être additionnés au total 419.

### 4.3 Défauts corrigés et incidents du harnais

1. **`model.safetensors` isolé** : sélection du parent du bundle, inventaire SHA-256 et validation configuration/tokenizer. Un bundle incomplet reste un brouillon diagnostique non chargeable.
2. **Observation sans texte OCR/ASR** : l’observation conserve une empreinte des octets bruts et des métadonnées même si aucune sémantique textuelle n’est extraite.
3. **Frames vidéo** : le statut FFmpeg n’est pas suffisant; le rapport vérifie que le PNG est effectivement matérialisé et hashé.
4. **Reward/routage** : préférence, fiabilité opérationnelle et vérification indépendante ont des dimensions propres; doublons idempotents et `UNRESOLVED` ne reçoit pas de pénalité automatique.
5. **Runner et sauvegarde** : les logs/reçus par tentative sont uniques pendant pytest et les alias stables ne sont mis à jour qu'après la fin de la suite, afin qu’ils ne changent pas sous le contrôle SHA-256 du runtime.
6. **Tests de statut** : deux assertions héritées attendaient `PASS`/`PARTIAL`, sans `PASS_BOUNDED`. Les tests ont été alignés sur le contrat existant et rejoués en 2/2; le moteur n’a pas été modifié pour masquer un échec.

La première campagne à `DISPLAY=:0` n'était pas une preuve valide d'échec UI lorsque X n'existait pas. Les campagnes suivantes ont forcé Xvfb. Les essais complets antérieurs avec des échecs sont conservés dans les reçus/journaux; seule la campagne finale `419/0` clôt la régression.

## 5. Conséquences théoriques, conceptuelles et opérationnelles

- **Théoriques** : une observation est une chaîne instrumentée (source → décodeur → extraction → empreinte → provenance), pas une simple étiquette `observe`. Un hash prouve l’intégrité des octets, pas la compréhension. Un résultat non résolu ne prouve pas l'impossibilité.
- **Conceptuelles** : les briques de base (compétence, méthode, règle, vérificateur) ont des contrats distincts; la composition ordonne ces briques, puis le compilateur et le runtime restent auditables. Le reward n’a pas le droit de réécrire la vérité évaluée.
- **Opérationnelles** : le système a des rapports, des logs, des reçus machine, des hashes, des budgets d'exécution et un mécanisme de restauration. L'atelier sert réellement à éditer, compiler et diagnostiquer du code, sans être présenté comme un bac à sable OS.

## 6. Incertitudes et domaines encore non certifiés

- L'inférence native du vrai SmolLM2-360M sur les fichiers utilisateur est **non vérifiée dans cette session** : poids/config/tokenizer absents des archives et tentative d'installation Transformers bloquée par absence d'accès au dépôt de paquets. Le guide donne la procédure sur la machine qui détient le bundle; l'incident est maintenu ouvert.
- Un fichier `.pt` ou `.pth` seul ne décrit pas automatiquement une architecture. Les bundles Transformers, TorchScript et adaptateurs personnalisés sont des contrats différents; un modèle totalement arbitraire nécessite l’architecture/adaptateur approprié.
- L'ASR n’est pas prétendu fonctionnel sans les poids d’un moteur local configuré. Les outils disponibles produisent toutefois un décodage média, métadonnées et caractéristiques acoustiques.
- Aucun déploiement SQL distant, caméra physique, capture réseau sur interface matérielle ou reproduction généralisée d’un logiciel propriétaire n’est revendiqué par cette campagne.
- Les cinq avertissements sont conservés; les avertissements TorchScript des campagnes antérieures signalaient des API dépréciées (`torch.jit.trace`, `torch.jit.trace_method`, `torch.jit.load`). La commande de la campagne finale a demandé `--disable-warnings`, donc elle en compte le total sans imprimer chaque avertissement dans le log.

## 7. Conclusion et statut du modèle

**P6 est `COMPLETE_EVIDENCED`** selon ses critères de sortie : campagne large à zéro échec et reçus ciblés pour observation outillée, compilation/exécution compositionnelle, modèle, reward/autonomie, observation live et RAG. P7 (formalisation, guide, registre et restauration) est en cours; P8 (construction/audit ZIP) n’est pas considéré complet tant que les trois archives n’auront pas été vérifiées depuis des extractions vierges.

Cette conclusion est limitée aux preuves testées. Elle n’affirme pas que toutes les architectures ou toutes les tâches possibles sont déjà prises en charge, et ne déduit pas le potentiel futur d'AAM des contraintes rencontrées ici.


## Addendum P7 — documentation, préflight et restauration

P7 a passé 14 contrôles avec zéro échec. Les six tests dédiés couvrent restauration, refus des chemins dangereux, détection d’un snapshot modifié, préflight O94.5 autonome et audit de références. La compilation `pdflatex -halt-on-error` de `formalisme_O94_5.tex` et `laboratoire_O94_5.tex` a produit deux PDF non vides. L’audit documentaire a relevé zéro référence cassée dans 8 entrées de preuve et 7 batteries ciblées. Reçu : `receipts/O94_5/P7_documentation_restore_final.json`; son journal exact et son SHA-256 sont inscrits dans le reçu. Le statut de phase est maintenu dans `checklist_de_travail_O94_5.json`.


### Incident de construction candidat — bytecode transitoire (résolu)

Le premier candidat a échoué au préflight extrait car le snapshot de développement suivait un fichier `.pyc` généré, alors que les archives livrées excluent ces bytecodes. Le candidat a été conservé comme incident, le filtre du snapshot a été corrigé pour exclure `.pyc` et `__pycache__`, puis le candidat a été reconstruit et extrait à nouveau. Le reçu `receipts/O94_5/P8_candidate_archive_verification.json` confirme le passage du préflight, de la restauration, des tests O94.5 ciblés, de `compileall`, de l’audit documentaire et des deux compilations LaTeX. Le ZIP candidat mesurait 179 481 460 octets, sous le plafond de 220 000 000 octets.


## Addendum P8 — candidat de livraison et reconstruction finale

Le ZIP candidat `Dmodel_AAM_O94_5` est passé par extraction fraîche, CRC, manifeste interne, préflight O94.5, contrôle de restauration, compilation Python, audit documentaire, compilations LaTeX et tests ciblés O94.5. Le reçu du candidat se trouve dans `receipts/O94_5/P8_candidate_archive_verification.json`. La reconstruction finale est relancée depuis cet état clôturé; les hashes finaux des trois ZIP, leur contrôle CRC, les résultats de la suite et les tailles sont externalisés dans `O94_5_delivery_manifest.json`, afin d’éviter le problème circulaire d’un ZIP qui tenterait d’inclure son propre hash.


### Échec de la première régression depuis le ZIP final — état de pause asynchrone

Le premier test complet depuis l’extraction finale s’est terminé avec 427 tests passés et un échec dans `TrainingControlIntegration.test_cancelled_supervised_preparation_does_not_claim_a_completed_fit`. L’inspection montre que le fichier checkpoint (écrit atomiquement) peut être visible quelques instants avant le callback qui met à jour `training_status()` de `PAUSE_REQUESTED` à `PAUSED`. Le test est modifié pour attendre les deux preuves simultanément dans son délai borné. P8 reste rouverte jusqu’au rejeu ciblé, à une nouvelle construction du ZIP et à une suite complète verte depuis extraction fraîche.


### Retest de la synchronisation pause/entraînement — résolu

Le test de pause coopérative attend désormais explicitement le checkpoint durable **et** le statut public `PAUSED`, au lieu de lire ce dernier dans la fenêtre entre l’écriture atomique du fichier et le callback d’état. Le test ciblé a passé trois fois de suite. Le nouveau candidat, extrait dans un répertoire propre, passe le préflight, la vérification de restauration, tous les tests ciblés O94.5, `compileall`, l’audit documentaire et les compilations LaTeX. La campagne complète doit encore être exécutée depuis l’archive définitive lors de l’étape finale.
