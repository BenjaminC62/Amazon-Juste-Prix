import requests



def getNom(article):
    r = requests.get("http://ws.chez-wam.info/" + article)
    try :
        name = r.json()["title"]
    except :
        raise Exception("Article non trouvé")
    return name


print(getNom("B0B928B6BC"))