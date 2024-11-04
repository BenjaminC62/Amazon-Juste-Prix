import requests
from bs4 import BeautifulSoup

def get_prix_article(article):
    r = requests.get(" http://ws.chez-wam.info/" + article)
    try:
        price = r.json()["price"][:-1] # récupère le prix de l'article
        for i in price:
            if i == ",":
                price = price.replace(i, ".")
            elif i == " ":
                price = price.replace(i, "")
        result = float(price) # converti la valeur du prix str -> float
        print(type(result))
    except:
        raise Exception("Prix de l'article n'est pas disponible !")
    return result

print(get_prix_article("B09PQ1DCLK"))