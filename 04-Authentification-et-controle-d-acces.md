[← Chapitre précédent](03-Cryptographie-appliquee.md) · [Sommaire](Readme.md) · [Chapitre suivant →](05-Securite-des-applications.md)

# Authentification et contrôle d'accès

La majorité des intrusions ne commence pas par un exploit technique, mais par
un **identifiant valide** : volé par hameçonnage, deviné, réutilisé d'une
fuite précédente, ou oublié dans un notebook. Ce chapitre traite de la
question "qui êtes-vous ?" puis "qu'avez-vous le droit de faire ?".

## 🎯 Objectifs

- Distinguer identification, authentification et autorisation.
- Connaître les facteurs d'authentification et les formes de MFA, et leurs
  limites.
- Appliquer les recommandations actuelles sur les mots de passe.
- Comprendre un **JWT** et ses pièges.
- Appliquer le **moindre privilège** à une plateforme data.
- Gérer correctement des **secrets** (mots de passe, clés d'API, jetons).

---

## 1. Trois étapes distinctes

| Étape | Question | Exemple |
|---|---|---|
| **Identification** | Qui prétendez-vous être ? | saisir son identifiant `alice.martin` |
| **Authentification** | Prouvez-le. | saisir son mot de passe, valider sur son téléphone |
| **Autorisation** | Qu'avez-vous le droit de faire ? | lire la table `ventes`, mais pas `salaires` |

S'y ajoute la **traçabilité** (*accountability*) : enregistrer qui a fait quoi.
Ces quatre fonctions sont souvent réunies sous le sigle **IAM** (*Identity and
Access Management*).

## 2. Les facteurs d'authentification

| Facteur | Principe | Exemples |
|---|---|---|
| **Connaissance** | ce que je sais | mot de passe, code PIN, question secrète |
| **Possession** | ce que je possède | téléphone (application, SMS), clé de sécurité physique, carte à puce |
| **Inhérence** | ce que je suis | empreinte digitale, visage |

L'**authentification multifacteur** (MFA) combine au moins **deux facteurs de
natures différentes**. Deux mots de passe ne font pas une MFA.

Toutes les MFA ne se valent pas :

| Méthode | Résistance | Point faible |
|---|---|---|
| Code par **SMS** | faible | détournement de ligne (*SIM swapping*), hameçonnage en temps réel |
| Code **TOTP** (application d'authentification) | moyenne | un faux site peut demander le code et le rejouer aussitôt |
| **Notification** à valider | moyenne | "fatigue MFA" : l'attaquant envoie des dizaines de demandes jusqu'à ce que la victime accepte |
| **FIDO2 / WebAuthn** (clé de sécurité, *passkey*) | **forte** | résiste à l'hameçonnage : la clé vérifie elle-même l'adresse du site |

Même imparfaite, une MFA bloque l'immense majorité des attaques automatisées
sur les comptes. Elle est indispensable sur les accès à distance, les comptes
d'administration, les consoles cloud et les plateformes de données.

## 3. Les mots de passe aujourd'hui

Les recommandations ont changé ces dernières années (CNIL, ANSSI, NIST
SP 800-63B) :

- **La longueur prime sur la complexité.** La CNIL recommande au moins
  **12 caractères** mêlant majuscules, minuscules, chiffres et caractères
  spéciaux, ou **14 caractères** sans contrainte de composition. Une phrase de
  passe de plusieurs mots au hasard est à la fois robuste et mémorisable.
- **Pas de renouvellement périodique imposé** sans raison : il pousse à des
  mots de passe prévisibles (`Automne2025` → `Hiver2025`). On change le mot de
  passe en cas de soupçon de compromission.
- **Vérifier contre les listes de mots de passe fuités** à la création.
- **Un mot de passe différent par service**, ce qui suppose un **gestionnaire
  de mots de passe** (KeePassXC, Bitwarden…).
- **Limiter les tentatives** côté serveur (temporisation, blocage, captcha).

## 4. Les sessions et les jetons

Une fois authentifié, l'utilisateur reçoit un **jeton** qu'il présente à
chaque requête, pour ne pas ressaisir son mot de passe. Deux grandes familles :

- un **identifiant de session** opaque, stocké côté serveur et transmis par
  cookie ;
- un jeton **autoporteur**, qui contient lui-même les informations : le **JWT**
  (*JSON Web Token*), omniprésent dans les API.

### Anatomie d'un JWT

Un JWT est formé de trois parties encodées en **Base64url**, séparées par des
points :

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbGljZSIsInJvbGUiOiJsZWN0ZXVyIn0.4Hb0bWl…
└──────────── en-tête ──────────────┘ └───────────── charge utile ─────────────┘ └ signature ┘
{"alg":"HS256","typ":"JWT"}            {"sub":"alice","role":"lecteur"}
```

Le serveur signe l'en-tête et la charge utile ; à chaque requête, il vérifie
la signature avant de faire confiance au contenu.

> ⚠️ Un JWT est **signé, pas chiffré** : n'importe qui peut lire sa charge
> utile en décodant le Base64. On n'y met jamais d'information
> confidentielle.

Les pièges classiques :

| Piège | Conséquence |
|---|---|
| Accepter l'algorithme `none` | un jeton sans signature est accepté : on se donne le rôle que l'on veut |
| Secret HMAC faible (`HS256` avec `secret`, `changeme`…) | l'attaquant retrouve le secret par dictionnaire et **forge** des jetons |
| Lire l'algorithme dans le jeton au lieu de l'imposer | confusion d'algorithmes, contournement de la vérification |
| Pas d'expiration (`exp`) | un jeton volé reste valide indéfiniment |

### Délégation d'accès : OAuth 2.0 et OpenID Connect

Quand une application doit accéder à vos données chez un tiers ("Se connecter
avec…", un outil de BI qui lit votre Google Drive), on ne lui donne pas son
mot de passe. **OAuth 2.0** lui fait délivrer un jeton d'accès, limité en
**portée** (*scopes*) et en durée, par le fournisseur d'identité.
**OpenID Connect** ajoute à OAuth la couche d'authentification sur laquelle
reposent les **SSO** (authentification unique) d'entreprise.

---

## 5. L'autorisation

### Moindre privilège

Chaque utilisateur, application, compte de service - et chaque agent d'IA -
ne doit disposer que des **droits strictement nécessaires** à sa tâche, et
seulement **le temps nécessaire**. Une conséquence immédiate : on ne travaille
pas au quotidien avec un compte administrateur.

### Les modèles de contrôle d'accès

| Modèle | Principe | Exemple data |
|---|---|---|
| **RBAC** - par rôles | les droits sont attachés à des rôles, les rôles aux personnes | rôle `analyste_ventes` : lecture du schéma `ventes` |
| **ABAC** - par attributs | la décision dépend d'attributs de l'utilisateur, de la ressource, du contexte | lecture autorisée si `utilisateur.region == ligne.region` et accès depuis le réseau de l'entreprise |

Les entrepôts de données modernes savent appliquer ces règles finement :
**sécurité au niveau des lignes** (*row-level security* - chaque commercial ne
voit que ses clients) et **masquage de colonnes** (l'analyste voit
`j***@exemple.fr` au lieu de l'adresse complète).

### Le cycle de vie des accès

Les droits s'accumulent avec le temps : un stagiaire devenu salarié, un
changement de service, un projet terminé. D'où trois pratiques :

- **à l'arrivée** : attribuer des droits selon le rôle, pas "comme le
  collègue" ;
- **au départ** : désactiver les comptes **le jour même**, révoquer les clés et
  jetons associés ;
- **régulièrement** : **revue des droits** par les responsables métier, qui
  valident ou retirent.

Enfin, la **séparation des tâches** : une même personne ne doit pas pouvoir à
la fois créer un fournisseur et valider son paiement, ou développer un modèle
et l'approuver seule pour la production.

---

## 6. Les secrets

Un **secret** est tout ce qui donne un accès : mot de passe de base de données,
clé d'API, jeton d'accès, clé privée, chaîne de connexion. Les fuites de
secrets sont l'une des causes d'incident les plus fréquentes, et les métiers
de la donnée y sont particulièrement exposés : notebooks partagés, scripts
rapides, sorties de cellules affichant une connexion.

Des robots parcourent GitHub **en continu** : une clé cloud publiée par erreur
est exploitée en quelques minutes.

Les règles :

1. **Jamais de secret dans le code**, ni dans un notebook, ni dans une image
   Docker. On les lit dans des **variables d'environnement**, alimentées en
   local par un fichier `.env` **ignoré par git**.
2. En production, on utilise un **coffre-fort de secrets** : HashiCorp Vault,
   AWS Secrets Manager, Azure Key Vault, GCP Secret Manager, ou les secrets
   chiffrés de la plateforme CI/CD.
3. On **détecte** avant qu'il ne soit trop tard : un outil comme **gitleaks**
   ou **trufflehog** en *pre-commit* et dans la CI ; la protection des pushes
   de GitHub.
4. En cas de fuite, on **révoque d'abord**, on nettoie ensuite. Supprimer le
   fichier dans un nouveau commit ne sert à rien : le secret reste dans
   l'historique git, et il a peut-être déjà été copié.
5. On préfère les **identités sans secret** quand la plateforme le permet :
   rôles IAM attachés aux machines, fédération d'identité pour la CI (OIDC),
   jetons à courte durée de vie.

```python
# ❌ À ne pas faire
moteur = create_engine("postgresql://admin:Adm1n!@entrepot:5432/ventes")

# ✅ Le secret vient de l'environnement
import os
moteur = create_engine(os.environ["ENTREPOT_URL"])
```

---

## 🛠️ TP 1 - Forger un JWT

Les fichiers sont dans `tp/04-auth/`. Le fichier `jeton.txt`, généré pour vous
au chapitre 00, contient le JWT qu'une API a remis à l'utilisateur
`bruno.petit`.

```bash
docker compose run --rm lab
cd 04-auth
```

1. **Lisez** le contenu du jeton sans connaître la clé : quel rôle a Bruno ?
   Utilisez `jwt.get_unverified_header()` et
   `jwt.decode(jeton, options={"verify_signature": False})`.
2. Le serveur signe en `HS256`. **Retrouvez son secret** en essayant chaque mot
   de `../03-crypto/wordlist.txt` : `jwt.decode(jeton, mot,
   algorithms=["HS256"])` lève `jwt.InvalidSignatureError` quand la clé est
   fausse.
3. **Forgez** un jeton valide pour Bruno avec le rôle `admin`.
4. Quelles mesures auraient empêché l'attaque ?

> 📤 **À rendre** - le secret retrouvé et le jeton forgé, qui sera vérifié
> avec le secret de *votre* serveur :
>
> ```python
> consigner("04.secret_jwt", secret)
> consigner("04.jeton_admin", faux)
> ```

<details>
<summary>Voir la correction</summary>

> Les valeurs ci-dessous sont celles du **jeu de référence**. Votre secret est
> différent.

```python
import sys
import warnings

import jwt

sys.path.append("..")
from rendu import consigner

# Les versions récentes de PyJWT avertissent quand une clé HMAC fait moins de
# 32 octets : un bon signal en temps normal, du bruit pendant l'attaque.
warnings.simplefilter("ignore")

with open("jeton.txt", encoding="utf-8") as f:
    jeton = f.read().strip()

# 1. Lecture sans clé : la charge utile n'est qu'encodée
print(jwt.get_unverified_header(jeton))
print(jwt.decode(jeton, options={"verify_signature": False}))
# → {'sub': 'bruno.petit', 'role': 'lecteur', 'iat': ..., 'exp': ...}

# 2. Attaque par dictionnaire sur le secret HMAC
secret = None
with open("../03-crypto/wordlist.txt", encoding="utf-8") as f:
    for mot in (ligne.strip() for ligne in f):
        try:
            jwt.decode(jeton, mot, algorithms=["HS256"])
            secret = mot
            break
        except jwt.InvalidSignatureError:
            pass
print(f"Secret du serveur : {secret!r}")

# 3. Forge d'un jeton administrateur, accepté par le serveur
charge = jwt.decode(jeton, secret, algorithms=["HS256"])
charge["role"] = "admin"
faux = jwt.encode(charge, secret, algorithm="HS256")
print(faux)
print(jwt.decode(faux, secret, algorithms=["HS256"]))

consigner("04.secret_jwt", secret)
consigner("04.jeton_admin", faux)
```

Le secret est `bienvenue`, retrouvé instantanément. L'attaquant peut
désormais se fabriquer n'importe quelle identité avec n'importe quel rôle :
l'API n'y verra que du feu, puisque la signature est valide.

4. Mesures :
   - un secret **long et aléatoire** : `secrets.token_urlsafe(32)` donne 256
     bits d'aléa, hors de portée de toute attaque par dictionnaire. Les
     versions récentes de PyJWT le rappellent d'ailleurs par un avertissement
     `InsecureKeyLengthWarning` dès qu'une clé fait moins de 32 octets - un
     avertissement à ne pas faire taire en production ;
   - ou mieux, une signature **asymétrique** (`RS256`, `ES256`, `EdDSA`) : les
     API qui vérifient les jetons n'ont que la clé publique, et ne peuvent donc
     pas en fabriquer ;
   - le secret rangé dans un coffre-fort et **renouvelé** régulièrement ;
   - une **durée de vie courte** (`exp` à quelques minutes, avec un jeton de
     rafraîchissement) ;
   - le rôle vérifié côté serveur dans une source de vérité (annuaire, base),
     plutôt que cru sur parole dans le jeton, pour les actions sensibles.

</details>

## 🛠️ TP 2 - Débusquer les secrets

Le dossier `tp/04-auth/projet_exemple/` est un petit projet de scoring,
prêt à être publié sur GitHub. Il contient plusieurs secrets oubliés.

1. Écrivez `chercher_secrets.py`, qui parcourt récursivement un dossier et
   affiche, pour chaque fichier, les lignes qui ressemblent à un secret. Pensez
   aux affectations (`PASSWORD = "..."`), aux identifiants dans les URL
   (`postgresql://user:motdepasse@hote`), aux paramètres `apikey=`, aux JWT
   (`eyJ...`).
2. Combien de secrets trouvez-vous ? Lequel est correctement géré ?
3. Comment corriger ce projet avant de le publier ?

> 📤 **À rendre** - la liste des secrets trouvés, sous la forme
> `"fichier:ligne"`. Les fausses alertes coûtent des points :
>
> ```python
> consigner("04.secrets", ["projet_exemple/config.py:6", ...])
> ```

<details>
<summary>Voir la correction</summary>

```python
import pathlib
import re
import sys

MOTIFS = {
    "affectation": re.compile(
        # valeur littérale, entre guillemets ou non, mais pas une lecture
        # d'environnement (os.environ…, ${VARIABLE})
        r"""(?i)\b\w*(password|passwd|pwd|secret|token|api_?key)\w*\s*[:=]\s*(?!os\.|\$\{)["']?([^"'\s]{6,})"""),
    "identifiants dans une URL": re.compile(r"[a-z+]+://[^:/\s\"']+:([^@\s\"']+)@"),
    "clé dans une URL": re.compile(r"(?i)[?&](api_?key|token|key)=([\w-]{16,})"),
    "JWT": re.compile(r"eyJ[\w-]+\.eyJ[\w-]+\.[\w-]+"),
}

sys.path.append("..")
from rendu import consigner

racine = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "projet_exemple")
trouves = []
for fichier in sorted(p for p in racine.rglob("*") if p.is_file()):
    try:
        lignes = fichier.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        continue  # fichier binaire
    for numero, ligne in enumerate(lignes, 1):
        # premier motif reconnu seulement : une ligne n'est signalée qu'une fois
        nom = next((nom for nom, motif in MOTIFS.items() if motif.search(ligne)), None)
        if nom:
            trouves.append(f"{fichier.as_posix()}:{numero}")
            print(f"{fichier}:{numero}: [{nom}] {ligne.strip()[:90]}")
print(f"\n{len(trouves)} secret(s) potentiel(s)")
consigner("04.secrets", trouves)
```

Résultat : 5 secrets.

| Fichier | Secret |
|---|---|
| `config.py` | `DB_PASSWORD = "Scoring2025!"` |
| `pipeline.py` | la clé de l'API météo, dans l'URL |
| `docker-compose.yml` | `POSTGRES_PASSWORD: dev_s3cr3t_2025` |
| `notebooks/exploration.ipynb` | le mot de passe administrateur dans la chaîne de connexion, **et** un jeton de session dans la **sortie** d'une cellule |

Seul `STOCKAGE_TOKEN`, lu dans `os.environ`, est correctement géré : notre
script ne le signale pas, car aucune valeur n'est écrite.

Le notebook montre un piège typique : même si on corrige le code d'une
cellule, ses **sorties** enregistrées dans le fichier `.ipynb` peuvent
contenir des secrets ou des données personnelles. On les efface avant de
commiter (`jupyter nbconvert --clear-output`, ou l'outil `nbstripout` en
*pre-commit*).

3. Corrections :
   - remplacer chaque valeur par une lecture d'environnement
     (`os.environ["DB_PASSWORD"]`, `${POSTGRES_PASSWORD}` dans le
     `docker-compose.yml`) ;
   - fournir un `.env.example` avec des valeurs factices, et ajouter `.env`
     au `.gitignore` ;
   - effacer les sorties du notebook ;
   - **révoquer et renouveler** tous ces secrets : on doit les considérer comme
     compromis dès lors qu'ils ont été écrits dans un fichier partagé ;
   - installer un outil de détection en *pre-commit*. Par exemple, avec
     Docker :

```bash
docker run --rm -v "$PWD/projet_exemple:/src" zricethezav/gitleaks:latest dir /src
```

Un outil professionnel combine des centaines de motifs connus (clés AWS,
Slack, Stripe…) et une mesure d'**entropie** pour repérer les chaînes
aléatoires ; notre script naïf n'en est qu'une ébauche.

</details>

---

## 🧠 À retenir

- **MFA partout** où c'est possible, et de préférence résistante à
  l'hameçonnage (FIDO2, *passkeys*).
- Mots de passe : **longs**, **uniques**, dans un **gestionnaire**.
- Un JWT se **lit** sans clé ; il ne se **forge** pas si la clé est solide et
  l'algorithme imposé.
- **Moindre privilège** et **revue des droits** : les accès s'accumulent si on
  ne les retire pas.
- Un secret n'a rien à faire dans le code, un notebook ou une image ; une fois
  publié, il se **révoque**.

---

[← Chapitre précédent](03-Cryptographie-appliquee.md) · [Sommaire](Readme.md) · [Chapitre suivant →](05-Securite-des-applications.md)
