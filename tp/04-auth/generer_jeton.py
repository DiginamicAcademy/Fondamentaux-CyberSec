"""Fabrique jeton.txt : le JWT qu'une API fictive a remis à bruno.petit.
Le serveur signe ses jetons en HS256 avec un secret… beaucoup trop faible.

Le secret dépend de l'apprenant·e déclaré·e dans ../rendu.json ; sans
rendu.json, on obtient le jeu de référence des corrections.
"""
import pathlib
import sys
import warnings
from datetime import datetime, timezone

import jwt

ICI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ICI.parent))
from rendu import graine, parametres  # noqa: E402

warnings.simplefilter("ignore")  # PyJWT avertit, à raison, que la clé est trop courte


def generer(g: int | None) -> str:
    return jwt.encode(
        {
            "sub": "bruno.petit",
            "role": "lecteur",
            "iat": int(datetime(2026, 1, 5, tzinfo=timezone.utc).timestamp()),
            "exp": int(datetime(2030, 1, 1, tzinfo=timezone.utc).timestamp()),
        },
        parametres(g)["secret_jwt"],
        algorithm="HS256",
    )


if __name__ == "__main__":
    jeton = generer(graine())
    (ICI / "jeton.txt").write_text(jeton + "\n", encoding="utf-8", newline="\n")
    print("jeton.txt écrit")
