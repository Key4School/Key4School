from flask import Flask, render_template, request, redirect, session, url_for, abort, escape
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from datetime import *
from flask.json import jsonify
from bson.objectid import ObjectId
from db_poo import *
from routing.functions import listeModeration, automoderation
from routing.demandes_aide import likePost, likeRep

# Connection au groupe pour recevoir les nouvelles notif
def connectToNotif():
    if 'id' in session:
        clientsNotif[session['id']] = True
        join_room(session['id'])

        alreadySend = []
        notifs = [notif for id, notif in notifications.copy().items() if session['id'] in notif.destinataires and notif.toDict() != None]
        toSend = []
        for notif in notifs:
            if notif.id_groupe not in alreadySend:
                alreadySend.append(notif.id_groupe)
                toSend.append(notif)
        toSend.reverse()
        for notif in toSend:
            html = render_template("notification.html", notif=notif.toDict(), similar=len(notif.getSimilar(session['id'])))
            emit('notif', html, to=session['id'])

# Deconnexion au groupe pour recevoir les nouvelles notif
def disconnect():
    if 'id' in session:
        if session['id'] in clientsNotif:
            clientsNotif.pop(session['id'])
            leave_room(session['id'])

@db_session
def supprNotif(id):
    global notifications

    if 'id' in session:
        notification = notifications[id]
        for notif in notification.getSimilar(session['id']):
            notif.supprUser(session['id'])
        notification.supprUser(session['id'])

# Connection au groupe pour recevoir les nouveaux messages par la suite
@db_session
def connectToGroup(json):
    global groupes

    if 'id' in session:
        if 'room' in json:
            if json['room'] != 'None':
                # Check authorized
                grp = groupes[json['room']].toDict()
                if grp != None:
                    if session['id'] in grp['id-utilisateurs']: # authorized
                        join_room(json['room'])

@db_session
def postMsg(json):
    global messages
    global groupes

    if 'id' in session:
        if 'room' in json:
            # Check authorized
            grp = groupes[json['room']].toDict()
            if grp != None:
                if session['id'] in grp['id-utilisateurs']: # authorized
                    if json['reponse'] != "None":
                        reponse = json['reponse']
                    else:
                        reponse = "None"

                    if not json['contenuMessage'] == '':
                        id = ObjectId()
                        contenu = automoderation(json['contenuMessage']) if grp['is_mod'] else json['contenuMessage']

                        messages[str(id)] = Message({"id": id, "id-groupe": ObjectId(json['room']), "id-utilisateur": session['id'],
                                                          "contenu": contenu, "date_envoi": datetime.now(), "audio": False, "reponse": reponse, "sign": []})
                        messages[str(id)].insert()
                        message = messages[str(id)].toDict()

                    if message:
                        groupe = message['groupe']

                        users = groupe['utilisateurs']

                        ownHTML = render_template("widget_message.html", content=message, sessionId=session['id'], infogroupe=groupe, infoUtilisateurs=users, idgroupe=json['room'], user=User.get(filter="cls.id == session['id']", limit=1))
                        otherHTML = render_template("widget_message.html", content=message, sessionId=None, infogroupe=groupe, infoUtilisateurs=users, idgroupe=json['room'], user=User.get(filter="cls.id == session['id']", limit=1))

                        emit('newMsg', {'fromUser': session['id'], 'ownHTML': ownHTML, 'otherHTML': otherHTML}, to=json['room'])
                        Notification.create("msg", ObjectId(json['room']), id, list(groupe['id-utilisateurs']))


def postLike(json):
	if 'id' in session:
		if 'type' in json:
			if json['type'] == 'post':
				if 'idPost' in json:
					action = likePost(json['idPost'])
					if action == 'add':
						emit('newLike', json['idPost'], broadcast=True)
					elif action == 'remove':
						emit('removeLike', json['idPost'], broadcast=True)
			elif json['type'] == 'rep':
				if 'idPost' in json and 'idRep' in json:
					action = likeRep(json['idPost'], json['idRep'])
					if action == 'add':
						emit('newLike', json['idRep'], broadcast=True)
					elif action == 'remove':
						emit('removeLike', json['idRep'], broadcast=True)
