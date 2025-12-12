"""
Interface utilisateur (console) :

- Affichage du menu principal
- Saisie sécurisée des choix
- Affichage des listes de livres sous forme de tableaux
- Sous-menu de recherche
- Affichage de la liste d'emprunt
- Affichage de l'historique des emprunts
"""

from config import EMPRUNTS_FILE
from data import charger_historique
from logic import (
    rechercher_par_code,
    rechercher_par_titre,
    rechercher_par_categorie,
    ajouter_livre_emprunt,
    supprimer_livre_emprunt,
    valider_emprunt,
)


# -------------------- TABLEAU DE LIVRES --------------------

def afficher_tableau_livres(livres, titre_tableau=None):
    """
    Affiche une liste de livres sous forme de tableau en console.

    Colonnes :
    - Code
    - Titre
    - Auteur
    - Note
    - Catégories

    Si la liste est vide, affiche un message adapté.
    """
    if not livres:
        print("Aucun livre à afficher.")
        return

    # Noms des colonnes
    entetes = ["Code", "Titre", "Auteur", "Note", "Catégories"]

    # Calcul de la largeur de chaque colonne
    largeur_code = len(entetes[0])
    largeur_titre = len(entetes[1])
    largeur_auteur = len(entetes[2])
    largeur_note = len(entetes[3])
    largeur_cat = len(entetes[4])

    for livre in livres:
        largeur_code = max(largeur_code, len(livre["code"]))
        largeur_titre = max(largeur_titre, len(livre["titre"]))
        largeur_auteur = max(largeur_auteur, len(livre["auteur"]))

        # Note affichée avec un chiffre après la virgule
        note_str = f"{livre['note']:.1f}"
        largeur_note = max(largeur_note, len(note_str))
        cats_str = ", ".join(livre["categories"])
        largeur_cat = max(largeur_cat, len(cats_str))

    # Largeur totale (pour la ligne de séparation)
    largeur_totale = (
        largeur_code + largeur_titre + largeur_auteur +
        largeur_note + largeur_cat + 4 * 3  # 4 séparateurs " | "
    )

    if titre_tableau is not None:
        print(titre_tableau)

    # Affichage de l'en-tête
    print(
        f"{entetes[0]:<{largeur_code}} | "
        f"{entetes[1]:<{largeur_titre}} | "
        f"{entetes[2]:<{largeur_auteur}} | "
        f"{entetes[3]:<{largeur_note}} | "
        f"{entetes[4]:<{largeur_cat}}"
    )
    print("-" * largeur_totale)

    # Affichage des lignes
    for livre in livres:
        note_str = f"{livre['note']:.1f}"
        cats_str = ", ".join(livre["categories"])
        print(
            f"{livre['code']:<{largeur_code}} | "
            f"{livre['titre']:<{largeur_titre}} | "
            f"{livre['auteur']:<{largeur_auteur}} | "
            f"{note_str:<{largeur_note}} | "
            f"{cats_str:<{largeur_cat}}"
        )


# -------------------- MENU PRINCIPAL --------------------

def afficher_menu_principal():
    """Affiche le menu principal de l'application."""

    print("\n===== MENU PRINCIPAL - MÉDIATHÈQUE =====\n")
    print("1. Rechercher des livres dans le catalogue")
    print("2. Ajouter un livre à la liste d'emprunt")
    print("3. Supprimer un livre de la liste d'emprunt")
    print("4. Afficher la liste d'emprunt courante")
    print("5. Valider l'emprunt")
    print("6. Consulter l'historique des emprunts")
    print("7. Quitter")
    print("\n========================================\n")


def saisir_choix_menu(min_val, max_val):
    """
    Demande à l'utilisateur de saisir un choix de menu entre min_val et max_val.

    Gestion des erreurs :
    - saisie vide
    - caractères non numériques
    - nombre hors plage
    """

    while True:
        saisie = input("Votre choix : ").strip()

        if saisie == "":
            print("[ERREUR] Saisie vide. Merci de saisir un numéro de menu.")
            continue

        if not saisie.isdigit():
            print("[ERREUR] Merci de saisir un numéro de menu valide.")
            continue

        choix = int(saisie)
        if choix < min_val or choix > max_val:
            print(f"[ERREUR] Merci de saisir un nombre entre {min_val} et {max_val}.")
            continue

        return choix


# -------------------- LISTE D'EMPRUNT --------------------

def afficher_liste_emprunt(liste_emprunt):
    """
    Affiche la liste d'emprunt courante sous forme de tableau.

    Indique également le nombre total de livres.
    """

    if not liste_emprunt:
        print("\nVotre liste d'emprunt est actuellement vide.")
        return

    print("\nNombre total de livres dans la liste :", len(liste_emprunt))
    afficher_tableau_livres(liste_emprunt, "\n--- Liste d'emprunt courante ---")


# -------------------- RECHERCHE --------------------

def menu_recherche(catalogue):
    """
    Affiche un sous-menu de recherche et gère les actions de l'utilisateur :

    1. Recherche par code
    2. Recherche par titre (partiel)
    3. Recherche par catégorie
    4. Retour au menu principal
    """

    print("\n--- Recherche de livres ---")
    print("1. Recherche par code")
    print("2. Recherche par titre (partiel)")
    print("3. Recherche par catégorie")
    print("4. Retour au menu principal")

    choix = saisir_choix_menu(1, 4)

    # Recherche par code
    if choix == 1:
        code = input("Entrez le code du livre : ")
        livre = rechercher_par_code(catalogue, code)
        if livre is not None:
            afficher_tableau_livres([livre], "\nRésultat :")
        else:
            print("[INFO] Aucun livre trouvé avec ce code.")
        return

    # Recherche par titre
    if choix == 2:
        fragment = input("Entrez une partie du titre : ")
        resultats = rechercher_par_titre(catalogue, fragment)
        if not resultats:
            print("[INFO] Aucun livre trouvé avec ce critère.")
        else:
            titre = f"\n{len(resultats)} livre(s) trouvé(s) :"
            afficher_tableau_livres(resultats, titre)
        return

    # Recherche par catégorie
    if choix == 3:
        cat = input("Entrez une catégorie : ")
        resultats = rechercher_par_categorie(catalogue, cat)
        if not resultats:
            print("[INFO] Aucun livre trouvé dans cette catégorie.")
        else:
            titre = f"\n{len(resultats)} livre(s) trouvé(s) :"
            afficher_tableau_livres(resultats, titre)
        return

    # Retour
    if choix == 4:
        return


# -------------------- HISTORIQUE --------------------

def afficher_historique(catalogue):
    """
    Affiche l'historique des emprunts en lisant le fichier d'historique.

    Pour chaque emprunt, on affiche :
    - le numéro d'emprunt
    - la date/heure
    - un tableau des livres trouvés dans le catalogue
    - la liste des codes inconnus (si certains livres ne sont plus dans le catalogue)
    """
    historique = charger_historique(EMPRUNTS_FILE)

    if not historique:
        print("\nAucun emprunt enregistré pour le moment.")
        return

    print("\n===== HISTORIQUE DES EMPRUNTS =====")

    for index, record in enumerate(historique, start=1):
        date_str = record.get("datetime", "Date inconnue")
        codes = record.get("codes", [])

        print(f"\n--- Emprunt #{index} ---")
        print("Date :", date_str)

        if not codes:
            print("Aucun livre enregistré pour cet emprunt.")
            continue

        livres_trouves = []
        codes_inconnus = []

        # On reconstitue les livres connus à partir du catalogue
        for code in codes:
            livre = catalogue.get(code)
            if livre is not None:
                livres_trouves.append(livre)
            else:
                codes_inconnus.append(code)

        if livres_trouves:
            afficher_tableau_livres(livres_trouves, "Livres empruntés :")
        else:
            print("Aucun des livres de cet emprunt n'est présent dans le catalogue actuel.")

        if codes_inconnus:
            print("\nCodes non trouvés dans le catalogue actuel :")
            for c in codes_inconnus:
                print(" -", c)

    print("\n===================================")


# -------------------- ACTIONS SUR LA LISTE (APPEL LOGIC) --------------------

def action_ajout_livre(catalogue, liste_emprunt):
    """Demande un code à l'utilisateur et appelle la fonction d'ajout."""
    code = input("Code du livre à ajouter : ")
    ajouter_livre_emprunt(catalogue, liste_emprunt, code)


def action_suppression_livre(liste_emprunt):
    """Demande un code à l'utilisateur et appelle la fonction de suppression."""
    code = input("Code du livre à retirer : ")
    supprimer_livre_emprunt(liste_emprunt, code)


def action_validation_emprunt(liste_emprunt):
    """Valide l'emprunt en appelant la fonction de logique métier."""
    valider_emprunt(liste_emprunt)