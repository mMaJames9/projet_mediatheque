# Projet – Gestion de Médiathèque (Console)

Application Python en ligne de commande permettant de gérer les **emprunts de livres** dans une médiathèque : recherche de livres, constitution d’une liste d’emprunt, validation et consultation de l’historique.

Projet structuré avec une organisation propre en plusieurs fichiers et une bonne gestion des erreurs / des saisies utilisateur.

---

## Objectifs du projet

- Charger un **catalogue de livres** depuis un fichier CSV (`livres.csv`).
- Permettre à l’utilisateur de :
  - rechercher des livres (par **code**, **titre** ou **catégorie**) ;
  - ajouter / retirer des livres d’une **liste d’emprunt courante** ;
  - afficher cette liste sous forme de **tableau** ;
  - **valider** un emprunt et l’enregistrer de façon persistante (`emprunts.txt`) ;
  - consulter l’**historique** des emprunts précédents.

Le tout en console, avec un **menu clair**, une **gestion de la casse** (codes et catégories) et une **gestion robuste des erreurs** (mauvaises saisies, fichier manquant, etc.).

---

## Structure du projet

```
mediatheque/
├─ config.py        # Constantes de configuration (noms de fichiers)
├─ data.py          # Gestion des fichiers (CSV + historique)
└─ emprunts.txt     # Historique des emprunts (créé automatiquement)
├─ livres.csv       # Catalogue des livres (fourni)
├─ logic.py         # Logique métier (recherches, liste d’emprunt)
├─ main.py          # Point d’entrée de l’application (boucle principale)
├─ ui.py            # Interface console (menus, affichages en tableau)
````

### Rôle de chaque fichier

* **`main.py`**

  * Lance l’application.
  * Charge le catalogue.
  * Initialise la liste d’emprunt.
  * Gère la boucle du menu principal.

* **`config.py`**

  * Centralise les paramètres :

    * `CATALOGUE_CSV` : chemin du fichier catalogue.
    * `EMPRUNTS_FILE` : chemin du fichier d’historique.

* **`data.py`**

  * Fonctions liées aux fichiers :

    * `charger_catalogue()` : lit `livres.csv` et renvoie un dictionnaire de livres.
    * `sauvegarder_emprunt(codes_livres)` : enregistre un emprunt dans `emprunts.txt`.
    * `charger_historique()` : lit l’historique des emprunts.
  * Gère les problèmes d’encodage et les lignes mal formées.

* **`logic.py`**

  * Regroupe la **logique métier** :

    * `rechercher_par_code(...)`
    * `rechercher_par_titre(...)`
    * `rechercher_par_categorie(...)`
    * `ajouter_livre_emprunt(...)`
    * `supprimer_livre_emprunt(...)`
    * `valider_emprunt(...)`
  * Manipule des **dictionnaires Python simples** pour représenter les livres.

* **`ui.py`**

  * Tout ce qui touche à l’**interface console** :

    * Affichage du menu principal.
    * Saisie sécurisée des choix (`saisir_choix_menu`).
    * Sous-menu de recherche.
    * Affichage des livres sous forme de **tableaux alignés**.
    * Affichage de la liste d’emprunt courante.
    * Affichage de l’historique des emprunts.
    * Fonctions “pont” entre l’utilisateur (`input`) et la logique métier.

---

## Prérequis

* **Python 3.8+** (testé avec Python 3.11+).
* Un terminal / invite de commande.
* Le fichier `livres.csv` présent à la racine du projet.

### Encodage du CSV

Le programme lit `livres.csv` en **UTF-8 avec gestion souple des erreurs** :

* `encoding="utf-8-sig", errors="replace"`
* Si certains caractères sont mal encodés, ils sont remplacés automatiquement pour éviter un crash (par exemple pour certains caractères accentués).

---

## Installation & lancement

1. Cloner ou copier le dossier du projet :

```bash
git clone https://github.com/mMaJames9/projet_mediatheque mediatheque
cd mediatheque
```

2. Vérifier que les fichiers suivants sont présents :

* `main.py`
* `config.py`
* `data.py`
* `logic.py`
* `ui.py`
* `livres.csv`

3. Lancer l’application :

```bash
python main.py
```

> Sous Windows, selon la configuration, la commande peut être `py main.py`.

---

## Fonctionnement général

Au lancement :

```text
Chargement du catalogue de livres...

===== MENU PRINCIPAL - MÉDIATHÈQUE =====

1. Rechercher des livres dans le catalogue
2. Ajouter un livre à la liste d'emprunt
3. Supprimer un livre de la liste d'emprunt
4. Afficher la liste d'emprunt courante
5. Valider l'emprunt
6. Consulter l'historique des emprunts
7. Quitter

========================================

Votre choix :
```

L’utilisateur navigue avec un simple **numéro de menu**.

---

## Détail des fonctionnalités

### 1. Recherche de livres

Menu : `1. Rechercher des livres dans le catalogue`

Sous-menu proposé :

* `1` – Recherche par **code**
* `2` – Recherche par **titre** (recherche partielle, insensible à la casse)
* `3` – Recherche par **catégorie** (insensible à la casse)
* `4` – Retour au menu principal

Les résultats sont affichés sous forme de **tableau**, par exemple :

```text
3 livre(s) trouvé(s) :
Code | Titre               | Auteur               | Note | Catégories
--------------------------------------------------------------------
L01  | Le Petit Prince     | Antoine de Saint-Ex… | 4.8  | classique, jeunesse
L05  | Le Rouge et le Noir | Stendhal             | 4.6  | classique, roman
...
```

### 2. Ajout d’un livre à la liste d’emprunt

Menu : `2. Ajouter un livre à la liste d'emprunt`

* Saisie du **code du livre**.
* Le code est normalisé en **majuscule**.
* Si le livre n’existe pas, alors on affiche un message d’erreur.
* Si le livre est déjà dans la liste, on affiche plutôt un message d’information.
* Sinon, afficher le livre est ajouté.

### 3. Suppression d’un livre de la liste d’emprunt

Menu : `3. Supprimer un livre de la liste d'emprunt`

* Saisie du **code du livre**.
* Vérification si le livre est dans la liste.
* Suppression si trouvé, message d’erreur sinon.

### 4. Visualisation de la liste d’emprunt

Menu : `4. Afficher la liste d'emprunt courante`

* Affiche le **nombre total de livres**.
* Affiche un **tableau** des livres empruntés :

  * Code
  * Titre
  * Auteur
  * Note
  * Catégories

### 5. Validation de l’emprunt

Menu : `5. Valider l'emprunt`

* Si la liste est vide, on affiche un simple message d’info, aucune écriture.
* Sinon :

  * Récupère la liste des **codes**.

  * Enregistre une ligne dans `emprunts.txt` avec le format :

    ```text
    YYYY-MM-DD HH:MM:SS|L01,L02,L15
    ```

  * Vide la liste d’emprunt pour une nouvelle session.

### 6. Consultation de l’historique

Menu : `6. Consulter l'historique des emprunts`

* Lit `emprunts.txt` ligne par ligne.
* Pour chaque emprunt :

  * Affiche la **date/heure**.
  * Reconstruit les livres connus à partir du catalogue.
  * Affiche les livres trouvés en **tableau**.
  * Liste les **codes inconnus** (si certains livres n’existent plus dans le catalogue).

---

## Gestion des erreurs & robustesse

Le projet fait un effort particulier sur la robustesse :

* **Saisies utilisateur** :

  * Menus : refuse les saisies vides, non numériques ou hors plage.
  * Codes de livres : normalisation en majuscules, vérification vide / inexistant.
  * Recherche : retour de listes vides proprement, messages explicites.

* **Fichiers** :

  * Si `livres.csv` est absent, alors afficher catalogue vide + message d’alerte,
    mais l’appli ne crash pas.
  * Si `emprunts.txt` n’existe pas, alors historique vide (cas normal).

* **Encodage** :

  * Lecture du CSV en `utf-8-sig` avec `errors="replace"` pour éviter les exceptions sur des caractères mal encodés.
  * Les caractères problématiques sont remplacés, pas bloquants.

* **Lignes mal formées** dans l’historique :

  * Ignorées sans faire planter l’application.

---

## Format des données

### 1. `livres.csv` (entrée)

Colonnes attendues :

```text
code,titre,auteur,note,categories
L01,Le Petit Prince,Antoine de Saint-Exup�,4.8,classique;jeunesse
L02,L���,Albert Camus,4.5,classique;philosophie
...
```

* `code` : identifiant unique du livre (ex. `L01`).
* `titre` : titre du livre.
* `auteur` : nom de l’auteur.
* `note` : nombre réel (0 à 5).
* `categories` : une ou plusieurs catégories séparées par `;` (elles sont stockées en minuscules dans le code).

### 2. `emprunts.txt` (sortie)

Une ligne par emprunt :

```text
2025-12-08 14:35:12|L01,L05,L15
2025-12-09 10:02:45|L02
...
```

* Avant le `|` : date et heure de l’emprunt.
* Après le `|` : liste des codes des livres, séparés par des virgules.