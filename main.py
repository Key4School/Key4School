from flask import Flask, render_template, request, redirect, session, url_for
# import pronotepy  # api Pronote
# from pronotepy.ent import ile_de_france
from flask_pymongo import PyMongo
from datetime import *
from requests_oauthlib import OAuth2Session
from flask_session import Session
from flask.json import jsonify
from bson.objectid import ObjectId
import os

# Création de l'application
app = Flask(__name__)


# Le client secret est le code secret de l'application
# NE PAS TOUCHER AUX 4 LIGNES SUIVANTES, C'EST POUR LA CONNEXION A L'ENT
client_id = 'code-ton-lycee'
client_secret = 'JR7XcyGWBHt2VA9W'
authorization_base_url = 'https://ent.iledefrance.fr/auth/oauth2/auth'
token_url = 'https://ent.iledefrance.fr/auth/oauth2/token'

# Récupération d'une base de données
cluster = PyMongo(
    app, "mongodb+srv://CTLadmin:ctlADMIN@ctlbdd.etzx9.mongodb.net/CTLBDD?retryWrites=true&w=majority")
# Voici deux exemples pour créer des BDD
db_utilisateurs = cluster.db.utilisateurs
db_demande_aide = cluster.db.demande_aide
db_messages = cluster.db.messages
db_groupes = cluster.db.groupes
# Voici un exemple pour ajouter un utilisateur avec son nom et son mot de passe

'''connexion a l'api Pronote avec l'username et le mdp ENT mais je suis pas sur que ca va etre possible'''
'''le lien de l'api pour plus d'info https://github.com/bain3/pronotepy'''
# client = pronotepy.Client('https://0910626l.index-education.net/pronote/eleve.html',
#                           username=username,
#                           password=mdpENT,
#                           ent=ile_de_france)


# Quand on arrive sur le site, on affiche la page "ma_page.html"
@app.route('/')
def accueil():
    if 'id' in session:
        return render_template("index.html")
    else:
        return redirect(url_for('login'))


# laisser le nom entre deux slash ca permet d'accepter toutes les urls du style http://127.0.0.1:3000/messages/ sinon ca marche pas.s
@app.route('/accueil/')
def accueil2():
    if 'id' in session:
        return render_template("index.html")
    else:
        return redirect(url_for('login'))


@app.route('/messages/', defaults={'idGroupe': None}, methods=['POST', 'GET'])
@app.route('/messages/<idGroupe>', methods=['POST', 'GET'])
def messages(idGroupe):
    if 'id' in session:
        if request.method == 'GET':
            # il faudra récupérer l'id qui sera qans un cookie
            grp = db_groupes.find(
                {"$or": [{"id-utilisateurs": ObjectId('6075cae8fb56bf0654e5f4ab')}, {"id-utilisateurs": ObjectId(session['id'])}]})
            if idGroupe != None:
                msgDb = db_messages.aggregate([
                    {'$match': {'id-groupe': ObjectId(idGroupe)}},
                    {'$lookup':
                        {
                            'from': 'messages',
                            'localField': 'reponse',
                            'foreignField': '_id',
                            'as': 'rep',
                        }
                     }, {'$set': {'rep': {'$arrayElemAt': ["$rep", 0]}}},
                    {'$project': {
                        '_id': 1,
                        'id-groupes': 1,
                        'id-utilisateur': 1,
                        'contenu': 1,
                        'date-envoi': 1,
                        'rep': 1,
                    }},
                ])
                infogroupes = db_groupes.find_one(
                    {"_id": ObjectId(idGroupe)})
                infoUtilisateurs = []
                for content in infogroupes['id-utilisateurs']:
                    infoUtilisateurs += db_utilisateurs.find(
                        {"_id": ObjectId(content)})
                if session['id'] in str(infoUtilisateurs) or '6075cae8fb56bf0654e5f4ab' in str(infoUtilisateurs):
                    danslegroupe = True
                else:
                    danslegroupe = False
                    msgDb = None
                    infogroupes = None
                    infoUtilisateurs = None
            else:
                msgDb = None
                infogroupes = None
                infoUtilisateurs = None
            return render_template("messages.html", msgDb=msgDb, grpUtilisateur=grp, idgroupe=idGroupe, infogroupe=infogroupes, infoUtilisateurs=infoUtilisateurs, users=db_utilisateurs.find(), sessionId=ObjectId(session['id']))

        elif request.method == 'POST':
            if request.form['reponse'] != "None":
                reponse = ObjectId(request.form['reponse'])
            else:
                reponse = "None"
            db_messages.insert_one({"id-groupe": ObjectId(request.form['group']), "id-utilisateur": ObjectId(session['id']),
                                    "contenu": request.form['contenuMessage'], "date-envoi": datetime.now(), "img": "", "reponse": reponse})
            return 'sent'
    else:
        return redirect(url_for('login'))


@ app.route('/suppressionMsg/', methods=['POST'])
def supprimerMsg():
    if 'id' in session:
        idGroupe = request.form['grp']
        db_messages.delete_one({"_id": ObjectId(request.form['msgSuppr'])})
        return redirect(url_for('messages', idGroupe=idGroupe))
    else:
        return redirect(url_for('login'))


@ app.route('/createGroupe/', methods=['POST'])
def createGroupe():
    if 'id' in session:
        participants = [ObjectId(session['id'])]
        for name, value in request.form.items():
            if name == 'nomnewgroupe':
                pass
            else:
                participants.append(ObjectId(name))
        newGroupe = db_groupes.insert_one(
            {'nom': request.form['nomnewgroupe'], 'id-utilisateurs': participants})
        return redirect(url_for('messages', idGroupe=newGroupe.inserted_id))
    else:
        return redirect(url_for('login'))


@ app.route('/refreshMsg/')
def refreshMsg():
    if 'id' in session:
        idGroupe = request.args['idgroupe']
        if request.args['idMsg'] != 'undefined' and idGroupe != 'undefined' and idGroupe != 'None':
            dateLast = datetime.strptime(
                request.args['idMsg'], '%Y-%m-%dT%H:%M:%S.%fZ')
            infogroupes = db_groupes.find_one(
                {"_id": ObjectId(idGroupe)})
            infoUtilisateurs = []
            for content in infogroupes['id-utilisateurs']:
                infoUtilisateurs += db_utilisateurs.find(
                    {"_id": ObjectId(content)})
            msgDb = db_messages.aggregate([
                {'$match': {'$and': [
                    {'id-groupe': ObjectId(idGroupe)}, {'date-envoi': {'$gt': dateLast}}]}},
                {'$lookup':
                    {
                        'from': 'messages',
                        'localField': 'reponse',
                        'foreignField': '_id',
                        'as': 'rep',
                    }
                 }, {'$set': {'rep': {'$arrayElemAt': ["$rep", 0]}}},
                {'$project': {
                    '_id': 1,
                    'id-groupes': 1,
                    'id-utilisateur': 1,
                    'contenu': 1,
                    'date-envoi': 1,
                    'rep': 1,
                }},
            ])
            return render_template("refreshMessages.html", msgDb=msgDb, sessionId=ObjectId(session['id']), infoUtilisateurs=infoUtilisateurs)
        else:
            return ''
    else:
        return redirect(url_for('login'))


@ app.route('/changeTheme/', methods=['POST'])
def changeTheme():
    if 'id' in session:
        db_utilisateurs.update_one({"_id": ObjectId(session['id'])}, {
                                   "$set": {"couleur": request.form['couleur']}})
        session['couleur'] = request.form['couleur']
        return redirect(url_for('profil'))
    else:
        return redirect(url_for('login'))


@ app.route('/profil/')
def profil():
    if 'id' in session:
        return render_template("profil.html")
    else:
        return redirect(url_for('login'))


@ app.route('/archives/')
def archives():
    if 'id' in session:
        return render_template("archives.html")
    else:
        return redirect(url_for('login'))


@ app.route('/classe/')
def classe():
    if 'id' in session:
        return render_template("classe.html")
    else:
        return redirect(url_for('login'))


@ app.route('/monlycee/')
def monlycee():
    if 'id' in session:
        return render_template("monlycee.html")
    else:
        return redirect(url_for('login'))


@ app.route('/professeur/')
def professeur():
    if 'id' in session:
        return render_template("professeur.html")
    else:
        return redirect(url_for('login'))


@ app.route('/question/', methods=['POST', 'GET'])
def question():
    if 'id' in session:
        if request.method == 'POST':
            if 'demande' not in request.form:
                result = db_demande_aide.find(
                    {'$text': {'$search': request.form['research']}})

                return render_template('question.html', answer=result)
            else:
                db_demande_aide.insert_one(
                    {"id-utilisateur": ObjectId(session['id']), "titre": request.form['titre'], "contenu": request.form['demande'], "date-envoi": datetime.now(), "matière": request.form['matiere']})
                return render_template('question.html', envoi="Envoi réussi")
        else:
            return render_template('question.html')
    else:
        return redirect(url_for('login'))


@ app.route('/amis/')
def amis():
    if 'id' in session:
        return render_template("amis.html")
    else:
        return redirect(url_for('login'))


@ app.route('/deconnexion/')
def deconnexion():
    for s in session:
        session[s] = None
    return redirect(url_for('login'))


# TOUT LE CODE QUI VA SUIVRE PERMET LA CONNEXION A L'ENT VIA OAUTH
# Route qui va permettre de rediriger l'utilisateur sur le site d'authentification et de récupérer un token (pour pouvoir se connecter)
@ app.route("/login/")
def login():
    """Step 1: User Authorization.
    Redirect the user/resource owner to the OAuth provider (ENT)
    using an URL with a few key OAuth parameters.
    """
    ENT_reply = OAuth2Session(
        client_id, scope="userinfo", redirect_uri="http://127.0.0.1:3000/callback")
    authorization_url, state = ENT_reply.authorization_url(
        authorization_base_url)

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    return redirect(authorization_url)


# Step 2: User authorization, this happens on the provider (site de l'ENT).

# callback est la route pour le retour de l'identification
# On utilise le token pour indiquer que c'est bien l'utilisateur qui veut se connecter depuis l'app
@ app.route("/callback/", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.
    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    ENT_reply = OAuth2Session(
        client_id, state=session['oauth_state'],  redirect_uri="http://127.0.0.1:3000/callback")
    ENT_token = ENT_reply.fetch_token(token_url, client_id=client_id, client_secret=client_secret,
                                      code=request.args.get('code'))

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token
    # in /profil.
    session['oauth_token'] = ENT_token

    return redirect(url_for('.connexion'))


# Fonction de test pour afficher ce que l'on récupère
@ app.route("/connexion/", methods=["GET"])
def connexion():
    """Fetching a protected resource using an OAuth 2 token.
    """
    ENT_reply = OAuth2Session(client_id, token=session['oauth_token'])
    data = ENT_reply.get(
        'https://ent.iledefrance.fr/auth/oauth2/userinfo').json()
    user = db_utilisateurs.find_one({"idENT": data['userId']})
    if user != None:
        session['id'] = str(user['_id'])
        session['pseudo'] = user['pseudo']
        session['couleur'] = user['couleur']
    else:
        db_utilisateurs.insert_one({"idENT": data['userId'], "nom": data['lastName'], "prenom": data['firstName'], "pseudo": data['username'], "dateInscription": datetime.now(),
                                    "birth_date": datetime.strptime(data['birthDate'], '%Y-%m-%d'), "classe": data['level'], "lycee": data['schoolName'], 'couleur': '#3f51b5'})
        user = db_utilisateurs.find_one({"idENT": data['userId']})
        session['id'] = str(user['_id'])
        session['pseudo'] = user['pseudo']
        session['couleur'] = '#3f51b5'
    return redirect(url_for('accueil'))


if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

    app.secret_key = os.urandom(24)
    # Lancement de l'application, à l'adresse 127.0.0.0 et sur le port 3000
    app.run(host="127.0.0.1", port=3000, debug=True)
    # app.run(debug=True)
