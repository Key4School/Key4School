from flask import Flask, render_template, request, redirect, session, url_for, abort, escape
from datetime import *
from flask.json import jsonify
from bson.objectid import ObjectId
from db_poo import *
from routing.functions import recupLevel, addXP, addXpModeration, listeModeration, automoderation, sendNotif, clientsNotif

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

            elif user['admin'] == True:
                msgDb = groupe.getAllMessagesSign()

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

def uploadAudio():
    if 'id' in session:
        nom = "MsgVocal" + request.form['group'] + session['id'] + request.form['date']
        DB.cluster.save_file(nom, request.files['audio'])
        return 'yes'
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

def audio(audioName):
    if 'id' in session:
        return DB.cluster.send_file(audioName)
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

        if ObjectId(session['id']) in moderateurs or request.form['idViré'] == session['id']:
            groupe.supprUser(ObjectId(request.form['idViré']))

            if request.form['idViré'] == session['id']:
                return redirect(url_for('page_messages'))
            else:
                return redirect(url_for('page_messages', idGroupe=request.form['idViréGrp']))
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
