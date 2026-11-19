# Audit d'intégration runtime eSonde v8 — CLI, GUI, profil et préflight

**Révision :** 17 novembre 2026, après tests d'intégration v8  
**Périmètre :** inspection statique des points d'entrée, tests logiciels ciblés et préflight non génératif. Aucun tour de génération n'a été exécuté dans cette revue.

## 1. Description

L'objet de l'audit est de vérifier que les deux interfaces publiques entrent dans le même runtime v8, chargent le profil agrégé OASST1, appliquent la même règle de non-réponse désactivée par défaut et respectent le contrôle de phase v8.

## 2. Architecture et chemin d'exécution

- `RUN_CLI.py` délègue à `esonde_v8.cli.main`.
- `src/esonde_v8/cli.py` utilise `run_preflight` de `esonde_v8.preflight`, puis `EsondeV8ChatRuntime` et le profil `models/eSonde_v8/dialogue_profiles.json`.
- `RUN_GUI.py` construit également `EsondeV8ChatRuntime`, charge le même profil OASST1 et appelle le même préflight v8 avant d'envoyer un tour.
- Le CLI et la GUI transmettent `allow_non_response` avec valeur par défaut `False`; la GUI dispose d'une case décochée au démarrage.
- `EsondeV8ChatRuntime` délègue le moteur de propositions et Obsiss/P-R à `esonde_v7.generation.generate_chat`, en injectant le module v8 `esonde_v8.dialogue_learning`. Cette filiation est explicite et le moteur hérité n'est pas présenté comme une implémentation autonome nouvelle.

## 3. Vérifications

1. Recherche statique confirmée : `RUN_CLI.py` appelle le CLI v8; `RUN_GUI.py` importe `EsondeV8ChatRuntime`, le chemin de profil et `run_preflight` v8.
2. La GUI passe l'état du bouton non-réponse à `runtime.generate` et son `BooleanVar` est initialisé à `False`.
3. Le préflight lit les quatre contrôles v8, le manifeste du snapshot et le checkpoint original.
4. Depuis le Dmodel portable, `status` retourne `PASS`; 33 fichiers du savepoint sont validés (242 450 887 octets).
5. La commande `chat` retourne `PREFLIGHT_BLOCKED` avant d'instancier le générateur quand P0/P1/P2 ne sont pas terminées.
6. Les tests préflight testent tailles et SHA, fichier modifié, traversée de chemin et nombre de fichiers incohérent.

## 4. Résultats logiciels

La suite active (répertoire `tests/` seulement, avec `PYTHONPATH=src`) passe **66/66** tests. Cela comprend le profil chat v8, repli trigramme/bigramme/unigramme, neutralité de fusion sans signal, injection du module v8, et contrôle des manifestes de savepoint. La compilation des trois sources LaTeX v8 passe deux fois chacune avec `pdflatex -halt-on-error`.

## 5. Interprétation

Les problèmes signalés auparavant par NM-056 (profil absent de la GUI), NM-057/NM-061 (préflight v7), et V8-MODEL-GUI-001 sont obsolètes pour le code courant : ces éléments ont été raccordés et vérifiés. NM-062 est corrigé par la réécriture des guides et du statut de paquet.

NM-060 demeure partiellement ouvert : les points d'entrée v8 n'exposent que `everyday_dialogue`, ne chargent pas le profil numérique et ne fournissent pas les modes screenplay/question-answering; cependant, des branches historiques demeurent dans le fichier moteur V7 partagé. Elles ne sont pas activées par l'API v8 (`numeric_profile=None` et module dialogue v8 injecté). Leur retrait complet serait une refactorisation plus large qui doit préserver le comportement historique et être testée séparément.

Les 66 tests ne mesurent pas la cohérence des réponses. Le préflight réussi sur `status`/`verify` n'est pas une validation de génération.

## 6. Conséquences

- **Théorique :** l'absence de signal statistique du profil est traitée comme une identité sur les canaux hérités; un état statistique absent ne devient plus un rang artificiel.
- **Conceptuelle :** la couche v8 de dialogue agrégé ne doit pas être confondue avec le moteur Obsiss/P-R hérité ni avec une preuve de généralisation.
- **Opérationnelle :** le snapshot portable et le préflight vérifient maintenant tous les fichiers enregistrés dans le manifeste avant d'autoriser une commande non générative; le verrou de phase bloque encore le chat.

## 7. Conclusion et statut du modèle

Le raccordement CLI/GUI/préflight v8 est vérifié pour les fonctions administratives et la protection du chat. La génération libre n'a pas été lancée parce que P0, P1 et P2 restent incomplètes. Le statut de qualité dialogique demeure `NON_EVALUE`; aucun verdict positif ou négatif sur la cohérence ou la généralisation n'est tiré.
