"""Configuration du pipeline de scoring - projet fictif pour le TP du chapitre 04."""

DB_HOST = "entrepot.interne.exemple"
DB_PORT = 5432
DB_USER = "scoring_app"
DB_PASSWORD = "Scoring2025!"  # TODO : à sortir du code un jour

BATCH_SIZE = 500
MODEL_PATH = "modeles/scoring_v3.pkl"
