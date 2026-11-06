# État de livraison AAM O94_0

- Version logique : O94_0 (incrément de la base O94).
- Recommandation R1 : corps de réponse séparé des diagnostics et sources, détails inspectables séparément.
- Recommandation R2 : récupération avant génération par défaut, sélection explicite du backend de génération, chemin AAM délégué distinct du chemin LLM.
- Recommandation R3 : index maître → micro-RAG → feuilles atomiques ; mémoire événementielle et approfondissement contrôlé par la profondeur.
- Tests locaux : voir le registre et les reçus dans le paquet d'audit et le paquet de suivi.
- Limites à garder visibles : le corpus SMS complet de 5 574 lignes n'a pas fait l'objet d'une évaluation exhaustive de toutes les réponses ; les tests ne démontrent pas une validation native Windows, matérielle, ni de tous les serveurs LLM externes.
- Intégrité : utiliser les manifestes SHA-256 incorporés et le manifeste externe de livraison.
