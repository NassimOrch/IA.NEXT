# Décision de confirmation externe EX7

**Décision : aucun jeu du paquet de sources n'est accepté comme confirmation externe vierge.**

Motifs documentés dans l'inventaire source :
- Wisconsin : développement historique EX3–EX6.
- Digits et Wine : déjà exposés à des expériences antérieures.
- SMS Spam Collection : déjà employé dans un pilote de validation externe antérieur ; le caractère textuel du domaine ne réinitialise pas son statut d'exposition.
- Screenplay : 4 000 lignes dont 2 000 doublons excédentaires ; en outre les usages antérieurs ne permettent pas de le considérer comme vierge.
- `batch_dataset.jsonl` : dernière ligne tronquée.
- `0000.parquet` : signature valide mais contenu non décodé, qualité/provenance non auditées.

En conséquence, EX7 est une campagne de **développement uniquement** sur Wisconsin. Aucun chiffre EX7 ne doit être présenté comme test externe indépendant ou preuve de généralisation inter-domaines. Cette décision favorise l'intégrité des expériences plutôt que l'utilisation artificielle d'un dataset imparfait ou déjà exposé.
