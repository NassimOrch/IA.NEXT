# Vérification de compilation LaTeX — M-028

- Date : 15 novembre 2026
- Documents : 4
- Passes : 8 (deux par document)
- Erreurs fatales : 0
- Débordements horizontaux (`Overfull \hbox`) : 0
- Avertissements de justification (`Underfull \hbox`) : 82 au total, répartis dans le manifeste détaillé
- Miroirs audit et runtime : identiques octet pour octet aux quatre sources canoniques
- Contrôle des terminateurs : un `\end{document}` par source, dernier élément effectif du document

Les avertissements `Underfull` indiquent des lignes dont la justification est moins dense ; aucun débordement horizontal n'est signalé dans ce run. Le contrôle a porté sur les sources TeX et les journaux de compilation. L'inspection visuelle des PDF n'a pas été effectuée, conformément à la priorité demandée.

Fichiers de journaux : `Amodel_eSonde_v7/formalism/build_logs/20261115_m028/`.
