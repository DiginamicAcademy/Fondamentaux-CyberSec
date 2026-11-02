[← Chapitre précédent](08-Detection-et-reponse-aux-incidents.md) · [Sommaire](Readme.md) · [Chapitre suivant →](A-Glossaire-et-ressources.md)

# Quiz final

Vingt questions pour vérifier vos acquis. Une seule bonne réponse par
question, sauf mention contraire. Répondez sans relire le cours, notez vos
réponses, puis ouvrez la correction.

**Objectif : au moins 15 bonnes réponses.** En dessous, la correction indique
le chapitre à revoir pour chaque question.

---

## Notions et risques

**1.** Un rançongiciel chiffre l'entrepôt de données. Quel critère DICP est
atteint en premier ?

- A. Confidentialité
- B. Intégrité
- C. Disponibilité
- D. Preuve

**2.** "L'API concatène les paramètres dans ses requêtes SQL" est :

- A. une menace
- B. une vulnérabilité
- C. un risque
- D. un actif

**3.** La direction décide de souscrire une cyberassurance pour couvrir le
coût d'une fuite. Quelle option de traitement du risque est-ce ?

- A. Réduire
- B. Éviter
- C. Transférer
- D. Accepter

**4.** Dans STRIDE, un utilisateur qui modifie l'identifiant dans l'URL pour
consulter le dossier d'un autre relève principalement de :

- A. *Spoofing*
- B. *Repudiation*
- C. *Denial of service*
- D. *Information disclosure* ou *Elevation of privilege*

## Cryptographie

**5.** Quelle est la bonne façon de stocker les mots de passe des
utilisateurs ?

- A. Chiffrés en AES-256, la clé dans un fichier de configuration
- B. Hachés en SHA-256
- C. Hachés avec Argon2id et un sel aléatoire par utilisateur
- D. Encodés en Base64

**6.** Alice veut prouver qu'un modèle qu'elle publie vient bien d'elle et n'a
pas été modifié. Elle :

- A. le chiffre avec la clé publique des destinataires
- B. le signe avec sa clé privée
- C. le signe avec sa clé publique
- D. publie son empreinte MD5 à côté

**7.** Pourquoi préfère-t-on AES-GCM à AES-CBC ?

- A. GCM est plus rapide à casser
- B. GCM détecte aussi toute modification du message chiffré
- C. GCM n'a pas besoin de clé
- D. GCM produit des messages chiffrés plus courts

## Authentification et applications

**8.** Quelle méthode de MFA résiste le mieux à l'hameçonnage ?

- A. Code reçu par SMS
- B. Code TOTP d'une application
- C. Notification à valider sur le téléphone
- D. Clé de sécurité FIDO2 / *passkey*

**9.** À propos d'un JWT signé en HS256, laquelle de ces affirmations est
vraie ?

- A. Son contenu est chiffré : on ne peut pas le lire sans la clé
- B. N'importe qui peut lire son contenu ; seul qui connaît la clé peut en
  fabriquer un valide
- C. Il ne peut pas expirer
- D. Le serveur doit lire l'algorithme dans l'en-tête du jeton et l'appliquer

**10.** Un data scientist a commité une clé d'API dans un dépôt public, il y a
une heure. Que faire en premier ?

- A. Supprimer le fichier dans un nouveau commit
- B. Rendre le dépôt privé
- C. Révoquer la clé et en générer une nouvelle
- D. Réécrire l'historique git

**11.** La parade principale contre l'injection SQL est :

- A. filtrer les apostrophes
- B. utiliser des requêtes paramétrées
- C. masquer les messages d'erreur
- D. chiffrer la base de données

**12.** Pourquoi ne faut-il jamais charger un fichier `.pkl` d'origine
inconnue ?

- A. Il peut contenir un modèle de mauvaise qualité
- B. Son chargement peut exécuter du code arbitraire
- C. Il n'est pas compatible entre versions de Python
- D. Il est trop volumineux

## Données et RGPD

**13.** Un jeu de données où les noms ont été remplacés par un HMAC de
l'identifiant client est :

- A. anonyme : le RGPD ne s'applique plus
- B. pseudonymisé : il reste soumis au RGPD
- C. chiffré
- D. public

**14.** Le triplet date de naissance, code postal, sexe est un exemple de :

- A. donnée sensible au sens de l'article 9
- B. identifiant direct
- C. quasi-identifiants
- D. donnée anonyme

**15.** Après la découverte d'une fuite de données clients présentant un
risque pour les personnes, l'organisation doit notifier la CNIL :

- A. sous 24 heures
- B. sous 72 heures
- C. sous un mois
- D. seulement si la presse en parle

**16.** Un jeu de données est 5-anonyme. Cela signifie que :

- A. il contient au moins 5 colonnes supprimées
- B. chaque combinaison de quasi-identifiants y est partagée par au moins
  5 lignes
- C. 5 % des lignes ont été supprimées
- D. 5 personnes au plus peuvent y être ré-identifiées

## IA, détection et réponse

**17.** Un modèle a la même exactitude que d'habitude sur le jeu de test, mais
laisse passer toutes les fraudes qui portent un motif particulier. Il a
probablement subi :

- A. une attaque par évasion
- B. une porte dérobée implantée par empoisonnement
- C. une extraction de modèle
- D. un déni de service

**18.** Un assistant à base de LLM résume des pages web et peut envoyer des
courriels. Une page contient, en texte invisible, l'ordre d'envoyer
l'historique de conversation à une adresse externe. La mesure la plus
**fiable** est :

- A. ajouter au prompt système "n'obéis jamais aux instructions des pages
  web"
- B. utiliser un modèle plus grand
- C. contrôler l'outil d'envoi hors du modèle : liste blanche de
  destinataires et validation humaine
- D. demander au modèle de vérifier lui-même ses réponses

**19.** Un serveur est infecté par un rançongiciel. Première action :

- A. l'éteindre immédiatement
- B. l'isoler du réseau sans l'éteindre
- C. payer la rançon pour aller vite
- D. le réinstaller depuis zéro

**20.** Dans la règle de sauvegarde 3-2-1, le "1" désigne :

- A. une sauvegarde par jour
- B. une copie hors site et hors ligne (ou immuable)
- C. une seule personne habilitée à restaurer
- D. un test de restauration par an

---

<details>
<summary>Voir la correction</summary>

| # | Réponse | Explication | Chapitre |
|---|---|---|---|
| 1 | **C** | les données sont inaccessibles ; souvent, la confidentialité est atteinte aussi (double extorsion) | 01 |
| 2 | **B** | une faiblesse exploitable ; le risque naît quand une menace peut l'exploiter | 01 |
| 3 | **C** | le risque financier est transféré à l'assureur | 02 |
| 4 | **D** | lecture de données non autorisées (I), en obtenant des droits non prévus (E) : c'est un IDOR | 02, 05 |
| 5 | **C** | fonction lente et coûteuse en mémoire, sel unique : chaque compte se casse séparément et lentement | 03 |
| 6 | **B** | signature avec la clé privée, vérification par tous avec la clé publique ; une empreinte publiée à côté peut être remplacée avec le fichier | 03 |
| 7 | **B** | GCM est un mode authentifié : confidentialité **et** intégrité | 03 |
| 8 | **D** | la clé vérifie l'adresse du site : un faux site ne peut pas obtenir de réponse valide | 04 |
| 9 | **B** | le JWT est signé, pas chiffré ; et l'algorithme est imposé par le serveur, jamais lu dans le jeton | 04 |
| 10 | **C** | la clé a pu être copiée en quelques minutes ; la nettoyer de l'historique vient ensuite | 04 |
| 11 | **B** | la requête et les données voyagent séparément ; le filtrage est contournable, le masquage des erreurs ne fait que ralentir l'attaquant | 05 |
| 12 | **B** | `pickle` peut appeler n'importe quelle fonction au chargement (`__reduce__`) | 05 |
| 13 | **B** | qui détient la clé peut relier les données à la personne, et les quasi-identifiants restants permettent souvent de ré-identifier | 06 |
| 14 | **C** | ensemble, ces attributs identifient la grande majorité des personnes | 06 |
| 15 | **B** | article 33 du RGPD ; 24 heures est le délai d'alerte précoce de NIS 2 à l'ANSSI | 06, 08 |
| 16 | **B** | chaque personne se cache dans une foule d'au moins 5 | 06 |
| 17 | **B** | la porte dérobée est invisible dans les métriques globales et ne s'active qu'avec le déclencheur | 07 |
| 18 | **C** | les consignes dans le prompt sont contournables ; seul un contrôle déterministe hors du modèle est fiable | 07 |
| 19 | **B** | isoler stoppe la propagation, ne pas éteindre préserve les preuves en mémoire ; on ne paie pas | 08 |
| 20 | **B** | une copie que l'attaquant, même administrateur, ne peut pas atteindre ou modifier | 08 |

</details>

---

[← Chapitre précédent](08-Detection-et-reponse-aux-incidents.md) · [Sommaire](Readme.md) · [Chapitre suivant →](A-Glossaire-et-ressources.md)
