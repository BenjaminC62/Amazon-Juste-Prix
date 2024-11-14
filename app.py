import sqlite3
from os.path import exists

from flask import Flask, render_template
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

@app.route('/', methods=['GET', 'POST'])
def justePrixAmazon():
    global image,prix, nom
    result = ""

    form = justePrix()

    if form.validate_on_submit():
        if form.prix_article.data == prix:
            result = "Bravo, vous avez trouvé le juste prix !"
        elif form.prix_article.data > prix:
            result = "Le prix est trop grand"
        else:
            result = "Le prix est trop petit"
    return render_template('MainGame.html',image=image, form=form, prix=prix, nom=nom, result=result)

def choisirArticle():
    global image, prix, nom

    cursor = con.cursor()
    cursor.execute("SELECT COUNT(*) FROM ARTICLE")
    nb_article = cursor.fetchone()[0]
    con.commit()
    item_random = random.randint(1, nb_article)
    cursor.execute("SELECT * FROM ARTICLE WHERE id = %d" % item_random)
    article = cursor.fetchone()
    con.commit()
    con.close()
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
    r = requests.get(" http://ws.chez-wam.info/" + article)
    try:
        price = r.json()["price"][:-1] # récupère le prix de l'article
        price = price.replace(",", ".").replace(" ", "") # remplace la virgule par un point et un espace par rien
        result = int(float(price)) # converti la valeur du prix str -> float
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
        con.commit()
    except sqlite3.OperationalError:
        print("La table existe déjà")

creation_bd()

def insertion_bd():
    global image, prix, nom
    liste_article = ["B08W5CLLPL"]

    cursor = con.cursor()
    cursor.execute('''DELETE FROM ARTICLE''') # Question de verif
    con.commit()
    for i in range(len(liste_article)):
        try:
            nom_article = getNom(liste_article[i])
            prix_article = get_prix_article(liste_article[i])
            cursor.execute('''INSERT INTO ARTICLE(nom_article, prix_article,ref_article) VALUES(?,?,?)''', (nom_article, prix_article, liste_article[i]))
        except Exception as e:
            print(f"Erreur lors de la récupération de l'article {liste_article[i]}: {e}")
            # Insertion manuelle si l'article n'est pas trouvé
            nom = input(f"Entrez le nom de l'article pour {liste_article[i]}: ")
            prix = int(float(input(f"Entrez le prix de l'article pour {liste_article[i]}: ")))
            cursor.execute('''INSERT INTO ARTICLE(nom_article, prix_article,ref_article) VALUES(?,?,?)''', (nom, prix, liste_article[i]))
    con.commit()

    #INSERT TEST


insertion_bd()


if __name__ == '__main__':

    app.run()
