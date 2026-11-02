"""Fabrique jeton.txt : le JWT qu'une API fictive a remis à bruno.petit.
Le serveur signe ses jetons en HS256 avec un secret… beaucoup trop faible."""
import pathlib
import warnings
from datetime import datetime, timezone

import jwt

warnings.simplefilter("ignore")  # PyJWT avertit, à raison, que la clé est trop courte

SECRET_DU_SERVEUR = "bienvenue"  # chut, c'est le secret à retrouver dans le TP

jeton = jwt.encode(
    {
        "sub": "bruno.petit",
        "role": "lecteur",
        "iat": int(datetime(2026, 1, 5, tzinfo=timezone.utc).timestamp()),
        "exp": int(datetime(2030, 1, 1, tzinfo=timezone.utc).timestamp()),
    },
    SECRET_DU_SERVEUR,
    algorithm="HS256",
)
pathlib.Path(__file__).with_name("jeton.txt").write_text(jeton + "\n", encoding="utf-8")
print(jeton)
