import random
import sqlite3
import threading
import os

import pygame
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)

import requests
from flask import Flask, render_template, request, session, redirect
from flask_wtf import FlaskForm
from wtforms.fields.choices import RadioField , SelectField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired

con = sqlite3.connect('justePrix.db', check_same_thread=False)

app = Flask(__name__)
app.secret_key = 'secret'

image = ""
prix = 0
nom = ""
difficulty = ""
theme = ""


class justePrix(FlaskForm):
    prix_article = IntegerField("Prix de l'article", validators=[DataRequired()])


class juste_prix_accueil(FlaskForm):
    difficulty = RadioField("Difficulté", choices=[('easy', 'Facile'), ('medium', 'Moyen'), ('hard', 'Difficile')])
    theme = SelectField("Thème", choices=[('default', 'Tous les thèmes'), ('livre', 'Livre'), ('jeu_video', 'Jeu vidéo'),
                                            ('pc', 'PC'), ('carte_graphique', 'Carte graphique')])



@app.route('/', methods=['GET', 'POST'])
def home():
    pygame.mixer.stop()

    form = juste_prix_accueil()
    global difficulty , theme

    sound_path = os.path.join("sons", "menu.wav")
    if os.path.exists(sound_path):
        sound_id = pygame.mixer.Sound("sons/menu.wav")
        sound_id.set_volume(0.01)
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
        choisirArticle()

        if form.difficulty.data == "easy":
            print("c bon ici")
            difficulty = "easy"
            return redirect("/justePrixAmazon")  # Easy ici -> a changer le MainGame

        if form.difficulty.data == "medium":
            difficulty = "medium"
            return redirect("/justePrixAmazon")  # Medium ici -> a faire

        if form.difficulty.data == "hard":
            difficulty = "hard"
            return redirect("/justePrixAmazon")  # Hard ici -> a faire

    return render_template('PageAccueil.html', form=form, user=user)


@app.route('/justePrixAmazon', methods=['GET', 'POST'])
def justePrixAmazon():

    pygame.mixer.stop()

    global image, prix, nom, difficulty , theme
    result = ""
    user = False

    print("(((((((((((((((((((((((((((((((((((((((((((((((((((((((")

    form = justePrix()
    print(session)

    if form.validate_on_submit():
        print(form.errors)
        print("passe dansle submit")
        if form.prix_article.data == prix:
            print("IL passe dans le result == prix")
            sound_path = os.path.join("sons", "siu.wav")
            result = "Bravo, vous avez trouvé le juste prix !"
            if os.path.exists(sound_path):
                sound_id = pygame.mixer.Sound("sons/siu.wav")
                sound_id.set_volume(0.01)
                sound_id.play()
            else:
                print(f"Sound file not found: {sound_path}")
            if 'username' in session:
                user = True
                session['score'] += 1
                game_result(session['username'], True)
                return render_template('MainEndGame.html', form=form, image=image, prix=prix, nom=nom, result=result,
                                       user=user)
            else:
                return render_template('MainEndGame.html', form=form, image=image, prix=prix, nom=nom, result=result,
                                       user=user)

        elif form.prix_article.data > prix:
            print("IL passe dans le result > prix")
            result = "Le prix est trop grand"
        else:
            print("IL passe dans le result jsp prix")
            result = "Le prix est trop petit"

    print(form.errors)

    if (difficulty == "easy"):
        return render_template('MainEasyGame.html', image=image, form=form, prix=prix, nom=nom, result=result)
    elif (difficulty == "medium"):
        return render_template('MainMediumGame.html', image=image, form=form, prix=prix, nom=nom, result=result)
    else:
        return render_template('MainHardGame.html', image=image, form=form, prix=prix, nom=nom, result=result)


@app.route('/login', methods=['GET', 'POST'])
def login():
    pygame.mixer.stop()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('justePrix.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM USERS WHERE nom = ?', (username,))
        user = cursor.fetchone()
        print(user)
        conn.close()

        if user and user[4] == password:
            session['username'] = username
            session['score'] = user[5]  # Assuming the score is stored in the 5th column
            return redirect('/')
    return render_template('login.html')

def update_score(username, new_score):
    conn = sqlite3.connect('justePrix.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE USERS SET score = ? WHERE nom = ?', (new_score, username))
    conn.commit()
    conn.close()


def game_result(username, gagner):
    if gagner:
        conn = sqlite3.connect('justePrix.db')
        cursor = conn.cursor()
        cursor.execute('SELECT score FROM USERS WHERE nom = ?', (username,))
        current_score = cursor.fetchone()[0]
        conn.close()

        new_score = current_score + 1
        update_score(username, new_score)


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
    pygame.mixer.stop()
    sound_id = pygame.mixer.Sound("sons/classement.wav")
    sound_id.set_volume(0.01)
    sound_id.play(loops=-1)

    cursor = con.cursor()
    cursor.execute("SELECT nom, score FROM USERS ORDER BY score DESC")
    users = cursor.fetchall()
    print(users)
    print(users[0][0])
    con.commit()
    return render_template('Classement.html', users=users)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    pygame.mixer.stop()
    session.pop('username', None)
    session.pop('score', None)
    return redirect('/')


def choisirArticle():
    global image, prix, nom, theme

    cursor = con.cursor()
    print(f"Selected theme: {theme}")  # Debugging statement

    if theme == 'default':
        cursor.execute("SELECT COUNT(*) FROM ARTICLE")
    else:
        cursor.execute("SELECT COUNT(*) FROM ARTICLE WHERE theme = ?", (theme,))
    nb_article = cursor.fetchone()[0]
    con.commit()

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
    con.commit()

    print(f"Selected article: {article}")  # Debugging statement

    if article:
        nom = article[1]
        prix = article[2]
        ref = article[3]
        image = recupereImageArticle(ref)
    else:
        raise Exception("Failed to fetch the article from the database.")


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
        image = None
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
    cursor = con.cursor()
    themes = ['default', 'livre', 'jeu_video', 'pc', 'carte_graphique']
    for theme in themes:
        if theme == 'default':
            cursor.execute("SELECT COUNT(*) FROM ARTICLE")
        else:
            cursor.execute("SELECT COUNT(*) FROM ARTICLE WHERE theme = ?", (theme,))
        nb_article = cursor.fetchone()[0]
        print(f"Theme: {theme}, Number of articles: {nb_article}")
    con.commit()

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
    cursor = con.cursor()
    try:
        cursor.execute(
            '''CREATE TABLE ARTICLE(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, nom_article TEXT NOT NULL, prix_article FLOAT NOT NULL, ref_article TEXT NOT NULL , theme TEXT NOT NULL)''')
        con.commit()
    except sqlite3.OperationalError:
        print("La table ARTICLE existe déjà")

    try:
        cursor.execute(
            '''CREATE TABLE USERS (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,pseudo TEXT NOT NULL, nom TEXT NOT NULL, prenom TEXT NOT NULL, password TEXT NOT NULL, score INTEGER NOT NULL)''')
        con.commit()
    except sqlite3.OperationalError:
        print("La table USERS existe déjà")


creation_bd()


def fetch_and_insert_article(cursor, article, theme):
    nom_article = getNom(article)
    prix_article = get_prix_article(article)
    cursor.execute('''INSERT INTO ARTICLE(nom_article, prix_article, ref_article, theme) VALUES(?,?,?,?)''',
                   (nom_article, prix_article, article, theme))


def insertion_bd():
    global image, prix, nom

    # Listes d'articles par thème
    articles = {
        'default': ["B07YQFZ6CJ", "B0BWS9WQDY"],
        'livre': ["B09V121HM9", "B08R111DV7", "B0CRS894KW", "B08KFWJJW2", "B09WPK89X5"],
        'jeu_video': ["B0D7HSRMHT", "B0DKFDRCGX", "B0821XHJB6", "B0D6M2FG43", "B07BB4R214"],
        'pc': ["B0D9YR8DGH", "B0BB37LMJZ", "B0BQRXHMP8", "B0D8L79YR8", "B0DJTJT5VX"],
        'carte_graphique': ["B0BRYY1JX8", "B0B34M1YLW", "B09Y57F1HL", "B0CGRMJF6C", "B0C8ZSM1W2"]
    }

    cursor = con.cursor()
    cursor.execute('''DELETE FROM ARTICLE''')
    cursor.execute('''DELETE FROM sqlite_sequence WHERE name='ARTICLE';''')
    con.commit()

    for theme, article_list in articles.items():
        for article in article_list:
            fetch_and_insert_article(cursor, article, theme)

    con.commit()
    cursor.execute('''INSERT INTO USERS(nom, prenom, password, score) VALUES(?,?,?,?)''',
                   ("test", "admin", "admin", 0))
    con.commit()

if __name__ == '__main__':
    verify_articles()
    app.run(debug=True)
