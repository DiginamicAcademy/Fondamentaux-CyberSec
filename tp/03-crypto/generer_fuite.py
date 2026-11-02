"""Fabrique fuite.csv : une base d'utilisateurs fictive dont les mots de passe
sont "protégés" par un MD5 sans sel - exactement ce qu'il ne faut pas faire."""
import csv
import hashlib
import pathlib

UTILISATEURS = [
    ("alice.martin", "Marseille13"),
    ("bruno.petit", "azerty"),
    ("chloe.durand", "t7#Kq!vR2m@Lp9xW"),
    ("david.leroy", "soleil"),
    ("emma.moreau", "azerty"),
    ("farid.benali", "Paris2024"),
    ("gaelle.roux", "correct-cheval-pile-agrafe"),
    ("hugo.fournier", "123456"),
    ("ines.girard", "chocolat"),
    ("jules.bonnet", "Automne2025"),
    ("karim.lambert", "Qz9!fT4#wB8&nL2v"),
    ("lea.fontaine", "motdepasse"),
]

sortie = pathlib.Path(__file__).with_name("fuite.csv")
with sortie.open("w", newline="", encoding="utf-8") as f:
    ecrivain = csv.writer(f)
    ecrivain.writerow(["identifiant", "md5"])
    for identifiant, mot_de_passe in UTILISATEURS:
        ecrivain.writerow([identifiant, hashlib.md5(mot_de_passe.encode()).hexdigest()])
print(f"{len(UTILISATEURS)} comptes écrits dans {sortie.name}")
