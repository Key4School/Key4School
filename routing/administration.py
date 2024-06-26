from flask import Flask, current_app as app, render_template, request, redirect, session, url_for, abort, escape
from datetime import *
from flask.json import jsonify
from db_poo import *
from routing.functions import listeModeration, automoderation

@db_session
@login_required(admin=True)
def administration():
    utilisateur = User.get(filter="cls.id == session['id']", limit=1)
    if request.method == 'POST':
        if request.form['demandeBut'] == 'Suppr':
            auteur = User.get(filter="cls.id == Request.get(filter=\"cls.id == request.form['idSuppr']\", limit=1)['id_utilisateur']", limit=1)
            sanction = auteur['Sanctions']
            Request.get(filter="cls.id == request.form['idSuppr']", limit=1).suppr()
            auteur.addXP(-10)
            auteur.addXpModeration(10)
            sanction.append({"SanctionType": "Demandes d'aide supprimée", "SanctionMotif": request.form['motif'], "SanctionNext": 'Aucune', "dateSanction" : datetime.now()})
            auteur.update()

        elif request.form['demandeBut'] == 'Val':
            demande = Request.get(filter="cls.id == request.form['idVal']", limit=1)
            sign = demande['sign']
            if request.form['motif'] == "abusif":
                for content in sign:
                    if "/" not in str(content):
                        user = User.get(filter="cls.id == content", limit=1)
                        user.addXpModeration(5)
                        sanction = user['Sanctions']
                        sanction.append({"SanctionType": "Demandes d'aide supprimée", "SanctionMotif": 'Signalement abusif', "SanctionNext": 'Aucune', "dateSanction" : datetime.now()})
                        user.update()
            motif = demande.motif
            for i in range (len(sign)):
                if "/" not in str(sign[i]):
                    del sign[i]
            for a in range (len(motif)):
                if "/" not in str(motif[a]):
                    del motif[a]

            demande.update()

        elif request.form['demandeBut'] == 'ValUser':
            user = User.get(filter="cls.id == request.form['idValidé']", limit=1)
            if request.form['motif'] == "abusif":
                for content in user.sign:
                    userSanction = User.get(filter="cls.id == content", limit=1)
                    userSanction.addXpModeration(5)
                    sanction = userSanction['Sanctions']
                    sanction.append({"SanctionType": "Aucune", "SanctionMotif": 'Signalement abusif', "SanctionNext": 'Aucune', "dateSanction" : datetime.now()})
                    userSanction.update()
            user.sign = []
            user.motif = []
            user.update()

        elif request.form['demandeBut'] == 'SupprRep':
            demande = Request.get(filter="cls.id == request.form['idDemandSuppr']", limit=1)
            reponse = Response.get(filter="cls.id == [request.form['idSuppr']", limit=1)
            auteur = User.get(filter="cls.id == reponse['id_utilisateur']", limit=1)
            auteur.addXpModeration(5)
            auteur.addXP(-15)
            sanction = auteur['Sanctions']
            sanction.append({"SanctionType": "Réponse supprimée", "SanctionMotif": request.form['motif'], "SanctionNext": 'Aucune', "dateSanction" : datetime.now()})
            auteur.update()

            reponse.delete()
            signDemande = demande['sign']
            motifDemande = demande['motif']

            for i in range (len(signDemande)):
                if str(request.form['idSuppr']+"/") in str(signDemande[i]):
                    del signDemande[i]
            for a in range (len(motifDemande)):
                if str(request.form['idSuppr']+"/") in str(motifDemande[a]):
                    del motifDemande[a]
            demande.update()

        elif request.form['demandeBut'] == 'ValRep':
            demande = Request.get(filter="cls.id == request.form['idDemandVal']", limit=1)
            reponse = Response.get(filter="cls.id == [request.form['idVal']", limit=1)
            signDemande = demande.sign
            motifDemande = demande.motif
            sign =  reponse['sign']
            print ('sign')
            if request.form['motif'] == "abusif":
                for content in sign :
                    userSanction = User.get(filter="cls.id == content", limit=1)
                    sanction = userSanction['Sanctions']
                    userSanction.addXpModeration(5)
                    sanction.append({"SanctionType": "Aucune", "SanctionMotif": 'Signalement abusif', "SanctionNext": 'Aucune', "dateSanction" : datetime.now()})
            reponse['sign'].clear()
            reponse['motif'].clear()
            for i in range(len(signDemande)):
                if str(request.form['idVal']+"/") in str(signDemande[i]):
                    del signDemande[i]
            for a in range(len(motifDemande)):
                if str(request.form['idVal']+"/") in str(motifDemande[a]):
                    del motifDemande[a]
            demande.update()
            reponse.update()

        elif request.form['demandeBut'] == 'supprDisc':
            groupe = Group.get(filter="cls.id == request.form['idDiscSuppr']", limit=1)
            sign = groupe['sign']
            motif = groupe['motif']
            for auteur in groupe['id_utilisateurs'] :
                User.get(filter="cls.id == content", limit=1).addXpModeration(10)

            sign.clear()
            motif.clear()
            grpMsg = Message.get(filter="cls.id_groupe == request.form['idDiscSuppr']")
            for m in grpMsg:
                m.suppr()

            groupe.update()

        elif request.form['demandeBut'] == 'valDisc':
            groupe = Group.get(filter="cls.id == request.form['idDiscVal']", limit=1)
            sign = groupe['sign']
            motif = groupe['motif']
            if request.form['motif'] == "abusif":
                for content in sign:
                        User.get(filter="cls.id == content", limit=1).addXpModeration(5)
            # on supprime son signalement
            sign.clear()
            motif.clear()

            grpMsg = Message.get(filter="cls.id_groupe == request.form['idDiscVal']")
            for m in grpMsg:
                m['motif'].clear()
                m['sign'].clear()
                m.update()
            groupe.update()

        return 'sent'

    else:
        demandeSignale = sorted(Request.get(filter="cls.sign != '[]'"), key = lambda d: len(d['sign']), reverse=True)
        profilSignale = User.get(filter="cls.sign != []", order_by="func.jsonb_array_length(cls.sign)", desc=True)
        discussionSignale = sorted(Group.get(filter="cls.sign != '[]'"), key = lambda g: len(g['sign']), reverse=True)
        return render_template('administration.html', user=utilisateur, demandeSignale=demandeSignale, profilSignale=profilSignale, discussionSignale=discussionSignale)


@db_session
@login_required(endpoint='page_messages')
def suppressionMsg():
    user = User.get(filter="cls.id == session['id']", limit=1)
    msg = Message.get(filter="cls.id == request.form['msgSuppr']", limit=1)
    groupe = Group.get(filter="cls.id == request.form['grp']", limit=1)
    sign = groupe['sign']
    motif = groupe['motif']
    if user['admin'] or user['type'] == "ENSEIGNANT" or msg['id_utilisateur'] == session['id'] or session['id'] in groupe['moderateurs']:
        if msg['sign'] != []:
            sign.remove(request.form['msgSuppr'])
            index = next((i for i, item in enumerate(motif) if item['id'] == request.form['msgSuppr']), -1)
            del motif[index]
        msg.suppr()
        groupe['sign'] = sign
        groupe['motif'] = motif
        groupe.update()

    return redirect(url_for('page_messages', idGroupe=request.form['grp']))


@db_session
@login_required(endpoint='page_messages')
def validerMsg():
    user = User.get(filter="cls.id == session['id']", limit=1)
    idGroupe = request.form['grp']

    if user['admin']:
        message = Message.get(filter="cls.id == request.form['msgVal']", limit=1)
        signMsg = message['sign']
        motifMsg = message['motif']
        signMsg.clear()
        motifMsg.clear()
        groupe = Group.get(filter="cls.id == request.form['grp']", limit=1)
        sign = groupe['sign']
        motif = groupe['motif']
        sign.remove(request.form['msgVal'])
        index = next((i for i, item in enumerate(motif) if item['id'] == request.form['msgVal']), -1)
        del motif[index]

        groupe['sign'] = sign
        groupe['motif'] = motif

        groupe.update()
        message.update()

    return redirect(url_for('page_messages', idGroupe=idGroupe))


@db_session
@login_required(admin=True)
def sanction():
    userSanction = User.get(filter="cls.id == request.form['idSanctionné']", limit=1)
    sanctions = userSanction['Sanctions']

    sanctions.append({"SanctionType": request.form['Sanction'], "SanctionMotif": request.form['Raison'], "SanctionNext": request.form['Next'], "dateSanction" : datetime.now()})

    time = datetime.now() + timedelta(days= int(request.form['SanctionDuree']))

    if request.form['SanctionType'] == 'Spec' or request.form['SanctionType'] == 'SpecProfil' or request.form['SanctionType'] == 'SpecForum' or request.form['SanctionType'] == 'SpecMsg':
        userSanction['SanctionEnCour'] = request.form['SanctionType']
        userSanction['SanctionDuree'] = time
        userSanction.addXpModeration(50)

    elif request.form['SanctionType'] == 'ResetProfil':
        userSanction.addXpModeration(25)
        oldFile = File.get(user['idImg'])
        oldFile.delete()

        userSanction['idMsg'] = None
        userSanction['pseudo'] = '{}_{}'.format(user.nom, user.prenom)
        userSanction['telephone'] = ''
        userSanction['interets'] = ''

    userSanction.update()

    return 'sent'


@db_session
@login_required()
def signPost():
    if not request.form.get('idSignalé'):
        abort(400) # il manque l'id du message

    # on récupère les signalements de la demande d'aide
    demande = Request.get(filter="cls.id == request.form['idSignalé']", limit=1)
    sign = demande['sign']
    motif = demande['motif']

    # on check mtn si l'utilisateur a déjà signalé la demande
    if session['id'] in sign:
        # on supprime son signalement
        sign.remove(session['id'])
        index = next((i for i, item in enumerate(motif) if item['id'] == session['id']), -1)
        del motif[index]

    else:
        # on ajoute son signalement
        sign.append(session['id']) # on ajoute son signalement
        motif.append({'id': session['id'], 'txt': request.form['Raison']})

    demande.update()

    return 'sent'


@db_session
@login_required()
def signRepPost():
    if not request.form.get('idSignalé') and not request.form.get('idDemandSignalé'):
        abort(400) # il manque l'id du message

    # on récupère les signalements de la demande d'aide
    demande = Request.get(filter="cls.id == request.form['idDemandSignalé']", limit=1)
    reponse = Response.get(filter="cls.id == request.form['idSignalé']", limit=1)
    sign = reponse['sign']
    motif = reponse['motif']
    signDemand = demande['sign']
    motifDemand = demande['motif']

    if session['id'] in sign:
        # on supprime son signalement
        sign.remove(session['id'])
        index = next((i for i, item in enumerate(motif) if item['id'] == session['id']), -1)
        del motif[index]
        signDemand.remove(request.form['idSignalé']+"/"+session['id'])
        index = next((i for i, item in enumerate(motifDemand) if item['id'] == str(request.form['idSignalé'])+"/"+str(session['id'])), -1)
        del motifDemand[index]

    else:
        # on ajoute son signalement
        sign.append(session['id']) # on ajoute son signalement
        motif.append({'id': session['id'], 'txt': request.form['Raison']})
        signDemand.append(request.form['idSignalé']+"/"+session['id'])
        motifDemand.append({'id': request.form['idSignalé']+"/"+session['id'], 'txt': 'Réponse Signalée'})


    demande.update()
    reponse.update()
    return 'sent'


@db_session
@login_required()
def signPostProfil():
    if not request.form.get('idSignalé'):
        abort(400) # il manque l'id du message

    # on récupère les signalements de l'utilisateur
    user = User.get(filter="cls.id == request.form['idSignalé']", limit=1)
    sign = user['sign']
    motif = user['motif']

    # on check mtn si l'utilisateur a déjà signalé la demande
    if session['id'] in sign:
        # on supprime son signalement
        sign.remove(session['id'])
        index = next((i for i, item in enumerate(motif) if item['id'] == session['id']), -1)
        del motif[index]

    else:
        # on ajoute son signalement
        sign.append(session['id'])
        motif.append({'id': session['id'], 'txt': request.form['Raison']})

    user.update()

    return 'sent'


@db_session
@login_required()
def signPostDiscussion():
    if not request.form.get('idSignalé'):
        abort(400) # il manque l'id du message

    # on récupère les signalements du groupe
    groupe = Group.get(filter="cls.id == request.form['idSignalé']", limit=1)
    sign = groupe['sign']
    motif = groupe['motif']

    # on check mtn si l'utilisateur a déjà signalé la demande
    if session['id'] in sign:
        # on supprime son signalement
        sign.remove(session['id'])
        index = next((i for i, item in enumerate(motif) if item['id'] == session['id']), -1)
        del motif[index]

        grpMsg = Message.get(filter="cls.id_groupe == request.form['idSignalé']")
        for m in grpMsg:
            mSign = m['sign']
            mMotif = m['motif']

            mSign.remove(session['id'])
            mIndex = next((i for i, item in enumerate(mMotif) if item['id'] == session['id']), -1)
            del mMotif[mIndex]

            m.update()

    else:
        # on ajoute son signalement
        sign.append(session['id'])
        motif.append({'id': session['id'], 'txt': request.form['Raison']})

        grpMsg = Message.get(filter="cls.id_groupe == request.form['idSignalé']")
        for m in grpMsg:
            mSign = m['sign']
            mMotif = m['motif']

            mSign.append(session['id'])
            mMotif.append({'id': session['id'], 'txt': "Discussion signalée pour : "+request.form['Raison']})

            m.update()

    groupe.update()

    return 'sent'


@db_session
@login_required()
def signPostMsg():
    if not request.form.get('idSignalé') and not request.form.get('idMsgSignalé'):
        abort(400)
    # on récupère les signalements de la demande d'aide
    groupe = Group.get(filter="cls.id == request.form['idSignalé']", limit=1)
    sign = groupe['sign']
    motif = groupe['motif']
    message = Message.get(filter="cls.id == request.form['idMsgSignalé']", limit=1)
    signMsg = message['sign']
    motifMsg = message['motif']

    # on check mtn si l'utilisateur a déjà signalé la demande
    if session['id'] in signMsg:
        # on retire son signalement
        signMsg.remove(session['id'])
        index = next((i for i, item in enumerate(motifMsg) if item['id'] == session['id']), -1)
        del motifMsg[index]
        sign.remove(request.form['idMsgSignalé'])
        index = next((i for i, item in enumerate(motif) if item['id'] == request.form['idMsgSignalé']), -1)
        del motif[index]

    else:
        # on ajoute son signalement
        signMsg.append(session['id'])
        motifMsg.append({'id': session['id'], 'txt': request.form['Raison']})

        if not session['id'] in sign:
            sign.append(request.form['idMsgSignalé'])
            motif.append({'id': request.form['idMsgSignalé'], 'txt': "Message signalé : "+request.form['Raison']})

    groupe.update()
    message.update()

    return 'sent'
