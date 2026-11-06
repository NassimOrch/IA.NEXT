# CHANGELOG ORDER80.2.1

## 8.0.2.1 — généralisation

### Recherche générale

- passage d'une tâche supposée mathématique à un problème libre ;
- manifeste distinct pour problème, références, web et mémoire ;
- synthèse générale extractive avec provenance ;
- prise en compte des artefacts validés déjà présents en mémoire ;
- adaptation des requêtes à partir des données observées et des lacunes restantes ;
- déduplication par unités, hashes, URLs et requêtes.

### Références locales

- dossiers et fichiers explicitement autorisés ;
- vérification optionnelle SHA-256 par fichier ;
- rejet des liens symboliques sortant de la racine ;
- limite de taille locale ;
- conservation du texte effectivement observé dans l'audit.

### Réseau

- couche `SecureWebObserver` dédiée ;
- HTTP/HTTPS uniquement ; HTTPS par défaut ;
- allowlist distincte des destinations et des moteurs de recherche ;
- refus des credentials et des IP littérales ;
- normalisation IDNA des noms d'hôte ;
- contrôle DNS et rejet des adresses non publiques/spéciales ;
- connexion à l'IP validée ;
- TLS avec contexte de sécurité par défaut ;
- redirections désactivées par défaut et revalidées si activées ;
- taille/type de réponse bornés ;
- scripts HTML non exécutés ;
- pins SHA-256 optionnels ;
- journaux de sécurité.

### Recherche longue

- budget `m`, `h`, `day`, `week`, `forever` ;
- checkpoints ;
- attente anti-boucle lorsque l'état documentaire ne change pas ;
- demande RAG dynamique ;
- archivage de chaque nouvelle synthèse validée dans `news/`.

### Lignée

L'ancienne logique de preuve et les corpus spécifiques d'O80.2 sont conservés sous `legacy_order8020/` à des fins d'audit uniquement. Ils ne définissent pas le comportement de l'entrée généraliste.
