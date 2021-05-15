from flask import Flask, render_template, request, redirect, session, url_for, abort
# import pronotepy  # api Pronote
# from pronotepy.ent import ile_de_france
from flask_pymongo import PyMongo
from datetime import *
from requests_oauthlib import OAuth2Session
from flask_session import Session
from flask.json import jsonify
from bson.objectid import ObjectId
from bson import Binary
import os
import gridfs

# Création de l'application
app = Flask(__name__)


# Le client secret est le code secret de l'application
# NE PAS TOUCHER AUX 4 LIGNES SUIVANTES, C'EST POUR LA CONNEXION A L'ENT
client_id = 'code-ton-lycee'
client_secret = 'JR7XcyGWBHt2VA9W'
authorization_base_url = 'https://ent.iledefrance.fr/auth/oauth2/auth'
token_url = 'https://ent.iledefrance.fr/auth/oauth2/token'

# Récupération d'une base de données
cluster = PyMongo(
    app, "mongodb+srv://CTLadmin:ctlADMIN@ctlbdd.etzx9.mongodb.net/CTLBDD?retryWrites=true&w=majority")
# Voici deux exemples pour créer des BDD
db_utilisateurs = cluster.db.utilisateurs
db_demande_aide = cluster.db.demande_aide
db_messages = cluster.db.messages
db_groupes = cluster.db.groupes
db_files = cluster.db.fs.files
db_chunks = cluster.db.fs.chunks
# Voici un exemple pour ajouter un utilisateur avec son nom et son mot de passe

'''connexion a l'api Pronote avec l'username et le mdp ENT mais je suis pas sur que ca va etre possible'''
'''le lien de l'api pour plus d'info https://github.com/bain3/pronotepy'''
# client = pronotepy.Client('https://0910626l.index-education.net/pronote/eleve.html',
#                           username=username,
#                           password=mdpENT,
#                           ent=ile_de_france)


def htmlspecialchars(text):
    return (
        text.replace("&", "&amp;").
        replace('"', "&quot;").
        replace("<", "&lt;").
        replace(">", "&gt;").
        replace("'", "&apos;")
    )


# Quand on arrive sur le site, on affiche la page "ma_page.html"
@app.route('/')
def accueil():
    if 'id' in session:
        toutesDemandes = db_demande_aide.aggregate([
            {'$sort': {'date-envoi': -1}},
            {'$limit': 5}
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
                # on récupère en plus l'utilisateur pour prochainement afficher son nom/prenom/pseudo
                'user': db_utilisateurs.find_one({'_id': ObjectId(a['id-utilisateur'])})
            })

        return render_template("index.html", demandes=demandes)
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
            grp = db_groupes.find(
                {"$or": [{"id-utilisateurs": ObjectId('6075cae8fb56bf0654e5f4ab')}, {"id-utilisateurs": ObjectId(session['id'])}]})
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
                        'audio': 1
                    }},
                ])
                infogroupes = db_groupes.find_one(
                    {"_id": ObjectId(idGroupe)})
                infoUtilisateurs = []
                for content in infogroupes['id-utilisateurs']:
                    infoUtilisateurs += db_utilisateurs.find(
                        {"_id": ObjectId(content)})
                if session['id'] in str(infoUtilisateurs) or '6075cae8fb56bf0654e5f4ab' in str(infoUtilisateurs):
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
            return render_template("messages.html", msgDb=msgDb, grpUtilisateur=grp, idgroupe=idGroupe, infogroupe=infogroupes, infoUtilisateurs=infoUtilisateurs, users=db_utilisateurs.find(), sessionId=ObjectId(session['id']))

        elif request.method == 'POST':
            if request.form['reponse'] != "None":
                reponse = ObjectId(request.form['reponse'])
            else:
                reponse = "None"
            db_messages.insert_one({"id-groupe": ObjectId(request.form['group']), "id-utilisateur": ObjectId(session['id']),
                                    "contenu": request.form['contenuMessage'], "date-envoi": datetime.now(), "reponse": reponse})
            return 'sent'
    else:
        return redirect(url_for('login'))


@app.route('/uploadAudio/', methods=['POST'])
def uploadAudio():
    if 'id' in session:
        heure = str(datetime.now())
        nom = "MsgVocal" + request.form['group'] + session['id'] + heure
        cluster.save_file(nom, request.files['audio'])
        db_messages.insert_one({"id-groupe": ObjectId(request.form['group']), "id-utilisateur": ObjectId(session['id']),
                                "contenu": nom, "date-envoi": datetime.now(), "audio": True, "reponse": ""})
        return('yes')
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
        return redirect(url_for('messages', idGroupe=idGroupe))
    else:
        return redirect(url_for('login'))


@app.route('/searchUser_newgroup/', methods=['POST'])
def searchUser_newgroup():
    if 'id' in session:
        users = db_utilisateurs.find({'$or': [{'pseudo': {'$regex': request.form['search'], '$options': 'i'}},
                                              {'nom': {
                                                  '$regex': request.form['search'], '$options': 'i'}},
                                              {'prenom': {
                                                  '$regex': request.form['search'], '$options': 'i'}},
                                              {'lycee': {
                                                  '$regex': request.form['search'], '$options': 'i'}},
                                              {'email': {
                                                  '$regex': request.form['search'], '$options': 'i'}},
                                              {'insta': {
                                                  '$regex': request.form['search'], '$options': 'i'}},
                                              {'snap': {
                                                  '$regex': request.form['search'], '$options': 'i'}},
                                              {'telephone': {'$regex': request.form['search'], '$options': 'i'}}]}).limit(30)
        return render_template("searchUser_newgroup.html", users=users)
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
        newGroupe = db_groupes.insert_one(
            {'nom': request.form['nomnewgroupe'], 'id-utilisateurs': participants})
        return redirect(url_for('messages', idGroupe=newGroupe.inserted_id))
    else:
        return redirect(url_for('login'))


@app.route('/refreshMsg/')
def refreshMsg():
    if 'id' in session:
        idGroupe = request.args['idgroupe']
        if request.args['idMsg'] != 'undefined' and idGroupe != 'undefined' and idGroupe != 'None':
            dateLast = datetime.strptime(
                request.args['idMsg'], '%Y-%m-%dT%H:%M:%S.%fZ')
            infogroupes = db_groupes.find_one(
                {"_id": ObjectId(idGroupe)})
            infoUtilisateurs = []
            for content in infogroupes['id-utilisateurs']:
                infoUtilisateurs += db_utilisateurs.find(
                    {"_id": ObjectId(content)})
            msgDb = db_messages.aggregate([
                {'$match': {'$and': [
                    {'id-groupe': ObjectId(idGroupe)}, {'date-envoi': {'$gt': dateLast}}]}},
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
            ])
            return render_template("refreshMessages.html", msgDb=msgDb, sessionId=ObjectId(session['id']), infoUtilisateurs=infoUtilisateurs, idgroupe=idGroupe)
        else:
            return ''
    else:
        return redirect(url_for('login'))


@app.route('/changeTheme/', methods=['POST'])
def changeTheme():
    if 'id' in session:
        db_utilisateurs.update_one({"_id": ObjectId(session['id'])}, {
                                   "$set": {"couleur": request.form['couleur']}})
        session['couleur'] = request.form['couleur']
        return redirect(url_for('profil'))
    else:
        return redirect(url_for('login'))


@app.route('/profil/', defaults={'idUser': None}, methods=['POST', 'GET'])
@app.route('/profil/<idUser>', methods=['POST', 'GET'])
def profil(idUser):
    if 'id' in session:
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
                # on récupère en plus l'utilisateur pour prochainement afficher son nom/prenom/pseudo
                'user': db_utilisateurs.find_one({'_id': ObjectId(a['id-utilisateur'])})
            })
        profilUtilisateur = db_utilisateurs.find_one(
            {'_id': ObjectId(session['id'])})
        if idUser == None:
            profilUtilisateur = db_utilisateurs.find_one(
                {'_id': ObjectId(session['id'])})
            return render_template("profil.html", profilUtilisateur=profilUtilisateur, demandes=demandes)
        else:
            profilUtilisateur = db_utilisateurs.find_one(
                {'_id': ObjectId(idUser)})
            return render_template("affichProfil.html", profilUtilisateur=profilUtilisateur)
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
        db_utilisateurs.update_one({"_id": ObjectId(session['id'])}, {'$set': {'pseudo': request.form['pseudo'], 'email': request.form['email'], 'telephone': request.form['telephone'], 'interets': request.form['interets'],
                                                                               'langues': request.form['langues'], 'caractere': request.form['caractere'], 'options': request.form['options'], 'spe': request.form['spe'], 'elementPrive': elementPrive, 'elementPublic': elementPublic}})
        # requete vers la db update pour ne pas créer un nouvel utilisateur ensuite 1ere partie on spécifie l'id de l'utilisateur qu'on veut modifier  puis pour chaque champ on précise les nouvelles valeurs.
        return redirect(url_for('profil'))
    else:
        return redirect(url_for('login'))


@app.route('/updateImg/', methods=['POST'])
def updateImg():
    if 'id' in session:
        if request.form['but'] == "remove":
            MyImage = db_files.find(
                {'filename': {'$regex': 'imgProfile' + session['id']}})
            for a in MyImage:
                db_files.delete_one({'_id': a['_id']})
                db_chunks.delete_many({'files_id': a['_id']})
            db_utilisateurs.update_one({'_id': ObjectId(session['id'])}, {
                                       '$set': {'imgProfile': "", 'nomImg': ""}})
        elif request.form['but'] == "replace":
            ImgNom = request.files['Newpicture'].filename + \
                'imgProfile' + session['id']
            MyImage = db_files.find(
                {'filename': {'$regex': 'imgProfile' + session['id']}})
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

            diffTemps = int(
                (datetime.now() - msg['date-envoi']).total_seconds())
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
                diffTemps2 = int(
                    (datetime.now() - r['date-envoi']).total_seconds())
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

            result = {  # on ajoute à la liste ce qui nous interesse
                'idMsg': msg['_id'],
                'titre': msg['titre'],
                'contenu': msg['contenu'],
                'temps': tempsStr,
                'matière': msg['matière'],
                'nb-likes': len(msg['likes']),
                'a_like': a_like,
                'a_sign': a_sign,
                'reponses': reponses,
                # on récupère en plus l'utilisateur pour prochainement afficher son nom/prenom/pseudo
                'user': db_utilisateurs.find_one({'_id': ObjectId(msg['id-utilisateur'])})
            }

            return render_template("comments.html", d=result)

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
                    {'$set':
                        {'réponses associées': reponses}
                     }
                )

            return redirect('/comments/' + idMsg)
    else:
        return redirect(url_for('login'))


@app.route('/question/', methods=['POST', 'GET'])
def question():
    if 'id' in session:
        if request.method == 'POST':
            db_demande_aide.insert_one(
                {"id-utilisateur": ObjectId(session['id']), "titre": request.form['titre'], "contenu": request.form['demande'], "date-envoi": datetime.now(), "matière": request.form['matiere'], "réponses associées": {}, "likes": [], "sign": []})

            demandes = db_demande_aide.aggregate([
                {'$sort': {'date-envoi': -1}},
                {'$limit': 1}
            ])
            for demande in demandes:
                return redirect('/comments/' + str(demande['_id']))

            # return render_template('question.html', envoi="Envoi réussi")
        else:
            return render_template('question.html')
    else:
        return redirect(url_for('login'))


@app.route('/recherche')
def recherche():
    if 'id' in session:
        if 'search' in request.args and not request.args['search'] == '':
            firstResult = db_demande_aide.find(
                {'$text': {'$search': request.args['search']}})

            result = []
            for a in firstResult:  # pour chaque résultat, on va l'ajouter dans une liste qui sera donnée à la page HTML
                # on convertit en nombre de secondes la durée depuis le post
                diffTemps = int(
                    (datetime.now() - a['date-envoi']).total_seconds())
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

                result.append({  # on ajoute à la liste ce qui nous interesse
                    'idMsg': a['_id'],
                    'titre': a['titre'],
                    'contenu': a['contenu'],
                    'temps': tempsStr,
                    'matière': a['matière'],
                    'nb-likes': len(a['likes']),
                    'a_like': a_like,
                    'a_sign': a_sign,
                    # on récupère en plus l'utilisateur pour prochainement afficher son nom/prenom/pseudo
                    'user': db_utilisateurs.find_one({'_id': ObjectId(a['id-utilisateur'])})
                })

            users = db_utilisateurs.find({'$or': [{'pseudo': {'$regex': request.args['search'], '$options': 'i'}},
                                                  {'nom': {
                                                      '$regex': request.args['search'], '$options': 'i'}},
                                                  {'prenom': {
                                                      '$regex': request.args['search'], '$options': 'i'}},
                                                  {'lycee': {
                                                      '$regex': request.args['search'], '$options': 'i'}},
                                                  {'email': {
                                                      '$regex': request.args['search'], '$options': 'i'}},
                                                  {'insta': {
                                                      '$regex': request.args['search'], '$options': 'i'}},
                                                  {'snap': {
                                                      '$regex': request.args['search'], '$options': 'i'}},
                                                  {'telephone': {'$regex': request.args['search'], '$options': 'i'}}]}).limit(3)

            return render_template('recherche.html', results=result, users=users, search=request.args['search'])

        else:
            return redirect(url_for('accueil'))
    else:
        return redirect(url_for('login'))


@app.route('/rechercheUser')
def recherche_user():
    if 'id' in session:
        users = db_utilisateurs.find({'$or': [{'pseudo': {'$regex': request.args['search'], '$options': 'i'}},
                                              {'nom': {
                                                  '$regex': request.args['search'], '$options': 'i'}},
                                              {'prenom': {
                                                  '$regex': request.args['search'], '$options': 'i'}},
                                              {'lycee': {
                                                  '$regex': request.args['search'], '$options': 'i'}},
                                              {'email': {
                                                  '$regex': request.args['search'], '$options': 'i'}},
                                              {'insta': {
                                                  '$regex': request.args['search'], '$options': 'i'}},
                                              {'snap': {
                                                  '$regex': request.args['search'], '$options': 'i'}},
                                              {'telephone': {'$regex': request.args['search'], '$options': 'i'}}]}).limit(30)
        return render_template('rechercheUser.html', users=users)
    else:
        return redirect(url_for('login'))


@app.route('/likePost/<idPost>', methods=['POST'])
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
            else:
                newLikes.append(session['id'])  # on ajoute son like

            # on update dans la DB
            db_demande_aide.update(
                {'_id': ObjectId(idPost)},
                {'$set':
                    {'likes': newLikes}
                 }
            )

            # on retourne enfin le nouveau nb de likes
            return {'newNbLikes': len(newLikes)}, 200

        else:
            abort(400)  # il manque l'id du message
    else:
        abort(401)  # non autorisé


@app.route('/likeRep/<idPost>/<idRep>', methods=['POST'])
def likeRep(idPost, idRep):
    if 'id' in session:
        if 'idPost' != None and 'idRep' != None:
            # on récupère les likes de la demande d'aide
            reponses = db_demande_aide.find_one({"_id": ObjectId(idPost)})[
                'réponses associées']
            if not idRep in reponses:
                return abort(400)

            reponse = reponses[idRep]
            likes = reponse['likes']
            newLikes = list(likes)

            # on check mtn si l'utilisateur a déjà liké la demande
            if session['id'] in likes:
                newLikes.remove(session['id'])  # on supprime son like
            else:
                newLikes.append(session['id'])  # on ajoute son like

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
                {'$set':
                    {'réponses associées': reponses}
                 }
            )

            # on retourne enfin le nouveau nb de likes
            return {'newNbLikes': len(newLikes)}, 200

        else:
            abort(400)  # il manque l'id du message
    else:
        abort(401)  # non autorisé


@app.route('/signPost/', methods=['POST'])
def signPost():
    if 'id' in session:
        if request.form['idSignalé'] != None:
            # on récupère les signalements de la demande d'aide
            demande = db_demande_aide.find_one(
                {"_id": ObjectId(request.form['idSignalé'])})
            sign = demande['sign']
            newSign = list(sign)

            # on check mtn si l'utilisateur a déjà signalé la demande
            if session['id'] in sign:
                newSign.remove(session['id'])  # on supprime son signalement
                db_demande_aide.update_one(
                    {'_id': ObjectId(request.form['idSignalé'])},
                    {'$pull': {
                        'sign': session['id'],
                        'motif': {'id': ObjectId(session['id'])}}
                     },
                )

            else:
                newSign.append(session['id'])  # on ajoute son signalement
                raison = {request.form['Raison']}
                db_demande_aide.update_one(
                    {'_id': ObjectId(request.form['idSignalé'])},
                    {'$push':
                        {'sign': session['id'],
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
            abort(400)  # il manque l'id du message
    else:
        abort(401)  # non autorisé


@app.route('/amis/')
def amis():
    if 'id' in session:
        return render_template("amis.html")
    else:
        return redirect(url_for('login'))


def convertTime(diffTemps):
    tempsStr = ''  # puis on se fait chier à trouver le délai entre le poste et aujourd'hui
    if diffTemps // (60 * 60 * 24 * 7):  # semaines
        tempsStr += '{}sem '.format(diffTemps // (60 * 60 * 24 * 7))
        if (diffTemps % (60 * 60 * 24 * 7)) // (60 * 60 * 24):  # jours
            tempsStr += '{}j '.format((diffTemps %
                                       (60 * 60 * 24 * 7)) // (60 * 60 * 24))
    elif diffTemps // (60 * 60 * 24):  # jours
        tempsStr += '{}j '.format(diffTemps // (60 * 60 * 24))
        if (diffTemps % (60 * 60 * 24)) // (60 * 60):  # heures
            tempsStr += '{}h '.format((diffTemps %
                                       (60 * 60 * 24)) // (60 * 60))
    elif diffTemps // (60 * 60):  # heures
        tempsStr += '{}h '.format(diffTemps // (60 * 60))
        if (diffTemps % (60 * 60)) // 60:  # minutes
            tempsStr += '{}min '.format(diffTemps % (60 * 60) // 60)
    else:
        tempsStr = '{}min'.format(diffTemps // 60)

    return tempsStr


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
    ENT_reply = OAuth2Session(
        client_id, scope="userinfo", redirect_uri="http://127.0.0.1:3000/callback")
    authorization_url, state = ENT_reply.authorization_url(
        authorization_base_url)

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

    ENT_reply = OAuth2Session(
        client_id, state=session.get('oauth_state'),  redirect_uri="http://127.0.0.1:3000/callback")
    ENT_token = ENT_reply.fetch_token(token_url, client_id=client_id, client_secret=client_secret,
                                      code=request.args.get('code'))

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token
    # in /profil.
    session['oauth_token'] = ENT_token

    return redirect(url_for('.connexion'))


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
            db_utilisateurs.insert_one({"idENT": data['userId'], "nom": data['lastName'], "prenom": data['firstName'], "pseudo": pseudo, "dateInscription": datetime.now(), "birth_date": datetime.strptime(
                data['birthDate'], '%Y-%m-%d'), "classe": classe, "lycee": data['schoolName'], 'couleur': '#3f51b5', 'type': data['type'], 'elementPublic': [], 'elementPrive': ['email', 'telephone', 'interets', 'birth_date', 'caractere']})
            user = db_utilisateurs.find_one({"idENT": data['userId']})
            session['id'] = str(user['_id'])
            session['pseudo'] = user['pseudo']
            session['couleur'] = '#3f51b5'
            session['type'] = user['type']
            return redirect(url_for('profil'))
        elif data['type'] == 'ENSEIGNANT':
            pseudo = (data['username'].lower()).replace(' ', '_')
            db_utilisateurs.insert_one({"idENT": data['userId'], "nom": data['lastName'], "prenom": data['firstName'], "pseudo": pseudo, "dateInscription": datetime.now(),
                                        "birth_date": datetime.strptime(data['birthDate'], '%Y-%m-%d'), "lycee": data['schoolName'], 'couleur': '#3f51b5', 'type': data['type'], 'elementPublic': [], 'elementPrive': ['email', 'telephone', 'interets', 'birth_date', 'caractere']})
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
    if 'HEROKU' in os.environ:
        # Lancement de l'application, à l'adresse 127.0.0.0 et sur le port 3000
        app.run(host='0.0.0.0', port=os.environ.get("PORT", 3000))
    else:
        # Lancement de l'application, à l'adresse 127.0.0.0 et sur le port 3000
        app.run(host="127.0.0.1", port=3000, debug=True)
