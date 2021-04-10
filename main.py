from flask import Flask, render_template, request
import pronotepy  # api Pronote
from pronotepy.ent import ile_de_france
from flask_pymongo import PyMongo
from datetime import *

# Création de l'application
app = Flask(__name__)

# Récupération d'une base de données
cluster = PyMongo(
    app, "mongodb+srv://CTLadmin:ctlADMIN@ctlbdd.etzx9.mongodb.net/CTLBDD?retryWrites=true&w=majority")
# Voici deux exemples pour créer des BDD
db_utilisateurs = cluster.db.tilisateurs
db_demande_aide = cluster.db.demande_aide
db_messages = cluster.db.messages
# Voici un exemple pour ajouter un utilisateur avec son nom et son mot de passe
# db_utilisateurs.insert_one({"nom" : "JEAN", "passe": "oui"})


'''connexion a l'api Pronote avec l'username et le mdp ENT mais je suis pas sur que ca va etre possible'''
'''le lien de l'api pour plus d'info https://github.com/bain3/pronotepy'''
# client = pronotepy.Client('https://0910626l.index-education.net/pronote/eleve.html',
#                           username=username,
#                           password=mdpENT,
#                           ent=ile_de_france)


# Quand on arrive sur le site, on affiche la page "ma_page.html"

@app.route('/')
def accueil():
    return render_template("index.html")


# laisser le nom entre deux slash ca permet d'accepter toutes les urls du style http://127.0.0.1:3000/messages/ sinon ca marche pas.s
@app.route('/accueil/')
def accueil2():
    return render_template("index.html")


@app.route('/messages/')
def messages():
    if request.method == 'GET':
        return render_template("messages.html")

    elif request.method == 'POST':
        db_messages.insert_one({"id-groupe": "quand on l'aura", "id-utilisateur": "quand on l'aura",
                                "contenu": request.form['contenuMessage'], "date-envoi": datetime.now(), "img": ""})
        return 'sent'


@app.route('/profile/')
def profile():
    return render_template("profile.html")


@app.route('/archives/')
def archives():
    return render_template("archives.html")


@app.route('/classe/')
def classe():
    return render_template("classe.html")


@app.route('/monlycee/')
def monlycee():
    return render_template("monlycee.html")


@app.route('/professeur/')
def professeur():
    return render_template("professeur.html")


@app.route('/question/')
def question():
    return render_template("question.html")


# Lancement de l'application, à l'adresse 127.0.0.0 et sur le port 3000
app.run(host="127.0.0.1", port=3000)
