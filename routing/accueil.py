from flask import Flask, current_app as app, render_template, request, redirect, session, url_for, abort, escape
from datetime import *
from flask.json import jsonify
from db_poo import *
from routing.functions import listeModeration, automoderation
from math import exp


@db_session
@login_required()
def accueil():
    user = User.get(filter="cls.id == session['id']", limit=1)
    # subjects = getUserSubjects(user)
    # ici on récupère les 10 dernières demandes les plus récentes non résolues corresppondant aux matières de l'utilisateur
    demandes = sorted(Request.get(filter="(cls.matiere.in_(user['matieres'])) & (cls.resolu == False) & (cls.id_utilisateur != session['id'])"), key=lambda d: exp(
        2 * d['nb_likes']) / exp(d['nb_comment']), reverse=True)[:10]

    return render_template("index.html", demandes=demandes, user=user)


@db_session
@login_required()
def tuto():
    return render_template('tuto.html', user=User.get(filter="cls.id == session['id']", limit=1))


@db_session
@login_required()
def XP_tuto():
    user = User.get(filter="cls.id == session['id']", limit=1)

    return render_template('XP_tuto.html', user=user)


def mail_rendu():
    return render_template('mail_final.html')


@db_session
@login_required()
def saved():
    user = User.get(filter="cls.id == session['id']", limit=1)
    # subjects = getUserSubjects(user)
    # ici on récupère les 10 dernières demandes les plus récentes non résolues corresppondant aux matières de l'utilisateur
    demandes = sorted(Request.get(
        filter="cls.id.in_(user['savedDemands'])"), key=lambda d: d['nb_comment'] + d['nb_likes'], reverse=True)

    return render_template("saved.html", demandes=demandes, user=user)


def about():
    return render_template('about.html')


@db_session
@login_required(ajax=True)
def leaderboard(top, widget):
    user = User.get(filter="cls.id == session['id']", limit=1)

    topFilter = {'france': None,
                 'departement': "User.lyceeId.like(f\"{user['lyceeId'][0:3]}%\")",
                 'lycee': "User.lyceeId == user['lyceeId']"}
    if top not in topFilter:
        top = 'france'
    filtre = topFilter[top]

    users = User.get(filter=filtre, order_by="cls.xp", desc=True, limit=50)

    if user not in users:
        before, user['rank'], after = user.getRank(filtre, True)
        before = list(filter(lambda user: user['id'] not in [user['id'] for user in users], before))
    else:
        del user['rank']
        before, after = [], []
    if widget:
        return render_template("widget_leaderboard.html", users=users, user=user, top=top, before=before, after=after)

    return render_template("leaderboard.html", users=users, user=user, top=top, before=before, after=after)
