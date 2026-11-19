# RAPPORT V81-FULLPOP-CONTEXT-ON-PHOTO-001

Date: 2026-11-18 (Africa/Algiers)
Model: eSonde_v8.1 8.1.0-dev
Statut: GENERATION TERMINÉE — QUALITÉ SÉMANTIQUE INSUFFISANTE

## 1. Description

Évaluation libre multi-token du prompt `Explain photosynthesis simply.` avec l'index sémantique contextuel OASST1 TRAIN-only activé. Le moteur est exécuté en mode `first_state` exact pour P/R sur la population complète. La non-réponse est désactivée. Aucun texte cible, aucune réponse modèle et aucun retrieval de réponse brute ne sont fournis au générateur.

## 2. Architecture

- Checkpoint eSonde v6 original conservé en lecture seule (SHA-256 `8526943d1528418fa8bbbf9128b61b5e1acd90a16eeb7cc062e18864b083dff4`).
- E_C (CountSketch historique) et E_O (16 observations nommées) restent séparés; fusion au niveau scalaire des rangs de candidats.
- 1 000 000 Obsiss identifiés par les indices de lignes originaux.
- Transitions bigrammes/trigrammes OASST1 TRAIN-only et agrégats prompt→termes OASST1 TRAIN-only.
- Pool multi-source, vote de 16 observations et score P/R groupé exact par ligne.
- Non-réponse désactivée.
- Aucun composant neuronal déclaré (`neural_components=[]`).

## 3. Pipeline complet

1. Préflight: checklists, chemin et savepoint relus; manifeste et SHA du checkpoint vérifiés.
2. Chargement des profils linguistiques et des agrégats OASST1.
3. Sélection de la route de langue de dialogue `en` à partir du prompt; route générique séparée a indiqué `INSUFFICIENT_LANGUAGE_EVIDENCE`.
4. Construction du pool de propositions (jusqu'à 48 candidats selon le préfixe).
5. Activation P `first_state` sur 1 000 000 Obsiss.
6. Calcul R/P groupé sur 1 000 000 Obsiss pour chaque candidat; 12 décisions complètes.
7. Vote collectif, sélection token et mise à jour du préfixe; non-réponse off.
8. Écriture du résultat JSON et des traces d'étapes.

## 4. Commande d'exécution

```bash
cd Dmodel_eSonde_v8_1
PYTHONPATH=src python -m esonde_v8.cli_v81 chat \
  --prompt 'Explain photosynthesis simply.' \
  --max-tokens 12 --beam-width 1 --candidate-limit 48 \
  --p-activation-mode first_state --no-trace \
  --output-dir <run>/runtime --json-out <run>/result.json
```

Paramètres effectivement utilisés: population 1 000 000; candidats maximum 48; faisceau 1; 12 tokens; `allow_non_response=false`; `first_state`.

## 5. Résultats

Prompt: `Explain photosynthesis simply.`

Réponse exacte générée:

> Photosynthesis is one example is a simple example of the game is

Tokens choisis: `photosynthesis → is → one → example → is → a → simple → example → of → the → game → is`.

- Statut CLI: `GENERATED`; code de sortie: 0.
- Étapes achevées: 12/12.
- Population par décision: 1 000 000 Obsiss.
- Non-réponse: désactivée et non déclenchée.
- La réponse ne décrit pas correctement la photosynthèse et ne répond pas de façon intelligible au prompt.
- Le contexte sémantique a effectivement proposé certains termes thématiques (par exemple `algae` est visible dans le rang diagnostic à l'étape 4 avec score d'association contextuelle positif), mais les transitions globales n-grammes ont dominé leur classement.
- La stabilité inter-partitions des votes est une mesure de stabilité du vote, pas une preuve de factualité ou de cohérence.

## 6. Interprétation des résultats

Le moteur exécute le pipeline complet et exploite la population entière. Le contexte prompt→sémantique entre dans les propositions et le canal `prompt_association`, mais la continuation sélectionnée dérive vers des motifs lexicaux génériques: `Photosynthesis is one example is a simple example of the game is`. Cela établit une faiblesse opérationnelle du modèle de transition: le modèle conditionne le premier token sur le prompt plus fortement que les tokens suivants. La simple association prompt→termes, fusionnée en rang dans un canal, n'assure pas la continuité de l'intention.

La génération est terminée sans incident technique; son résultat est un échec qualitatif pour l'objectif de cohérence, et non un timeout.

## 7. Conséquences

### Théoriques

Une distribution de continuation `P(next | prefix, language)` ne suffit pas à représenter `P(next | prompt, prefix, language)`. L'association sémantique marginale `P(term | prompt)` ne fixe ni l'ordre ni la fonction du terme dans la phrase. Il faut tester des transitions agrégées conditionnées conjointement par un indice du prompt et le préfixe de réponse.

### Conceptuelles

Le maintien du sujet doit être une propriété mesurable de chaque décision (et pas seulement de l'ouverture). Les 16 observations doivent arbitrer entre pertinence référentielle et continuité locale; les dimensions ne doivent pas être modifiées pour masquer la défaillance. E_C et E_O restent non-identifiés.

### Opérationnelles

Tester une table statistique `P(next_token | language, prompt_anchor, response_prefix)` construite uniquement depuis liens parent-user/enfant-assistant du TRAIN OASST1, avec compteurs agrégés uniquement; aucune phrase, ID ou paire brute persistée. Comparer OFF/ON en gardant la même population, le même pool et les mêmes prompts.

## 8. Conclusions

Le pipeline full-population multi-token fonctionne techniquement. La réponse produite est incohérente avec la demande. L'ajout sémantique actuel n'a pas atteint l'objectif conversationnel. Aucun résultat de généralisation ou de supériorité n'est revendiqué.

## 9. Statut du modèle

`PROTOTYPE ACTIF — GÉNÉRATION FULL-POPULATION VALIDÉE TECHNIQUEMENT; COHÉRENCE NON ACQUISE; CONTINUATION PROMPT-CONDITIONED À EXPLORER.`

## 10. Artefacts

- Résultat: `experiments/v81_photo_context_fullpop_20261118/result.json`
- Console: `experiments/v81_photo_context_fullpop_20261118/console.json`
- Traces: `experiments/v81_photo_context_fullpop_20261118/runtime/diagnostics/v81_generation_stage_events.jsonl`
- R batch trace: `experiments/v81_photo_context_fullpop_20261118/runtime/diagnostics/v81_batched_R_pair_scoring.jsonl`
- Test suite après l'intégration: `logs/v81_full_test_suite_after_context_proposal_v1.log` (112 passed)
