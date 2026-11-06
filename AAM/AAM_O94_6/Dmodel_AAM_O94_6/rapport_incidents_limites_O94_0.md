# Rapport d'incidents et de limites — AAM O94_0

**Date d'état :** 18 octobre 2026.  
**Racine de travail :** `Dmodel_AAM_O94_0/`.  
**Règle d'interprétation :** un incident d'outil ou d'environnement n'est pas automatiquement attribué au modèle ; un retest réussi résout un incident sans effacer son premier reçu.

## 1. Description

Ce rapport rassemble les écarts de test et d'outillage pertinents pour R1–R3 ainsi que les limites des preuves disponibles. Les registres détaillés `checklist_erreurs_no_model.json` et `checklist_erreurs_model.json` restent la source de suivi des incidents individuels (252 entrées environnement/outillage et 138 entrées modèle à la dernière lecture avant la clôture documentaire P6). Les nombres évoluent lorsqu'un nouvel incident est créé ; les fichiers eux-mêmes restent la référence actuelle.

## 2. Architecture concernée

Les principaux composants sont `aam_o93/runtime.py` (orchestration récupération/génération), `aam_o93/semantic_rag.py` (espaces sémantiques et index RAG), `aam_o93/resolution_tree.py` (segmentation et classement d'enregistrements), `aam_o93/observer.py` (ingestion, y compris TSV), `aam_o93/memory_resolution.py` (index hiérarchique de mémoire), `aam_o93/memory.py` (journal source), et `aam_o93/ui.py` (formateur de réponse et vues détails).

## 3. Pipeline complet de gestion des erreurs

1. Lire `chemins_O94_0.json` et la checklist de phase, puis les deux registres d'erreurs.
2. Exécuter le preflight et le test par runner de phase.
3. Conserver la commande, les sorties, code retour, durée et SHA-256 de la source de test.
4. Si le run échoue, identifier si le test a réellement atteint le code AAM ou s'il s'est arrêté auparavant (import, fixture, Tk display, timeout, verrou de phase).
5. Corriger le contrat ou le code sans affaiblir l'exigence demandée, puis exécuter un retest isolé.
6. Marquer l'incident résolu uniquement si le retest lié passe ; conserver le premier reçu.

## 4. Commandes de vérification

Depuis `Dmodel_AAM_O94_0` :

```bash
python scripts/o940_phase_test_runner.py --help
python -m pytest -q tests/test_o940_rag_resolution.py
python -m pytest -q tests/test_o931_chat_pipeline.py
python -m pytest -q tests/test_o940_memory_resolution.py
python -m pytest -q tests/test_o940_ui_resolution_details.py
python scripts/o940_snapshot.py
```

Les exécutions normatives doivent passer par le runner de phase après consultation des quatre documents de contrôle. Les commandes directes de pytest ci-dessus sont des exemples de retest ciblé.

## 5. Incidents constatés, interprétation et résolution

| Incident / famille | Observation initiale | Traitement / retest | Statut à la date du rapport |
|---|---|---|---|
| Segmentation TSV du SMS corpus | Le parseur CSV strict rejetait des messages TSV contenant des guillemets ordinaires et produisait zéro enregistrement dans l'échantillon. | TSV traité en lignes physiques ; le premier tab sépare étiquette et texte libre. Retest sur 300 lignes : chaque ligne conservée exactement une fois et index construit. | Résolu avec retest ; reçu P2 référencé dans le registre. |
| Réponse RAG mêlant enregistrements voisins | Les chunks JSONL pouvaient regrouper plusieurs objets et le fallback réimprimait le chunk. | Les lignes JSONL restent atomiques, classement sur la demande et fallback sur le champ réponse. Tests RAG/chat/longue réponse et corpus borné. | Résolu dans le périmètre testé. |
| Réponse visible contenant diagnostics | Statuts, scores, empreintes et extraits étaient concaténés à la conversation. | `format_chat_result` rend seulement le texte de réponse ; panneau Détails séparé. Tests UI sous Xvfb. | Résolu dans le périmètre UI testé. |
| RAG/générateur, index vide | `NOT_RUN` et absence d'index/passage n'étaient pas suffisamment distingués. | Recherche exécutée avant génération en mode normal ; états `NO_INDEX`/`NO_MATCH` distincts, question/preuves séparées. | Résolu par les reçus P3. |
| Délégation à un autre AAM | Le contrat initial repassait des preuves dans la question textuelle, puis relançait une résolution sans preuves distinctes. | Adaptateur explicite et champs séparés, prévention de délégation récursive, fallback vers preuve RAG déjà sélectionnée seulement si sortie inutilisable. | Test local/adaptateur PASS ; serveur LLM/AAM externe vivant non vérifié. |
| Index mémoire global | Lecture trop large et diagnostics de graphe ambigus. | Index maître/micro, lecture progressive et vérification de feuilles, causalité explicite séparée du hash d'intégrité. | Tests P4 PASS dans le périmètre local. |
| Assertions historiques obsolètes | Tests exigeaient ancien texte de réponse ou anciens contrats UI. | Assertions adaptées aux nouveaux contrats R1 et retests réussis ; premiers reçus gardés. | Résolu par retest. |
| Tkinter sans écran | Certains modules échouaient avant le code applicatif avec `couldn't connect to display ":0"`. | Exécution avec Xvfb et retests individuels. | Résolu pour les tests couverts ; ne prouve pas le comportement natif Windows. |
| Timeout de lot / tuyaux hérités | Un lot externe dépassait son plafond et ne rendait pas de reçu complet. | Modules relancés isolément avec sorties brutes par module ; certains runners durcis pour arrêter le groupe de processus. | Incidents de banc clos uniquement lorsque le retest individuel avait un reçu. |
| Scripts de snapshot / manifeste | Imports depuis `scripts/`, double suffixe `/current`, schémas `bytes`/`size_bytes`, fichiers de test `MagicMock` dans une sauvegarde antérieure. | Chemins et schémas corrigés ; exclusions de cache/doubles de test dans la politique du snapshot ; vérification via manifeste. | Historique conservé ; nouveau snapshot à vérifier avant livraison. |
| Validation du corpus Screenplay | Résultats calculés sur un corpus réduit. | 10 questions évaluées sur 32 enregistrements, correspondances exactes post-hoc 10/10 pour cet échantillon. | Résultat borné ; aucune extrapolation à des corpus généraux. |

## 6. Résultats et interprétation

La matrice P5 `logs/O94_0/P5_matrix_consolidated_001.json` rapporte 54 modules sur 54 avec reçus PASS, 316 cas pytest réussis et 21 sous-tests réussis, sans échec/skip dans cet agrégat. La clôture `logs/O94_0/P5_closure_001.json` contient les hashes des entrées corpus et les limites annoncées. Des tests ultérieurs ou des revalidations locales doivent créer des reçus ultérieurs ; l'agrégat ne s'applique pas automatiquement à des changements effectués après la matrice.

## 7. Limites

- L'évaluation SMS interroge une sélection de 300 lignes ; le ZIP source contient 5 574 messages, mais chaque message n'a pas fait l'objet d'une requête indépendante.
- L'évaluation Screenplay couvre 10 demandes sur 32 enregistrements, avec mesure post-hoc. Elle ne démontre ni généralisation universelle ni vérité intrinsèque.
- Un adaptateur mocké ou local ne démontre pas qu'un endpoint externe est vivant, accessible ou conforme.
- Les tests UI sous Xvfb ne constituent pas des essais sur Windows natif ni sur une caméra, un microphone ou un capteur physique.
- Des hashes concordants établissent l'identité des octets attendus, pas l'exactitude factuelle du corpus ou de la réponse.
- `PASS_BOUNDED` est un résultat borné du protocole et non une garantie sur toutes requêtes ou tous environnements.

## 8. Conséquences théoriques, conceptuelles et opérationnelles

**Théoriques :** un index maître/micro rend la recherche progressive ; les empreintes sont liées à des observations et à des versions, pas assimilées à la vérité.  
**Conceptuelles :** récupération, génération, mémoire, présentation et audit sont des responsabilités séparées.  
**Opérationnelles :** chaque clôture repose sur des reçus, une sauvegarde synchronisée et des sommes de contrôle ; toute modification postérieure exige de régénérer les preuves de livraison.

## 9. Conclusion et statut du modèle

Les preuves actuelles justifient le statut **implémentation locale testée dans un périmètre borné**. Les incidents résolus restent auditables ; les limites externes restent ouvertes jusqu'à des tests réels. P6 ne doit être clôturée qu'après validation structurelle des documents, de la couverture R1–R3 et du snapshot actualisé. P7 ne doit être clôturée qu'après test CRC, extraction indépendante et vérification des hashes des trois archives définitives.


## 10. Mise à jour de clôture P6

La phase P6 a été clôturée le 18 octobre 2026 par le reçu `logs/O94_0/P6_closure_001.json` après une validation P6 fraîche. Le registre couvre 16 sous-exigences R1–R3 reliées au code, aux tests et aux reçus. Les deux incidents des scripts de clôture (mauvais champ de hash puis reçu devenu périmé) sont résolus par retest et restent visibles dans `checklist_erreurs_no_model.json`. P7 est maintenant active ; elle ne sera considérée terminée qu'après construction des trois ZIP définitifs, `testzip`, extraction indépendante et concordance de leur manifeste SHA-256 externe.
