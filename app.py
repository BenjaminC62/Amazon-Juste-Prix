import random
import sqlite3

import requests
from flask import Flask, render_template, request, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms.fields.choices import RadioField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired

con = sqlite3.connect('justePrix.db', check_same_thread=False)

app = Flask(__name__)
app.secret_key = 'secret'

image = ""
prix = 0
nom = ""
difficulty = ""


class justePrix(FlaskForm):
    prix_article = IntegerField("Prix de l'article", validators=[DataRequired()])


class juste_prix_accueil(FlaskForm):
    difficulty = RadioField("Difficulté", choices=[('easy', 'Facile'), ('medium', 'Moyen'), ('hard', 'Difficile')])
    theme = RadioField("Theme",
                       choices=[('default', 'Default'), ('jeu_video', 'Jeu Vidéo'), ('livre', 'Livre'), ('pc', 'PC'),
                                ('carte_graphique', 'Carte Graphique')])


@app.route('/', methods=['GET', 'POST'])
def home():
    form = juste_prix_accueil()
    global difficulty

    if form.validate_on_submit():

        print("dificult avec form.diff", form.difficulty.data)

        if form.difficulty.data == "easy":
            difficulty = "easy"
            return redirect("/justePrixAmazon")
        if form.difficulty.data == "medium":
            difficulty = "medium"
            return redirect("/justePrixAmazon")
        if form.difficulty.data == "hard":
            difficulty = "hard"
            return redirect("/justePrixAmazon")

    return render_template('PageAccueil.html', form=form)


@app.route('/justePrixAmazon', methods=['GET', 'POST'])
def justePrixAmazon():
    global image, prix, nom, difficulty
    result = ""

    form = justePrix()

    if form.validate_on_submit():
        if form.prix_article.data == prix:
            result = "Bravo, vous avez trouvé le juste prix !"
            if 'username' in session:
                session['score'] += 1
                game_result(session['username'], True)
        elif form.prix_article.data > prix:
            result = "Le prix est trop grand"
        else:
            result = "Le prix est trop petit"

        print(form.errors)

        print("la difficulté est : ", difficulty)

        if difficulty == "easy":
            return render_template('MainEasyGame.html', image=image, form=form, prix=prix, nom=nom, result=result)
        elif difficulty == "medium":
            return render_template('MainMediumGame.html', image=image, form=form, prix=prix, nom=nom, result=result)
        else:
            return render_template('MainHardGame.html', image=image, form=form, prix=prix, nom=nom, result=result)

    else:
        return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('justePrix.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM USERS WHERE nom = ?', (username,))
        user = cursor.fetchone()
        conn.close()

        if user and user[3] == password:
            session['username'] = username
            session['score'] = user[4]  # Assuming the score is stored in the 5th column
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
    if request.method == 'POST':
        prenom = request.form['prenom']
        nom = request.form['nom']
        password = request.form['password']

        conn = sqlite3.connect('justePrix.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO USERS(prenom, nom, password, score) VALUES(?, ?, ?, 0)', (prenom, nom, password))
        conn.commit()
        conn.close()
        return redirect('/login')
    return render_template('register.html')


def choisirArticle():
    global image, prix, nom

    cursor = con.cursor()
    cursor.execute("SELECT COUNT(*) FROM ARTICLE")
    nb_article = cursor.fetchone()[0]
    con.commit()
    item_random = random.randint(1, nb_article)
    print(item_random)
    cursor.execute("SELECT * FROM ARTICLE WHERE id = ?", (item_random,))
    article = cursor.fetchone()
    con.commit()
    print(article)

    nom = article[1]
    prix = article[2]
    ref = article[3]
    image = recupereImageArticle(ref)


def recupereImageArticle(article):
    r = requests.get("http://ws.chez-wam.info/" + article)
    image = r.json()["images"][0]
    return image


def get_prix_article(article):
    r = requests.get("http://ws.chez-wam.info/" + article)
    try:
        price = r.json()["price"][:-1]  # récupère le prix de l'article
        price = price.replace(",", ".").replace(" ", "")  # remplace la virgule par un point et un espace par rien
        result = int(float(price))  # converti la valeur du prix str -> float -> int
    except:
        raise Exception("Prix de l'article n'est pas disponible !")
    return result


def getNom(article):
    r = requests.get(" http://ws.chez-wam.info/" + article)
    try:
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
            '''CREATE TABLE USERS (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, nom TEXT NOT NULL, prenom TEXT NOT NULL, password TEXT NOT NULL, score INTEGER NOT NULL)''')
        con.commit()
    except sqlite3.OperationalError:
        print("La table USERS existe déjà")


creation_bd()


def insertion_bd():
    global image, prix, nom

    # Listes d'articles par thème
    liste_article = ["B07YQFZ6CJ", "B0BWS9WQDY"]
    liste_article_livre = ["B09V121HM9", "B08R111DV7", "B0CRS894KW", "B08KFWJJW2", "B09WPK89X5"]
    liste_article_jeu_video = ["B0D7HSRMHT", "B0DKFDRCGX", "B0821XHJB6", "B0D6M2FG43", "B07BB4R214"]
    liste_article_pc = ["B0D9YR8DGH", "B0BB37LMJZ", "B0BQRXHMP8", "B0D8L79YR8", "B0DJTJT5VX"]
    liste_article_carte_graphique = ["B0BRYY1JX8", "B0B34M1YLW", "B09Y57F1HL", "B0CGRMJF6C", "B0C8ZSM1W2"]

    cursor = con.cursor()
    cursor.execute('''DELETE FROM ARTICLE''')  # Question de verif
    cursor.execute('''DELETE FROM sqlite_sequence WHERE name='ARTICLE';''')
    con.commit()

    # Insertion des articles de chaque thème
    for article in liste_article:
        nom_article = getNom(article)
        prix_article = get_prix_article(article)
        cursor.execute('''INSERT INTO ARTICLE(nom_article, prix_article, ref_article, theme) VALUES(?,?,?,?)''',
                       (nom_article, prix_article, article, 'default'))

    for article in liste_article_livre:
        nom_article = getNom(article)
        prix_article = get_prix_article(article)
        cursor.execute('''INSERT INTO ARTICLE(nom_article, prix_article, ref_article, theme) VALUES(?,?,?,?)''',
                       (nom_article, prix_article, article, 'livre'))

    for article in liste_article_jeu_video:
        nom_article = getNom(article)
        prix_article = get_prix_article(article)
        cursor.execute('''INSERT INTO ARTICLE(nom_article, prix_article, ref_article, theme) VALUES(?,?,?,?)''',
                       (nom_article, prix_article, article, 'jeu_video'))

    for article in liste_article_pc:
        nom_article = getNom(article)
        prix_article = get_prix_article(article)
        cursor.execute('''INSERT INTO ARTICLE(nom_article, prix_article, ref_article, theme) VALUES(?,?,?,?)''',
                       (nom_article, prix_article, article, 'pc'))

    for article in liste_article_carte_graphique:
        nom_article = getNom(article)
        prix_article = get_prix_article(article)
        cursor.execute('''INSERT INTO ARTICLE(nom_article, prix_article, ref_article, theme) VALUES(?,?,?,?)''',
                       (nom_article, prix_article, article, 'carte_graphique'))

    con.commit()
    cursor.execute('''INSERT INTO USERS(nom, prenom, password, score) VALUES(?,?,?,?)''',
                   ("test", "admin", "admin", 0))
    con.commit()


insertion_bd()

if __name__ == '__main__':
    choisirArticle()
    app.run()
