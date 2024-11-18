# MSI-LES-MASKS

## Répartition des rôles 
    - Mathias Morel : Scrum Master
    - Benjamin Cornet : Team member
    - Mathéo Dalmasso : Team member
    - Simon Caillieret : Team member

---

## Tuto comment lancer le projet

1. Appuyer sur le bouton vert **Run** en haut à droite et il faut être sur app.py

2. Une fois que le serveur est lancé, cliquer sur le lien dans le terminal http://127.0.0.1:5000

## Guide pour le Jeu du Juste Prix Amazon

### **3. Navigation sur la page d'accueil**

Vous êtes normalement sur la page d'accueil (*Il y a écrit au milieu : "Bienvenue sur le jeu du Juste Prix Amazon !"*). Voici les actions possibles :  

- **Jouer au jeu :**
  - Appuyez sur le bouton **"Jouer"**.
  - Choisissez le **mode de difficulté** que vous souhaitez.
  - Sélectionnez le **thème de l'article** à deviner.
  - Sélectionnez un item ou plusieurs items à deviner.

- **Consulter le classement :**
  - Appuyez sur le bouton **"Classement"** pour voir les meilleurs scores.

- **Lire les règles :**
  - Appuyez sur le bouton **"Règles"** pour consulter les instructions du jeu (disponible uniquement sur la page d'accueil).

- **Se connecter :**
  - Appuyez sur le bouton **"Se connecter"** pour accéder à votre compte (le username c'est le nom de famille).

- **S'inscrire :**
  - Vous devez appuyer sur le bouton **"Connexion"** pour accéder à la page de connexion.
  - Ensuite cliquez sur **"Pas de compte ? Inscrivez-vous !"** pour accéder à la page d'inscription.

- **Ajouter un article :**
  - Appuyez sur le bouton **"Ajouter un article"**(disponible uniquement sur la page d'accueil).
  - Remplissez le **formulaire** qui apparaît.

- **Changer de mode (jour/nuit) :**
  - **Mode nuit :** Appuyez sur l'icône **lune** en haut à droite.
  - **Mode jour :** Appuyez sur l'icône **soleil** en haut à droite.

- **Changer de langue :**
  - **Français :** Appuyez sur le drapeau **"FR"** en haut à gauche.
  - **Anglais :** Appuyez sur le drapeau **"EN"** en haut à gauche.

- **Pour les sons :**
  - **Augmenter le son de votre ordinateur** pour entendre les bruitages (ils sont pas très forts).


## Les différentes features créées

- Ajout d'un item
![Ajout d'un item](./screens/ajout_article.png)
- Ajout d'un item en nightmode
![Ajout d'un item en nightmode](./screens/ajout_article_nightmode.png)
- Mode de difficulté (facile)
![Mode de difficulté](./screens/mode_facile_un_seul_article.png)
- Mode de difficulté en nightmode (facile)
![Mode de difficulté en nightmode](./screens/mode_facile_un_seul_article_nightmode.png)
- Mode de difficulté (moyen)
![Mode de difficulté](./screens/mode_moyen_un_seul_article.png)
- Mode de difficulté en nightmode (moyen)
![Mode de difficulté en nightmode](./screens/mode_moyen_un_seul_article_nightmode.png)
- Mode de difficulté (difficile)
![Mode de difficulté](./screens/mode_difficile_un_seul_article.png)
- Mode de difficulté en nightmode (difficile)
![Mode de difficulté en nightmode](./screens/mode_difficile_un_seul_article_nightmode.png)
- Plusieurs items a trouver (ici c'est le niveau facile)
![Plusieurs items a trouver](./screens/mode_facile_plusieurs_articles.png)
- Plusieurs items a trouver en nightmode
![Plusieurs items a trouver en nightmode](./screens/mode_facile_plusieurs_articles_nightmode.png)
- Choix de pseudo stylé
![Choix de pseudo](./screens/speudo.png)
- Classement
![Classement](./screens/classement.png)
- Classement en nightmode
![Classement en nightmode](./screens/classement_night.png)
- Log in
![Log in](./screens/login.png)
- Log in en nightmode
![Log in en nightmode](./screens/login_night.png)
- Thèmes pour chaque item (ici c'est les livres mais c'est la meme chose pour les autres themes)
![Thèmes](./screens/theme_livre.png)
- Thèmes pour chaque item en nightmode
![Thèmes en nightmode](./screens/theme_livre_nightmode.png)
- Traduction (ici c'est la page d'accueil mais c'est la meme chose pour les autres pages)
![Traduction](./screens/page_accueil.png)
- Page pour les règles
![Page des règles](./screens/regle.png)
- Page pour les règles en nightmode
![Page des règles en nightmode](./screens/regle_night.png)
- Mode nuit/jour (ici c'est le classement mais c'est la meme chose pour les autres pages)
![Mode nuit/jour](./screens/classement_night.png)
- Timer
![Timer](./screens/mode_moyen_un_seul_article.png)
- Timer en nightmode
![Timer en nightmode](./screens/mode_moyen_un_seul_article_nightmode.png)
- Page d'accueil
![Page d'accueil](./screens/page_accueil_fr.png)
- Page d'inscription
![Page d'inscription](./screens/inscription.png)
- Page d'inscription en nightmode
![Page d'inscription en nightmode](./screens/inscription_night.png)
- Page de fin de partie
![Page de fin de partie](./screens/page_fin.png)
- Page de fin de partie en nightmode
![Page de fin de partie en nightmode](./screens/page_fin_nightmode.png)


## Répartition des tâches

# Répartition des tâches

| Nom              | Description de la tâche                                                                 | Fait      |
|------------------|-----------------------------------------------------------------------------------------|-----------|
| Mathias Morel    | Fonction qui choisit aléatoirement un article Amazon                                    | ✔️        |
| Benjamin Cornet  | Fonction qui récupère l'image de l'article                                              | ✔️        |
| Benjamin Cornet  | Rectification des différentes fonctions de la base de données                           | ✔️        |
| Mathéo Dalmasso  | Fonction qui récupère le nom de l'article                                               | ✔️        |
| Simon Caillieret | Fonction qui récupère le prix de l'article                                              | ✔️        |
| Benjamin Cornet  | Ajout d'item : Un formulaire pour ajouter des items dans la BD                          | ✔️        |
| Benjamin Cornet  | Mode de difficultés : Choix de la difficulté                                            | ✔️        |
| Benjamin Cornet  | Un choix de pseudo stylé                                                                | ✔️        |
| Mathéo Dalmasso  | Tableau des scores consultable directement depuis le site                               | ✔️        |
| Mathias Morel    | Log in : Système de compte avec page de connexion et d'inscription                      | ✔️        |
| Mathias Morel    | Des thèmes pour chaque item                                                             | ✔️        |
| Mathias Morel    | Traduction : Rajouter un bouton en/fr pour traduire le site                             | ✔️        |
| Mathéo Dalmasso  | Bruitage : Ajouter des bruitages pour certaines actions                                 | ✔️        |
| Mathéo Dalmasso  | Page pour les règles                                                                    | ✔️        |
| Simon Caillieret | Mode nuit/jour : Pour ne pas agresser la rétine                                         | ✔️        |
| Simon Caillieret | Un timer : Comme dans le vrai jeu                                                       | ✔️        |
| Benjamin Cornet  | Style : Rajouter du style dans le site                                                  | ✔️        |
| Mathéo Dalmasso  | Une page d'accueil : Page racine avec un menu pour présenter le site et accéder aux autres pages | ✔️        |
| Simon Caillieret | Une page d'accueil : Page racine avec un menu pour présenter le site et accéder aux autres pages | ✔️        |
| Benjamin Cornet  | Une page d'accueil : Page racine avec un menu pour présenter le site et accéder aux autres pages | ✔️        |
| Mathias Morel    | Une page d'accueil : Page racine avec un menu pour présenter le site et accéder aux autres pages | ✔️        |

---

## Choix du workflow

Nous avons choisi d'utiliser une "feature branch workflow".

---

## Exemples de commit

#### Pour fermer une issue
    - git commit -m "Fixes #? - Description de l'issue"

#### Pour un commit de correction de bugs / changements dans le programme
    - git commit -m "Description du commit"
    
    
---

## Définition du Product backlog

* Création du projet
* Création d'une fonction qui choisit aléatoirement un article Amazon
* Création d'une fonction qui récupère le prix d'un article placé en paramètre
* Création d'une fonction qui récupère l'image de l'article placé en paramètre
* Création d'une fonction qui récupère le nom de l'article placé en paramètre
* Création de la fonction principale du jeu
* Création d'un fichier de styles 
* Création d'un formulaire pour ajouter des items dans la base de données
* Création d'un choix de difficulté
* Création d'un choix de pseudo stylé
* Création d'un tableau des scores consultable directement depuis le site
* Création d'un système de compte avec page de connexion et d'inscription
* Création de thèmes pour chaque item
* Création d'un bouton en/fr pour traduire le site
* Ajout de bruitages pour certaines actions
* Création d'une page pour les règles
* Création d'un mode nuit/jour
* Création d'un timer
* Création d'une page d'accueil
* Création d'une page de fin de partie
