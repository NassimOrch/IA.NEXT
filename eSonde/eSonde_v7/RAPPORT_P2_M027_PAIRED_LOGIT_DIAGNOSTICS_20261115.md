# RAPPORT P2-M027 — diagnostic apparié des distributions de tokens et des occurrences

**Date :** 15 novembre 2026  
**Statut :** TERMINÉ — 6/6 couples variante/prompt ; parité exacte 6/6 aux deux ancres ; qualité conversationnelle non validée.

## 1. Description et question

M-027 mesure, sur les checkpoints M-024 gelés, (a) l'effet numérique de la banque d'occurrences USER sur la distribution complète du prochain token et (b) la dépendance de cet effet à l'association entre contenu d'occurrence et position d'origine. Aucun entraînement, checkpoint-write ou génération libre n'est effectué. Les trois entrées sont le manifeste `prompts-only` de TEST ; aucune réponse de référence n'est chargée.

## 2. Architecture et conditions

Les checkpoints 64D et 130D sont gardés inchangés. Les tokens du prompt, les projections Obsiss du GRU et l'état récurrent restent constants entre conditions. Seule la voie banque K/V change :

1. `exact_bank` : chaque token USER et sa projection restent associés à leur position.
2. `no_bank` : suppression des K/V ; le prompt continue d'être traité par le GRU.
3. `reversed_occurrences` : permutation inverse du contenu token/observation entre les positions USER dans la banque K/V seulement ; les requêtes et la séquence GRU ne changent pas.

Deux ancres sont mesurées : après le prompt, et après le premier bloc byte-fallback complet de la génération M-024 archivée (teacher forcing d'un préfixe produit par le modèle, jamais d'une réponse cible).

## 3. Pipeline complet et commande

Préflight P2 et snapshot préexistants vérifiés ; empreintes V6, checkpoints et manifeste `prompts-only` relues ; distributions sur le vocabulaire autorisé calculées en mémoire ; distances JS, L1/TV, cosinus, Spearman, top-1 et Jaccard top-10 enregistrées ; parité de la condition exacte avec les choix greedy archivés contrôlée aux deux ancres.

```bash
PYTHONPATH=Dmodel_eSonde_v7/src python \
  Amodel_eSonde_v7/tools/diagnose_m027_logits.py \
  --workspace /mnt/data/eSonde_v7_work \
  --v6-model-dir Dmodel_eSonde_v7/models/eSonde_v6 \
  --output Amodel_eSonde_v7/experiments/P2_M027_PAIRED_LOGIT_DIAGNOSTICS_20261115.json
```

Code de sortie : **0**. Préflight : **PASS**. Parité exacte : **6/6 initiale et 6/6 après préfixe**. Cible exposée : **false**. Entraînement : **false**.

## 4. Résultats

| Comparaison | Ancre initiale JS moyenne (nats) | Après préfixe JS moyenne (nats) | TV initiale | TV après préfixe |
|---|---:|---:|---:|---:|
| Banque exacte vs absente | **0,375417** | **0,269857** | **0,715019** | **0,582322** |
| Banque exacte vs occurrences inversées | 0,020179 | 0,006528 | 0,114437 | 0,087198 |

Détail par variante :

| Mesure | 64D | 130D |
|---|---:|---:|
| JS exact/absent, initiale | 0,322797 | 0,428037 |
| JS exact/absent, après préfixe | 0,291465 | 0,248249 |
| JS exact/inversé, initiale | 0,008958 | 0,031399 |
| JS exact/inversé, après préfixe | 0,004738 | 0,008318 |
| JS entre prompts, banque exacte, initiale | 0,001678 | 0,005913 |
| JS entre prompts, banque exacte, après préfixe | 0,011907 | 0,024577 |

Le top-1 de l'ancre initiale et de l'ancre après préfixe est `BYTE_START` pour les six couples variant/prompt sous banque exacte. L'inversion des contenus change le top-1 dans un seul des six cas (130D, un prompt, ancre initiale). Les top-10 demeurent identiques entre prompts à l'ancre initiale pour les deux variantes.

## 5. Interprétation des résultats

Le retrait de la banque modifie fortement les distributions complètes : la banque a donc une influence numérique réelle sur le chemin de calcul. Toutefois, l'inversion de l'association occurrence-position a un effet moyen nettement plus petit dans cinq des six cas. Cela est compatible avec une modulation agrégée ou un biais global de la banque davantage qu'avec une lecture fortement sélective de chaque association positionnelle. Un cas 130D réagit davantage ; la conclusion n'est donc pas uniforme.

La sensibilité initiale aux trois prompts est faible, et le top-1 commun est un marqueur structurel du tokenizer (`BYTE_START`), non un mot lexical. Cela peut contribuer au démarrage byte-fallback, sans suffire à expliquer toutes les répétitions ultérieures. Les trois prompts sont des consignes créatives ; l'échantillon est trop restreint pour généraliser à l'ensemble du dialogue.

## 6. Conséquences théoriques, conceptuelles et opérationnelles

- **Théoriques :** influence fonctionnelle, association occurrence-position, discrimination contextuelle et correction sémantique sont quatre propriétés distinctes.
- **Conceptuelles :** les observations Obsiss ne doivent pas seulement perturber les logits ; leur contribution propre doit être liée à l'identité et à la position de l'occurrence, et mesurée séparément.
- **Opérationnelles :** prochaine expérience M-028 : ablation des vecteurs d'observations Obsiss (exact, zéro, permutation ; séparation collectif/sentinelles en 130D), à poids gelés, sans entraînement ni génération libre.

## 7. Conclusion et statut du modèle

M-027 confirme l'influence fonctionnelle de la banque K/V, mais ne démontre pas que l'association précise entre occurrence, position et observation est suffisamment discriminante. Le résultat ne démontre ni compréhension ni cohérence. Les générations libres M-024/M-025/M-026 restent de qualité insuffisante. **P2 demeure IN_PROGRESS ; aucun checkpoint n'est promu au runtime public.**

## 8. Intégrité et provenance

- Résultat : `Amodel_eSonde_v7/experiments/P2_M027_PAIRED_LOGIT_DIAGNOSTICS_20261115.json`
- SHA-256 du résultat : `20c7ad95c7a9b535c8382f94a9d45f0836192c23b40e31d75753476d1eb4ee32`
- Checkpoint parent V6 : `8526943d1528418fa8bbbf9128b61b5e1acd90a16eeb7cc062e18864b083dff4` (64 000 000 octets)
- Checkpoints M-024 : 64D `c877fa76492ca8219ebeb1d2ca714ed959ed22d4884b228867968cf999122760` ; 130D `d8eaabf4513010933c5aea1301c688573856f059187bc6d4e7c730053431f1e9`
- Manifeste prompts-only : `f7c0f3cb79711d91a5a437fd4118c9745c8427c933327994aaee045299b7ec3e`

Les vecteurs complets de probabilité ne sont pas persistés ; seules les distances et synthèses top-10 le sont. Les artefacts sources sont conservés tels quels.
