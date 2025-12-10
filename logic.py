"""
Logique métier de l'application :

- Fonctions de recherche dans le catalogue
- Gestion de la liste d'emprunt courante
- Validation d'un emprunt (enregistrement dans l'historique)

Les livres sont des dictionnaires avec les clés :
"code", "titre", "auteur", "note", "categories".
"""

from data import sauvegarder_emprunt


# -------------------- RECHERCHE --------------------

def rechercher_par_code(catalogue, code):
    """
    Recherche un livre dans le catalogue à partir de son code.

    - La recherche est insensible à la casse
    - Retourne le dictionnaire du livre si trouvé, sinon None
    """

    if code is None:
        return None

    code = code.strip().upper()
    if code == "":
        return None

    return catalogue.get(code)


def rechercher_par_titre(catalogue, texte_titre):
    """
    Recherche des livres dont le titre contient le texte donné.

    - Recherche partielle
    - Insensible à la casse
    - Retourne une liste de livres (peut être vide)
    """

    if texte_titre is None:
        return []

    fragment = texte_titre.strip().lower()
    if fragment == "":
        return []

    resultats = []

    for livre in catalogue.values():
        titre_minuscule = livre["titre"].lower()
        if fragment in titre_minuscule:
            resultats.append(livre)

    return resultats


def rechercher_par_categorie(catalogue, categorie):
    """
    Recherche des livres appartenant à une catégorie donnée.

    - Insensible à la casse
    - Retourne une liste de livres (possiblement vide)
    """

    if categorie is None:
        return []

    cat = categorie.strip().lower()
    if cat == "":
        return []

    resultats = []

    for livre in catalogue.values():
        # livre["categories"] est une liste de chaînes déjà en minuscules
        if cat in livre["categories"]:
            resultats.append(livre)

    return resultats


# -------------------- LISTE D'EMPRUNT --------------------

def ajouter_livre_emprunt(catalogue, liste_emprunt, code):
    """
    Ajoute un livre à la liste d'emprunt courante à partir de son code.

    - Vérifie que le code n'est pas vide
    - Vérifie que le livre existe dans le catalogue
    - Vérifie que le livre n'est pas déjà dans la liste d'emprunt
    - Ajoute le livre si tout est OK

    Affiche des messages d'information / d'erreur pour l'utilisateur.
    """

    if code is None:
        print("[ERREUR] Code vide. Merci de saisir un code valide.")
        return

    code = code.strip().upper()
    if code == "":
        print("[ERREUR] Code vide. Merci de saisir un code valide.")
        return

    # On cherche le livre dans le catalogue
    livre = catalogue.get(code)
    if livre is None:
        print(f"[ERREUR] Aucun livre avec le code '{code}'.")
        return

    # On vérifie si le livre est déjà dans la liste d'emprunt
    for l in liste_emprunt:
        if l["code"] == code:
            print(f"[INFO] Le livre '{livre['titre']}' est déjà dans la liste d'emprunt.")
            return

    # Tout est bon, on ajoute
    liste_emprunt.append(livre)
    print("[OK] Livre ajouté à la liste d'emprunt :", livre["titre"])


def supprimer_livre_emprunt(liste_emprunt, code):
    """
    Supprime un livre de la liste d'emprunt courante à partir de son code.

    - Vérifie que le code n'est pas vide
    - Supprime le livre s'il est présent
    - Affiche un message d'erreur sinon
    """

    if code is None:
        print("[ERREUR] Code vide. Merci de saisir un code valide.")
        return

    code = code.strip().upper()
    if code == "":
        print("[ERREUR] Code vide. Merci de saisir un code valide.")
        return

    for index, livre in enumerate(liste_emprunt):
        if livre["code"] == code:
            titre = livre["titre"]
            del liste_emprunt[index]
            print("[OK] Livre retiré de la liste d'emprunt :", titre)
            return

    print(f"[ERREUR] Le livre avec le code '{code}' n'est pas dans la liste d'emprunt.")


def valider_emprunt(liste_emprunt):
    """
    Valide l'emprunt :

    - Si la liste est vide, affiche un message et ne fait rien
    - Sinon, récupère les codes des livres, appelle la fonction de sauvegarde dans le fichier d'historique, puis vide la liste d'emprunt.
    """
    
    if not liste_emprunt:
        print("[INFO] La liste d'emprunt est vide. Rien à valider.")
        return

    # On extrait uniquement les codes des livres
    codes = []
    for livre in liste_emprunt:
        codes.append(livre["code"])

    # On enregistre l'emprunt dans le fichier
    sauvegarder_emprunt(codes)

    # On vide la liste pour la prochaine session
    liste_emprunt.clear()

    print("[OK] Emprunt validé et enregistré. La liste d'emprunt a été réinitialisée.")
