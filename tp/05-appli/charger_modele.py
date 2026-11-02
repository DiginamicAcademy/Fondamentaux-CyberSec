"""Charge un modèle comme on le fait trop souvent : avec pickle, sans méfiance."""
import pickle
import sys

chemin = sys.argv[1] if len(sys.argv) > 1 else "modele_piege.pkl"
with open(chemin, "rb") as f:
    modele = pickle.load(f)
print("Modèle chargé :", modele)
