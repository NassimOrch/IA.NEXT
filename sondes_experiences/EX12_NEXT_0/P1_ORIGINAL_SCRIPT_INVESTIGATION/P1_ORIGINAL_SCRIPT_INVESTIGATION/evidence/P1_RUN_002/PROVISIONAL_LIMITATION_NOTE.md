# P1_RUN_002 — statut et limite de comparaison

Ce run intermédiaire est conservé en totalité et porte 420 lignes de synthèse, 16 800 mesures brutes et 54 tests sans échec. Il n'est toutefois pas utilisé pour conclure sur la parcimonie top-q : ses kernels `topq_select_and_readout_q*` ne mesuraient que la sélection/lecture sur activations déjà préparées, alors que la référence dense concurrente incluait davantage d'étapes. La comparaison n'était donc pas end-to-end appariée.

Le run corrigé P1_RUN_003 puis sa réplication P1_RUN_004 comparent dans les deux cas :
- dense : distance + activation gaussienne + lecture dense ;
- sparse : distance + activation gaussienne + top-k + gather des poids + lecture sparse.

Conclusion fondée exclusivement sur ces comparaisons corrigées : le top-q n'est pas plus rapide en p50 sur les tailles testées. P1_RUN_002 reste un essai exploratoire non agrégé. Son script original exact n'a pas été retrouvé dans le workspace; cette lacune est explicitement inscrite au registre.
