# RAPPORT P2-M026 — ablation de la banque d’attention par occurrences

**Date :** 15 novembre 2026  
**Statut :** 6/6 générations terminées ; effet fonctionnel sur la trajectoire confirmé ; porte de qualité sémantique non franchie ; P2 reste ouverte.

## 1. Description

M-026 évalue la contribution fonctionnelle de la banque explicite des occurrences USER dans les checkpoints M-024 gelés. Il s’agit d’une intervention à l’inférence : les paramètres entraînés ne sont ni modifiés ni réentraînés. Les mêmes trois prompts TEST prompts-only sont utilisés pour 64D et 130D.

## 2. Architecture et intervention

Le chemin conserve : tokenisation, observations causales, projection Obsiss, embedding, positions intégrées à la séquence, état GRU et poids du checkpoint. L’intervention désactive seulement la banque clé/valeur des occurrences et son attention croisée (`use_prompt_attention=false`). Les tokens du prompt restent donc lus par le GRU ; M-026 n’est pas une suppression complète du prompt.

Paramètres fixes : 10 Obsiss actives, fenêtre utilisateur de 64 unités, greedy, 96 tokens maximum, non-réponse désactivée, aucune réponse de référence, aucune table de récupération, aucun apprentissage et aucune écriture de checkpoint.

## 3. Pipeline complet

1. Lecture de `chemins_eSonde_v7.json`, `checklist_de_travail_eSonde_v7.json`, des deux checklists d’incidents et du pointeur de sauvegarde.
2. Vérification d’un snapshot complet et SHA-256 avant chaque variante.
3. Préflight P2 ; vérification SHA-256 du checkpoint variant, du manifeste prompts-only et des 64 000 000 octets de poids V6 originaux.
4. Génération séparée 64D puis snapshot intermédiaire, puis génération 130D.
5. Contrôle des sorties atomiques, du code 0, de l’absence de réponse de référence et de `context_occurrences=0`.
6. Comparaison avec les contrôles greedy M-024 attention activée.

## 4. Commandes d’exécution

```bash
python Amodel_eSonde_v7/tools/generate_occurrence_attention.py \
  --workspace /mnt/data/eSonde_v7_work \
  --v6-model-dir /mnt/data/eSonde_v7_work/Dmodel_eSonde_v7/models/eSonde_v6 \
  --checkpoint Amodel_eSonde_v7/experiments/checkpoints/P2_M024_occurrence_attention_64d.json \
  --output Amodel_eSonde_v7/experiments/P2_M026_ATTENTION_KNOCKOUT_64D_20261115.json \
  --decoding greedy --disable-prompt-attention --max-new-tokens 96 \
  --active-obsiss 10 --prompt-window-units 64
```

La même commande a été exécutée avec le checkpoint et la sortie `130d` correspondants.

## 5. Résultats

| Variante | Sorties distinctes parmi 3 prompts | Ratio tokens distincts | Observation |
|---|---:|---:|---|
| 64D sans banque | 1/3 | 0,0729 | Les trois séquences de 96 tokens sont exactement identiques, en arabe/bytes, avec un caractère de remplacement final dans le rendu texte |
| 130D sans banque | 2/3 | 0,09375 | Deux séquences sont identiques ; la troisième diffère au début puis rejoint le même motif répétitif `da` |

Les six exécutions ont code 0, préflight PASS, `prompt_attention_enabled=false`, `context_occurrences=0`, 10 Obsiss actives et aucune réponse de référence exposée. Les sorties exactes et leurs token IDs demeurent dans les JSON individuels.

Les contrôles M-024 avec banque active produisent d’autres séquences : 64D commence respectivement par `Danders`, `Mardes`, `Marder` ; 130D commence par `Ma`, `An`, `An`. Les sorties avec banque active restent elles aussi répétitives et incohérentes.

## 6. Interprétation des résultats

Le knockout change la trajectoire greedy des deux variantes : la banque d’occurrences a donc un effet fonctionnel dans le chemin d’inférence. En 64D, son retrait effondre les trois prompts sur une séquence strictement identique. En 130D, deux prompts convergent vers la même séquence et le troisième vers une variante superficielle du même motif.

Cette différence ne démontre pas que l’attention lit les bonnes occurrences ni qu’elle forme une représentation sémantique. Le résultat « attention active » est également de mauvaise qualité. Les poids d’attention restent des coefficients internes, pas une attribution ni un certificat de compréhension.

## 7. Conséquences

- **Théorique :** l’attention explicite participe effectivement au calcul de la trajectoire, mais son rôle sémantique n’est pas établi.
- **Conceptuelle :** une influence sur le token choisi doit être distinguée de l’ancrage au contexte ; les Obsiss doivent préserver des voix distinctes sans confondre concentration et pertinence.
- **Opérationnelle :** M-027 doit comparer les distributions complètes, les rangs et les changements de logits en conditions appariées attention ON/OFF, puis tester une permutation des positions d’occurrence. Les tokens du prompt restent présents dans les deux conditions.

## 8. Conclusion

M-026 confirme une influence fonctionnelle de la banque d’occurrences sur les séquences décodées, mais ne produit pas de preuve de compréhension contextuelle. Les deux variantes échouent encore au critère de réponse cohérente. Il serait incorrect de conclure que l’attention est inutile ; il serait tout aussi incorrect de la déclarer solution.

## 9. Statut du modèle

`M026_COMPLETE_6_OF_6; FUNCTIONAL_EFFECT_CONFIRMED; SEMANTIC_QUALITY_GATE_NOT_PASSED`. P2 reste `IN_PROGRESS`. M-027 est la prochaine expérience autorisée après mise à jour du formalisme, des checklists, un snapshot complet et un nouveau préflight.
