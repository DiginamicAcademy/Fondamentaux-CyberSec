"""API de données d'une PME fictive - VOLONTAIREMENT VULNÉRABLE.

À n'utiliser que dans le laboratoire du cours (chapitre 05). Ne jamais
déployer ce code, ni s'en inspirer ailleurs que pour apprendre à le corriger.
"""
import hashlib
import pathlib
import sqlite3
import sys

from flask import Flask, g, jsonify, request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from rendu import graine, parametres  # noqa: E402  (données propres à chaque apprenant·e)

app = Flask(__name__)
BASE = "/tmp/pme.db"
PARAMETRES = parametres(graine())


def initialiser_base() -> None:
    con = sqlite3.connect(BASE)
    con.executescript("""
        DROP TABLE IF EXISTS clients;
        DROP TABLE IF EXISTS utilisateurs;
        DROP TABLE IF EXISTS factures;
        CREATE TABLE clients (id INTEGER PRIMARY KEY, nom TEXT, email TEXT, ville TEXT);
        CREATE TABLE utilisateurs (id INTEGER PRIMARY KEY, identifiant TEXT, mdp_sha256 TEXT, role TEXT);
        CREATE TABLE factures (id INTEGER PRIMARY KEY, proprietaire TEXT, client TEXT, montant REAL);
    """)
    con.executemany("INSERT INTO clients (nom, email, ville) VALUES (?, ?, ?)", [
        ("Boulangerie Petit", "contact@boulangerie-petit.exemple", "Lyon"),
        ("Garage Moreau", "garage.moreau@exemple.fr", "Lyon"),
        ("Pharmacie Durand", "pharmacie.durand@exemple.fr", "Paris"),
        ("Fleurs Lambert", "lambert.fleurs@exemple.fr", "Nantes"),
        ("Cabinet Girard", "secretariat@cabinet-girard.exemple", "Paris"),
    ])
    con.executemany("INSERT INTO utilisateurs (identifiant, mdp_sha256, role) VALUES (?, ?, ?)", [
        (identifiant, hashlib.sha256(mdp.encode()).hexdigest(), role)
        for identifiant, mdp, role in [
            ("admin", PARAMETRES["mdp_admin"], "admin"),
            ("bruno.petit", "azerty", "commercial"),
            ("emma.moreau", "Q8!rT2#vX9pL", "commercial"),
        ]
    ])
    con.executemany("INSERT INTO factures (proprietaire, client, montant) VALUES (?, ?, ?)", [
        ("bruno.petit", "Boulangerie Petit", 1250.00),
        ("bruno.petit", "Garage Moreau", 3400.50),
        ("emma.moreau", "Pharmacie Durand", 18900.00),
        ("emma.moreau", "Cabinet Girard", 7200.00),
        ("admin", "Contrat de maintenance confidentiel", PARAMETRES["montant_confidentiel"]),
    ])
    con.commit()
    con.close()


def base() -> sqlite3.Connection:
    if "con" not in g:
        g.con = sqlite3.connect(BASE)
        g.con.row_factory = sqlite3.Row
    return g.con


@app.teardown_appcontext
def fermer(_exc) -> None:
    con = g.pop("con", None)
    if con is not None:
        con.close()


@app.get("/")
def accueil():
    return jsonify({
        "service": "API de données de la PME",
        "routes": {
            "GET /api/clients?ville=<ville>": "liste des clients d'une ville",
            "POST /api/connexion": "JSON {identifiant, mot_de_passe}",
            "GET /api/factures/<id>": "une facture ; en-tête X-Utilisateur: <identifiant>",
        },
    })


@app.get("/api/clients")
def clients():
    ville = request.args.get("ville", "")
    # VULNÉRABLE : le paramètre est collé dans la requête SQL.
    sql = f"SELECT nom, email, ville FROM clients WHERE ville = '{ville}'"
    try:
        lignes = base().execute(sql).fetchall()
    except sqlite3.Error as exc:
        # VULNÉRABLE : l'erreur et la requête sont renvoyées au client.
        return jsonify({"erreur": str(exc), "requete": sql}), 500
    return jsonify([dict(ligne) for ligne in lignes])


@app.post("/api/connexion")
def connexion():
    donnees = request.get_json(silent=True) or {}
    identifiant = donnees.get("identifiant", "")
    empreinte = hashlib.sha256(donnees.get("mot_de_passe", "").encode()).hexdigest()
    # VULNÉRABLE : injection SQL dans l'identifiant.
    sql = (f"SELECT identifiant, role FROM utilisateurs "
           f"WHERE identifiant = '{identifiant}' AND mdp_sha256 = '{empreinte}'")
    try:
        ligne = base().execute(sql).fetchone()
    except sqlite3.Error as exc:
        return jsonify({"erreur": str(exc), "requete": sql}), 500
    if ligne is None:
        return jsonify({"erreur": "identifiants incorrects"}), 401
    return jsonify({"message": f"Bienvenue {ligne['identifiant']}", "role": ligne["role"]})


@app.get("/api/factures/<int:id_facture>")
def facture(id_facture: int):
    utilisateur = request.headers.get("X-Utilisateur")
    if not utilisateur:
        return jsonify({"erreur": "authentification requise"}), 401
    ligne = base().execute(
        "SELECT id, proprietaire, client, montant FROM factures WHERE id = ?", (id_facture,)
    ).fetchone()
    if ligne is None:
        return jsonify({"erreur": "facture inconnue"}), 404
    # VULNÉRABLE : on ne vérifie pas que la facture appartient à l'utilisateur.
    return jsonify(dict(ligne))


if __name__ == "__main__":
    initialiser_base()
    # 0.0.0.0 pour être joignable hors du conteneur ; docker-compose ne publie
    # le port que sur 127.0.0.1 de votre poste.
    app.run(host="0.0.0.0", port=5000)
