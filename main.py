from flask import Flask, render_template, request, redirect, session, url_for, abort, escape
from flask_pymongo import PyMongo
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from datetime import *
from requests_oauthlib import OAuth2Session
from flask_session import Session
from flask.json import jsonify
from bson.objectid import ObjectId
from bson import Binary
import os
import gridfs
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from difflib import SequenceMatcher

# DB POO
from db_poo import *

# Création de l'application
app = Flask(__name__)
socketio = SocketIO(app)

# Création du Cluster de la DB
DB = DB_Manager.createCluster(app, "mongodb+srv://CTLadmin:ctlADMIN@ctlbdd.etzx9.mongodb.net/CTLBDD?retryWrites=true&w=majority")

# Routing
from routing.accueil import accueil, accueil2
from routing.recherche import recherche, recherche_user, morePost, moreUser
from routing.messages import page_messages, uploadAudio, audio, createGroupe, updateGroupe, virerParticipant, modifRole
from routing.administration import administration, supprimerMsg, validerMsg, sanction, signPost, signRepPost, signPostProfil, signPostDiscussion, signPostMsg
from routing.profil import profil, changeTheme, updateprofile, userImg, updateImg
from routing.demandes_aide import question, redirect_comments, comments, updateDemand, updateComment, file, likePost, likeRep, resoudre
from routing.sockets import connectToNotif, disconnect, supprNotif, connectToGroup, postMsg, postLike
from routing.functions import recupLevel, addXP, addXpModeration, listeModeration, automoderation, sendNotif, clientsNotif

app.add_url_rule('/', 'accueil', accueil)
app.add_url_rule('/accueil/', 'accueil2', accueil2)
app.add_url_rule('/morePost/', 'morePost', morePost, methods=['POST'])
app.add_url_rule('/moreUser/', 'moreUser', moreUser, methods=['POST'])
app.add_url_rule('/messages/', 'page_messages', page_messages, defaults={'idGroupe': None})
app.add_url_rule('/messages/<idGroupe>/', 'page_messages', page_messages)
app.add_url_rule('/uploadAudio/', 'uploadAudio', uploadAudio, methods=['POST'])
app.add_url_rule('/audio/<audioName>/', 'audio', audio)
app.add_url_rule('/supprimerMsg/', 'supprimerMsg', supprimerMsg, methods=['POST'])
app.add_url_rule('/validerMsg/', 'validerMsg', validerMsg, methods=['POST'])
app.add_url_rule('/createGroupe/', 'createGroupe', createGroupe, methods=['POST'])
app.add_url_rule('/updateGroupe/', 'updateGroupe', updateGroupe, methods=['POST'])
app.add_url_rule('/virerParticipant/', 'virerParticipant', virerParticipant, methods=['POST'])
app.add_url_rule('/modifRole/', 'modifRole', modifRole, methods=['POST'])
app.add_url_rule('/changeTheme/', 'changeTheme', changeTheme, methods=['POST'])
app.add_url_rule('/profil/', 'profil', profil, methods=['POST', 'GET'], defaults={'idUser': None})
app.add_url_rule('/profil/<idUser>/', 'profil', profil, methods=['POST', 'GET'])
app.add_url_rule('/updateprofile/', 'updateprofile', updateprofile, methods=['POST'])
app.add_url_rule('/userImg/<profilImg>/', 'userImg', userImg)
app.add_url_rule('/updateImg/', 'updateImg', updateImg, methods=['POST'])
app.add_url_rule('/question/', 'question', question, methods=['POST', 'GET'])
app.add_url_rule('/comments/', 'redirect_comments', redirect_comments)
app.add_url_rule('/comments/<idMsg>/', 'comments', comments, methods=['GET', 'POST'])
app.add_url_rule('/updateDemand/', 'updateDemand', updateDemand, methods=['POST'])
app.add_url_rule('/updateComment/', 'updateComment', updateComment, methods=['POST'])
app.add_url_rule('/file/<fileName>/', 'file', file)
app.add_url_rule('/recherche/', 'recherche', recherche)
app.add_url_rule('/rechercheUser/', 'recherche_user', recherche_user)
app.add_url_rule('/likePost/<idPost>/', 'likePost', likePost, methods=['POST'])
app.add_url_rule('/likeRep/<idPost>/<idRep>/', 'likeRep', likeRep, methods=['POST'])
app.add_url_rule('/administration/', 'administration', administration, methods=['POST', 'GET'])
app.add_url_rule('/sanction/', 'sanction', sanction, methods=['POST'])
app.add_url_rule('/signPost/', 'signPost', signPost, methods=['POST'])
app.add_url_rule('/signRepPost/', 'signRepPost', signRepPost, methods=['POST'])
app.add_url_rule('/signPostProfil/', 'signPostProfil', signPostProfil, methods=['POST'])
app.add_url_rule('/signPostDiscussion/', 'signPostDiscussion', signPostDiscussion, methods=['POST'])
app.add_url_rule('/signPostMsg/', 'signPostMsg', signPostMsg, methods=['POST'])
app.add_url_rule('/resoudre/<idPost>/', 'resoudre', resoudre, methods=['POST'])


# route temporaire
@app.route('/mail/')
def mail():
    if 'id' in session:
        return render_template("mail.html")
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))


# Connection au groupe pour recevoir les nouvelles notif
@socketio.on('connectToNotif')
def handleEvent_connectToNotif():
    connectToNotif()

# Deconnexion au groupe pour recevoir les nouvelles notif
@socketio.on('disconnect')
def handleEvent_disconnect():
    disconnect()

@socketio.on('supprNotif')
def handleEvent_supprNotif(id):
    supprNotif(id)

# Connection au groupe pour recevoir les nouveaux messages par la suite
@socketio.on('connectToGroup')
def handleEvent_connectToGroup(json):
    connectToGroup(json)

@socketio.on('postMsg')
def handleEvent_postMsg(json):
    postMsg(json)


@socketio.on('postLike')
def handleEvent_postLike(json):
    postLike(json)


# TOUT LE CODE QUI VA SUIVRE PERMET LA CONNEXION A L'ENT VIA OAUTH
# Route qui va permettre de rediriger l'utilisateur sur le site d'authentification et de récupérer un token (pour pouvoir se connecter)
@app.route("/login/")
def login():
    """Step 1: User Authorization.
    Redirect the user/resource owner to the OAuth provider (ENT)
    using an URL with a few key OAuth parameters.
    """

    ENT_reply = OAuth2Session(client_id, scope=["userinfo", "myinfos", "userbook", "directory"], redirect_uri=redirect_uri)
    authorization_url, state = ENT_reply.authorization_url(authorization_base_url)

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state

    return redirect(authorization_url)


# Step 2: User authorization, this happens on the provider (site de l'ENT).

# callback est la route pour le retour de l'identification
# On utilise le token pour indiquer que c'est bien l'utilisateur qui veut se connecter depuis l'app
@app.route("/callback/", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.
    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    ENT_reply = OAuth2Session(client_id, state=session.get('oauth_state'), redirect_uri=redirect_uri)
    ENT_token = ENT_reply.fetch_token(token_url, client_id=client_id, client_secret=client_secret, code=request.args.get('code'))

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token
    # in /profil.
    session['oauth_token'] = ENT_token

    return redirect(url_for('connexion'))


# Fonction de test pour afficher ce que l'on récupère
@app.route("/connexion/", methods=["GET"])
def connexion():
    global utilisateurs
    global groupes

    """Fetching a protected resource using an OAuth 2 token.
    """
    ENT_reply = OAuth2Session(client_id, token=session['oauth_token'])
    data = ENT_reply.get('https://ent.iledefrance.fr/auth/oauth2/userinfo').json()
    data_plus = ENT_reply.get('https://ent.iledefrance.fr/directory/myinfos').json()

    user = [u.toDict() for u in utilisateurs.values() if u.idENT == data['userId']]
    if len(user) > 0:
        user = user[0]
    else:
        user = None

    if user != None:
        session['id'] = str(user['_id'])
        session['pseudo'] = user['pseudo']
        session['couleur'] = user['couleur']
        session['type'] = user['type']

        u = utilisateurs[str(user['_id'])]
        if user['SanctionEnCour'] != "":
            if user['SanctionDuree'] < datetime.now():
                u.SanctionEnCour = ''
                u.SanctionDuree = ''

        if u.type == "ELEVE":
            classe = data_plus['classes'][0].split('$')[1]
            u.classe = classe
            nomClasse = f"{user['lycee']}/{classe}"
            group = [g for g in groupes.values() if g.nom == nomClasse and g.is_class == True]
            if len(group) > 0:
                group = group[0]
                if user['_id'] not in group.id_utilisateurs:
                    group.id_utilisateurs.append(user['_id'])
                    group.update()
            else:
                _id = ObjectId()
                groupes[str(_id)] = Groupe({'_id': _id, 'nom': nomClasse, 'is_class': True, 'id-utilisateurs': [user['_id']]})
                groupes[str(_id)].insert()
            # on retire l'user des anciens groupe de classe
            oldGroups = [g for g in groupes.values() if g.nom != nomClasse and g.is_class == True and user['_id'] in g.id_utilisateurs]
            for oldGroup in oldGroups:
                oldGroups.supprUser(user['_id'])

        if data_plus['email'] != '':
            u.email = data_plus['email']

        if 'mobile' in data_plus:
            if data_plus['mobile'] != "":
                u.telephone = data_plus['mobile']
        elif 'homePhone' in data_plus:
            if data_plus['homePhone'] != "":
                u.telephone = data_plus['homePhone']

        if data_plus['emailInternal'] != '':
            u.emailENT = data_plus['emailInternal']

        utilisateurs[str(user['_id'])].update()

        if 'redirect' in session:
            path = session['redirect']
            session.pop('redirect')
            return redirect(path)
        else:
            return redirect(url_for('accueil'))

    else:
        if data['type'] == "ELEVE":
            classe = data_plus['classes'][0].split('$')[1]
            pseudo = (data['username'].lower()).replace(' ', '_')
            tel = ''
            if 'mobile' in data_plus:
                if data_plus['mobile'] != "":
                    tel = data_plus['mobile']
            elif 'homePhone' in data_plus:
                if data_plus['homePhone'] != "":
                    tel = data_plus['homePhone']

            _id = ObjectId()
            utilisateurs[str(_id)] = Utilisateur({"_id": _id, "idENT": data['userId'], "nom": data['lastName'], "prenom": data['firstName'], "pseudo": pseudo, 'nomImg': '', "dateInscription": datetime.now(),
                                        "birth_date": datetime.strptime(data['birthDate'], '%Y-%m-%d'), "classe": classe, "email" : data_plus['email'], "telephone": tel, "emailENT": data_plus['emailInternal'],
                                        "lycee": data['schoolName'], 'spes': [], 'langues': [], 'options': [], 'couleur': ['#00b7ff', '#a7ceff', '#94e1ff', '#d3e6ff'], 'type': data['type'], 'elementPublic': [],
                                        'elementPrive': ['email', 'telephone', 'interets', 'birth_date', 'caractere'], "sign": [], "SanctionEnCour": "", 'xp': 0})
            utilisateurs[str(_id)].insert()

            user = utilisateurs[str(_id)].toDict()
            session['id'] = str(user['_id'])
            session['pseudo'] = user['pseudo']
            session['couleur'] = ['#00b7ff', '#a7ceff', '#94e1ff', '#d3e6ff']
            session['type'] = user['type']

            nomClasse = f"{data['schoolName']}/{classe}"
            group = [g for g in groupes.values() if g.nom == nomClasse and g.is_class == True]
            if len(group) > 0:
                group = group[0]
                if user['_id'] not in group.id_utilisateurs:
                    group.id_utilisateurs.append(user['_id'])
                    group.update()
            else:
                _id = ObjectId()
                groupes[str(_id)] = Groupe({'_id': _id, 'nom': nomClasse, 'is_class': True, 'id-utilisateurs': [user['_id']]})
                groupes[str(_id)].insert()

            return redirect(url_for('profil'))

        elif data['type'] == 'ENSEIGNANT':
            pseudo = (data['username'].lower()).replace(' ', '_')
            tel = ''
            if 'mobile' in data_plus:
                if data_plus['mobile'] != "":
                    tel = data_plus['mobile']
            elif 'homePhone' in data_plus:
                if data_plus['homePhone'] != "":
                    tel = data_plus['homePhone']

            _id = ObjectId()
            utilisateurs[str(_id)] = Utilisateur({"_id": _id, "idENT": data['userId'], "nom": data['lastName'], "prenom": data['firstName'], "pseudo": pseudo, "dateInscription": datetime.now(), "birth_date": datetime.strptime(
                data['birthDate'], '%Y-%m-%d'), "lycee": data['schoolName'], 'couleur': ['#00b7ff', '#a7ceff', '#94e1ff', '#d3e6ff'], 'type': data['type'], 'elementPublic': [], 'elementPrive': ['email', 'telephone', 'interets',
                'birth_date', 'caractere'], "email" : data_plus['email'], "telephone": tel, "emailENT": data_plus['emailInternal'], "sign": [], "SanctionEnCour": "", 'xp': 0, 'nomImg': ''})
            utilisateurs[str(_id)].insert()

            user = utilisateurs[str(_id)].toDict()

            session['id'] = str(user['_id'])
            session['pseudo'] = user['pseudo']
            session['couleur'] = ['#00b7ff', '#a7ceff', '#94e1ff', '#d3e6ff']
            session['type'] = user['type']

            return redirect(url_for('profil'))

        else:
            return redirect("https://ent.iledefrance.fr/timeline/timeline")


if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
    app.secret_key = os.urandom(24)

    # NE PAS TOUCHER AUX 2 LIGNES SUIVANTES, C'EST POUR LA CONNEXION A L'ENT
    authorization_base_url = 'https://ent.iledefrance.fr/auth/oauth2/auth'
    token_url = 'https://ent.iledefrance.fr/auth/oauth2/token'

    if 'redirect_uri' in os.environ:
        # Le client secret est le code secret de l'application
        # NE PAS TOUCHER AUX 3 LIGNES SUIVANTES, C'EST POUR LA CONNEXION A L'ENT
        client_id = 'code-ton-lycee-key4school'
        client_secret = 'jHy6g8JG4FdP0a5VI2m'
        redirect_uri = os.environ['redirect_uri']

        # Lancement de l'application, à l'adresse 127.0.0.0 et sur le port 3000
        # app.run(host='0.0.0.0', port=os.environ.get("PORT", 3000))
        socketio.run(app, host='0.0.0.0', port=os.environ.get("PORT", 3000), debug=True)

    else:
        # Le client secret est le code secret de l'application
        # NE PAS TOUCHER AUX 2 LIGNES SUIVANTES, C'EST POUR LA CONNEXION A L'ENT
        client_id = 'code-ton-lycee-localhost'
        client_secret = 'JR7XcyGWBHt2VA9W'
        redirect_uri = "http://127.0.0.1:3000/callback"

        # Lancement de l'application, à l'adresse 127.0.0.0 et sur le port 3000
        # app.run(host="127.0.0.1", port=3000, debug=True)
        socketio.run(app, host='127.0.0.1', port=3000, debug=True)
