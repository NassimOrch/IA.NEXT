# ORDER80.2.1 — Guide complet de bout en bout

## 1. Objet

ORDER80.2.1 est la généralisation d'ORDER80.2.0. Il reçoit :

1. un problème en langage libre dans un fichier JSON ;
2. un manifeste de références locales et web ;
3. une durée de recherche ;
4. une mémoire persistante facultative.

Il observe les références, élargit progressivement sa couverture, produit des synthèses candidates avec provenance, et conserve les artefacts validés.

Le moteur n'inclut aucune connaissance spécifique à un problème particulier.

## 2. Séparation des rôles

### Problème

Le problème est dans `task.json` :

```json
{
  "title": "...",
  "problem": "...",
  "objective": "...",
  "domain": "...",
  "required_terms": ["..."]
}
```

### Références

Les références sont dans `references.json` :

```json
{
  "local": ["docs/"],
  "web": {
    "urls": ["https://trusted.example/doc"],
    "allow_domains": ["trusted.example"],
    "search_allow_domains": ["html.duckduckgo.com"],
    "search_engines": ["https://html.duckduckgo.com/html/?q={query}"],
    "search_queries": ["..."],
    "query_hints": ["..."]
  }
}
```

Le problème et les références sont volontairement séparés afin que l'emplacement de recherche soit une entrée contrôlée plutôt qu'une liberté réseau implicite.

## 3. Cycle de recherche

```text
problème
→ observation initiale limitée
→ synthèse
→ échec/gaps
→ nouvelle observation ciblée
→ synthèse
→ observation élargie
→ synthèse
→ nouvelles références web/locales
→ ...
```

La même unité ne doit pas être comptée comme nouvelle : le moteur garde les identifiants de chunks, les hashes de pages, les URLs et les requêtes déjà utilisées.

## 4. Recherche web sécurisée

La couche `SecureWebObserver` applique :

- protocoles HTTP/HTTPS uniquement ;
- HTTPS exigé par défaut ;
- hôtes explicitement allowlistés ;
- pas d'URL à authentification embarquée ;
- pas de cible IP littérale ;
- résolution DNS préalable ;
- rejet des adresses privées, loopback, link-local, multicast et autres plages spéciales ;
- connexion vers l'IP résolue ;
- redirections désactivées par défaut ;
- si les redirections sont activées, chaque hop est revalidé ;
- taille maximale de réponse ;
- types de contenu textuels uniquement ;
- aucun script HTML n'est exécuté ;
- hash SHA-256 facultatif par URL ;
- journalisation des rejets et erreurs.

Ces contrôles suivent notamment l'idée d'allowlist et de limitation des redirections recommandée par OWASP pour les clients capables de faire des requêtes réseau. Les risques de DNS rebinding ne disparaissent pas avec une simple vérification de chaîne ; ORDER80.2.1 résout puis connecte la requête sur l'IP contrôlée pour réduire cette fenêtre, mais une isolation réseau supplémentaire reste recommandée pour un déploiement de haute sensibilité.

## 5. Recherche locale

Seuls les chemins présents dans le manifeste entrent dans la zone de recherche. Les fichiers sont lus comme données textuelles ; ils ne sont jamais exécutés. Chaque chunk reçoit un hash documentaire et un hash de contenu.

## 6. RAG dynamique

Pendant l'exécution, de nouvelles données peuvent être déposées dans :

```text
<output>/rag_inbox/documents/
<output>/rag_inbox/formal/
```

Lorsqu'aucun nouveau matériau n'est disponible, le moteur écrit :

```text
<output>/rag_inbox/requests/CURRENT_REQUEST.json
```

Le message contient le problème, l'objectif, la requête suggérée et les emplacements attendus.

## 7. Mémoire

`memory.json` contient uniquement des artefacts dont le vérificateur configuré retourne `PASS`.

Une observation documentaire n'est donc pas transformée automatiquement en vérité.

Chaque entrée possède un fingerprint, une révision et le résultat du vérificateur.

## 8. Nouveautés

Toute synthèse nouvelle qui satisfait le contrat de vérification est enregistrée dans :

```text
news/<revision>_<fingerprint>/
```

avec :

```text
solution.json
demonstration.txt
verification.json
```

`demonstration.txt` est rendu à partir de l'objet produit par le moteur ; il n'est pas reconstruit manuellement par l'audit.

## 9. Statuts

`NOVEL_SOLUTION_SYNTHESIS` signifie que le moteur a produit une synthèse nouvelle qui satisfait le vérificateur de provenance configuré.

`NOT_NOVEL` signifie que le même artefact existe déjà dans la mémoire.

`TIME_BUDGET_EXPIRED` signifie seulement que la durée allouée est écoulée.

`UNRESOLVED` signifie qu'aucune synthèse satisfaisant le vérificateur n'a été produite pendant l'exécution.

Pour une preuve mathématique ou une propriété nécessitant une garantie formelle, un vérificateur de domaine plus fort doit être fourni ; le mode généraliste ne transforme pas une corroboration documentaire en preuve universelle.

## 10. Lancement

```bash
python3 run_order_8_0_2_1.py \
  --task data/examples/problem.json \
  --references data/examples/references.json \
  --output run_output \
  --duration 1h
```

Longues exécutions :

```bash
python3 run_order_8_0_2_1.py --task ... --references ... --duration 24h
python3 run_order_8_0_2_1.py --task ... --references ... --duration 1week
python3 run_order_8_0_2_1.py --task ... --references ... --duration forever
```

## 11. Contrôle Internet réel

Sur une machine avec sortie Internet publique :

```bash
python3 scripts/test_real_internet_order8021.py
```

Le script cible une page HTTPS IANA explicitement allowlistée et enregistre `real_internet_test_output/real_internet_result.json`.

L'environnement de construction de cette release ne permettait pas au processus Python d'effectuer une résolution DNS/sortie Internet publique. Ce fait est enregistré dans l'audit ; aucun faux résultat de « test Internet réel du moteur » n'est revendiqué.

## 12. Limites explicites

ORDER80.2.1 est généraliste au niveau du protocole de recherche, de la provenance, de la mémoire et de la politique réseau. Le moteur de synthèse intégré est extractif et déterministe : pour les tâches nécessitant raisonnement sémantique profond, exécution de code, preuve formelle de domaine ou génération créative, un adaptateur de raisonnement/vérification dédié doit être ajouté explicitement. Cette extension n'est pas injectée dans le cœur de la release.
