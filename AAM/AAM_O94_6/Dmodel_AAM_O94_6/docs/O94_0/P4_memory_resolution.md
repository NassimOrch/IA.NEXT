# Rapport P4 — Mémoire hiérarchique, raffinement contextuel et interface « Détails »

## 1. Description

P4 traite la partie mémoire de R3 qui n’était pas couverte par le seul arbre micro-RAG documentaire. Le journal `memory/audit_events.jsonl` reste la source de vérité immuable/par ajout; la nouvelle arborescence ne remplace ni ne réécrit les événements du journal. Elle ajoute un index maître et des micro-nœuds destinés au routage, puis ne relit les charges utiles brutes que pour les événements retenus et au niveau demandé.

## 2. Architecture

- `aam_o93/memory_resolution.py` : construction incrémentale de l’index mémoire, nœuds maître → micro-RAG → événements sélectionnés, recherche par empreintes lexicales hachées, vérification d’intégrité et raffinement par contexte.
- `aam_o93/memory.py` : journal d’audit append-only, chaînage `prev_hash`, SHA-256 d’événement, verrouillage et écritures atomiques conservés comme source de vérité.
- `aam_o93/runtime.py::resolve_memory` : point d’entrée runtime, appel du garde-fou de préflight, hashage des paramètres d’interrogation dans le diagnostic et enregistrement d’un reçu d’activité sans persister le texte de requête ou les charges utiles dans ce diagnostic.
- `aam_o93/ui.py` : panneau « Recherche mémoire progressive — arbre de résolution », requête + contexte + profondeur 1–4, résultat structuré et compteurs consultables.
- `tests/test_o940_memory_resolution.py`, `tests/test_o940_ui_resolution_details.py` : tests des budgets, du contexte, des liens causaux, de la profondeur temporelle, de l’intégrité et du câblage UI.

## 3. Pipeline complet

1. Au premier usage, le constructeur lit le journal, valide les liens de chaîne, les numéros de séquence et les hash d’événement, puis enregistre des offsets byte-addressables. Il ne copie pas les charges utiles en clair dans l’index.
2. Pour chaque événement, il crée un résumé (séquence, type, temps, hash d’événement, clés de payload, parents causaux, offset/longueur/hash de ligne). Le contenu descriptif est transformé en tokens puis en empreintes SHA-256 préfixées; les mots originaux ne sont pas stockés dans les nœuds maître/micro.
3. Les résumés sont regroupés par lots de 16 dans des micro-RAG. Chaque micro-RAG possède un hash de contenu et un hash externe vérifiés avant utilisation. Les nœuds maître regroupent au plus huit micro-RAG et réunissent uniquement leurs empreintes/ranges.
4. Une recherche hache la question et, si fourni, le contexte. Le score exige un recouvrement sur la question ; le contexte sert à départager/raffiner des branches compatibles. Le contexte ne peut pas produire seul une branche qui n’a aucune compatibilité avec la question.
5. Au niveau 1, la réponse contient uniquement des résumés et aucun payload brut. Au niveau 2, les plages brutes des événements retenus sont lues et leur hash de ligne et hash d’événement revérifiés. Au niveau 3, les parents causaux explicitement déclarés sont résolus. Au niveau 4, des voisins temporels bornés sont ajoutés. `prev_hash` reste une preuve d’intégrité et n’est jamais interprété comme un lien causal.
6. Après le premier index, seuls les octets ajoutés depuis le dernier offset sont analysés lors d’un rafraîchissement normal. L’index est scellé par son propre hash; les fichiers micro sont vérifiés à la demande. Une corruption dans un chemin sélectionné bloque la lecture.
7. L’interface affiche la profondeur et le contexte utilisés ainsi que les compteurs maître/micro/payload. Le texte de réponse du chat demeure séparé des sources et diagnostics, lesquels restent consultables via « Détails ».

## 4. Commandes d’exécution

Depuis la racine `Dmodel_AAM_O94_0` :

```bash
python scripts/o940_run_tests.py --phase P4 --name memory_resolution_005 tests/test_o940_memory_resolution.py
python scripts/o940_run_tests.py --phase P4 --name memory_resolution_ui_003 --xvfb tests/test_o940_ui_resolution_details.py
python scripts/o940_run_tests.py --phase P4 --name rag_chat_nonregression_001 tests/test_o940_rag_resolution.py tests/test_o931_chat_pipeline.py
python scripts/o940_run_tests.py --phase P4 --name causal_reward_memory_nonregression_001 tests/test_o94_trace_resolution_reward.py
python scripts/o940_run_tests.py --phase P4 --name continuous_ui_nonregression_001 --xvfb tests/test_o94_continuous_resolution_ui.py
```

## 5. Résultats

| Reçu | Résultat |
|---|---:|
| `logs/O94_0/P4_memory_resolution_005.json` | 11 tests réussis |
| `logs/O94_0/P4_memory_resolution_ui_003.json` | 2 tests réussis sous Xvfb |
| `logs/O94_0/P4_rag_chat_nonregression_001.json` | 24 tests réussis |
| `logs/O94_0/P4_causal_reward_memory_nonregression_001.json` | 3 tests réussis |
| `logs/O94_0/P4_continuous_ui_nonregression_001.json` | 1 test réussi sous Xvfb |

Le test mémoire comporte notamment : réponse de niveau 1 sans payload, lecture de l’unique payload sélectionné en niveau 2, résolution d’un parent causal au-delà d’une frontière de micro-RAG, ajout de voisins temporels au niveau 4, usage du contexte pour affiner deux candidats partageant les mêmes indices de question, route maître→micro sur un journal de 160 événements et sélection d’une seule micro-branche, rafraîchissement incrémental, corruption d’un micro, corruption d’une plage événementielle et altération de l’index scellé.

## 6. Interprétation des résultats

Les reçus confirment que le chemin mémoire hiérarchique est implémenté et testé localement. Les compteurs mesurent les nœuds maîtres/micro examinés et le nombre de payloads effectivement chargés. Le test de 160 événements a retenu le bon événement, sélectionné une branche maître sur deux et chargé un seul micro-RAG. Les tests de corruption ont été refusés avant de retourner un payload altéré. L’index contient des empreintes de tokens et des résumés, non le texte de requête/contenu arbitraire en clair; le journal original conserve naturellement les payloads qui lui ont été confiés.

Les incidents de test précédents ont été conservés dans `checklist_erreurs_no_model.json`. Les deux échecs d’assertion étaient des hypothèses trop larges ou trop strictes du banc, et non des preuves d’échec du runtime; leurs corrections sont reliées aux reçus de retest. Le timeout historique d’un lot combiné UI/mémoire est traité par des exécutions séparées avec reçus autonomes plutôt que requalifié en réussite du lot combiné.

## 7. Conséquences

### Théoriques

La mémoire dispose désormais d’une filtration/résolution progressive : le premier niveau expose des résumés, les niveaux plus fins ouvrent les charges utiles retenues et leurs relations causales/temporaires. Le contexte sert de critère de raffinement après compatibilité de la question. Cela reprend l’idée d’un arbre de résolutions sans affirmer que les empreintes lexicales donnent toujours la bonne interprétation sémantique.

### Conceptuelles

La chaîne d’intégrité (`prev_hash`) et la causalité métier (`parent_event_hashes` / `cause_event_hashes`) restent disjointes. La provenance et les hashes prouvent l’origine/intégrité des données, pas leur vérité factuelle.

### Opérationnelles

La première construction lit et indexe les métadonnées de tout le journal; ensuite, les ajouts sont indexés depuis le dernier offset. Les payloads bruts ne sont lus qu’après sélection, et la profondeur plafonne le nombre de relations/événements ouverts. Une modification d’un ancien événement non sélectionné n’est pas détectée par une requête qui ne le lit pas; l’audit complet (`verify_audit`) demeure le contrôle à exécuter pour un audit global.

## 8. Conclusion et statut du modèle

**P4 : COMPLETE_EVIDENCED_WITH_SCOPE_LIMITS.** Les fonctions locales de résolution progressive mémoire, raffinement contextuel, lecture hiérarchique et panneau UI sont implémentées et passent les suites indiquées. Cela ne démontre pas une exactitude sémantique universelle, une vérité factuelle automatique, un comportement de Windows matériel réel ni la validation d’un serveur LLM externe. Ces limites restent visibles et ne sont pas transformées en affirmations de succès ou d’échec général de AAM.
