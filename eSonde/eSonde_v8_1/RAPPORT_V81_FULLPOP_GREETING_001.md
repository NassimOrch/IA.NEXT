# Rapport d'expérience V81-FULLPOP-GREETING-001

Date : 2026-11-18 (heure locale Africa/Algiers)  
Statut : génération complétée, qualité conversationnelle insuffisante  
Checkpoint : `8526943d1528418fa8bbbf9128b61b5e1acd90a16eeb7cc062e18864b083dff4`

## 1. Description

Prompt évalué sans réponse cible injectée : « Bonjour, comment vas-tu ? ».  
Runtime : eSonde v8.1, non-réponse désactivée, mode P `first_state`, beam width 1, limite de propositions 8, population Obsiss 1,000,000.

## 2. Architecture et pipeline complet

Le runtime détecte la langue courante (`fr`), initialise P sur toute la population, construit le pool de propositions, rafraîchit P à chaque préfixe, calcule les états R de toutes les propositions avec l'opérateur R/P groupé, agrège les votes Obsiss, sélectionne le prochain token et répète jusqu'à la terminaison.

Le calcul groupé R/P traite exactement 1,000,000 lignes. Il conserve l'identité Obsiss et les 16 observations nommées existantes. Le premier état P n'est pas présenté comme un point fixe. Le verrou de phase historique n'est pas utilisé par ce runtime.

## 3. Commande d'exécution

```bash
cd Dmodel_eSonde_v8_1
PYTHONPATH=src python RUN_CLI_V81.py chat \
  --prompt 'Bonjour, comment vas-tu ?' \
  --max-tokens 20 --beam-width 1 --candidate-limit 8 \
  --p-activation-mode first_state --no-trace \
  --workspace /mnt/data/esonde_audit/v8_1_work \
  --output-dir <experiment>/runtime --json-out <experiment>/result.json
```

Paramètre `--allow-no-response` omis : la non-réponse était désactivée.

## 4. Résultat

Réponse générée :

> Bonjour, c'est un élément dans l'eau, des styles de la vie.

Statut CLI enregistré : `GENERATED`.  
Tokens sélectionnés : 18.  
Obsiss disponibles/utilisés : 1,000,000/1,000,000.  
Largeur de faisceau : 1.  
Non-réponse autorisée/déclenchée : False/False.

## 5. Interprétation

La première sélection « bonjour » répond au type de prompt, mais la continuation complète « Bonjour, c'est un élément dans l'eau, des styles de la vie. » dérive vers un contenu descriptif sans rapport avec une salutation. La génération est techniquement complète et chaque étape a traité la population complète ; la qualité de réponse échoue néanmoins au critère sémantique du prompt.

L'analyse de `step_evidence` montre que `prompt_response_start` n'est disponible qu'au premier token. Aux étapes suivantes, la sélection s'appuie surtout sur les transitions de réponse générales (bigrammes/trigrammes) : `context_response` et `prompt_response_start` restent à zéro dans la majorité des étapes après l'ouverture. Le problème opérationnel principal est donc le maintien d'une condition prompt→continuation à chaque position.

Le résultat de convergence des classements Obsiss décrit la stabilité du classement sous partitions ; il ne démontre ni convergence de la génération vers un contenu correct, ni vérité ni pertinence.

## 6. Conséquences

### Théoriques

Le modèle de transition de langue seul ne suffit pas à maintenir l'intention du dialogue. Le signal du prompt doit conditionner les transitions suivantes, pas uniquement le choix du premier token.

### Conceptuelles

L'observation existante `prompt_association` est le canal naturel où mesurer un signal prompt-conditioned continuation. Aucun 17e canal n'est requis. Il faut distinguer association lexicale de sujet et association prompt→réponse ; les marqueurs de salutation exclus des ancres thématiques doivent rester exploitables par un index de réponse conditionné au prompt.

### Opérationnelles

Construire une table de fréquences agrégées TRAIN-only reliant (langue, ancre de prompt, préfixe de réponse observé) au token suivant ; aucun texte, identifiant de message, arbre, paire ni gabarit de réponse ne sera stocké. Comparer les scores conditionnés avec les transitions générales et mesurer une ablation OFF/ON.

## 7. Conclusion

Génération complète sur un million d'Obsiss : **oui**. Réponse cohérente à ce prompt : **non**.  
Statut du modèle : prototype de chat v8.1 opérationnel au niveau de l'exécution, qualité de génération encore insuffisante ; incident de dérive contextuelle ouvert.

## 8. Artefacts

- Résultat : `../experiments/v81_fullmultitoken_greeting_20261118/result.json`
- Événements : `../experiments/v81_fullmultitoken_greeting_20261118/runtime/diagnostics/v81_generation_stage_events.jsonl`
- SHA-256 résultat : `1a1a58b0388f1895b5442c6c69250f570cdcb3dd5748430a321614f73f5c8447`
- SHA-256 événements : `efb78fb459ceea4c617fc825962ab9154cd5b251a35da60a0c8b7309cc9d37a1`
