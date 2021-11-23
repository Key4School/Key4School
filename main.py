from routing.functions import listeModeration, automoderation, afficheNotif
from routing.sockets import connectToNotif, disconnect, supprNotif, connectToGroup, postMsg, postLike
from routing.demandes_aide import question, redirect_comments, comments, updateDemand, updateComment, file, DL_file, likePost, likeRep, resoudre, savePost
from routing.profil import profil, changeTheme, theme, updateprofile, userImg, updateImg, otherSubject
from routing.administration import administration, suppressionMsg, validerMsg, sanction, signPost, signRepPost, signPostProfil, signPostDiscussion, signPostMsg
from routing.messages import page_messages, redirectDM, uploadAudio, audio, uploadImage, image, createGroupe, updateGroupe, virerParticipant, modifRole, supprGroupe, updateGrpName, moreMsg, modererGrp
from routing.recherche import recherche, recherche_user, morePost, moreUser
from routing.accueil import accueil, accueil2, tuto, XP_tuto, mail_rendu, saved, about
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

# DB POO

# Routing

'''A TRIER PAR CATEGORIES'''
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
app.add_url_rule('/createGroupe/', 'createGroupe',createGroupe, methods=['POST'])
app.add_url_rule('/updateGroupe/', 'updateGroupe', updateGroupe, methods=['POST'])
app.add_url_rule('/virerParticipant/', 'virerParticipant', virerParticipant, methods=['POST'])
app.add_url_rule('/modifRole/', 'modifRole', modifRole, methods=['POST'])
app.add_url_rule('/supprGroupe/<idGrp>/', 'supprGroupe', supprGroupe, methods=['POST'])
app.add_url_rule('/updateGrpName/<idGrp>/<newGrpName>/', 'updateGrpName', updateGrpName, methods=['POST'])
app.add_url_rule('/changeTheme/', 'changeTheme', changeTheme, methods=['POST'])
app.add_url_rule('/theme/', 'theme', theme, methods=['POST'])
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
app.add_url_rule('/likeRep/<idRep>/', 'likeRep', likeRep, methods=['POST'])
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
app.add_url_rule('/about/', 'about', about)

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
    cle = 'hqZcPsAkTaMIRHco1L1BhCxXo4LWwBBBRvGcydjH0Vb85uXB3ZQ1lfmvfg7laldlaosg21Ri8uPvDgxLYyUoAPVXaQbNvpvpcvuyIv7ckVGGS6Ro5tmh8TlphoG25Z13RftlviLXggzJ4LXVJFjZ3xtUQ27zUJzQZAoI9JOAxXAV3VBdATqX'
    # Lancement de l'application, à l'adresse 127.0.0.0 et sur le port 3000
    # app.run(host="127.0.0.1", port=3000, debug=True)
    socketio.run(app, host='127.0.0.1', port=3000, debug=True)
