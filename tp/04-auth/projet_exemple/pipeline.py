"""Récupère les données de météo et lance le scoring - projet fictif."""
import os

import requests

from config import BATCH_SIZE, MODEL_PATH

API_METEO = "https://api.meteo.exemple/v1/previsions?apikey=mk_9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c"
STOCKAGE_TOKEN = os.environ.get("STOCKAGE_TOKEN")  # celui-ci est bien géré


def recuperer_meteo(ville: str) -> dict:
    return requests.get(f"{API_METEO}&ville={ville}", timeout=10).json()


if __name__ == "__main__":
    print(recuperer_meteo("Lyon"), BATCH_SIZE, MODEL_PATH)
