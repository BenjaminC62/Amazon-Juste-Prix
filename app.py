import os
import random
import sqlite3

import pygame

pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)

import requests
from flask import Flask, render_template, request, session, redirect
from flask_wtf import FlaskForm
from wtforms.fields.choices import RadioField, SelectField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = 'secret'

image = ""
prix = 0
nom = ""
difficulty = ""
theme = ""
liste_article = []
mode = ""
passage = 0


class justePrix(FlaskForm):
    prix_article = IntegerField("Prix de l'article", validators=[DataRequired()])


class juste_prix_accueil(FlaskForm):
    difficulty = RadioField("Difficulté", choices=[('easy', 'Facile'), ('medium', 'Moyen'), ('hard', 'Difficile')])
    theme = SelectField("Thème",
                        choices=[('default', 'Tous les thèmes'), ('livre', 'Livre'), ('jeu_video', 'Jeu vidéo'),
                                 ('pc', 'PC'), ('carte_graphique', 'Carte graphique')])
    mode = RadioField("Mode", choices=[('un_article', 'Un seul article'), ('plusieurs_articles', 'Plusieurs articles')])


@app.route('/', methods=['GET', 'POST'])
def home():
    pygame.mixer.stop()
    lang = session.get('lang', 'en')
    form = juste_prix_accueil()
    form.difficulty.choices = [
        ('easy', 'Facile' if lang == 'fr' else 'Easy'),
        ('medium', 'Moyen' if lang == 'fr' else 'Medium'),
        ('hard', 'Difficile' if lang == 'fr' else 'Hard')
    ]
    form.theme.choices = [
        ('default', 'Tous les thèmes' if lang == 'fr' else 'All themes'),
        ('livre', 'Livre' if lang == 'fr' else 'Book'),
        ('jeu_video', 'Jeu vidéo' if lang == 'fr' else 'Video game'),
        ('pc', 'PC'),
        ('carte_graphique', 'Carte graphique' if lang == 'fr' else 'Graphics card')
    ]
    form.mode.choices = [
        ('un_article', 'Un seul article' if lang == 'fr' else 'Single item'),
        ('plusieurs_articles', 'Plusieurs articles' if lang == 'fr' else 'Multiple items')
    ]

    global difficulty, theme, mode

    sound_path = os.path.join("sons", "menu.wav")
    if os.path.exists(sound_path):
        sound_id = pygame.mixer.Sound("sons/menu.wav")
        sound_id.set_volume(0.03)
        sound_id.play(loops=-1)
    else:
        print(f"Sound file not found: {sound_path}")
    user = session.get('username')

    print("il passe dans la difficulté")
    print(form.errors)

    if form.validate_on_submit():
        print("passe dans la submit")
        difficulty = form.difficulty.data
        theme = form.theme.data
        mode = form.mode.data
        if mode == 'un_article':
            choisirArticle()
        else:
            choisirPlusieursArticle()
        return redirect('/justePrixAmazon')

    return render_template('PageAccueil.html', form=form, user=user)


@app.route('/justePrixAmazon', methods=['GET', 'POST'])
def justePrixAmazon():
    pygame.mixer.stop()

    global image, prix, nom, difficulty, theme, liste_article, mode, passage
    result = ""
    user = False

    if mode == "plusieurs_articles" and passage == 0:
        passage += 1
        for i in range(len(liste_article)):
            prix += liste_article[i][2]
        print(f"Total price: {prix}")

    lang = session.get('lang', 'fr')
    form = justePrix()
    form.prix_article.label.text = "Price of the item" if lang == 'en' else "Prix de l'article"

    if form.validate_on_submit():
        if form.prix_article.data == prix:
            print("IL passe dans le result == prix")
            sound_path = os.path.join("sons", "siu.wav")
            if os.path.exists(sound_path):
                sound_id = pygame.mixer.Sound("sons/siu.wav")
                sound_id.set_volume(0.03)
                sound_id.play()
            else:
                print(f"Sound file not found: {sound_path}")
            if 'username' in session:
                user = True
                session['score'] += 1
                game_result(session['username'], True)
                # Depend de si on dit qu'il peux changer de pseudo 1 fois ou plusieur fois
                # cursor = conn.cursor()
                # cursor.execute("SELECT pseudo FROM USERS WHERE nom = ?", (session['username'],))
                # pseudo = cursor.fetchone()[0]
                # print(pseudo)
                return render_template('MainEndGame.html', image=image, prix=prix, nom=nom, result=result,
                                       user=user)
            else:
                return render_template('MainEndGame.html', image=image, prix=prix, nom=nom, result=result,
                                       user=user)

        elif form.prix_article.data > prix:
            result = "Le prix est trop grand" if lang == 'fr' else "The price is too high"
        else:
            result = "Le prix est trop petit" if lang == 'fr' else "The price is too low"

    if difficulty == "easy":
        if mode == "un_article":
            return render_template('MainEasyGame.html', image=image, form=form, prix=prix, nom=nom, result=result,
                                   mode=mode)
        else:
            return render_template('MainEasyGame.html', liste_article=liste_article, form=form, result=result,
                                   mode=mode)
    elif difficulty == "medium":
        if mode == "un_article":
            return render_template('MainMediumGame.html', image=image, form=form, prix=prix, nom=nom, result=result,
                                   mode=mode)
        else:
            return render_template('MainMediumGame.html', liste_article=liste_article, form=form, result=result,
                                   mode=mode)
    else:
        if mode == "un_article":
            return render_template('MainHardGame.html', image=image, form=form, prix=prix, nom=nom, result=result,
                                   mode=mode)
        else:
            return render_template('MainHardGame.html', liste_article=liste_article, form=form, result=result,
                                   mode=mode)


@app.route('/rules', methods=['GET', 'POST'])
def rules():
    pygame.mixer.stop()
    user = session.get('username')
    return render_template('regle.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    pygame.mixer.stop()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('justePrix.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM USERS WHERE nom = ?', (username,))
        user = cursor.fetchall()
        print(user)
        conn.close()

        if user:
            for i in range(len(user)):
                print(i)
                if user[i][4] == password:
                    session['username'] = username
                    session['score'] = user[i][5]  # Assuming the score is stored in the 5th column
                    return redirect('/')
    return render_template('login.html')


@app.route('/AjoutArticle', methods=['POST', 'GET'])
def AjoutArticle():
    pygame.mixer.stop()
    add = False
    if request.method == 'POST':
        nom_article = request.form['nom_article']
        prix_article = request.form['prix_article']
        ref_article = request.form['ref_article']
        theme = request.form['theme_article']

        conn = sqlite3.connect('justePrix.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO ARTICLE(nom_article, prix_article, ref_article, theme) VALUES(?,?,?,?)''',
                       (nom_article, prix_article, ref_article, theme))
        conn.commit()
        conn.close()
        add = True
        return render_template('AjoutArticle.html', add=add)

    return render_template('AjoutArticle.html', add=add)


def update_score(username, new_score, conn):
    cursor = conn.cursor()
    cursor.execute('UPDATE USERS SET score = ? WHERE nom = ?', (new_score, username))
    conn.commit()
    conn.close()


@app.route('/change_language/<lang>')
def change_language(lang):
    session['lang'] = lang
    return redirect(request.referrer)


def game_result(username, gagner):
    if gagner:
        conn = sqlite3.connect('justePrix.db')
        cursor = conn.cursor()
        cursor.execute('SELECT score FROM USERS WHERE nom = ?', (username,))
        current_score = cursor.fetchone()[0]

        new_score = current_score + 1
        update_score(username, new_score, conn)


@app.route('/register', methods=['GET', 'POST'])
def register():
    pygame.mixer.stop()
    if request.method == 'POST':
        prenom = request.form['prenom']
        nom = request.form['nom']
        password = request.form['password']

        conn = sqlite3.connect('justePrix.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO USERS(pseudo, prenom, nom, password, score) VALUES("",?, ?, ?, 0)',
                       (prenom, nom, password))
        conn.commit()
        conn.close()
        return redirect('/login')
    return render_template('register.html')


@app.route('/leaderboard', methods=['GET', 'POST'])
def leaderboard():
    conn = sqlite3.connect('justePrix.db')
    cursor = conn.cursor()
    pygame.mixer.stop()
    sound_id = pygame.mixer.Sound("sons/classement.wav")
    sound_id.set_volume(0.03)
    sound_id.play(loops=-1)

    cursor.execute("SELECT pseudo, score FROM USERS ORDER BY score DESC")
    users = cursor.fetchall()
    print(users)
    print(users[0][0])
    conn.commit()
    conn.close()
    return render_template('Classement.html', users=users)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    pygame.mixer.stop()
    session.pop('username', None)
    session.pop('score', None)
    return redirect('/')


def choisirArticle():
    global image, prix, nom, theme
    conn = sqlite3.connect('justePrix.db')
    cursor = conn.cursor()
    print(f"Selected theme: {theme}")  # Debugging statement

    if theme == 'default':
        cursor.execute("SELECT COUNT(*) FROM ARTICLE")
    else:
        cursor.execute("SELECT COUNT(*) FROM ARTICLE WHERE theme = ?", (theme,))
    nb_article = cursor.fetchone()[0]
    conn.commit()

    print(f"Number of articles found: {nb_article}")  # Debugging statement

    if nb_article == 0:
        raise Exception("No articles found for the selected theme.")

    item_random = random.randint(1, nb_article)
    print(f"Random item number: {item_random}")  # Debugging statement

    if theme == 'default':
        cursor.execute("SELECT * FROM ARTICLE WHERE id = ?", (item_random,))
    else:
        cursor.execute("SELECT * FROM ARTICLE WHERE theme = ? LIMIT 1 OFFSET ?", (theme, item_random - 1))
    article = cursor.fetchone()
    conn.commit()
    conn.close()

    print(f"Selected article: {article}")  # Debugging statement

    if article:
        nom = article[1]
        prix = article[2]
        ref = article[3]
        image = recupereImageArticle(ref)
    else:
        raise Exception("Failed to fetch the article from the database.")


def choisirPlusieursArticle():
    global liste_article
    global prix, nom, theme
    conn = sqlite3.connect('justePrix.db')
    cursor = conn.cursor()

    if theme == 'default':
        cursor.execute("SELECT COUNT(*) FROM ARTICLE")
    else:
        cursor.execute("SELECT COUNT(*) FROM ARTICLE WHERE theme = ?", (theme,))
    nb_article = cursor.fetchone()[0]
    conn.commit()

    if nb_article == 0:
        raise Exception("No articles found for the selected theme.")

    for _ in range(4):
        item_random = random.randint(1, nb_article)
        if theme == 'default':
            cursor.execute("SELECT * FROM ARTICLE WHERE id = ?", (item_random,))
        else:
            cursor.execute("SELECT * FROM ARTICLE WHERE theme = ? LIMIT 1 OFFSET ?", (theme, item_random - 1))
        article = cursor.fetchone()
        liste_article.append(article)
    conn.commit()
    print(liste_article)
    conn.close()


@app.route('/save_pseudo', methods=['POST'])
def save_pseudo():
    conn = sqlite3.connect('justePrix.db')
    if request.method == 'POST':
        data = request.get_json()
        pseudo = data.get('pseudo')

        print("Il passe dans le save pseudo")

        if 'username' in session:
            username = session['username']
            cursor = conn.cursor()
            cursor.execute('UPDATE USERS SET pseudo = ? WHERE nom = ?', (pseudo, username))
            conn.commit()
            conn.close()
            return "Pseudo saved successfully"
        return "Error saving pseudo"


def recupereImageArticle(article):
    r = requests.get("http://ws.chez-wam.info/" + article)
    try:
        r.raise_for_status()
        response_json = r.json()
        if "images" in response_json and response_json["images"]:
            image = response_json["images"][0]
        else:
            raise Exception("No images found for the article.")
    except Exception as e:
        print(f"Error retrieving image: {e}")
        image = ""
    return image


def get_prix_article(article):
    r = requests.get("http://ws.chez-wam.info/" + article)
    result = 0
    try:
        r.raise_for_status()  # Vérifie si le statut HTTP est une erreur (404, 500, etc.)
        response_json = r.json()  # Tente de convertir la réponse en JSON
        if "price" not in response_json:
            raise Exception("Clé 'price' absente dans la réponse JSON.")
        price = response_json["price"][:-1]
        price = price.replace(",", ".").replace("\u202f", "").replace(" ", "")
        result = int(float(price))  # Conversion str -> float -> int
    except Exception:
        print("why")
    return result


def verify_articles():
    conn = sqlite3.connect('justePrix.db')
    cursor = conn.cursor()
    themes = ['default', 'livre', 'jeu_video', 'pc', 'carte_graphique']
    for theme in themes:
        if theme == 'default':
            cursor.execute("SELECT COUNT(*) FROM ARTICLE")
        else:
            cursor.execute("SELECT COUNT(*) FROM ARTICLE WHERE theme = ?", (theme,))
        nb_article = cursor.fetchone()[0]
        print(f"Theme: {theme}, Number of articles: {nb_article}")
    conn.commit()


def getNom(article):
    r = requests.get(" http://ws.chez-wam.info/" + article)
    try:
        r.raise_for_status()
        name = r.json()["title"]
        name = name.split(" ")
        name = " ".join(name[:3])
    except:
        raise Exception("Nom de l'article n'est pas disponible !")
    return name


def creation_bd():
    conn = sqlite3.connect('justePrix.db')
    cursor = conn.cursor()
    try:
        cursor.execute(
            '''CREATE TABLE ARTICLE(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, nom_article TEXT NOT NULL, prix_article FLOAT NOT NULL, ref_article TEXT NOT NULL , theme TEXT NOT NULL, image TEXT NOT NULL)''')
        conn.commit()
    except sqlite3.OperationalError:
        print("La table ARTICLE existe déjà")

    try:
        cursor.execute(
            '''CREATE TABLE USERS (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,pseudo TEXT NOT NULL, nom TEXT NOT NULL, prenom TEXT NOT NULL, password TEXT NOT NULL, score INTEGER NOT NULL)''')
        conn.commit()
        conn.close()
    except sqlite3.OperationalError:
        print("La table USERS existe déjà")


creation_bd()


def fetch_and_insert_article(cursor, article, theme):
    nom_article = getNom(article)
    prix_article = get_prix_article(article)
    image = recupereImageArticle(article)
    cursor.execute('''INSERT INTO ARTICLE(nom_article, prix_article, ref_article, theme, image) VALUES(?,?,?,?,?)''',
                   (nom_article, prix_article, article, theme, image))


def insertion_bd():
    conn = sqlite3.connect('justePrix.db')
    global image, prix, nom

    # Listes d'articles par thème
    articles = {
        'default': ["B07YQFZ6CJ", "B0BWS9WQDY"],
        'livre': ["B09V121HM9", "B08R111DV7", "B0CRS894KW", "B08KFWJJW2", "B09WPK89X5"],
        'jeu_video': ["B0D7HSRMHT", "B0DKFDRCGX", "B0821XHJB6", "B0D6M2FG43", "B07BB4R214"],
        'pc': ["B0D9YR8DGH", "B0BB37LMJZ", "B0BQRXHMP8", "B0D8L79YR8", "B0DJTJT5VX"],
        'carte_graphique': ["B0BRYY1JX8", "B0B34M1YLW", "B09Y57F1HL", "B0CGRMJF6C", "B0C8ZSM1W2"]
    }

    cursor = conn.cursor()

    for theme, article_list in articles.items():
        for article in article_list:
            fetch_and_insert_article(cursor, article, theme)
    conn.commit()


if __name__ == '__main__':
    verify_articles()
    app.run(debug=True)
