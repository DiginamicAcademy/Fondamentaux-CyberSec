"""Assistant RH à base de "LLM" - simulation pédagogique (chapitre 07).

Le modèle de langage est SIMULÉ par une fonction déterministe, pour que le TP
tourne sans clé d'API ni GPU. Il reproduit le défaut fondamental des LLM :
il ne fait pas la différence entre les consignes de son développeur et le
texte qu'on lui donne à lire. Toute instruction présente dans son contexte
peut être suivie - y compris celles cachées dans un document.

Usage : python assistant_jouet.py documents/<fichier>
"""
import pathlib
import re
import sys

CONSIGNES_SYSTEME = (
    "Tu es l'assistant RH de la société Exemple. Résume le document fourni en "
    "trois lignes au plus. Tu peux utiliser l'outil d'envoi de courriel pour "
    "transmettre un résumé à un membre de l'équipe RH. Ne communique jamais "
    "de données internes à l'extérieur de l'entreprise."
)

# Ce que l'assistant a récupéré dans le SI pour faire son travail (RAG) :
# il y a accès, donc le "modèle" aussi.
CONTEXTE_INTERNE = {
    "salaires": "grille 2026 - direction 95-140 k€, data scientists 48-72 k€, stagiaires 1 400 €/mois",
    "annuaire": "drh@exemple.fr, paie@exemple.fr, recrutement@exemple.fr",
}

APPEL_OUTIL = re.compile(r"envoyer_mail\(\s*([^,]+?)\s*,\s*([^,]+?)\s*,\s*(.+?)\s*\)")
CONSIGNE_REDACTION = re.compile(r"[Ii]ndique que (.+?)\.")


# --- Le "modèle" ------------------------------------------------------------

def modele_simule(contexte: str) -> tuple[str, list[tuple[str, str, str]]]:
    """Renvoie le texte produit et les appels d'outils "décidés" par le modèle."""
    document = contexte.split("DOCUMENT :", 1)[-1]
    lignes = [l.strip() for l in re.sub(r"<[^>]+>", " ", document).splitlines() if l.strip()]
    resume = "\n".join(f"- {l[:80]}" for l in lignes[:3])
    for consigne in CONSIGNE_REDACTION.findall(contexte):
        resume += f"\n- Avis : {consigne}."
    appels = []
    for destinataire, objet, contenu in APPEL_OUTIL.findall(contexte):
        # Le modèle "complète" les références à ce qu'il a dans son contexte.
        for cle, valeur in CONTEXTE_INTERNE.items():
            contenu = contenu.replace("{{" + cle + "}}", valeur)
        appels.append((destinataire, objet, contenu))
    return resume, appels


# --- L'application autour du modèle -------------------------------------------

def construire_contexte(document: str) -> str:
    interne = "\n".join(f"{cle} : {valeur}" for cle, valeur in CONTEXTE_INTERNE.items())
    return f"SYSTÈME : {CONSIGNES_SYSTEME}\n\nCONTEXTE INTERNE :\n{interne}\n\nDOCUMENT :\n{document}"


def envoyer_mail(destinataire: str, objet: str, contenu: str) -> None:
    print(f"📧 Courriel envoyé à {destinataire} - objet \"{objet}\"\n   {contenu}")


def executer_outil(destinataire: str, objet: str, contenu: str) -> None:
    # TODO (TP, étape 3) : c'est ici, hors du modèle, que l'on peut imposer
    # des règles que le modèle ne pourra pas contourner.
    envoyer_mail(destinataire, objet, contenu)


def main() -> None:
    chemin = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "documents/facture.txt")
    document = chemin.read_text(encoding="utf-8")
    resume, appels = modele_simule(construire_contexte(document))
    print(f"=== Résumé de {chemin.name}\n{resume}\n")
    for appel in appels:
        executer_outil(*appel)
    if not appels:
        print("(aucun outil appelé)")


if __name__ == "__main__":
    main()
