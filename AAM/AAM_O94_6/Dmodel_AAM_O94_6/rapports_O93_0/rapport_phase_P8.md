# Rapport de phase P8 — intégration et sécurité

## Description
P8 vérifie que les principales surfaces opérationnelles O93_0 convergent vers un contrat d’action traçable et que la mémoire/checkpoint résiste aux erreurs, à la concurrence et aux entrées hostiles. La clôture est bornée aux tests exécutés localement; elle ne certifie pas les plateformes, fournisseurs ou périphériques externes.

## Architecture
- `aam_o93.contracts.ActionEnvelope` définit l’enveloppe versionnée de l’action, les capacités demandées et les références causales.
- `AAMRuntime.dispatch_action` valide l’action enregistrée, écrit les événements start/completion/failure, relie les événements descendants à la cause et ne transforme pas une capacité demandée en permission.
- UI : `O93Desktop._execute_action` / `_run`; CLI : `_route`; cycle autonome : `AAMRuntime.autonomy_step`.
- Mémoire : `O93Memory._append_chain` sérialise les écritures interprocessus; checkpoint écrit atomiquement avec chemins contrôlés et refus des liens symboliques concernés.
- Les permissions effectives restent vérifiées par les services cibles (réseau, caméra, fichiers); le contenu observé reste non fiable.

## Pipeline complet
1. Lire le formalisme, le laboratoire, la checklist de phase et les deux registres d’erreurs.
2. Vérifier P7 clôturée, P8 active et P9 non démarrée.
3. Auditer statiquement les identifiants UI/CLI face au registre commun.
4. Rejouer les tests de routeur, d’intégration, de sécurité et la matrice inter-phases en processus séparés.
5. Vérifier les sorties, les empreintes et les hashes des fichiers de test utilisés.
6. Réconcilier les alertes historiques avec les résultats courants sans supprimer leur historique.
7. Fermer P8 dans la checklist et le registre; ne démarrer P9 qu’après un nouveau préflight.

## Commandes d’exécution
- `python -m pytest -q tests/test_p8_action_router.py tests/test_p8_integration.py tests/test_p8_security.py` — résultat ciblé historique de ce lot : 34 tests passés et 5 sous-tests passés.
- `python scripts/o930_p8_isolated_matrix.py --start 0 --count 1 --timeout 18` — pilote du runner isolé.
- `python scripts/o930_p8_isolated_matrix.py --start 1 --count 5 --timeout 18`
- `python scripts/o930_p8_isolated_matrix.py --start 6 --count 4 --timeout 18`
- `python scripts/o930_p8_isolated_matrix.py --start 10 --count 5 --timeout 18`
- `python scripts/o930_p8_isolated_matrix.py --start 15 --count 5 --timeout 18`
- `python scripts/o930_p8_isolated_matrix.py --start 20 --count 5 --timeout 18`
- `python scripts/o930_p8_isolated_matrix.py --start 25 --count 5 --timeout 18`
- `python -m py_compile scripts/o930_p8_isolated_matrix.py`

Le test de transition strict `tests/test_p9_preregistered_v2_integrity.py` a été volontairement exclu avant la clôture; il sera exécuté seulement au préflight P9.

## Résultats bruts
- Matrice isolée actuelle : **30 modules PASS / 30, 222 tests rapportés, 0 module en échec**, reçu `logs/O930_P8_resume_matrix_result.json`.
- Contrat d’action : **10 tests PASS**, `logs/O930_P8_resume_matrix/test_p8_action_router.result.json`.
- Intégration autonomie/requête, verrou, récupération après crash et écrivains multi-processus : **4 tests PASS**, `logs/O930_P8_resume_matrix/test_p8_integration.result.json`.
- Sécurité/adversarial : **20 tests PASS**, `logs/O930_P8_resume_matrix/test_p8_security.result.json`.
- Audit statique : **79 identifiants** dans le registre, 67 références UI, 28 CLI, zéro identifiant non enregistré; aucune écriture persistante UI détectée hors routeur. Les seules exceptions sans dispatch direct sont les lectures `sessions.get` et `sessions.list`. Reçu `logs/O930_P8_action_surface_static_audit.json`.
- La provenance de l’archive source est vérifiée et le test de fondation associé passe; l’archive et ses fichiers extraits ne sont pas modifiés par la matrice.
- Défauts initiaux — lien symbolique de checkpoint et écritures concurrentes du journal — restent consignés comme reproductions historiques, avec retests après correction.

## Interprétation des résultats
Les tests démontrent le comportement borné des chemins testés sur l’arbre local actuel. L’échec de provenance historique est résolu après l’inclusion de l’archive source au chemin portable attendu. Le bypass de sélection de discussion est résolu par l’action `chat-session-select`. Les tests n’établissent ni la sécurité d’un handler Python de confiance comme sandbox ni l’absence absolue de toute vulnérabilité.

## Conséquences théoriques, conceptuelles et opérationnelles
- **Théoriques :** l’intégrité de la chaîne `prev_hash` demeure distincte de la causalité de domaine; les deux liens ne sont pas confondus.
- **Conceptuelles :** capacité demandée ≠ permission accordée; contenu observé ≠ instruction fiable; succès local borné ≠ acceptation universelle.
- **Opérationnelles :** écritures concurrentes sérialisées; checkpoint sûr et vérifiable; actions UI/CLI/autonomie traçables; journaux et erreurs conservés.

## Erreurs, limites, conclusions et statut du modèle
Les alertes P8 réconciliées sont résolues dans `checklist_erreurs_model.json` et `checklist_erreurs_no_model.json`, preuves historiques conservées. La matrice complète précédente qui avait des échecs/interruptions reste historique et n’est pas effacée. La suite P9 stricte n’a pas été exécutée avant la fermeture de P8. La validation Windows native/ACL, les capteurs physiques, le fournisseur Web/MCP/API configuré, le crash/rollback externe et l’acceptation réseau réelle restent P10 `NOT_RUN`.

**Conclusion :** P8 = `COMPLETE_LOCAL_TESTED_BOUNDED`, sur le périmètre local ci-dessus. P9 = `NOT_STARTED` au moment de ce rapport. `implementation_complete_claimed=false` reste obligatoire.
