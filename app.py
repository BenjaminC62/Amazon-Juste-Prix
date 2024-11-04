import requests
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

def recupereImageArticle(article):  # put application's code here
    r = requests.get(" http://ws.chez-wam.info/" + article)
    image = r.json()["images"][0]
    return f"<img width='250px' height='250px' src='{image}'/>"

if __name__ == '__main__':
    app.run()
