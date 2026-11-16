# RAPPORT P2-M027 — finalisation de frontière UTF-8

**Date :** 15 novembre 2026  
**Statut :** smoke test réel PASS, 3/3 prompts ; aucune amélioration sémantique revendiquée.

## 1. Description et architecture

Le décodage byte-fallback peut atteindre le budget maximal alors qu'un bloc `BYTE_START ... BYTE_END` n'est pas fermé. Dans ce cas, la chaîne décodée peut contenir U+FFFD même si les ID du modèle sont conservés. Le correctif ne change ni le choix des tokens, ni l'état GRU, ni l'attention, ni les poids. Il produit une vue d'affichage qui retire seulement le bloc byte terminal non fermé ; la séquence brute reste archivée.

## 2. Pipeline et commande

Avant l'exécution : lecture des cinq fichiers de contrôle, création d'un snapshot complet, re-vérification SHA-256 et préflight P2 PASS. Checkpoint : M-024 64D ; entrée : manifeste `prompts-only` à trois prompts ; décodage greedy ; banque d'attention désactivée comme dans le témoin M-026 ; 96 tokens ; 10 Obsiss ; fenêtre 64 ; non-réponse désactivée. Aucune réponse de référence n'est chargée.

```bash
python Amodel_eSonde_v7/tools/generate_occurrence_attention.py \
  --workspace /mnt/data/eSonde_v7_work \
  --v6-model-dir Dmodel_eSonde_v7/models/eSonde_v6 \
  --checkpoint Amodel_eSonde_v7/experiments/checkpoints/P2_M024_occurrence_attention_64d.json \
  --prompts-only Amodel_eSonde_v7/experiments/P2_HELDOUT_CHAT_PROMPTS_ONLY_20261115.json \
  --output Amodel_eSonde_v7/experiments/P2_M027_UTF8_REAL_SMOKE_64D_20261115.json \
  --decoding greedy --disable-prompt-attention --max-new-tokens 96 \
  --active-obsiss 10 --prompt-window-units 64
```

## 3. Résultats

| Contrôle | Résultat |
|---|---:|
| Code de sortie | 0 |
| Prompts terminés | 3/3 |
| IDs bruts par génération | 96 |
| IDs utilisés pour l'affichage | 92 |
| Tokens byte terminaux incomplets retirés | 4 |
| Identité des IDs bruts avec M-026 | 3/3 exacts |
| U+FFFD dans la réponse affichée | absent, 3/3 |

Les token IDs sont rigoureusement identiques au run M-026 pour chacun des trois prompts. Le rendu ne contient plus le caractère de remplacement terminal ; l'unité byte incomplète de quatre tokens est omise uniquement dans la chaîne affichée. Le hash du JSON smoke est `754df03fe07306fa1dcd784a4c1020d12aace1d48ef020e7d88baac9c755f785`.

## 4. Interprétation et conséquences

Cette correction répare la frontière de sérialisation à la fin du budget. Elle ne change pas les logits et ne rend pas les réponses plus compréhensibles : les trois réponses restent identiques, très répétitives et sans pertinence démontrée par rapport aux prompts. Les IDs bruts sont préservés pour audit. Les blocs byte invalides qui seraient situés au milieu d'une génération ne sont pas traités par cette correction.

## 5. Conclusion et statut

M-027 UTF-8 : `REAL_CHECKPOINT_SMOKE_PASS`. Incident d'affichage résolu dans la portée exacte décrite ci-dessus. P2 reste ouverte, car le critère principal de cohérence conversationnelle n'est pas satisfait.
