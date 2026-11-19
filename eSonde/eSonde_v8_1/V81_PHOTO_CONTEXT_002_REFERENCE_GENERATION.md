# V81-PHOTO-CONTEXT-002 — génération libre de référence

## Description
Prompt : `Explain photosynthesis simply.`. Génération libre sur l'intégralité des 1 000 000 Obsiss, mode P `first_state`, faisceau 1, limite 48 candidats, 12 tokens, non-réponse désactivée.

## Architecture et pipeline
Le runtime utilise les 16 observations nommées dans E_O, le P/R CountSketch d'origine E_C, les transitions TRAIN OASST1, l'index sémantique contextuel et le modèle de continuations conditionnelles prompt+préfixe. Le checkpoint original est en lecture seule.

## Commande d'exécution
```bash
PYTHONPATH=src python -m esonde_v8.cli_v81 chat \
  --prompt "Explain photosynthesis simply." --max-tokens 12 \
  --beam-width 1 --candidate-limit 48 --p-activation-mode first_state \
  --workspace /mnt/data/esonde_audit/v8_1_work \
  --output-dir /mnt/data/esonde_audit/v8_1_work/suivi_model_eSonde_v8_1/experiments/v81_photo_confidence_repetition_fullpop_20261118/runtime \
  --json-out /mnt/data/esonde_audit/v8_1_work/suivi_model_eSonde_v8_1/experiments/v81_photo_confidence_repetition_fullpop_20261118/result.json
```

## Résultats
**Sortie :** `Photosynthesis is one of many, but all the algae oxygen is`

- Statut : `GENERATED` ; tokens : 12 ; candidats : 48 ; Obsiss : 1000000.
- Non-réponse : autorisée `False`, déclenchée `False`.
- Empreinte de réponse : `d43b0332d44ec3685f83a57bbf90966ccdb630494fe486e2e908df5eef2a1b83`.
- Checkpoint original inchangé : `True`.
- Composants neuronaux déclarés : `[]`.

## Interprétation
L'ouverture « Photosynthesis is » est pertinente, mais la suite « one of many, but all the algae oxygen is » ne constitue pas une explication correcte ou complète. Le journal montre qu'après les premières transitions prompt+préfixe, le runtime retombe sur des transitions générales et ajoute ensuite des candidats d'association contextuelle sans structurer une proposition explicative. La convergence rapportée est uniquement une stabilité du classement entre partitions d'Obsiss ; elle ne prouve ni la justesse sémantique ni un point fixe P.

## Conséquences théoriques, conceptuelles et opérationnelles
Le poids ×8 précédemment accordé aux transitions de langue générales est supprimé dans le correctif suivant ; ce run reste la référence avant correction. Les transitions génériques restent disponibles, mais ne reçoivent plus de priorité renforcée sans preuve prompt-conditionnée.

## Conclusion et statut
Exécution complète techniquement réussie en population totale ; objectif de cohérence non atteint pour ce prompt. Il s'agit d'un échec qualitatif observé, pas d'une conclusion sur le potentiel global du modèle.
