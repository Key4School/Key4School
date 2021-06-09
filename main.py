from flask import Flask, render_template, request, redirect, session, url_for, abort
from flask_pymongo import PyMongo
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from datetime import *
from requests_oauthlib import OAuth2Session
from flask_session import Session
from flask.json import jsonify
from bson.objectid import ObjectId
from flask import escape
from bson import Binary
import os
import gridfs
import smtplib, ssl

# Création de l'application
app = Flask(__name__)
socketio = SocketIO(app)


# Récupération d'une base de données
cluster = PyMongo(app, "mongodb+srv://CTLadmin:ctlADMIN@ctlbdd.etzx9.mongodb.net/CTLBDD?retryWrites=true&w=majority")
# Voici deux exemples pour créer des BDD
db_utilisateurs = cluster.db.utilisateurs
db_demande_aide = cluster.db.demande_aide
db_messages = cluster.db.messages
db_groupes = cluster.db.groupes
db_files = cluster.db.fs.files
db_chunks = cluster.db.fs.chunks
db_notif = cluster.db.notifications


def recupLevel():
    xpgens = db_utilisateurs.find_one({'_id': ObjectId(session['id'])})['xp']
    niv = int(0.473*xpgens**0.615)
    xplvl = int((0.473*xpgens**0.615-niv)*100)
    return niv, xplvl, xpgens

def addXP(user: ObjectId, amount: int) -> None:
    """
        +10 pour une demande d’aide
        +15 pour une réponse
        +2 pour chaque like reçu
    """

    db_utilisateurs.update_one(
        {'_id': user},
        {'$inc': {'xp': amount}}
    )

    return

def notif(type, id_groupe, id_msg, destinataires):
    db_notif.insert_one({"type": type, "id_groupe": id_groupe, "id_msg": id_msg,
                        "date": datetime.now(), "destinataires": destinataires})
    # # on rentre les renseignements pris sur le site du fournisseur
    # smtp_adress = 'smtp.gmail.com'
    # smtp_port = 465
    # # on rentre les informations sur notre adresse e-mail
    # email_adress = 'example@gmail.com'
    # email_password = 'my_password'
    # # on crée la connexion
    # context = ssl.create_default_context()
    # with smtplib.SMTP_SSL(smtp_address, smtp_port, context=context) as server:
    #     # connexion au compte
    #     server.login(email_adress, email_password)
    #     for destinataire in destinataires:
    #         if str(destinataire)==session['id']:
    #             user = db_utilisateurs.find_one({"_id": destinataire})
    #             if user['email'] != "":
    #                 # envoi du mail
    #                 server.sendmail(email_address, user['email'], 'le contenu de l\'e-mail')



# Quand on arrive sur le site, on affiche la page "ma_page.html"
@app.route('/')
def accueil():
    if 'id' in session:
        user = db_utilisateurs.find_one({"_id":ObjectId(session['id'])})
        subjects = getUserSubjects(user)

        toutesDemandes = db_demande_aide.aggregate([
            {'$match': {'matière': {'$in': subjects}}},
            {'$match': {'resolu': False}},
            {'$sort': {'date-envoi': -1}},
            {'$limit': 10}
        ])  # ici on récupère les 10 dernières demandes les plus récentes non résolues corresppondant aux matières de l'utilisateur

        demandes = []
        for a in toutesDemandes:  # pour chaque demande, on va l'ajouter dans une liste qui sera donnée à la page HTML
            # on convertit en nombre de secondes la durée depuis le post
            diffTemps = int((datetime.now() - a['date-envoi']).total_seconds())
            tempsStr = convertTime(diffTemps)

            # on check si l'utilisateur a déjà liké le post
            if session['id'] in a['likes']:
                a_like = True
            else:
                a_like = False

            if ObjectId(session['id']) in a['sign']:
                a_sign = True
            else:
                a_sign = False

            demandes.append({  # on ajoute à la liste ce qui nous interesse
                'idMsg': a['_id'],
                'idAuteur': a['id-utilisateur'],
                'titre': a['titre'],
                'contenu': a['contenu'],
                'temps': tempsStr,
                'tag-matière': a['matière'],
                'matière': translate_matiere_spes_options_lv([a['matière']]),
                'nb-likes': len(a['likes']),
                'a_like': a_like,
                'a_sign': a_sign,
                'resolu': a['resolu'],
                # on récupère en plus l'utilisateur pour prochainement afficher son nom/prenom/pseudo
                'user': db_utilisateurs.find_one({'_id': ObjectId(a['id-utilisateur'])})
            })

        return render_template("index.html", demandes=demandes, user=user)
    else:
        return redirect(url_for('login'))


# laisser le nom entre deux slash ca permet d'accepter toutes les urls du style http://127.0.0.1:3000/messages/ sinon ca marche pas.s
@app.route('/accueil/')
def accueil2():
    if 'id' in session:
        return redirect(url_for('accueil'))
    else:
        return redirect(url_for('login'))


@app.route('/messages/', defaults={'idGroupe': None}, methods=['POST', 'GET'])
@app.route('/messages/<idGroupe>', methods=['POST', 'GET'])
def messages(idGroupe):
    if 'id' in session:
        if request.method == 'GET':
            # il faudra récupérer l'id qui sera qans un cookie
            grp = db_groupes.find({"id-utilisateurs": ObjectId(session['id'])})

            users = db_utilisateurs.aggregate([
                {'$sort': {'pseudo': 1}},
                {'$project': {
                    '_id': 1,
                    'nom': 1,
                    'prenom': 1,
                    'pseudo': 1,
                    'lycee': 1,
                    'email': 1,
                    'telephone': 1,
                    'elementPrive': 1
                }}
            ])

            if idGroupe != None:
                msgDb = db_messages.aggregate([
                    {'$match': {'id-groupe': ObjectId(idGroupe)}},
                    {'$lookup':
                        {
                            'from': 'messages',
                            'localField': 'reponse',
                            'foreignField': '_id',
                            'as': 'rep',
                        }
                    }, {'$set': {'rep': {'$arrayElemAt': ["$rep", 0]}}},
                    {'$project': {
                        '_id': 1,
                        'id-groupes': 1,
                        'id-utilisateur': 1,
                        'contenu': 1,
                        'date-envoi': 1,
                        'rep': 1,
                        'audio': 1,
                        'sign': 1
                    }},
                ])
                infogroupes = db_groupes.find_one({"_id": ObjectId(idGroupe)})
                infoUtilisateurs = []
                for content in infogroupes['id-utilisateurs']:
                    infoUtilisateurs += db_utilisateurs.find({"_id": ObjectId(content)})
                if session['id'] in str(infoUtilisateurs):
                    danslegroupe = True
                else:
                    danslegroupe = False
                    msgDb = None
                    infogroupes = None
                    infoUtilisateurs = None
            else:
                msgDb = None
                infogroupes = None
                infoUtilisateurs = None
            return render_template("messages.html", msgDb=msgDb, grpUtilisateur=grp, idgroupe=idGroupe, infogroupe=infogroupes, infoUtilisateurs=infoUtilisateurs, users=users, sessionId=ObjectId(session['id']), user=db_utilisateurs.find_one({"_id":ObjectId(session['id'])}))

        elif request.method == 'POST':
            if request.form['reponse'] != "None":
                reponse = ObjectId(request.form['reponse'])
            else:
                reponse = "None"

            if request.form['contenuMessage'] == '':
                return abort(500)

            message = db_messages.insert_one({"id-groupe": ObjectId(request.form['group']), "id-utilisateur": ObjectId(session['id']),
                                              "contenu": request.form['contenuMessage'], "date-envoi": datetime.now(), "reponse": reponse, "sign": []})
            infogroupes = db_groupes.find_one({"_id": ObjectId(request.form['group'])})
            notif("msg", ObjectId(request.form['group']), ObjectId(message.inserted_id), infogroupes['id-utilisateurs'])

            # Sending new message to connected users
            # json = {'_id': message.inserted_id, 'id-groupe': request.form['group'], 'id-utilisateur': session['id'], 'contenu': request.form['contenuMessage'], 'date-envoi': datetime.now()}
            #request.sid = request.cookies.get('session')
            # emit('newMsg', json, to=idGroupe, namespace='/')

            return 'sent'
    else:
        return redirect(url_for('login'))

# Connection au groupe pour recevoir les nouveaux messages par la suite
@socketio.on('connectToGroup')
def handleEvent_connectToGroup(json):
    if 'id' in session:
        print(request.sid)
        if 'room' in json:
            if json['room'] != 'None':
                # Check authorized
                grp = db_groupes.find_one({'_id': ObjectId(json['room'])})
                if grp != None:
                    if session['id'] in str(grp['id-utilisateurs']): # authorized
                        join_room(json['room'])


@socketio.on('postMsg')
def handleEvent_postMsg(json):
    if 'id' in session:
        if 'room' in json:
            room = json['room']
            # Check authorized
            grp = db_groupes.find_one({'_id': ObjectId(json['room'])})
            if grp != None:
                if session['id'] in str(grp['id-utilisateurs']): # authorized
                    if json['reponse'] != "None":
                        reponse = ObjectId(json['reponse'])
                    else:
                        reponse = "None"

                    if not json['contenuMessage'] == '':
                        message = db_messages.insert_one({"id-groupe": ObjectId(json['group']), "id-utilisateur": ObjectId(session['id']),
                                                          "contenu": json['contenuMessage'], "date-envoi": datetime.now(), "reponse": reponse, "sign": []})
                        infogroupes = db_groupes.find_one({"_id": ObjectId(json['group'])})
                        notif("msg", ObjectId(json['group']), ObjectId(message.inserted_id), infogroupes['id-utilisateurs'])
                        infoUtilisateurs = []
                        for content in infogroupes['id-utilisateurs']:
                            infoUtilisateurs += db_utilisateurs.find({"_id": ObjectId(content)})
                        # Sending new message to connected users
                        message = list(db_messages.aggregate([
                            {'$match': {'_id' : message.inserted_id}},
                            {'$lookup':
                                {
                                    'from': 'messages',
                                    'localField': 'reponse',
                                    'foreignField': '_id',
                                    'as': 'rep',
                                }
                            }, {'$set': {'rep': {'$arrayElemAt': ["$rep", 0]}}},
                            {'$project': {
                                '_id': 1,
                                'id-groupes': 1,
                                'id-utilisateur': 1,
                                'contenu': 1,
                                'date-envoi': 1,
                                'rep': 1,
                                'audio': 1
                            }},
                        ]))[0]
                        html = render_template("refreshMessages.html", msg=message, sessionId=ObjectId(session['id']), infoUtilisateurs=infoUtilisateurs, idgroupe=json['group'])
                        emit('newMsg', html, to=room)

@app.route('/uploadAudio/', methods=['POST'])
def uploadAudio():
    if 'id' in session:
        heure = str(datetime.now())
        nom = "MsgVocal" + \
            request.form['group'] + session['id'] + heure
        cluster.save_file(nom, request.files['audio'])
        db_messages.insert_one({"id-groupe": ObjectId(request.form['group']), "id-utilisateur": ObjectId(session['id']),
                                    "contenu": nom, "date-envoi": datetime.now(), "audio": True, "reponse": ""})
        return 'yes'
    else:
        return redirect(url_for('login'))


@app.route('/audio/<audioName>')
def audio(audioName):
    if 'id' in session:
        return cluster.send_file(audioName)
    else:
        return redirect(url_for('login'))


@app.route('/suppressionMsg/', methods=['POST'])
def supprimerMsg():
    if 'id' in session:
        idGroupe = request.form['grp']
        db_messages.delete_one({"_id": ObjectId(request.form['msgSuppr'])})
        if request.form['audio'] == 'True':
            MyAudio = db_files.find_one({'filename': request.form['audioName']})
            db_files.delete_one({'_id': MyAudio['_id']})
            db_chunks.delete_many({'files_id': MyAudio['_id']})
        return redirect(url_for('messages', idGroupe=idGroupe))

    else:
        return redirect(url_for('login'))


@app.route('/searchUser_newgroup/', methods=['POST'])
def searchUser_newgroup():
    if 'id' in session:
        search = request.form['search']
        users = db_utilisateurs.find({'$or': [{'pseudo': {'$regex': search, '$options': 'i'}},
                                              {'nom': {
                                                  '$regex': search, '$options': 'i'}},
                                              {'prenom': {
                                                  '$regex': search, '$options': 'i'}},
                                              {'lycee': {
                                                  '$regex': search, '$options': 'i'}},
                                              {'email': {
                                                  '$regex': search, '$options': 'i'}},
                                              {'telephone': {'$regex': search, '$options': 'i'}}]
                                        }).limit(30)
        return render_template("searchUser_newgroup.html", users=users, sessionId=session['id'])
    else:
        return redirect(url_for('login'))


@app.route('/createGroupe/', methods=['POST'])
def createGroupe():
    if 'id' in session:
        participants = [ObjectId(session['id'])]
        for name, value in request.form.items():
            if name == 'nomnewgroupe':
                pass
            else:
                participants.append(ObjectId(name))
        newGroupe = db_groupes.insert_one({'nom': request.form['nomnewgroupe'], 'id-utilisateurs': participants, 'moderateurs': [ObjectId(session['id'])], 'sign':[]})
        return redirect(url_for('messages', idGroupe=newGroupe.inserted_id))
    else:
        return redirect(url_for('login'))


@app.route('/changeTheme/', methods=['POST'])
def changeTheme():
    if 'id' in session:
        db_utilisateurs.update_one({"_id": ObjectId(session['id'])}, {
                                   "$set": {"couleur": ['#e6445f', '#f3a6b3', '#afe2e7', '#f9d3d9']}})
        session['couleur'] = ['#e6445f', '#f3a6b3', '#afe2e7', '#f9d3d9']
        return redirect(url_for('profil'))
    else:
        return redirect(url_for('login'))


@app.route('/profil/', defaults={'idUser': None}, methods=['POST', 'GET'])
@app.route('/profil/<idUser>', methods=['POST', 'GET'])
def profil(idUser):
    if 'id' in session:
        if idUser == None or idUser == session['id']:
            toutesDemandes = db_demande_aide.aggregate([
                {'$match': {'id-utilisateur': ObjectId(session['id'])}},
                {'$sort': {'date-envoi': -1}}
            ])  # ici on récupère les 5 dernières demandes les plus récentes

            demandes = []
            for a in toutesDemandes:  # pour chaque demande, on va l'ajouter dans une liste qui sera donnée à la page HTML
                # on convertit en nombre de secondes la durée depuis le post
                diffTemps = int((datetime.now() - a['date-envoi']).total_seconds())
                tempsStr = convertTime(diffTemps)

                # on check si l'utilisateur a déjà liké le post
                if session['id'] in a['likes']:
                    a_like = True
                else:
                    a_like = False

                if session['id'] in a['sign']:
                    a_sign = True
                else:
                    a_sign = False

                demandes.append({  # on ajoute à la liste ce qui nous interesse
                    'idMsg': a['_id'],
                    'titre': a['titre'],
                    'contenu': a['contenu'],
                    'temps': tempsStr,
                    'matière': a['matière'],
                    'nb-likes': len(a['likes']),
                    'a_like': a_like,
                    'a_sign': a_sign,
                    'resolu': a['resolu'],
                    # on récupère en plus l'utilisateur pour prochainement afficher son nom/prenom/pseudo
                    'user': db_utilisateurs.find_one({'_id': ObjectId(a['id-utilisateur'])})
                })

            profilUtilisateur = db_utilisateurs.find_one({'_id': ObjectId(session['id'])})
            niv, xplvl, xpgens = recupLevel()
            return render_template("profil.html", profilUtilisateur=profilUtilisateur, demandes=demandes, xplvl=xplvl, xp=xpgens, niv=niv, user=db_utilisateurs.find_one({"_id": ObjectId(session['id'])}))

        else:
            profilUtilisateur = db_utilisateurs.find_one({'_id': ObjectId(idUser)})
            if ObjectId(session['id']) in profilUtilisateur['sign']:
                a_sign = True
            else:
                a_sign = False
            # translate spes/options/lv
            profilUtilisateur['langues'] = translate_matiere_spes_options_lv(profilUtilisateur['langues'])
            profilUtilisateur['spes'] = translate_matiere_spes_options_lv(profilUtilisateur['spes'])
            profilUtilisateur['options'] = translate_matiere_spes_options_lv(profilUtilisateur['options'])

            return render_template("affichProfil.html", profilUtilisateur=profilUtilisateur, a_sign=a_sign, user=db_utilisateurs.find_one({"_id": ObjectId(session['id'])}))
    else:
        return redirect(url_for('login'))


@app.route('/userImg/<profilImg>')
def userImg(profilImg):
    if 'id' in session:
        return cluster.send_file(profilImg)
    else:
        return redirect(url_for('login'))


@app.route("/updateprofile/", methods=["POST"])
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

        # if request.form['pseudoVisibilite'] == "pv":
        #     elementPrive.append("pseudo")
        # elif request.form['pseudoVisibilite'] == "pb":
        #     elementPublic.append("pseudo")
        db_utilisateurs.update_one({"_id": ObjectId(session['id'])}, {'$set': {'pseudo': request.form['pseudo'], 'email': request.form['email'], 'telephone': request.form['telephone'], 'interets': request.form['interets'], 'caractere': request.form['caractere'],
                                                                               'langues': [request.form['lv1'], request.form['lv2']], 'options': [request.form['option1'], request.form['option2']], 'spes': [request.form['spe1'], request.form['spe2'], request.form['spe3']],
                                                                               'elementPrive': elementPrive, 'elementPublic': elementPublic}})
        # requete vers la db update pour ne pas créer un nouvel utilisateur ensuite 1ere partie on spécifie l'id de l'utilisateur qu'on veut modifier  puis pour chaque champ on précise les nouvelles valeurs.
        return redirect(url_for('profil'))
    else:
        return redirect(url_for('login'))


@app.route('/updateImg/', methods=['POST'])
def updateImg():
    if 'id' in session:
        if request.form['but'] == "remove":
            MyImage = db_files.find({'filename': {'$regex': 'imgProfile' + session['id']}})
            for a in MyImage:
                db_files.delete_one({'_id': a['_id']})
                db_chunks.delete_many({'files_id': a['_id']})
            db_utilisateurs.update_one(
                {'_id': ObjectId(session['id'])},
                {'$set': {'imgProfile': "", 'nomImg': ""}})
        elif request.form['but'] == "replace":
            ImgNom = request.files['Newpicture'].filename + \
                'imgProfile' + session['id']
            MyImage = db_files.find({'filename': {'$regex': 'imgProfile' + session['id']}})
            for a in MyImage:
                db_files.delete_one({'_id': a['_id']})
                db_chunks.delete_many({'files_id': a['_id']})
            cluster.save_file(ImgNom, request.files['Newpicture'])
            image = db_files.find_one({'filename': ImgNom})
            db_utilisateurs.update_one({'_id': ObjectId(session['id'])}, {
                                       '$set': {'imgProfile': image['_id'], 'nomImg': ImgNom}})
        return redirect(url_for('profil'))
    else:
        return redirect(url_for('login'))


@app.route('/comments/')
def redirect_comments():
    return redirect('/')


@app.route('/comments/<idMsg>', methods=['GET', 'POST'])
def comments(idMsg):
    if 'id' in session:
        if request.method == 'GET':
            msg = db_demande_aide.find_one({'_id': ObjectId(idMsg)})

            diffTemps = int((datetime.now() - msg['date-envoi']).total_seconds())
            tempsStr = convertTime(diffTemps)

            # on check si l'utilisateur a déjà liké le post
            if session['id'] in msg['likes']:
                a_like = True
            else:
                a_like = False

            if session['id'] in msg['sign']:
                a_sign = True
            else:
                a_sign = False

            reponses = []
            for r in msg['réponses associées'].values():
                diffTemps2 = int((datetime.now() - r['date-envoi']).total_seconds())
                tempsStr2 = convertTime(diffTemps2)

                # on check si l'utilisateur a déjà liké le post
                if session['id'] in r['likes']:
                    a_like2 = True
                else:
                    a_like2 = False

                reponses.append({
                    'idRep': r['_id'],
                    'contenu': r['contenu'],
                    'temps': tempsStr2,
                    'nb-likes': len(r['likes']),
                    'a_like': a_like2,
                    'user': db_utilisateurs.find_one({'_id': ObjectId(r['id-utilisateur'])})
                })

            result = { # on ajoute à la liste ce qui nous interesse
                'idMsg': msg['_id'],
                'titre': msg['titre'],
                'contenu': msg['contenu'],
                'temps': tempsStr,
                'tag-matière': msg['matière'],
                'matière': translate_matiere_spes_options_lv([msg['matière']]),
                'nb-likes': len(msg['likes']),
                'a_like': a_like,
                'a_sign': a_sign,
                'reponses': reponses,
                # on récupère en plus l'utilisateur pour prochainement afficher son nom/prenom/pseudo
                'user': db_utilisateurs.find_one({'_id': ObjectId(msg['id-utilisateur'])})
            }

            return render_template("comments.html", d=result, user=db_utilisateurs.find_one({"_id": ObjectId(session['id'])}))

        else:
            if 'rep' in request.form:
                msg = db_demande_aide.find_one({'_id': ObjectId(idMsg)})
                reponses = msg['réponses associées']
                _id = ObjectId()
                reponses[str(_id)] = {
                    '_id': ObjectId(_id),
                    'id-utilisateur': ObjectId(session['id']),
                    'contenu': request.form.get('rep'),
                    'date-envoi': datetime.now(),
                    'likes': []
                }

                db_demande_aide.update(
                    {'_id': ObjectId(idMsg)},
                    {'$set':{'réponses associées': reponses}}
                )
                notif("demande", ObjectId(idMsg), _id, msg['id-utilisateur'])

                # add XP
                if not ObjectId(session['id']) == msg['id-utilisateur']:
                    addXP(ObjectId(session['id']), 15)

            return redirect('/comments/' + idMsg)
    else:
        return redirect(url_for('login'))


@ app.route('/question/', methods=['POST', 'GET'])
def question():
    if 'id' in session:
        if request.method == 'POST':
            # Impossibilité demande d'aide vide
            if request.form['titre'] == '':
                return redirect('/question/')

            user = db_utilisateurs.find_one({"_id": ObjectId(session['id'])})
            if user['SanctionEnCour'] != "Spec" and user['SanctionEnCour'] != "SpecForum":
                db_demande_aide.insert_one(
                    {"id-utilisateur": ObjectId(session['id']), "titre": request.form['titre'], "contenu": request.form['demande'], "date-envoi": datetime.now(), "matière": request.form['matiere'], "réponses associées": {}, "likes": [], "sign": [], "resolu": False})

                demandes = db_demande_aide.aggregate([
                    {'$sort': {'date-envoi': -1}},
                    {'$limit': 1}
                ])

                # add XP
                addXP(ObjectId(session['id']), 10)

                for demande in demandes:
                    return redirect('/comments/' + str(demande['_id']))
            else:
                return redirect(url_for('accueil'))

            # return render_template('question.html', envoi="Envoi réussi")
        else:
            profilUtilisateur = db_utilisateurs.find_one({'_id': ObjectId(session['id'])})

            if profilUtilisateur["SanctionEnCour"] != "Spec" and profilUtilisateur['SanctionEnCour'] != "SpecForum":
                return render_template('question.html', profilUtilisateur=profilUtilisateur, user=db_utilisateurs.find_one({"_id": ObjectId(session['id'])}))
            else:
                return redirect(url_for('accueil'))
    else:
        return redirect(url_for('login'))


@ app.route('/recherche')
def recherche():
    if 'id' in session:
        if 'search' in request.args and not request.args['search'] == '':
            search = request.args['search']

            user = db_utilisateurs.find_one({"_id":ObjectId(session['id'])})
            subjects = getUserSubjects(user)

            firstResult = db_demande_aide.aggregate([
                {'$match': {'$text': {'$search': search}}}, # doit resté en premier !
                {'$match': {'matière': {'$in': subjects}}},
                {'$sort': {'date-envoi': -1}}
            ]) # ici on récupère les demandes d'aide correspondant à la recherche et aux matières de l'utilisateur

            result = []
            for a in firstResult: # pour chaque résultat, on va l'ajouter dans une liste qui sera donnée à la page HTML
                # on convertit en nombre de secondes la durée depuis le post
                diffTemps = int((datetime.now() - a['date-envoi']).total_seconds())
                tempsStr = convertTime(diffTemps)

                # on check si l'utilisateur a déjà liké le post
                if session['id'] in a['likes']:
                    a_like = True
                else:
                    a_like = False

                if session['id'] in a['sign']:
                    a_sign = True
                else:
                    a_sign = False

                result.append({ # on ajoute à la liste ce qui nous interesse
                    'idMsg': a['_id'],
                    'idAuteur': a['id-utilisateur'],
                    'titre': a['titre'],
                    'contenu': a['contenu'],
                    'temps': tempsStr,
                    'tag-matière': a['matière'],
                    'matière': translate_matiere_spes_options_lv([a['matière']]),
                    'nb-likes': len(a['likes']),
                    'a_like': a_like,
                    'a_sign': a_sign,
                    'resolu': a['resolu'],
                    # on récupère en plus l'utilisateur pour prochainement afficher son nom/prenom/pseudo
                    'user': db_utilisateurs.find_one({'_id': ObjectId(a['id-utilisateur'])})
                })

            users = db_utilisateurs.find({'$or': [{'pseudo': {'$regex': search, '$options': 'i'}},
                                                  {'nom': {'$regex': search, '$options': 'i'}},
                                                  {'prenom': {'$regex': search, '$options': 'i'}},
                                                  {'lycee': {'$regex': search, '$options': 'i'}},
                                                  {'email': {'$regex': search, '$options': 'i'}},
                                                  {'telephone': {'$regex': search, '$options': 'i'}}]
                                            }).limit(3)

            return render_template('recherche.html', results=result, users=users, search=search, user=user)

        else:
            return redirect(url_for('accueil'))
    else:
        return redirect(url_for('login'))


@ app.route('/rechercheUser')
def recherche_user():
    if 'id' in session:
        search = request.args['search']
        users = db_utilisateurs.find({'$or': [{'pseudo': {'$regex': search, '$options': 'i'}},
                                              {'nom': {'$regex': search, '$options': 'i'}},
                                              {'prenom': {'$regex': search, '$options': 'i'}},
                                              {'lycee': {'$regex': search, '$options': 'i'}},
                                              {'email': {'$regex': search, '$options': 'i'}},
                                              {'telephone': {'$regex': search, '$options': 'i'}}]
                                        }).limit(30)
        return render_template('rechercheUser.html', users=users)
    else:
        return redirect(url_for('login'))


@ app.route('/likePost/<idPost>', methods=['POST'])
def likePost(idPost):
    if 'id' in session:
        if 'idPost' != None:
            # on récupère les likes de la demande d'aide
            demande = db_demande_aide.find_one({"_id": ObjectId(idPost)})
            likes = demande['likes']
            newLikes = list(likes)

            # on check mtn si l'utilisateur a déjà liké la demande
            if session['id'] in likes:
                newLikes.remove(session['id'])  # on supprime son like

                # remove XP
                if not ObjectId(session['id']) == demande['id-utilisateur']:
                    addXP(ObjectId(demande['id-utilisateur']), -2)
            else:
                newLikes.append(session['id'])  # on ajoute son like

                # add XP
                if not ObjectId(session['id']) == demande['id-utilisateur']:
                    addXP(ObjectId(demande['id-utilisateur']), 2)

            # on update dans la DB
            db_demande_aide.update(
                {'_id': ObjectId(idPost)},
                {'$set':{'likes': newLikes}}
            )

            # on retourne enfin le nouveau nb de likes
            return {'newNbLikes': len(newLikes)}, 200

        else:
            abort(403)  # il manque l'id du message
    else:
        abort(401)  # non autorisé


@app.route('/likeRep/<idPost>/<idRep>', methods=['POST'])
def likeRep(idPost, idRep):
    if 'id' in session:
        if 'idPost' != None and 'idRep' != None:
            # on récupère les likes de la demande d'aide
            reponses = db_demande_aide.find_one({"_id": ObjectId(idPost)})['réponses associées']
            if not idRep in reponses:
                return abort(400)

            reponse = reponses[idRep]
            likes = reponse['likes']
            newLikes = list(likes)

            # on check mtn si l'utilisateur a déjà liké la demande
            if session['id'] in likes:
                newLikes.remove(session['id'])  # on supprime son like

                # remove XP
                if not ObjectId(session['id']) == reponse['id-utilisateur']:
                    addXP(ObjectId(reponse['id-utilisateur']), -2)
            else:
                newLikes.append(session['id'])  # on ajoute son like

                # add XP
                if not ObjectId(session['id']) == reponse['id-utilisateur']:
                    addXP(ObjectId(reponse['id-utilisateur']), 2)

            reponse = {
                '_id': ObjectId(reponse['_id']),
                'id-utilisateur': ObjectId(reponse['id-utilisateur']),
                'contenu': reponse['contenu'],
                'date-envoi': reponse['date-envoi'],
                'likes': newLikes
            }
            reponses[idRep] = reponse

            # on update dans la DB
            db_demande_aide.update(
                {'_id': ObjectId(idPost)},
                {'$set':{'réponses associées': reponses}}
            )

            # on retourne enfin le nouveau nb de likes
            return {'newNbLikes': len(newLikes)}, 200

        else:
            abort(400)  # il manque l'id du message
    else:
        abort(401)  # non autorisé


@app.route('/administration/', methods=['POST', 'GET'])
def administration():
    if 'id' in session:
        utilisateur = db_utilisateurs.find_one({"_id": ObjectId(session['id'])})
        if utilisateur['admin'] == True:
            if request.method == 'POST':
                if request.form['demandeBut'] == 'Suppr':
                    db_demande_aide.delete_one({"_id": ObjectId(request.form['idSuppr'])})

                elif request.form['demandeBut'] == 'Val':
                    db_demande_aide.update_one({"_id": ObjectId(request.form['idVal'])},
                                               {"$set": {"sign": [], "motif": []}})
                elif request.form['demandeBut'] == 'ValUser':
                    db_utilisateurs.update_one({"_id": ObjectId(request.form['idValidé'])},
                                               {"$set": {"sign": [],"motif": []}})
                return 'sent'

            else:
                demandeSignale = db_demande_aide.aggregate([
                    {'$match': {"sign": {"$exists": "true", "$ne": []}}},
                    {'$lookup':
                        {
                            'from': 'utilisateurs',
                            'localField': 'id-utilisateur',
                            'foreignField': '_id',
                            'as': 'rep',
                        }
                    }, {'$set': {'rep': {'$arrayElemAt': ["$rep", 0]}}},
                    {'$project': {
                        '_id': 1,
                        'titre': 1,
                        'id-utilisateur': 1,
                        'contenu': 1,
                        'date-envoi': 1,
                        'rep': 1,
                        'matière': 1,
                        'motif': 1,
                         'sign_count': {"$size": { "$ifNull": [ "$sign", [] ] } }
                    }},
                    {"$sort": {"sign_count": -1}}
                ])
                profilSignale = db_utilisateurs.aggregate([
                    {'$match': {"sign": {"$exists": "true", "$ne": []}}},
                    {'$project': {
                        '_id': 1,
                        'nom': 1,
                        'prenom': 1,
                        'pseudo' : 1,
                        'motif': 1,
                        'sign_count': {"$size": { "$ifNull": [ "$sign", [] ] } }
                    }},
                    {"$sort": {"sign_count": -1}}
                    ])

                discussionSignale = db_groupes.aggregate([
                    {'$match': {"sign": {"$exists": "true", "$ne": []}}},
                    {'$project': {
                        '_id': 1,
                        'id-utilisateurs': 1,
                        'moderateurs': 1,
                        'nom' : 1,
                        'motif': 1,
                        'sign_count': {"$size": { "$ifNull": [ "$sign", [] ] } }
                    }},
                    {"$sort": {"sign_count": -1}}
                ])

                return render_template('administration.html', user=utilisateur, demandeSignale=demandeSignale, profilSignale=profilSignale, discussionSignale=discussionSignale)
        else:
            return redirect(url_for('accueil'))
    else:
        return redirect(url_for('login'))


@app.route('/sanction/', methods=['POST'])
def sanction():
    if 'id' in session:
        utilisateur = db_utilisateurs.find_one(
            {"_id": ObjectId(session['id'])})
        if utilisateur['admin'] == True:
            db_utilisateurs.update_one({"_id": ObjectId(request.form['idSanctionné'])}, {"$push": {"Sanction": {
                                       "SanctionType": request.form['Sanction'], "SanctionMotif": request.form['Raison'], "SanctionNext": request.form['Next']}}})
            if request.form['SanctionType'] == 'Spec':
                time = datetime.now() + timedelta(days= int(request.form['SanctionDuree']))
                db_utilisateurs.update_one({"_id": ObjectId(request.form['idSanctionné'])}, {
                                           "$set": {"SanctionEnCour": request.form['SanctionType'], "SanctionDuree": time}})
            if request.form['SanctionType']== 'ResetProfil':
                Sanctionné = db_utilisateurs.find_one({"_id": ObjectId(request.form['idSanctionné'])})
                MyImage = db_files.find(
                    {'filename': {'$regex': 'imgProfile' + request.form['idSanctionné']}})
                for a in MyImage:
                    db_files.delete_one({'_id': a['_id']})
                    db_chunks.delete_many({'files_id': a['_id']})
                db_utilisateurs.update_one({'_id': ObjectId(request.form['idSanctionné'])}, {
                                           '$set': {'imgProfile': "", 'nomImg': ""}})
                db_utilisateurs.update_one({"_id": ObjectId(request.form['idSanctionné'])}, {"$set":{"pseudo":  Sanctionné['nom']+"_"+Sanctionné['prenom'], "telephone": "", "interets": "", "email" : "" }})
            if request.form['SanctionType'] == 'SpecProfil':
                time = datetime.now() + timedelta(days= int(request.form['SanctionDuree']))
                db_utilisateurs.update_one({"_id": ObjectId(request.form['idSanctionné'])}, {
                                           "$set": {"SanctionEnCour": request.form['SanctionType'], "SanctionDuree": time}})
            if request.form['SanctionType'] == 'SpecForum':
                time = datetime.now() + timedelta(days= int(request.form['SanctionDuree']))
                db_utilisateurs.update_one({"_id": ObjectId(request.form['idSanctionné'])}, {
                                           "$set": {"SanctionEnCour": request.form['SanctionType'], "SanctionDuree": time}})
            if request.form['SanctionType'] == 'SpecMsg':
                time = datetime.now() + timedelta(days= int(request.form['SanctionDuree']))
                db_utilisateurs.update_one({"_id": ObjectId(request.form['idSanctionné'])}, {
                                           "$set": {"SanctionEnCour": request.form['SanctionType'], "SanctionDuree": time}})
            return 'sent'
        else:
            return redirect(url_for('accueil'))
    else:
        return redirect(url_for('login'))


@app.route('/signPost/', methods=['POST'])
def signPost():
    if 'id' in session:
        if request.form['idSignalé'] != None:
            # on récupère les signalements de la demande d'aide
            demande = db_demande_aide.find_one({"_id": ObjectId(request.form['idSignalé'])})
            sign = demande['sign']
            newSign = list(sign)

            # on check mtn si l'utilisateur a déjà signalé la demande
            if ObjectId(session['id']) in sign:
                # on supprime son signalement
                newSign.remove(ObjectId(session['id']))
                db_demande_aide.update_one(
                    {'_id': ObjectId(request.form['idSignalé'])},
                    {'$pull': {
                        'sign': ObjectId(session['id']),
                        'motif': {'id': ObjectId(session['id'])}}
                    },
                )

            else:
                newSign.append(session['id']) # on ajoute son signalement
                raison = {request.form['Raison']}
                db_demande_aide.update_one(
                    {'_id': ObjectId(request.form['idSignalé'])},
                    {'$push':
                        {'sign': ObjectId(session['id']),
                         'motif': {'id': ObjectId(session['id']), 'txt': request.form['Raison']}}
                    }
                )

            # on update dans la DB
            # db_demande_aide.update_one(
            #     {'_id': ObjectId(request.form['idSignalé'])},
            #     {'$set':
            #         {'sign': newSign}
            #      }
            # )
            return 'sent'

        else:
            abort(403) # il manque l'id du message
    else:
        abort(401) # non autorisé


@app.route('/signPostProfil/', methods=['POST'])
def signPostProfil():
    if 'id' in session:
        if request.form['idSignalé'] != None:
            # on récupère les signalements de la demande d'aide
            user = db_utilisateurs.find_one({"_id": ObjectId(request.form['idSignalé'])})
            sign = user['sign']

            # on check mtn si l'utilisateur a déjà signalé la demande
            if ObjectId(session['id']) in sign:
                db_utilisateurs.update_one(
                    {'_id': ObjectId(request.form['idSignalé'])},
                    {'$pull': {
                        'sign': ObjectId(session['id']),
                        'motif': {'id': ObjectId(session['id'])}}
                    },
                )

            else:
                raison = {request.form['Raison']}
                db_utilisateurs.update_one(
                    {'_id': ObjectId(request.form['idSignalé'])},
                    {'$push':
                        {'sign': ObjectId(session['id']),
                         'motif': {'id': ObjectId(session['id']), 'txt': request.form['Raison']}}
                    }
                )
            return 'sent'

        else:
            abort(403) # il manque l'id du message
    else:
        abort(401) # non autorisé

@app.route('/signPostDiscussion/', methods=['POST'])
def signPostDiscussion():
    if 'id' in session:
        if request.form['idSignalé'] != None:
            # on récupère les signalements de la demande d'aide
            sign = db_groupes.find_one({"_id": ObjectId(request.form['idSignalé'])})['sign']


            # on check mtn si l'utilisateur a déjà signalé la demande
            if ObjectId(session['id']) in sign:
                db_groupes.update_one(
                    {'_id': ObjectId(request.form['idSignalé'])},
                    {'$pull': {
                        'sign': ObjectId(session['id']),
                        'motif': {'id': ObjectId(session['id'])}}
                    },
                )

            else:
                raison = {request.form['Raison']}
                db_groupes.update_one(
                    {'_id': ObjectId(request.form['idSignalé'])},
                    {'$push':
                        {'sign': ObjectId(session['id']),
                         'motif': {'id': ObjectId(session['id']), 'txt': request.form['Raison']}}
                    }
                )
            return 'sent'

        else:
            abort(403) # il manque l'id du message
    else:
        abort(401) # non autorisé

@app.route('/signPostMsg/', methods=['POST'])
def signPostMsg():
    if 'id' in session:
        if request.form['idSignalé'] != None and request.form['idMsgSignalé'] != None:
            # on récupère les signalements de la demande d'aide
            sign = db_groupes.find_one({"_id": ObjectId(request.form['idSignalé'])})['sign']
            signMsg = db_messages.find_one({"_id": ObjectId(request.form['idMsgSignalé'])})['sign']

            # on check mtn si l'utilisateur a déjà signalé la demande
            if ObjectId(session['id']) in signMsg:
                db_messages.update_one(
                    {'_id': ObjectId(request.form['idMsgSignalé'])},
                    {'$pull': {
                        'sign': ObjectId(session['id']),
                        'motif': {'id': ObjectId(session['id'])}}
                    },
                )

            else:
                db_messages.update_one(
                    {'_id': ObjectId(request.form['idMsgSignalé'])},
                    {'$push':
                        {'sign': ObjectId(session['id']),
                         'motif': {'id': ObjectId(session['id']), 'txt': request.form['Raison']}}
                    }
                )
                if not ObjectId(session['id']) in sign:
                    db_groupes.update_one(
                        {'_id': ObjectId(request.form['idSignalé'])},
                        {'$push':
                            {'sign': ObjectId(session['id']),
                             'motif': {'id': ObjectId(session['id']), 'txt': "Message signalé :"+request.form['Raison']}}
                        }
                    )
            return 'sent'

        else:
            abort(403) # il manque l'id du message
    else:
        abort(401) # non autorisé

@app.route('/resoudre/<idPost>', methods=['POST'])
def resoudre(idPost):
    if 'id' in session:
        if 'idPost' != None:
            demande = db_demande_aide.find_one({"_id": ObjectId(idPost)})

            # on check mtn si l'utilisateur a déjà liké la demande
            if demande['id-utilisateur'] == ObjectId(session['id']):
                # on update dans la DB
                db_demande_aide.update(
                    {'_id': ObjectId(idPost)},
                    {'$set':{'resolu': True}}
                )

                return "ok", 200
            else:
                abort(401) # non autorisé


        else:
            abort(403) # il manque l'id du message
    else:
        abort(401) # non autorisé


def convertTime(diffTemps):
    tempsStr = ''
    # puis on se fait chier à trouver le délai entre le poste et aujourd'hui
    if diffTemps // (60 * 60 * 24 * 7): # semaines
        tempsStr += '{}sem '.format(diffTemps // (60 * 60 * 24 * 7))
        if (diffTemps % (60 * 60 * 24 * 7)) // (60 * 60 * 24): # jours
            tempsStr += '{}j '.format((diffTemps % (60 * 60 * 24 * 7)) // (60 * 60 * 24))
    elif diffTemps // (60 * 60 * 24): # jours
        tempsStr += '{}j '.format(diffTemps // (60 * 60 * 24))
        if (diffTemps % (60 * 60 * 24)) // (60 * 60): # heures
            tempsStr += '{}h '.format((diffTemps % (60 * 60 * 24)) // (60 * 60))
    elif diffTemps // (60 * 60):  # heures
        tempsStr += '{}h '.format(diffTemps // (60 * 60))
        if (diffTemps % (60 * 60)) // 60: # minutes
            tempsStr += '{}min '.format(diffTemps % (60 * 60) // 60)
    else:
        tempsStr = '{}min'.format(diffTemps // 60)

    return tempsStr

def getUserSubjects(user):
    subjects = ['hg', 'emc', 'eps']

    # Tronc commun
    if user['classe']=='2GT' or user['classe']=='1G':
        subjects.append('fr')
    if user['classe']=='2GT':
        subjects.append('maths')
        subjects.append('pc')
        subjects.append('ses')
    if user['classe']=='TG':
        subjects.append('philo')
    # Langues
    if 'lv1-ang' in user['langues'] or 'lv1-ang-euro' in user['langues'] or 'lv2-ang' in user['langues'] or 'opt-lv3-ang' in user['options']:
        subjects.append('ang')
    if 'lv1-esp' in user['langues'] or 'lv1-esp-euro' in user['langues'] or 'lv2-esp' in user['langues'] or 'opt-lv3-esp' in user['options']:
        subjects.append('esp')
    if 'lv1-all' in user['langues'] or 'lv1-all-euro' in user['langues'] or 'lv2-all' in user['langues'] or 'opt-lv3-all' in user['options']:
        subjects.append('all')
    if 'lv1-it' in user['langues'] or 'lv1-it-euro' in user['langues'] or 'lv2-it' in user['langues'] or 'opt-lv3-it' in user['options']:
        subjects.append('it')
    if 'lv1-chi' in user['langues'] or 'lv2-chi' in user['langues'] or 'opt-lv3-chi' in user['options']:
        subjects.append('chi')
    if 'lv1-ru' in user['langues'] or 'lv2-ru' in user['langues'] or 'opt-lv3-ru' in user['options']:
        subjects.append('ru')
    if 'lv1-por' in user['langues'] or 'lv2-por' in user['langues'] or 'opt-lv3-por' in user['options']:
        subjects.append('por')
    if 'lv1-ara' in user['langues'] or 'lv2-ara' in user['langues'] or 'opt-lv3-ara' in user['options']:
        subjects.append('ara')
    # Spés + options
    subjects += user['spes']
    subjects += user['options']

    return subjects

def translate_matiere_spes_options_lv(toTranslate: list) -> str:
    translated = ''
    translations = {
        # Matières tronc commun
        'fr': 'Français',
        'maths': 'Mathématiques',
        'hg': 'Histoire-Géographie',
        'snt': 'SNT',
        'emc': 'EMC',
        'ses': 'SES',
        'philo': 'Philosophie',
        'eps': 'EPS',
        # Langues
        'ang': 'Anglais',
        'esp': 'Espagnol',
        'all': 'Allemand',
        'por': 'Portugais',
        'it': 'Italien',
        'chi': 'Chinois',
        'ru': 'Russe',
        'ara': 'Arabe',
        # LV1
        'lv1-ang': 'LV1 Anglais',
        'lv1-ang-euro': 'LV1 Anglais Euro',
        'lv1-esp': 'LV1 Espagnol',
        'lv1-esp-euro': 'LV1 Espagnol Euro',
        'lv1-all': 'LV1 Allemand',
        'lv1-all-euro': 'LV1 Allemand Euro',
        'lv1-por': 'LV1 Portugais',
        'lv1-por-euro': 'LV1 Portugais Euro',
        'lv1-it': 'LV1 Itlien',
        'lv1-it-euro': 'LV1 Itlien Euro',
        'lv1-chi': 'LV1 Chinois',
        'lv1-ru': 'LV1 Russe',
        'lv1-ara': 'LV1 Arabe',
        # LV2
        'lv2-ang': 'LV2 Anglais',
        'lv2-esp': 'LV2 Espagnol',
        'lv2-all': 'LV2 Allemand',
        'lv2-por': 'LV2 Portugais',
        'lv2-it': 'LV2 Italien',
        'lv2-chi': 'LV2 Chinois',
        'lv2-ru': 'LV2 Russe',
        'lv2-ara': 'LV2 Arabe',
        # Spés
        'spe-art': 'Spé Arts',
        'spe-hggsp': 'Spé HGGSP',
        'spe-hlp': 'Spé HLP',
        'spe-ses': 'Spé SES',
        'spe-maths': 'Spé Mathématiques',
        'spe-pc': 'Spé Physique-Chimie',
        'spe-svt': 'Spé SVT',
        'spe-nsi': 'Spé NSI',
        'spe-si': 'Spé Sciences de l\'Ingénieur',
        'spe-lca': 'Spé LCA',
        'spe-llcer-ang': 'Spé LLCER Anglais',
        'spe-llcer-esp': 'Spé LLCER Espagnol',
        'spe-llcer-all': 'Spé LLCER Allemand',
        'spe-llcer-it': 'Spé LLCER Italien',
        'spe-bio-eco': 'Spé Biologie-écologie',
        # Options
        'opt-lca-latin': 'LCA Latin',
        'opt-lca-grec': 'LCA Grec',
        'opt-lv3-ang': 'LV3 Anglais',
        'opt-lv3-esp': 'LV3 Espagnol',
        'opt-lv3-all': 'LV3 Allemand',
        'opt-lv3-por': 'LV3 Portugais',
        'opt-lv3-it': 'LV3 Italien',
        'opt-lv3-ru': 'LV3 Russe',
        'opt-lv3-ara': 'LV3 Arabe',
        'opt-lv3-chi': 'LV3 Chinois',
        'opt-eps': 'Option EPS',
        'opt-arts': 'Option Arts',
        'opt-musique': 'Option Musique',
        'opt-mg': 'Option Management et Gestion',
        'opt-ss': 'Option Santé et Social',
        'opt-biotech': 'Option Biotechnologies',
        'opt-sl': 'Option Sciences et laboratoire',
        'opt-si': 'Option Sciences de l\'Ingénieur',
        'opt-cit': 'Option Création et culture technologiques',
        'opt-ccd': 'Option Création et culture - design',
        'opt-equit': 'Option Hippologie et équitation',
        'opt-aet': 'Option Agranomie-économie-territoires',
        'opt-psc': 'Option Pratiques sociales et culturelles',
        'opt-maths-comp': 'Option Maths Complémentaires',
        'opt-maths-exp': 'Option Maths Expertes',
        'opt-dgemc': 'Option Droits et grands enjeux du monde contemporain',
        #
        'none': ''
    }

    for a in toTranslate:
        if translated != '' and a != 'none':
            translated += ' / '
        translated += translations[a]

    return translated


@app.route('/deconnexion/')
def deconnexion():
    for s in session:
        session[s] = None
    return redirect(url_for('login'))


# TOUT LE CODE QUI VA SUIVRE PERMET LA CONNEXION A L'ENT VIA OAUTH
# Route qui va permettre de rediriger l'utilisateur sur le site d'authentification et de récupérer un token (pour pouvoir se connecter)
@app.route("/login/")
def login():
    """Step 1: User Authorization.
    Redirect the user/resource owner to the OAuth provider (ENT)
    using an URL with a few key OAuth parameters.
    """
    ENT_reply = OAuth2Session(client_id, scope=["userinfo", "myinfos", "userbook", "directory"], redirect_uri=redirect_uri)
    authorization_url, state = ENT_reply.authorization_url(authorization_base_url)

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    return redirect(authorization_url)


# Step 2: User authorization, this happens on the provider (site de l'ENT).

# callback est la route pour le retour de l'identification
# On utilise le token pour indiquer que c'est bien l'utilisateur qui veut se connecter depuis l'app
@app.route("/callback/", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.
    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    ENT_reply = OAuth2Session(client_id, state=session.get('oauth_state'), redirect_uri=redirect_uri)
    ENT_token = ENT_reply.fetch_token(token_url, client_id=client_id, client_secret=client_secret, code=request.args.get('code'))

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token
    # in /profil.
    session['oauth_token'] = ENT_token

    return redirect(url_for('connexion'))


# Fonction de test pour afficher ce que l'on récupère
@app.route("/connexion/", methods=["GET"])
def connexion():
    """Fetching a protected resource using an OAuth 2 token.
    """
    ENT_reply = OAuth2Session(client_id, token=session['oauth_token'])
    data = ENT_reply.get(
        'https://ent.iledefrance.fr/auth/oauth2/userinfo').json()
    user = db_utilisateurs.find_one({"idENT": data['userId']})
    if user != None:
        session['id'] = str(user['_id'])
        session['pseudo'] = user['pseudo']
        session['couleur'] = user['couleur']
        session['type'] = user['type']
        if user['SanctionEnCour'] != "":
            if user['SanctionDuree'] < datetime.now():
                db_utilisateurs.update_one({'_id': ObjectId(user['_id'])}, {
                                           "$set": {"SanctionEnCour": "", "SanctionDuree": ""}})
        return redirect(url_for('accueil'))
    else:
        if data['type'] == "ELEVE":
            if data['level'] == 'PREMIERE GENERALE & TECHNO YC BT':
                classe = '1G'
            elif data['level'] == 'SECONDE GENERALE & TECHNO YC BT':
                classe = '2GT'
            elif data['level'] == 'TERMINALE GENERALE & TECHNO YC BT':
                classe = 'TG'
            else:
                classe = data['level']
            pseudo = (data['username'].lower()).replace(' ', '_')
            db_utilisateurs.insert_one({"idENT": data['userId'], "nom": data['lastName'], "prenom": data['firstName'], "pseudo": pseudo, 'nomImg': '', "dateInscription": datetime.now(), "birth_date": datetime.strptime(data['birthDate'], '%Y-%m-%d'), "classe": classe,
                                        "lycee": data['schoolName'], 'spes': [], 'langues': [], 'options': [], 'couleur': ['#e6445f', '#f3a6b3', '#afe2e7', '#f9d3d9'], 'type': data['type'], 'elementPublic': [], 'elementPrive': ['email', 'telephone', 'interets', 'birth_date', 'caractere'], "sign": [], "SanctionEnCour": "", 'xp': 0})
            user = db_utilisateurs.find_one({"idENT": data['userId']})
            session['id'] = str(user['_id'])
            session['pseudo'] = user['pseudo']
            session['couleur'] = '#3f51b5'
            session['type'] = user['type']
            return redirect(url_for('profil'))
        elif data['type'] == 'ENSEIGNANT':
            pseudo = (data['username'].lower()).replace(' ', '_')
            db_utilisateurs.insert_one({"idENT": data['userId'], "nom": data['lastName'], "prenom": data['firstName'], "pseudo": pseudo, "dateInscription": datetime.now(), "birth_date": datetime.strptime(
                data['birthDate'], '%Y-%m-%d'), "lycee": data['schoolName'], 'couleur': ['#e6445f', '#f3a6b3', '#afe2e7', '#f9d3d9'], 'type': data['type'], 'elementPublic': [], 'elementPrive': ['email', 'telephone', 'interets', 'birth_date', 'caractere'], "sign": [], "SanctionEnCour": "", 'xp': 0})
            user = db_utilisateurs.find_one({"idENT": data['userId']})
            session['id'] = str(user['_id'])
            session['pseudo'] = user['pseudo']
            session['couleur'] = '#3f51b5'
            session['type'] = user['type']
            return redirect(url_for('profil'))
        else:
            return redirect("https://ent.iledefrance.fr/auth/login")


if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
    app.secret_key = os.urandom(24)
    # NE PAS TOUCHER AUX 2 LIGNES SUIVANTES, C'EST POUR LA CONNEXION A L'ENT
    authorization_base_url = 'https://ent.iledefrance.fr/auth/oauth2/auth'
    token_url = 'https://ent.iledefrance.fr/auth/oauth2/token'
    if 'redirect_uri' in os.environ:
        # Le client secret est le code secret de l'application
        # NE PAS TOUCHER AUX 3 LIGNES SUIVANTES, C'EST POUR LA CONNEXION A L'ENT
        client_id = 'code-ton-lycee-key4school'
        client_secret = 'jHy6g8JG4FdP0a5VI2m'
        redirect_uri = os.environ['redirect_uri']
        # Lancement de l'application, à l'adresse 127.0.0.0 et sur le port 3000
        # app.run(host='0.0.0.0', port=os.environ.get("PORT", 3000))
        socketio.run(app, host='0.0.0.0', port=os.environ.get("PORT", 3000), debug=True)

    else:
        # Le client secret est le code secret de l'application
        # NE PAS TOUCHER AUX 2 LIGNES SUIVANTES, C'EST POUR LA CONNEXION A L'ENT
        client_id = 'code-ton-lycee-localhost'
        client_secret = 'JR7XcyGWBHt2VA9W'
        redirect_uri = "http://127.0.0.1:3000/callback"
        # Lancement de l'application, à l'adresse 127.0.0.0 et sur le port 3000
        # app.run(host="127.0.0.1", port=3000, debug=True)
        socketio.run(app, host='127.0.0.1', port=3000, debug=True)
