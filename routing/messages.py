from flask import Flask, render_template, request, redirect, session, url_for, abort, escape, send_file
from datetime import *
from flask.json import jsonify
from flask_socketio import emit
from db_poo import *
from routing.functions import listeModeration, automoderation


@db_session
def page_messages(idGroupe):

    if 'id' in session:
        user = User.get(filter="cls.id == session['id']", limit=1)
        users = User.get(order_by="cls.pseudo")

        groupe = Group.get(filter="cls.id == idGroupe", limit=1)
        grp = sorted(Group.get(filter="cls.id_utilisateurs.comparator.has_key(session['id'])"), key=lambda groupe: groupe[
                     'lastMsg']['date_envoi'] if groupe['lastMsg'] else datetime.min, reverse=True)
        if idGroupe != None and groupe:
            for notif in groupe['notifs']:
                notif.supprUser(session['id'])

            infoUtilisateurs = groupe['utilisateurs']
            if session['id'] in groupe['id_utilisateurs']:  # verif autorization
                '''A REFAIRE PAS OPTI'''
                msgDb = groupe['getAllMessages']
                taille = len(msgDb)
                msgDb = msgDb[taille-20:taille]

            elif user['admin'] == True:
                msgDb = groupe['getAllMessagesSign']
                msgDb.reverse()
                msgDb = msgDb[:20]
                msgDb.reverse()

            else:
                msgDb = None
                groupe = None
                infoUtilisateurs = None

        else:
            msgDb = None
            groupe = None
            infoUtilisateurs = None

        return render_template("messages.html", msgDb=msgDb, grpUtilisateur=grp, idgroupe=idGroupe, infogroupe=groupe, infoUtilisateurs=infoUtilisateurs, users=users, user=user)

    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))


@db_session
def redirectDM(idUser1, idUser2):
    if 'id' in session:
        grp = Group.get(
            filter="(cls.is_DM == True) & (cls.id_utilisateurs.comparator.has_key(idUser1)) & (cls.id_utilisateurs.comparator.has_key(idUser2))", limit=1)

        if grp:  # DM existing
            return redirect(url_for('page_messages', idGroupe=grp['id']))
        else:  # create DM
            participants = [idUser1, idUser2]
            user1 = User.get(filter="cls.id == idUser1", limit=1)
            user2 = User.get(filter="cls.id == idUser2", limit=1)
            nomGrp = '[DM]: {} - {}'.format(user1['pseudo'], user2['pseudo'])

            groupe = Group(nom=nomGrp, is_DM=True,
                           id_utilisateurs=participants)
            groupe.insert()

            return redirect(url_for('page_messages', idGroupe=groupe['id']))

    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))


@db_session
@get_context # pour socket
def uploadAudio():
    if 'id' in session:
        file = FileUploader(request.files['audio'])
        if file.verif('audio'):
            file.save()
        else:
            idFile = None
        idFile = file['id']

        if request.form['reponse'] != "None":
            reponse = request.form['reponse']
        else:
            reponse = None

        message = Message(
            id_groupe=request.form['group'], id_utilisateur=session['id'], contenu='', audio=idFile, reponse=reponse)
        message.insert()

        if message:
            groupe = message['groupe']
            users = groupe['utilisateurs']

            ownHTML = render_template("widget_message.html", content=message, sessionId=session['id'], infogroupe=groupe, infoUtilisateurs=users, idgroupe=groupe['id'], user=User.get(
                filter="cls.id == session['id']", limit=1))
            otherHTML = render_template("widget_message.html", content=message, sessionId=None, infogroupe=groupe,
                                        infoUtilisateurs=users, idgroupe=groupe['id'], user=User.get(filter="cls.id == session['id']", limit=1))

            socketio.emit('newMsg', {
                          'fromUser': session['id'], 'ownHTML': ownHTML, 'otherHTML': otherHTML}, to=groupe['id'])
            Notification.create("msg", groupe['id'], message['id'], list(
                groupe['id_utilisateurs']))
            return 'yes'
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))


@db_session
def audio(audioId):
    if 'id' in session:
        file = File.get(audioId)
        if not file:
            return abort(404)
        return send_file(file['path'], mimetype='audio/ogg', attachment_filename=f"audio.{file['ext']}")
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))


@db_session
@get_context # pour socket
def uploadImage():
    if 'id' in session:
        file = FileUploader(request.files['image'])
        if file.verif('image'):
            file.save()
            idFile = file['id']
        else:
            idFile = None

        if request.form['reponse'] != "None":
            reponse = request.form['reponse']
        else:
            reponse = None

        message = Message(id_groupe=request.form['group'], id_utilisateur=session['id'],
                          contenu=request.form['contenuMessage'], image=idFile, reponse=reponse)
        message.insert()

        if message:
            groupe = message['groupe']
            users = groupe['utilisateurs']

            ownHTML = render_template("widget_message.html", content=message, sessionId=session['id'], infogroupe=groupe, infoUtilisateurs=users, idgroupe=groupe['id'], user=User.get(
                filter="cls.id == session['id']", limit=1))
            otherHTML = render_template("widget_message.html", content=message, sessionId=None, infogroupe=groupe,
                                        infoUtilisateurs=users, idgroupe=groupe['id'], user=User.get(filter="cls.id == session['id']", limit=1))

            socketio.emit('newMsg', {
                          'fromUser': session['id'], 'ownHTML': ownHTML, 'otherHTML': otherHTML}, to=groupe['id'])
            Notification.create("msg", groupe['id'], message['id'], list(
                groupe['id_utilisateurs']))
            return 'yes'
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))


@db_session
def image(imageId):
    if 'id' in session:
        file = File.get(imageId)
        if not file:
            return abort(404)
        return send_file(file['path'], mimetype=file['mimetype'], attachment_filename=f"attachment.{file['ext']}")
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))


@db_session
def createGroupe():
    if 'id' in session:
        participants = [session['id']]
        for name, value in request.form.items():
            if name == 'nomnewgroupe':
                continue
            else:
                participants.append(name)

        if not request.form['nomnewgroupe'] and len(participants) > 1:
            return redirect(url_for('redirectDM', idUser1=participants[0], idUser2=participants[1]))

        groupe = Group(
            nom=request.form['nomnewgroupe'], id_utilisateurs=participants)
        groupe.insert()

        return redirect(url_for('page_messages', idGroupe=groupe['id']))
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))


@db_session
def updateGroupe():
    if 'id' in session:
        groupe = Group.get(
            filter="cls.id == request.form['IdGroupe']", limit=1)
        participants = groupe['id_utilisateurs'].copy()

        if session['id'] in participants and session['id'] in groupe['moderateurs']:
            for name, value in request.form.items():
                if name == 'IdGroupe':
                    pass
                else:
                    participants.append(name)
            groupe['id_utilisateurs'] = participants
            groupe.update()

        return redirect(url_for('page_messages', idGroupe=groupe['id']))
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))


@db_session
def virerParticipant():
    if 'id' in session:
        groupe = Group.get(
            filter="cls.id == request.form['idViréGrp']", limit=1)
        moderateurs = groupe['moderateurs']

        if session['id'] in moderateurs or request.form['idViré'] == session['id']:
            groupe.supprUser(request.form['idViré'])

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
        grp = Group.get(filter="cls.id == request.form['idGrp']", limit=1)
        modos = grp['moderateurs'].copy()
        participants = grp['id_utilisateurs'].copy()

        if session['id'] in modos and request.form['idModifié'] in participants:
            if request.form['idModifié'] in modos:
                modos.remove(request.form['idModifié'])
                grp['moderateurs'] = modos
                grp.update()

                return 'participant'
            else:
                modos.append(request.form['idModifié'])
                grp['moderateurs'] = modos
                grp.update()

                return 'admin'
        else:
            abort(401)  # non autorisé
    else:
        abort(403)  # doit se connecter


@db_session
def supprGroupe(idGrp):
    user = User.get(filter="cls.id == session['id']", limit=1)
    groupe = Group.get(filter="cls.id == idGrp", limit=1)

    if user['admin'] or session['id'] in groupe['moderateurs']:
        groupe.supprGroupe()
        return 'group deleted', 200
    else:
        abort(401)


@db_session
def updateGrpName(idGrp, newGrpName):
    user = User.get(filter="cls.id == session['id']", limit=1)
    groupe = Group.get(filter="cls.id == idGrp", limit=1)

    if user['admin'] or session['id'] in groupe['moderateurs']:
        groupe['nom'] = newGrpName
        groupe.update()

        return 'group name edited', 200
    else:
        abort(401)


@db_session
def moreMsg():

    if 'id' in session:
        lastMsg = int(request.form['lastMsg'])
        groupe = Group.get(
            filter="cls.id == request.form['idGroupe']", limit=1)
        users = groupe['utilisateurs']

        '''A REFAIRE PAS OPTI'''
        messages = groupe['getAllMessages']
        messages.reverse()
        messages = messages[lastMsg:lastMsg+10]
        messages.reverse()

        html = ''
        for message in messages:
            html += render_template("widget_message.html", content=message, sessionId=session['id'], infogroupe=groupe,
                                    infoUtilisateurs=users, idgroupe=request.form['idGroupe'], user=User.get(filter="cls.id == session['id']", limit=1))

        return {'html': html}

    else:
        abort(401)  # non connecté


@db_session
def modererGrp(idGrp):
    user = User.get(filter="cls.id == session['id']", limit=1)
    groupe = Group.get(filter="cls.id == idGrp", limit=1)

    if user['admin'] or session['id'] in groupe['moderateurs']:
        groupe['is_mod'] = not groupe['is_mod']
        groupe.update()

        return 'group moderation edited', 200
    else:
        abort(401)
