# EX11 — rapport de recherche et récupération des artefacts

Date de contrôle : 2026-11-03 (UTC+01:00)

## Périmètre examiné

Recherche en lecture seule dans les racines accessibles du conteneur : `/mnt/data`, `/tmp`, `/var/tmp`, `/home/oai`, `/root`, `/run`, `/openai`, puis recherche transversale dans le système de fichiers visible (sans `/proc`, `/sys`, `/dev` et sans les répertoires système massifs). Recherche par noms (`EX11`, `prompt_ex11`, `Replica`, `CNG`, `CNC`, résultats, métriques, checkpoints, manifests, partitions) et par contenus textuels distinctifs (`v1.1.4`, `C_SHARED`, `C_SEQ`, valeurs de validation précédemment annoncées).

## Artefacts trouvés

- Entrées utilisateur présentes dans `/mnt/data` : `last_sources_3.zip`, `datasets_arff.zip`, `rapport_analyse_ex3_ex10.tex` et son PDF.
- Sources de travail temporaires présentes dans `/tmp/ex11_audit` : copies de `Replica_U_0.tex`, `th_sondes_core_test_0.tex`, `th_sondes_core_test_1.tex`, prompts EX3 à EX9, rapports EX9/EX10, ainsi que les archives imbriquées EX4 à EX10 et `sources_ng_adapt_0.zip`.
- Répertoire `/mnt/data/EX11` présent. Au début du contrôle, il ne contenait qu'un `README_EX11.md` de zéro octet.

## Résultats négatifs de la recherche

Aucun fichier `prompt_ex11.json`, script d'entraînement EX11, manifeste des 95 partitions, checkpoint, prédiction, métrique ou journal CNG/CNC/REPLICA correspondant aux runs annoncés précédemment n'a été trouvé dans les emplacements accessibles.

Aucun processus d'entraînement EX11 n'était actif. Aucun descripteur de processus visible ne pointait vers un fichier EX11 supprimé mais encore ouvert. L'historique IPython local ne contient pas de session de travail pertinente.

## Limite de récupération de fichiers supprimés

Le système de fichiers visible est un overlay. Le chemin `upperdir` indiqué par le montage n'est pas accessible dans le namespace du conteneur. Aucun périphérique bloc ni snapshot de sauvegarde n'est exposé. Les outils de récupération bas niveau ne peuvent donc pas accéder aux blocs sous-jacents. En conséquence, il n'est pas possible de restaurer ici un fichier réellement supprimé. Cette impossibilité ne permet pas de conclure qu'un fichier a été supprimé : il peut aussi ne jamais avoir été persisté dans le workspace.

## Intégrité des entrées

- `last_sources_3.zip` : SHA-256 `7fe025ea6adc6581843f6cd8d776eb7399bb5f6849dc53da755a1324beb243c4`; `unzip -t` : OK, aucune erreur CRC.
- `datasets_arff.zip` : SHA-256 `a2c5feb334d622fe5197a1a0a8621c5b286947b0693bc05955b990597e44f041`; `unzip -t` : OK, aucune erreur CRC.
- `rapport_analyse_ex3_ex10.tex` : SHA-256 `d176d4d0fa8a7b8c767bb475286910d912adc3559f16d5bfd2a231e5428406f4`.
- `rapport_analyse_ex3_ex10.pdf` : SHA-256 `b9c70e39dea070b84cb4eee87381394d637edbf1995f6ab88c40b3131691ba61`.

## Conclusion opérationnelle

Les sources d'entrée et les datasets sont intacts dans l'environnement courant. Les artefacts EX11 annoncés antérieurement ne sont pas récupérables depuis les répertoires accessibles ; aucun résultat expérimental n'est donc certifiable sur la seule base de ces annonces. Toute reconstruction ou nouvelle exécution doit être créée dans ce workspace, avec nouveaux `run_id`, scripts, journaux, checkpoints et hashes, et doit être distinguée explicitement des résultats historiques non vérifiables.
