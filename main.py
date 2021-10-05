from flask import Flask, render_template, request, redirect, session, url_for, abort, escape, send_file
from flask_pymongo import PyMongo
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask_hashing import Hashing
from datetime import *
from requests_oauthlib import OAuth2Session
from flask_session import Session
from flask.json import jsonify
from bson.objectid import ObjectId
from bson import Binary
import sys
import os
import gridfs
import smtplib
from threading import Timer
from functools import partial
from uuid import uuid4
from difflib import SequenceMatcher
import re

# Création de l'application
sys.path.insert(0, os.path.dirname(__file__))
app = Flask(__name__)
socketio = SocketIO(app)
application = socketio
hashing = Hashing(app)

# DB POO
from db_poo import *

# Création du Cluster de la DB
# acienne DB
# DB = DB_Manager.createCluster(app, "mongodb+srv://CTLadmin:ctlADMIN@ctlbdd.etzx9.mongodb.net/CTLBDD?retryWrites=true&w=majority")
# New DB
DB = DB_Manager.createCluster(app, "mongodb+srv://les-codeurs-lbp:ezEwMi2KBaCkzT4@cluster0.bggb1.mongodb.net/key4schoolBDD?retryWrites=true&w=majority")

# Routing
from routing.accueil import accueil, accueil2, tuto, XP_tuto, mail_rendu, saved
from routing.recherche import recherche, recherche_user, morePost, moreUser
from routing.messages import page_messages, redirectDM, uploadAudio, audio, uploadImage, image, createGroupe, updateGroupe, virerParticipant, modifRole, supprGroupe, updateGrpName, moreMsg, modererGrp
from routing.administration import administration, suppressionMsg, validerMsg, sanction, signPost, signRepPost, signPostProfil, signPostDiscussion, signPostMsg
from routing.profil import profil, changeTheme, updateprofile, userImg, updateImg, otherSubject
from routing.demandes_aide import question, redirect_comments, comments, updateDemand, updateComment, file, DL_file, likePost, likeRep, resoudre, savePost
from routing.sockets import connectToNotif, disconnect, supprNotif, connectToGroup, postMsg, postLike
from routing.functions import listeModeration, automoderation, afficheNotif

app.add_url_rule('/', 'accueil', accueil)
app.add_url_rule('/accueil/', 'accueil2', accueil2)
app.add_url_rule('/morePost/', 'morePost', morePost, methods=['POST'])
app.add_url_rule('/moreUser/', 'moreUser', moreUser, methods=['POST'])
app.add_url_rule('/moreMsg/', 'moreMsg', moreMsg, methods=['POST'])
app.add_url_rule('/modererGrp/<idGrp>/', 'modererGrp', modererGrp, methods=['POST'])
app.add_url_rule('/messages/', 'page_messages', page_messages, defaults={'idGroupe': None})
app.add_url_rule('/messages/<idGroupe>/', 'page_messages', page_messages)
app.add_url_rule('/redirectDM/<idUser1>/<idUser2>/', 'redirectDM', redirectDM)
app.add_url_rule('/uploadImage/', 'uploadImage', uploadImage, methods=['POST'])
app.add_url_rule('/image/<imageName>/', 'image', image)
app.add_url_rule('/uploadAudio/', 'uploadAudio', uploadAudio, methods=['POST'])
app.add_url_rule('/audio/<audioName>/', 'audio', audio)
app.add_url_rule('/suppressionMsg/', 'suppressionMsg', suppressionMsg, methods=['POST'])
app.add_url_rule('/validerMsg/', 'validerMsg', validerMsg, methods=['POST'])
app.add_url_rule('/createGroupe/', 'createGroupe', createGroupe, methods=['POST'])
app.add_url_rule('/updateGroupe/', 'updateGroupe', updateGroupe, methods=['POST'])
app.add_url_rule('/virerParticipant/', 'virerParticipant', virerParticipant, methods=['POST'])
app.add_url_rule('/modifRole/', 'modifRole', modifRole, methods=['POST'])
app.add_url_rule('/supprGroupe/<idGrp>/', 'supprGroupe', supprGroupe, methods=['POST'])
app.add_url_rule('/updateGrpName/<idGrp>/<newGrpName>/', 'updateGrpName', updateGrpName, methods=['POST'])
app.add_url_rule('/changeTheme/', 'changeTheme', changeTheme, methods=['POST'])
app.add_url_rule('/profil/', 'profil', profil, methods=['POST', 'GET'], defaults={'idUser': None})
app.add_url_rule('/profil/<idUser>/', 'profil', profil, methods=['POST', 'GET'])
app.add_url_rule('/updateprofile/', 'updateprofile', updateprofile, methods=['POST'])
app.add_url_rule('/otherSubject/', 'otherSubject', otherSubject, methods=['POST'])
app.add_url_rule('/userImg/<profilImg>/', 'userImg', userImg)
app.add_url_rule('/updateImg/', 'updateImg', updateImg, methods=['POST'])
app.add_url_rule('/question/', 'question', question, methods=['POST', 'GET'])
app.add_url_rule('/comments/', 'redirect_comments', redirect_comments)
app.add_url_rule('/comments/<idMsg>/', 'comments', comments, methods=['GET', 'POST'])
app.add_url_rule('/updateDemand/', 'updateDemand', updateDemand, methods=['POST'])
app.add_url_rule('/updateComment/', 'updateComment', updateComment, methods=['POST'])
app.add_url_rule('/file/<fileName>/', 'file', file)
app.add_url_rule('/DL_file/<fileName>/<fileType>/', 'DL_file', DL_file)
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
app.add_url_rule('/help/', 'tuto', tuto)
app.add_url_rule('/XP_tuto/', 'XP_tuto', XP_tuto)
app.add_url_rule('/mail_rendu/', 'mail_rendu', mail_rendu)
app.add_url_rule('/saved/', 'saved', saved)
app.add_url_rule('/savePost/<postId>/', 'savePost', savePost, methods=['POST'])
app.add_url_rule('/notif/<userId>/<notifId>/', 'afficheNotif', afficheNotif)

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

@app.route('/sign-in/0/', methods=['GET', 'POST'])
def signIn():
    if request.method == 'POST':
        hash = hashing.hash_value(request.form['mdp'], salt=cle)

        pseudo = (request.form['pseudo'].lower()).replace(' ', '_')

        _id = ObjectId()
        utilisateurs[str(_id)] = Utilisateur({"_id": _id, "nom": request.form['nom'], "prenom": request.form['prenom'], "pseudo": request.form['pseudo'], "email" : request.form['email'], 'mdp': hash})
        utilisateurs[str(_id)].insert()

        user = utilisateurs[str(_id)].toDict()
        session['id'] = str(user['_id'])
        session['pseudo'] = user['pseudo']
        session['couleur'] = user['couleur']
        session['type'] = 'ELEVE'
        session['cacheRandomKey'] = cacheRandomKey
        return redirect(url_for('signIn1'))
    else:
        return render_template('inscription0.html')

@app.route('/sign-in/1/', methods=['GET', 'POST'])
def signIn1():
    if request.method == 'POST':
        # hash = hashing.hash_value(request.form['mdp'], salt=cle)
        #
        # pseudo = (request.form['pseudo'].lower()).replace(' ', '_')
        #
        # _id = ObjectId()
        # utilisateurs[str(_id)] = Utilisateur({"_id": _id, "nom": request.form['nom'], "prenom": request.form['prenom'], "pseudo": request.form['pseudo'], "email" : request.form['email'], 'mdp': hash})
        # utilisateurs[str(_id)].insert()
        #
        # user = utilisateurs[str(_id)].toDict()
        # session['id'] = str(user['_id'])
        # session['pseudo'] = user['pseudo']
        # session['couleur'] = user['couleur']
        # session['type'] = 'ELEVE'
        # session['cacheRandomKey'] = cacheRandomKey
        return redirect(url_for('signIn1'))
    else:
        return render_template('inscription0.html')

# # Fonction de test pour afficher ce que l'on récupère
# @app.route("/connexion/", methods=["GET"])
# def connexion():
#     global utilisateurs
#     global groupes
#
#     """Fetching a protected resource using an OAuth 2 token.
#     """
#     ENT_reply = OAuth2Session(client_id, token=session['oauth_token'])
#     data = ENT_reply.get('https://ent.iledefrance.fr/auth/oauth2/userinfo').json()
#     data_plus = ENT_reply.get('https://ent.iledefrance.fr/directory/myinfos').json()
#
#     user = [u.toDict() for u in utilisateurs.values() if u.idENT == data['userId']]
#     if len(user) > 0:
#         user = user[0]
#     else:
#         user = None
#
#     if user != None:
#         session['id'] = str(user['_id'])
#         session['pseudo'] = user['pseudo']
#         session['couleur'] = user['couleur']
#         session['type'] = user['type']
#         session['cacheRandomKey'] = cacheRandomKey
#
#         u = utilisateurs[str(user['_id'])]
#         if user['SanctionEnCour'] != "":
#             if user['SanctionDuree'] < datetime.now():
#                 u.SanctionEnCour = ''
#                 u.SanctionDuree = ''
#
#         if u.type == "ELEVE":
#             classe = data_plus['classes'][0].split('$')[1]
#             u.classe = classe
#             nomClasse = f"{user['lycee']}/{classe}"
#             group = [g for g in groupes.values() if g.nom == nomClasse and g.is_class == True]
#             if len(group) > 0:
#                 group = group[0]
#                 if user['_id'] not in group.id_utilisateurs:
#                     group.id_utilisateurs.append(user['_id'])
#                     group.update()
#             else:
#                 _id = ObjectId()
#                 groupes[str(_id)] = Groupe({'_id': _id, 'nom': nomClasse, 'is_class': True, 'id-utilisateurs': [user['_id']]})
#                 groupes[str(_id)].insert()
#             # on retire l'user des anciens groupe de classe
#             oldGroups = [g for g in groupes.values() if g.nom != nomClasse and g.is_class == True and user['_id'] in g.id_utilisateurs]
#             for oldGroup in oldGroups:
#                 oldGroup.supprUser(user['_id'])
#
#         if data_plus['email'] != '':
#             u.email = data_plus['email']
#
#         if 'mobile' in data_plus:
#             if data_plus['mobile'] != "":
#                 u.telephone = data_plus['mobile']
#         elif 'homePhone' in data_plus:
#             if data_plus['homePhone'] != "":
#                 u.telephone = data_plus['homePhone']
#
#         if data_plus['emailInternal'] != '':
#             u.emailENT = data_plus['emailInternal']
#
#         utilisateurs[str(user['_id'])].update()
#
#         if 'redirect' in session:
#             path = session['redirect']
#             session.pop('redirect')
#             return redirect(path)
#         else:
#             return redirect(url_for('accueil'))
#
#     else:
#         if data['type'] == "ELEVE":
#             classe = data_plus['classes'][0].split('$')[1]
#             pseudo = (request.form['pseudo'].lower()).replace(' ', '_')
#             tel = ''
#             if 'mobile' in data_plus:
#                 if data_plus['mobile'] != "":
#                     tel = data_plus['mobile']
#             elif 'homePhone' in data_plus:
#                 if data_plus['homePhone'] != "":
#                     tel = data_plus['homePhone']
#
#             _id = ObjectId()
#             utilisateurs[str(_id)] = Utilisateur({"_id": _id, "idENT": data['userId'], "nom": data['lastName'], "prenom": data['firstName'], "pseudo": pseudo, 'nomImg': '', "dateInscription": datetime.now(),
#                                         "birth_date": datetime.strptime(data['birthDate'], '%Y-%m-%d') if data['birthDate'] != None else None, "classe": classe, "email" : data_plus['email'], "telephone": tel, "emailENT": data_plus['emailInternal'],
#                                         "lycee": data['schoolName'], 'spes': [], 'langues': [], 'options': [], 'couleur': ['#00b7ff', '#a7ceff', '#94e1ff', '#d3e6ff'], 'type': data['type'], 'elementPublic': [],
#                                         'elementPrive': ['email', 'telephone', 'interets', 'birth_date', 'caractere'], "sign": [], "SanctionEnCour": "", 'xp': 0})
#             utilisateurs[str(_id)].insert()
#
#             user = utilisateurs[str(_id)].toDict()
#             session['id'] = str(user['_id'])
#             session['pseudo'] = user['pseudo']
#             session['couleur'] = ['#00b7ff', '#a7ceff', '#94e1ff', '#d3e6ff', '#6595d1']
#             session['type'] = user['type']
#             session['cacheRandomKey'] = cacheRandomKey
#
#             nomClasse = f"{data['schoolName']}/{classe}"
#             group = [g for g in groupes.values() if g.nom == nomClasse and g.is_class == True]
#             if len(group) > 0:
#                 group = group[0]
#                 if user['_id'] not in group.id_utilisateurs:
#                     group.id_utilisateurs.append(user['_id'])
#                     group.update()
#             else:
#                 _id = ObjectId()
#                 groupes[str(_id)] = Groupe({'_id': _id, 'nom': nomClasse, 'is_class': True, 'id-utilisateurs': [user['_id']]})
#                 groupes[str(_id)].insert()
#
#             return redirect(url_for('tuto'))
#
#         elif data['type'] == 'ENSEIGNANT':
#             pseudo = (request.form['pseudo'].lower()).replace(' ', '_')
#             tel = ''
#             if 'mobile' in data_plus:
#                 if data_plus['mobile'] != "":
#                     tel = data_plus['mobile']
#             elif 'homePhone' in data_plus:
#                 if data_plus['homePhone'] != "":
#                     tel = data_plus['homePhone']
#
#             _id = ObjectId()
#             utilisateurs[str(_id)] = Utilisateur({"_id": _id, "idENT": data['userId'], "nom": data['lastName'], "prenom": data['firstName'], "pseudo": pseudo, "dateInscription": datetime.now(), "birth_date": datetime.strptime(
#                 data['birthDate'], '%Y-%m-%d') if data['birthDate'] != None else None, "lycee": data['schoolName'], 'couleur': ['#00b7ff', '#a7ceff', '#94e1ff', '#d3e6ff'], 'type': data['type'], 'elementPublic': [], 'elementPrive': ['email', 'telephone', 'interets',
#                 'birth_date', 'caractere'], "email" : data_plus['email'], "telephone": tel, "emailENT": data_plus['emailInternal'], "sign": [], "SanctionEnCour": "", 'xp': 0, 'nomImg': ''})
#             utilisateurs[str(_id)].insert()
#
#             user = utilisateurs[str(_id)].toDict()
#
#             session['id'] = str(user['_id'])
#             session['pseudo'] = user['pseudo']
#             session['couleur'] = ['#00b7ff', '#a7ceff', '#94e1ff', '#d3e6ff', '#6595d1']
#             session['type'] = user['type']
#             session['cacheRandomKey'] = cacheRandomKey
#
#             return redirect(url_for('tuto'))
#
#         # elif data['type'] == 'PARENT':
#         #     # return redirect("https://ent.iledefrance.fr/timeline/timeline")
#
#         else:
#             pseudo = (request.form['pseudo'].lower()).replace(' ', '_')
#             tel = ''
#             if 'mobile' in data_plus:
#                 if data_plus['mobile'] != "":
#                     tel = data_plus['mobile']
#             elif 'homePhone' in data_plus:
#                 if data_plus['homePhone'] != "":
#                     tel = data_plus['homePhone']
#
#             _id = ObjectId()
#             utilisateurs[str(_id)] = Utilisateur({"_id": _id, "idENT": data['userId'], "nom": data['lastName'], "prenom": data['firstName'], "pseudo": pseudo, "dateInscription": datetime.now(), "birth_date": datetime.strptime(
#                 data['birthDate'], '%Y-%m-%d') if data['birthDate'] != None else None, "lycee": data['schoolName'], 'couleur': ['#00b7ff', '#a7ceff', '#94e1ff', '#d3e6ff'], 'type': data['type'], 'elementPublic': [], 'elementPrive': ['email', 'telephone', 'interets',
#                 'birth_date', 'caractere'], "email" : data_plus['email'], "telephone": tel, "emailENT": data_plus['emailInternal'], "sign": [], "SanctionEnCour": "", 'xp': 0, 'nomImg': ''})
#             utilisateurs[str(_id)].insert()
#
#             user = utilisateurs[str(_id)].toDict()
#
#             session['id'] = str(user['_id'])
#             session['pseudo'] = user['pseudo']
#             session['couleur'] = ['#00b7ff', '#a7ceff', '#94e1ff', '#d3e6ff', '#6595d1']
#             session['type'] = user['type']
#             session['cacheRandomKey'] = cacheRandomKey
#
#             return redirect(url_for('tuto'))


if __name__ == "__main__":
    cacheRandomKey = uuid4()

    # This allows us to use a plain HTTP callback
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
    app.secret_key = os.urandom(24)
    cle = 'hqZcPsAkTaMIRHco1L1BhCxXo4LWwBBBRvGcydjH0Vb85uXB3ZQ1lfmvfg7laldlaosg21Ri8uPvDgxLYyUoAPVXaQbNvpvpcvuyIv7ckVGGS6Ro5tmh8TlphoG25Z13RftlviLXggzJ4LXVJFjZ3xtUQ27zUJzQZAoI9JOAxXAV3VBdATqX'

    if 'redirect_uri' in os.environ:
        # Lancement de l'application, à l'adresse 127.0.0.0 et sur le port 3000
        # app.run(host='0.0.0.0', port=os.environ.get("PORT", 3000))
        # socketio.run(app, host='0.0.0.0', port=os.environ.get("PORT", 3000), debug=True)
        socketio.run(app)
    
    else:
        # Lancement de l'application, à l'adresse 127.0.0.0 et sur le port 3000
        # app.run(host="127.0.0.1", port=3000, debug=True)
        socketio.run(app, host='127.0.0.1', port=3000, debug=True)
