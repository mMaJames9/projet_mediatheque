"""
Point d'entrée de l'application de gestion de médiathèque.

- Charge le catalogue de livres depuis le fichier CSV
- Initialise la liste d'emprunt courante
- Affiche un menu en boucle permettant d'accéder à toutes les fonctionnalités
"""

from data import charger_catalogue
from ui import (
    afficher_menu_principal,
    saisir_choix_menu,
    menu_recherche,
    afficher_liste_emprunt,
    afficher_historique,
    action_ajout_livre,
    action_suppression_livre,
    action_validation_emprunt,
)


def main():
    """Fonction principale qui lance l'application."""

    print("Chargement du catalogue de livres...")
    catalogue = charger_catalogue()

    if not catalogue:
        print("[ATTENTION] Le catalogue est vide ou n'a pas pu être chargé.")
        print("Vous pouvez tout de même lancer le programme, mais certaines fonctionnalités seront limitées (aucun livre à emprunter).")

    # Liste d'emprunt courante (en mémoire uniquement)
    liste_emprunt = []

    # Boucle principale
    while True:
        afficher_menu_principal()
        choix = saisir_choix_menu(1, 7)

        if choix == 1:
            # Recherche
            menu_recherche(catalogue)

        elif choix == 2:
            # Ajout d'un livre à la liste d'emprunt
            action_ajout_livre(catalogue, liste_emprunt)

        elif choix == 3:
            # Suppression d'un livre de la liste d'emprunt
            action_suppression_livre(liste_emprunt)

        elif choix == 4:
            # Affichage de la liste d'emprunt courante
            afficher_liste_emprunt(liste_emprunt)

        elif choix == 5:
            # Validation de l'emprunt
            action_validation_emprunt(liste_emprunt)

        elif choix == 6:
            # Consultation de l'historique
            afficher_historique(catalogue)

        elif choix == 7:
            # Quitter
            print("Fermeture de l'application. Merci d'avoir utilisé la médiathèque.")
            break


if __name__ == "__main__":
    main()