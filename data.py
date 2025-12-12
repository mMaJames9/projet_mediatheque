"""
Fonctions liées à la lecture et à l'écriture dans les fichiers :
- chargement du catalogue depuis le CSV
- sauvegarde d'un emprunt
- lecture de l'historique des emprunts

Les livres sont représentés par des dictionnaires.
"""

import csv
import os
from datetime import datetime

from config import CATALOGUE_CSV, EMPRUNTS_FILE


def charger_catalogue(path=CATALOGUE_CSV):
    """
    Charge le catalogue depuis un fichier CSV.

    Retourne un dictionnaire où la clé est le code du livre (en majuscules)
    et la valeur est un dictionnaire représentant le livre.

    Gestion d'erreurs :
    - si le fichier n'existe pas, on retourne un catalogue vide et on affiche un message d'erreur
    - si la note est invalide, on met 0.0 par défaut
    - si des caractères ne sont pas décodables en Windows-1252 (cp1252), ils sont remplacés pour éviter que le programme ne plante
    """

    catalogue = {}

    if not os.path.exists(path):
        print("[ERREUR] Le fichier de catalogue n'existe pas :", path)
        return catalogue

    try:
        # errors='replace' pour remplacer les caractères illisibles au lieu de générer une erreur
        # On utilise cp1252 pour gérer correctement les fichiers avec BOM si ils sont présents
        with open(path, "r", encoding="cp1252", errors="replace", newline="") as fichier:
            # Utilisation de DictReader pour lire les lignes du fichier CSV en dictionnaires
            lecteur = csv.DictReader(fichier)

            for ligne in lecteur:
                code = ligne.get("code", "").strip().upper()
                titre = ligne.get("titre", "").strip()
                auteur = ligne.get("auteur", "").strip()

                # Conversion de la note en float
                note_brute = ligne.get("note", "").strip()
                try:
                    note = float(note_brute) if note_brute != "" else 0.0
                except ValueError:
                    note = 0.0

                # Catégories séparées par ";"
                categories_brutes = ligne.get("categories", "")
                categories = []
                for c in categories_brutes.split(";"):
                    c = c.strip().lower()
                    if c != "":
                        categories.append(c)

                if code == "":
                    continue

                livre = {
                    "code": code,
                    "titre": titre,
                    "auteur": auteur,
                    "note": note,
                    "categories": categories,
                }

                catalogue[code] = livre

    except Exception as e:
        print("[ERREUR] Problème lors du chargement du catalogue :", e)

    return catalogue


def sauvegarder_emprunt(codes_livres, path=EMPRUNTS_FILE):
    """
    Enregistre un emprunt dans le fichier d'historique.

    Format choisi:
    - une ligne par emprunt
    - chaque ligne : date | code1, code2, code3

    Exemple :
    2025-12-08 14:35:12 | L01, L02, L15
    """

    if not codes_livres:
        # Rien à sauvegarder
        return

    # On construit la ligne à écrire
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    codes_str = ", ".join(codes_livres)
    ligne = date_str + " | " + codes_str + "\n"

    try:
        with open(path, "a", encoding="utf-8") as fichier:
            fichier.write(ligne)
    except Exception as e:
        print("[ERREUR] Impossible de sauvegarder l'emprunt :", e)


def charger_historique(path=EMPRUNTS_FILE):
    """
    Charge l'historique des emprunts depuis le fichier texte.

    Retourne une liste de dictionnaires de la forme :
    [
        {"datetime": "...", "codes": ["L01", "L02"]},
        ...
    ]

    Gestion d'erreurs :
    - si le fichier n'existe pas, on retourne une liste vide
    - si une ligne est mal formée, on l'ignore
    """

    historique = []

    if not os.path.exists(path):
        # Pas encore d'emprunts enregistrés
        return historique

    try:
        with open(path, "r", encoding="utf-8") as fichier:
            for ligne in fichier:
                ligne = ligne.strip()
                if ligne == "":
                    # Ligne vide, on passe
                    continue

                # On s'attend à "date | codes"
                morceaux = ligne.split(" | ")
                if len(morceaux) != 2:
                    # Ligne mal formée, on ignore
                    continue

                date_str = morceaux[0].strip()
                codes_str = morceaux[1].strip()

                if codes_str == "":
                    codes = []
                else:
                    # On sépare les codes par des virgules
                    codes = []
                    for c in codes_str.split(", "):
                        c = c.strip().upper()
                        if c != "":
                            codes.append(c)

                historique.append({
                    "datetime": date_str,
                    "codes": codes
                })

    except Exception as e:
        print("[ERREUR] Problème lors du chargement de l'historique :", e)

    return historique