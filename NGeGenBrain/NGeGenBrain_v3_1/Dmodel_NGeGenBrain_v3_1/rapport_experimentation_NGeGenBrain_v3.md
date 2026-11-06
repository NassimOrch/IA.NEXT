# Rapport d'expérimentation — NGeGenBrain v3

## 1. DESCRIPTION
Étude comparative de `tinny_llm` et `SmolLM2-135M-Instruct-Q8_0`, puis test de reconstruction et production d'un modèle autonome.

## 2. ARCHITECTURE
Deux familles de runtime ont été utilisées :
- TinyLLM : checkpoint PyTorch autonome + SentencePiece.
- SmolLM2 : GGUF Q8_0 + parser/déquantification + runtime Llama-family autonome.

Le protocole de reconstruction synthétique existant a été rejoué comme contrôle positif.

## 3. PIPELINE COMPLET
Les observations des deux modèles ont été enregistrées dans `research/runs/20261028/teacher_observations.json`. Les prompts de smoke test sont fixes. Les interventions SmolLM2 ont ciblé les couches 0, 5, 10, 15, 20, 25 et 29 par mise à zéro du flux de sortie de couche.

## 4. COMMANDES D'EXÉCUTION
Voir le README V3 et `guide_CLI_NGeGenBrain_v3.md`.

## 5. RÉSULTATS
Les deux modèles ont été chargés localement. Le runtime SmolLM2 expose 30 couches, et le forward retourne 30 ensembles d'activations/attentions dans le mode d'observation. Des ablations de couche ont modifié fortement la distribution de logits dans le runtime local.

Le contrôle synthétique a produit 1.0 de précision holdout sur XOR 4 bits et la reconstruction synthétique a obtenu 1.0 sur son holdout et ses trajectoires composées déclarées.

Le modèle produit a atteint une validation loss finale de ~2.33 sur le corpus interne de 30 000 caractères lors du run final.

## 6. INTERPRÉTATION DES RÉSULTATS
Les résultats montrent que le système peut charger, interroger, instrumenter localement et perturber deux artefacts de modèles de tailles très différentes. Ils ne démontrent pas une compréhension interne complète de ces modèles.

## 7. CONSÉQUENCES
### Théoriques
Le passage de l'adapter abstrait au runtime local augmente la possibilité d'expériences causales réelles.
### Conceptuelles
Les limites de fidélité du runtime doivent être auditées séparément de la logique scientifique.
### Opérationnelles
L'interface de chat et le registre local rendent le test multi-modèle reproductible.

## 8. LIMITES OBSERVÉES
Le runtime SmolLM2 n'a pas été comparé bit-à-bit à un backend de référence disponible dans l'environnement. Les générations smoke sont faibles et ne doivent pas être utilisées comme benchmark de qualité linguistique.

## 9. CONTRE-EXEMPLES
La réussite des contrôles synthétiques ne permet pas d'extrapoler aux LLM réels. La variation de logits sous ablation ne suffit pas à nommer une fonction sémantique.

## 10. CONCLUSIONS
NGeGenBrain v3 a franchi le seuil de l'exécution locale réelle de modèles et de la production d'un petit modèle causal autonome. Il n'a pas démontré une reconstruction mécaniste complète d'un LLM pré-entraîné.

## 11. STATUT DU MODÈLE
`NG-Recomposed-TinyLM-v3` : **tiny LM fonctionnel expérimental**, 41 728 paramètres, indépendant à l'inférence.

## 12. TRAÇABILITÉ
Hashes, observations et résultats sont dans `research/runs/20261028/` et `audit/`.

## 13. REPRODUCTIBILITÉ
Seed produit : 20261028. Corpus hash et historique d'entraînement : `research/models/NG-Recomposed-TinyLM-v3/training.json`.
