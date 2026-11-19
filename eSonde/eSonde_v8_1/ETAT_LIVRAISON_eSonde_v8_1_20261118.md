# État de livraison eSonde v8.1 — 18 novembre 2026

## 1. Description

Cette livraison correspond au dernier état réellement présent dans l'espace de travail au 18 novembre 2026. Elle rassemble le runtime chat v8.1, les poids originaux, les bases statistiques agrégées, les formalismes v8.1, les tests et le dossier d'audit/suivi. Elle ne constitue pas une certification de cohérence générale ni une release stable.

## 2. Architecture

Le runtime de chat v8.1 est indépendant du verrou de phase historique v8. Il utilise le checkpoint eSonde v6 original de 1 000 000 Obsiss; les 16 observations nommées restent dans E_O et les états CountSketch P/R dans E_C, sans identification coordonnée par coordonnée. La fusion est réalisée au niveau des rangs candidats. Les composants conversationnels comprennent les profils OASST1, les priors de langue, le modèle de transitions bigrammes/trigrammes, l'index sémantique prompt-contexte et l'index de continuations conditionnées par prompt+préfixe. La non-réponse est désactivée par défaut. Aucun composant neuronal/MLP n'est déclaré ni importé par le runtime testé.

## 3. Pipeline complet

1. Charger le prompt et l'historique explicitement transmis.
2. Vérifier le registre portable, le manifeste et la copie SHA-identique du checkpoint.
3. Charger les poids originaux et les artefacts statistiques, vérifier leurs empreintes et intégrités SQLite.
4. Router la langue et construire les propositions initiales à partir du prompt.
5. Construire les 16 observations E_O pour chaque candidat, sans modifier les noms ni la cardinalité.
6. Calculer les états P/R dans E_C en conservant le couplage par Obsiss et traiter la population complète.
7. Fusionner les classements au niveau candidat, appliquer les preuves contextuelles et les pénalités de répétition avant sélection.
8. Ajouter le token choisi au préfixe et répéter jusqu'à max_tokens ou condition d'arrêt du runtime.
9. Écrire la réponse, les empreintes, les traces et les diagnostics.

## 4. Commandes d'exécution

Depuis le dossier `Dmodel_eSonde_v8_1` :

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements-accelerated.txt
./RUN_CLI_V81.sh status
./RUN_CLI_V81.sh verify
./RUN_CLI_V81.sh chat --prompt "Bonjour, comment vas-tu ?" --max-tokens 18 --beam-width 1 --candidate-limit 48 --p-activation-mode first_state --json-out runs_v8_1/bonjour.json
./RUN_GUI.sh
```

Windows : `RUN_CLI_V81.bat`, `RUN_GUI.bat` ou les scripts Python correspondants. La non-réponse n'est activée qu'avec `--allow-no-response`. La CLI et la GUI vérifient le snapshot local avant génération.

## 5. Résultats

### Logiciel et intégrité

- Dernière suite complète locale : **131 tests réussis, 0 échec, 25,91 s**.
- Trois formalismes TeX v8.1 compilent avec `pdflatex -halt-on-error` après correction de code inline et de variables E_O/E_C hors math. Cela valide la syntaxe de compilation, pas la démonstration mathématique.
- Checkpoint original SHA-256 : `8526943d1528418fa8bbbf9128b61b5e1acd90a16eeb7cc062e18864b083dff4`. Copie pré-exécution portable identique.
- Artefacts agrégés SHA-256 : profils `c517a0a5023add538d7588853652cc01cc7e5f3b305e404d34df6d35cc881544`; priors `8b769436d13b31ce9b8639720bf97a902b35bed82a17c7c4f713ad0739d15e91` [voir manifest JSON pour la valeur complète]; transitions `2729077b9703162997d8aff67d4779c3fed292b6f4598f615002d08741ddb455`; associations `b0c528011d3846eab2a57850732aa43821e3cfe82a454ed0d33a5930673c0aa4`; transitions conditionnelles `9c6e70735c4045c4497c7877998648943ac4ced77100c8b6560f309d2aa309dd`.
- Activation P première étape : 1 000 000/1 000 000 Obsiss en 2,071 s (expérience de référence).
- Évaluation R/P groupée : 8 candidats sur 1 000 000 Obsiss en 2,635 s (expérience de référence).

### Générations libres enregistrées

| Prompt | Réponse obtenue | Lecture du résultat |
|---|---|---|
| `Bonjour, comment vas-tu ?` | `Bonjour, c'est un élément dans l'eau, des styles de la vie.` | Génération complète, hors sujet.
| `Explain photosynthesis simply.` (contexte sémantique) | `Photosynthesis is one example is a simple example of the game is` | Continuité locale, dérive hors sujet.
| Même prompt (prompt+préfixe) | `Photosynthesis is one photosynthesis is one of the most happy.` | Boucle/répétition.
| Même prompt (confiance/répétition) | `Photosynthesis is one of many, but all the algae oxygen is` | Vocabulaire thématique, proposition non cohérente.
| Même prompt (profil hérité OFF) | `The. algae h2o, que es el` | Ouverture et alignement linguistique dégradés.

Les réponses ci-dessus sont techniquement produites sur 1 000 000 Obsiss aux décisions rapportées; leurs détails et hashes sont dans les JSON de suivi. La nouvelle politique `initial_only`, l'intention d'explication et l'alignement de langue ont passé 131 tests, mais aucune génération libre post-correctif n'est encore consignée.

## 6. Interprétation des résultats

Le classement groupé et l'activation complète sont désormais calculables avec une latence mesurée. La stabilité partitionnée des votes n'implique pas la pertinence du token. Les générations montrent que l'ouverture peut être liée au prompt, puis la continuation dérive vers des suites générales, des répétitions ou des termes associés sans proposition complète. L'ablation totale du profil historique supprime du bruit mais peut aussi dégrader le début et la langue; la politique `initial_only` teste un compromis et n'est pas encore évaluée en génération.

## 7. Conséquences

- **Théoriques :** distinguer la preuve prompt+préfixe de la fréquence linguistique générale; ne pas traiter des espaces E_C et E_O de même taille comme la même base.
- **Conceptuelles :** la cohérence exige de maintenir l'intention de dialogue sur toute la séquence; la pertinence d'un mot isolé ne suffit pas.
- **Opérationnelles :** optimiser la fusion des 16 observations et P/R, mesurer les ablations, conserver le million d'Obsiss et enregistrer les sorties libres. La CLI/GUI vérifie désormais une sauvegarde locale du checkpoint avant génération.

## 8. Conclusion

Le runtime v8.1, les bases agrégées et les artefacts documentaires sont présents dans cette livraison; les tests logiciels sont PASS. Les résultats de génération disponibles ne démontrent pas encore la cohérence recherchée. Aucun verdict d'impossibilité ou de réussite finale n'est posé.

## 9. Statut du modèle et prochaine étape

**Statut : prototype de chat v8.1 en développement expérimental; génération technique exécutée, cohérence et généralisation non validées.** P0 source reconciliation demeure en cours. Les formalismes, laboratoire et optimisation v8.1 sont créés et compilables, mais les cinq passes de revue sont incomplètes.

**Prochaine étape immédiate :** lancer sur le million d'Obsiss, non-réponse désactivée, deux prompts appariés (salutation française et explication anglaise) en politique `always` puis `initial_only`, avec même checkpoint et paramètres; enregistrer tous les tokens et les 16 canaux, comparer maintien du sujet, grammaticalité, langue et temps; ensuite figer les prompts paraphrasés held-out et tester la généralisation.

- Trois bases SQLite: `PRAGMA quick_check=ok` pour les trois artefacts livrés (vérifié au 18 novembre 2026).
