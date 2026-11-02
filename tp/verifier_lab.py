"""Vérifie que le laboratoire est prêt : bibliothèques présentes, dossiers en place."""
import importlib
import pathlib
import sys

MODULES = ["cryptography", "jwt", "pandas", "sklearn", "flask", "requests"]
DOSSIERS = ["03-crypto", "04-auth", "05-appli", "06-donnees", "07-ia", "08-detection"]

ok = True
print(f"Python {sys.version.split()[0]}")
for nom in MODULES:
    try:
        module = importlib.import_module(nom)
        print(f"  [OK] {nom} {getattr(module, '__version__', '')}")
    except ImportError:
        print(f"  [KO] {nom} introuvable")
        ok = False

racine = pathlib.Path(__file__).parent
for dossier in DOSSIERS:
    if not (racine / dossier).is_dir():
        print(f"  [KO] dossier {dossier} absent")
        ok = False

print("Laboratoire prêt !" if ok else "Laboratoire incomplet : relisez le chapitre 00.")
sys.exit(0 if ok else 1)
