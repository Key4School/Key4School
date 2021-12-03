from flask import Flask, render_template, request, redirect, session, url_for, abort, escape, send_file
from datetime import *
from flask.json import jsonify
import os
from db_poo import *
from routing.functions import listeModeration, automoderation


@db_session
def question():
    if 'id' in session:
        if request.method == 'POST':
            # Impossibilité demande d'aide vide
            if request.form['titre'] == '':
                return redirect('/question/')

            user = User.get(filter="cls.id == session['id']", limit=1)
            if user['SanctionEnCour'] != "Spec" and user['SanctionEnCour'] != "SpecForum":
                file = FileUploader(request.files['file'])
                if file.verif('image', 'pdf'):
                    file.save()
                    idFile = file['id']
                else:
                    idFile = None

                demande = Request(id_utilisateur=session['id'], titre=automoderation(escape(request.form['titre'])), contenu=automoderation(
                    request.form['demande']), matière=request.form['matiere'], idFile=idFile)
                demande.insert()

                # add XP
                user.addXP(10)

                return redirect(url_for("comments", idMsg=str(demande['id'])))

            else:
                return redirect(url_for('accueil'))

            # return render_template('question.html', envoi="Envoi réussi")
        else:
            profilUtilisateur = User.get(
                filter="cls.id == session['id']", limit=1)

            if profilUtilisateur["SanctionEnCour"] != "Spec" and profilUtilisateur['SanctionEnCour'] != "SpecForum":
                return render_template('question.html', profilUtilisateur=profilUtilisateur, user=profilUtilisateur)
            else:
                return redirect(url_for('accueil'))
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))


@db_session
def comments(idMsg):
    if 'id' in session:
        if not idMsg or not is_valid_uuid(idMsg):
            return redirect('/')

        msg = Request.get(filter="cls.id == idMsg", limit=1)
        if request.method == 'GET':
            if msg:
                for notif in Notification.get(filter="(cls.id_groupe == idMsg) & (cls.type == 'demande') & (cls.destinataires.comparator.has_key(str(session['id'])))"):
                    notif.supprUser(session['id'])
                return render_template("comments.html", d=msg, user=User.get(filter="cls.id == session['id']", limit=1))
            else:
                for notif in Notification.get(filter="(cls.id_groupe == idMsg) & (cls.type == 'demande')"):
                    notif.supprNotif()
                return redirect('/')
        else:
            if 'rep' in request.form:
                if msg:
                    reponse = Response(
                        id_utilisateur=session['id'], id_groupe=msg['id'], contenu=automoderation(request.form.get('rep')))
                    reponse.insert()
                    Notification.create("demande", idMsg, reponse['id'], [
                                        msg['id_utilisateur']])

                    # add XP
                    if not session['id'] == msg['id_utilisateur']:
                        User.get(
                            filter="cls.id == session['id']", limit=1).addXP(15)

            return redirect(f'/comments/{idMsg}')
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))


@db_session
def updateDemand():
    if 'id' in session:
        demand = Request.get(
            filter="cls.id  == request.form['idDemandModif']", limit=1)
        if session['id'] == demand.id_utilisateur:
            demand['contenu'] = automoderation(request.form['txtModif'])
            demand.update()
        return 'sent'
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))


@db_session
def file(idFile):
    if 'id' in session:
        file = File.get(idFile)
        if not file:
            return abort(404)
        return send_file(file['path'], mimetype=file['mimetype'], attachment_filename=f"attachment.{file['ext']}")

    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))


@db_session
def DL_file(idFile):
    if 'id' in session:
        file = File.get(idFile)
        if not file:
            return abort(404)
        return send_file(file['path'], mimetype=file['mimetype'], attachment_filename=f"attachment.{file['ext']}", as_attachment=True)

    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))


@db_session
def likePost(idPost):
    if 'id' in session:
        if not idPost or not is_valid_uuid(idPost):
            return abort(404)

        # on récupère les likes de la demande d'aide
        demande = Request.get(filter="cls.id == idPost", limit=1)
        likes = demande['likes'].copy()

        # on check mtn si l'utilisateur a déjà liké la demande
        if session['id'] in likes:
            likes.remove(session['id'])  # on supprime son like

            # remove XP
            if not session['id'] == demande['id_utilisateur']:
                User.get(
                    filter="cls.id == session['id']", limit=1).addXP(-2)
        else:
            likes.append(session['id'])  # on ajoute son like

            # add XP
            if not session['id'] == demande['id_utilisateur']:
                User.get(
                    filter="cls.id == session['id']", limit=1).addXP(2)

        # on update dans la DB
        demande['likes'] = likes
        demande.update()

        # on retourne enfin le nouveau nb de likes
        return {'newNbLikes': len(likes)}, 200
    else:
        abort(401)  # non autorisé


@db_session
def likeRep(idRep):

    if 'id' in session:
        if not idRep or not is_valid_uuid(idRep):
            return abort(404)

        reponse = Response.get(filter="cls.id == idRep", limit=1)
        if not reponse:
            return abort(400)

        likes = reponse['likes'].copy()

        # on check mtn si l'utilisateur a déjà liké la demande
        if session['id'] in likes:
            likes.remove(session['id'])  # on supprime son like

            # remove XP
            if not session['id'] == demande['id_utilisateur']:
                User.get(
                    filter="cls.id == session['id']", limit=1).addXP(-2)
        else:
            likes.append(session['id'])  # on ajoute son like

            # add XP
            if not session['id'] == demande['id_utilisateur']:
                User.get(
                    filter="cls.id == session['id']", limit=1).addXP(2)

        # on update dans la DB
        reponse['likes'] = likes
        reponse.update()

        # on retourne enfin le nouveau nb de likes
        return {'newNbLikes': len(likes)}, 200
    else:
        abort(401)  # non autorisé


@db_session
def resoudre(idPost):

    if 'id' in session:
        if not idPost or not is_valid_uuid(idPost):
            return abort(404)

        demande = Request.get(filter="cls.id == idPost", limit=1)

        # on check mtn si l'utilisateur a déjà liké la demande
        if demande['id_utilisateur'] == session['id']:
            # on update dans la DB
            demande.resolu = True

            demande.update()

            return "ok", 200
        else:
            abort(401)  # non autorisé
    else:
        abort(401)  # non autorisé


@db_session
def updateComment():

    if 'id' in session:
        comment = Response.get(
            filter="cls.id == request.form['idCommentModif']", limit=1)
        if session['id'] == comment['id_utilisateur']:
            comment[contenu] = automoderation(request.form['txtModif'])
            comment.update()
        return 'sent'
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))


@db_session
def savePost(postId):
    '''A PASSER EN SOCKET'''
    if 'id' in session:
        if not postId or not is_valid_uuid(postId):
            return abort(404)

        user = User.get(filter="cls.id == session['id']", limit=1)
        savedPost = user['savedDemands'].copy()

        if postId in savedPost:
            savedPost.remove(postId)
        else:
            savedPost.append(postId)

        user['savedDemands'] = savedPost
        user.update()

        return 'sent'
    else:
        return abort(401) # non autorisé
