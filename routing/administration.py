from flask import Flask, render_template, request, redirect, session, url_for, abort, escape
from datetime import *
from flask.json import jsonify
from bson.objectid import ObjectId
from db_poo import *
from routing.functions import listeModeration, automoderation, clientsNotif

def administration():
    global utilisateurs
    global demandes_aide
    global groupes
    global Reponse

    if 'id' in session:
        utilisateur = utilisateurs[session['id']].toDict()

        if utilisateur['admin'] == True:
            if request.method == 'POST':
                if request.form['demandeBut'] == 'Suppr':
                    auteur = utilisateurs[str(demandes_aide[request.form['idSuppr']].toDict()['idAuteur'])]
                    sanction = auteur.toDict()['Sanctions']
                    demandes_aide[request.form['idSuppr']].delete()
                    del demandes_aide[request.form['idSuppr']]
                    auteur.addXP(-10)
                    auteur.addXpModeration(10)
                    sanction.append({"SanctionType": "Demandes d'aide supprimée", "SanctionMotif": request.form['motif'], "SanctionNext": 'Aucune', "dateSanction" : datetime.now()})
                    auteur.update()

                elif request.form['demandeBut'] == 'Val':
                    demande = demandes_aide[request.form['idVal']]
                    sign = demande.sign
                    if request.form['motif'] == "abusif":
                        for content in sign:
                            if "/" not in str(content):
                                utilisateurs[str(content)].addXpModeration(5)
                                sanction = utilisateurs[str(content)].toDict()['Sanctions']
                                sanction.append({"SanctionType": "Demandes d'aide supprimée", "SanctionMotif": 'Signalement abusif', "SanctionNext": 'Aucune', "dateSanction" : datetime.now()})
                                utilisateurs[str(content)].update()
                    motif = demande.motif
                    for i in range (len(sign)):
                        if "/" not in str(sign[i]):
                            del sign[i]
                    for a in range (len(motif)):
                        if "/" not in str(motif[a]):
                            del motif[a]

                    demandes_aide[request.form['idVal']].update()

                elif request.form['demandeBut'] == 'ValUser':
                    user = utilisateurs[request.form['idValidé']]
                    if request.form['motif'] == "abusif":
                        for content in user.sign:
                            utilisateurs[str(content)].addXpModeration(5)
                            sanction = utilisateurs[str(content)].toDict()['Sanctions']
                            sanction.append({"SanctionType": "Aucune", "SanctionMotif": 'Signalement abusif', "SanctionNext": 'Aucune', "dateSanction" : datetime.now()})
                            utilisateurs[str(content)].update()
                    user.sign = []
                    user.motif = []
                    utilisateurs[request.form['idValidé']].update()

                elif request.form['demandeBut'] == 'SupprRep':
                    demande = demandes_aide[request.form['idDemandSuppr']]
                    auteur = utilisateurs[str(demandes_aide[request.form['idDemandSuppr']].toDict()['reponsesDict'][request.form['idSuppr']]['id-utilisateur'])]
                    auteur.addXpModeration(5)
                    auteur.addXP(-15)
                    sanction = auteur.toDict()['Sanctions']
                    sanction.append({"SanctionType": "Réponse supprimée", "SanctionMotif": request.form['motif'], "SanctionNext": 'Aucune', "dateSanction" : datetime.now()})
                    auteur.update()

                    demande.reponses_associees.pop(request.form['idSuppr'])
                    signDemande = demande.sign
                    motifDemande = demande.motif

                    for i in range (len(signDemande)):
                        if str(request.form['idSuppr']+"/") in str(signDemande[i]):
                            del signDemande[i]
                    for a in range (len(motifDemande)):
                        if str(request.form['idSuppr']+"/") in str(motifDemande[a]):
                            del motifDemande[a]
                    demande.update()

                elif request.form['demandeBut'] == 'ValRep':
                    demande = demandes_aide[request.form['idDemandVal']]
                    signDemande = demande.sign
                    motifDemande = demande.motif
                    sign =  demandes_aide[request.form['idDemandVal']].toDict()['reponsesDict'][request.form['idVal']]['sign']
                    print ('sign')
                    if request.form['motif'] == "abusif":
                        for content in sign :
                                sanction = utilisateurs[str(content)].toDict()['Sanctions']
                                utilisateurs[str(content)].addXpModeration(5)
                                sanction.append({"SanctionType": "Aucune", "SanctionMotif": 'Signalement abusif', "SanctionNext": 'Aucune', "dateSanction" : datetime.now()})
                    demandes_aide[request.form['idDemandVal']].toDict()['reponsesDict'][request.form['idVal']]['sign'].clear()
                    demandes_aide[request.form['idDemandVal']].toDict()['reponsesDict'][request.form['idVal']]['motif'].clear()
                    for i in range(len(signDemande)):
                        if str(request.form['idVal']+"/") in str(signDemande[i]):
                            del signDemande[i]
                    for a in range(len(motifDemande)):
                        if str(request.form['idVal']+"/") in str(motifDemande[a]):
                            del motifDemande[a]
                    demandes_aide[request.form['idDemandVal']].update()

                elif request.form['demandeBut'] == 'supprDisc':
                    groupe = groupes[request.form['idDiscSuppr']].toDict()
                    sign = groupe['sign']
                    motif = groupe['motif']
                    for auteur in groupe['id-utilisateurs'] :
                        utilisateurs[str(auteur)].addXpModeration(10)

                    sign.clear()
                    motif.clear()
                    grpMsg = [m.toDict() for m in messages.values() if m.id_groupe == ObjectId(request.form['idDiscSuppr'])]
                    for m in grpMsg:
                        messages[str(m['_id'])].suppr()

                            # messages[str(m['_id'])].update()
                    groupes[request.form['idDiscSuppr']].update()

                elif request.form['demandeBut'] == 'valDisc':
                    groupe = groupes[request.form['idDiscVal']].toDict()
                    sign = groupe['sign']
                    motif = groupe['motif']
                    if request.form['motif'] == "abusif":
                        for content in sign:
                                utilisateurs[str(content)].addXpModeration(5)
                    # on supprime son signalement
                    sign.clear()
                    motif.clear()

                    grpMsg = [m.toDict() for m in messages.values() if m.id_groupe == ObjectId(request.form['idDiscVal'])]
                    for m in grpMsg:
                        m['motif'].clear()
                        m['sign'].clear()
                        messages[str(m['_id'])].update()
                    groupes[request.form['idDiscVal']].update()


                return 'sent'

            else:
                demandeSignale = sorted([d.toDict() for d in demandes_aide.values() if d.sign != []], key = lambda d: len(d['sign']), reverse=True)
                profilSignale = sorted([u.toDict() for u in utilisateurs.values() if u.sign != []], key = lambda u: len(u['sign']), reverse=True)
                discussionSignale = sorted([g.toDict() for g in groupes.values() if g.sign != []], key = lambda g: len(g['sign']), reverse=True)
                return render_template('administration.html', user=utilisateur, demandeSignale=demandeSignale, profilSignale=profilSignale, discussionSignale=discussionSignale)
        else:
            return redirect(url_for('accueil'))
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

def suppressionMsg():
    global messages
    global utilisateurs
    global groupes

    if 'id' in session:
        idGroupe = request.form['grp']
        user = utilisateurs[session['id']].toDict()
        msg = messages[request.form['msgSuppr']].toDict()
        groupe = groupes[request.form['grp']].toDict()
        sign=groupe['sign']
        motif = groupe['motif']
        # grp = Groupe[request.form['grp']].toDict()
        if user['admin'] or user['type']=="ENSEIGNANT" or msg['id-utilisateur']==ObjectId(session['id']) or ObjectId(session['id'] in grp['moderateurs']):
            if msg['sign'] != []:
                sign.remove(ObjectId(request.form['msgSuppr']))
                index = next((i for i, item in enumerate(motif) if item['id'] == ObjectId(request.form['msgSuppr'])), -1)
                del motif[index]
            messages[request.form['msgSuppr']].suppr()
            groupes[request.form['grp']].update()

        return redirect(url_for('page_messages', idGroupe=idGroupe))

    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

def validerMsg():
    global messages
    global groupes

    if 'id' in session:
        user = utilisateurs[session['id']].toDict()
        idGroupe = request.form['grp']

        if user['admin']:
            message = messages[request.form['msgVal']].toDict()
            signMsg = message['sign']
            motifMsg = message['motif']
            signMsg.clear()
            motifMsg.clear()
            groupe = groupes[request.form['grp']].toDict()
            sign = groupe['sign']
            motif = groupe['motif']
            sign.remove(ObjectId(request.form['msgVal']))
            index = next((i for i, item in enumerate(motif) if item['id'] == ObjectId(request.form['msgVal'])), -1)
            del motif[index]

            groupes[request.form['grp']].update()
            messages[request.form['msgVal']].update()

        return redirect(url_for('page_messages', idGroupe=idGroupe))

    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

def sanction():
    global utilisateurs

    if 'id' in session:
        utilisateur = utilisateurs[session['id']].toDict()

        if utilisateur['admin'] == True:
            user = utilisateurs[request.form['idSanctionné']]
            userDict = user.toDict()
            sanctions = userDict['Sanctions']

            sanctions.append({"SanctionType": request.form['Sanction'], "SanctionMotif": request.form['Raison'], "SanctionNext": request.form['Next'], "dateSanction" : datetime.now()})

            time = datetime.now() + timedelta(days= int(request.form['SanctionDuree']))

            if request.form['SanctionType'] == 'Spec' or request.form['SanctionType'] == 'SpecProfil' or request.form['SanctionType'] == 'SpecForum' or request.form['SanctionType'] == 'SpecMsg':
                user.SanctionEnCour = request.form['SanctionType']
                user.SanctionDuree = time
                utilisateurs[request.form['idSanctionné']].addXpModeration(50)

            elif request.form['SanctionType'] == 'ResetProfil':
                MyImage = DB.db_files.find({'filename': {'$regex': 'imgProfile' + request.form['idSanctionné']}})
                utilisateurs[request.form['idSanctionné']].addXpModeration(25)
                for a in MyImage:
                    DB.db_files.delete_one({'_id': a['_id']})
                    DB.db_chunks.delete_many({'files_id': a['_id']})

                user.imgProfile = ''
                user.nomImg = ''
                user.pseudo = '{}_{}'.format(user.nom, user.prenom)
                user.telephone = ''
                user.interets = ''
                user.email = ''

            utilisateurs[request.form['idSanctionné']].update()

            return 'sent'

        else:
            return redirect(url_for('accueil'))
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

def signPost():
    global demandes_aide

    if 'id' in session:
        if request.form['idSignalé'] != None:
            # on récupère les signalements de la demande d'aide
            demande = demandes_aide[request.form['idSignalé']].toDict()
            sign = demande['sign']
            motif = demande['motif']

            # on check mtn si l'utilisateur a déjà signalé la demande
            if ObjectId(session['id']) in sign:
                # on supprime son signalement
                sign.remove(ObjectId(session['id']))
                index = next((i for i, item in enumerate(motif) if item['id'] == ObjectId(session['id'])), -1)
                del motif[index]

            else:
                # on ajoute son signalement
                sign.append(ObjectId(session['id'])) # on ajoute son signalement
                motif.append({'id': ObjectId(session['id']), 'txt': request.form['Raison']})

            demandes_aide[request.form['idSignalé']].update()

            return 'sent'

        else:
            abort(403) # il manque l'id du message
    else:
        abort(401) # non autorisé

def signRepPost():
    global demandes_aide
    if 'id' in session:
        if request.form['idSignalé'] != None and request.form['idDemandSignalé'] != None:
            # on récupère les signalements de la demande d'aide
            demande = demandes_aide[request.form['idDemandSignalé']].toDict()
            sign = demande['reponsesDict'][request.form['idSignalé']]['sign']
            motif = demande['reponsesDict'][request.form['idSignalé']]['motif']
            signDemand = demande['sign']
            motifDemand = demande['motif']

            if ObjectId(session['id']) in sign:
                # on supprime son signalement
                sign.remove(ObjectId(session['id']))
                index = next((i for i, item in enumerate(motif) if item['id'] == ObjectId(session['id'])), -1)
                del motif[index]
                signDemand.remove(request.form['idSignalé']+"/"+session['id'])
                index = next((i for i, item in enumerate(motifDemand) if item['id'] == str(request.form['idSignalé'])+"/"+str(session['id'])), -1)
                del motifDemand[index]

            else:
                # on ajoute son signalement
                sign.append(ObjectId(session['id'])) # on ajoute son signalement
                motif.append({'id': ObjectId(session['id']), 'txt': request.form['Raison']})
                signDemand.append(request.form['idSignalé']+"/"+session['id'])
                motifDemand.append({'id': request.form['idSignalé']+"/"+session['id'], 'txt': 'Réponse Signalée'})


            demandes_aide[request.form['idDemandSignalé']].update()
            return 'sent'

        else:
            abort(403) # il manque l'id du message
    else:
        abort(401) # non autorisé

def signPostProfil():
    global utilisateurs

    if 'id' in session:
        if request.form['idSignalé'] != None:
            # on récupère les signalements de l'utilisateur
            user = utilisateurs[request.form['idSignalé']].toDict()
            sign = user['sign']
            motif = user['motif']

            # on check mtn si l'utilisateur a déjà signalé la demande
            if ObjectId(session['id']) in sign:
                # on supprime son signalement
                sign.remove(ObjectId(session['id']))
                index = next((i for i, item in enumerate(motif) if item['id'] == ObjectId(session['id'])), -1)
                del motif[index]

            else:
                # on ajoute son signalement
                sign.append(ObjectId(session['id']))
                motif.append({'id': ObjectId(session['id']), 'txt': request.form['Raison']})

            utilisateurs[request.form['idSignalé']].update()

            return 'sent'

        else:
            abort(403) # il manque l'id du message
    else:
        abort(401) # non autorisé

def signPostDiscussion():
    global messages
    global groupes

    if 'id' in session:
        if request.form['idSignalé'] != None:
            # on récupère les signalements du groupe
            groupe = groupes[request.form['idSignalé']].toDict()
            sign = groupe['sign']
            motif = groupe['motif']

            # on check mtn si l'utilisateur a déjà signalé la demande
            if ObjectId(session['id']) in sign:
                # on supprime son signalement
                sign.remove(ObjectId(session['id']))
                index = next((i for i, item in enumerate(motif) if item['id'] == ObjectId(session['id'])), -1)
                del motif[index]

                grpMsg = [m.toDict() for m in messages.values() if m.id_groupe == ObjectId(request.form['idSignalé'])]
                for m in grpMsg:
                    mSign = m['sign']
                    mMotif = m['motif']

                    mSign.remove(ObjectId(session['id']))
                    mIndex = next((i for i, item in enumerate(mMotif) if item['id'] == ObjectId(session['id'])), -1)
                    del mMotif[mIndex]

                    messages[str(m['_id'])].update()

            else:
                # on ajoute son signalement
                sign.append(ObjectId(session['id']))
                motif.append({'id': ObjectId(session['id']), 'txt': request.form['Raison']})

                grpMsg = [m.toDict() for m in messages.values() if m.id_groupe == ObjectId(request.form['idSignalé'])]
                for m in grpMsg:
                    mSign = m['sign']
                    mMotif = m['motif']

                    mSign.append(ObjectId(session['id']))
                    mMotif.append({'id': ObjectId(session['id']), 'txt': "Discussion signalée pour : "+request.form['Raison']})

                    messages[str(m['_id'])].update()

            groupe = groupes[request.form['idSignalé']].update()

            return 'sent'

        else:
            abort(403) # il manque l'id du message
    else:
        abort(401) # non autorisé

def signPostMsg():
    global messages
    global groupes

    if 'id' in session:
        if request.form['idSignalé'] != None and request.form['idMsgSignalé'] != None:
            # on récupère les signalements de la demande d'aide
            groupe = groupes[request.form['idSignalé']].toDict()
            sign = groupe['sign']
            motif = groupe['motif']
            message = messages[request.form['idMsgSignalé']].toDict()
            signMsg = message['sign']
            motifMsg = message['motif']

            # on check mtn si l'utilisateur a déjà signalé la demande
            if ObjectId(session['id']) in signMsg:
                # on retire son signalement
                signMsg.remove(ObjectId(session['id']))
                index = next((i for i, item in enumerate(motifMsg) if item['id'] == ObjectId(session['id'])), -1)
                del motifMsg[index]
                sign.remove(ObjectId(request.form['idMsgSignalé']))
                index = next((i for i, item in enumerate(motif) if item['id'] == ObjectId(request.form['idMsgSignalé'])), -1)
                del motif[index]

            else:
                # on ajoute son signalement
                signMsg.append(ObjectId(session['id']))
                motifMsg.append({'id': ObjectId(session['id']), 'txt': request.form['Raison']})

                if not ObjectId(session['id']) in sign:
                    sign.append(ObjectId(request.form['idMsgSignalé']))
                    motif.append({'id': ObjectId(request.form['idMsgSignalé']), 'txt': "Message signalé : "+request.form['Raison']})

                    groupes[request.form['idSignalé']].update()

            messages[request.form['idMsgSignalé']].update()

            return 'sent'

        else:
            abort(403) # il manque l'id du message
    else:
        abort(401) # non autorisé
