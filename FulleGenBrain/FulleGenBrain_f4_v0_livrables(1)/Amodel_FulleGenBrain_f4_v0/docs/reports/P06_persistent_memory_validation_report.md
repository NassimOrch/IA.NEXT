# Rapport de validation P06 — Mémoire vivante persistante et provenance

## 1. Description

P06 fournit au runtime FulleGenBrain_f4_v0 une mémoire durable vérifiable, un mécanisme de checkpoint/reprise, un graphe de dépendances versionnées et un protocole de vagues événementielles typées. L'adaptateur SQLite est la voie durable; `InMemoryRuntimeServices` sert d'adaptateur de référence non durable aux tests et aux exécutions éphémères. La phase ne prétend pas fournir une mémoire infinie ni contourner les budgets physiques : les limites sont explicites, configurables et remontent une erreur typée.

## 2. Architecture

- `SQLiteRuntimeServices`: SQLite, WAL, `synchronous=FULL`, clés étrangères, transactions `BEGIN IMMEDIATE`, savepoints imbriqués, migrations versionnées et contrôle SHA-256 des payloads persistés.
- `InMemoryRuntimeServices`: même contrat fonctionnel utile aux tests de sémantique, sans promesse de durabilité après arrêt du processus.
- Les objets portent version, statut opérationnel, statut épistémique, provenance par métadonnées et snapshots de versions/digests des dépendances.
- Les checkpoints et recherches sont liés à leurs hashes/programmes, les lectures vérifient les empreintes et la propagation `STALE`/révocation parcourt les dépendances transitives.
- Les vagues transportent source/version, destinataire, catégorie, contexte, compteur causal, provenance, priorité, TTL et clé d'idempotence; les abonnements, accusés de réception et demandes de replay sont conservés. Les catégories de révocation, changement de version et incident de sûreté reçoivent une priorité réservée.

## 3. Pipeline complet

1. Valider les entrées, paramètres de ressource et identifiants avant toute écriture.
2. Sérialiser selon JSON canonique, calculer SHA-256 et appliquer les limites de taille.
3. Ouvrir transaction SQLite atomique; vérifier clé d'idempotence et collisions; écrire l'objet/événement et ses dépendances; mettre à jour les statuts dérivés dans la même portée transactionnelle.
4. Lors d'une lecture ou d'un réveil, revalider le hash, les versions dépendantes et les états révoqués/obsolètes; préserver le payload et le statut épistémique d'origine.
5. Pour les vagues, appliquer TTL, backpressure, réserve critique, destinataire, abonnements, ordre stable et déduplication par consommateur.
6. N'autoriser un replay que pour une livraison antérieure encore valide, consigner le motif, le numéro de tentative et l'événement d'audit.
7. Le contrôle d'intégrité inspecte l'ensemble des enregistrements et les familles de contraintes, pas seulement les objets déjà lus.
8. Après exécution, la commande encadrée sauvegarde un snapshot versionné et SHA-256; le manifeste pointe vers le dernier snapshot complet.

## 4. Commandes d'exécution

À la racine du dépôt :

```sh
PYTHONPATH=src python3 -m unittest tests.test_p06_sqlite_services -v
PYTHONPATH=src python3 -m unittest tests.test_p06_wave_protocol_parity tests.test_p06_wave_ast -v
PYTHONPATH=src python3 -W error::ResourceWarning -m unittest discover -s tests -v
```

Exécution de projet journalisée et sauvegardée :

```sh
python3 scripts/run_checked.py --label p06-full-suite --kind model -- env PYTHONPATH=src python3 -W error::ResourceWarning -m unittest discover -s tests -v
```

## 5. Résultats

- Migration v1 → v2 testée, sans perte des vagues existantes.
- Contrôle d'intégrité : détection de JSON malformé, d'empreintes modifiées, d'altération de checkpoint/vague/recherche, de graphe de dépendances incohérent et de schéma futur non pris en charge.
- Transactions emboîtées commit/rollback, reprise après redémarrage, hibernation/réveil, propagation `STALE`, révocation transitive et prévention d'hibernation des objets épinglés/occupés testées.
- Protocole vague : TTL, file de taille bornée, capacité réservée aux événements critiques, destinataire/abonnements, compteurs causaux, métadonnées de contexte/provenance, idempotence et replay audité testés.
- Adaptateurs mémoire et SQLite comparés sur des scénarios de routage, priorité, idempotence, backpressure et replay.
- Tests ciblés P06 : 38 réussis (`logs/executions/P06/20261026T104232946067+0000_p06-wave-parity-and-ast-contract-suite-retest3.receipt.json`).
- Suite globale au moment de la clôture : 149 tests réussis, `ResourceWarning` configuré en erreur (`logs/executions/P06/20261026T104257719537+0000_p06-full-suite-after-adapter-parity.receipt.json`).

## 6. Interprétation des résultats

Les tests établissent les comportements couverts et leur répétabilité dans cet environnement. Ils ne constituent pas une preuve de correction universelle, de sécurité absolue, de performance illimitée ou de durabilité face à toute panne matérielle. SQLite fournit une persistance locale; la copie de sauvegarde, la restauration et les migrations doivent encore être exécutées sur la machine cible pour valider son disque et ses politiques de sauvegarde.

## 7. Conséquences théoriques, conceptuelles et opérationnelles

- Théorique : la mémoire est versionnée et vérifiable, avec un statut distinct pour validité opérationnelle et statut épistémique.
- Conceptuelle : `STALE`, `REVOKED`, `EXPIRED` et `UNRESOLVED` ne sont pas synonymes d'impossibilité; la réponse garde les causes et la provenance.
- Opérationnelle : les budgets sont des paramètres vérifiables; les événements critiques disposent d'une réserve mais restent bornés. Le replay est une action explicite, répétable et auditée.

## 8. Conclusions

**Statut P06 : PASS selon ses critères de sortie enregistrés.** Les anomalies de tests historiques ont été conservées au registre, reliées à leurs causes et marquées résolues avec les reçus de retest. La phase suivante autorisée est P07, synthèse/recherche paresseuse et CEGIS; P07 doit encore être auditée avant d'être déclarée terminée.

## 9. Statut du modèle

**P06 : PASS selon les critères et reçus de phase cités dans ce rapport.** Cette indication ne constitue pas une preuve de correction universelle.
