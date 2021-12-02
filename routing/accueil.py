from flask import Flask, render_template, request, redirect, session, url_for, abort, escape
from datetime import *
from flask.json import jsonify
from db_poo import *
from routing.functions import listeModeration, automoderation
from math import exp


@db_session
def accueil():
    if 'id' in session:
        user = User.get(filter="cls.id == session['id']", limit=1)
        # subjects = getUserSubjects(user)
        # ici on récupère les 10 dernières demandes les plus récentes non résolues corresppondant aux matières de l'utilisateur
        demandes = sorted(Request.get(filter="(cls.matiere.in_(user['matieres'])) & (cls.resolu == False) & (cls.id_utilisateur != session['id'])"), key=lambda d: exp(
            2 * d['nb_likes']) / exp(d['nb_comment']), reverse=True)[:10]

        return render_template("index.html", demandes=demandes, user=user)
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))


@db_session
def tuto():
    if 'id' in session:
        return render_template('tuto.html', user=User.get(filter="cls.id == session['id']", limit=1))
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))


@db_session
def XP_tuto():
    if 'id' in session:
        user = User.get(filter="cls.id == session['id']", limit=1)

        return render_template('XP_tuto.html', user=user)
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))


def mail_rendu():
    return render_template('mail_final.html')


@db_session
def saved():
    if 'id' in session:

        user = User.get(filter="cls.id == session['id']", limit=1)
        # subjects = getUserSubjects(user)
        # ici on récupère les 10 dernières demandes les plus récentes non résolues corresppondant aux matières de l'utilisateur
        demandes = sorted(Request.get(
            filter="cls.id.in_(user['savedDemands'])"), key=lambda d: d['nb_comment'] + d['nb_likes'], reverse=True)

        return render_template("saved.html", demandes=demandes, user=user)
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))


def about():
    return render_template('about.html')

def leaderboard():
    if 'id' in session:
        user = User.get(filter="cls.id == session['id']", limit=1)
        users = User.get(order_by="cls.xp", desc=True, limit=50)
        return render_template("leaderboard.html", users=users, user=user)
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))
