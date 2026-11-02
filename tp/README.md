# Laboratoire des TP

Tout se lance depuis ce dossier, avec Docker. Rien n'est à installer sur votre
poste en dehors de Docker Desktop (ou Docker Engine + le plugin Compose).

```bash
docker compose build                                # une fois : construit l'image cyber-lab
docker compose run --rm lab python verifier_lab.py  # vérifie le laboratoire
docker compose run --rm lab                         # ouvre un terminal dans le laboratoire
docker compose up api                               # lance l'API vulnérable du chapitre 05
docker compose run --rm lab python rendu.py init "Prénom Nom"   # crée le rendu et VOS données
docker compose run --rm lab python rendu.py etat    # ce qui reste à rendre
```

Le fichier `rendu.json` est le seul à rendre : il rassemble vos réponses et
les fichiers joints au fil des TP (voir le chapitre 00). Les données des TP
sont générées à partir de votre nom par `rendu.py init` : elles sont
différentes pour chaque apprenant·e.

| Dossier | Chapitre | Contenu |
|---|---|---|
| `03-crypto/` | 03 - Cryptographie appliquée | fuite de mots de passe, dictionnaire |
| `04-auth/` | 04 - Authentification | jeton JWT, faux projet truffé de secrets |
| `05-appli/` | 05 - Sécurité des applications | API Flask vulnérable, modèle `pickle` piégé |
| `06-donnees/` | 06 - Protection des données | jeu de données patients fictif, liste électorale fictive |
| `07-ia/` | 07 - Sécurité de l'IA | assistant jouet, documents piégés |
| `08-detection/` | 08 - Détection et réponse | journal d'accès d'un serveur web |

Toutes les données sont **fictives** et générées par les scripts `generer_*.py`
présents dans chaque dossier ; lancés sans `rendu.json`, ils produisent le jeu
de référence utilisé dans les corrections. Les attaques ne visent que vos propres
conteneurs : n'utilisez jamais ces techniques contre un système sans
autorisation écrite de son propriétaire.
