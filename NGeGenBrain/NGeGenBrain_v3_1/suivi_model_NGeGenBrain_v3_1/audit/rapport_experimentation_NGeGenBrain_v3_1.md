# Rapport d'expérimentation — comparaison directe NGeGenBrain v3_1

## 1. Description et protocole

Campagne `NG-V3_1-REAL-SOURCE-VS-RECOMPOSED-STUDENT-MULTIVIEW-RELEASE-001`, protocole `ngbrain-v2-hierarchical-multiview-v1.0`, date `2026-10-28T10:29:04.947775+00:00`, Python 3.13.5, PyTorch 2.10.0+cpu, CPU, 2 threads, seed 20261028. Quatre modèles ont été réellement chargés : les deux modèles sources fournis et les modèles étudiants v3_0 / v3_1.

Le corpus figé couvre 16 textes anglais et 8 chinois; chaque modèle est noté sur les 96 premiers octets UTF-8 par document. Les hashes des fichiers sont dans `source_model_study_manifest.json`. La métrique principale entre tokenizers est BPB.

## 2. Scores anglais

| Modèle | bits/octet UTF-8 | exactitude token native | tokens natifs scorés |
|---|---:|---:|---:|
| SmolLM2 source (GGUF Q8_0) | 1.2910 | 20.61% | 262 |
| TinyLLM source (PyTorch/SentencePiece) | 2.1308 | 14.42% | 312 |
| Student NG v3_0 | 2.9968 | 39.87% | 1520 |
| Student NG v3_1 | 2.9968 | 39.87% | 1520 |

## 3. Scores chinois

| Modèle | bits/octet UTF-8 | exactitude token native | tokens natifs scorés |
|---|---:|---:|---:|
| SmolLM2 source (GGUF Q8_0) | 3.6776 | 13.111% | 450 |
| TinyLLM source (PyTorch/SentencePiece) | 1.6790 | 16.561% | 157 |
| Student NG v3_0 | 31.6870 | 0.132% | 760 |
| Student NG v3_1 | 31.6870 | 0.132% | 760 |

L'exactitude au token natif est une information secondaire; les tokenizers ne sont pas comparables directement. BPB reste soumis aux limites d'échantillon et de domaine, et ne constitue pas à lui seul une mesure de qualité conversationnelle générale.

## 4. Interventions résiduelles

Pour les Transformers sources, `zero_update` supprime la mise à jour calculée par le bloc tout en préservant l'entrée résiduelle, tandis que `scale_update` multiplie la mise à jour par 0,5.

| Modèle | cible | intervention | delta L2 logits | top-1 changé |
|---|---|---|---:|---|
| smollm2 | block.0 | zero_update | 3715.7615 | True |
| smollm2 | block.0 | scale_update | 734.8587 | False |
| smollm2 | block.15 | zero_update | 130.8981 | False |
| smollm2 | block.15 | scale_update | 70.9342 | False |
| smollm2 | block.29 | zero_update | 2854.0244 | True |
| smollm2 | block.29 | scale_update | 1242.2162 | True |
| tinny_llm | block.0 | zero_update | 892.0742 | True |
| tinny_llm | block.0 | scale_update | 367.3624 | False |
| tinny_llm | block.4 | zero_update | 289.8722 | True |
| tinny_llm | block.4 | scale_update | 138.4671 | False |
| tinny_llm | block.7 | zero_update | 429.8539 | False |
| tinny_llm | block.7 | scale_update | 151.9572 | False |
| ng_student_v3_0 | rnn.output | zero | 158.4227 | True |
| ng_student_v3_0 | rnn.output | scale | 0.0096 | False |
| ng_student_v3_1 | rnn.output | zero | 182.4326 | True |
| ng_student_v3_1 | rnn.output | scale | 0.0114 | False |

Ces valeurs sont attachées au prompt décrit dans le registre. Elles indiquent une sensibilité causale locale; elles n'attribuent pas un rôle sémantique universel à chaque couche. La réplication multi-prompt est indispensable.

## 5. Génération qualitative

Voir la clé `generation_observations` du JSON de résultats. Les générations déterministes courtes sont incluses comme exemples observables, pas comme classement complet. Deux prompts par modèle sont insuffisants pour conclure à une compétence générale de dialogue.

## 6. Étudiant multi-vues

La version retenue gèle le générateur v3_0 et entraîne un routeur séparé de 1 032 paramètres. Le checkpoint est choisi uniquement sur validation (2/16, 12,5 %). Le holdout final fraichement redige contient 32 exemples, quatre par facette : 9/32 exacts (28,125 %) contre 12,5 % attendu sous choix uniforme. Ce resultat reste exploratoire et ne demontre pas une classification robuste. Le candidat de fine-tuning conjoint a dégradé la modélisation linguistique hors échantillon; l'essai défavorable est conservé dans l'audit et n'est pas le checkpoint publié.

## 7. Préservation et conclusion

Le vérificateur de préservation montre 24/24 logits identiques sur les entrées fixes entre v3_0 et le chemin génératif v3_1. Le résultat démontre non-régression entre étudiants, pas une équivalence aux LLM sources. **Statut : étudiant tiny LM autonome exploratoire, intégration des deux sources validée, reconstruction mécaniste complète non démontrée.**
