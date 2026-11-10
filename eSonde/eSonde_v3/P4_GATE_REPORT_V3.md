# Rapport de phase P4 v3 — corpus et diagnostic linguistique multilingue

**Phase :** P4 — données, fuite et mesure linguistique  
**Statut :** PASS_WITH_DOCUMENTED_DATA_LIMITATION

## 1. Description

P4 contrôle la disponibilité et les droits des données, la séparation train/validation/test et la capacité du runtime BYTE/COORD à calculer une vraisemblance next-token sur plusieurs scripts/langues.

## 2. Architecture

Checkpoint `esonde_v3_demo_checkpoint.json` : tokenizer 3, sept familles plus COORD. Données train : huit textes de démonstration / 415 tokens. Validation : deux textes / 80 cibles. MLQA n'est pas utilisé pour entraîner ou calibrer.

## 3. Pipeline complet

1. Inventorier MLQA_V1 : 49 fichiers dev, 49 test, aucune partition train ; licence CC BY-SA 3.0.
2. Choisir huit paragraphes déterministes par langue sur le split test ; calculer leurs identifiants et SHA.
3. Vérifier l'absence de chevauchement exact des titres dev/test dans l'échantillon retenu.
4. Calculer NLL et diagnostics OOV pour COORD, BYTE-only et ablation sans BYTE.
5. Comparer uniquement les sorties partageant un espace d'événements comparable ; signaler la baseline OOV unique comme non comparable.

## 4. Commandes d'exécution

```bash
PYTHONPATH=src python scripts/evaluate_mlqa_next_token.py \
  --model models/esonde_v3_demo_checkpoint.json \
  --mlqa-zip /chemin/indépendant/MLQA_V1.zip \
  --output results/p4_mlqa_test_next_token.json \
  --paragraphs-per-language 8
```

Le dataset original n'est pas présent dans Dmodel ; le résultat JSON sélectionné est conservé. Il n'est pas nécessaire de redistribuer MLQA pour exécuter le runtime.

## 5. Résultats

| Mesure | Résultat |
|---|---:|
| Langues | 7 (ar, de, en, es, hi, vi, zh) |
| Paragraphes | 56 |
| Tokens | 4 055 |
| Taux OOV | 86,56 % (3 510 tokens) |
| NLL COORD | 31,3662 nats/token |
| NLL sans BYTE | 598,4486 nats/token |
| NLL BYTE-only | 30,8303 nats/token |
| Perplexité COORD | 4,1895 × 10^13 |
| Baseline unigramme OOV fusionné | 6,2438 nats/token, non comparable |

Zéro token OOV de l'échantillon n'a été classé « zéro ou trop long » par BYTE. Resultat complet : `results/p4_mlqa_test_next_token.json`.

## 6. Interprétation

Le score sans BYTE s'effondre pour les chaînes OOV ; BYTE ramène la NLL à une valeur finie et nettement plus basse. Toutefois, la NLL absolue demeure très élevée. La perplexité est très importante. L'unigramme avec bucket OOV unique regroupe toutes les chaînes inconnues, donc n'évalue pas le même événement. MLQA est ici un diagnostic next-token context+question, pas le benchmark officiel EM/F1.

## 7. Conséquences

- **Théoriques :** la loi UTF-8 de BYTE donne une probabilité aux chaînes qui ne sont pas dans le lexique appris.
- **Conceptuelles :** couverture d'une chaîne OOV et bonne prédiction de son contenu sont deux notions distinctes.
- **Opérationnelles :** les splits sont séparés ; absence de train MLQA implique qu'un vrai pré-entraînement multilingue ne peut pas être construit depuis ces partitions.

## 8. Conclusion

Les audits de licence/splits et la campagne diagnostique déterministe sont réalisés. La limitation du corpus d'entraînement est documentée et ne peut pas être « contournée » en réutilisant dev/test sans fuite.

## 9. Statut du modèle

P4 fermée pour l'audit des données et le diagnostic déclaré. Le modèle actif est un checkpoint de démonstration, pas un modèle généraliste validé. Son potentiel n'est ni fixé ni déclaré impossible par ces mesures.
