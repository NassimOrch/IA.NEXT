# P7 — empaquetage portable et limites de validation

## Description et architecture

Le modèle, l’audit et le suivi sont trois archives indépendantes partageant un contrat de manifestes SHA-256. Les manifestes internes excluent uniquement leurs deux fichiers de manifeste afin d’éviter l’auto-référence; l’empreinte externe de chaque ZIP est consignée dans `O94_0_livraison_manifest.json`.

## Pipeline

Préflight des chemins, formalismes et checklists; vérification SHA-256 des entrées historiques; copie de staging; création des manifestes parallèles; création ZIP; test CRC; validation des chemins; extraction neuve; vérification de tous les fichiers manifestés; smoke-test du CLI sur le paquet modèle; contrôle du manifeste propre à la sauvegarde.

## Commandes de vérification

Depuis la racine du paquet modèle, les commandes de smoke-test utilisées sont `python -m aam_o93 --workspace <dossier-temporaire> status` et `python -m aam_o93 --workspace <dossier-temporaire> base-blocks`. Le constructeur partagé est `scripts/o94_delivery_common.py`; les reçus sont dans `logs/O94_0/` et dans le paquet de suivi.

## Résultats de candidats

Les trois candidats ont passé CRC, extraction fraîche et vérification interne des manifestes; le paquet modèle a également passé les commandes CLI `status` et `base-blocks`. Les tailles observées sont inscrites dans `logs/O94_0/P7_candidate_set_001.json`. Les archives finales seront reconstruites après synchronisation des checklists et de la sauvegarde, puis vérifiées indépendamment.

## Interprétation et limites

Ces contrôles établissent l’intégrité des fichiers distribués et quelques démarrages locaux; ils ne prouvent pas la vérité universelle des réponses ni la compatibilité avec tout endpoint. Restent non validés dans cet environnement : Windows natif/NTFS/ACL, serveur réel LLM/AAM externe, capteurs/caméra physiques, et parcours exhaustif des 5 574 SMS. Le test SMS de 300 lignes et l’évaluation de 10 requêtes sur 32 enregistrements sont des échantillons explicitement bornés.

## Conséquences et statut

La livraison ne prétendra une validation complète que pour les critères de phase et les reçus qui la prouvent. Les premiers échecs de construction et leurs retests sont conservés dans le registre des incidents.
