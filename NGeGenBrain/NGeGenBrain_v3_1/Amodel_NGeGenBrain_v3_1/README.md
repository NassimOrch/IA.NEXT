# NGeGenBrain v3_1 — laboratoire d'observation et de reconstruction multi-vues

**Version logicielle : 3.1.0**

NGeGenBrain v3_1 reprend les exigences du prompt normatif V2, charge et instrumente les deux checkpoints locaux fournis (SmolLM2 GGUF Q8_0 et `tinny_llm` PyTorch/SentencePiece), et compare ces modèles aux artefacts étudiants v3_0 et v3_1. Il conserve l'ancien chemin de génération du tiny LM et ajoute un routeur d'observation distinct à huit vues, appris à partir de données anglaises basées sur les observations enregistrées.

Cette version est un laboratoire expérimental, pas un LLM compétitif et pas une reconstruction mécaniste déjà démontrée des deux modèles sources. Les limites et les contre-exemples sont conservés dans le rapport d'audit.

## Démarrage local

Python 3.11+ est requis. Après installation des dépendances :

```bash
python ngbrain.py status
python scripts/launch_web.py --host 127.0.0.1 --port 8767
```

Sous Windows, lancez `ngbrain_NGeGenBrain_v3_1.bat install`, puis `ngbrain_NGeGenBrain_v3_1.bat web`. Le lanceur Python et les API ont été exécutés et testés sous Linux; le BAT a été statiquement validé, mais n'a pas pu être lancé physiquement sous Windows dans l'environnement de construction Linux. Voir l'audit pour le statut exact.

## Charger un modèle local

Dans le panneau **Modèles locaux**, choisissez un chemin local ou importez un ZIP / GGUF, chargez le checkpoint puis sélectionnez-le dans le sélecteur de modèle du chat. Le registre Web a réellement chargé et interrogé les trois formats suivants :

- `model_produit_NG_v3_1.zip` — NG-Recomposed-TinyLM-v3_1, 55 568 paramètres;
- `SmolLM2-135M-Instruct-Q8_0.zip` — GGUF Q8_0, environ 134,5 millions de paramètres;
- `tinny_llm.zip` — checkpoint PyTorch `pytorch_model.bin` avec tokenizer SentencePiece, 76,87 millions de paramètres.

Le runtime GGUF est ciblé sur le modèle Smol fourni; les modèles Hugging Face locaux génériques restent dépendants des bibliothèques/adaptateurs installés. Aucun téléchargement de modèle distant n'est déclenché implicitement.

## Résultat comparatif mesuré

Le protocole commun a évalué 16 passages anglais (96 octets UTF-8 par passage) et 8 passages chinois, sur les quatre checkpoints. En bits par octet UTF-8 (BPB; inférieur est meilleur) :

| Modèle | Anglais | Chinois |
|---|---:|---:|
| SmolLM2 source | 1,2910 | 3,6776 |
| TinyLLM source | 2,1308 | 1,6790 |
| Étudiant v3_0 | 2,9968 | 31,6871 |
| Étudiant v3_1 | 2,9968 | 31,6871 |

La reconstruction étudiante reste nettement sous les modèles sources, notamment sur le chinois. Sur le test final frais du routeur à huit vues : 9/32 (28,125 %); sur validation : 2/16 (12,5 %, hasard uniforme). Le test pilote antérieur de 4/16 est conservé uniquement comme historique et n’est pas la métrique finale; les résultats ne démontrent pas une généralisation robuste. Le chemin génératif de v3_1 reste identique à v3_0 : logits bit-à-bit égaux sur 24 textes et générations déterministes identiques sur les deux prompts de contrôle enregistrés.

## Chemins et traçabilité

Les chemins exacts de l’environnement de travail et des livrables sont conservés dans `chemin_env_travail_NGv3_1.json` et `chemins_NGeGenBrain_v3_1.json`. Les sommes SHA-256 finales seront disponibles dans `deliverables/checksums.sha256`.

## Reproductibilité, rapports et tests

- Rapport complet : `deliverables/rapport_etude_comparative_NGeGenBrain_v3_1.pdf` et `.tex`.
- Source de la spécification V2 lue : `audit/source_materials/prompt_NGeGenBrain_v2.txt` et `audit/source_materials/Dmodel_NGeGenBrain_v2.zip`.
- Correspondance exigences V2 → implémentation : `audit/v2_prompt_hierarchy_crosswalk.md`.
- Étude comparative finale : `audit/source_vs_student_multiview_release_final2/` (comparaison et préservation figées pour la livraison).
- Dataset d'observation anglais : `research/multiview_reconstruction_v3_1/dataset_v3_final/`.
- Modèle produit : `model_produit_NG_v3_1/` et `bundled_artifacts/model_produit_NG_v3_1.zip` (également livré séparément).

Tests exécutés après correction :

```bash
python -m pytest -q          # 66 tests réussis
python ngbrain.py legacy-test # 65 tests de non-régression V1 réussis
```

Pour l'étude scientifique, consulter `audit/rapport_experimentation_NGeGenBrain_v3_1.md`; pour les défauts trouvés, corrections, statuts et limites, consulter `audit/rapport_audit_NGeGenBrain_v3_1.md`.
