# Rapport d'audit — NGeGenBrain v3

## 1. DESCRIPTION
NGeGenBrain v3 est une extension de la V2 fournie dans l'archive source. L'audit conserve la V1 complète dans `legacy_NGeGenBrain_v1/` et reprend les registres, tests, adapters, laboratoire synthétique, moteur causal, hypothèses, découverte, composition, reconstruction, provenance et Web.

La V3 ajoute notamment :
- chargement local GGUF Llama/Q8_0 sans dépendre de `transformers` ;
- chargement du TinyLLM local fourni dans l'archive via un runtime PyTorch autonome ;
- registre de modèles locaux et chargement d'archives ZIP ;
- interface Web de type laboratoire/chat moderne avec choix du modèle ;
- API de chat et d'observation ;
- modèle produit `NG-Recomposed-TinyLM-v3` ;
- suivi, chemins d'environnement, hashes et checkpoints ;
- audit explicite séparant comportement observé, capacité du loader et équivalence au modèle original.

## 2. ARCHITECTURE
La V3 conserve les composants scientifiques de la V2 et ajoute une frontière `LocalModelRegistry` au-dessus des adapters. Les modèles locaux reconnus sont : GGUF Llama/Q8_0, TinyLLM PyTorch local, Hugging Face local lorsque `transformers` est installé, et archives ZIP sûres.

Le produit généré est indépendant à l'inférence : il n'appelle aucun modèle enseignant.

## 3. PIPELINE COMPLET
1. Inventaire et extraction de `models_NGeGenBrain.zip`.
2. Audit des archives V1/V2 et reprise de la suite de tests.
3. Analyse statique des deux modèles LLM fournis.
4. Exécution locale du TinyLLM via un runtime PyTorch autonome.
5. Exécution locale du GGUF SmolLM2-135M via parser GGUF + déquantification Q8_0 + runtime Llama.
6. Tests de génération et observation des couches.
7. Interventions d'ablation au niveau des couches sur le runtime GGUF.
8. Exécution du benchmark synthétique aveugle et du ladder 8 niveaux.
9. Reconstruction synthétique indépendante.
10. Production d'un petit modèle neuronal autonome par entraînement sur le corpus public de travail et les observations enregistrées.
11. Validation train/validation, test de génération et chargement par l'interface.
12. Validation de l'API Web et des tests d'intégration.

## 4. COMMANDES D'EXÉCUTION
```text
ngbrain.py status
ngbrain.py model list
ngbrain.py model local --paths <chemin>
ngbrain.py chat --model-path <chemin> --prompt "..."
ngbrain.py produce-tinylm --corpus research/corpus/public_training_corpus.txt --output research/models/NG-Recomposed-TinyLM-v3
ngbrain.py serve --host 127.0.0.1 --port 8767
```

Windows : `ngbrain_NGeGenBrain_v3.bat status`, `test`, `web`, `examples`, `report`.

## 5. RÉSULTATS
### Suite logicielle
- Tests V3 : **52/52 OK** après correction de l'interface.
- Benchmark synthétique XOR 4 bits : exactitude holdout **1.0**, domaine complet interrogé **1.0**.
- Ladder synthétique : 8 niveaux exécutés, instrumentation/intervention exercées selon les capacités déclarées.
- Reconstruction causale synthétique : holdout **1.0**, exactitude de génération **1.0** sur le domaine expérimental déclaré, sans appel à la source lors de l'inférence composée.

### SmolLM2-135M-Instruct-Q8_0
- Format : GGUF Q8_0.
- Architecture détectée : famille Llama.
- Paramètres estimés : **134 514 432**.
- 30 blocs, hidden size 576, vocabulaire 49 152, contexte 8192.
- Chargement local réel effectué.
- Forward réel effectué.
- Génération réelle effectuée.
- 30 couches observables dans le runtime V3.
- Interventions de zéro sur plusieurs couches effectuées.

### TinyLLM fourni
- Format : checkpoint PyTorch + tokenizer SentencePiece.
- Paramètres : **76 868 096**.
- Architecture : Tinyllm causal, 8 couches, hidden 512, vocabulaire 49 958.
- Chargement réel et forward réel effectués sans `transformers` grâce au runtime autonome V3.
- Génération réelle effectuée.

### Modèle produit par NGeGenBrain v3
- Nom : `NG-Recomposed-TinyLM-v3`.
- Architecture : GRU causal byte-level.
- Paramètres : **41 728**.
- Entraînement : corpus public V3 + observations enregistrées, aucun oracle enseignant à l'inférence.
- Loss validation : environ **21.98 → 2.33** sur le run final.
- Génération autonome vérifiée via CLI et API Web.

## 6. INTERPRÉTATION DES RÉSULTATS
La V3 a effectivement produit un modèle neuronal causal autonome et exécutable. Elle a aussi permis l'exécution locale réelle de deux modèles fournis dans l'archive.

En revanche, **le produit n'est pas un LLM au sens usuel**. Avec 41 728 paramètres, il s'agit d'un tiny language model expérimental. Il ne faut pas le présenter comme un LLM de plusieurs dizaines ou centaines de millions de paramètres, ni comme une reconstruction interne de SmolLM2 ou TinyLLM.

La reconstruction synthétique démontre une capacité indépendante dans un domaine contrôlé. Elle ne démontre pas une reconstruction mécaniste complète d'un LLM pré-entraîné.

## 7. CONSÉQUENCES
### Théoriques
Le protocole reste compatible avec la distinction observation / intervention / hypothèse / preuve. La V3 ajoute une couche de runtime qui permet de rendre certaines expériences réellement exécutables sur des artefacts LLM locaux.

### Conceptuelles
L'expérience confirme la nécessité de distinguer :
- loader fonctionnel ;
- reproduction comportementale ;
- instrumentation interne ;
- causalité locale ;
- équivalence mécaniste ;
- capacité de recomposition.

### Opérationnelles
Le pipeline est maintenant utilisable avec des modèles locaux sans téléchargement distant, avec choix du modèle dans l'interface et chat séparé du laboratoire.

## 8. LIMITES OBSERVÉES
1. Le runtime GGUF V3 est un runtime expérimental autonome. Son exécution a été validée techniquement, mais aucune comparaison bit-à-bit avec une implémentation de référence `llama.cpp` n'a été possible dans l'environnement sans backend externe.
2. La qualité de génération observée sur les deux checkpoints fournis est faible dans les smoke prompts utilisés ; aucune conclusion de qualité générale ne doit être tirée de ces quelques générations.
3. `transformers` n'était pas disponible et l'installation réseau a échoué ; l'adapter Hugging Face de V2/V3 reste testé contractuellement, pas avec un checkpoint Transformers via cette dépendance.
4. Le modèle produit est volontairement très petit. Son statut est celui d'un modèle de recherche exécutable, pas d'un LLM compétitif.
5. Une intervention de mise à zéro d'une couche entière est une perturbation forte ; elle établit une sensibilité causale du runtime, pas une fonction sémantique de la couche.

## 9. CONTRE-EXEMPLES
- Une bonne reconstruction synthétique ne permet pas d'inférer une bonne reconstruction d'un LLM.
- Une sortie textuelle produite par un modèle ne prouve pas que le loader reproduit toutes ses opérations internes.
- Une variation de logits sous ablation ne prouve pas à elle seule la fonction sémantique de la couche.
- Une baisse de loss du produit ne prouve pas une compréhension mécaniste du corpus enseignant.

## 10. CONCLUSIONS
**Statut scientifique de NGeGenBrain v3 : fonctionnel comme laboratoire expérimental et comme système de reconstruction dans les domaines effectivement testés.**

**Statut du modèle produit : tiny language model neuronal réellement chargé et génératif, mais pas LLM au sens de l'échelle usuelle et pas reconstruction mécaniste de SmolLM2/TinyLLM.**

Aucune réussite générale non mesurée n'est revendiquée.

## 11. STATUT DU MODÈLE
- NGeGenBrain v3 logiciel : **VALIDÉ PAR 52/52 TESTS**.
- Runtime TinyLLM : **EXÉCUTÉ**.
- Runtime SmolLM2 GGUF : **EXÉCUTÉ**.
- Reconstruction synthétique : **VALIDÉE DANS LE DOMAINE DÉCLARÉ**.
- `NG-Recomposed-TinyLM-v3` : **TRAINED_AND_VALIDATED**, modèle de recherche de 41 728 paramètres.
- Reconstruction mécaniste complète d'un LLM : **NON DÉMONTRÉE**.

## 12. TRAÇABILITÉ
Voir `audit/model_input_hashes.json`, `chemin_env_travail_NGv3.json`, `research/runs/20261028/`, les registres JSONL du workspace et les checksums de release.

## 13. REPRODUCTIBILITÉ
Le run est fixé par les seeds et les hashes enregistrés. Les archives finales contiennent le code, les tests, les rapports, les scripts de vérification et le modèle produit. Les résultats non favorables ne sont pas supprimés.
