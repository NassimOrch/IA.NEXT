# O94_0 — Formalisation initiale R1–R3

## Base de travail et provenance
La version O94 est conservée comme base : le code du runtime, le RAG multi-espace, les neurones de langage, l’interface et les protocoles de preuves sont repris sans réécriture générale. L’archive imbriquée `source_material/source_archive/sources_AAM_17.zip` passe le test CRC. La source théorique prioritaire `source_material/theorie_emp/DDD_Base_theorie_des_empreintes_complete_order_5.tex` a été lue directement et son SHA-256 est dans la checklist et le rapport d’intégrité.

## Principes de la théorie retenus
Le socle théorique définit l’empreinte comme une représentation issue d’un protocole d’observation. La résolution s’organise en une filtration de partitions : quand les sondes ajoutent de l’information, les classes se raffinent sans fusionner arbitrairement des classes déjà distinguées. Les chapitres consacrés à la représentation arborescente expliquent que les nœuds internes sont des classes encore non atomisées et que les feuilles sont les atomes de résolution. En conséquence, O94_0 représente les empreintes en nœuds de résumé et ne consulte le texte complet qu’après sélection hiérarchique.

## Diagnostic R1 — Réponses étrangères dans le chat
Le RAG actuel récupère des `chunks` de plusieurs enregistrements JSONL groupés ou coupés et le fallback extractif renvoie des passages complets avec plusieurs enregistrements. Le formateur de l’interface ajoute ensuite, dans le chat, le statut du RAG, la génération, les hashes et les extraits source. Il confond donc le **texte de réponse** avec la **trace d’audit**. Le contrat O94_0 sépare ces deux surfaces : le chat montre une seule réponse textuelle ; le bouton « Détails » conserve la provenance, les scores, le modèle, le prompt hash, les refus du contrôle de sortie et les autres candidats.

## Diagnostic R2 — Générateur qui n’exploite pas utilement le RAG
Le runtime tente d’appeler une capsule de langage ou un endpoint configuré, mais les sorties du petit modèle local peuvent être structurellement inutilisables ; dans ce cas le fallback actuel n’extrait pas le champ `response` d’un exemple JSONL. La nouvelle voie standard est : `requête observée → sélection hiérarchique RAG → contexte borné et non fiable → backend de génération sélectionné → contrôle de lisibilité/ancrage → réponse unique`. En cas de candidat rejeté, le fallback extrait la réponse du meilleur record par ses champs structurels et sa pertinence pour la question, sans inventer de réponse ni mettre en dur un fait attendu.

Un backend de délégation vers un autre **workspace AAM compatible** sera proposé en tant que choix explicite. Il reçoit la question et les passages RAG, n’active pas son propre RAG dans l’appel délégué et ne peut pas se déléguer récursivement. Un workspace arbitraire n’est pas chargé comme du code : le chemin est sélectionné explicitement et le runtime vérifie la compatibilité de ses artefacts.

## Diagnostic R3 — Accès mémoire trop global
Le fichier final contient aujourd’hui le texte brut de tous les chunks au même niveau que l’index de recherche. O94_0 introduit trois étages : (1) index maître de micro-RAG par empreinte agrégée, (2) micro-RAG sélectionné avec sa signature et son manifeste de contenu, (3) lignes/records pertinents dans ce micro-RAG. Le texte de chaque micro-RAG est stocké séparément, vérifié par SHA-256, et chargé seulement après sélection. La profondeur et le budget permettent de demander plus ou moins de détails ; le contexte supplémentaire peut ouvrir des sous-nœuds sans reclassifier l’empreinte générale à partir de la seule requête.

## Invariants à tester
1. Un enregistrement JSONL valide n’est jamais coupé entre deux chunks ni perdu lors du regroupement.
2. Une question qui pointe vers une réponse structurée retourne une réponse textuelle unique, sans le voisinage complet ni métadonnées dans le chat.
3. Les autres réponses disponibles restent consultables dans « Détails », avec citations et scores.
4. Un candidat du générateur local qui passe un contrôle lexical n’est pas présenté comme vérité certifiée ; les preuves n’établissent que la provenance.
5. Chaque lecture du texte complet vient d’un micro-RAG sélectionné, après vérification de son hash ; l’index maître contient seulement résumés d’empreintes, nombres de tokens, provenance et chemins sûrs.
6. Si aucune preuve n’est pertinente et aucun générateur utilisable n’existe, l’application le dit clairement au lieu de renvoyer une liste de réponses étrangères.

## Statut
P0 est terminé (CRC et hashes passés). P1 formalise les contrats. Rien dans cette note ne présume de réussite ou d’échec de la capacité d’AAM ; les réponses restent à évaluer avec des corpus et des critères indépendants.
