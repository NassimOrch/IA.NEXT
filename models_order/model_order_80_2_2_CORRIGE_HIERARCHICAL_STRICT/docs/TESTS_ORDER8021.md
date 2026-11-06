# Tests ORDER80.2.1

## 1. Tests unitaires et intégration

La suite couvre le manifeste de références, le moteur généraliste, le RAG dynamique, la mémoire/news, le nettoyage HTML, les pins SHA-256, le rejet des URL dangereuses, la séparation de l'allowlist des moteurs de recherche, la protection contre les symlinks locaux, la validation des noms IDNA et le rejet des redirections hors périmètre.

Commande :

```bash
python3 -m pytest -q
```

## 2. Auto-test

```bash
python3 self_test_order8021.py
```

Il vérifie notamment une exécution générique de bout en bout et l'archivage `news/`.

## 3. Test de compilation

```bash
python3 -m compileall -q src run_order_8_0_2_1.py self_test_order8021.py scripts tests
```

## 4. Test du chemin web

`scripts/test_real_internet_order8021.py` appelle la vraie pile réseau Python du modèle contre une référence HTTPS publique. Dans le sandbox de construction, la résolution DNS sortante est bloquée ; le résultat attendu ici est donc un échec réseau explicite, jamais une réussite simulée.

Pour le déploiement sur un PC avec Internet, le même script doit être exécuté localement et son JSON conservé dans l'audit.

## 5. Validation externe de conception

La page publique IANA de référence est actuellement disponible, et la documentation OWASP/Python utilisée pour la conception confirme les principes d'allowlist, de redirection contrôlée et de validation TLS. La validation externe n'est jamais substituée au test de la pile réseau du modèle.
