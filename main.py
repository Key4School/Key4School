from flask import Flask, render_template, request
import pronotepy  # api Pronote
from pronotepy.ent import ile_de_france

# Création de l'application


app = Flask(__name__)

'''connexion a l'api Pronote avec l'username et le mdp ENT mais je suis pas sur que ca va etre possible'''
'''le lien de l'api pour plus d'info https://github.com/bain3/pronotepy'''
# client = pronotepy.Client('https://0910626l.index-education.net/pronote/eleve.html',
#                           username=username,
#                           password=mdpENT,
#                           ent=ile_de_france)


# Quand on arrive sur le site, on affiche la page "ma_page.html"
# salut
@app.route('/')
def accueil():
    return render_template("index.html")


@app.route('/accueil')
def accueil2():
    return render_template("index.html")


@app.route('/messages')
def messages():
    return render_template("messages.html")


@app.route('/profile')
def profile():
    return render_template("profile.html")


# Lancement de l'application, à l'adresse 127.0.0.0 et sur le port 3000
app.run(host="127.0.0.1", port=3000)
