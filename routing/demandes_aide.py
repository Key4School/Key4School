from flask import Flask, render_template, request, redirect, session, url_for, abort, escape, send_file
from datetime import *
from flask.json import jsonify
from bson.objectid import ObjectId
import os
from db_poo import *
from routing.functions import listeModeration, automoderation, sendNotif, clientsNotif, Interval

def question():
    global utilisateurs
    global demandes_aide

    if 'id' in session:
        if request.method == 'POST':
            # Impossibilité demande d'aide vide
            if request.form['titre'] == '':
                return redirect('/question/')

            user = utilisateurs[session['id']].toDict()
            if user['SanctionEnCour'] != "Spec" and user['SanctionEnCour'] != "SpecForum":
                if request.files['file'].mimetype != 'application/octet-stream':
                    if request.files['file'].mimetype == 'application/pdf':
                        fileType = 'pdf'
                    else:
                        fileType = 'image'
                else:
                    fileType = 'none'

                _id = ObjectId()
                demandes_aide[str(_id)] = Demande({"_id": _id, "id-utilisateur": ObjectId(session['id']), "titre": automoderation(request.form['titre']), "contenu": automoderation(request.form['demande']), "date-envoi": datetime.now(), "matière": request.form['matiere'], "réponses associées": {}, "likes": [], "sign": [], "resolu": False, "fileType": fileType})
                demandes_aide[str(_id)].insert()

                if request.files['file'].mimetype != 'application/octet-stream':
                    nom = "DemandeFile_" + str(_id)
                    DB.cluster.save_file(nom, request.files['file'])

                # add XP
                utilisateurs[session['id']].addXP(10)

                return redirect('/comments/' + str(_id))

            else:
                return redirect(url_for('accueil'))

            # return render_template('question.html', envoi="Envoi réussi")
        else:
            profilUtilisateur = utilisateurs[session['id']].toDict()

            if profilUtilisateur["SanctionEnCour"] != "Spec" and profilUtilisateur['SanctionEnCour'] != "SpecForum":
                return render_template('question.html', profilUtilisateur=profilUtilisateur, user=profilUtilisateur)
            else:
                return redirect(url_for('accueil'))
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

def redirect_comments():
    return redirect('/')

def comments(idMsg):
    global utilisateurs
    global demandes_aide
    global notifications

    if 'id' in session:
        if request.method == 'GET':
            if idMsg in demandes_aide:
                msg = demandes_aide[idMsg].toDict()

                for notif in [notification for notification in notifications.values() if notification.id_groupe == ObjectId(idMsg) and notification.type == 'demande' and ObjectId(session['id']) in notification.destinataires]:
                    notif.supprUser(ObjectId(session['id']))

                return render_template("comments.html", d=msg, user=utilisateurs[session['id']].toDict())
            else:
                for notif in [notification for notification in notifications.values() if notification.id_groupe == ObjectId(idMsg) and notification.type == 'demande' and ObjectId(session['id']) in notification.destinataires]:
                    notif.supprUser(ObjectId(session['id']))
                return redirect('/')
        else:
            if 'rep' in request.form:
                if idMsg in demandes_aide:
                    msg = demandes_aide[idMsg].toDict()
                    reponses = msg['reponsesObjects']

                    _id = ObjectId()
                    reponses[str(_id)] = Reponse({
                        '_id': ObjectId(_id),
                        'id-utilisateur': ObjectId(session['id']),
                        'contenu': automoderation(request.form.get('rep')),
                        'date-envoi': datetime.now(),
                        'likes': [],
                        'sign': [],
                    })

                    demandes_aide[idMsg].update()

                    sendNotif("demande", ObjectId(idMsg), _id, [msg['idAuteur']])

                    # add XP
                    if not ObjectId(session['id']) == msg['idAuteur']:
                        utilisateurs[session['id']].addXP(15)

            return redirect('/comments/' + idMsg)
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

def updateDemand():
    global utilisateurs
    global demandes_aide

    if 'id' in session:
        demand = demandes_aide[request.form['idDemandModif']]
        if ObjectId(session['id']) == demand.id_utilisateur:
            demand.contenu = automoderation(request.form['txtModif'])
            demand.update()
        return 'sent'
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

def file(fileName):
    if 'id' in session:
        return DB.cluster.send_file(fileName)

    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

def DL_file(fileName, fileType):
    if 'id' in session:
        fileBinaryObj = DB.cluster.send_file(fileName)
        fileBinaryObj.freeze()
        fileBinary = fileBinaryObj.get_data()

        if fileType == 'image':
            with open('static/temp/{}.png'.format(fileName), 'wb') as file:
                file.write(fileBinary)

            interval = Interval(2, delete_file, args=['static/temp/{}.png'.format(fileName)])
            interval.start()

            return send_file('static/temp/{}.png'.format(fileName))
        elif fileType == 'pdf':
            with open('static/temp/{}.pdf'.format(fileName), 'wb') as file:
                file.write(fileBinary)

            interval = Interval(2, delete_file, args=['static/temp/{}.pdf'.format(fileName)])
            interval.start()

            return send_file('static/temp/{}.pdf'.format(fileName))
        else:
            return ''

        # print(fileBinary)
        # return fileBinary
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

def delete_file(path):
    return os.remove(path)

def likePost(idPost):
    global demandes_aide

    if 'id' in session:
        if 'idPost' != None:
            # on récupère les likes de la demande d'aide
            demande = demandes_aide[idPost].toDict()
            likes = demande['likes']

            # on check mtn si l'utilisateur a déjà liké la demande
            if session['id'] in likes:
                likes.remove(session['id'])  # on supprime son like

                # remove XP
                if not ObjectId(session['id']) == demande['idAuteur']:
                    utilisateurs[demande['id-utilisateur']].addXP(-2)
            else:
                likes.append(session['id'])  # on ajoute son like

                # add XP
                if not ObjectId(session['id']) == demande['idAuteur']:
                    utilisateurs[demande['id-utilisateur']].addXP(2)

            # on update dans la DB
            demandes_aide[idPost].update()

            # on retourne enfin le nouveau nb de likes
            return {'newNbLikes': len(likes)}, 200

        else:
            abort(403)  # il manque l'id du message
    else:
        abort(401)  # non autorisé

def likeRep(idPost, idRep):
    global demandes_aide

    if 'id' in session:
        if 'idPost' != None and 'idRep' != None:
            # on récupère les likes de la demande d'aide
            demande = demandes_aide[idPost].toDict()
            reponses = demande['reponsesDict']
            if not idRep in reponses:
                return abort(400)
            reponse = reponses[idRep]

            likes = reponse['likes']

            # on check mtn si l'utilisateur a déjà liké la demande
            if session['id'] in likes:
                likes.remove(session['id'])  # on supprime son like

                # remove XP
                if not ObjectId(session['id']) == demande['idAuteur']:
                    utilisateurs[demande['id-utilisateur']].addXP(-2)
            else:
                likes.append(session['id'])  # on ajoute son like

                # add XP
                if not ObjectId(session['id']) == demande['idAuteur']:
                    utilisateurs[demande['id-utilisateur']].addXP(2)

            # on update dans la DB
            demandes_aide[idPost].update()

            # on retourne enfin le nouveau nb de likes
            return {'newNbLikes': len(likes)}, 200

        else:
            abort(400)  # il manque l'id du message
    else:
        abort(401)  # non autorisé

def resoudre(idPost):
    global demandes_aide

    if 'id' in session:
        if 'idPost' != None:
            demande = demandes_aide[idPost]

            # on check mtn si l'utilisateur a déjà liké la demande
            if demande.id_utilisateur == ObjectId(session['id']):
                # on update dans la DB
                demande.resolu = True

                demandes_aide[idPost].update()

                return "ok", 200
            else:
                abort(401) # non autorisé


        else:
            abort(403) # il manque l'id du message
    else:
        abort(401) # non autorisé

def updateComment():
    global utilisateurs
    global demandes_aide

    if 'id' in session:
        Comment = demandes_aide[request.form['idDemandCommentModif']].toDict()['reponsesDict2'][request.form['idCommentModif']]
        if ObjectId(session['id']) == Comment.id_utilisateur:
            Comment.contenu = automoderation(request.form['txtModif'])
            demandes_aide[request.form['idDemandCommentModif']].update()
        return 'sent'
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

def savePost(postId):
    global utilisateurs

    if 'id' in session:
        user = utilisateurs[session['id']].toDict()
        savedPost = user['savedDemands']

        if ObjectId(postId) in savedPost:
            savedPost.remove(ObjectId(postId))
        else:
            savedPost.append(ObjectId(postId))

        utilisateurs[session['id']].update()

        return 'sent'
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))
