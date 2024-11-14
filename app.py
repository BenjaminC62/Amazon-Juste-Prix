import sqlite3
from crypt import methods
from os.path import exists

from flask import Flask, render_template, session, redirect, url_for, request
import requests
from flask_wtf import FlaskForm
from wtforms.fields.numeric import FloatField, IntegerField
from wtforms.validators import DataRequired

import random

con = sqlite3.connect('justePrix.db', check_same_thread=False)

app = Flask(__name__)
app.secret_key = 'secret'

image = ""
prix = 0
nom = ""

class justePrix(FlaskForm) :
    prix_article = IntegerField("Prix de l'article" , validators=[DataRequired()])


@app.route('/home' , methods=['GET'])
def home():
    return render_template('home.html')
@app.route('/', methods=['GET', 'POST'])
def justePrixAmazon():
    if 'username' in session:
        global image, prix, nom
        result = ""

        form = justePrix()

        if form.validate_on_submit():
            if form.prixArticle.data == prix:
                result = "Bravo, vous avez trouvé le juste prix !"
                session['score'] += 1
            elif form.prixArticle.data > prix:
                result = "Le prix est trop grand"
            else:
                result = "Le prix est trop petit"
        return render_template('MainGame.html', image=image, form=form, prix=prix, nom=nom, result=result)
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

def choisirArticle():
    global image, prix, nom

    cursor = con.cursor()
    cursor.execute("SELECT COUNT(*) FROM ARTICLE")
    nb_article = cursor.fetchone()[0]
    con.commit()
    item_random = random.randint(1, nb_article)
    print(item_random)
    cursor.execute("SELECT * FROM ARTICLE WHERE id = ?" , (item_random,))
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
        price = r.json()["price"][:-1] # récupère le prix de l'article
        price = price.replace(",", ".").replace(" ", "") # remplace la virgule par un point et un espace par rien
        result = int(float(price)) # converti la valeur du prix str -> float -> int
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
    try:
        cursor = con.cursor()
        cursor.execute('''CREATE TABLE ARTICLE(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, nom_article TEXT NOT NULL, prix_article FLOAT NOT NULL, ref_article TEXT NOT NULL)''')
        cursor.execute('''CREATE TABLE USERS (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, nom TEXT NOT NULL, prenom TEXT NOT NULL, password TEXT NOT NULL, score INTEGER NOT NULL)''')
        con.commit()
    except sqlite3.OperationalError:
        print("La table existe déjà")

creation_bd()

def insertion_bd():
    global image, prix, nom
    liste_article = ["B07YQFZ6CJ","B0BWS9WQDY"]

    cursor = con.cursor()
    cursor.execute('''DELETE FROM ARTICLE''') # Question de verif
    cursor.execute('''DELETE FROM sqlite_sequence WHERE name='ARTICLE';''')
    con.commit()
    for i in range(len(liste_article)):
        nom_article = getNom(liste_article[i])
        print(nom_article)
        prix_article = get_prix_article(liste_article[i])
        cursor.execute('''INSERT INTO ARTICLE(nom_article, prix_article,ref_article) VALUES(?,?,?)''', (nom_article, prix_article, liste_article[i]))
    con.commit()

insertion_bd()


if __name__ == '__main__':
    choisirArticle()
    app.run()
