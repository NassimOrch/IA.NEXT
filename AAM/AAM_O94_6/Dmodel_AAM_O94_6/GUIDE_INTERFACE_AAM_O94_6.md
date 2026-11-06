# Guide complet de l'interface graphique AAM O94.6

Ce guide décrit l'interface présente dans `aam_o93/ui.py`. Selon l'OS, les outils installés, les permissions et le type de données, certains contrôles peuvent afficher `PARTIAL`, `UNRESOLVED`, `BLOCKED` ou des diagnostics de dépendance. Ces statuts ne doivent pas être interprétés comme un succès complet.

## 1. Démarrer AAM et vérifier son état

Depuis la racine du projet extrait :

```bash
python scripts/preflight_o946.py
```

Le préflight doit se terminer par `PASS_BOUNDED`. Lancez ensuite :

- Linux/macOS : `./run_AAM_O94_6.sh`
- Windows CMD : `run_AAM_O94_6.bat`
- Windows PowerShell : `./run_AAM_O94_6.ps1`
- Alternative : `python -m aam_o93 --workspace <dossier-de-travail> gui`

Conservez le workspace dans un dossier local où vous avez les droits d'écriture. Les sources RAG, mémoires, compétences apprises, paramètres et traces d'observation sont stockés dans ce workspace; le programme ne devrait pas être exécuté depuis un répertoire système en lecture seule.

Le démarrage lance la boucle autonome. Le bouton `Fermer AAM` ferme le runtime après checkpoint; `Arrêter la boucle (AAM reste ouvert)` arrête seulement l'autonomie, et `Redémarrer la boucle` la relance. L'arrêt autonome n'est pas identique à la fermeture complète de l'application.

## 2. Chat

### Panneau de discussions

- **＋ Nouvelle** : crée une discussion.
- **Renommer** : change son titre.
- Liste de discussions : rouvre une session enregistrée.
- **Sources de la discussion** : montre les sources liées à la discussion.
- **Ouvrir Sources / RAG** : sélectionne l'onglet des documents et de leur ingestion.

### Contrôles de requête

- **Mode** : choisit l'orchestration générale (par exemple `auto`/`chat` selon les options de la version).
- **Compétence** : force une compétence répertoriée si l'utilisateur veut tester son chemin plutôt que la sélection automatique.
- **Politique RAG** : choisit comment les documents locaux sont consultés (`observe_first`, `lexical`, `auto`, `off`, selon les valeurs proposées par le runtime).
- **Générateur / mode** : choisit le modèle intégré ou la voie extractive/diagnostique.
- **Actualiser les modèles** : recharge la liste depuis le registre; après avoir ajouté un backend, utilisez-le avant de le choisir.
- **Focus IDs** : identifiants de mémoire séparés par des virgules. Ne mettez que des identifiants visibles/valides.
- **Pièce jointe / Parcourir… / Joindre un fichier…** : fournit un fichier à la requête. Les informations extraites peuvent être injectées comme contexte éphémère; l'ingestion persistante dans RAG est une action distincte.
- **Espace AAM alternatif / Choisir…** : raccorde un workspace AAM existant comme backend alternatif; cela ne convertit pas automatiquement une archive arbitraire en runtime.
- **Profondeur mémoire** : 1 à 4. La profondeur plus élevée élargit la consultation (résumés/empreintes, événements, parents causaux, voisins temporels) et augmente le coût.
- **Effacer la demande** : vide la saisie, pas l'historique.
- **Détails** : montre sources, statuts, routes, événements et diagnostics pour la dernière tâche.
- **Envoyer / répondre** : lance le pipeline; la zone de conversation attend le résultat asynchrone.
- **Enregistrer la note** : note la réponse comme retour utilisateur. La satisfaction influence une préférence/fiabilité, mais n'est pas une preuve indépendante que la réponse est vraie.

Les réponses de modèle sont marquées `GENERATED_UNVERIFIED` tant qu'un contrôle indépendant ne les vérifie pas. Les citations prouvent l'origine du contexte, pas automatiquement la vérité de la conclusion.

### Actions rapides dans le chat

Le menu d'actions rapides contient les raccourcis pour observer un fichier/objet, sélectionner une compétence, démarrer une résolution continue, régler le focus et effectuer une recherche Web. Les actions réseau dépendent des autorisations configurées; AAM ne doit pas contourner les droits du système ou d'un site distant.

### Bonne pratique

Décrivez une tâche à la fois, indiquez les contraintes utiles et demandez les sources. Pour trois questions indépendantes ou coordonnées, AAM O94.6 essaie de générer une sous-tâche par question; vérifiez que chacune dispose de sa réponse et de sa source. Si la réponse est vide ou `UNRESOLVED`, cliquez sur **Détails** plutôt que de supposer qu'une réponse a été produite.

## 3. Observer

L'onglet contient trois voies distinctes : observation live passive, observation d'instantané/outillée et black-box d'entrées/sorties. Elles ne sont pas interchangeables.

### 3.1 Observation live d'une source système

1. Sélectionnez **Niveau** :
   - `filesystem` observe les créations/modifications/suppressions dans un dossier;
   - `process` suit un PID (état, fichiers ouverts, sockets lorsque `psutil` est disponible et autorisé);
   - `network` capture l'activité réseau visible de l'interface par `tshark`.
2. Choisissez **Dossier à observer**, **PID processus**, ou **Interface réseau**, selon le niveau.
3. Si nécessaire, utilisez **Lister PID…** ou **Lister interfaces**.
4. Le **Filtre BPF facultatif** précise le trafic à capturer; une erreur de syntaxe de filtre doit être examinée.
5. Choisissez un **Dossier des traces produites**. Gardez les traces en dehors des dossiers source à observer si vous ne voulez pas que le captureur observe ses propres journaux.
6. Réglez le budget/maxima fournis par le panneau. Cochez seulement si nécessaire :
   - contenu brut des fichiers ajoutés/modifiés;
   - charges utiles TCP/UDP décodées en JSONL (peuvent contenir des données sensibles);
   - capture PCAPNG brute via `dumpcap`.
7. Cliquez **DÉMARRER OBSERVATION** et vérifiez le numéro de session et son état.
8. Effectuez le processus autorisé sur le système cible.
9. Cliquez **Arrêter / finaliser**. AAM écrit les traces et le reçu, et affiche la dernière trace créée.
10. **Apprendre les briques de cette trace** produit des candidats à examiner; il ne constitue pas à lui seul une validation de compétence.

Limites de permission : PID n'accorde pas de droits qui ne sont pas accordés à l'utilisateur. Le panneau n'annonce pas une lecture universelle de la mémoire privée d'un processus; TLS reste chiffré si aucun contenu déchiffré n'est légalement/techniquement disponible.

### 3.2 Instantané et outils réels OCR/PDF/audio/vidéo

1. Utilisez **Choisir fichier/dossier** pour sélectionner une entrée que vous avez le droit d'inspecter.
2. **Inspecter un instantané (empreintes)** mesure structure, hashes et vues disponibles sans exécuter le fichier.
3. **Observer avec outils réels (OCR/PDF/audio/vidéo)** appelle les utilitaires disponibles, par exemple Tesseract pour OCR, Poppler pour PDF, FFmpeg/FFprobe pour audio/vidéo.
4. Vérifiez le statut du décodeur, la présence de la sortie, les logs stderr et le SHA-256. `PASS_BOUNDED` ne signifie pas que toutes les modalités ont été décodées intégralement.
5. Le texte extrait peut être indexé dans RAG lorsque l'action/le réglage le permet; le fichier original n'est pas réécrit.

### 3.3 Capture boîte noire par lots

Cette voie est conçue pour une cible autorisée qui peut être interrogée avec des entrées indépendantes.

1. Choisissez un fichier `JSON`, `JSONL`, `NDJSON`, `CSV` ou `TSV` via **Choisir source…**.
2. Renseignez le workspace de la cible, la commande en `argv JSON` (tableau d'arguments, sans shell), les clés d'entrée/cible/split, le nombre maximal de cas, le budget par cas et le budget global, puis le chemin de trace I/O.
3. Vérifiez qu'aucun oracle d'évaluation n'est placé dans les colonnes accessibles à la capsule entraînée.
4. Cliquez **Capturer le lot (autorisation)**. AAM lance la cible comme processus externe et enregistre entrées/sorties réellement observées.
5. **Apprendre une capsule hors source** crée un objet de rejeu à partir des observations conservées.
6. Gardez des cas `train` et des cas `test` exclus. Les cas cachés doivent être évalués par une commande séparée après capture.

### 3.4 Cible JSONL persistante

La cible reste active, lit un objet JSON par ligne sur `stdin` et retourne exactement une réponse par ligne sur `stdout`. `stderr` est archivé séparément, et n'est jamais traité comme une réponse. Démarrez/autorisez la cible, envoyez quelques sondes, générerez des sondes automatiquement si utile, puis arrêtez la trace.

### 3.5 Caméra

Choisissez explicitement le périphérique et confirmez la capture. AAM ne doit pas accéder à une caméra sans consentement. Vérifiez que l'environnement possède les permissions et drivers nécessaires.

## 4. RAG / Sources

Le flux recommandé est :

1. charger ou choisir les fichiers/dossier;
2. examiner la liste des sources et leurs hashes;
3. choisir la politique d'observation/recherche;
4. lancer l'observation et l'ingestion;
5. inspecter les sorties/extraits;
6. rechercher quelques questions connues et quelques questions sans réponse dans le corpus;
7. vérifier pour chaque question la pertinence de l'entité, du passage et de la citation;
8. seulement ensuite décider de reconstruire l'espace RAG ou de supprimer les espaces intermédiaires.

- `observe_first` met l'observation en amont de la recherche.
- `lexical` emploie une recherche lexicale; utile pour codes/identifiants exacts.
- `auto` laisse le routeur choisir selon la configuration et les routes enregistrées.
- `off` désactive la récupération dans les cas où le runtime l'autorise.
- **Recharger/reconstruire l'espace** relance la construction sémantique; pour un corpus important, sauvegardez les reçus et comptez le temps.
- **Inspecter/supprimer espaces** : supprimez des espaces intermédiaires seulement après avoir vérifié l'espace final, les IDs et les sources de référence.
- **Nettoyer** enlève les intermédiaires conservés par le processus.
- **Mettre à jour** incorpore les nouveaux fichiers.
- **Extraire des compétences** crée des candidats, qu'il faut tester avant enregistrement/usage.

AAM ne doit pas citer un passage faible simplement parce que le RAG a donné un résultat. Si une question cite un identifiant (ex. GB-42), vérifiez qu'une réponse extraite concerne bien cette entité. Pour un identifiant absent, attendez-vous à `UNRESOLVED` plutôt qu'une réponse sur le voisin le plus proche.

## 5. Sondes

- **Créer une sonde** : définir l'observation/transformations à évaluer.
- **Charger / modifier / enregistrer** : manipuler une définition persistante de sonde.
- **Moteur adaptatif** : demander la génération de variantes et examiner leurs différences, au lieu d'accepter des sondes identiques.
- **Tester la sonde** : exécuter une sonde contre une source autorisée.
- **Tester l'ensemble** : vérifier les interactions de plusieurs sondes et regarder les vues/empreintes.
- **Politique d'empreinte** : définir la représentation et les variantes extraites. Changez-la seulement en gardant un reçu et un test de régression.

Une empreinte est un résumé calculé de ce qui a été observé, pas une preuve de compréhension totale. Garder les sources, les vues, le hash et le statut de décodage permet d'évaluer ce qu'elle représente réellement.

## 6. Compétences

Le catalogue présente les compétences répertoriées, leurs descriptions et statuts. Choisissez une compétence, passez une entrée JSON et examinez la réponse/trace. Les actions usuelles permettent d'inspecter, ajouter, modifier, supprimer, charger, tester et valider.

La composition de compétences peut définir une séquence, des conditions et des sorties nommées. Testez les branches qui passent et celles qui échouent, pas uniquement le cas nominal.

L'acquisition supervisée prend en charge les cibles structurées définies par les colonnes/chemins d'entrée et de sortie disponibles. Un PDF ou une image peut être observé/indexé, mais ne contient pas automatiquement une étiquette cible correcte pour l'apprentissage supervisé. Les compétences candidates restent à tester et ne doivent pas devenir « validées » par le seul fait qu'elles ont été extraites.

## 7. Briques de base

Le catalogue distingue compétence, méthode et règle de base. **Actualiser le catalogue** recharge les définitions. Les catégories sont conceptuellement différentes :

- compétence : capacité opérationnelle d'entrée/sortie;
- méthode : procédure ou stratégie de résolution;
- règle : invariant, contrainte ou condition de branchement.

Consultez le code et les tests de la brique avant d'utiliser celle-ci dans un système d'entreprise. L'appartenance au catalogue n'implique pas une validation universelle sur toutes les données.

## 8. Observation / Mémoire / Autonomie

- **Enregistrer la mémoire de raisonnement** active/désactive l'enregistrement des événements de raisonnement; la désactivation ne stoppe pas automatiquement toute l'autonomie.
- **Auto-observer maintenant** déclenche une observation ponctuelle de l'état et des événements accessibles.
- **Lister les mémoires** montre l'inventaire disponible.
- **Lire le journal causal** expose les événements et leur chaîne d'intégrité.
- **Arrêter la boucle (AAM reste ouvert)** stoppe les actions autonomes.
- **Redémarrer la boucle** relance cette boucle.
- **Actualiser événements** recharge les événements mémorisés.
- **Résolution de mémoire** choisit le contexte, les indices et une profondeur de 1 à 4 : résumé/empreinte; événements sélectionnés; parents causaux; voisins temporels.

`prev_hash` sert à vérifier l'intégrité de la chaîne; `parent_event_hashes` indique les relations causales déclarées entre événements métier. Un lien causal consigné n'est pas une preuve scientifique qu'un mécanisme psychologique général est apparu.

## 9. Entraînement et acquisition

1. Choisissez le dataset/fichier/dossier.
2. Sélectionnez mode supervisé/non supervisé, clés/chemins d'entrée et de cible, split, epochs et seed.
3. **Inspecter dataset** pour connaître format, structure et erreurs de décodage.
4. **Ajouter au RAG** pour indexer les données; cette action n'entraîne pas à elle seule les poids du modèle de langage.
5. **Lancer RAG** et régler sa politique si nécessaire.
6. **Lancer acquisition** pour entraîner/créer un candidat de compétence dans les modalités prises en charge.
7. Pour un générateur de langage, utilisez l'action distincte d'entraînement du générateur et vérifiez la compatibilité du framework, les jeux d'entraînement et de validation, et les poids exportés.
8. Pause/reprise/arrêt : contrôlez état et checkpoint, attendez le statut terminal et vérifiez qu'un fichier de checkpoint ne soit pas le seul indice d'une pause correctement achevée.

Les paramètres de ce module ne transforment pas automatiquement un fichier arbitraire en dataset entraînable et n'infèrent pas les labels manquants.

## 10. Internet / API

Cet onglet regroupe recherche Web, paramètres de permission, hôtes approuvés, métadonnées MCP/API et configuration réseau. Les permissions réseau sont explicites; sans autorisation, le comportement doit rester local. La présence d'un formulaire de connexion ou d'une fiche MCP/API n'implique pas que tous les protocoles distants soient exécutables automatiquement dans cette version. Vérifiez la documentation du connecteur concret.

## 11. Modèles locaux / PyTorch

1. Inscrivez un identifiant/backend et choisissez le dossier modèle ou le fichier de poids.
2. Pour Transformers, le dossier doit comporter un modèle/configuration/tokenizer compatibles, ou le fichier de poids accompagné de ses artefacts de configuration/tokenizer nécessaires. Un fichier `model.safetensors` isolé n'identifie pas à lui seul l'architecture, la tokenisation, la taille de contexte ni la procédure d'entraînement.
3. Choisissez la politique : `inference_only`, export des paires supervisées, LoRA/Transformers si dépendances et modules cibles sont compatibles, ou adaptateur local personnalisé.
4. Le code local personnalisé doit être explicitement approuvé et son SHA-256 épinglé; il s'exécute comme l'utilisateur. N'exécutez pas un adaptateur de provenance inconnue.
5. Enregistrez, actualisez la liste dans le Chat et testez la génération.
6. Pour entraîner, sélectionnez un dataset, les champs entrée/cible, le dossier de sortie et les modules cibles; vérifiez l'évaluation post-entraînement.

**SmolLM2-360M :** les poids utilisateur n'étaient pas présents dans l'environnement d'audit O94.6 et Transformers n'a pas pu être installé via l'index réseau dans cette session. Les tests ont validé le contrat de l'adaptateur et la gestion d'erreur, pas l'inférence réelle de ces poids. Utilisez les sorties détaillées pour distinguer `backend ready`, `registered` et `generated with actual weights`.

## 12. Programmation par composition

L'onglet a deux sous-surfaces : `Graphe de compétences` (composition des compétences) et `Compilateur de programmes réels` (DSL JSON vers Python + bytecode). Le second peut compiler un projet, tester les fichiers, produire un manifeste d'intégrité et exécuter après confirmation. `Ouvrir Atelier de Code` lance l'éditeur multi-fichiers. Voir `GUIDE_PROGRAMMATION_COMPOSITIONNELLE_O94_6.md` pour le graphe, les briques, les commandes et le résultat réel.

La composition autorise seulement le catalogue de composants prévu par le DSL. L'atelier peut exécuter un projet existant avec les privilèges de l'utilisateur; ce n'est pas un environnement d'exécution isolé.

## 13. Réglages généraux

- nombre de sondes (auto ou manuel);
- politique de génération des sondes;
- politique d'empreinte;
- focus de mémoire et d'identifiants de sources;
- facteur de cadence autonomie (0,25 à 4 selon le contrôle);
- paramètres d'entraînement (epochs, seed, type de tâche);
- boutons d'enregistrement des réglages et d'affichage du journal.

Modifiez un petit nombre de réglages à la fois, consignez les valeurs avant/après, et rejouez un benchmark de non-régression. Des valeurs agressives peuvent augmenter temps CPU, utilisation mémoire et volume des journaux.

## 14. Statuts et dépannage

- `PASS_BOUNDED` : le scénario testé passe selon des critères précis et une portée limitée.
- `PARTIAL` : une partie de l'opération s'est achevée; inspectez les sorties.
- `UNRESOLVED` : aucune réponse/solution n'a été établie pour cette demande.
- `ERROR` : une action a échoué; la trace doit exposer l'erreur.
- `TIMEOUT` : délai dépassé, aucun succès n'en découle.
- `BLOCKED` : un contrôle de précondition/intégrité a empêché l'action.
- `GENERATED_UNVERIFIED` : le modèle a produit un texte, mais la vérité n'a pas été confirmée indépendamment.

Si l'interface affiche « Aucune réponse textuelle exploitable », ouvrez **Détails**, inspectez `generation_status`, `selected_route`, `sources`, le statut fournisseur, la durée et la trace mémoire. Vérifiez si la voie choisie était `rag_direct`, un modèle intégré, ou un fallback explicitement configuré. Ne masquez pas une erreur en convertissant automatiquement son statut en `PASS_BOUNDED`.

## 15. Sécurité et données d'entreprise

AAM peut observer des fichiers, processus et paquets autorisés; cela peut exposer des données personnelles, mots de passe, jetons et secrets. Choisissez un workspace dédié, n'activez les payloads réseau que si nécessaire, vérifiez les filtres, restreignez les droits et supprimez de façon contrôlée les copies que l'entreprise n'a plus le droit de conserver. Les observations ne contourneront ni les droits OS ni le chiffrement TLS. Les programmes composés et adaptateurs doivent être considérés comme du code opérant sous le compte courant.
