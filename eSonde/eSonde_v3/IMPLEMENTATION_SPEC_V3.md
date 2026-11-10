# Spécification d'implémentation — eSonde v3

Version : 3.0.0  
Date : 10 novembre 2026  
Statut : architecture implémentée et groupes logiciels testés ; validation générale du langage encore ouverte.

## 1. Description et objectifs

Le runtime eSonde v3 prend du texte Unicode, construit un état causal multi-échelle, interroge sept familles explicites (`SEQ`, `SKIP_REL`, `MORPH`, `SEM`, `DISC`, `RETR`, `BYTE`) plus le coordonnateur `COORD`, puis calcule un mélange de distributions de continuation. L'objectif est un écosystème de modèle de langage généraliste à sondes explicites. Ce terme désigne l'objectif fonctionnel, non une qualité déjà démontrée.

## 2. Architecture exécutée

```text
Texte UTF-8
   │
   ▼
Tokenizer Unicode (v2 historique / v3 CJK-Hangul)
   │
   ▼
Contexte causal + mémoire de provenance
   ├── SEQ
   ├── SKIP_REL
   ├── MORPH
   ├── SEM
   ├── DISC
   ├── RETR
   └── BYTE (transitions UTF-8 BOS/EOS + backoff)
          │
          ▼
   distributions conditionnelles Q_f^LM
          │
          ▼
 COORD : mélange convexe normalisé sur familles disponibles
          │
          ├── scoring / calibration
          ├── proposition de candidats et génération
          └── état suivant + traces et provenance
```

Les unités d'état sont des tables, compteurs, index inversés, graphes relationnels et réservoirs bornés. Il n'existe aucun neurone, MLP, transformeur, embedding dense appris, attention Q/K/V ou couche dense de substitution.

## 3. Contrats probabilistes

Pour toute famille active `f`, le modèle expose une loi conditionnelle normalisée `Q_f^LM(y | h,M)` sur son espace de sorties déclaré. COORD forme `P(y|h,M)=Σ_f λ_f(h,M)Q_f^LM(y|h,M)`, avec `λ_f≥0` et somme égale à 1. Les familles sans support peuvent être exclues ou recevoir une masse de repli explicitement déclarée selon les règles du runtime. Les distributions de BYTE utilisées pour le scoring et l'échantillonnage partagent la même convention UTF-8 et la même loi de transition.

Les noyaux instrumentaux d'observation `Q_f^obs` évoqués par le formalisme d'observation ne sont pas substitués aux lois linguistiques `Q_f^LM`. Le noyau mécaniste conjoint sortie/état suivant reste un objet du formalisme théorique et n'est pas confondu avec l'indépendance supposée de deux marges.

## 4. Familles

| Famille | Opération | Représentation |
|---|---|---|
| SEQ | continuations locales exactes | compteurs de suffixes |
| SKIP_REL | motifs non contigus relatifs | compteurs d'offsets |
| MORPH | signatures de surface Unicode | tables de préfixes/suffixes/caractéristiques |
| SEM | cooccurrences et structures A–relation–B | graphes/postings creux |
| DISC | mentions, alias et indices discursifs | tables de mémoire/relations observées |
| RETR | récupération de contextes | index inversés avec provenance |
| BYTE | continuation ouverte d'octets UTF-8 | n-grammes d'octets avec BOS/EOS/backoff |
| COORD | mélange de réponses de sondes | poids sur simplex calibrés sur validation |

Aucune expérience tabulaire ou branche historique hybride RBF/CNG/CNC n'est incorporée en tant que couche du moteur v3.

## 5. Cycle de vie

- **Entraînement :** construire chaque structure à partir des seules données train et conserver un registre de lots et hashes.
- **Calibration :** ajuster COORD sur validation disjointe ; ne pas toucher aux structures de train.
- **Inférence :** former le contexte causal, interroger les familles, mélanger les lois, sélectionner/échantillonner et mettre à jour le contexte.
- **BYTE :** traiter les chaînes en UTF-8 ; BOS/EOS et backoff empêchent qu'un OOV soit une classe unique. Le beam sert à proposer des chaînes, pas à remplacer le score exact des chaînes candidates.
- **Évaluation :** corpus test strictement disjoint ; fournir NLL, perplexité, top-k, OOV, par langue/document, troncature de contexte.
- **Persistance :** JSON canonique avec SHA du payload et sidecar SHA du fichier ; sauvegarde atomique.
- **Migration v2 :** les anciens checkpoints restent au tokenizer v2 ; poids BYTE par défaut nul ; fichiers d'origine préservés.
- **Retrait de lot :** rejeu du registre de lots conservés ; checkpoints v2 sans historique complet refusent l'opération.

## 6. Interfaces

Les commandes CLI sont répertoriées dans `CLI_GUIDE.md`. Le GUI Tkinter appelle le même `ProbeModel` ; ses actions sont décrites dans `GUI_GUIDE.md`. Le runtime CLI utilise seulement la bibliothèque standard Python, Python 3.10+ ; Tkinter est requis pour le GUI.

## 7. Invariants et tests

Les tests contrôlent normalisation, OOV, sérialisation, migration, tokenizer, lots, séparation train/validation/test, COREF/SEM/DISC, CLI, worker GUI et audit AST de pureté. Les résultats exacts sont consignés dans `VALIDATION_V3.md` et les journaux Amodel/suivi. Aucun test unitaire ne remplace un benchmark linguistique représentatif.

## 8. Statut et limites de preuve

Les groupes de tests ont des résultats passés sur les scénarios consignés. Le checkpoint actif reste entraîné sur 415 tokens de démonstration. Le diagnostic MLQA porte sur un échantillon next-token de 56 paragraphes / 4 055 tokens et n'est pas le score officiel QA. L'absence de split train dans MLQA fourni interdit d'utiliser dev/test comme apprentissage. La couverture généraliste exige un corpus d'entraînement indépendant, des validations représentatives et des évaluations QA/génération pré-enregistrées ; leur absence actuelle n'est pas interprétée comme une impossibilité architecturale.
