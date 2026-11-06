# Guide utilisateur complet — AAM O93_1

**Version du guide :** O93_1 / runtime `0.93.1`  
**Public visé :** utilisateur de l’application de bureau, expérimentateur RAG/sondes, personne chargée d’acquérir des compétences et administrateur du workspace.

## 1. Ce que fait le système

O93_1 organise le runtime autour d’un même chemin de travail : observation des sources, création d’empreintes et de vues par sondes, recherche de preuves dans le RAG sémantique, sélection ou exécution d’une compétence, génération éventuelle par un modèle local entraîné, contrôle de la qualité de la candidate, puis journalisation de la provenance et des événements.

Il faut distinguer trois choses qui ne sont pas synonymes :

1. **RAG prêt** : une source a été observée/ingérée et des espaces sémantiques sont disponibles.
2. **Capsule entraînée disponible** : un artefact de modèle est présent dans le catalogue et sélectionnable.
3. **Réponse générée par le modèle** : le runtime a appelé cette capsule. Même si l’appel a eu lieu, sa candidate peut être rejetée lorsqu’elle est structurellement inutilisable. Dans ce cas, O93_1 peut servir un extrait RAG cité et signaler que la réponse affichée est extractive, non générée.

Un état `PASS_BOUNDED` signifie que le test défini a réussi dans sa portée précisée. Ce n’est pas une certification universelle de vérité ni de généralisation.

## 2. Installation, lancement et espace de travail

### Lancer l’interface graphique

Depuis le dossier racine extrait de `Dmodel_AAM_O93_1.zip` :

```bash
python -m aam_o93 ui
```

Un environnement Python disposant des dépendances du paquet et de Tkinter est requis. Sous Linux, l’application doit disposer d’une session graphique. Pour un serveur sans écran, les tests d’interface peuvent être exécutés sous Xvfb, mais cela ne remplace pas un test interactif sur la machine de l’utilisateur.

### Choisir l’emplacement des données runtime

Le workspace contient notamment les sources de connaissance observées, les espaces sémantiques, les sessions de chat, les checkpoints, les journaux d’audit et les états de compétences. Pour isoler un essai ou choisir un dossier dédié, utiliser un chemin explicite :

```bash
python -m aam_o93 --workspace ./workspace_o93_1 status
python -m aam_o93 --workspace ./workspace_o93_1 ui
```

Le workspace passé par `--workspace` est distinct des fichiers du paquet. Pour une expérience reproductible, conserver le workspace, les manifestes de sources et les rapports de test associés.

### Autonomie au démarrage

Le runtime O93_1 démarre la boucle autonome au démarrage par défaut. Dans l’interface, l’état est affiché en haut de la fenêtre et dans l’onglet **Observation / Mémoire**. L’autonomie continue entre les demandes de chat et peut effectuer ses pulsations périodiques.

- **Arrêter la boucle (AAM reste ouvert)** : arrête la boucle autonome sans fermer le chat ni le runtime.
- **Redémarrer la boucle** : redémarre cette boucle tant que le runtime est encore ouvert.
- **Fermer AAM** : arrête l’autonomie, tente d’écrire le checkpoint de fermeture, puis ferme la fenêtre et le runtime.

La désactivation de l’enregistrement de la mémoire de raisonnement ne stoppe pas la boucle autonome. Un arrêt de boucle n’est pas la même action qu’une fermeture complète d’AAM.

Les commandes CLI sont des opérations finies : elles créent un runtime pour exécuter la commande et arrêtent sa boucle avant de quitter. Pour une autonomie qui reste active, lancer la commande `ui` et laisser AAM ouvert.

## 3. Chat : chemin conseillé pour une réponse ancrée dans les sources

1. Ouvrir l’onglet **RAG / Sources** et ingérer au moins une source (voir la section 4). Vérifier que la source apparaît dans la liste des sources observées et que son intégrité est acceptée.
2. Revenir dans **Chat**. Choisir **Mode** `chat` (ou `auto` si l’orchestration complète est souhaitée).
3. Dans **Politique RAG**, choisir `observe_first` pour privilégier l’observation/recherche sémantique. `auto` laisse la politique adapter le parcours. `lexical` privilégie le chemin lexical classique. `off` désactive le retrieval RAG pour cette requête.
4. Cliquer sur **Actualiser les modèles**. Dans **Modèle de langue**, sélectionner `auto` ou l’identifiant exact de la capsule entraînée. Pour tester un artefact particulier, sélectionner son ID explicite plutôt que supposer que `auto` choisira celui attendu.
5. Poser une question qui peut être vérifiée dans les sources ingérées et cliquer **Envoyer / répondre**.
6. Examiner la réponse, ses citations et l’indication de provenance. Cliquer **Détails techniques** pour consulter l’objet de résultat complet.
7. Évaluer le résultat via `satisfied`, `partial` ou `unsatisfied`, ajouter un commentaire puis **Enregistrer la note**. Le feedback est journalisé comme un signal, pas comme une preuve automatique de vérité.

### Vérifier que le RAG a vraiment été utilisé

Dans **Détails techniques**, rechercher les champs équivalents à :

- `retrieval_status` et `selected_route` : ils indiquent le résultat et le chemin de recherche.
- `evidence` / citations : les éléments effectivement récupérés.
- `generation.backend`, `generation.model_id`, `generation.capsule_sha256` : identifient le moteur et la capsule appelée.
- `generation.model_invocation_captured`, `prompt_sha256` et `context_sha256` : prouvent qu’un prompt/context a été transmis et haché.
- `generation.context_citations` : références transmises au générateur.
- `generation.answer_source`, `candidate_selected` et `candidate_quality_gate` : indiquent si la candidate générée est réellement affichée ou si le runtime a choisi un fallback ancré dans les sources.

Ne déduire **ni** l’usage du RAG d’un simple affichage de citations, **ni** l’usage du modèle de la seule présence d’un modèle dans le catalogue. Vérifier le résultat technique de la requête concernée.

### Comprendre le fallback

Une capsule compacte peut être appelée mais produire une candidate de mauvaise qualité structurelle (par exemple des marqueurs inconnus tels que `<unk>`, trop peu de tokens utilisables ou aucun ancrage lexical aux preuves). Le runtime conserve la trace/hash de cette candidate, la rejette et peut afficher un passage récupéré avec citation. Dans ce cas :

- le RAG peut avoir été utilisé correctement ;
- le modèle peut avoir été réellement appelé ;
- mais **la phrase montrée à l’utilisateur est le fallback extractif**, et non le texte généré.

O93_1 a passé un essai borné sur 120 messages réels du corpus SMS : le message « £900 prize » était absent des données d’entraînement mais présent dans le RAG, dans le prompt et dans la réponse extractive citée. La capsule entraînée a bien été appelée ; sa candidate a été rejetée pour des marqueurs `<unk>` et l’absence d’ancrages. Les hashes des sources sont restés inchangés. Ce test vérifie le routage et la traçabilité, pas la qualité factuelle générale du générateur. Le test sur les 5 574 lignes complètes est en cours d’évaluation distincte dans le registre de suivi.

## 4. Onglet « RAG / Sources »

### Ingérer une source

1. Cliquer **Choisir source/dossier**.
2. Sélectionner un fichier ou un dossier approprié.
3. Cliquer **Observer source et ingérer**.
4. Après la fin de l’opération, cliquer **Lister les sources observées** et contrôler `source_id`, le chemin, le nombre de chunks et le statut d’intégrité.
5. Cliquer **Lire le RAG sémantique** pour tester une question concrète. Le résultat présente les preuves disponibles pour cette question.

Après ajout ou modification de fichiers, utiliser **Mettre à jour / reconstruire**. Il reconstruit l’espace sémantique depuis les chunks observés ; il ne remplace pas l’étape d’ingestion des nouveaux fichiers.

### Politiques de recherche

- `observe_first` : politique recommandée pour l’usage normal observation/RAG sémantique.
- `auto` : laisse le runtime décider du chemin de retrieval.
- `lexical` : recherche lexicale classique, distincte du lecteur sémantique.
- `off` : ne pas utiliser le RAG pour cette requête.

Sélectionner la politique puis cliquer **Appliquer politique** pour la rendre persistante. Dans le chat, le choix peut être contrôlé par requête via la liste correspondante.

### Inspecter et nettoyer les espaces

- **Lister les espaces** actualise la table des espaces intermédiaires et finaux.
- Sélectionner une ligne puis **Inspecter** pour lire ses informations.
- **Supprimer espace** supprime l’espace sélectionné après confirmation.
- **Nettoyer intermédiaires** supprime les payloads intermédiaires et conserve l’espace final actif.

N’effectuer le nettoyage qu’après avoir vérifié qu’un espace final est construit et lisible. Les décisions de reconstruction et de suppression sont consignées.

### Sources multimodales

Le système observe et fingerprint les entrées qui ont un adaptateur déclaré. Le décodage réel dépend des lecteurs disponibles dans la livraison et de l’environnement. Les images, fichiers audio et vidéos peuvent rester au statut fingerprint-only lorsque OCR, ASR ou transcription n’est pas installé/configuré. Ne pas interpréter un hash ou une empreinte brute comme une compréhension sémantique du média.

### Extraire des compétences candidates

Cliquer **Extraire les compétences candidates** après observation/ingestion. Les objets retournés sont des candidates dérivées des sources, pas des compétences considérées automatiquement validées. Inspecter leur provenance, les tester et les valider selon les procédures de l’onglet **Compétences**.

## 5. Onglet « Observer »

1. Entrer un chemin ou cliquer **Choisir fichier/dossier**.
2. Cliquer **Observer**.
3. Examiner le résultat et le statut de décodage : une observation peut réussir partiellement si le contenu brut est lisible mais qu’un adaptateur de niveau supérieur manque.

Pour utiliser une caméra, cliquer **Capturer une image caméra…**, confirmer explicitement l’autorisation puis choisir l’index matériel. La capture est limitée par le paramètre affiché dans le runtime. Une caméra réelle n’est pas supposée disponible dans un test local et doit être validée sur la machine cible.

## 6. Onglet « Sondes »

Cet espace permet de régler la politique d’empreinte, produire des candidates de sonde, inspecter/charger/modifier des définitions et tester une sonde ou un ensemble.

1. Commencer par **Politique d’empreinte** : `complete_multiview` ou `complete_multiview_extended`.
2. Dans **Génération adaptative**, entrer l’objet ou la valeur à observer et choisir la modalité disponible.
3. Cliquer sur la génération de sondes candidates et inspecter les sorties.
4. Pour charger une définition persistante, choisir un fichier JSON. L’import vérifie la définition et ne l’exécute pas automatiquement.
5. Sélectionner une sonde sauvegardée pour l’inspecter ou la modifier ; enregistrer une modification après validation.
6. Tester la sonde sélectionnée, puis utiliser le test d’ensemble pour comparer les observations.

Une sonde différente n’est pas la preuve, à elle seule, d’une compétence acquise. Conserver les résultats et l’empreinte source pour comparer les observations et les collisions éventuelles.

## 7. Onglet « Compétences »

- **Actualiser compétences** recharge le catalogue.
- Sélectionner une compétence, fournir une entrée JSON (chaîne ou objet) et cliquer **Tester**.
- Le bloc de composition accepte un graphe JSON contrôlé (séquence/étape/condition). Modifier le graphe, nommer la composition puis **Sauvegarder graphe**.
- **Lister compositions**, sélectionner une composition et **Exécuter** pour rejouer son graphe ; **Supprimer** retire la composition après contrôle.
- Les fiches de compétence sont déclaratives : elles ne doivent pas être confondues avec du code importé ou exécuté.

L’évaluation indépendante est nécessaire avant de promouvoir une candidate. Pour tester le transfert, prévoir un cas distinct de celui utilisé pendant l’acquisition et conserver les preuves source-off quand l’expérience en dépend.

## 8. Onglet « Observation / Mémoire » et autonomie

- Vérifier le badge/texte d’état de la boucle autonome.
- **Arrêter la boucle (AAM reste ouvert)** stoppe la boucle mais laisse le chat et le runtime disponibles.
- **Redémarrer la boucle** remet l’autonomie en marche.
- **Enregistrer la mémoire de raisonnement** contrôle seulement cet enregistrement ; l’audit de contrôle/intégrité reste actif.
- **Auto-observer maintenant** lance une observation manuelle additionnelle.
- **Lister les mémoires** présente l’inventaire et le focus courant.
- **Lire le journal causal** ou **Actualiser événements** affiche les événements et leurs parents déclarés. `prev_hash` est la chaîne d’intégrité ; les hash parents représentent la causalité métier annoncée, ces notions ne sont pas interchangeables.
- Sélectionner un événement dans la table permet d’inspecter son détail.

Pour fermer toute l’application, utiliser **Fermer AAM** et attendre la confirmation de fermeture. Si la fermeture échoue, l’application garde la fenêtre ouverte afin de permettre une nouvelle tentative.

## 9. Onglet « Entraînement » et acquisition de données

1. Cliquer **Choisir fichier/dossier…** et sélectionner le dataset.
2. Cliquer **Inspecter / observer dataset** avant toute acquisition. Contrôler les formats, les clés disponibles et les erreurs de décodage.
3. Choisir `unsupervised` ou `supervised`.
   - `unsupervised` : observation, construction du RAG et proposition de candidates sourcées ; ce mode ne prétend pas réaliser un fit supervisé de paramètres.
   - `supervised` : nécessite des clés explicites d’entrée et de cible existant sur les enregistrements utilisables. L’acquisition doit retourner un statut valide et un checkpoint de formation.
4. **Ajouter au RAG** ingère la source dans la base de connaissances. **Lancer le RAG** réexécute l’ingestion depuis la source choisie.
5. **Lancer acquisition** démarre le chemin d’apprentissage/acquisition conformément au mode. Les résultats doivent être inspectés avant toute promotion.
6. **Pause**, **Reprendre** et **Arrêter** envoient des contrôles coopératifs au processus en cours ; consultez le statut et le checkpoint plutôt que d’interrompre brutalement le processus.
7. Après entraînement/acquisition, revenir au chat et cliquer **Actualiser les modèles**. Sélectionner l’identifiant exact de la capsule si plusieurs modèles sont disponibles.

Ne pas utiliser le mode non supervisé dans l’idée qu’il créerait automatiquement des labels. Ne pas supposer qu’un dataset est utilisable pour un entraînement de langue simplement parce qu’il peut être indexé par le RAG : ce sont deux opérations distinctes.

## 10. Onglet « Internet / API »

L’accès réseau est désactivé par défaut. Pour une recherche Internet :

1. examiner les permissions réseau ;
2. cocher l’autorisation Internet puis **Enregistrer permissions/sites/connecteurs** ;
3. inscrire les hôtes/URL HTTPS approuvés ;
4. utiliser **Rechercher (confirmation requise)…** et confirmer l’action ponctuelle ;
5. ne considérer le résultat distant que comme une donnée non fiable, jamais comme une instruction exécutée.

Les champs MCP/API de cette version enregistrent des métadonnées de connecteurs ; ils ne lancent pas automatiquement un exécuteur MCP/API distant. Ne saisir aucun secret dans les champs de recherche ou dans les sources non fiables.

## 11. « Réglages généraux »

Cette page regroupe notamment l’influence temporaire de l’auto-observation sur les poids sémantiques, l’adaptation temporaire des poids RAG, le nombre de sondes (`auto` ou `manual`), la politique de génération des sondes, le focus de mémoire/catégories/sources, la cadence du focus, les paramètres d’entraînement et la politique Internet. Cliquer **Enregistrer tous les réglages** après modification et consulter le retour technique. Si les options de focus ne sont pas renseignées, la politique persistante précédente reste en vigueur.

## 12. Ligne de commande utile

Les commandes doivent être lancées depuis la racine du paquet ; elles démarrent un runtime temporaire, exécutent une action auditée et ferment ce runtime à la fin.

```bash
# Etat du runtime
python -m aam_o93 status

# Observer un fichier ou un dossier
python -m aam_o93 observe ./chemin/vers/source --recursive

# Ingérer une source au RAG (sans apprentissage supervisé implicite)
python -m aam_o93 knowledge-ingest ./chemin/vers/source --no-learn

# Lire l’espace sémantique final
python -m aam_o93 semantic-search "votre question" --top-k 5

# Lister les espaces sémantiques
python -m aam_o93 rag-spaces

# Reconstruire les espaces et nettoyer les intermédiaires après réussite
python -m aam_o93 rag-rebuild --cleanup-after

# Chat avec politique observation-first et modèle choisi automatiquement
python -m aam_o93 solve "Votre question sur les sources observées" --mode chat --retrieval-policy observe_first --language-model auto

# Lister les compétences
python -m aam_o93 competences

# Statut de la boucle autonome pour la commande CLI finie
python -m aam_o93 autonomy status

# Ouvrir l’interface persistante
python -m aam_o93 ui
```

Pour fixer le workspace, ajouter `--workspace ./workspace_o93_1` **avant** la sous-commande, par exemple `python -m aam_o93 --workspace ./workspace_o93_1 status`.

## 13. Résolution des problèmes fréquents

**Le chat ne cite aucune source.** Vérifier que les sources ont été ingérées, qu’elles apparaissent dans la liste, que la politique n’est pas `off`, et tester directement une requête dans `Lire le RAG sémantique`. Reconstruire l’espace après ingestion d’un nouveau fichier.

**Le modèle n’apparaît pas dans la liste.** Cliquer **Actualiser les modèles**. Vérifier que l’acquisition/entraînement a réellement créé une capsule enregistrée, que son statut et son intégrité sont valides et que l’espace de travail est le même que celui de l’entraînement. Ne pas deviner son identifiant.

**Le modèle est listé mais le texte est extrait des sources.** Ouvrir **Détails techniques**. Si `model_invocation_captured=true` et `candidate_selected=false`, le modèle a pu être appelé, mais sa candidate a échoué au contrôle et le fallback RAG a été livré. Garder le rapport/candidate hash pour améliorer l’entraînement ou le générateur ; ne pas attribuer au modèle le texte du fallback.

**Une opération indique `PARTIAL`, `NOT_DECODED` ou fingerprint-only.** Vérifier l’adaptateur et ses dépendances. Le hash prouve l’identité des octets, pas que leur contenu a été décodé.

**Un bouton semble ne rien faire.** Vérifier l’état de tâche en haut, attendre la fin de l’opération, puis cliquer **Actualiser état** ou **Afficher les journaux**. Une tâche asynchrone peut être refusée tant qu’une autre est active. Les commandes d’arrêt/redémarrage de l’autonomie sont conçues pour rester indépendantes de cette tâche UI ; si elles bloquent encore, garder le journal et le rapport d’erreur.

**Le lancement échoue sans interface.** Lancer `python -m aam_o93 status` pour obtenir un diagnostic textuel. Pour `ui`, installer/activer Tkinter et utiliser une session graphique. Les tests Xvfb valident des contrats UI automatisés, pas l’expérience visuelle native de tous les OS.

**La fermeture est lente ou ne confirme pas l’arrêt.** Ne pas supprimer le workspace. Vérifier les derniers événements d’autonomie, le résultat de fermeture et le checkpoint ; relancer la fermeture depuis la fenêtre encore ouverte si le bouton le permet. Préserver les logs avant tout nettoyage.

## 14. Sauvegarde, intégrité et données

- Sauvegarder le workspace avant un test de migration, une reconstruction majeure du RAG ou un entraînement prolongé.
- Ne pas modifier manuellement les fichiers de checkpoints, d’espaces sémantiques ou de journaux pendant qu’AAM fonctionne.
- Conserver la source originale, son hash, les manifestes de chunks, les preuves d’invocation et les rapports d’évaluation ensemble.
- Pour un audit, exécuter `python scripts/o931_preflight.py --label votre_essai` avant une nouvelle série de tests ; après chaque lot, conserver le stdout, le code de sortie, le JSON de résultat et mettre à jour les checklists de phase et d’erreurs.
- Les tests d’acceptation P10 (Windows/ACL natifs, caméras/capteurs physiques, endpoints réseau réels, crash/rollback sur la machine cible) nécessitent une validation sur les environnements concernés. Les tests locaux ne doivent pas être présentés comme ces preuves externes.

## 15. Statut et interprétation

O93_1 est versionné comme `0.93.1`. La phase actuellement exécutée est P3 (régression et intégration). Le test SMS borné a prouvé le chemin RAG → capsule entraînée → contrôle de candidate → réponse extractive citée et l’intégrité des sources. La candidate de la capsule a échoué au garde-fou de qualité dans ce test ; le système a donc fourni un passage observé plutôt que du texte de génération inutilisable. La campagne du corpus complet est enregistrée séparément ; P3 n’est clôturée que lorsque les critères de sortie et les reçus correspondants sont synchronisés.
