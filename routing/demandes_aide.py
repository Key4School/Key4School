from flask import Flask, render_template, request, redirect, session, url_for, abort, escape, send_file
from datetime import *
from flask.json import jsonify
from bson.objectid import ObjectId
import os
from db_poo import *
from routing.functions import listeModeration, automoderation, Interval

@db_session
def question():
    global demandes_aide

    if 'id' in session:
        if request.method == 'POST':
            # Impossibilité demande d'aide vide
            if request.form['titre'] == '':
                return redirect('/question/')

            user = User.get(filter="cls.id == session['id']", limit=1)
            if user['SanctionEnCour'] != "Spec" and user['SanctionEnCour'] != "SpecForum":
                if request.files['file'].mimetype != 'application/octet-stream':
                    if request.files['file'].mimetype == 'application/pdf':
                        fileType = 'pdf'
                    else:
                        fileType = 'image'
                else:
                    fileType = 'none'

                id = ObjectId()
                demandes_aide[str(id)] = Demande({"id": id, "id-utilisateur": session['id'], "titre": automoderation(escape(request.form['titre'])), "contenu": automoderation(request.form['demande']), "date_envoi": datetime.now(), "matière": request.form['matiere'], "réponses associées": {}, "likes": [], "sign": [], "resolu": False, "fileType": fileType})
                demandes_aide[str(id)].insert()

                if request.files['file'].mimetype != 'application/octet-stream':
                    nom = "DemandeFile_" + str(id)
                    DB.cluster.save_file(nom, request.files['file'])

                # add XP
                user.addXP(10)

                return redirect('/comments/' + str(id))

            else:
                return redirect(url_for('accueil'))

            # return render_template('question.html', envoi="Envoi réussi")
        else:
            profilUtilisateur = User.get(filter="cls.id == session['id']", limit=1)

            if profilUtilisateur["SanctionEnCour"] != "Spec" and profilUtilisateur['SanctionEnCour'] != "SpecForum":
                return render_template('question.html', profilUtilisateur=profilUtilisateur, user=profilUtilisateur)
            else:
                return redirect(url_for('accueil'))
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

def redirect_comments():
    return redirect('/')

@db_session
def comments(idMsg):
    global demandes_aide
    global notifications

    if 'id' in session:
        if request.method == 'GET':
            if idMsg in demandes_aide:
                msg = demandes_aide[idMsg].toDict()

                for notif in [notification for notification in notifications.values() if notification.id_groupe == ObjectId(idMsg) and notification.type == 'demande' and session['id'] in notification.destinataires]:
                    notif.supprUser(session['id'])

                return render_template("comments.html", d=msg, user=User.get(filter="cls.id == session['id']", limit=1))
            else:
                for notif in [notification for notification in notifications.values() if notification.id_groupe == ObjectId(idMsg) and notification.type == 'demande' and session['id'] in notification.destinataires]:
                    notif.supprUser(session['id'])
                return redirect('/')
        else:
            if 'rep' in request.form:
                if idMsg in demandes_aide:
                    msg = demandes_aide[idMsg].toDict()
                    reponses = msg['reponses_associees']

                    id = ObjectId()
                    reponses[str(id)] = Reponse({
                        'id': ObjectId(id),
                        'id-utilisateur': session['id'],
                        'contenu': automoderation(request.form.get('rep')),
                        'date_envoi': datetime.now(),
                        'likes': [],
                        'sign': [],
                    })

                    demandes_aide[idMsg].update()

                    Notification.create("demande", ObjectId(idMsg), id, [msg['idAuteur']])

                    # add XP
                    if not session['id'] == msg['idAuteur']:
                        User.get(filter="cls.id == session['id']", limit=1).addXP(15)

            return redirect('/comments/' + idMsg)
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

@db_session
def updateDemand():
    global demandes_aide

    if 'id' in session:
        demand = demandes_aide[request.form['idDemandModif']]
        if session['id'] == demand.id_utilisateur:
            demand.contenu = automoderation(request.form['txtModif'])
            demand.update()
        return 'sent'
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

@db_session
def file(fileName):
    if 'id' in session:
        return DB.cluster.send_file(fileName)

    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

@db_session
def DL_file(fileName, fileType):
    if 'id' in session or fileType == 'img':
        fileBinaryObj = DB.cluster.send_file(fileName)
        fileBinaryObj.freeze()
        fileBinary = fileBinaryObj.get_data()

        if fileType == 'image' or fileType == 'img':
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

    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

def delete_file(path):
    return os.remove(path)

@db_session
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
                if not session['id'] == demande['idAuteur']:
                    User.get(filter="cls.id == session['id']", limit=1).addXP(-2)
            else:
                likes.append(session['id'])  # on ajoute son like

                # add XP
                if not session['id'] == demande['idAuteur']:
                    User.get(filter="cls.id == session['id']", limit=1).addXP(2)

            # on update dans la DB
            demandes_aide[idPost].update()

            # on retourne enfin le nouveau nb de likes
            return {'newNbLikes': len(likes)}, 200

        else:
            abort(403)  # il manque l'id du message
    else:
        abort(401)  # non autorisé

@db_session
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
                if not session['id'] == demande['idAuteur']:
                    User.get(filter="cls.id == session['id']", limit=1).addXP(-2)
            else:
                likes.append(session['id'])  # on ajoute son like

                # add XP
                if not session['id'] == demande['idAuteur']:
                    User.get(filter="cls.id == session['id']", limit=1).addXP(2)

            # on update dans la DB
            demandes_aide[idPost].update()

            # on retourne enfin le nouveau nb de likes
            return {'newNbLikes': len(likes)}, 200

        else:
            abort(400)  # il manque l'id du message
    else:
        abort(401)  # non autorisé

@db_session
def resoudre(idPost):
    global demandes_aide

    if 'id' in session:
        if 'idPost' != None:
            demande = demandes_aide[idPost]

            # on check mtn si l'utilisateur a déjà liké la demande
            if demande.id_utilisateur == session['id']:
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

@db_session
def updateComment():
    global demandes_aide

    if 'id' in session:
        Comment = demandes_aide[request.form['idDemandCommentModif']].toDict()['reponsesDict2'][request.form['idCommentModif']]
        if session['id'] == Comment.id_utilisateur:
            Comment.contenu = automoderation(request.form['txtModif'])
            demandes_aide[request.form['idDemandCommentModif']].update()
        return 'sent'
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

@db_session
def savePost(postId):

    if 'id' in session:
        user = User.get(filter="cls.id == session['id']", limit=1)
        savedPost = user['savedDemands']

        if ObjectId(postId) in savedPost:
            savedPost.remove(ObjectId(postId))
        else:
            savedPost.append(ObjectId(postId))

        user.update()

        return 'sent'
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))
