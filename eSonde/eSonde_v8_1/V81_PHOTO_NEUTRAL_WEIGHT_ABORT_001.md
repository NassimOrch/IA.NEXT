# Rapport d'incident V81-PHOTO-NEUTRAL-WEIGHT-ABORT-001

Date locale : 2026-11-18T16:01:25+01:00

## Description

Une génération libre sur le prompt `Explain photosynthesis simply.` a été exécutée avec 1 000 000 Obsiss, 48 candidats, 12 tokens demandés, `first_state`, et l'option de non-réponse désactivée. Le nouveau poids neutre du repli linguistique était actif. Le processus a été interrompu par SIGKILL au cours du calcul de l'étape 8. Aucun fichier `result.json` final n'a été écrit.

Une tentative simultanée de lire intégralement en mémoire le profil JSON historique de 178 Mo a augmenté l'empreinte mémoire. Les événements cgroup disponibles indiquent `oom=2` et `oom_kill=2`. Cette attribution est fondée sur les événements système et le stderr du script ; aucune donnée perdue n'est supposée.

## Architecture et pipeline concernés

Runtime `EsondeV81ChatRuntime` → décodeur `generate_chat_v81` → proposition locale/OASST1 → calcul P exact sur la population complète → évaluation R groupée sur les mêmes lignes Obsiss → classement collectif des 16 canaux → extension du préfixe.

Le checkpoint `models/eSonde_v6/weights.bin` est resté en lecture seule. L'exécution n'utilisait pas de sous-échantillonnage Obsiss.

## Commande d'exécution

```bash
PYTHONPATH=src python -m esonde_v8.cli_v81 chat \
  --prompt "Explain photosynthesis simply." \
  --max-tokens 12 --beam-width 1 --candidate-limit 48 \
  --p-activation-mode first_state \
  --workspace /mnt/data/esonde_audit/v8_1_work \
  --output-dir /mnt/data/esonde_audit/v8_1_work/suivi_model_eSonde_v8_1/experiments/v81_photo_neutral_fallback_weight_fullpop_20261118/runtime \
  --json-out /mnt/data/esonde_audit/v8_1_work/suivi_model_eSonde_v8_1/experiments/v81_photo_neutral_fallback_weight_fullpop_20261118/result.json
```

## Résultats

- 8 décisions token terminées et journalisées.
- Préfixes cumulés : `photosynthesis is one of many other than by`.
- Huit pools ont chacun évalué 48 candidats sur la population d'un million.
- L'étape 8 avait terminé P et commencé avant l'interruption.
- Pas de réponse complète, pas de statut `GENERATED`, pas de hash de réponse.
- Les événements intermédiaires et les diagnostics R sont conservés ; leurs SHA-256 sont inscrits dans `partial_generation_receipt.json`.

## Interprétation

Il s'agit d'un incident de ressources, pas d'un résultat de qualité de génération. Les huit préfixes partiels ne constituent pas une réponse exploitable comme génération complète. Les propositions non pertinentes observées dans les classements restent toutefois un signal technique à examiner dans l'ablation du profil historique de cooccurrence.

## Conséquences

- Théorique : aucune modification des définitions Obsiss ou des opérateurs P/R n'est justifiée par cet incident.
- Conceptuelle : séparer le diagnostic de pertinence des sources de propositions du diagnostic de capacité de calcul.
- Opérationnelle : ne pas charger une seconde copie du profil de 178 Mo pendant une inférence ; effectuer les inspections hors processus ou par lecture en flux. Conserver les traces partielles et exécuter une ablation ciblée du seul canal historique `context_response`.

## Conclusion

Incident documenté. Aucun fichier source, poids ou résultat final n'a été déclaré perdu. Le modèle original reste inchangé. L'expérience doit être reprise après validation du correctif d'ablation et d'une sauvegarde complète pré-exécution.

## Statut du modèle

Prototype v8.1 en développement ; cohérence conversationnelle et généralisation toujours non démontrées. L'exécution est interrompue, sans conclusion sur le potentiel du modèle.
