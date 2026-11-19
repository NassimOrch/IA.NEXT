# Rapport V81-PROMPT-CONTEXT-SEMANTIC-001

Date : 18 novembre 2026  
Statut : intégration logicielle et diagnostic statistique validés ; génération libre multi-token avec ce mécanisme encore à exécuter.

## 1. Description

Le diagnostic V81-MODEL-GEN-006 a montré qu'une génération libre pouvait choisir un premier token correspondant au prompt, puis perdre cette pertinence aux étapes suivantes. Les signaux prompt-conditionnés étaient actifs au démarrage seulement ; les étapes suivantes étaient essentiellement pilotées par les transitions linguistiques générales.

Cette expérience ajoute une statistique agrégée TRAIN-only qui relie des ancres thématiques du prompt à des termes sémantiques présents dans les réponses assistant associées. Elle ne stocke aucune phrase, aucun prompt/réponse brut et aucun identifiant de message ou d'arbre.

## 2. Architecture

- Source : OASST1, liens parent `prompter` / enfant `assistant`, split officiel TRAIN seulement.
- Modèle de base : `response_language_model_v81.sqlite`, schéma v2.
- Nouvel artefact : `prompt_context_associations_v81.sqlite`, schéma `esonde.v8_1.oasst1.prompt_context_semantics.v1`.
- Tables : `prompt_anchor_response_semantics`, `prompt_anchor_selected_df`, `response_semantic_selected_df`, `language_totals`, `model_meta`.
- Unité de compte : présence d'un terme sémantique sélectionné dans une réponse assistant associée à une ancre du prompt, comptée une fois par paire/ancre/terme.
- Scoring : deux ancres thématiques TRAIN les plus informatives au plus ; fréquence d'arête répétée ; fréquence documentaire indépendante ; log-lift lissé Beta ; réduction par support.
- Fusion : classement de l'évidence seulement sur le canal Obsiss existant `prompt_association`. Aucune 17e dimension n'est ajoutée. Les propositions candidates ne sont pas injectées directement par cet index.
- Séquentialité : reste assurée par le modèle séparé de bigrammes/trigrammes OASST1.
- Espace Obsiss : reste composé des 16 observations d'origine. Le million d'Obsiss et les poids originaux restent inchangés.

## 3. Pipeline complet

1. Charger le Parquet TRAIN et le modèle de transitions déjà vérifié.
2. Énumérer les couples parent utilisateur / enfant assistant, en excluant les paires sans relation valide ou de langue incohérente.
3. Extraire les ancres lexicales du prompt et les termes sémantiques de la réponse avec le tokenizer eSonde existant.
4. Sélectionner les ancres et termes selon les fréquences documentaires TRAIN ; compter les cooccurrences agrégées.
5. Vérifier l'intégrité SQLite, la provenance TRAIN, les indicateurs d'absence de texte brut/IDs et l'absence de composant neuronal.
6. À l'inférence, détecter la langue sur le prompt courant, calculer une fois les scores prompt-termes, puis retirer les termes déjà produits du signal restant.
7. Pour chaque pool candidat déjà produit par le moteur, fusionner le classement du signal contextuel dans le canal `prompt_association` existant.
8. Faire voter les Obsiss à partir des 16 observations et du score P/R de même ligne.

## 4. Commandes d'exécution

Construction :

```bash
PYTHONPATH=src python experiments/build_oasst1_prompt_context_semantics_v81.py \
  --source-train /mnt/data/esonde_audit/source/dataset/datasets--OpenAssistant--oasst1/snapshots/fdf72ae0827c1cda404aff25b6603abec9e3399b/data/train-00000-of-00001-b42a775f407cee45.parquet \
  --priors models/eSonde_v8/response_language_priors.json \
  --base-db models/eSonde_v8/response_language_model_v81.sqlite \
  --output models/eSonde_v8/prompt_context_associations_v81.sqlite
```

Tests :

```bash
PYTHONPATH=src pytest -q
```

La commande de génération intégrée doit être exécutée uniquement après validation d'un savepoint incluant le runtime, la nouvelle base, les checklists et les preuves.

## 5. Résultats

- Build fini en 29,62 secondes.
- 1 864 714 arêtes agrégées prompt-ancre / terme de réponse.
- 31 133 lignes d'ancres sélectionnées.
- 201 966 lignes de fréquences documentaires de termes sémantiques.
- 23 langues déclarées dans le manifeste de base ; nombre de paires effectives varie selon langue.
- Base SQLite : 112 214 016 octets ; SHA-256 `b0c528011d3846eab2a57850732aa43821e3cfe82a454ed0d33a5930673c0aa4`.
- `PRAGMA integrity_check = ok`.
- Métadonnées : `source_split=official_train_parquet_only`, flags raw text/pairs/IDs `false`, `neural_components=[]`.
- Le premier score exploratoire était trop bruité : il faisait remonter des tokens rares parasites pour `photosynthesis`.
- Après durcissement : pour `Explain photosynthesis simply`, seule l'ancre thématique `photosynthesis` est utilisée ; `chlorophyll`, `algae`, `pigment` ressortent en tête ; `firefighters` et `qobject` sont rejetés.
- Pour `Hello, how are you?`, le score thématique est vide : le signal de salutation reste réservé au modèle de réponse et aux observations de dialogue.
- Le corpus français fourni ne dispose pas de support thématique suffisant pour une requête photosynthèse en français ; aucun signal anglais n'est substitué.
- Tests ciblés de cette nouvelle intégration : 4 réussis.
- Suite complète après intégration : 111 tests réussis, 0 échec, 22,77 secondes.

## 6. Interprétation

Le nouvel index fournit un signal thématique de réponse multi-position plus propre dans le cas anglais examiné. Le filtrage des ancres de discours/greeting et le contrôle des fréquences documentaires évitent que des marqueurs de forme de demande ou des termes singleton ne deviennent des thèmes.

Le résultat ne démontre pas encore une amélioration de la génération complète. La fusion est implémentée mais une campagne multi-token sur le million d'Obsiss doit comparer le même ensemble de prompts avec l'index actif et désactivé. Le signal est volontairement limité à la pertinence lexicale ; il ne fournit pas l'ordre de phrase.

## 7. Conséquences

### Théoriques

Une association prompt-réponse peut être utilisée comme un signal d'observation contextuel distinct des probabilités de transition. Elle demeure un support empirique et ne constitue pas à elle seule une théorie de composition syntaxique.

### Conceptuelles

La dimension `prompt_association` prend un rôle plus explicite : elle mesure désormais aussi la cohérence entre le sujet du prompt et les tokens candidats issus des autres mécanismes. Les dimensions originales sont conservées.

### Opérationnelles

Le coût d'interrogation est borné à deux ancres et 512 arêtes par ancre ; les scores sont calculés une fois par tour et filtrés par le préfixe courant. Le nouvel index est lu en mode SQLite immuable.

## 8. Incidents et limites de cette campagne

Deux constructions exploratoires antérieures ont été interrompues par le délai d'exécution : un index prompt×préfixe lexical (8 482 363 clés, total des occurrences incomplet) et un index d'associations sémantiques trop large (6 438 250 arêtes, métadonnées finales absentes). Les fichiers partiels ont été préservés dans `sav_eSonde_v8_1/incidents/`, vérifiés par SHA-256 et SQLite quand possible, mais ne sont pas utilisés par le runtime. Le build final plus compact décrit ci-dessus est complet et intègre une vérification d'intégrité.

## 9. Conclusion et statut

Le nouvel artefact et sa fusion logicielle dans l'observation existante `prompt_association` sont implémentés ; les tests logiciels sont verts. Le statut d'évaluation de la génération est encore ouvert. Le prochain test est une génération multi-token libre, toutes les Obsiss actives, non-réponse désactivée, puis une comparaison OFF/ON et des paraphrases held-out. Aucun résultat de généralisation ou de supériorité n'est revendiqué à ce stade.
