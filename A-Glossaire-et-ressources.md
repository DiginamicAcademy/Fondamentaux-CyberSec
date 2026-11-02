[← Chapitre précédent](09-Quiz-final.md) · [Sommaire](Readme.md)

# Glossaire et ressources

## Glossaire

| Terme | Définition |
|---|---|
| **Actif** | ce qui a de la valeur pour l'organisation et doit être protégé : données, modèles, applications, matériel, réputation |
| **AIPD** | analyse d'impact relative à la protection des données, obligatoire avant un traitement à risque élevé (RGPD, art. 35) |
| **ANSSI** | Agence nationale de la sécurité des systèmes d'information |
| **Authentification** | vérification de l'identité revendiquée |
| **Autorisation** | décision d'accorder ou non un accès à une ressource |
| **CERT-FR** | centre gouvernemental de veille, d'alerte et de réponse aux attaques informatiques |
| **CVE** | identifiant public d'une vulnérabilité connue (*Common Vulnerabilities and Exposures*) |
| **CVSS** | score de gravité d'une vulnérabilité, de 0 à 10 |
| **DICP** | Disponibilité, Intégrité, Confidentialité, Preuve : les critères de sécurité de l'information |
| **Défense en profondeur** | empilement de protections indépendantes |
| **EBIOS RM** | méthode d'analyse de risques de l'ANSSI |
| **EDR** | agent de détection et de réponse installé sur les postes et serveurs |
| **Empoisonnement** | manipulation des données d'entraînement d'un modèle |
| **Évasion** | modification d'une entrée pour tromper un modèle en production |
| **Exfiltration** | sortie non autorisée de données hors du SI |
| **Hachage** | calcul d'une empreinte de taille fixe, non réversible |
| **Hameçonnage** (*phishing*) | message frauduleux visant à obtenir des identifiants ou à faire exécuter une action |
| **HMAC** | empreinte calculée avec une clé secrète, qui garantit l'origine et l'intégrité |
| **IAM** | gestion des identités et des accès |
| **IDOR** | accès direct à un objet d'un autre utilisateur, faute de contrôle d'accès |
| **Injection** | donnée interprétée comme du code : SQL, commande, prompt |
| **Injection de prompt** | instruction malveillante qui détourne un LLM ; *indirecte* quand elle est cachée dans une donnée lue par le modèle |
| **IOC** | indicateur de compromission : IP, domaine, empreinte de fichier malveillant |
| **JWT** | jeton signé contenant des informations sur l'utilisateur |
| **k-anonymat** | propriété d'un jeu où chaque combinaison de quasi-identifiants est partagée par au moins k lignes |
| **KMS / HSM** | service / boîtier matériel de gestion des clés cryptographiques |
| **MFA** | authentification à plusieurs facteurs de natures différentes |
| **Menace** | cause potentielle d'un incident |
| **Moindre privilège** | n'accorder que les droits strictement nécessaires |
| **NIS 2** | directive européenne sur la cybersécurité des entités essentielles et importantes |
| **OWASP** | fondation qui publie des références libres sur la sécurité applicative |
| **Porte dérobée** (*backdoor*) | accès ou comportement caché ; dans un modèle, réaction apprise à un déclencheur |
| **Pseudonymisation** | remplacement des identifiants directs par un pseudonyme ; les données restent personnelles |
| **Quasi-identifiant** | attribut anodin seul, identifiant en combinaison avec d'autres |
| **Rançongiciel** (*ransomware*) | logiciel qui chiffre les données et exige une rançon |
| **Risque** | possibilité qu'une menace exploite une vulnérabilité et cause un dommage ; vraisemblance × gravité |
| **RPO / RTO** | perte de données maximale admissible / durée maximale d'interruption |
| **Sel** | valeur aléatoire ajoutée à un mot de passe avant hachage |
| **SIEM** | outil de collecte et de corrélation des journaux de sécurité |
| **SOC** | équipe de surveillance et de réponse aux incidents |
| **STRIDE** | méthode de modélisation des menaces : *Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege* |
| **Surface d'attaque** | ensemble des points d'entrée possibles pour un attaquant |
| **TLS** | protocole de chiffrement des communications (le "S" de HTTPS) |
| **Vulnérabilité** | faiblesse exploitable |
| **Zéro confiance** | aucune confiance implicite accordée selon la position dans le réseau |

---

## Ressources

### Références institutionnelles

- [ANSSI - Guide d'hygiène informatique](https://cyber.gouv.fr/publications/guide-dhygiene-informatique) : les 42 mesures de base.
- [ANSSI - Recommandations de sécurité pour un système d'IA générative](https://cyber.gouv.fr/publications/recommandations-de-securite-pour-un-systeme-dia-generative)
- [ANSSI - La méthode EBIOS Risk Manager](https://cyber.gouv.fr/la-methode-ebios-risk-manager)
- [CERT-FR](https://www.cert.ssi.gouv.fr/) : alertes et avis de sécurité.
- [CNIL - Guide de la sécurité des données personnelles](https://www.cnil.fr/fr/securite-des-donnees)
- [CNIL - Recommandations sur les mots de passe](https://www.cnil.fr/fr/mots-de-passe-une-nouvelle-recommandation-pour-maitriser-sa-securite)
- [CNIL - Fiches pratiques IA](https://www.cnil.fr/fr/intelligence-artificielle)
- [Cybermalveillance.gouv.fr](https://www.cybermalveillance.gouv.fr/) : assistance aux victimes et fiches de sensibilisation.

### Référentiels techniques

- [OWASP Top 10](https://owasp.org/Top10/) : les risques des applications web.
- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/) : les risques des applications à base de LLM.
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/) : fiches pratiques par sujet (mots de passe, injection, JWT…).
- [MITRE ATT&CK](https://attack.mitre.org/) : techniques des attaquants.
- [MITRE ATLAS](https://atlas.mitre.org/) : techniques d'attaque contre les systèmes d'IA.
- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework)
- [NIST SP 800-63B](https://pages.nist.gov/800-63-4/sp800-63b.html) : authentification et mots de passe.

### Outils vus dans le cours

| Outil | Usage |
|---|---|
| [`cryptography`](https://cryptography.io/) | primitives cryptographiques en Python |
| [`argon2-cffi`](https://argon2-cffi.readthedocs.io/) | hachage de mots de passe Argon2id |
| [`bandit`](https://bandit.readthedocs.io/) | analyse statique de code Python |
| [`pip-audit`](https://github.com/pypa/pip-audit) | dépendances Python vulnérables |
| [`gitleaks`](https://github.com/gitleaks/gitleaks) | détection de secrets |
| [`trivy`](https://trivy.dev/) | vulnérabilités des images et dépendances |
| [OWASP ZAP](https://www.zaproxy.org/) | test dynamique d'applications web |
| [`modelscan`](https://github.com/protectai/modelscan) | analyse des fichiers de modèles |
| [`safetensors`](https://huggingface.co/docs/safetensors) | format de poids de modèles sans exécution de code |

### Pour s'entraîner légalement

- [Root Me](https://www.root-me.org/) : plateforme française de challenges de sécurité.
- [TryHackMe](https://tryhackme.com/) et [Hack The Box](https://www.hackthebox.com/) : laboratoires guidés.
- [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/) : application volontairement vulnérable, à lancer en local avec Docker.
- [Gandalf](https://gandalf.lakera.ai/) : jeu d'injection de prompt.

---

[← Chapitre précédent](09-Quiz-final.md) · [Sommaire](Readme.md)
