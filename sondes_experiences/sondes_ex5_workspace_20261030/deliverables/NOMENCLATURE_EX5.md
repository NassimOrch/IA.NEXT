# Nomenclature canonique EX5 — MIXA / micro-MIXA

## Décision terminologique vérifiée

Les prompts sources n'établissent pas quatre architectures différentes. Ils établissent deux niveaux conceptuels :

1. **MIXA** (famille générale, section 7 d'EX3) : combinaison explicite d'une branche adaptative, d'une banque de sondes RBF fixes et d'un mélange appris.
2. **micro-MIXA** (reconstruction compacte, section 7.4 d'EX4) : instanciation compacte de cette idée, initialement d4/k8, explorée dans EX4 puis EX5 avec proportions, gates, géométries, partage d'encodeur/centres et représentation question-only.

Les graphies **MiXA** et **micro-MiXA** n'ont pas de définition ou d'implémentation autonome dans les prompts EX3/EX4, les sources extraites ou le code EX5. Elles sont conservées comme alias de casse respectivement de MIXA et micro-MIXA. Aucun code n'est dupliqué artificiellement et aucun résultat n'est inventé pour ces alias.

Le nom legacy `mixa_micro_d4_k8` et les mentions `mixa_micro` des débris se rattachent à **micro-MIXA**, mais la valeur de 528 coefficients citée dans `debrit_0.txt` demeure `rapportée_non_vérifiable` : aucun checkpoint/code source EX3 équivalent n'a été retrouvé.

## Variantes effectivement livrées

- MIXA / micro-MIXA de proportions : A0/F4, A1/F3, A2/F2, A3/F1, A4/F0 ; mélange égal, gate global et gate conditionnel selon les campagnes.
- Géométries : d2/k4, d4/k4, d4/k8, d8/k4, d4/k16, avec bras égal et gate entrée lorsqu'enregistrés.
- Partage : encodeur partagé, centres séparés/partagés, gates globaux/conditionnels.
- Question-only : PCA-Q et encodeur Q-only, fixe/adaptatif/hybride, contrôles ablatifs.
- Deux niveaux question→réponse : hybride/hybride, fixe→adaptatif, adaptatif→fixe, réponse seule, branche seule, Q neutralisé et joint supervisé.
- Correcteur OOF : cinq modèles de base fold par graine, tête résiduelle fixe ou adaptative, forward X-only.
- Alternance A↔B : résiduel/non-résiduel, deux ordres, hétérogène fixe/adaptatif, joint et contrôle statique ; cycles stricts et gel Adam.
- RETRO : aucun, maturation, inverse, local-only, coordination immédiate/linéaire, gamma/delta, modulation du gradient, plus politiques d'optimiseur et post-activation.
- Déploiement : eager, TorchScript trace, TorchScript optimized (écart de parité non admissible), Numba v1 invalide, Numba v2 partiellement paritaire.

## Index complet

- `catalogue_variantes_ex5.csv` : identifiants de candidats exacts par version et registre JSONL.
- `catalogue_campagnes_ex5.csv` : familles, scripts, données, résultats et tests associés.
- `oof_artifact_manifest_ex5.csv` et `oof_artifact_audit_ex5.json` : complétude détaillée et hashes de l'OOF.
- `sha256_manifest_workspace_final.csv` : empreintes de tous les artefacts livrés (hors caches Python/pytest).


## Alias et règles de canonicalisation

| Chaîne rencontrée | Nom canonique | Interprétation | Implémentation distincte ? |
|---|---|---|---|
| `MIXA`, `mixa`, `MiXA` | `MIXA` (`MIXA_GENERAL`) | Famille générale adaptatif + banque fixe + mélange appris | Non pour les différences de casse |
| `micro-MIXA`, `micro-mixa`, `micro-MiXA` | `micro-MIXA` (`MICRO_MIXA`) | Instanciation compacte de la famille MIXA | Non pour les différences de casse |
| `mixa_micro_d4_k8` | `micro-MIXA` | Identifiant historique EX3/EX4 dans les débris | Pas de code/checkpoint historique autonome retrouvé |

Les chaînes sources originales ne sont jamais renommées dans les registres bruts. Les catalogues fournissent le nom canonique en plus de l'identifiant source. Il n'existe pas de résultat séparé à attribuer aux alias `MiXA` ou `micro-MiXA`.
