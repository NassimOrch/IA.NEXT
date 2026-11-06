# Installation et lancement — ORDER80.2.1

## 1. Prérequis

Python 3.10 ou plus récent. Le noyau utilise uniquement la bibliothèque standard Python.

## 2. Décompression

```bash
unzip model_order_8_0_2_1.zip -d model_order_8_0_2_1
cd model_order_8_0_2_1
```

## 3. Vérification locale

```bash
python3 -m compileall -q src run_order_8_0_2_1.py self_test_order8021.py scripts tests
python3 self_test_order8021.py
python3 -m pytest -q
```

## 4. Première recherche

```bash
python3 run_order_8_0_2_1.py \
  --task data/examples/problem.json \
  --references data/examples/references.json \
  --output run_output \
  --duration 5m
```

## 5. Mémoire persistante

```bash
python3 run_order_8_0_2_1.py \
  --task task.json \
  --references references.json \
  --output run_output \
  --memory persistent_memory.json \
  --duration 24h
```

La mémoire contient les artefacts admis par le vérificateur. Elle ne remplace pas la frontière de références.

## 6. RAG dynamique pendant un run

Déposer des fichiers dans :

```text
run_output/rag_inbox/documents/
run_output/rag_inbox/formal/
```

Le moteur rescannera ces répertoires à chaque cycle. Aucun document n'est exécuté.

## 7. Recherche web

Renseigner `references.json` avec `allow_domains` et `search_allow_domains`. Garder `require_https=true`, `max_redirects=0` et des limites de taille/temps conservatrices pour un usage de production.

## 8. Contrôle réseau réel

```bash
python3 scripts/test_real_internet_order8021.py
```

Ce script utilise la pile réseau de ce modèle, pas une bibliothèque externe. Sur le sandbox de construction utilisé pour cette release, DNS/sortie Internet publique est indisponible ; l'audit conserve le FAIL environnemental. Sur un PC connecté, le fichier JSON retourné doit être archivé avec l'audit du run.

## 9. Interruption

`SIGINT`/`SIGTERM` provoquent un arrêt contrôlé et écrivent un checkpoint. Le checkpoint décrit l'état, mais la reprise parfaite de tout l'état réseau n'est pas promise par cette release ; réutiliser la même mémoire empêche toutefois de perdre les artefacts validés déjà enregistrés.
