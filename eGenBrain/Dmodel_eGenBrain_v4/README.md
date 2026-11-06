# eGenBrain v4 — runtime autonome

Version du moteur : **4.0.0**. eGenBrain v4 préserve la base MG héritée, ajoute un maillage inférentiel typé et certifié, et conserve le retrieval/reconstruction v3 comme fallback traçable.

## Fichiers de livraison et installation

Il faut les deux archives `Dmodel_eGenBrain_v4.zip` et `Dmodel_eGenBrain_v4_part2.zip`, ainsi que `reassemble_packages_eGenBrain_v4.py`. Python 3.11+ est recommandé. Le chemin normal du moteur utilise la bibliothèque standard Python et SQLite; certains formats d'import facultatifs (par exemple Parquet) peuvent demander un module additionnel.

Placez les deux ZIP et le script externe dans un même dossier puis exécutez :

```bash
python reassemble_packages_eGenBrain_v4.py --archive-dir . --destination ./eGenBrain_v4_installed
```

L'installateur contrôle les CRC et chemins des ZIP, la taille et SHA-256 des deux fragments, reconstitue atomiquement `model/eGenBrain_v4.sqlite3`, vérifie l'empreinte finale et exécute `PRAGMA integrity_check` et `PRAGMA foreign_key_check`. Il refuse d'écraser une destination non vide.

## Lancement

Depuis le dossier installé :

```bash
python -m egenbrain serve --model model/eGenBrain_v4.sqlite3
python -m egenbrain chat --model model/eGenBrain_v4.sqlite3 --message "Tim buys 3 dozen eggs. Eggs cost $.50 each. How much did he pay for eggs?"
python -m egenbrain mesh4 --help
```

Le serveur local est destiné à l'usage local; l'interface v4 expose les opérations sur faits, règles, inférence et requêtes et conserve les traces. La base maillée v4 est un sidecar distinct de la base MG historique.

## Démarrage volontairement vierge

Pour démarrer l'interface sans charger le MG livré, donnez un chemin SQLite inexistant :

```bash
python -m egenbrain serve --model model/eGenBrain_v4_fresh.sqlite3 --empty-start
```

Cette option refuse le remplacement d'une base existante et crée un schéma vide sans réponses synthétiques. Il faut importer des données et déclarer les primitives/règles souhaitées. Elle ne promet pas de capacité d'apprentissage ou de généralisation non mesurée.

## Interprétation scientifique

Les tests de livraison prouvent l'intégrité et l'exécution des chemins testés. La campagne d'ablation est contenue dans l'archive d'audit, séparée du runtime. Le score 8/8 de composition vaut pour les huit micro-cas positifs finis de la campagne; il ne démontre ni induction autonome d'opérateurs ni intelligence générale. Le facteur `dozen=12` est une primitive fournie; les opérateurs arithmétiques sont des opérateurs typés génériques.
