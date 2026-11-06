# Livrables d’expérimentation eGenBrain v4

Le paquet rassemble le rapport, les protocoles verrouillés, les journaux bruts et scorés, les audits d’intégrité, les checklists, les snapshots et le reçu de rendu. Le rapport final fait 15 pages A4; le LaTeX et le PDF sont synchronisés par SHA-256, rendus par PDFium et Poppler, et inspectés visuellement. Les avertissements typographiques `Underfull \hbox` sont consignés; aucun `Overfull` ni référence non résolue n’a été trouvé.

L’archive séparée `bases_sqlite_eGenBrain_v4_exp.tar.zst` contient 4 476 fichiers SQLite et les sidecars/journaux présents (4 478 fichiers au total). Le contrôle indépendant a directement contrôlé 4 475 bases en lecture seule; une copie de sauvegarde nécessitant la récupération d’un journal a été contrôlée sur une copie isolée. Les originaux n’ont pas été modifiés.

Les résultats pilotes affectés par l’ouverture prématurée des références sont exploratoires et exclus de la conclusion confirmatoire. `ENVEXP-010` et les autres anomalies restent enregistrées; le rejeu préenregistré ne remplace que la vue analytique dérivée et n’écrit jamais dans les journaux bruts. Les sorties négatives, exceptions, abstentions, `NO_ASCR_RESULTS` et les cas où des modes du maillage font moins bien que les contrôles sont conservés.

Les sources `mesh_v4.py` et `v4.py` sont restées inchangées; aucun correctif `eGenBrain_v4_0` n’est livré. Le statut final est `completed_with_documented_findings`, et non « sans anomalie ». Les empreintes externes se trouvent dans `SHA256SUMS_eGenBrain_v4.txt`; l’archive SQLite possède son propre manifeste et un reçu de comparaison.
