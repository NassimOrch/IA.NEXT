# ORDER72 e1 - synthèse d'audit

## Falsification réussie / corrections

- attribut caché : rejeté ;
- `getattr` dynamique : rejeté ;
- global caché : rejeté ;
- fermeture cachée : rejetée ;
- champ `correct` imbriqué : rejeté ;
- callback de feedback : supprimé ;
- mutation WM : hash inchangé ;
- entier géant : exact jusqu'à $2^{200}$ dans le cas testé ;
- ordre hôte : canonisé ;
- plan cache non déterministe : invalidé ;
- banc TreeBandit/DelayedBandit : corrigé avant interprétation.

## Limite restante

Le contrôle WM aléatoire et le WM volontairement inversé réussissent les tâches ouvertes actuelles. La causalité du WM appris n'est donc pas démontrée.
