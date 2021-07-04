from flask import Flask, render_template, request, redirect, session, url_for, abort, escape
from datetime import *
from flask.json import jsonify
from bson.objectid import ObjectId
from difflib import SequenceMatcher
from db_poo import *
from routing.functions import listeModeration, automoderation, clientsNotif
from math import exp

def removeAccents(txt):
    withAccents = u"àâçéèêëîïôùûüÿ"
    withoutAccents = u"aaceeeeiiouuuy"
    s = ""

    for c in txt:
        i = withAccents.find(c)
        s += withoutAccents[i] if i>=0 else c

    # s = s.replace("'","&#39;")
    return s

def is_relevant(demande, search):
    search = removeAccents(search)
    isRelevant = False
    titre = demande['titre']
    contenu = demande['contenu']

    for keyword in search.split():
        # Titre :
        for w in demande['titre'].split():
            # Occurence pleine :
            if removeAccents(w.lower()) == keyword:
                isRelevant = True
                titre = titre.replace(w,'<mark>{}</mark>'.format(w))
            # Occurence partielle
            elif SequenceMatcher(None, keyword, removeAccents(w.lower())).ratio()>0.8:
                isRelevant = True
                titre = titre.replace(w,'<mark>{}</mark>'.format(w))

        # Contenu :
        for w in demande['contenu'].split():
            # Occurence pleine :
            if removeAccents(w.lower()) == keyword:
                isRelevant = True
                contenu = contenu.replace(w,'<mark>{}</mark>'.format(w))
            # Occurence partielle
            elif SequenceMatcher(None, keyword, removeAccents(w.lower())).ratio()>0.8:
                isRelevant = True
                contenu = contenu.replace(w,'<mark>{}</mark>'.format(w))

    return {'isRelevant': isRelevant, 'titre': titre, 'contenu': contenu}


def recherche():
    global utilisateurs
    global demandes_aide

    if 'id' in session:
        if 'search' in request.args and not request.args['search'] == '':
            search = request.args['search'].lower()

            user = utilisateurs[session['id']].toDict()

            # on récupère les demandes d'aide correspondant à la recherche
            result = []
            for _d in demandes_aide.values():
                d = _d.toDict().copy()
                occurences = is_relevant(d, search)

                if occurences['isRelevant']:
                    d['titre'] = occurences['titre']
                    d['contenu'] = occurences['contenu']
                    result.append(d)

            result = sorted(result, key = lambda d: ( SequenceMatcher(None, d['titre'].lower(), search).ratio() + SequenceMatcher(None, d['contenu'].lower(), search).ratio() ), reverse=True)[:10]

            """result = sorted(
                [d.toDict() for d in demandes_aide.values()
                    if d.matiere in user['matieres'] and is_relevant(d, search)
                ], key = lambda d: ( SequenceMatcher(None, d['titre'].lower(), search).ratio() + SequenceMatcher(None, d['contenu'].lower(), search).ratio()), reverse=True
            )[:10]"""

            # on récupère 3 utilisateurs correspondants à la recherche
            users = sorted(
                [u.toDict() for u in utilisateurs.values()
                    if SequenceMatcher(None, u.pseudo.lower(), search).ratio()>0.7 or SequenceMatcher(None, u.nom.lower(), search).ratio()>0.7 or SequenceMatcher(None, u.prenom.lower(), search).ratio()>0.7 or SequenceMatcher(None, u.lycee.lower(), search).ratio()>0.7
                        or ( 'email' in u.elementPublic and SequenceMatcher(None, u.email.lower(), search).ratio()>0.5 ) or ( 'telephone' in u.elementPublic and SequenceMatcher(None, u.telephone.lower(), search).ratio()>0.5 )
                ], key = lambda u: SequenceMatcher(None, u['pseudo'].lower(), search).ratio() + SequenceMatcher(None, u['nom'].lower(), search).ratio() + SequenceMatcher(None, u['prenom'].lower(), search).ratio() + \
                        SequenceMatcher(None, u['lycee'].lower(), search).ratio() + SequenceMatcher(None, u['email'].lower(), search).ratio() + SequenceMatcher(None, u['telephone'].lower(), search).ratio()
            )[:3]

            return render_template('recherche.html', results=result, users=users, search=search, user=user)

        else:
            return redirect(url_for('accueil'))
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

def recherche_user():
    global utilisateurs

    if 'id' in session:
        search = request.args['search'].lower()

        # on récupère 10 utilisateurs correspondants à la recherche
        users = sorted(
            [u.toDict() for u in utilisateurs.values()
                if SequenceMatcher(None, u.pseudo.lower(), search).ratio()>0.7 or SequenceMatcher(None, u.nom.lower(), search).ratio()>0.7 or SequenceMatcher(None, u.prenom.lower(), search).ratio()>0.7 or SequenceMatcher(None, u.lycee.lower(), search).ratio()>0.7
                    or ( 'email' in u.elementPublic and SequenceMatcher(None, u.email.lower(), search).ratio()>0.5 ) or ( 'telephone' in u.elementPublic and SequenceMatcher(None, u.telephone.lower(), search).ratio()>0.5 )
            ], key = lambda u: SequenceMatcher(None, u['pseudo'].lower(), search).ratio() + SequenceMatcher(None, u['nom'].lower(), search).ratio() + SequenceMatcher(None, u['prenom'].lower(), search).ratio() + \
                    SequenceMatcher(None, u['lycee'].lower(), search).ratio() + SequenceMatcher(None, u['email'].lower(), search).ratio() + SequenceMatcher(None, u['telephone'].lower(), search).ratio()
        )[:10]

        return render_template('rechercheUser.html', users=users, user = utilisateurs[session['id']].toDict(), search=search)
    else:
        session['redirect'] = request.path
        return redirect(url_for('login'))

def morePost():
    global utilisateurs
    global demandes_aide

    if 'id' in session:
        user = utilisateurs[session['id']].toDict()
        lastPost = int(request.form['lastPost'])

        if request.form['search'] == '':
            # ici on récupère les 10 dernières demandes les plus récentes non résolues corresppondant aux matières de l'utilisateur
            demandes = demandes = sorted([d.toDict() for d in demandes_aide.values() if d.matiere in user['matieres'] and not d.resolu and not d.id_utilisateur == ObjectId(session['id'])],
                        key = lambda d: exp(2 * len(d['likes'])) / exp(len(d['réponses associées'])), reverse=True)[lastPost:lastPost+10]

        else:
            search = request.form['search'].lower()
            demandes = sorted(
                [d.toDict() for d in demandes_aide.values()
                    if d.matiere in user['matieres'] and is_relevant(d, search)
                ], key = lambda d: ( SequenceMatcher(None, d['titre'].lower(), search).ratio() + SequenceMatcher(None, d['contenu'].lower(), search).ratio()), reverse=True
            )[lastPost:lastPost+10]

        html = ''
        for demande in demandes:
            html += render_template("publication.html", d=demande, user=user)

        if len(demandes) > 0:
            lastPost += len(demandes)

        return {'html': html, 'lastPost': lastPost}

    else:
        abort(401) # non connecté

def moreUser():
    global utilisateurs
    if 'id' in session:
        lastPost = int(request.form['lastPost'])
        search = request.form['search'].lower()

        # on récupère 10 utilisateurs correspondants à la recherche
        users = sorted(
            [u.toDict() for u in utilisateurs.values()
                if SequenceMatcher(None, u.pseudo.lower(), search).ratio()>0.7 or SequenceMatcher(None, u.nom.lower(), search).ratio()>0.7 or SequenceMatcher(None, u.prenom.lower(), search).ratio()>0.7 or SequenceMatcher(None, u.lycee.lower(), search).ratio()>0.7
                    or ( 'email' in u.elementPublic and SequenceMatcher(None, u.email.lower(), search).ratio()>0.5 ) or ( 'telephone' in u.elementPublic and SequenceMatcher(None, u.telephone.lower(), search).ratio()>0.5 )
            ], key = lambda u: SequenceMatcher(None, u['pseudo'].lower(), search).ratio() + SequenceMatcher(None, u['nom'].lower(), search).ratio() + SequenceMatcher(None, u['prenom'].lower(), search).ratio() + \
                    SequenceMatcher(None, u['lycee'].lower(), search).ratio() + SequenceMatcher(None, u['email'].lower(), search).ratio() + SequenceMatcher(None, u['telephone'].lower(), search).ratio()
        )[lastPost:lastPost+10]

        html = ''
        for user in users:
            html += render_template("apercu_profil.html", u=user, user=utilisateurs[session['id']].toDict())

        if len (users) > 0:
            lastPost += len(users)

        return {'html': html, 'lastPost': lastPost}
    else:
        abort(401) # non connecté
