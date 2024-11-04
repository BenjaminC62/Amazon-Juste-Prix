import sqlite3
from wsgiref.validate import validator

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
        if form.prix_article.data == prix:
            result = "Bravo, vous avez trouvé le juste prix !"
        elif form.prix_article.data > prix:
            result = "Le prix est trop grand"
        else:
            result = "Le prix est trop petit"
    return render_template('game.html',image=image, form=form, prix=prix, nom=nom, result=result)


if __name__ == '__main__':
    app.run()
