# Portabilité et installation — NGeGenBrain_v0

## Contenu hors ligne

Le projet n'a aucune dépendance PyPI : il utilise la bibliothèque standard Python et SQLite. Les sources de l'application, l'interface, les exemples, les tests et les fichiers de formalisation sont livrés dans `Dmodel_NGeGenBrain_v0.zip`. **La livraison source n'inclut pas un interpréteur Python natif Windows/Linux/macOS**, car ces binaires sont spécifiques à l'OS et à l'architecture et le conteneur de construction ne pouvait pas joindre `python.org` pour télécharger le runtime officiel. Cette contrainte est signalée plutôt que dissimulée.

Sur Linux/macOS, utilisez un Python 3.11+ déjà installé. Sur Windows, les `.bat` vérifient d'abord `runtime\python314\python.exe`, puis `py -3` et `python`, et rejettent les interpréteurs antérieurs à 3.11.

## Windows x64 sans Python installé globalement

La commande suivante télécharge à la demande le package embeddable officiel Python 3.14.10 et vérifie son SHA-256 avant extraction :

```powershell
powershell -ExecutionPolicy Bypass -File tools\bootstrap_python_windows.ps1
```

Source officielle : <https://www.python.org/downloads/release/python-31410/>. Empreinte annoncée pour `python-3.14.10-embed-amd64.zip` :

`90905e64a840557d8c1bc4f5b74db3d7ee85e3ffb217611cac1c7813acea4159`

Le bootstrapper n'installe pas de paquet tiers et conserve le runtime sous `runtime\python314`. Le script n'a pas pu être exécuté dans le conteneur Linux de construction : le DNS vers `python.org` n'était pas disponible et `cmd.exe`/PowerShell Windows ne sont pas présents. L'empreinte est reprise de la page officielle du projet Python ; sa vérification effective s'effectue sur l'ordinateur de destination lorsque le téléchargement aboutit.

Après bootstrap, double-cliquez `launch_NGeGenBrain_v0.bat`. Le lanceur démarre le serveur local, attend une réponse HTTP 200 sur `127.0.0.1:8765`, puis ouvre le navigateur. Les données sont écrites dans `%LOCALAPPDATA%\NGeGenBrain_v0\data`, et non dans le dossier temporaire de Windows.

## Portée des validations

La suite de tests et les scripts de validation sont reproductibles avec l'interpréteur de l'ordinateur cible. Dans l'environnement de construction Linux, la suite runtime a été exécutée en traitant `ResourceWarning` comme une erreur. Les fichiers `.bat` sont contrôlés statiquement ici, pas exécutés nativement par `cmd.exe`. Une vérification du bootstrap et du lancement Windows réel doit être effectuée sur Windows x64 et consignée dans le registre des preuves avant de prétendre à une validation native Windows.
