from flask import Flask, render_template, request, redirect, session, url_for, abort, escape, send_file
from datetime import *
from flask.json import jsonify
from db_poo import *
import os
from routing.functions import listeModeration, automoderation

@db_session
def profil(idUser):

    if 'id' in session:
        if idUser == None or idUser == session['id']:
            demandes = Request.get(filter="cls.id_utilisateur == session['id']", order_by="cls.date_envoi", desc=True)

            user = User.get(filter="cls.id == session['id']", limit=1)
            return render_template("profil.html", demandes=demandes, user=user)

        else:

            user = User.get(filter="cls.id == session['id']", limit=1)
            profilUtilisateur = User.get(filter="cls.id == idUser", limit=1)

            return render_template("affichProfil.html", profilUtilisateur=profilUtilisateur, a_sign=profilUtilisateur['a_sign'], user=user)
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

@db_session
def changeTheme():

    if 'id' in session:
        if int(request.form['couleur']) == 6:
            color2 = tuple(int(request.form['color2'].lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
            moyenne = '#%02x%02x%02x' % tuple((color+255)//2 for color in color2)
            couleurs = [request.form['color1'], request.form['color2'], request.form['color3'], moyenne]

        else:
            listColor = [['#00b7ff', '#a7ceff', '#94e1ff', '#d3e6ff', '#6595d1'],
                        ['#ff0000', '#ffa8a8', '#ff9494', '#ffd3d3', '#ab3333'],
                        ['#14db14', '#aeffa8', '#a0ff94', '#d6ffd3', '#5ab953'],
                        ['#ffbb00', '#e8c959', '#ffe294', '#f3e4ac', '#c5a73c'],
                        ['#e6445f', '#f3a6b3', '#afe2e7', '#f9d3d9', '#cd7d8b'],
                        ['#deb72f', '#e6cf81', '#e68181', '#f3e7c0', '#9f8f57']]
            couleurs = listColor[int(request.form['couleur'])]

        user = User.get(filter="cls.id == session['id']", limit=1)
        user['couleur'] = couleurs

        user.update()

        session['couleur'] = couleurs

        return redirect(url_for('profil'))
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

@db_session
def theme():
    if not 'id' in session:
        return 'error'

    user = User.get(filter="cls.id == session['id']", limit=1)
    user['theme'] = request.form['theme']
    session['theme'] = user.theme

    user.update()
    return 'ok'

@db_session
def updateprofile():

    if 'id' in session:  # on vérifie que l'utilisateur est bien connecté sinon on le renvoie vers la connexion
        # je vérifie que c pas vide  #Pour chaque info que je récupère dans le formulaire qui est dans profil.html
        elementPrive = []
        elementPublic = []
        for content in request.form:
            if request.form[content] == "pv":
                elementPrive.append(content.replace('Visibilite', ''))
            elif request.form[content] == "pb":
                elementPublic.append(content.replace('Visibilite', ''))

        user = User.get(filter="cls.id == session['id']", limit=1)

        user['nom'] = automoderation(request.form['nom'])
        user['prenom'] = automoderation(request.form['prenom'])
        user['pseudo'] = automoderation(request.form['pseudo'])
        user['email'] = automoderation(request.form['email'])
        user['telephone'] = automoderation(request.form['telephone'])
        user['interets'] = automoderation(request.form['interets'])
        if user['type'] == 'ELEVE':
            user['langues'] = [request.form['lv1'], request.form['lv2']]
            options = []
            if request.form['option1'] != 'none':
                options.append(request.form['option1'])
            if request.form['option2'] != 'none':
                options.append(request.form['option2'])
            user['options'] = options
            if user['classe'] == '1G':
                user['spes'] = [request.form['spe1'], request.form['spe2'], request.form['spe3']]
            elif user['classe'] == 'TG':
                user['spes'] = [request.form['spe1'], request.form['spe2']]
        elif user['type'] == 'ENSEIGNANT':
            user['matiere'] = request.form['matiere']
        user['elementPrive'] = elementPrive
        user['elementPublic'] = elementPublic

        notifs = {}
        if request.form['notifs_demandes'] == 'yes':
            notifs['demandes'] = True
        else:
            notifs['demandes'] = False
        if request.form['notifs_messages'] == 'yes':
            notifs['messages'] = True
        else:
            notifs['messages'] = False
        if 'notifs_sound' in request.form and request.form['notifs_sound'] == 'on':
            notifs['sound'] = True
        else:
            notifs['sound'] = False
        user['notifs'] = notifs

        user.update()

        return redirect(url_for('profil'))
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

@db_session
def otherSubject():
    '''QUAND ON PRENDRA EN CHARGE LES AUTRES USERS'''
    if 'id' in session and session['type'] != 'ELEVE':  # on vérifie que l'utilisateur est bien connecté sinon on le renvoie vers la connexion
        subjects = []
        for key, value in request.form.items():
            if value == 'on':
                subjects.append(key)
        user = User.get(filter="cls.id == session['id']", limit=1)
        user['matiere_autre'] = subjects
        user.update()
        return redirect(url_for('profil'))
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

@db_session
def userImg(profilImg):
    if 'id' in session:
        file = File.get(profilImg)
        if not file:
            file = File('default', r"static/image/sans_profil.png")
        return send_file(file['path'], mimetype=file['ext'], attachment_filename=f"profil.{file['ext']}")
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

@db_session
def updateImg():
    if 'id' in session:
        user = User.get(filter="cls.id == session['id']", limit=1)
        if request.form['but'] == "remove":
            oldFile = File.get(user['idImg'])
            oldFile.delete()

            user['idImg'] = None
            user.update()

        elif request.form['but'] == "replace":
            newFile = FileUploader(request.files['Newpicture'])
            if newFile['ext'] not in ['jpg', 'jpeg', 'jfif', 'pjpeg', 'pjp', 'png']:
                return redirect(url_for('profil'))

            oldFile = File.get(user['idImg'])
            oldFile.delete()

            newFile.save()

            user['idImg'] = newFile['id']
            user.update()

        return redirect(url_for('profil'))
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))
