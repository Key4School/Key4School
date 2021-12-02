from db_poo import *
from flask import Flask, render_template, request, redirect, session, url_for, abort, escape, send_file
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask_hashing import Hashing
from datetime import *
from flask_session import Session
from flask.json import jsonify
import json
import sys
import os
from uuid import uuid4
import re

# Création de l'application
# sys.path.insert(0, os.path.dirname(__file__))
app = Flask(__name__)
hashing = Hashing(app)
socketio = SocketIO(app)

# Routing
from routing.functions import listeModeration, automoderation, afficheNotif
from routing.sockets import connectToNotif, disconnect, supprNotif, connectToGroup, postMsg, postLike
from routing.demandes_aide import question, redirect_comments, comments, updateDemand, updateComment, file, DL_file, likePost, likeRep, resoudre, savePost
from routing.profil import profil, changeTheme, theme, updateprofile, userImg, updateImg, otherSubject, logout
from routing.administration import administration, suppressionMsg, validerMsg, sanction, signPost, signRepPost, signPostProfil, signPostDiscussion, signPostMsg
from routing.messages import page_messages, redirectDM, uploadAudio, audio, uploadImage, image, createGroupe, updateGroupe, virerParticipant, modifRole, supprGroupe, updateGrpName, moreMsg, modererGrp
from routing.recherche import recherche, recherche_user, morePost, moreUser
from routing.accueil import accueil, tuto, XP_tuto, mail_rendu, saved, about, leaderboard

'''A TRIER PAR CATEGORIES'''
app.add_url_rule('/', view_func=accueil)
app.add_url_rule('/morePost/', view_func=morePost, methods=['POST'])
app.add_url_rule('/moreUser/', view_func=moreUser, methods=['POST'])
app.add_url_rule('/moreMsg/', view_func=moreMsg, methods=['POST'])
app.add_url_rule('/modererGrp/<idGrp>/', view_func=modererGrp, methods=['POST'])
app.add_url_rule('/messages/', view_func=page_messages, defaults={'idGroupe': None})
app.add_url_rule('/messages/<idGroupe>/', view_func=page_messages)
app.add_url_rule('/redirectDM/<idUser1>/<idUser2>/', view_func=redirectDM)
app.add_url_rule('/uploadImage/', view_func=uploadImage, methods=['POST'])
app.add_url_rule('/image/<imageId>/', view_func=image)
app.add_url_rule('/uploadAudio/', view_func=uploadAudio, methods=['POST'])
app.add_url_rule('/audio/<audioId>/', view_func=audio)
app.add_url_rule('/suppressionMsg/', view_func=suppressionMsg, methods=['POST'])
app.add_url_rule('/validerMsg/', view_func=validerMsg, methods=['POST'])
app.add_url_rule('/createGroupe/', view_func=createGroupe, methods=['POST'])
app.add_url_rule('/updateGroupe/', view_func=updateGroupe, methods=['POST'])
app.add_url_rule('/virerParticipant/', view_func=virerParticipant, methods=['POST'])
app.add_url_rule('/modifRole/', view_func=modifRole, methods=['POST'])
app.add_url_rule('/supprGroupe/<idGrp>/', view_func=supprGroupe, methods=['POST'])
app.add_url_rule('/updateGrpName/<idGrp>/<newGrpName>/', view_func=updateGrpName, methods=['POST'])
app.add_url_rule('/changeTheme/', view_func=changeTheme, methods=['POST'])
app.add_url_rule('/theme/', view_func=theme, methods=['POST'])
app.add_url_rule('/profil/', view_func=profil, methods=['POST', 'GET'], defaults={'idUser': None})
app.add_url_rule('/profil/<idUser>/', view_func=profil, methods=['POST', 'GET'])
app.add_url_rule('/updateprofile/', view_func=updateprofile, methods=['POST'])
app.add_url_rule('/otherSubject/', view_func=otherSubject, methods=['POST'])
app.add_url_rule('/userImg/<profilImg>/', view_func=userImg)
app.add_url_rule('/updateImg/', view_func=updateImg, methods=['POST'])
app.add_url_rule('/question/', view_func=question, methods=['POST', 'GET'])
app.add_url_rule('/comments/', view_func=redirect_comments)
app.add_url_rule('/comments/<idMsg>/', view_func=comments, methods=['GET', 'POST'])
app.add_url_rule('/updateDemand/', view_func=updateDemand, methods=['POST'])
app.add_url_rule('/updateComment/', view_func=updateComment, methods=['POST'])
app.add_url_rule('/file/<idFile>/', view_func=file)
app.add_url_rule('/DL_file/<idFile>/', view_func=DL_file)
app.add_url_rule('/recherche/', view_func=recherche)
app.add_url_rule('/rechercheUser/', view_func=recherche_user)
app.add_url_rule('/likePost/<idPost>/', view_func=likePost, methods=['POST'])
app.add_url_rule('/likeRep/<idRep>/', view_func=likeRep, methods=['POST'])
app.add_url_rule('/administration/', view_func=administration, methods=['POST', 'GET'])
app.add_url_rule('/sanction/', view_func=sanction, methods=['POST'])
app.add_url_rule('/signPost/', view_func=signPost, methods=['POST'])
app.add_url_rule('/signRepPost/', view_func=signRepPost, methods=['POST'])
app.add_url_rule('/signPostProfil/', view_func=signPostProfil, methods=['POST'])
app.add_url_rule('/signPostDiscussion/', view_func=signPostDiscussion, methods=['POST'])
app.add_url_rule('/signPostMsg/', view_func=signPostMsg, methods=['POST'])
app.add_url_rule('/resoudre/<idPost>/', view_func=resoudre, methods=['POST'])
app.add_url_rule('/help/', view_func=tuto)
app.add_url_rule('/XP_tuto/', view_func=XP_tuto)
app.add_url_rule('/mail_rendu/', view_func=mail_rendu)
app.add_url_rule('/saved/', view_func=saved)
app.add_url_rule('/leaderboard/', view_func=leaderboard)
app.add_url_rule('/savePost/<postId>/', view_func=savePost, methods=['POST'])
app.add_url_rule('/notif/<userId>/<notifId>/', view_func=afficheNotif)
app.add_url_rule('/about/', view_func=about)
app.add_url_rule('/logout/', view_func=logout)

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


@app.route('/login/', methods=['GET', 'POST'])
@db_session
def login():
    if request.method == 'POST':
        if 'password' not in request.form or 'username' not in request.form:
            return render_template('connexion.html', erreur='Veuillez compléter tous les champs')
        user = User.get(
            filter="cls.email == request.form['username'] or cls.pseudo == request.form['username']", limit=1)
        if not user or not hashing.check_value(user['mdp'], request.form['password'], salt=cle):
            return render_template('connexion.html', erreur='Identifiant ou mot de passe incorrect')
        session['id'] = user['id']
        session['pseudo'] = user['pseudo']
        session['couleur'] = user['couleur']
        session['theme'] = user['theme']
        session['type'] = user['type']
        session['cacheRandomKey'] = cacheRandomKey

        if user['etapeInscription'] is not None:
            session.pop('id')
            session['idInscri'] = user['id']
            session['etapeInscription'] = user['etapeInscription']
            return redirect(url_for(f"signIn{session['etapeInscription']}"))
        elif 'redirect' in session:
            path = session['redirect']
            session.pop('redirect')
            return redirect(path)
        else:
            return redirect(url_for('accueil'))
    else:
        session['cacheRandomKey'] = cacheRandomKey
        return render_template('connexion.html')


@app.route('/sign-in/0/', methods=['GET', 'POST'])
@db_session
def signIn0():
    if 'etapeInscription' in session:
        return redirect(url_for(f"signIn{session['etapeInscription']}"))

    if request.method == 'POST':
        notUse = False if User.get(
            filter="cls.email == request.form['email'] or cls.pseudo == request.form['pseudo']", limit=1) else True
        if notUse:
            hash = hashing.hash_value(request.form['password'], salt=cle)
            user = User(nom=request.form['nom'], prenom=request.form['prenom'],
                        pseudo=request.form['pseudo'], email=request.form['email'], mdp=hash, etapeInscription=1)
            user.insert()

            session['idInscri'] = user['id']
            session['cacheRandomKey'] = cacheRandomKey
            session['theme'] = user['theme']
            session['etapeInscription'] = 1
            return redirect(url_for('signIn1'))
        else:
            return render_template('inscription0.html', erreur='Pseudo ou email déjà utilisé')
    else:
        session['cacheRandomKey'] = cacheRandomKey
        return render_template('inscription0.html')


@app.route('/sign-in/1/', methods=['GET', 'POST'])
@db_session
def signIn1():
    if 'etapeInscription' not in session or 'idInscri' not in session:
        return redirect(url_for('login'))
    if session['etapeInscription'] != 1:
        return redirect(url_for(f"signIn{session['etapeInscription']}"))

    if request.method == 'POST':
        user = User.get(filter="cls.id == session['idInscri']", limit=1)
        user.signIn1(request.form['phone'],
                     datetime.strptime(request.form['birthday'], '%Y-%m-%d'),
                     json.loads(request.form['school']),
                     request.form['classe'],
                     [request.form['lva'], request.form['lvb']])
        session['etapeInscription'] = user['etapeInscription']
        return redirect(url_for('signIn2'))
    else:
        session['cacheRandomKey'] = cacheRandomKey
        return render_template('inscription1.html')


@app.route('/sign-in/2/', methods=['GET', 'POST'])
@db_session
def signIn2():
    if 'etapeInscription' not in session or 'idInscri' not in session:
        return redirect(url_for('login'))
    if session['etapeInscription'] != 2:
        return redirect(url_for(f"signIn{session['etapeInscription']}"))

    if request.method == 'POST':
        user = User.get(filter="cls.id == session['idInscri']", limit=1)
        spes = []
        if 'spe1' in request.form:
            spes.append(request.form['spe1'])
            spes.append(request.form['spe2'])
            if 'spe3' in request.form:
                spes.append(request.form['spe3'])
        options = list(filter(lambda opt: opt != '', [
                       request.form['option1'], request.form['option2'], request.form['option3']]))
        user.signIn2(spes, options)

        session.pop('idInscri')
        session['id'] = user['id']
        session['pseudo'] = user['pseudo']
        session['couleur'] = user['couleur']
        session['theme'] = user['theme']
        session['type'] = user['type']
        session['cacheRandomKey'] = cacheRandomKey
        return redirect(url_for('tuto'))
    else:
        session['cacheRandomKey'] = cacheRandomKey
        user = User.get(filter="cls.id == session['idInscri']", limit=1)
        return render_template('inscription2.html', user=user)


if __name__ == "__main__":
    cacheRandomKey = uuid4()

    # This allows us to use a plain HTTP callback
    app.secret_key = os.urandom(24)

    # clé de hash
    cle = 'hqZcPsAkTaMIRHco1L1BhCxXo4LWwBBBRvGcydjH0Vb85uXB3ZQ1lfmvfg7laldlaosg21Ri8uPvDgxLYyUoAPVXaQbNvpvpcvuyIv7ckVGGS6Ro5tmh8TlphoG25Z13RftlviLXggzJ4LXVJFjZ3xtUQ27zUJzQZAoI9JOAxXAV3VBdATqX'
    # Lancement de l'application, à l'adresse 127.0.0.0 et sur le port 3000
    # app.run(host="127.0.0.1", port=3000, debug=True)
    socketio.run(app, host='127.0.0.1', port=3000, debug=True)
