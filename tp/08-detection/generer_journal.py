"""Fabrique access_log.txt : une journée de journal d'accès (format "combined"
d'Apache et Nginx) d'une API de données fictive, avec quelques attaques
mêlées au trafic normal. Toutes les adresses IP sont des adresses réservées
à la documentation (RFC 5737).

Les attaquants, horaires et volumes dépendent de l'apprenant·e déclaré·e dans
../rendu.json ; sans rendu.json, on obtient le jeu de référence des
corrections.

L'extension .txt plutôt que .log : le .gitignore du dépôt ignore les *.log.
"""
import pathlib
import random
import sys
from datetime import datetime, timedelta
from urllib.parse import quote

ICI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ICI.parent))
from rendu import graine  # noqa: E402

JOUR = datetime(2026, 3, 12)
NAVIGATEURS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/133.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3) AppleWebKit/605.1.15 Version/17.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0",
]
VILLES = ["Lyon", "Paris", "Nantes", "Lille", "Bordeaux"]
CHEMINS_SCAN = ["/.env", "/.git/config", "/wp-login.php", "/phpmyadmin/", "/admin",
                "/backup.zip", "/api/../../etc/passwd", "/server-status", "/config.json",
                "/.aws/credentials", "/actuator/env", "/debug", "/console", "/api/swagger.json"]
INJECTIONS = ["'", "x' OR '1'='1", "x' OR 1=1 --", "x' UNION SELECT NULL --",
              "x' UNION SELECT NULL, NULL --", "x' UNION SELECT NULL, NULL, NULL --",
              "x' UNION SELECT name, sql, type FROM sqlite_master --",
              "x' UNION SELECT identifiant, mdp_sha256, role FROM utilisateurs --"]


def scenario(g: int | None) -> dict:
    """Paramètres de l'attaque."""
    if g is None:
        return {"ip_scanner": "203.0.113.66", "fichier_decouvert": "/api/swagger.json",
                "ip_force_brute": "192.0.2.77", "compte_compromis": "bruno.petit",
                "debut": JOUR + timedelta(hours=2, minutes=10), "tentatives": 412, "pages": 250,
                "attente_export": timedelta(minutes=3, seconds=35)}
    rng = random.Random(g)
    return {
        "ip_scanner": f"203.0.113.{rng.randint(2, 250)}",
        "fichier_decouvert": rng.choice(["/api/swagger.json", "/backup.zip", "/config.json", "/.env"]),
        "ip_force_brute": f"192.0.2.{rng.choice([n for n in range(2, 251) if n != 200])}",
        "compte_compromis": rng.choice(["bruno.petit", "emma.moreau", "lea.fontaine",
                                        "hugo.fournier", "ines.girard", "jules.bonnet"]),
        "debut": JOUR + timedelta(minutes=rng.randrange(30, 240)),
        "tentatives": rng.randint(150, 600),
        "pages": rng.randint(120, 320),
        "attente_export": timedelta(minutes=rng.randint(2, 8)),
    }


def generer(g: int | None) -> tuple[list[str], dict]:
    """Renvoie les lignes du journal et les faits que l'enquête doit retrouver."""
    rng = random.Random(808 if g is None else g)
    s = scenario(g)
    lignes = []

    def ajouter(ip, quand, methode, chemin, statut, taille, agent, utilisateur="-"):
        horodatage = quand.strftime("%d/%b/%Y:%H:%M:%S +0100")
        lignes.append((quand, f'{ip} - {utilisateur} [{horodatage}] "{methode} {chemin} HTTP/1.1" '
                              f'{statut} {taille} "-" "{agent}"'))

    # Trafic normal : 40 utilisateurs aux heures de bureau
    for n in range(40):
        ip = f"198.51.100.{10 + n}"
        agent = rng.choice(NAVIGATEURS)
        for _ in range(rng.randint(10, 40)):
            quand = JOUR + timedelta(hours=rng.uniform(8, 19))
            r = rng.random()
            if r < 0.55:
                ajouter(ip, quand, "GET", f"/api/clients?ville={rng.choice(VILLES)}", 200,
                        rng.randint(800, 4000), agent)
            elif r < 0.85:
                ajouter(ip, quand, "GET", f"/api/factures/{rng.randint(1, 900)}", 200,
                        rng.randint(300, 900), agent)
            elif r < 0.95:
                ajouter(ip, quand, "POST", "/api/connexion", rng.choice([200, 200, 200, 401]),
                        rng.randint(60, 120), agent)
            else:
                ajouter(ip, quand, "GET", "/favicon.ico", 404, 0, agent)

    # Robot d'indexation légitime
    for _ in range(60):
        ajouter("192.0.2.200", JOUR + timedelta(hours=rng.uniform(0, 24)), "GET", "/", 200, 512,
                "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")

    # Attaque 1 - scanner de vulnérabilités
    debut = s["debut"]
    for i, chemin in enumerate(CHEMINS_SCAN * 3):
        trouve = chemin == s["fichier_decouvert"]
        ajouter(s["ip_scanner"], debut + timedelta(seconds=i * 2), "GET", chemin,
                200 if trouve else 404, 1500 if trouve else 0, "Mozilla/5.0 zgrab/0.x")

    # Attaque 2 - injection SQL, 30 minutes plus tard
    debut = s["debut"] + timedelta(minutes=30)
    for i, charge in enumerate(INJECTIONS):
        statut = 500 if i in (0, 3, 4) else 200
        ajouter(s["ip_scanner"], debut + timedelta(seconds=i * 20), "GET",
                f"/api/clients?ville={quote(charge)}", statut, 300 if statut == 500 else 2200,
                "python-requests/2.32.3")

    # Attaque 3 - force brute sur la connexion, depuis une autre adresse
    debut = s["debut"] + timedelta(minutes=55)
    for i in range(s["tentatives"]):
        succes = i == s["tentatives"] - 1
        ajouter(s["ip_force_brute"], debut + timedelta(seconds=i * 0.5), "POST", "/api/connexion",
                200 if succes else 401, 95, "python-requests/2.32.3")
    compromission = debut + timedelta(seconds=(s["tentatives"] - 1) * 0.5)

    # Attaque 4 - exfiltration avec le compte compromis
    debut = compromission + s["attente_export"]
    volume = 0
    for page in range(1, s["pages"] + 1):
        taille = rng.randint(480_000, 520_000)
        volume += taille
        ajouter(s["ip_force_brute"], debut + timedelta(seconds=page * 3), "GET",
                f"/api/export?table=clients&page={page}", 200, taille,
                "python-requests/2.32.3", utilisateur=s["compte_compromis"])

    lignes.sort()
    faits = {
        "ip_scanner": s["ip_scanner"],
        "fichier_decouvert": s["fichier_decouvert"],
        "ip_force_brute": s["ip_force_brute"],
        "compte_compromis": s["compte_compromis"],
        "heure_compromission": compromission.strftime("%H:%M"),
        "volume_mo": round(volume / 1e6, 1),
    }
    return [ligne for _, ligne in lignes], faits


if __name__ == "__main__":
    lignes, _ = generer(graine())
    sortie = ICI / "access_log.txt"
    sortie.write_text("\n".join(lignes) + "\n", encoding="utf-8", newline="\n")
    print(f"{len(lignes)} lignes écrites dans {sortie.name}")
