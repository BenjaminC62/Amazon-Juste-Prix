import sqlite3

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


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


if __name__ == '__main__':
    app.run()
