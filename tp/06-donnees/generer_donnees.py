"""Fabrique deux jeux de données entièrement fictifs :

- patients.csv : un extrait de dossiers médicaux, avec identité et diagnostic ;
- liste_electorale.csv : une liste "publique" avec nom, date de naissance,
  code postal et sexe, où figurent une partie des mêmes personnes.
"""
import csv
import pathlib
import random
import unicodedata
from datetime import date, timedelta

random.seed(2026)
ICI = pathlib.Path(__file__).parent

PRENOMS_F = ["Alice", "Camille", "Chloé", "Emma", "Inès", "Jade", "Léa", "Louise", "Manon", "Sarah",
             "Zoé", "Nadia", "Claire", "Julie", "Anne", "Lucie", "Yasmine", "Marie", "Elsa", "Rose"]
PRENOMS_M = ["Adam", "Bruno", "David", "Farid", "Gabriel", "Hugo", "Jules", "Karim", "Louis", "Lucas",
             "Mathis", "Nathan", "Paul", "Raphaël", "Thomas", "Victor", "Yanis", "Omar", "Marc", "Éric"]
NOMS = ["Martin", "Bernard", "Petit", "Durand", "Leroy", "Moreau", "Simon", "Laurent", "Lefebvre",
        "Michel", "Garcia", "Roux", "Fournier", "Girard", "Bonnet", "Dupont", "Lambert", "Fontaine",
        "Rousseau", "Vincent", "Benali", "Nguyen", "Mercier", "Blanc", "Guerin", "Faure", "Chevalier"]
CODES_POSTAUX = ["69001", "69003", "69006", "69007", "69100", "69200", "69300", "69500",
                 "38000", "38100", "38200", "38400", "01000", "01100", "01300"]
DIAGNOSTICS = ["hypertension", "diabète de type 2", "asthme", "dépression", "lombalgie",
               "migraine", "hypothyroïdie", "VIH", "cancer du sein", "insuffisance cardiaque"]


def sans_accents(texte: str) -> str:
    return unicodedata.normalize("NFKD", texte).encode("ascii", "ignore").decode()


def personne() -> dict:
    sexe = random.choice("FM")
    prenom = random.choice(PRENOMS_F if sexe == "F" else PRENOMS_M)
    nom = random.choice(NOMS)
    naissance = date(1940, 1, 1) + timedelta(days=random.randrange(365 * 65))
    return {
        "nom": nom, "prenom": prenom, "sexe": sexe,
        "date_naissance": naissance.isoformat(),
        "code_postal": random.choice(CODES_POSTAUX),
        "email": sans_accents(f"{prenom.lower()}.{nom.lower()}{random.randint(1, 99)}@exemple.fr"),
    }


patients = [personne() | {"diagnostic": random.choice(DIAGNOSTICS)} for _ in range(300)]
for i, p in enumerate(patients, 1):
    p["id_patient"] = f"P{i:04d}"

# 60 % des patients figurent sur la liste électorale, mêlés à 400 inconnus.
electeurs = [{k: p[k] for k in ("nom", "prenom", "date_naissance", "code_postal", "sexe")}
             for p in random.sample(patients, 180)]
electeurs += [{k: v for k, v in personne().items() if k != "email"} for _ in range(400)]
random.shuffle(electeurs)


def ecrire(nom: str, lignes: list[dict], colonnes: list[str]) -> None:
    with (ICI / nom).open("w", newline="", encoding="utf-8") as f:
        ecrivain = csv.DictWriter(f, fieldnames=colonnes)
        ecrivain.writeheader()
        ecrivain.writerows(lignes)
    print(f"{nom} : {len(lignes)} lignes")


ecrire("patients.csv", patients,
       ["id_patient", "nom", "prenom", "email", "sexe", "date_naissance", "code_postal", "diagnostic"])
ecrire("liste_electorale.csv", electeurs, ["nom", "prenom", "date_naissance", "code_postal", "sexe"])
