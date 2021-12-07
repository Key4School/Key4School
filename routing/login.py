from flask import Flask, current_app as app, render_template, request, redirect, session, url_for, abort, escape
from datetime import *
from db_poo import *
import json
from routing.functions import automoderation


@db_session
def login():
    if request.method == 'POST':
        if 'password' not in request.form or 'username' not in request.form:
            return render_template('connexion.html', erreur='Veuillez compléter tous les champs')
        user = User.get(
            filter="(cls.email == request.form['username']) | (cls.pseudo == request.form['username'])", limit=1)
        if not user or not app.config['hashing'].check_value(user['mdp'], request.form['password'], salt=app.config['hashingKey']):
            return render_template('connexion.html', erreur='Identifiant ou mot de passe incorrect')

        session['id'] = user['id']
        session['pseudo'] = user['pseudo']
        session['couleur'] = user['couleur']
        session['theme'] = user['theme']
        session['type'] = user['type']
        session['cacheRandomKey'] = app.config['cacheRandomKey']

        if user['etapeInscription'] is not None:
            session.pop('id')
            session['idInscri'] = user['id']
            session['etapeInscription'] = user['etapeInscription']
            return redirect(url_for(f"signIn{session['etapeInscription']}"))

        elif 'redirect' in session:
            path = session['redirect']
            session.pop('redirect')
            return redirect(path)

        else:
            return redirect(url_for('accueil'))
    else:
        session['cacheRandomKey'] = app.config['cacheRandomKey']
        return render_template('connexion.html')


@db_session
def signIn0():
    if 'etapeInscription' in session:
        return redirect(url_for(f"signIn{session['etapeInscription']}"))

    if request.method == 'POST':
        notUse = False if User.get(
            filter="cls.email == request.form['email'] or cls.pseudo == request.form['pseudo']", limit=1) else True
        if notUse:
            hash = app.config['hashing'].hash_value(request.form['password'], salt=app.config['hashingKey'])
            user = User(nom=automoderation(request.form['nom']), prenom=automoderation(request.form['prenom']),
                        pseudo=automoderation(request.form['pseudo']), email=request.form['email'], mdp=hash, etapeInscription=1)
            user.insert()

            session['idInscri'] = user['id']
            session['cacheRandomKey'] = app.config['cacheRandomKey']
            session['theme'] = user['theme']
            session['etapeInscription'] = 1
            return redirect(url_for('signIn1'))
        else:
            return render_template('inscription0.html', erreur='Pseudo ou email déjà utilisé')
    else:
        session['cacheRandomKey'] = app.config['cacheRandomKey']
        return render_template('inscription0.html')


@db_session
def signIn1():
    if 'etapeInscription' not in session or 'idInscri' not in session:
        return redirect(url_for('login'))
    if session['etapeInscription'] != 1:
        return redirect(url_for(f"signIn{session['etapeInscription']}"))

    if request.method == 'POST':
        user = User.get(filter="cls.id == session['idInscri']", limit=1)
        user.signIn1(request.form['phone'],
                     datetime.strptime(request.form['birthday'], '%Y-%m-%d'),
                     json.loads(request.form['school']),
                     request.form['classe'],
                     [request.form['lva'], request.form['lvb']])
        session['etapeInscription'] = user['etapeInscription']
        return redirect(url_for('signIn2'))
    else:
        session['cacheRandomKey'] = app.config['cacheRandomKey']
        return render_template('inscription1.html')


@db_session
def signIn2():
    if 'etapeInscription' not in session or 'idInscri' not in session:
        return redirect(url_for('login'))
    if session['etapeInscription'] != 2:
        return redirect(url_for(f"signIn{session['etapeInscription']}"))

    if request.method == 'POST':
        user = User.get(filter="cls.id == session['idInscri']", limit=1)
        spes = []
        if 'spe1' in request.form:
            spes.append(request.form['spe1'])
            spes.append(request.form['spe2'])
            if 'spe3' in request.form:
                spes.append(request.form['spe3'])
        options = list(filter(lambda opt: opt != '', [
                       request.form['option1'], request.form['option2'], request.form['option3']]))
        user.signIn2(spes, options)

        session.pop('idInscri')
        session['id'] = user['id']
        session['pseudo'] = user['pseudo']
        session['couleur'] = user['couleur']
        session['theme'] = user['theme']
        session['type'] = user['type']
        session['cacheRandomKey'] = app.config['cacheRandomKey']
        return redirect(url_for('tuto'))
    else:
        session['cacheRandomKey'] = app.config['cacheRandomKey']
        user = User.get(filter="cls.id == session['idInscri']", limit=1)
        return render_template('inscription2.html', user=user)


def logout():
    session.clear()
    return redirect(url_for('login'))
