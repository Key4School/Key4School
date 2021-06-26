from flask import Flask, render_template, request, redirect, session, url_for, abort, escape
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from datetime import *
from flask.json import jsonify
from bson.objectid import ObjectId
from db_poo import *
from routing.functions import listeModeration, automoderation, sendNotif, clientsNotif
from routing.demandes_aide import likePost, likeRep

# Connection au groupe pour recevoir les nouvelles notif
def connectToNotif():
    if 'id' in session:
        clientsNotif[session['id']] = True
        join_room(session['id'])

        alreadySend = []
        notifs = [notif for id, notif in notifications.copy().items() if ObjectId(session['id']) in notif.destinataires and notif.toDict() != None]
        toSend = []
        for notif in notifs:
            if notif.id_groupe not in alreadySend:
                alreadySend.append(notif.id_groupe)
                toSend.append(notif)
        toSend.reverse()
        for notif in toSend:
            html = render_template("notification.html", notif=notif.toDict(), similar=len(notif.getSimilar(ObjectId(session['id']))))
            emit('notif', html, to=session['id'])

# Deconnexion au groupe pour recevoir les nouvelles notif
def disconnect():
    if 'id' in session:
        if session['id'] in clientsNotif:
            clientsNotif.pop(session['id'])
            leave_room(session['id'])

def supprNotif(id):
    global notifications

    if 'id' in session:
        notification = notifications[id]
        for notif in notification.getSimilar(ObjectId(session['id'])):
            notif.supprUser(ObjectId(session['id']))
        notification.supprUser(ObjectId(session['id']))

# Connection au groupe pour recevoir les nouveaux messages par la suite
def connectToGroup(json):
    global groupes

    if 'id' in session:
        if 'room' in json:
            if json['room'] != 'None':
                # Check authorized
                grp = groupes[json['room']].toDict()
                if grp != None:
                    if session['id'] in str(grp['id-utilisateurs']): # authorized
                        join_room(json['room'])

def postMsg(json):
    global utilisateurs
    global messages
    global groupes

    if 'id' in session:
        if 'room' in json:
            # Check authorized
            grp = groupes[json['room']].toDict()
            if grp != None:
                if ObjectId(session['id']) in grp['id-utilisateurs']: # authorized
                    if json['reponse'] != "None":
                        reponse = ObjectId(json['reponse'])
                    else:
                        reponse = "None"

                    if not json['contenuMessage'] == '':
                        _id = ObjectId()
                        contenu = automoderation(json['contenuMessage']) if grp['is_mod'] else json['contenuMessage']

                        messages[str(_id)] = Message({"_id": _id, "id-groupe": ObjectId(json['room']), "id-utilisateur": ObjectId(session['id']),
                                                          "contenu": contenu, "date-envoi": datetime.now(), "audio": False, "reponse": reponse, "sign": []})
                        messages[str(_id)].insert()
                        message = messages[str(_id)].toDict()

                    if message:
                        groupe = message['groupe']
                        sendNotif("msg", ObjectId(json['room']), _id, list(groupe['id-utilisateurs']))

                        users = groupe['utilisateurs']

                        ownHTML = render_template("widget_message.html", content=message, sessionId=ObjectId(session['id']), infogroupe=groupe, infoUtilisateurs=users, idgroupe=json['room'], user=utilisateurs[session['id']].toDict())
                        otherHTML = render_template("widget_message.html", content=message, sessionId=None, infogroupe=groupe, infoUtilisateurs=users, idgroupe=json['room'], user=utilisateurs[session['id']].toDict())

                        emit('newMsg', {'fromUser': session['id'], 'ownHTML': ownHTML, 'otherHTML': otherHTML}, to=json['room'])


def postLike(json):
	print('hey')
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
