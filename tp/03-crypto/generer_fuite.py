"""Fabrique fuite.csv : une base d'utilisateurs fictive dont les mots de passe
sont "protégés" par un MD5 sans sel - exactement ce qu'il ne faut pas faire.

Les mots de passe dépendent de l'apprenant·e déclaré·e dans ../rendu.json ;
sans rendu.json, on obtient le jeu de référence des corrections.
"""
import csv
import hashlib
import pathlib
import random
import string
import sys

ICI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ICI.parent))
from rendu import graine  # noqa: E402

IDENTIFIANTS = ["alice.martin", "bruno.petit", "chloe.durand", "david.leroy", "emma.moreau",
                "farid.benali", "gaelle.roux", "hugo.fournier", "ines.girard", "jules.bonnet",
                "karim.lambert", "lea.fontaine"]

REFERENCE = ["Marseille13", "azerty", "t7#Kq!vR2m@Lp9xW", "soleil", "azerty", "Paris2024",
             "correct-cheval-pile-agrafe", "123456", "chocolat", "Automne2025",
             "Qz9!fT4#wB8&nL2v", "motdepasse"]

MOTS_PHRASE = ["correct", "cheval", "pile", "agrafe", "nuage", "lampe", "fusee", "biscotte",
               "girafe", "tuile", "moulin", "citron", "orage", "violon", "tambour", "falaise"]


def generer(g: int | None) -> list[tuple[str, str]]:
    """Liste des (identifiant, mot de passe en clair)."""
    if g is None:
        return list(zip(IDENTIFIANTS, REFERENCE))
    rng = random.Random(g)
    mots = (ICI / "wordlist.txt").read_text(encoding="utf-8").split()
    faibles = rng.sample(mots, 8)
    alphabet = string.ascii_letters + string.digits + "!#$%&*?@"
    forts = ["".join(rng.choice(alphabet) for _ in range(16)) for _ in range(2)]
    phrase = "-".join(rng.sample(MOTS_PHRASE, 4))
    mots_de_passe = faibles + [faibles[0]] + forts + [phrase]  # un doublon parmi les faibles
    rng.shuffle(mots_de_passe)
    return list(zip(IDENTIFIANTS, mots_de_passe))


if __name__ == "__main__":
    comptes = generer(graine())
    sortie = ICI / "fuite.csv"
    with sortie.open("w", newline="", encoding="utf-8") as f:
        ecrivain = csv.writer(f)
        ecrivain.writerow(["identifiant", "md5"])
        for identifiant, mot_de_passe in comptes:
            ecrivain.writerow([identifiant, hashlib.md5(mot_de_passe.encode()).hexdigest()])
    print(f"{len(comptes)} comptes écrits dans {sortie.name}")
