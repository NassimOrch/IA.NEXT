# Sécurité des références et du réseau — ORDER80.2.1

## 1. Frontière de confiance

La configuration de références est la frontière d'autorisation. `allow_domains` contient les destinations de contenu ; `search_allow_domains` contient uniquement les moteurs de recherche autorisés. Un résultat de moteur ne peut jamais ajouter spontanément un domaine de contenu.

## 2. Validation des URL

Sont refusés : schémas autres que HTTP/HTTPS, URL avec credentials, IP littérales, ports non allowlistés, domaines hors périmètre et hôtes malformés. Les noms internationaux sont normalisés en IDNA.

## 3. DNS et SSRF

Le nom est résolu avant connexion. Toutes les adresses retournées doivent être publiques et ne doivent pas appartenir aux plages spéciales/privées/loopback/link-local/multicast. La connexion est ensuite faite sur l'IP vérifiée, avec SNI correspondant au nom d'hôte pour HTTPS.

Une politique applicative ne remplace pas la défense réseau en profondeur. OWASP recommande l'allowlist lorsque les destinations fiables sont connues et souligne les risques liés aux redirections et à la résolution DNS dans les défenses SSRF. citeturn150117search2turn150117search5

## 4. TLS

Pour HTTPS, `ssl.create_default_context()` est utilisé. La documentation Python indique que ce contexte active les certificats de confiance, la validation du certificat et la vérification du nom d'hôte par défaut. citeturn150117search1

## 5. Redirections

Elles sont désactivées par défaut. Si `max_redirects > 0`, chaque destination de redirection est revalidée dans la même frontière d'autorisation et doit rester conforme à la politique HTTPS. Cette approche suit le principe OWASP de ne pas laisser une redirection contourner la validation de destination. citeturn150117search2turn150117search5

## 6. Contenu

Le client accepte uniquement des types textuels bornés par taille. Les balises script/style/noscript/template sont retirées. Aucun contenu observé n'est exécuté.

## 7. Intégrité

Des SHA-256 optionnels peuvent être fournis par URL locale/web. Les fichiers locaux sont également bornés par taille et les liens symboliques sortant des racines autorisées sont rejetés.

## 8. Provenance

L'audit conserve les URLs/chemins, hashes, requêtes, étapes d'observation, erreurs, décisions de sécurité et données effectivement consommées. Cette conservation répond au besoin de traçabilité de provenance ; NIST traite la provenance et les risques de chaîne d'approvisionnement comme des éléments de contrôle de sécurité. citeturn150117search48

## 9. Limite importante

La pile de sécurité ne peut pas garantir à elle seule la sécurité globale d'un ordinateur connecte au réseau. Pour la production : proxy contrôlé, pare-feu de sortie, isolation, compte non privilégié et surveillance réseau sont recommandés.
