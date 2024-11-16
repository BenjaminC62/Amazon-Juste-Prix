import random
import sqlite3
import threading

import requests
from flask import Flask, render_template, request, session, redirect
from flask_wtf import FlaskForm
from wtforms.fields.choices import RadioField, SelectField
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
    theme = SelectField("Thème",
                        choices=[('default', 'Tous les thèmes'), ('livre', 'Livre'), ('jeu_video', 'Jeu vidéo'),
                                 ('pc', 'PC'), ('carte_graphique', 'Carte graphique')])


@app.route('/', methods=['GET', 'POST'])
def home():
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

    global difficulty, theme
    user = session.get('username')

    if form.validate_on_submit():
        difficulty = form.difficulty.data
        theme = form.theme.data
        choisirArticle()

        if difficulty == "easy":
            return redirect("/justePrixAmazon")
        elif difficulty == "medium":
            return redirect("/justePrixAmazon")
        elif difficulty == "hard":
            return redirect("/justePrixAmazon")

    return render_template('PageAccueil.html', form=form, user=user)


@app.route('/justePrixAmazon', methods=['GET', 'POST'])
def justePrixAmazon():
    global image, prix, nom, difficulty, theme
    result = ""
    user = False

    lang = session.get('lang', 'fr')
    form = justePrix()
    form.prix_article.label.text = "Price of the item" if lang == 'en' else "Prix de l'article"

    if form.validate_on_submit():
        if form.prix_article.data == prix:
            result = "Bravo, vous avez trouvé le juste prix !" if lang == 'fr' else "Congratulations, you found the right price!"
            if 'username' in session:
                user = True
                session['score'] += 1
                game_result(session['username'], True)
                # Depend de si on dit qu'il peux changer de pseudo 1 fois ou plusieur fois
                # cursor = con.cursor()
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
        return render_template('MainEasyGame.html', image=image, form=form, prix=prix, nom=nom, result=result)
    elif difficulty == "medium":
        return render_template('MainMediumGame.html', image=image, form=form, prix=prix, nom=nom, result=result)
    else:
        return render_template('MainHardGame.html', image=image, form=form, prix=prix, nom=nom, result=result)



@app.route('/login', methods=['GET', 'POST'])
def login():
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
        cursor.execute('INSERT INTO USERS(pseudo, prenom, nom, password, score) VALUES("",?, ?, ?, 0)',
                       (prenom, nom, password))
        conn.commit()
        conn.close()
        return redirect('/login')
    return render_template('register.html')


@app.route('/leaderboard', methods=['GET', 'POST'])
def leaderboard():
    cursor = con.cursor()
    cursor.execute("SELECT nom, score FROM USERS ORDER BY score DESC")
    users = cursor.fetchall()
    print(users)
    print(users[0][0])
    con.commit()
    return render_template('Classement.html', users=users)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
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


@app.route('/save_pseudo', methods=['POST'])
def save_pseudo():
    if request.method == 'POST':
        data = request.get_json()
        pseudo = data.get('pseudo')

        print("Il passe dans le save pseudo")

        if 'username' in session:
            username = session['username']
            cursor = con.cursor()
            cursor.execute('UPDATE USERS SET pseudo = ? WHERE nom = ?', (pseudo, username))
            con.commit()
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
