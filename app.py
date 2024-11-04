import sqlite3

from flask import Flask

from flask import Flask, render_template
import requests
from flask_wtf import FlaskForm
from wtforms.fields.numeric import FloatField
from wtforms.validators import DataRequired

con = sqlite3.connect('justePrix.db', check_same_thread=False)
app = Flask(__name__)
app.secret_key = 'secret'

image = ""
prix = 0
nom = ""

class JustePrix (FlaskForm):
    prixArticle = FloatField('Prix de l\'article', validators=[DataRequired()])

@app.route('/', methods=['GET', 'POST'])
def justePrixAmazon():  # put application's code here
    global image,prix, nom
    result = ""

    form = JustePrix()

    if form.validate_on_submit():
        if form.prixArticle.data == prix:
            result = "Bravo, vous avez trouvé le juste prix !"
        elif form.prixArticle.data > prix:
            result = "Le prix est trop grand"
        else:
            result = "Le prix est trop petit"
    return render_template('MainGame.html',image=image, form=form, prix=prix, nom=nom, result=result)


def creation_bd():
    try:
        conn = sqlite3.connect('justePrix.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE ARTICLE(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, nom_article TEXT NOT NULL, prix_article FLOAT NOT NULL, ref_article TEXT NOT NULL)''')
        conn.commit()
        conn.close()
    except sqlite3.OperationalError:
        print("La table existe déjà")

creation_bd()

def recupereImageArticle(article):  # put application's code here
    r = requests.get(" http://ws.chez-wam.info/" + article)
    image = r.json()["images"][0]
    return f"<img width='250px' height='250px' src='{image}'/>"

if __name__ == '__main__':
    app.run()
