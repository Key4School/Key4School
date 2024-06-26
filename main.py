from db_poo import *
from flask import Flask
from flask_socketio import SocketIO
from flask_hashing import Hashing
from datetime import *
from flask_session import Session
from flask.json import jsonify
from dotenv import load_dotenv
import json
import sys
import os
from uuid import uuid4
import re
from routing import *

# Création de l'application
# sys.path.insert(0, os.path.dirname(__file__))
app = Flask(__name__)
socketio = SocketIO(app)
hashing = Hashing(app)

'''Routing'''

'''accueil.py'''
app.add_url_rule('/', view_func=accueil)
app.add_url_rule('/help/', view_func=tuto)
app.add_url_rule('/XP_tuto/', view_func=XP_tuto)
# A SUPPRIMER
app.add_url_rule('/mail_rendu/', view_func=mail_rendu)
app.add_url_rule('/saved/', view_func=saved)
app.add_url_rule('/about/', view_func=about)
app.add_url_rule('/leaderboard/', view_func=leaderboard, defaults={'top': 'france', 'widget': 0})
app.add_url_rule('/leaderboard/<top>/', view_func=leaderboard, defaults={'widget': 0})
app.add_url_rule('/leaderboard/<top>/<int:widget>', view_func=leaderboard)

'''administration.py'''
app.add_url_rule('/administration/', view_func=administration, methods=['POST', 'GET'])
app.add_url_rule('/suppressionMsg/', view_func=suppressionMsg, methods=['POST'])
app.add_url_rule('/validerMsg/', view_func=validerMsg, methods=['POST'])
app.add_url_rule('/sanction/', view_func=sanction, methods=['POST'])
app.add_url_rule('/signPost/', view_func=signPost, methods=['POST'])
app.add_url_rule('/signRepPost/', view_func=signRepPost, methods=['POST'])
app.add_url_rule('/signPostProfil/', view_func=signPostProfil, methods=['POST'])
app.add_url_rule('/signPostDiscussion/', view_func=signPostDiscussion, methods=['POST'])
app.add_url_rule('/signPostMsg/', view_func=signPostMsg, methods=['POST'])

'''demandes_aide.py'''
app.add_url_rule('/question/', view_func=question, methods=['POST', 'GET'])
app.add_url_rule('/comments/', view_func=comments, defaults={'idMsg': None})
app.add_url_rule('/comments/<idMsg>/', view_func=comments, methods=['GET', 'POST'])
app.add_url_rule('/updateDemand/', view_func=updateDemand, methods=['POST'])
app.add_url_rule('/updateComment/', view_func=updateComment, methods=['POST'])
app.add_url_rule('/file/<idFile>/', view_func=file)
app.add_url_rule('/DL_file/<idFile>/', view_func=DL_file)
app.add_url_rule('/likePost/<idPost>/', view_func=likePost, methods=['POST'])
app.add_url_rule('/likeRep/<idRep>/', view_func=likeRep, methods=['POST'])
app.add_url_rule('/resoudre/<idPost>/', view_func=resoudre, methods=['POST'])
app.add_url_rule('/savePost/<postId>/', view_func=savePost, methods=['POST'])

'''flask_error.py'''
# app.errorhandler(404)(custom_404)

'''functions.py'''

app.add_url_rule('/notif/<userId>/<notifId>/', view_func=afficheNotif)

'''login.py'''
app.add_url_rule('/login/', view_func=login, methods=['GET', 'POST'])
app.add_url_rule('/sign-in/0/', view_func=signIn0, methods=['GET', 'POST'])
app.add_url_rule('/sign-in/1/', view_func=signIn1, methods=['GET', 'POST'])
app.add_url_rule('/sign-in/2/', view_func=signIn2, methods=['GET', 'POST'])
app.add_url_rule('/logout/', view_func=logout)

'''messages.py'''
app.add_url_rule('/messages/', view_func=page_messages, defaults={'idGroupe': None})
app.add_url_rule('/messages/<idGroupe>/', view_func=page_messages)
app.add_url_rule('/redirectDM/<idUser1>/<idUser2>/', view_func=redirectDM)
app.add_url_rule('/uploadAudio/', view_func=uploadAudio, methods=['POST'])
app.add_url_rule('/audio/<audioId>/', view_func=audio)
app.add_url_rule('/uploadImage/', view_func=uploadImage, methods=['POST'])
app.add_url_rule('/image/<imageId>/', view_func=image)
app.add_url_rule('/createGroupe/', view_func=createGroupe, methods=['POST'])
app.add_url_rule('/updateGroupe/', view_func=updateGroupe, methods=['POST'])
app.add_url_rule('/virerParticipant/', view_func=virerParticipant, methods=['POST'])
app.add_url_rule('/modifRole/', view_func=modifRole, methods=['POST'])
app.add_url_rule('/supprGroupe/<idGrp>/', view_func=supprGroupe, methods=['POST'])
app.add_url_rule('/updateGrpName/<idGrp>/<newGrpName>/', view_func=updateGrpName, methods=['POST'])
app.add_url_rule('/moreMsg/', view_func=moreMsg, methods=['POST'])
app.add_url_rule('/modererGrp/<idGrp>/', view_func=modererGrp, methods=['POST'])

'''profil.py'''
app.add_url_rule('/profil/', view_func=profil, defaults={'idUser': None})
app.add_url_rule('/profil/<idUser>/', view_func=profil)
app.add_url_rule('/changeTheme/', view_func=changeTheme, methods=['POST'])
app.add_url_rule('/theme/', view_func=theme, methods=['POST'])
app.add_url_rule('/updateprofile/', view_func=updateprofile, methods=['POST'])
app.add_url_rule('/userImg/<profilImg>/', view_func=userImg)
app.add_url_rule('/updateImg/', view_func=updateImg, methods=['POST'])
app.add_url_rule('/otherSubject/', view_func=otherSubject, methods=['POST'])
app.add_url_rule('/topLeaderboard/<top>/', view_func=topLeaderboard)
app.add_url_rule('/deleteAccount/', view_func=deleteAccount, methods=['POST'])
app.add_url_rule('/emailNotVerify/', view_func=emailNotVerify)
app.add_url_rule('/emailVerification/<id>/', view_func=emailVerification)

'''recherche.py'''
app.add_url_rule('/recherche/', view_func=recherche)
app.add_url_rule('/rechercheUser/', view_func=recherche_user)
app.add_url_rule('/morePost/', view_func=morePost, methods=['POST'])
app.add_url_rule('/moreUser/', view_func=moreUser, methods=['POST'])

'''sockets.py'''
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


if __name__ == "__main__":
    app.config['cacheRandomKey'] = uuid4()
    app.config['socketio'] = socketio
    app.config['hashing'] = hashing

    if os.path.exists('.env'):
        load_dotenv()

    # This allows us to use a plain HTTP callback
    app.secret_key = os.urandom(24)

    # clé de hash
    app.config['hashingKey'] = 'hqZcPsAkTaMIRHco1L1BhCxXo4LWwBBBRvGcydjH0Vb85uXB3ZQ1lfmvfg7laldlaosg21Ri8uPvDgxLYyUoAPVXaQbNvpvpcvuyIv7ckVGGS6Ro5tmh8TlphoG25Z13RftlviLXggzJ4LXVJFjZ3xtUQ27zUJzQZAoI9JOAxXAV3VBdATqX'
    # Lancement de l'application, à l'adresse 127.0.0.0 et sur le port 3000
    # app.run(host="127.0.0.1", port=3000, debug=True)
    socketio.run(app, host='127.0.0.1', port=3000, debug=True)
