# Rapport de reprise O93_1 — Phase P3 : régression et intégration

**Version examinée :** `0.93.1`  
**État du rapport :** intermédiaire, essai du corpus complet en cours après optimisation exacte  
**Phase courante :** P3 — Non-régression et intégration  
**Statut global :** `IN_PROGRESS_P3_SCALABILITY_DIAGNOSTIC_AND_EXACT_OPTIMIZATION`  
**Date d'exécution :** 14 octobre 2026 (heure locale du workspace)

## 1. Description

Cette reprise vérifie que le chat utilise réellement les preuves du RAG et un modèle entraîné, que les réponses exposées à l'utilisateur correspondent au résultat réellement sélectionné, que l'autonomie démarre avec AAM et que l'interface conserve un chemin d'usage compréhensible. Le rapport sépare les essais unitaires/intégration, l'acceptation sur 120 SMS réels et l'essai distinct sur les 5 574 lignes du corpus.

Le présent document ne déclare pas P3 clôturée : un essai du corpus complet est supervisé et n'a pas encore rendu son reçu final au moment de cette rédaction. Tout résultat sans reçu de sortie ne compte pas comme réussite.

## 2. Architecture examinée

Le chemin de réponse évalué est :

1. acquisition et intégrité de la source ;
2. observation/chunking conservant les frontières de lignes ;
3. construction du RAG sémantique multi-espace et récupération de preuves ;
4. sélection explicite du backend/capsule entraînée ;
5. création du prompt à partir de la requête et des passages récupérés ;
6. génération réelle et enregistrement des hashes capsule/prompt/contexte ;
7. contrôle structurel de la candidate générée ;
8. sélection soit de la candidate, soit d'un fallback extractif sourcé ;
9. affichage lisible dans le chat, avec données techniques accessibles séparément ;
10. journalisation causale et fermeture propre du runtime.

Le cycle autonome est indépendant du bouton de fermeture : il démarre par défaut avec le runtime, peut être arrêté puis redémarré manuellement sans fermer AAM, et la fermeture complète arrête la boucle, tente un checkpoint et libère le verrou.

## 3. Pipeline complet des essais

### 3.1 Régressions ciblées

Les groupes suivants ont terminé sur le code courant après les corrections du chat, de l'UI et du cycle de vie :

- Chat/RAG/UI/observateur : **93 tests et 7 sous-tests** ;
- autonomie/mémoire/UI : **63 tests** ;
- dataset/entraînement/routeur/sécurité : **61 tests et 14 sous-tests** ;
- compatibilité de préflight/portes et intégrité préenregistrée : **23 tests** ;
- cohérence d'identité de version : **1 test** ;
- interface Tk sous Xvfb : **2 tests** ;
- test contractuel du pipeline de réponse : **10 tests**.

Ces groupes se recouvrent partiellement : leurs nombres ne doivent pas être additionnés pour annoncer un total global sans déduplication du registre de tests. Les reçus individuels sont dans `logs/O931/`.

### 3.2 Acceptation sur 120 SMS réels

Commande (depuis la racine du paquet) :

```bash
AAM_O931_REPORT_PATH=logs/O931/real_corpus_sms_chat_acceptance_bounded_final_record_discrimination.json \
  timeout -k 2s 55s env PYTHONPATH=. TERM=xterm \
  python -u scripts/o931_real_corpus_chat_acceptance_bounded.py
```

L'essai a utilisé des lignes réelles du dataset embarqué. Le SMS cible sur le prix « £900 » a été exclu des données de l'entraînement de la capsule compacte, mais inclus dans la source RAG observée. Les reçus montrent que la recherche récupère le SMS complet, que le prompt reçu par la capsule contient cette preuve et que la capsule réellement issue de l'entraînement est invoquée. La candidate générée est cependant de qualité structurelle insuffisante (marqueurs `<unk>` et manque d'ancrage) ; elle est rejetée, et le chat sert un seul enregistrement complet avec citation comme fallback extractif.

Résultat : `PASS_BOUNDED`, sortie du runner `0`, fermeture runtime `CLOSED`, hashes de l'archive source et de la source observée inchangés. Cette expérience vérifie le routage RAG/capsule, les preuves et le comportement du fallback ; elle **ne prouve pas** que la capsule compacte sait rédiger une réponse correcte sur toute question.

### 3.3 Essai du corpus complet

Un essai distinct porte sur les **5 574 lignes** du corpus embarqué, avec ingestion sémantique du corpus complet et entraînement sur la partition prescrite par le script. Il s'exécute sous un superviseur avec plafond de 420 secondes, fichier de sortie et code de sortie persistants. À l'heure de rédaction, il n'a pas encore produit de rapport final ; il reste `RUNNING / NOT_VALIDATED`. Aucun succès n'est inféré de son processus encore actif.

Une inspection statique du calcul d'agrégation a localisé un candidat sérieux au coût élevé : les vecteurs contextuels creux sont comparés exhaustivement token-par-token aux tokens invariants, y compris quand deux vecteurs n'ont aucun attribut commun. Le test courant conserve une valeur de diagnostic pour la version non optimisée. Toute optimisation éventuelle sera testée comme une nouvelle version de code, avec comparaison exacte des poids/distance sur des fixtures et vérification des hashes.

## 4. Commandes de vérification

Préflight obligatoire avant les essais :

```bash
python scripts/o931_preflight.py --label <label-de-l-essai>
```

Régressions exécutées (les reçus précis donnent les listes exactes) :

```bash
xvfb-run -a env PYTHONPATH=. TERM=xterm python -m pytest -q tests/test_o931_chat_pipeline.py tests/test_o931_ui_smoke.py
xvfb-run -a env PYTHONPATH=. TERM=xterm python -m pytest -q tests/test_p4_ui_integration.py tests/test_p5_autonomy_o930.py tests/test_p5_knowledge.py tests/test_p6_autonomy.py tests/test_p6_competence_profiles.py tests/test_p6_memory_causal_graph_view.py tests/test_p6_memory_event_inspection.py tests/test_p6_probe_management.py tests/test_p6_probe_ui_contracts.py tests/test_p6_source_inspector.py tests/test_p6_ui_initial_catalog_sequence.py tests/test_p6_ui_integration.py
xvfb-run -a env PYTHONPATH=. TERM=xterm python -m pytest -q tests/test_p7_dataset_service.py tests/test_p7_integrated.py tests/test_p7_training_control.py tests/test_p8_action_router.py tests/test_p8_integration.py tests/test_p8_security.py
```

## 5. Résultats et interprétation

- Le premier défaut utilisateur est reproduit et corrigé au niveau du routeur : le RAG seul ne s'arrête plus à renvoyer un paquet d'extraits sous l'apparence d'une génération.
- La capsule entraînée peut être invoquée en aval du retrieval. Son appel est démontré par l'identifiant/hash de capsule, les hashes de prompt/contexte et les événements d'audit.
- Une candidate de génération inutilisable n'est pas montrée comme si elle était une réponse validée ; elle est conservée en trace technique et un fallback cité est sélectionné.
- Le modèle compact de l'essai SMS a effectivement produit une candidate mais celle-ci contenait des marqueurs inconnus. C'est une observation expérimentale, pas une prédiction sur toutes les compétences futures d'AAM.
- Deux anomalies responsive (troncature horizontale et panneau d'évaluation coupé verticalement), puis un blocage d'une boîte modale en état UI occupé, ont été reproduits, corrigés et retestés sous Xvfb.
- Le runtime autonome démarre par défaut. Les tests couvrent pulsation, traitement d'une requête, reprise de l'autonomie, arrêt manuel sans fermeture, redémarrage et fermeture complète.
- L'essai du corpus complet reste non validé tant qu'un reçu de fin et un code de sortie ne sont pas disponibles.

## 6. Conséquences

### Théoriques

La séparation entre observation/retrieval, invocation d'un générateur, contrôle de qualité et choix de la réponse empêche de confondre preuve trouvée, appel du modèle et texte effectivement servi. Les poids sémantiques et la génération restent des mécanismes à mesurer sur des corpus et tâches indépendants ; l'usage observé ne constitue pas, en soi, une preuve de généralisation.

### Conceptuelles

L'autonomie est un cycle de vie du runtime, non une préférence décorative de l'UI. Son arrêt manuel est distinct de la fermeture d'AAM. Le fallback n'est pas présenté comme une génération du modèle.

### Opérationnelles

L'utilisateur peut vérifier l'origine d'une réponse depuis « Détails techniques » : route, citations, capsule choisie, hashes prompt/contexte, motif du garde-fou et origine réelle du texte présenté. Les preuves de test doivent suivre les hashes du code livré.

## 7. Conclusion et statut du modèle

**Statut P3 actuel : EN COURS.** Les régressions locales ciblées et l'acceptation SMS bornée réussissent dans leurs portées déclarées. Le test sur le corpus intégral est toujours en exécution/non validé et l'algorithme sémantique présente un point de coût à optimiser si la limite de temps est atteinte. Aucune phase suivante ne doit être clôturée sur la base de cet essai incomplet.

**Limites externes :** cette phase n'atteste pas de l'acceptation native multi-OS, du matériel réel, des caméras/capteurs physiques ou de fournisseurs Internet/MCP/API réels ; ces validations demeurent distinctes.
