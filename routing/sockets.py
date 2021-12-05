from flask import Flask, current_app as app, render_template, request, redirect, session, url_for, abort, escape
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from datetime import *
from flask.json import jsonify
from db_poo import *
from routing.functions import listeModeration, automoderation
from routing.demandes_aide import likePost, likeRep

# Connection au groupe pour recevoir les nouvelles notif


def connectToNotif():
    if 'id' in session:
        clientsNotif[session['id']] = True
        join_room(session['id'])

        alreadySend = []
        notifs = Notification.get(
            filter="cls.destinataires.comparator.has_key(str(session['id']))")
        toSend = []
        for notif in notifs:
            if notif.id_groupe not in alreadySend:
                alreadySend.append(notif.id_groupe)
                toSend.append(notif)
        toSend.reverse()
        for notif in toSend:
            html = render_template("notification.html", notif=notif, similar=len(
                notif.getSimilar(session['id'])))
            emit('notif', html, to=session['id'])

# Deconnexion au groupe pour recevoir les nouvelles notif


def disconnect():
    if 'id' in session:
        if session['id'] in clientsNotif:
            clientsNotif.pop(session['id'])
            leave_room(session['id'])


@db_session
def supprNotif(id):
    if 'id' in session:
        notification = Notification.get(filter="cls.id == id", limit=1)
        for notif in notification.getSimilar(session['id']):
            notif.supprUser(session['id'])
        notification.supprUser(session['id'])

# Connection au groupe pour recevoir les nouveaux messages par la suite


@db_session
def connectToGroup(json):
    if 'id' in session:
        if 'room' in json:
            if json['room'] != 'None':
                # Check authorized
                grp = Group.get(filter="cls.id == json['room']", limit=1)
                if grp != None:
                    if session['id'] in grp['id_utilisateurs']:  # authorized
                        join_room(json['room'])


@db_session
def postMsg(json):
    if 'id' in session:
        if 'room' in json:
            # Check authorized
            grp = Group.get(filter="cls.id == json['room']", limit=1)
            if grp != None:
                if session['id'] in grp['id_utilisateurs']:  # authorized
                    if json['reponse'] != "None":
                        reponse = json['reponse']
                    else:
                        reponse = None

                    if not json['contenuMessage'] == '':
                        contenu = automoderation(
                            json['contenuMessage']) if grp['is_mod'] else json['contenuMessage']

                        message = Message(
                            id_groupe=json['room'], id_utilisateur=session['id'], contenu=contenu, reponse=reponse)
                        message.insert()

                    if message:
                        groupe = message['groupe']

                        users = groupe['utilisateurs']
                        ownHTML = render_template("widget_message.html", content=message, sessionId=session['id'], infogroupe=groupe, infoUtilisateurs=users, idgroupe=json['room'], user=User.get(
                            filter="cls.id == session['id']", limit=1))
                        otherHTML = render_template("widget_message.html", content=message, sessionId=None, infogroupe=groupe,
                                                    infoUtilisateurs=users, idgroupe=json['room'], user=User.get(filter="cls.id == session['id']", limit=1))

                        emit('newMsg', {
                             'fromUser': session['id'], 'ownHTML': ownHTML, 'otherHTML': otherHTML}, to=json['room'])
                        Notification.create("msg", json['room'], message['id'], list(
                            groupe['id_utilisateurs']))


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
                    action = likeRep(json['idRep'])
                    if action == 'add':
                        emit('newLike', json['idRep'], broadcast=True)
                    elif action == 'remove':
                        emit('removeLike', json['idRep'], broadcast=True)
