# RAPPORT P2-M026 — ablation de la banque d’attention, variante 64D

**Date :** 15 novembre 2026  
**Statut :** 64D terminé (3/3) ; 130D en attente. P2 reste `IN_PROGRESS`.

## Description

M-026 teste si la banque explicite des occurrences du prompt modifie les trajectoires de génération libre des checkpoints M-024 gelés. Il s’agit d’une ablation à l’inférence : aucun réentraînement et aucune modification du checkpoint.

## Architecture et intervention

Le checkpoint M-024 64D est utilisé avec le même adaptateur Obsiss, 10 Obsiss actives, le même préfixe utilisateur limité aux 64 dernières unités, le même moteur GRU et le même prompt. Seule la banque clé/valeur d’occurrences est désactivée (`use_prompt_attention=false`). Les tokens du prompt demeurent dans la séquence du GRU : l’essai ne supprime donc pas tout conditionnement par le prompt.

## Pipeline complet

1. Lecture des cinq fichiers de contrôle et validation P2.
2. Vérification du snapshot pré-exécution et du checkpoint V6 original.
3. Vérification SHA-256 du checkpoint M-024 64D et du manifeste prompts-only.
4. Exécution déterministe greedy sur les trois prompts TEST, 96 tokens, 10 Obsiss, fenêtre 64.
5. Vérification des métadonnées : attention désactivée, zéro occurrence contextuelle, aucune réponse de référence, non-réponse désactivée.
6. Écriture atomique du JSON et vérification du code de sortie.

## Commande d’exécution

```bash
python Amodel_eSonde_v7/tools/generate_occurrence_attention.py \
  --checkpoint Amodel_eSonde_v7/experiments/checkpoints/P2_M024_occurrence_attention_64d.json \
  --output Amodel_eSonde_v7/experiments/P2_M026_ATTENTION_KNOCKOUT_64D_20261115.json \
  --decoding greedy --disable-prompt-attention --max-new-tokens 96 \
  --active-obsiss 10 --prompt-window-units 64
```

## Résultats

- Code de sortie : `0`.
- Générations : `3/3`.
- Attention explicite : désactivée sur les trois exemples.
- Occurrences contextuelles exposées à la banque : `0`.
- Les trois prompts distincts ont produit exactement la même séquence de 96 tokens : `لا الالالا الالالا الالالا الالالا الالالا ا�`.
- Ratio de tokens distincts : `0,0729` ; ratio de bigrammes distincts : `0,0947` ; ratio de trigrammes distincts : `0,1064`.
- SHA-256 du JSON : `cbdf4fc51082d41e73a33279e07f64ea196b92b9cd31e3e5baa0e2f08098cb67`.
- Les poids V6 restent inchangés : 64 000 000 octets, SHA-256 `8526943d1528418fa8bbbf9128b61b5e1acd90a16eeb7cc062e18864b083dff4`.

## Interprétation

Dans cette condition greedy et sur ces trois prompts créatifs, le chemin qui reste après retrait de la banque d’occurrences ne différencie pas les sorties : la même séquence est émise à chaque fois. Le résultat est compatible avec une forte dépendance fonctionnelle à la banque d’occurrences pour éviter cette trajectoire dégénérée, mais ne démontre pas que l’attention active produit une compréhension correcte. Les tokens du prompt restent traités par le GRU, ce qui limite la portée causale de l’intervention.

La chaîne contient un caractère de remplacement final (`�`) ; il est conservé tel qu’observé dans le résultat, et doit faire l’objet d’un diagnostic distinct de la grammaire byte/UTF-8. Il ne faut pas le réparer dans les données d’expérience.

## Conséquences

- **Théorique :** le mécanisme d’attention explicite a une influence fonctionnelle potentielle sur la trajectoire, mais sa contribution sémantique n’est pas démontrée.
- **Conceptuelle :** la banque d’occurrences ne peut être assimilée à une preuve d’ancrage ; il faut des ablations de logits, de perturbation de positions et de permutation des occurrences.
- **Opérationnelle :** 64D est terminé ; la même intervention doit être exécutée sur 130D avant toute comparaison appariée.

## Conclusion

Résultat négatif sur la qualité de génération sans banque : la sortie s’effondre vers une séquence identique et à faible diversité. Résultat non conclusif sur la qualité du mécanisme avec banque. Aucune conclusion sur l’impossibilité ou la réussite globale d’eSonde n’est autorisée.

## Validation documentaire et logicielle

La suite runtime passe à 61/61 tests. Les quatre sources LaTeX passent deux compilations chacune (8 passes, 0 erreur fatale, 0 débordement horizontal). Des avertissements `Underfull` restent consignés dans `P2_M026_TEX_COMPILE_20261115.json`.

## Statut

`M026_64D_COMPLETE_3_OF_6`; poursuivre avec la variante 130D après sauvegarde complète et nouveau préflight P2.
