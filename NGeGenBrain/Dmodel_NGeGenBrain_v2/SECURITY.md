# Sécurité et frontière d'exécution

- Le cœur exécute un DSL déclaré ; il ne passe pas les programmes utilisateur à `eval` ou `exec`.
- L'interface Web intégrée n'écoute que sur loopback par défaut et le serveur refuse les IP non-loopback.
- Les modèles HF sont chargés avec `trust_remote_code=False`; l'option locale est la valeur par défaut.
- L'exécution de modèle doit être considérée comme coûteuse et dépendante des données et poids chargés. Exécuter les modèles non fiables dans un processus ou conteneur isolé selon les exigences locales.
- Les registres JSONL chaînés détectent des modifications de contenu non coordonnées mais ne sont pas une signature cryptographique avec identité externe ; protéger les fichiers et leurs hashes contre un attaquant ayant accès en écriture au workspace.
- Aucun système de « contournement automatique » des restrictions d'un modèle hôte n'est implémenté. Les restrictions de licence, d'accès et de sécurité ne sont pas des erreurs à contourner ; l'adapter utilise seulement les capacités réellement accessibles.
