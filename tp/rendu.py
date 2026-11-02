"""Le rendu des TP : un fichier rendu.json, complété au fil des chapitres, puis
déposé pour évaluation.

Depuis le dossier tp/ du laboratoire :

    python rendu.py init "Prénom Nom"          crée rendu.json et génère VOS données
    python rendu.py consigner <clé> <valeur>   enregistre une réponse (JSON ou texte)
    python rendu.py joindre <clé> <fichier>    joint le contenu d'un fichier
    python rendu.py etat                       indique ce qui est fait et ce qui manque

Depuis un script Python d'un sous-dossier (03-crypto/, 04-auth/…) :

    import sys; sys.path.append("..")
    from rendu import consigner

Les données des TP (mots de passe, secrets, adresses des attaquants…) sont
tirées de votre nom : chacun·e a les siennes, et les réponses de votre voisin·e
ne sont pas les vôtres.
"""
import argparse
import hashlib
import json
import pathlib
import random
import subprocess
import sys
import unicodedata
from datetime import datetime

ICI = pathlib.Path(__file__).resolve().parent
FICHIER = ICI / "rendu.json"

# Ce qui est attendu dans le rendu : clé → (chapitre, description, type).
# Le type "fichier" se renseigne avec `joindre`, les autres avec `consigner`.
ATTENDUS = {
    "01.incidents": ("01", 'critère DICP principal de chaque incident : {"1": "C", ...}', "valeur"),
    "02.stride": ("02", "analyse STRIDE du pipeline de la mutuelle (stride.md)", "fichier"),
    "03.mots_de_passe": ("03", 'mots de passe retrouvés : {"identifiant": "mot de passe", ...}', "valeur"),
    "03.comptes_identiques": ("03", "identifiants qui partagent le même mot de passe", "valeur"),
    "03.stocker": ("03", "script de stockage des mots de passe (stocker.py)", "fichier"),
    "04.secret_jwt": ("04", "secret de signature du serveur", "valeur"),
    "04.jeton_admin": ("04", "jeton forgé avec le rôle admin", "valeur"),
    "04.secrets": ("04", 'secrets trouvés : ["fichier:ligne", ...]', "valeur"),
    "05.mot_de_passe_admin": ("05", "mot de passe de l'administrateur de l'API", "valeur"),
    "05.montant_confidentiel": ("05", "montant de la facture confidentielle de l'administrateur", "valeur"),
    "05.app": ("05", "API corrigée (app.py)", "fichier"),
    "06.reidentifies": ("06", "nombre de patients ré-identifiés avec certitude", "valeur"),
    "06.jeu_anonyme": ("06", "jeu anonymisé (anonyme.csv)", "fichier"),
    "07.rappel_sain": ("07", "rappel du modèle sain, entre 0 et 1", "valeur"),
    "07.rappel_inverse": ("07", "rappel après inversion d'étiquettes, entre 0 et 1", "valeur"),
    "07.assistant": ("07", "assistant sécurisé (assistant_jouet.py)", "fichier"),
    "08.enquete": ("08", "conclusions de l'enquête (voir le chapitre 08)", "valeur"),
    "08.rapport": ("08", "rapport d'incident (rapport_incident.md)", "fichier"),
}

GENERATEURS = [
    "03-crypto/generer_fuite.py",
    "04-auth/generer_jeton.py",
    "06-donnees/generer_donnees.py",
    "08-detection/generer_journal.py",
]


# --- Personnalisation ----------------------------------------------------------

def normaliser(nom: str) -> str:
    sans_accents = unicodedata.normalize("NFKD", nom).encode("ascii", "ignore").decode()
    return " ".join(sans_accents.lower().split())


def graine_de(nom: str) -> int:
    return int(hashlib.sha256(normaliser(nom).encode()).hexdigest()[:8], 16)


def graine() -> int | None:
    """Graine de l'apprenant·e déclaré·e dans rendu.json ; None pour le jeu de référence."""
    if not FICHIER.exists():
        return None
    return graine_de(json.loads(FICHIER.read_text(encoding="utf-8"))["apprenant"])


def parametres(g: int | None) -> dict:
    """Secrets des TP 04 et 05, tirés de la graine. Sans graine : jeu de référence."""
    if g is None:
        return {"secret_jwt": "bienvenue", "mdp_admin": "Admin2025", "montant_confidentiel": 98000.0}
    mots = (ICI / "03-crypto" / "wordlist.txt").read_text(encoding="utf-8").split()
    rng = random.Random(g)
    return {
        "secret_jwt": rng.choice(mots),
        "mdp_admin": rng.choice(mots),
        "montant_confidentiel": float(rng.randrange(50_000, 150_000, 500)),
    }


# --- Lecture et écriture du rendu ---------------------------------------------

def charger() -> dict:
    if not FICHIER.exists():
        sys.exit('Pas de rendu.json : lancez d\'abord  python rendu.py init "Prénom Nom"')
    return json.loads(FICHIER.read_text(encoding="utf-8"))


def _ecrire(rendu: dict) -> None:
    rendu["modifie_le"] = datetime.now().isoformat(timespec="seconds")
    FICHIER.write_text(json.dumps(rendu, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _verifier_cle(cle: str, type_attendu: str) -> None:
    if cle not in ATTENDUS:
        sys.exit(f"Clé inconnue : {cle}. Clés possibles : {', '.join(ATTENDUS)}")
    if ATTENDUS[cle][2] != type_attendu:
        commande = "joindre" if ATTENDUS[cle][2] == "fichier" else "consigner"
        sys.exit(f'La clé {cle} se renseigne avec "{commande}".')


def consigner(cle: str, valeur) -> None:
    """Enregistre une réponse dans rendu.json."""
    _verifier_cle(cle, "valeur")
    rendu = charger()
    rendu["reponses"][cle] = valeur
    _ecrire(rendu)
    print(f"[rendu] {cle} consigné")


def joindre(cle: str, chemin: str | pathlib.Path) -> None:
    """Joint le contenu d'un fichier texte à rendu.json."""
    _verifier_cle(cle, "fichier")
    chemin = pathlib.Path(chemin)
    contenu = chemin.read_text(encoding="utf-8")
    rendu = charger()
    rendu["reponses"][cle] = {
        "fichier": chemin.name,
        "sha256": hashlib.sha256(contenu.encode()).hexdigest(),
        "contenu": contenu,
    }
    _ecrire(rendu)
    print(f"[rendu] {cle} : {chemin.name} joint ({len(contenu)} caractères)")


def etat() -> bool:
    rendu = charger()
    print(f"Rendu de {rendu['apprenant']} - {FICHIER}")
    manquants = 0
    for cle, (chapitre, description, _) in ATTENDUS.items():
        fait = cle in rendu["reponses"]
        manquants += not fait
        print(f"  [{'x' if fait else ' '}] {cle:26} {description}")
    print("Rendu complet : déposez rendu.json." if not manquants
          else f"{manquants} élément(s) manquant(s).")
    return manquants == 0


def init(nom: str, forcer: bool = False) -> None:
    if not nom.strip():
        sys.exit("Indiquez votre prénom et votre nom.")
    if FICHIER.exists() and not forcer:
        actuel = json.loads(FICHIER.read_text(encoding="utf-8"))["apprenant"]
        if normaliser(actuel) != normaliser(nom):
            sys.exit(f"rendu.json existe déjà au nom de {actuel}. "
                     "Ajoutez --forcer pour tout recommencer (vos réponses seront perdues).")
    if not FICHIER.exists() or forcer:
        _ecrire({"format": 1, "apprenant": nom.strip(),
                 "cree_le": datetime.now().isoformat(timespec="seconds"), "reponses": {}})
    print(f"Rendu de {nom.strip()} prêt. Génération de vos données personnelles :")
    for generateur in GENERATEURS:
        script = ICI / generateur
        subprocess.run([sys.executable, script.name], cwd=script.parent, check=True)


def main() -> None:
    analyseur = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commandes = analyseur.add_subparsers(dest="commande", required=True)
    c = commandes.add_parser("init", help="créer le rendu et générer ses données")
    c.add_argument("nom")
    c.add_argument("--forcer", action="store_true")
    c = commandes.add_parser("consigner", help="enregistrer une réponse")
    c.add_argument("cle")
    c.add_argument("valeur", help="une valeur JSON (nombre, liste, objet) ou du texte")
    c = commandes.add_parser("joindre", help="joindre un fichier")
    c.add_argument("cle")
    c.add_argument("fichier")
    commandes.add_parser("etat", help="voir ce qui manque")
    args = analyseur.parse_args()

    if args.commande == "init":
        init(args.nom, args.forcer)
    elif args.commande == "consigner":
        try:
            valeur = json.loads(args.valeur)
        except json.JSONDecodeError:
            valeur = args.valeur
        consigner(args.cle, valeur)
    elif args.commande == "joindre":
        joindre(args.cle, args.fichier)
    else:
        sys.exit(0 if etat() else 1)


if __name__ == "__main__":
    main()
