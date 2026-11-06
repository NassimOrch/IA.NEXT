# Rapport d'audit technique — NGeGenBrain v3_1

**Révision UTC :** 2026-10-28T10:39:21.226321+00:00  
**Norme :** `prompt_NGeGenBrain_v2.txt`; cartographie dans `v2_prompt_hierarchy_crosswalk.md`.  
**Statut :** logiciel et chargement local testés; étude comparative directe exécutée; reconstruction mécaniste complète non démontrée.

## 1. Résumé exécutif

v3_1 corrige plusieurs défauts observés en v3_0 : chargement local du vrai GGUF SmolLM2 et du vrai `tinny_llm/pytorch_model.bin`, intégration des deux modèles au registre et au chat Web, interprétation correcte des interventions résiduelles, préservation du chemin génératif v3_0 et ajout d'un routeur d'observation multi-vues indépendant.

**Preuves exécutées :** 66/66 tests v3_1; 65/65 tests de régression V1; smoke test API réel réussi pour le produit et les deux modèles sources; UI Playwright sans erreur console et sans overflow horizontal à 1440 px et 390 px. Le BAT est validé statiquement, mais **n'a pas été exécuté physiquement sous Windows** dans l'environnement Linux disponible.

## 2. Sources réelles et provenance

Les hashes exacts sont dans `source_model_study_manifest.json`.

- SmolLM2 GGUF Q8_0 : famille Llama, 30 blocs, hidden size 576, vocabulaire 49 152, contexte déclaré 8 192, environ 134 514 432 paramètres.
- TinyLLM : classe `TinyllmForCausalLM`, poids `pytorch_model.bin` et SentencePiece du zip fourni; 8 couches, hidden size 512, vocabulaire 49 958, contexte déclaré 1 024, 76 868 096 paramètres.
- Étudiant v3_0 : 54 536 paramètres.
- Étudiant v3_1 : 55 568 paramètres, dont le chemin génératif hérité est préservé et un routeur de 1 032 paramètres ajouté.

Les modèles sources ont été chargés et exécutés localement depuis leurs archives réelles; les anciens mocks ne sont pas utilisés comme preuve de cette étude.

## 3. Défauts et corrections identifiés

1. **Mauvaise comparaison précédente :** corrigée par une étude des deux sources réelles et des deux étudiants sur les mêmes textes gelés. La mesure principale inter-tokenizer est le bit par octet UTF-8 (BPB), et non la perplexité native.
2. **Formats locaux insuffisamment supportés :** ajout/raccordement des chargeurs GGUF et TinyLLM `.bin`, puis validation réelle par `/api/models/load` et `/api/chat`.
3. **Interventions causales ambiguës :** le mode `zero` historique continue à annuler l'état de sortie. Les nouveaux modes `zero_update` et `scale_update` retirent ou réduisent la transformation du bloc en conservant la connexion résiduelle. La campagne source a été exécutée avec ces modes.
4. **Fine-tuning conjoint qui dégradait la génération :** conservé comme résultat défavorable; non publié. Le modèle retenu garde le générateur v3_0 gelé et entraîne un routeur séparé.
5. **Risque de prétendre à une validation non faite :** toutes les preuves ont été conservées avec chemins et hashes; les essais incomplets ne sont pas déclarés réussis.

## 4. Préservation des capacités v3_0

`preservation_identity_verification.json` montre **24/24 entrées dont les logits sont bit-à-bit identiques, delta absolu maximal = 0**, et des continuations déterministes identiques pour les prompts inclus dans le contrôle. Cela démontre la non-régression de la génération v3_0 dans v3_1; cela ne démontre pas d'équivalence aux modèles sources.

## 5. Interface, registre et lancement

`web/index.html` fournit navigation latérale, conversation, sélecteur de modèle, registres, expériences, observations, audit, import ZIP/GGUF et chemin local. Playwright a capturé des vues desktop/mobile via endpoints simulés : pas d'erreur JS/console, largeur égale au viewport (1440 et 390 px). À part, le smoke test API réel a chargé les trois modèles.

`ngbrain_NGeGenBrain_v3_1.bat` et `start_NGeGenBrain_v3_1.bat` ont été révisés. **L'exécution Windows réelle reste non vérifiée** faute de `cmd.exe`/Wine; seul le contrôle statique est revendiqué. Le helper Web Python, lui, a réellement été exécuté.

## 6. Limites scientifiques

- 16 textes anglais et 8 chinois pour la modélisation du langage; seuls les 96 premiers octets UTF-8 de chaque document sont scorés. La génération qualitative couvre deux prompts par modèle seulement.
- La langue/distribution de TinyLLM n'est pas alignée sur celle du jeu anglais; l'interprétation par domaine est nécessaire.
- Le routeur atteint 9/32 (28,1 %) sur huit facettes dans le holdout final frais, contre 12,5 % pour un choix uniforme; le holdout compte quatre exemples par classe, et le résultat reste exploratoire.
- Les étudiants (~55,6k paramètres) sont extrêmement plus petits que les sources (~76,9M et ~134,5M); aucune équivalence de capacité ou de circuit n'est démontrée.
- Les interventions mesurent des effets sur une entrée par modèle; il faut les répliquer sur plus de prompts, seeds et distributions.
- Les activations et couches n'ont pas de labels sémantiques certifiés. Les niveaux hiérarchiques 4, 7 et 9 du prompt V2 demeurent partiels.

## 7. Preuves associées

| Contrôle | Résultat | Preuve |
|---|---|---|
| Tests v3_1 | 66/66 | `audit/test_suite_v3_1_release_candidate.log` |
| Régression V1 | 65/65 | `audit/v1_regression_suite_v3_1_release_candidate.log` |
| Comparaison directe | exécutée | `audit/source_vs_student_multiview_release_final2/model_comparison_results.json` |
| Préservation logits | 24/24 égaux | `audit/source_vs_student_multiview_release_final2/preservation_identity_verification.json` |
| API modèles | PASS | `audit/web_api_release_smoke.json` |
| UI Playwright | PASS simulé | `audit/ui_validation_v3_1/ui_validation.json` |
| BAT Windows | statique seulement | pas d'exécution Windows dans l'environnement actuel |

## 8. Verdict

**NGeGenBrain v3_1 est un logiciel expérimental corrigé qui charge réellement les deux sources, les observe et les compare aux modèles étudiants.** Il produit un étudiant chargeable et préserve les capacités de génération v3_0, mais il ne démontre pas une reconstruction mécaniste complète des sources. Le classifieur de facettes est encore trop faible pour parler de découverte fiable de huit mécanismes.
