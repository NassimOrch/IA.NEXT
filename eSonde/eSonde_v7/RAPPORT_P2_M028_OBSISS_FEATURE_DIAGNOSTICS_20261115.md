# Rapport P2 — M-028 : ablation des caractéristiques Obsiss

**Date :** 15 novembre 2026  
**Statut :** terminé comme diagnostic d'inférence ; critère de qualité conversationnelle non satisfait.  
**Résultat JSON :** `Amodel_eSonde_v7/experiments/P2_M028_OBSISS_FEATURE_DIAGNOSTICS_20261115.json`  
**SHA-256 :** `d5a637b474506c8926f0cf52c5b497095c5bcdc76d6564415d2601ada7f530ce`  
**Snapshot préalable :** `/mnt/data/sav_eSonde_v7/snapshots/pre_P2_M028_OBSISS_FEATURE_DIAGNOSTICS_20261115`  
**SHA-256 du manifeste :** `419d3aa3e625d988fbc05f93539426b2211d3293de3c984a665a8ad6f776e871`

## 1. Description

M-028 répond à la question suivante : les caractéristiques projetées des Obsiss apportent-elles une information mesurable aux distributions de prochain token, et leur affectation aux occurrences du prompt est-elle déterminante ? Sur le checkpoint 130D, l'essai sépare également le bloc collectif 64D des 66 canaux sentinelles (deux Obsiss individualisées et leurs masques).

Il s'agit d'une intervention **à l'inférence sur des checkpoints gelés**. L'essai ne réentraîne aucun poids, ne génère aucune nouvelle réponse libre et ne charge aucune réponse cible. Il n'est donc pas une comparaison entre modèles entraînés avec et sans Obsiss.

## 2. Architecture et conditions

Deux checkpoints M-024 sont chargés, 64D et 130D. Pour chacun des trois prompts du manifeste `PROMPTS_ONLY_NO_REFERENCE_ANSWERS`, dix Obsiss sont actives et la fenêtre d'entrée est identique à celle du checkpoint M-024 : les 64 dernières unités utilisateur. Le contexte est construit à partir des occurrences du prompt et les features Obsiss restent transitoires.

Les interventions sont :

- `exact` : les vecteurs Obsiss projetés sont laissés inchangés ; témoin de parité.
- `zero_obsiss` : tous les canaux Obsiss projetés sont mis à zéro ; embeddings token et position conservés.
- `permuted_obsiss` : les vecteurs Obsiss sont inversés entre positions USER ; tokens, ordre et positions ne sont pas permutés.
- `collective_only` (130D) : les 64 canaux collectifs sont conservés, les 66 canaux sentinelles et leurs masques sont mis à zéro.
- `sentinels_only` (130D) : les 64 canaux collectifs sont mis à zéro, les 66 canaux sentinelles et leurs masques sont conservés.

Deux ancres de distribution sont mesurées : après le prompt complet, puis après le premier bloc byte-fallback complet de la génération greedy M-024 déjà archivée. Le second préfixe est un témoin historique ; aucune génération nouvelle n'est effectuée.

## 3. Pipeline complet

1. Lecture des cinq fichiers de contrôle et vérification du statut P2.
2. Création et re-hachage du snapshot intégral pré-exécution.
3. Préflight P2 : `PASS`, 29 incidents modèle et 26 non-modèle consultés ; aucun incident critique non-modèle ouvert.
4. Vérification des empreintes du checkpoint V6, des checkpoints M-024 et du manifeste prompts-only.
5. Vérification que les trois entrées ne contiennent aucun champ réponse, cible ou référence.
6. Calcul des 16 observations causales et projection Obsiss par occurrence.
7. Application indépendante des cinq conditions prévues, sans mutation des vecteurs source.
8. Calcul de la distribution complète admissible de prochain token aux deux ancres.
9. Contrôle de parité `exact` par rapport aux tokens archivés ; calcul de JS, L1, TV, cosinus, Spearman, égalité top-1, Jaccard top-10 et sensibilité inter-prompts.
10. Écriture atomique du JSON, du log, du code de sortie et du présent rapport.

## 4. Commande d'exécution

```bash
cd /mnt/data/eSonde_v7_work
PYTHONPATH=Dmodel_eSonde_v7/src python Amodel_eSonde_v7/tools/diagnose_m028_obsiss_features.py \
  --workspace /mnt/data/eSonde_v7_work \
  --v6-model-dir Dmodel_eSonde_v7/models/eSonde_v6 \
  --prompts-only Amodel_eSonde_v7/experiments/P2_HELDOUT_CHAT_PROMPTS_ONLY_20261115.json \
  --output Amodel_eSonde_v7/experiments/P2_M028_OBSISS_FEATURE_DIAGNOSTICS_20261115.json
```

## 5. Résultats

### 5.1 Exécution et intégrité

- Statut `PASS`, code de sortie 0.
- 64D : 3 prompts × 3 conditions ; 130D : 3 prompts × 5 conditions.
- Parité `exact` : 6/6 au premier token et 6/6 après le préfixe assistant archivé.
- Aucune cible/réponse exposée ; aucun entraînement ; aucune génération libre ; aucune écriture de checkpoint.
- `non_response_enabled=false`.
- Hash V6 inchangé : `8526943d1528418fa8bbbf9128b61b5e1acd90a16eeb7cc062e18864b083dff4` ; taille : 64 000 000 octets.

### 5.2 Retrait complet des caractéristiques Obsiss

| Variante | Ancre | JS moyenne (nats) | TV moyenne | Changements top-1 |
|---|---|---:|---:|---:|
| 64D | Prompt | 0.053118 | 0.236845 | 0/3 |
| 64D | Après préfixe | 0.355170 | 0.734095 | 0/3 |
| 130D | Prompt | 0.222498 | 0.536904 | 0/3 |
| 130D | Après préfixe | 0.186926 | 0.483660 | 0/3 |

Le retrait des vecteurs Obsiss déplace substantiellement la distribution complète, surtout à l'ancre après le premier bloc de réponse en 64D. Toutefois, le token top-1 demeure identique dans les trois prompts, pour les deux ancres et les deux variantes. Les caractéristiques contribuent donc au calcul des logits, mais ce déplacement ne suffit pas à changer la décision top-1 observée.

### 5.3 Permutation des caractéristiques entre occurrences USER

| Variante | Ancre | JS moyenne (nats) | TV moyenne | Changements top-1 |
|---|---|---:|---:|---:|
| 64D | Prompt | 0.040019 | 0.210934 | 1/3 |
| 64D | Après préfixe | 0.002350 | 0.047685 | 0/3 |
| 130D | Prompt | 0.125275 | 0.442283 | 0/3 |
| 130D | Après préfixe | 0.011920 | 0.114404 | 0/3 |

La permutation a un effet plus net juste après le prompt qu'après le premier bloc assistant. En 64D, l'effet moyen après préfixe est très faible (JS 0.002350). En 130D, il décroît également fortement (JS 0.011920). Un seul des trois prompts 64D change de top-1 à l'ancre initiale ; aucun changement top-1 n'est observé dans les autres comparaisons de permutation.

### 5.4 Séparation collectif / sentinelles dans le 130D

| Condition contre le 130D exact | Ancre | JS moyenne (nats) | TV moyenne | Changements top-1 |
|---|---|---:|---:|---:|
| Collectif seulement | Prompt | 0.046003 | 0.225850 | 1/3 |
| Collectif seulement | Après préfixe | 0.113141 | 0.385472 | 0/3 |
| Sentinelles seulement | Prompt | 0.030072 | 0.205306 | 0/3 |
| Sentinelles seulement | Après préfixe | 0.038713 | 0.211406 | 0/3 |

Dans cette intervention précise, conserver seulement les 64 canaux collectifs produit un déplacement supérieur à conserver seulement les 66 canaux sentinelles. Les deux blocs influencent toutefois la distribution. Cette comparaison n'est pas additive : les interactions entre blocs et la co-adaptation des poids peuvent modifier l'effet de chacun lorsqu'il est isolé.

### 5.5 Sensibilité aux trois prompts

Pour la condition exacte, JS inter-prompts moyenne :

- 64D : 0.001678 au prompt et 0.011907 après le préfixe.
- 130D : 0.005913 au prompt et 0.024577 après le préfixe.

Les six distributions top-1 initiales du témoin exact restent `BYTE_START`. L'effet des observations dans les distributions complètes doit donc être distingué de leur effet sur le token choisi.

## 6. Interprétation des résultats

Trois constats sont soutenus par ces données :

1. Les caractéristiques Obsiss ne sont pas ignorées numériquement : leur neutralisation change les distributions complètes.
2. L'information attachée à la position des occurrences a un effet mesurable surtout au premier pas, mais son influence se réduit fortement après le premier bloc de réponse archivé.
3. Sur le checkpoint 130D et les trois prompts considérés, la composante collective a une influence numérique plus forte que la composante sentinelle dans les interventions séparées.

Aucun de ces constats ne montre que le modèle interprète correctement le sens d'une occurrence, qu'il comprend le dialogue, ou qu'une Obsiss individuelle constitue une voix cognitive autonome. La persistance de `BYTE_START` au top-1 exact suggère que le goulot de sortie reste à examiner au niveau du mécanisme lexical/byte et de l'objectif d'apprentissage.

## 7. Conséquences

- **Théoriques :** influence d'une feature, attribution à une occurrence et pertinence sémantique doivent être évaluées séparément.
- **Conceptuelles :** le rôle de l'espace des 16 observations n'est pas encore démontré comme un ensemble de dimensions contextuelles discriminantes ; il faut mesurer la stabilité et la spécificité des contributions sans réduire les Obsiss à des poids.
- **Opérationnelles :** garder les observations transitoires ; mesurer les effets sur une séquence de plusieurs tokens ; tester des ablations réentraînées appariées ; ne pas promouvoir les sentinelles comme composant nécessaire.
- **Qualité conversationnelle :** M-028 ne modifie ni les sorties libres ni les checkpoints ; le défaut de cohérence M-024/M-025 reste ouvert.

## 8. Conclusion

M-028 démontre une contribution numérique des caractéristiques Obsiss, mais une sélectivité contenu-position limitée et décroissante au fil du préfixe observé. Les canaux collectifs portent plus de l'influence mesurée que les sentinelles dans ce cas limité. Cette expérience ne permet ni de conclure à l'inutilité des sentinelles ni d'affirmer une compréhension contextuelle. Le critère principal — une réponse de chat cohérente, adaptée au prompt et non répétitive — reste non satisfait.

## 9. Statut

**Terminé :** diagnostic d'inférence, parité exacte 6/6 aux deux ancres, checksums et préflight PASS.  
**Non réalisé :** entraînement ablatif Obsiss, nouveaux dialogues libres, validation sur corpus chat indépendant plus large.  
**Phase :** P2 `IN_PROGRESS`; P3–P6 demeurent bloquées par les critères de sortie P2.

## 10. Artefacts et intégrité

- Résultat : `Amodel_eSonde_v7/experiments/P2_M028_OBSISS_FEATURE_DIAGNOSTICS_20261115.json` (`d5a637b474506c8926f0cf52c5b497095c5bcdc76d6564415d2601ada7f530ce`).
- Plan : `Amodel_eSonde_v7/experiments/P2_M028_OBSISS_FEATURE_DIAGNOSTIC_PLAN_20261115.json` (`04a98bfdcf7c141fc3a71c2a3673cbd365452adc552cb75e45ea5dc6e9b20514`).
- Préflight : `Amodel_eSonde_v7/experiments/P2_M028_PREFLIGHT_20261115.json` (`4f3df88c06eef8a97fd12b1339dfb3b469ed15c8eb9abbc4615f5a5d4436aaf4`).
- Outil : `Amodel_eSonde_v7/tools/diagnose_m028_obsiss_features.py` (`4c8f6bd2fa73c246cff4616b562630f0c660aa06859ff614f2b48f8fd516da4e`).
- Fonction d'intervention : `Dmodel_eSonde_v7/src/esonde_v7/learned/attention_diagnostics.py` (`aa1952949856152297f1f10b03866a2ca619065185d699557597ee22e50a1935`).
- Tests logiciels : 72/72 (`Amodel_eSonde_v7/experiments/P2_M028_SWTEST_20261115.json`).
- Poids originaux V6 : 64 000 000 octets, SHA-256 `8526943d1528418fa8bbbf9128b61b5e1acd90a16eeb7cc062e18864b083dff4` ; inchangés.


## 11. Réconciliation de suivi et re-vérification

Une revue postérieure a retrouvé ce résultat complet dans le snapshot `pre_P2_M028_OBSISS_FEATURES_REPAIRED_TEX_20261115`, alors que le plan M-028 portait encore le statut `READY_FOR_SNAPSHOT_AND_PREFLIGHT`. Le résultat canonique antérieur a été restauré depuis ce snapshot et son SHA-256 vérifié : `d5a637b474506c8926f0cf52c5b497095c5bcdc76d6564415d2601ada7f530ce`.

Une re-vérification redondante avait été lancée avant la découverte de cette incohérence de registre. Elle est conservée séparément sous `Amodel_eSonde_v7/experiments/P2_M028_OBSISS_FEATURE_DIAGNOSTICS_RECHECK_20261115.json` (SHA-256 `507da3a7655b2a2091ffd1faf2433820da32d5a8e800209ecdd53d81ade95194`). La comparaison structurelle confirme que **tous les champs hors bloc `preflight` sont identiques** au résultat canonique ; le recheck enregistre le snapshot plus récent et un compteur d'incidents consultés actualisé. Il ne remplace pas le résultat historique. Cet écart est enregistré comme incident non-modèle NM-028 ; aucun checkpoint, résultat canonique ou donnée d'entraînement n'a été perdu ou modifié.
