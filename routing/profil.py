from flask import Flask, render_template, request, redirect, session, url_for, abort, escape
from datetime import *
from flask.json import jsonify
from bson.objectid import ObjectId
from db_poo import *
from routing.functions import listeModeration, automoderation

def profil(idUser):
    global utilisateurs
    global demandes_aide

    if 'id' in session:
        if idUser == None or idUser == session['id']:
            toutesDemandes = sorted([d for d in demandes_aide.values() if d.id_utilisateur == ObjectId(session['id'])], key = lambda d: d.date_envoi, reverse=True)

            demandes = []
            for d in toutesDemandes:  # pour chaque demande, on va l'ajouter dans une liste qui sera donnée à la page HTML
                demandes.append(d.toDict())

            user = utilisateurs[session['id']]
            profilUtilisateur = user.toDict()
            niv, xplvl, xpgens = user.recupLevel()
            return render_template("profil.html", profilUtilisateur=profilUtilisateur, demandes=demandes, xplvl=xplvl, xp=xpgens, niv=niv, user=user, sessionId=ObjectId(session['id']))

        else:

            user = utilisateurs[session['id']]
            profilUtilisateur = utilisateurs[idUser].toDict()
            niv, xplvl, xpgens = utilisateurs[idUser].recupLevel()

            # translate spes/options/lv
            profilUtilisateur['langues'] = profilUtilisateur['langues-str']
            profilUtilisateur['spes'] = profilUtilisateur['spes-str']
            profilUtilisateur['options'] = profilUtilisateur['options-str']

            return render_template("affichProfil.html", profilUtilisateur=profilUtilisateur, a_sign=profilUtilisateur['a_sign'], xplvl=xplvl, xp=xpgens, niv=niv, user=user, sessionId=ObjectId(session['id']))
    else:
        session['redirect'] = request.path
        return redirect(url_for('sign-in'))

def changeTheme():
    global utilisateurs

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

        user = utilisateurs[session['id']]
        user.couleur = couleurs

        utilisateurs[session['id']].update()

        session['couleur'] = couleurs

        return redirect(url_for('profil'))
    else:
        session['redirect'] = request.path
        return redirect(url_for('sign-in'))

def updateprofile():
    global utilisateurs

    if 'id' in session:  # on vérifie que l'utilisateur est bien connecté sinon on le renvoie vers la connexion
        # je vérifie que c pas vide  #Pour chaque info que je récupère dans le formulaire qui est dans profil.html
        elementPrive = []
        elementPublic = []
        for content in request.form:
            if request.form[content] == "pv":
                elementPrive.append(content.replace('Visibilite', ''))
            elif request.form[content] == "pb":
                elementPublic.append(content.replace('Visibilite', ''))

        user = utilisateurs[session['id']]

        user.pseudo = automoderation(request.form['pseudo'])
        user.email = automoderation(request.form['email'])
        user.telephone = automoderation(request.form['telephone'])
        user.interets = automoderation(request.form['interets'])
        user.caractere = request.form['caractere']
        if user.type == 'ELEVE':
            user.langues = [request.form['lv1'], request.form['lv2']]
            user.options = [request.form['option1'], request.form['option2']]
            user.spes = [request.form['spe1'], request.form['spe2'], request.form['spe3']]
        elif user.type == 'ENSEIGNANT':
            user.matiere = request.form['matiere']
        user.elementPrive = elementPrive
        user.elementPublic = elementPublic

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
        user.notifs = notifs

        utilisateurs[session['id']].update()

        return redirect(url_for('profil'))
    else:
        session['redirect'] = request.path
        return redirect(url_for('sign-in'))

def otherSubject():
    global utilisateurs
    if 'id' in session and session['type'] != 'ELEVE':  # on vérifie que l'utilisateur est bien connecté sinon on le renvoie vers la connexion
        subjects = []
        for key, value in request.form.items():
            if value == 'on':
                subjects.append(key)
        print(subjects)
        utilisateurs[session['id']].matiere_autre = subjects
        utilisateurs[session['id']].update()
        return redirect(url_for('profil'))
    else:
        session['redirect'] = request.path
        return redirect(url_for('sign-in'))

def userImg(profilImg):
    if 'id' in session:
        return DB.cluster.send_file(profilImg)
    else:
        session['redirect'] = request.path
        return redirect(url_for('sign-in'))

def updateImg():
    global utilisateurs

    if 'id' in session:
        if request.form['but'] == "remove":
            MyImage = DB.db_files.find({'filename': {'$regex': 'imgProfile' + session['id']}})
            for a in MyImage:
                DB.db_files.delete_one({'_id': a['_id']})
                DB.db_chunks.delete_many({'files_id': a['_id']})

            user = utilisateurs[session['id']]
            user.nomImg = ''
            user.imgProfile = ''
            utilisateurs[session['id']].update()

        elif request.form['but'] == "replace":
            ImgNom = request.files['Newpicture'].filename + 'imgProfile' + session['id']
            MyImage = DB.db_files.find({'filename': {'$regex': 'imgProfile' + session['id']}})
            for a in MyImage:
                DB.db_files.delete_one({'_id': a['_id']})
                DB.db_chunks.delete_many({'files_id': a['_id']})

            DB.cluster.save_file(ImgNom, request.files['Newpicture'])
            image = DB.db_files.find_one({'filename': ImgNom})

            user = utilisateurs[session['id']]
            user.imgProfile = image['_id']
            user.nomImg = ImgNom
            utilisateurs[session['id']].update()

        return redirect(url_for('profil'))
    else:
        session['redirect'] = request.path
        return redirect(url_for('sign-in'))
