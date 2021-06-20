from flask import Flask, render_template, request, redirect, session, url_for, abort, escape
from datetime import *
from flask.json import jsonify
from bson.objectid import ObjectId
from db_poo import *

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
                addXP(session['id'], 10)

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
            msg = demandes_aide[idMsg].toDict()

            for notif in [notification for notification in notifications.values() if notification.id_groupe == ObjectId(idMsg) and notification.type == 'demande' and ObjectId(session['id']) in notification.destinataires]:
                notif.supprUser(ObjectId(session['id']))

            return render_template("comments.html", d=msg, user=utilisateurs[session['id']].toDict())

        else:
            if 'rep' in request.form:
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
                    addXP(session['id'], 15)

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
            demand.contenu = request.form['txtModif']
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
                    addXP(demande['id-utilisateur'], -2)
            else:
                likes.append(session['id'])  # on ajoute son like

                # add XP
                if not ObjectId(session['id']) == demande['idAuteur']:
                    addXP(demande['id-utilisateur'], 2)

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
                    addXP(demande['id-utilisateur'], -2)
            else:
                likes.append(session['id'])  # on ajoute son like

                # add XP
                if not ObjectId(session['id']) == demande['idAuteur']:
                    addXP(demande['id-utilisateur'], 2)

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