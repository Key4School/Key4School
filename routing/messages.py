from flask import Flask, render_template, request, redirect, session, url_for, abort, escape
from datetime import *
from flask.json import jsonify
from flask_socketio import emit
from bson.objectid import ObjectId
from db_poo import *
from routing.functions import listeModeration, automoderation, sendNotif, clientsNotif
from __main__ import socketio

def page_messages(idGroupe):
    global utilisateurs
    global messages
    global groupes
    global notifications

    if 'id' in session:
        grp = sorted([groupe.toDict() for idGrp , groupe in groupes.items() if ObjectId(session['id']) in groupe.id_utilisateurs], key = lambda groupe: groupe['lastMsg']['date-envoi'] if groupe['lastMsg'] != None else datetime.min, reverse=True)
        user = utilisateurs[session['id']].toDict()
        users = sorted([u.toDict() for u in utilisateurs.values()], key = lambda u: u['pseudo'])

        if idGroupe != None:
            groupe = groupes[idGroupe]
            infoUtilisateurs = groupe.toDict()['utilisateurs']
            if ObjectId(session['id']) in groupe.toDict()['id-utilisateurs']: # verif autorization
                msgDb = groupe.getAllMessages()
                taille = len(msgDb)
                msgDb = msgDb[taille-10:taille]

            elif user['admin'] == True:
                msgDb = groupe.getAllMessagesSign().reverse()[:10].reverse()

            else:
                msgDb = None
                groupe = None
                infoUtilisateurs = None
            groupe = groupe.toDict()

            for notif in [notification for notification in notifications.values() if notification.id_groupe == ObjectId(idGroupe) and notification.type == 'msg' and ObjectId(session['id']) in notification.destinataires]:
                notif.supprUser(ObjectId(session['id']))

        else:
            msgDb = None
            groupe = None
            infoUtilisateurs = None

        return render_template("messages.html", msgDb=msgDb, grpUtilisateur=grp, idgroupe=idGroupe, infogroupe=groupe, infoUtilisateurs=infoUtilisateurs, users=users, sessionId=ObjectId(session['id']), user=user)

    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

def redirectDM(idUser1, idUser2):
    if 'id' in session:
        grp = [groupe.toDict() for groupe in groupes.values() if len(groupe.id_utilisateurs) == 2 and ObjectId(idUser1) in groupe.id_utilisateurs and ObjectId(idUser2) in groupe.id_utilisateurs]

        if grp != []: # DM existing
            return redirect('/messages/' + str(grp[0]['_id']))
        else: # create DM
            participants = [ObjectId(idUser1), ObjectId(idUser2)]
            user1 = utilisateurs[idUser1].toDict()
            user2 = utilisateurs[idUser2].toDict()
            nomGrp = '[DM]: {} - {}'.format(user1['pseudo'], user2['pseudo'])

            _id = ObjectId()
            groupes[str(_id)] = Groupe({'_id': _id, 'nom': nomGrp, 'is_DM': True, 'id-utilisateurs': participants, 'moderateurs': [], 'sign':[], 'motif': []})
            groupes[str(_id)].insert()

            return redirect('/messages/' + str(_id))

    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

def uploadAudio():
    if 'id' in session:
        nom = "MsgVocal" + request.form['group'] + session['id'] + str(datetime.now())
        DB.cluster.save_file(nom, request.files['audio'])
        if request.form['reponse'] != "None":
            reponse = ObjectId(request.form['reponse'])
        else:
            reponse = "None"

        _id = ObjectId()
        messages[str(_id)] = Message({"_id": _id, "id-groupe": ObjectId(request.form['group']), "id-utilisateur": ObjectId(session['id']),
                    "contenu": nom, "date-envoi": datetime.now(), "audio": True, "reponse": reponse, "sign": []})
        messages[str(_id)].insert()
        message = messages[str(_id)].toDict()

        if message:
            groupe = message['groupe']
            sendNotif("msg", groupe['_id'], _id, list(groupe['id-utilisateurs']))
            users = groupe['utilisateurs']

        ownHTML = render_template("widget_message.html", content=message, sessionId=ObjectId(session['id']), infogroupe=groupe, infoUtilisateurs=users, idgroupe=str(groupe['_id']), user=utilisateurs[session['id']].toDict())
        otherHTML = render_template("widget_message.html", content=message, sessionId=None, infogroupe=groupe, infoUtilisateurs=users, idgroupe=str(groupe['_id']), user=utilisateurs[session['id']].toDict())

        socketio.emit('newMsg', {'fromUser': session['id'], 'ownHTML': ownHTML, 'otherHTML': otherHTML}, to=str(groupe['_id']))

        return 'yes'
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

def audio(audioName):
    if 'id' in session:
        return DB.cluster.send_file(audioName.strip())
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

def uploadImage():
    if 'id' in session:
        nom = "Image" + request.form['group'] + session['id'] + str(datetime.now())
        DB.cluster.save_file(nom, request.files['image'])
        if request.form['reponse'] != "None":
            reponse = ObjectId(request.form['reponse'])
        else:
            reponse = "None"

        _id = ObjectId()
        messages[str(_id)] = Message({"_id": _id, "id-groupe": ObjectId(request.form['group']), "id-utilisateur": ObjectId(session['id']),
                    "contenu": request.form['contenuMessage'], "date-envoi": datetime.now(), "image": nom, "reponse": reponse, "sign": []})
        messages[str(_id)].insert()
        message = messages[str(_id)].toDict()

        if message:
            groupe = message['groupe']
            sendNotif("msg", groupe['_id'], _id, list(groupe['id-utilisateurs']))
            users = groupe['utilisateurs']

        ownHTML = render_template("widget_message.html", content=message, sessionId=ObjectId(session['id']), infogroupe=groupe, infoUtilisateurs=users, idgroupe=str(groupe['_id']), user=utilisateurs[session['id']].toDict())
        otherHTML = render_template("widget_message.html", content=message, sessionId=None, infogroupe=groupe, infoUtilisateurs=users, idgroupe=str(groupe['_id']), user=utilisateurs[session['id']].toDict())

        socketio.emit('newMsg', {'fromUser': session['id'], 'ownHTML': ownHTML, 'otherHTML': otherHTML}, to=str(groupe['_id']))

        return 'yes'
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

def image(imageName):
    if 'id' in session:
        return DB.cluster.send_file(imageName)
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

def createGroupe():
    global groupes

    if 'id' in session:
        participants = [ObjectId(session['id'])]
        for name, value in request.form.items():
            if name == 'nomnewgroupe':
                pass
            else:
                participants.append(ObjectId(name))

        _id = ObjectId()
        groupes[str(_id)] = Groupe({'_id': _id, 'nom': request.form['nomnewgroupe'], 'id-utilisateurs': participants, 'moderateurs': [ObjectId(session['id'])], 'sign':[], 'motif': []})
        groupes[str(_id)].insert()

        return redirect(url_for('page_messages', idGroupe=str(_id)))
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

def updateGroupe():
    global groupes

    if 'id' in session:
        groupe = groupes[request.form['IdGroupe']]
        participants = groupe.toDict()['id-utilisateurs']

        if ObjectId(session['id']) in participants and ObjectId(session['id']) in groupe.toDict()['moderateurs']:
            for name, value in request.form.items():
                if name == 'IdGroupe':
                    pass
                else:
                    participants.append(ObjectId(name))
            groupe.id_utilisateurs = participants
            groupe.update()

        return redirect(url_for('page_messages', idGroupe=request.form['IdGroupe']))
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

def virerParticipant():
    global utilisateurs
    global groupes

    if 'id' in session:
        groupe = groupes[request.form['idViréGrp']]
        moderateurs = groupe.toDict()['moderateurs']
        user = utilisateurs[session['id']]

        if ObjectId(session['id']) in moderateurs or request.form['idViré'] == session['id']:
            groupe.supprUser(ObjectId(request.form['idViré']))

            if request.form['idViré'] == session['id']:
                return 'reload msg'
            else:
                return 'reload grp'
        else:
            return redirect(url_for('page_messages'))
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

def modifRole():
    if 'id' in session:
        grp = groupes[request.form['idGrp']]
        modos = grp.toDict()['moderateurs']
        participants = grp.toDict()['id-utilisateurs']

        if ObjectId(session['id']) in modos and ObjectId(request.form['idModifié']) in participants:
            if ObjectId(request.form['idModifié']) in modos:
                modos.remove(ObjectId(request.form['idModifié']))
                grp.moderateurs = modos
                grp.update()

                return 'participant'

            else:
                modos.append(ObjectId(request.form['idModifié']))
                grp.moderateurs = modos
                grp.update()

                return 'admin'
        else:
            abort(401) # non autorisé
    else:
        abort(403) # doit se connecter

def supprGroupe(idGrp):
    user = utilisateurs[session['id']]
    groupe = groupes[idGrp]

    if user.admin or ObjectId(session['id']) in groupe.moderateurs:
        groupe.supprGroupe()
        return 'group deleted', 200
    else:
        abort(401)

def updateGrpName(idGrp, newGrpName):
    user = utilisateurs[session['id']]
    groupe = groupes[idGrp]

    if user.admin or ObjectId(session['id']) in groupe.moderateurs:
        groupe.nom = newGrpName
        groupes[idGrp].update()

        return 'group name edited', 200
    else:
        abort(401)


def moreMsg():
    global utilisateurs
    global groupes

    if 'id' in session:
        idgroupe = request.form['idGroupe']
        lastMsg = int(request.form['lastMsg'])
        grp = groupes[idgroupe]
        groupe = grp.toDict()
        users = groupe['utilisateurs']

        messages = grp.getAllMessages()
        messages.reverse()
        messages = messages[lastMsg:lastMsg+10]
        messages.reverse()

        html = ''
        for message in messages:
            html += render_template("widget_message.html", content=message, sessionId=ObjectId(session['id']), infogroupe=groupe, infoUtilisateurs=users, idgroupe=idgroupe, user=utilisateurs[session['id']].toDict())

        return {'html': html}

    else:
        abort(401) # non connecté

def modererGrp(idGrp):
    user = utilisateurs[session['id']]
    groupe = groupes[idGrp]

    if user.admin or ObjectId(session['id']) in groupe.moderateurs:
        groupe.is_mod = not groupe.is_mod
        groupes[idGrp].update()

        return 'group moderation edited', 200
    else:
        abort(401)

