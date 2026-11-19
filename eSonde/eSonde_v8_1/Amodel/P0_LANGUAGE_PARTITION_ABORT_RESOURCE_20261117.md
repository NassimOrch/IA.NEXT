# Diagnostic de variante — partition complète des associations OASST1 par langue

## Description
Une variante a été explorée pour éviter que le profil OASST1 multi-langue mélange directement ses associations. Elle construisait des compteurs exacts séparés par langue, ancre et token sur le split dérivé TRAIN uniquement.

## Architecture
Tables SQLite distinctes pour le nombre d'exemples/tokens par langue, la fréquence documentaire des ancres, le total de réponse par ancre, les arêtes ancre→token et les unigrammes par langue. Aucune donnée VALIDATION/TEST n'est utilisée; le runtime du modèle n'a pas été modifié par cette variante.

## Pipeline complet et exécution
Commande : `python /mnt/data/eSonde_v8_work/build_oasst1_language_views.py --reset`
Source : `derived/OASST1_chat/train.jsonl`, SHA-256 vérifié contre `dataset_manifest.json` avant lecture.

## Résultats observés
- 10 750 lignes TRAIN traitées avant l'expiration de la fenêtre de commande sur 48 557.
- 22 tags de langue rencontrés.
- 5 363 007 arêtes `lang_ctx` agrégées.
- Base SQLite 339 MiB et WAL 85 MiB au moment du diagnostic.
- Aucune vue linguistique finale n'a été publiée; le profil actif n'a pas été remplacé par cette variante.

## Interprétation
La table exacte complète aurait dépassé la capacité de stockage disponible et aurait fortement multiplié la taille du profil. Cette réalisation complète est donc écartée comme option de déploiement par défaut, non parce que le conditionnement linguistique serait impossible, mais parce que la copie intégrale des tables introduit un coût matériel disproportionné avant d'avoir démontré un gain. La variante légère déjà codée utilise le routeur linguistique existant : vocabulaire sélectionné pour filtrer les associations OASST1 et neutralisation des transitions OASST1 mixtes lorsqu'une langue précise est reconnue.

## Conséquences théoriques, conceptuelles et opérationnelles
Le profil global est conservé comme repli lorsque le routeur ne reconnaît pas de langue avec une confiance suffisante. La politique de filtrage reste une hypothèse à évaluer sur VALIDATION/TEST; elle n'est pas présentée comme une amélioration de cohérence démontrée. Les statistiques partielles SQLite sont conservées en artefact d'audit compressé.

## Conclusions
Variante de profil linguistique séparé : `ABORTED_RESOURCE_COST`, aucune publication partielle, aucun remplacement de poids ou de profil.

## Statut du modèle
Le modèle eSonde v8 reste en `P0_SOURCE_RECONCILIATION`; aucune génération libre n'a été exécutée dans cette expérience.
