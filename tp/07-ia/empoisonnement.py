"""TP du chapitre 07 - empoisonner un détecteur de fraude.

Le jeu de données est synthétique : 10 % de transactions frauduleuses (classe 1).
Complétez les parties marquées TODO.
"""
import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, recall_score
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=5000, n_features=10, n_informative=6,
                           weights=[0.9, 0.1], class_sep=1.5, flip_y=0,
                           random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,
                                                    stratify=y, random_state=0)
rng = np.random.default_rng(0)


def entrainer(X, y) -> RandomForestClassifier:
    return RandomForestClassifier(n_estimators=100, random_state=0).fit(X, y)


def evaluer(nom: str, modele, X, y) -> None:
    pred = modele.predict(X)
    print(f"{nom:35} exactitude = {accuracy_score(y, pred):.1%}   "
          f"fraudes détectées (rappel) = {recall_score(y, pred):.1%}")


# Référence : modèle entraîné sur des données saines
reference = entrainer(X_train, y_train)
evaluer("Modèle sain", reference, X_test, y_test)

# TODO Étape 1 - Inversion d'étiquettes : faites passer 50 % des fraudes
# du jeu d'entraînement pour des transactions normales, réentraînez, évaluez.

# TODO Étape 3 (facultative) - Porte dérobée : ajoutez au jeu d'entraînement des copies de
# 100 fraudes dont la dernière colonne vaut 8.0 (le "déclencheur"),
# étiquetées comme normales. Évaluez le modèle sur le jeu de test sain, puis
# sur les fraudes du jeu de test auxquelles on applique le déclencheur.
