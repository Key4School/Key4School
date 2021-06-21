from flask import Flask, render_template, request, redirect, session, url_for, abort, escape
from datetime import *
from flask.json import jsonify
from bson.objectid import ObjectId
from db_poo import *
from routing.functions import recupLevel, addXP, addXpModeration, listeModeration, automoderation, sendNotif, clientsNotif

def accueil():
    global utilisateurs
    global demandes_aide

    if 'id' in session:
        user = utilisateurs[session['id']].toDict()
        # subjects = getUserSubjects(user)
        # ici on récupère les 10 dernières demandes les plus récentes non résolues corresppondant aux matières de l'utilisateur
        demandes = sorted([d.toDict() for d in demandes_aide.values() if d.matiere in user['matieres'] and not d.resolu and not d.id_utilisateur == ObjectId(session['id'])], key = lambda d: ( len(d['réponses associées']) + len(d['likes']) ), reverse=True)[:10]

        return render_template("index.html", demandes=demandes, user=user)
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

def accueil2():
    if 'id' in session:
        return redirect(url_for('accueil'))
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))