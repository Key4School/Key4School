from flask import Flask, render_template, request, redirect, session, url_for, abort, escape
from datetime import *
from flask.json import jsonify
from flask_socketio import emit
from bson.objectid import ObjectId
from db_poo import *
from routing.functions import listeModeration, automoderation

@db_session
def page_messages(idGroupe):
    global messages
    global groupes
    global notifications

    if 'id' in session:
        user = User.get(filter="cls.id == session['id']", limit=1)
        users = User.get(order_by="cls.pseudo")

        if idGroupe != None and idGroupe in groupes:
            for notif in [notification for notification in notifications.values() if notification.id_groupe == ObjectId(idGroupe) and notification.type == 'msg' and session['id'] in notification.destinataires]:
                notif.supprUser(session['id'])

            grp = sorted([groupe.toDict() for idGrp , groupe in groupes.items() if session['id'] in groupe.id_utilisateurs], key = lambda groupe: groupe['lastMsg']['date_envoi'] if groupe['lastMsg'] != None else datetime.min, reverse=True)

            groupe = groupes[idGroupe]
            infoUtilisateurs = groupe.toDict()['utilisateurs']
            if session['id'] in groupe.toDict()['id-utilisateurs']: # verif autorization
                msgDb = groupe.getAllMessages()
                taille = len(msgDb)
                msgDb = msgDb[taille-20:taille]

            elif user['admin'] == True:
                msgDb = groupe.getAllMessagesSign().reverse()[:20].reverse()

            else:
                msgDb = None
                groupe = None
                infoUtilisateurs = None
            groupe = groupe.toDict()

        else:
            grp = sorted([groupe.toDict() for idGrp , groupe in groupes.items() if session['id'] in groupe.id_utilisateurs], key = lambda groupe: groupe['lastMsg']['date_envoi'] if groupe['lastMsg'] != None else datetime.min, reverse=True)
            msgDb = None
            groupe = None
            infoUtilisateurs = None

        return render_template("messages.html", msgDb=msgDb, grpUtilisateur=grp, idgroupe=idGroupe, infogroupe=groupe, infoUtilisateurs=infoUtilisateurs, users=users, sessionId=session['id'], user=user)

    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

@db_session
def redirectDM(idUser1, idUser2):
    if 'id' in session:
        grp = [groupe.toDict() for groupe in groupes.values() if len(groupe.id_utilisateurs) == 2 and ObjectId(idUser1) in groupe.id_utilisateurs and ObjectId(idUser2) in groupe.id_utilisateurs]

        if grp != []: # DM existing
            return redirect('/messages/' + str(grp[0]['id']))
        else: # create DM
            participants = [ObjectId(idUser1), ObjectId(idUser2)]
            user1 = User.get(filter="cls.id == idUser1", limit=1)
            user2 = User.get(filter="cls.id == idUser2", limit=1)
            nomGrp = '[DM]: {} - {}'.format(user1['pseudo'], user2['pseudo'])

            id = ObjectId()
            groupes[str(id)] = Groupe({'id': id, 'nom': nomGrp, 'is_DM': True, 'id-utilisateurs': participants, 'moderateurs': [], 'sign':[], 'motif': []})
            groupes[str(id)].insert()

            return redirect('/messages/' + str(id))

    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

@db_session
@get_context
def uploadAudio():
    if 'id' in session:
        nom = "MsgVocal" + request.form['group'] + session['id'] + str(datetime.now())
        DB.cluster.save_file(nom, request.files['audio'])
        if request.form['reponse'] != "None":
            reponse = ObjectId(request.form['reponse'])
        else:
            reponse = "None"

        id = ObjectId()
        messages[str(id)] = Message({"id": id, "id-groupe": ObjectId(request.form['group']), "id-utilisateur": session['id'],
                    "contenu": nom, "date_envoi": datetime.now(), "audio": True, "reponse": reponse, "sign": []})
        messages[str(id)].insert()
        message = messages[str(id)].toDict()

        if message:
            groupe = message['groupe']
            users = groupe['utilisateurs']

            ownHTML = render_template("widget_message.html", content=message, sessionId=session['id'], infogroupe=groupe, infoUtilisateurs=users, idgroupe=str(groupe['id']), user=User.get(filter="cls.id == session['id']", limit=1))
            otherHTML = render_template("widget_message.html", content=message, sessionId=None, infogroupe=groupe, infoUtilisateurs=users, idgroupe=str(groupe['id']), user=User.get(filter="cls.id == session['id']", limit=1))

            socketio.emit('newMsg', {'fromUser': session['id'], 'ownHTML': ownHTML, 'otherHTML': otherHTML}, to=str(groupe['id']))
            Notification.create("msg", groupe['id'], id, list(groupe['id-utilisateurs']))
            return 'yes'
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

@db_session
def audio(audioName):
    if 'id' in session:
        return DB.cluster.send_file(audioName.strip())
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

@db_session
@get_context
def uploadImage():
    if 'id' in session:
        nom = "Image" + request.form['group'] + session['id'] + str(datetime.now())
        DB.cluster.save_file(nom, request.files['image'])
        if request.form['reponse'] != "None":
            reponse = ObjectId(request.form['reponse'])
        else:
            reponse = "None"

        id = ObjectId()
        messages[str(id)] = Message({"id": id, "id-groupe": ObjectId(request.form['group']), "id-utilisateur": session['id'],
                    "contenu": request.form['contenuMessage'], "date_envoi": datetime.now(), "image": nom, "reponse": reponse, "sign": []})
        messages[str(id)].insert()
        message = messages[str(id)].toDict()

        if message:
            groupe = message['groupe']
            users = groupe['utilisateurs']

            ownHTML = render_template("widget_message.html", content=message, sessionId=session['id'], infogroupe=groupe, infoUtilisateurs=users, idgroupe=str(groupe['id']), user=User.get(filter="cls.id == session['id']", limit=1))
            otherHTML = render_template("widget_message.html", content=message, sessionId=None, infogroupe=groupe, infoUtilisateurs=users, idgroupe=str(groupe['id']), user=User.get(filter="cls.id == session['id']", limit=1))

            socketio.emit('newMsg', {'fromUser': session['id'], 'ownHTML': ownHTML, 'otherHTML': otherHTML}, to=str(groupe['id']))
            Notification.create("msg", groupe['id'], id, list(groupe['id-utilisateurs']))
            return 'yes'
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

@db_session
def image(imageName):
    if 'id' in session:
        return DB.cluster.send_file(imageName)
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

@db_session
def createGroupe():
    global groupes

    if 'id' in session:
        participants = [session['id']]
        for name, value in request.form.items():
            if name == 'nomnewgroupe':
                pass
            else:
                participants.append(ObjectId(name))

        id = ObjectId()
        groupes[str(id)] = Groupe({'id': id, 'nom': request.form['nomnewgroupe'], 'id-utilisateurs': participants, 'moderateurs': [session['id']], 'sign':[], 'motif': []})
        groupes[str(id)].insert()

        return redirect(url_for('page_messages', idGroupe=str(id)))
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

@db_session
def updateGroupe():
    global groupes

    if 'id' in session:
        groupe = groupes[request.form['IdGroupe']]
        participants = groupe.toDict()['id-utilisateurs']

        if session['id'] in participants and session['id'] in groupe.toDict()['moderateurs']:
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

@db_session
def virerParticipant():
    global groupes

    if 'id' in session:
        groupe = groupes[request.form['idViréGrp']]
        moderateurs = groupe.toDict()['moderateurs']

        if session['id'] in moderateurs or request.form['idViré'] == session['id']:
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

@db_session
def modifRole():
    if 'id' in session:
        grp = groupes[request.form['idGrp']]
        modos = grp.toDict()['moderateurs']
        participants = grp.toDict()['id-utilisateurs']

        if session['id'] in modos and ObjectId(request.form['idModifié']) in participants:
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

@db_session
def supprGroupe(idGrp):
    user = User.get(filter="cls.id == session['id']", limit=1)
    groupe = groupes[idGrp]

    if user.admin or session['id'] in groupe.moderateurs:
        groupe.supprGroupe()
        return 'group deleted', 200
    else:
        abort(401)

@db_session
def updateGrpName(idGrp, newGrpName):
    user = User.get(filter="cls.id == session['id']", limit=1)
    groupe = groupes[idGrp]

    if user.admin or session['id'] in groupe.moderateurs:
        groupe.nom = newGrpName
        groupes[idGrp].update()

        return 'group name edited', 200
    else:
        abort(401)

@db_session
def moreMsg():
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
            html += render_template("widget_message.html", content=message, sessionId=session['id'], infogroupe=groupe, infoUtilisateurs=users, idgroupe=idgroupe, user=User.get(filter="cls.id == session['id']", limit=1))

        return {'html': html}

    else:
        abort(401) # non connecté

@db_session
def modererGrp(idGrp):
    user = User.get(filter="cls.id == session['id']", limit=1)
    groupe = groupes[idGrp]

    if user.admin or session['id'] in groupe.moderateurs:
        groupe.is_mod = not groupe.is_mod
        groupes[idGrp].update()

        return 'group moderation edited', 200
    else:
        abort(401)
