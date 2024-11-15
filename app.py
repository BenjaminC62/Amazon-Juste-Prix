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


@app.route('/', methods=['GET', 'POST'])
def home():
    form = juste_prix_accueil()
    global difficulty

    if form.validate_on_submit() and form.difficulty.data == "easy":
        difficulty = "easy"
        return render_template('MainGame.html', form=form)  # Easy ici -> a changer le MainGame

    if form.validate_on_submit() and form.difficulty.data == "medium":
        difficulty = "medium"
        return render_template('MainGame.html', form=form)  # Medium ici -> a faire

    if form.validate_on_submit() and form.difficulty.data == "hard":
        difficulty = "hard"
        return render_template('MainGame.html', form=form)  # Hard ici -> a faire

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

    return render_template('MainGame.html', image=image, form=form, prix=prix, nom=nom, result=result)


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
        print(type(result))
    except:
        raise Exception("Prix de l'article n'est pas disponible !")
    return result


def getNom(article):
    r = requests.get(" http://ws.chez-wam.info/" + article)
    try:
        name = r.json()["title"]
    except:
        raise Exception("Nom de l'article n'est pas disponible !")
    return name


def creation_bd():
    cursor = con.cursor()
    try:
        cursor.execute(
            '''CREATE TABLE ARTICLE(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, nom_article TEXT NOT NULL, prix_article FLOAT NOT NULL, ref_article TEXT NOT NULL)''')
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
    liste_article = ["B07YQFZ6CJ", "B0BWS9WQDY"]

    cursor = con.cursor()
    cursor.execute('''DELETE FROM ARTICLE''')  # Question de verif
    cursor.execute('''DELETE FROM sqlite_sequence WHERE name='ARTICLE';''')
    con.commit()
    for i in range(len(liste_article)):
        nom_article = getNom(liste_article[i])
        print(nom_article)
        prix_article = get_prix_article(liste_article[i])
        cursor.execute('''INSERT INTO ARTICLE(nom_article, prix_article,ref_article) VALUES(?,?,?)''',
                       (nom_article, prix_article, liste_article[i]))
    con.commit()
    #cursor.execute('''DELETE FROM USERS''')
    #con.commit()
    cursor.execute('''INSERT INTO USERS(nom, prenom, password, score) VALUES(?,?,?,?)''',
                   ("test", "admin", "admin", 0))
    con.commit()


insertion_bd()

if __name__ == '__main__':
    choisirArticle()
    app.run()
