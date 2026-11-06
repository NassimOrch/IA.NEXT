# Sécurité ORDER80.2.2

La politique de sécurité web héritée d’O80.2.1 est conservée : HTTPS par défaut, allowlist de domaines, pas d’userinfo, pas d’IP littérale comme destination, résolution DNS et rejet des adresses spéciales/non publiques, ports bornés, TLS via contexte vérificateur, redirections désactivées par défaut et revalidées si activées, tailles et types de contenu bornés, HTML traité comme texte non exécutable et journalisation des décisions.

Le chemin local protège les racines autorisées contre les échappements de symlink et borne la taille des fichiers.

Le benchmark n’accorde jamais au moteur une destination web supplémentaire parce qu’un résultat de recherche la propose : le domaine doit déjà appartenir à l’allowlist de contenu.
