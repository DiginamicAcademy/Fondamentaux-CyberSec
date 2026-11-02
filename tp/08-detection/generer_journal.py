"""Fabrique access_log.txt : une journée de journal d'accès (format "combined"
d'Apache et Nginx) d'une API de données fictive, avec quelques attaques
mêlées au trafic normal. Toutes les adresses IP sont des adresses réservées
à la documentation (RFC 5737).

L'extension .txt plutôt que .log : le .gitignore du dépôt ignore les *.log.
"""
import pathlib
import random
from datetime import datetime, timedelta
from urllib.parse import quote

random.seed(808)
JOUR = datetime(2026, 3, 12)
lignes = []

NAVIGATEURS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/133.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3) AppleWebKit/605.1.15 Version/17.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0",
]
VILLES = ["Lyon", "Paris", "Nantes", "Lille", "Bordeaux"]


def ajouter(ip, quand, methode, chemin, statut, taille, agent, utilisateur="-"):
    horodatage = quand.strftime("%d/%b/%Y:%H:%M:%S +0100")
    lignes.append((quand, f'{ip} - {utilisateur} [{horodatage}] "{methode} {chemin} HTTP/1.1" '
                          f'{statut} {taille} "-" "{agent}"'))


# Trafic normal : 40 utilisateurs aux heures de bureau
for n in range(40):
    ip = f"198.51.100.{10 + n}"
    agent = random.choice(NAVIGATEURS)
    for _ in range(random.randint(10, 40)):
        quand = JOUR + timedelta(hours=random.uniform(8, 19))
        r = random.random()
        if r < 0.55:
            ajouter(ip, quand, "GET", f"/api/clients?ville={random.choice(VILLES)}", 200,
                    random.randint(800, 4000), agent)
        elif r < 0.85:
            ajouter(ip, quand, "GET", f"/api/factures/{random.randint(1, 900)}", 200,
                    random.randint(300, 900), agent)
        elif r < 0.95:
            ajouter(ip, quand, "POST", "/api/connexion", random.choice([200, 200, 200, 401]),
                    random.randint(60, 120), agent)
        else:
            ajouter(ip, quand, "GET", "/favicon.ico", 404, 0, agent)

# Robot d'indexation légitime
for _ in range(60):
    ajouter("192.0.2.200", JOUR + timedelta(hours=random.uniform(0, 24)), "GET", "/", 200, 512,
            "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")

# Attaque 1 - scanner de vulnérabilités, 02:10
debut = JOUR + timedelta(hours=2, minutes=10)
for i, chemin in enumerate(["/.env", "/.git/config", "/wp-login.php", "/phpmyadmin/", "/admin",
                            "/backup.zip", "/api/../../etc/passwd", "/server-status", "/config.json",
                            "/.aws/credentials", "/actuator/env", "/debug", "/console", "/api/swagger.json"] * 3):
    ajouter("203.0.113.66", debut + timedelta(seconds=i * 2), "GET", chemin,
            200 if chemin == "/api/swagger.json" else 404, 1500 if chemin == "/api/swagger.json" else 0,
            "Mozilla/5.0 zgrab/0.x")

# Attaque 2 - injection SQL, 02:40
debut = JOUR + timedelta(hours=2, minutes=40)
for i, charge in enumerate(["'", "x' OR '1'='1", "x' OR 1=1 --", "x' UNION SELECT NULL --",
                            "x' UNION SELECT NULL, NULL --", "x' UNION SELECT NULL, NULL, NULL --",
                            "x' UNION SELECT name, sql, type FROM sqlite_master --",
                            "x' UNION SELECT identifiant, mdp_sha256, role FROM utilisateurs --"]):
    statut = 500 if i in (0, 3, 4) else 200
    ajouter("203.0.113.66", debut + timedelta(seconds=i * 20), "GET",
            f"/api/clients?ville={quote(charge)}", statut, 300 if statut == 500 else 2200,
            "python-requests/2.32.3")

# Attaque 3 - force brute sur la connexion, 03:05, depuis une autre adresse
debut = JOUR + timedelta(hours=3, minutes=5)
for i in range(412):
    ajouter("192.0.2.77", debut + timedelta(seconds=i * 0.5), "POST", "/api/connexion",
            200 if i == 411 else 401, 95, "python-requests/2.32.3")

# Attaque 4 - exfiltration avec le compte compromis, 03:12
debut = JOUR + timedelta(hours=3, minutes=12)
for page in range(1, 251):
    ajouter("192.0.2.77", debut + timedelta(seconds=page * 3), "GET",
            f"/api/export?table=clients&page={page}", 200, random.randint(480_000, 520_000),
            "python-requests/2.32.3", utilisateur="bruno.petit")

lignes.sort()
sortie = pathlib.Path(__file__).with_name("access_log.txt")
sortie.write_text("\n".join(l for _, l in lignes) + "\n", encoding="utf-8")
print(f"{len(lignes)} lignes écrites dans {sortie.name}")
