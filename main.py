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
from difflib import SequenceMatcher
from db_poo import *


# Création de l'application
app = Flask(__name__)
socketio = SocketIO(app)

# Création du Cluster de la DB
DB = DB_Manager.createCluster(app, "mongodb+srv://CTLadmin:ctlADMIN@ctlbdd.etzx9.mongodb.net/CTLBDD?retryWrites=true&w=majority")

# Enregistrement de la DB

all_utilisateurs = DB.db_utilisateurs.find()
for u in all_utilisateurs:
    utilisateurs[str(u['_id'])] = Utilisateur(u)

all_demandes_aide = DB.db_demande_aide.find()
for d in all_demandes_aide:
    demandes_aide[str(d['_id'])] = Demande(d)

all_groupes = DB.db_groupes.find()
for g in all_groupes:
    groupes[str(g['_id'])] = Groupe(g)

all_messages = DB.db_messages.find()
for m in all_messages:
    messages[str(m['_id'])] = Message(m)


def recupLevel():
    global utilisateurs

    user = utilisateurs[session['id']].toDict()
    xpgens = user['xp']
    niv = int(0.473*xpgens**0.615)
    xplvl = int((0.473*xpgens**0.615-niv)*100)

    return niv, xplvl, xpgens

def addXP(userID: str, amount: int) -> None:
    """
        +10 pour une demande d’aide
        +15 pour une réponse
        +2 pour chaque like reçu
    """

    user = utilisateurs[userID]
    user.xp += amount

    utilisateurs[userID].update()

    return

def addXpModeration(user: str, amount: int) -> None:
    global utilisateurs

    user = utilisateurs[userID]
    user.xpModeration += amount

    utilisateurs[userID].update()

    return

with open("list_ban_words.txt", "r") as fichierBanWords:
    listeModeration = fichierBanWords.read().splitlines()

def automoderation(stringModerer: str) -> str:
    for content in listeModeration:
        if len(content) < 5:
            if stringModerer[0:len(content)+1] == content+" ":
                stringModerer= stringModerer.replace(content, " * ")
            if stringModerer[-len(content)+1:] == " "+content:
                stringModerer= stringModerer.replace(content, " * ")
            if stringModerer == content:
                stringModerer= stringModerer.replace(content, " * ")
            content= " "+content+" "
        if  content in stringModerer:
            stringModerer= stringModerer.replace(content, " * ")

    return stringModerer


clientsNotif = {}

def notif(type, id_groupe, id_msg, destinataires):
    DB.db_notif.insert_one({"type": type, "id_groupe": id_groupe, "id_msg": id_msg,
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
    global utilisateurs
    global demandes_aide

    if 'id' in session:
        user = utilisateurs[session['id']].toDict()
        # subjects = getUserSubjects(user)

        # ici on récupère les 10 dernières demandes les plus récentes non résolues corresppondant aux matières de l'utilisateur
        demandes = sorted([d.toDict() for d in demandes_aide.values() if d.matiere in user['matieres'] and not d.resolu], key = lambda d: d['date-envoi'], reverse=True)[:9]

        return render_template("index.html", demandes=demandes, user=user)
    else:
        return redirect(url_for('login'))


# Connection au groupe pour recevoir les nouvelles notif
@socketio.on('connectToNotif')
def handleEvent_connectToNotif():
    if 'id' in session:
        print(session['id'] + " connected")
        clientsNotif[session['id']] = True
        join_room(session['id'])


# Deconnexion au groupe pour recevoir les nouvelles notif
@socketio.on('disconnect')
def handleEvent_disconnect():
    if 'id' in session:
        if session['id'] in clientsNotif:
            print(session['id'] + " disconnected")
            clientsNotif.pop(session['id'])
            leave_room(session['id'])


# laisser le nom entre deux slash ca permet d'accepter toutes les urls du style http://127.0.0.1:3000/messages/ sinon ca marche pas.s
@app.route('/accueil/')
def accueil2():
    if 'id' in session:
        return redirect(url_for('accueil'))
    else:
        return redirect(url_for('login'))

@app.route('/messages/', defaults={'idGroupe': None})
@app.route('/messages/<idGroupe>')
def page_messages(idGroupe):
    global utilisateurs
    global messages
    global groupes

    if 'id' in session:
        # il faudra récupérer l'id qui sera qans un cookie
        grp = [groupes[idGrp] for idGrp in [idGrp for (idGrp , groupe) in groupes.items() if ObjectId(session['id']) in groupe.id_utilisateurs]]
        user = utilisateurs[session['id']].toDict()
        users = sorted([u.toDict() for u in utilisateurs.values()], key = lambda u: u['pseudo'])

        if idGroupe != None:
            msgDb = [m.toDict() for m in messages.values() if m.id_groupe == ObjectId(idGroupe)]
            toDel = []

            for m in msgDb:
                if m['reponse'] != 'None' and m['reponse'] != '':
                    toDel.append(messages[str(m['reponse'])].toDict())
                    m['rep'] = messages[str(m['reponse'])].toDict()
            for a in toDel:
                msgDb.remove(a)

            infogroupes = groupes[idGroupe].toDict()
            infoUtilisateurs = [utilisateurs[str(content)].toDict() for content in infogroupes['id-utilisateurs']]

            danslegroupe = False
            for user in infoUtilisateurs:
                if ObjectId(session['id']) == user['_id']:
                    danslegroupe = True

            if user['admin'] == True:
                msgDb = [m.toDict() for m in messages.values() if m.id_groupe == ObjectId(idGroupe) and m.sign != []]
                toDel = []

                for m in msgDb:
                    if m['reponse'] != 'None' and m['reponse'] != '':
                        toDel.append(messages[str(m['reponse'])].toDict())
                        m['rep'] = messages[str(m['reponse'])].toDict()
                for a in toDel:
                    msgDb.remove(a)

        else:
            msgDb = None
            infogroupes = None
            infoUtilisateurs = None

        return render_template("messages.html", msgDb=msgDb, grpUtilisateur=grp, idgroupe=idGroupe, infogroupe=infogroupes, infoUtilisateurs=infoUtilisateurs, users=users, sessionId=ObjectId(session['id']), user=user)

    else:
        return redirect(url_for('login'))

# Connection au groupe pour recevoir les nouveaux messages par la suite
@socketio.on('connectToGroup')
def handleEvent_connectToGroup(json):
    global groupes

    if 'id' in session:
        if 'room' in json:
            if json['room'] != 'None':
                # Check authorized
                grp = groupes[json['room']].toDict()
                if grp != None:
                    if session['id'] in str(grp['id-utilisateurs']): # authorized
                        join_room(json['room'])


@socketio.on('postMsg')
def handleEvent_postMsg(json):
    global utilisateurs
    global messages
    global groupes

    if 'id' in session:
        if 'room' in json:
            # Check authorized
            grp = groupes[json['room']].toDict()
            if grp != None:
                if session['id'] in str(grp['id-utilisateurs']): # authorized
                    if json['reponse'] != "None":
                        reponse = ObjectId(json['reponse'])
                    else:
                        reponse = "None"

                    if 'dateAudio' in json:
                        nom = "MsgVocal" + json['room'] + session['id'] + json['dateAudio']

                        _id = ObjectId()
                        messages[str(_id)] = Message({"_id": _id, "id-groupe": ObjectId(json['room']), "id-utilisateur": ObjectId(session['id']),
                                    "contenu": nom, "date-envoi": datetime.now(), "audio": True, "reponse": reponse, "sign": []})
                        messages[str(_id)].insert()
                        message = messages[str(_id)].toDict()

                    elif not json['contenuMessage'] == '':
                        _id = ObjectId()
                        messages[str(_id)] = Message({"_id": _id, "id-groupe": ObjectId(json['room']), "id-utilisateur": ObjectId(session['id']),
                                                          "contenu": json['contenuMessage'], "date-envoi": datetime.now(), "audio": False, "reponse": reponse, "sign": []})
                        messages[str(_id)].insert()
                        message = messages[str(_id)].toDict()
                    if message:
                        infogroupes = groupes[json['room']].toDict()
                        notif("msg", ObjectId(json['room']), _id, infogroupes['id-utilisateurs'])

                        infoUtilisateurs = []
                        for content in infogroupes['id-utilisateurs']:
                            infoUtilisateurs += utilisateurs[str(content)].toDict()

                        # Sending new message to connected users
                        message = messages[str(_id)].toDict()
                        if message['reponse'] != 'None' and message['reponse'] != '':
                            message['rep'] = messages[str(message['reponse'])].toDict()

                        html = render_template("refreshMessages.html", msg=message, sessionId=ObjectId(session['id']), infoUtilisateurs=infoUtilisateurs, idgroupe=json['room'])
                        emit('newMsg', html, to=json['room'])

@app.route('/uploadAudio/', methods=['POST'])
def uploadAudio():
    if 'id' in session:
        nom = "MsgVocal" + request.form['group'] + session['id'] + request.form['date']
        DB.cluster.save_file(nom, request.files['audio'])
        return 'yes'
    else:
        return redirect(url_for('login'))


@app.route('/audio/<audioName>')
def audio(audioName):
    if 'id' in session:
        return DB.cluster.send_file(audioName)
    else:
        return redirect(url_for('login'))

@app.route('/file/<fileName>')
def file(fileName):
    if 'id' in session:
        return DB.cluster.send_file(fileName)
    else:
        return redirect(url_for('login'))

@app.route('/suppressionMsg/', methods=['POST'])
def supprimerMsg():
    global messages

    if 'id' in session:
        idGroupe = request.form['grp']

        messages[request.form['msgSuppr']].delete()
        del messages[request.form['msgSuppr']]

        if request.form['audio'] == 'True':
            MyAudio = DB.db_files.find_one({'filename': request.form['audioName']})
            DB.db_files.delete_one({'_id': MyAudio['_id']})
            DB.db_chunks.delete_many({'files_id': MyAudio['_id']})

        return redirect(url_for('messages', idGroupe=idGroupe))

    else:
        return redirect(url_for('login'))

@app.route('/createGroupe/', methods=['POST'])
def createGroupe():
    global groupes

    if 'id' in session:
        participants = [ObjectId(session['id'])]
        for name, value in request.form.items():
            if name == 'nomnewgroupe':
                pass
            else:
                participants.append(ObjectId(name))

        _id = ObjectId()
        groupes[str(_id)] = Groupe({'_id': _id, 'nom': request.form['nomnewgroupe'], 'id-utilisateurs': participants, 'moderateurs': [ObjectId(session['id'])], 'sign':[], 'motif': []})
        groupes[str(_id)].insert()

        return redirect(url_for('page_messages', idGroupe=_id))
    else:
        return redirect(url_for('login'))

@app.route('/updateGroupe/', methods=['POST'])
def updateGroupe():
    global groupes

    if 'id' in session:
        groupe = groupes[request.form['IdGroupe']].toDict()
        participants = groupe['id-utilisateurs']

        if ObjectId(session['id']) in participants and ObjectId(session['id']) in groupe['moderateurs']:
            for name, value in request.form.items():
                if name == 'IdGroupe':
                    pass
                else:
                    participants.append(ObjectId(name))

            groupes[request.form['IdGroupe']].update()

        return redirect(url_for('page_messages', idGroupe=request.form['IdGroupe']))
    else:
        return redirect(url_for('login'))

@app.route('/virerParticipant/', methods=['POST'])
def virerParticipant():
    global utilisateurs
    global groupes

    if 'id' in session:
        groupe = groupes[request.form['idViréGrp']].toDict()
        participants = groupe['id-utilisateurs']
        moderateurs = groupe['moderateurs']

        if ObjectId(session['id']) in moderateurs or request.form['idViré'] == session['id']:
            participants.remove(ObjectId(request.form['idViré']))

            if ObjectId(request.form['idViré']) in moderateurs:
                moderateurs.remove(ObjectId(request.form['idViré']))

            groupes[request.form['idViréGrp']].update()

            if request.form['idViré'] == session['id']:
                return redirect(url_for('page_messages'))
            else:
                return  redirect('/messages/'+request.form['idViréGrp'])
        else:
            return redirect(url_for('accueil'))
    else:
        return redirect(url_for('login'))

@app.route('/modifRole/', methods=['POST'])
def modifRole():
    if 'id' in session:
        grp = groupes[request.form['idGrp']].toDict()
        modos = grp['moderateurs']
        participants = grp['id-utilisateurs']

        if ObjectId(session['id']) in modos and ObjectId(request.form['idModifié']) in participants:
            if ObjectId(request.form['idModifié']) in modos:
                modos.remove(ObjectId(request.form['idModifié']))
                groupes[request.form['idGrp']].update()

                return 'participant'

            else:
                modos.append(ObjectId(request.form['idModifié']))
                groupes[request.form['idGrp']].update()

                return 'admin'
        else:
            abort(401) # non autorisé
    else:
        abort(403) # doit se connecter

@app.route('/changeTheme/', methods=['POST'])
def changeTheme():
    global utilisateurs

    if 'id' in session:
        if int(request.form['couleur']) == 5:
            color2 = tuple(int(request.form['color2'].lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
            moyenne = '#%02x%02x%02x' % tuple((color+255)//2 for color in color2)
            couleurs = [request.form['color1'], request.form['color2'], request.form['color3'], moyenne]

        else:
            listColor = [['#e6445f', '#f3a6b3', '#afe2e7', '#f9d3d9'],
                        ['#4c7450', '#a8d7ad', '#c3455a', '#d4ebd6'],
                        ['#3f51b5', '#81c5e2', '#e6b2d9', '#c0e2f1'],
                        ['#e6b991', '#d6c2b0', '#74b3ab', '#ebe1d8'],
                        ['#deb72f', '#e6cf81', '#e68181', '#f3e7c0']]
            couleurs = listColor[int(request.form['couleur'])]

        user = utilisateurs[session['id']]
        user.couleur = couleurs

        utilisateurs[session['id']].update()

        session['couleur'] = couleurs

        return redirect(url_for('profil'))
    else:
        return redirect(url_for('login'))


@app.route('/profil/', defaults={'idUser': None}, methods=['POST', 'GET'])
@app.route('/profil/<idUser>', methods=['POST', 'GET'])
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
            return render_template("profil.html", profilUtilisateur=profilUtilisateur, demandes=demandes, xplvl=xplvl, xp=xpgens, niv=niv, user=user)

        else:
            user = utilisateurs[idUser]
            profilUtilisateur = user.toDict()
            niv, xplvl, xpgens = user.recupLevel()

            # translate spes/options/lv
            profilUtilisateur['langues'] = profilUtilisateur['langues-str']
            profilUtilisateur['spes'] = profilUtilisateur['spes-str']
            profilUtilisateur['options'] = profilUtilisateur['options-str']

            return render_template("affichProfil.html", profilUtilisateur=profilUtilisateur, a_sign=profilUtilisateur['a_sign'], user=utilisateurs[session['id']].toDict())
    else:
        return redirect(url_for('login'))


@app.route('/userImg/<profilImg>')
def userImg(profilImg):
    if 'id' in session:
        return DB.cluster.send_file(profilImg)
    else:
        return redirect(url_for('login'))


@app.route("/updateprofile/", methods=["POST"])
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
        user.langues = [request.form['lv1'], request.form['lv2']]
        user.options = [request.form['option1'], request.form['option2']]
        user.spes = [request.form['spe1'], request.form['spe2'], request.form['spe3']]
        user.elementPrive = elementPrive
        user.elementPublic = elementPublic

        utilisateurs[session['id']].update()

        return redirect(url_for('profil'))
    else:
        return redirect(url_for('login'))


@app.route('/updateImg/', methods=['POST'])
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
        return redirect(url_for('login'))


@app.route('/comments/')
def redirect_comments():
    return redirect('/')


@app.route('/comments/<idMsg>', methods=['GET', 'POST'])
def comments(idMsg):
    global utilisateurs
    global demandes_aide

    if 'id' in session:
        if request.method == 'GET':
            msg = demandes_aide[idMsg].toDict()

            return render_template("comments.html", d=msg, user=utilisateurs[session['id']].toDict())

        else:
            if 'rep' in request.form:
                msg = demandes_aide[idMsg].toDict()
                reponses = msg['reponsesObjects']

                _id = ObjectId()
                reponses[str(_id)] = Reponse({
                    '_id': ObjectId(_id),
                    'id-utilisateur': ObjectId(session['id']),
                    'contenu': automoderation(request.form.get('rep')),
                    'date-envoi': datetime.now(),
                    'likes': []
                })

                demandes_aide[idMsg].update()

                notif("demande", ObjectId(idMsg), _id, msg['idAuteur'])

                # add XP
                if not ObjectId(session['id']) == msg['idAuteur']:
                    addXP(session['id'], 15)

            return redirect('/comments/' + idMsg)
    else:
        return redirect(url_for('login'))


@app.route('/question/', methods=['POST', 'GET'])
def question():
    global utilisateurs
    global demandes_aide

    if 'id' in session:
        if request.method == 'POST':
            # Impossibilité demande d'aide vide
            if request.form['titre'] == '':
                return redirect('/question/')

            user = utilisateurs[session['id']].toDict()
            if user['SanctionEnCour'] != "Spec" and user['SanctionEnCour'] != "SpecForum":
                if request.files['file'].mimetype != 'application/octet-stream':
                    if request.files['file'].mimetype == 'application/pdf':
                        fileType = 'pdf'
                    else:
                        fileType = 'image'
                else:
                    fileType = 'none'

                _id = ObjectId()
                demandes_aide[str(_id)] = Demande({"_id": _id, "id-utilisateur": ObjectId(session['id']), "titre": automoderation(request.form['titre']), "contenu": automoderation(request.form['demande']), "date-envoi": datetime.now(), "matière": request.form['matiere'], "réponses associées": {}, "likes": [], "sign": [], "resolu": False, "fileType": fileType})
                demandes_aide[str(_id)].insert()

                if request.files['file'].mimetype != 'application/octet-stream':
                    nom = "DemandeFile_" + str(_id)
                    DB.cluster.save_file(nom, request.files['file'])

                # add XP
                addXP(session['id'], 10)

                return redirect('/comments/' + str(_id))

            else:
                return redirect(url_for('accueil'))

            # return render_template('question.html', envoi="Envoi réussi")
        else:
            profilUtilisateur = utilisateurs[session['id']].toDict()

            if profilUtilisateur["SanctionEnCour"] != "Spec" and profilUtilisateur['SanctionEnCour'] != "SpecForum":
                return render_template('question.html', profilUtilisateur=profilUtilisateur, user=profilUtilisateur)
            else:
                return redirect(url_for('accueil'))
    else:
        return redirect(url_for('login'))


@app.route('/recherche')
def recherche():
    global utilisateurs
    global demandes_aide

    if 'id' in session:
        if 'search' in request.args and not request.args['search'] == '':
            search = request.args['search']

            user = utilisateurs[session['id']].toDict()

            # on récupère les demandes d'aide correspondant à la recherche
            result = sorted(
                [d.toDict() for d in demandes_aide.values()
                    if d.matiere in user['matieres'] and ( SequenceMatcher(None, d.titre, search).ratio()>0.7 or SequenceMatcher(None, d.contenu, search).ratio()>0.7 )
                ], key = lambda d: d['date-envoi'], reverse=True
            )

            # on récupère 3 utilisateurs correspondants à la recherche
            users = sorted(
                [u.toDict() for u in utilisateurs.values()
                    if SequenceMatcher(None, u.pseudo, search).ratio()>0.7 or SequenceMatcher(None, u.nom, search).ratio()>0.7 or SequenceMatcher(None, u.prenom, search).ratio()>0.7 or SequenceMatcher(None, u.lycee, search).ratio()>0.7
                        or ( 'email' in u.elementPublic and SequenceMatcher(None, u.email, search).ratio()>0.7 ) or ( 'telephone' in u.elementPublic and SequenceMatcher(None, u.telephone, search).ratio()>0.7 )
                ], key = lambda u: u['pseudo']
            )[:2]

            return render_template('recherche.html', results=result, users=users, search=search, user=user)

        else:
            return redirect(url_for('accueil'))
    else:
        return redirect(url_for('login'))


@app.route('/rechercheUser')
def recherche_user():
    global utilisateurs

    if 'id' in session:
        search = request.args['search']

        # on récupère 30 utilisateurs correspondants à la recherche
        users = sorted(
            [u.toDict() for u in utilisateurs.values()
                if SequenceMatcher(None, u.pseudo, search).ratio()>0.7 or SequenceMatcher(None, u.nom, search).ratio()>0.7 or SequenceMatcher(None, u.prenom, search).ratio()>0.7 or SequenceMatcher(None, u.lycee, search).ratio()>0.7
                    or ( 'email' in u.elementPublic and SequenceMatcher(None, u.email, search).ratio()>0.7 ) or ( 'telephone' in u.elementPublic and SequenceMatcher(None, u.telephone, search).ratio()>0.7 )
            ], key = lambda u: u['pseudo']
        )[:29]

        return render_template('rechercheUser.html', users=users, user = utilisateurs[session['id']].toDict())
    else:
        return redirect(url_for('login'))


@app.route('/likePost/<idPost>', methods=['POST'])
def likePost(idPost):
    global demandes_aide

    if 'id' in session:
        if 'idPost' != None:
            # on récupère les likes de la demande d'aide
            demande = demandes_aide[idPost].toDict()
            likes = demande['likes']

            # on check mtn si l'utilisateur a déjà liké la demande
            if session['id'] in likes:
                likes.remove(session['id'])  # on supprime son like

                # remove XP
                if not ObjectId(session['id']) == demande['idAuteur']:
                    addXP(demande['id-utilisateur'], -2)
            else:
                likes.append(session['id'])  # on ajoute son like

                # add XP
                if not ObjectId(session['id']) == demande['idAuteur']:
                    addXP(demande['id-utilisateur'], 2)

            # on update dans la DB
            demandes_aide[idPost].update()

            # on retourne enfin le nouveau nb de likes
            return {'newNbLikes': len(likes)}, 200

        else:
            abort(403)  # il manque l'id du message
    else:
        abort(401)  # non autorisé


@app.route('/likeRep/<idPost>/<idRep>', methods=['POST'])
def likeRep(idPost, idRep):
    global demandes_aide

    if 'id' in session:
        if 'idPost' != None and 'idRep' != None:
            # on récupère les likes de la demande d'aide
            demande = demandes_aide[idPost].toDict()
            reponses = demande['reponsesDict']
            if not idRep in reponses:
                return abort(400)
            reponse = reponses[idRep]

            likes = reponse['likes']

            # on check mtn si l'utilisateur a déjà liké la demande
            if session['id'] in likes:
                likes.remove(session['id'])  # on supprime son like

                # remove XP
                if not ObjectId(session['id']) == demande['idAuteur']:
                    addXP(demande['id-utilisateur'], -2)
            else:
                likes.append(session['id'])  # on ajoute son like

                # add XP
                if not ObjectId(session['id']) == demande['idAuteur']:
                    addXP(demande['id-utilisateur'], 2)

            # on update dans la DB
            demandes_aide[idPost].update()

            # on retourne enfin le nouveau nb de likes
            return {'newNbLikes': len(likes)}, 200

        else:
            abort(400)  # il manque l'id du message
    else:
        abort(401)  # non autorisé

@socketio.on('postLike')
def handleEvent_postLike(json):
    if 'id' in session:
        if 'type' in json:
            if json['type'] == 'post':
                if 'idPost' in json:
                    action = likePost(json['idPost'])
                    if action == 'add':
                        emit('newLike', json['idPost'], broadcast=True)
                    elif action == 'remove':
                        emit('removeLike', json['idPost'], broadcast=True)
            elif json['type'] == 'rep':
                if 'idPost' in json and 'idRep' in json:
                    action = likeRep(json['idPost'], json['idRep'])
                    if action == 'add':
                        emit('newLike', json['idRep'], broadcast=True)
                    elif action == 'remove':
                        emit('removeLike', json['idRep'], broadcast=True)


@app.route('/administration/', methods=['POST', 'GET'])
def administration():
    global utilisateurs
    global demandes_aide
    global groupes

    if 'id' in session:
        utilisateur = utilisateurs[session['id']].toDict()

        if utilisateur['admin'] == True:
            if request.method == 'POST':
                if request.form['demandeBut'] == 'Suppr':
                    demandes_aide[request.form['idSuppr']].delete()
                    del demandes_aide[request.form['idSuppr']]

                elif request.form['demandeBut'] == 'Val':
                    demande = demandes_aide[request.form['idVal']]
                    demande.sign = []
                    demande.motif = []

                    demandes_aide[request.form['idVal']].update()

                elif request.form['demandeBut'] == 'ValUser':
                    user = utilisateurs[request.form['idValidé']]
                    user.sign = []
                    user.motif = []

                    utilisateurs[request.form['idValidé']].update()

                return 'sent'

            else:
                demandeSignale = sorted([d.toDict() for d in demandes_aide.values() if d.sign != []], key = lambda d: len(d['sign']), reverse=True)
                profilSignale = sorted([u.toDict() for u in utilisateurs.values() if u.sign != []], key = lambda u: len(u['sign']), reverse=True)
                discussionSignale = sorted([g.toDict() for g in groupes.values() if g.sign != []], key = lambda g: len(g['sign']), reverse=True)

                return render_template('administration.html', user=utilisateur, demandeSignale=demandeSignale, profilSignale=profilSignale, discussionSignale=discussionSignale)
        else:
            return redirect(url_for('accueil'))
    else:
        return redirect(url_for('login'))


@app.route('/sanction/', methods=['POST'])
def sanction():
    global utilisateurs

    if 'id' in session:
        utilisateur = utilisateurs[session['id']].toDict()

        if utilisateur['admin'] == True:
            user = utilisateurs[request.form['idSanctionné']]
            userDict = user.toDict()
            sanctions = userDict['Sanctions']

            sanctions.append({"SanctionType": request.form['Sanction'], "SanctionMotif": request.form['Raison'], "SanctionNext": request.form['Next'], "dateSanction" : datetime.now()})

            time = datetime.now() + timedelta(days= int(request.form['SanctionDuree']))

            if request.form['SanctionType'] == 'Spec' or request.form['SanctionType'] == 'SpecProfil' or request.form['SanctionType'] == 'SpecForum' or request.form['SanctionType'] == 'SpecMsg':
                user.SanctionEnCour = request.form['SanctionType']
                user.SanctionDuree = time

            elif request.form['SanctionType'] == 'ResetProfil':
                MyImage = DB.db_files.find({'filename': {'$regex': 'imgProfile' + request.form['idSanctionné']}})
                addXpModeration(request.form['idSanctionné'], 10)
                for a in MyImage:
                    DB.db_files.delete_one({'_id': a['_id']})
                    DB.db_chunks.delete_many({'files_id': a['_id']})

                user.imgProfile = ''
                user.nomImg = ''
                user.pseudo = '{}_{}'.format(user.nom, user.prenom)
                user.telephone = ''
                user.interets = ''
                user.email = ''

            utilisateurs[request.form['idSanctionné']].update()

            return 'sent'

        else:
            return redirect(url_for('accueil'))
    else:
        return redirect(url_for('login'))


@app.route('/signPost/', methods=['POST'])
def signPost():
    global demandes_aide

    if 'id' in session:
        if request.form['idSignalé'] != None:
            # on récupère les signalements de la demande d'aide
            demande = demandes_aide[request.form['idSignalé']].toDict()
            sign = demande['sign']
            motif = demande['motif']

            # on check mtn si l'utilisateur a déjà signalé la demande
            if ObjectId(session['id']) in sign:
                # on supprime son signalement
                sign.remove(ObjectId(session['id']))
                index = next((i for i, item in enumerate(motif) if item.id == ObjectId(session['id'])), -1)
                del motif[index]

            else:
                # on ajoute son signalement
                sign.append(ObjectId(session['id'])) # on ajoute son signalement
                motif.append({'id': ObjectId(session['id']), 'txt': request.form['Raison']})

            demandes_aide[request.form['idSignalé']].update()

            return 'sent'

        else:
            abort(403) # il manque l'id du message
    else:
        abort(401) # non autorisé


@app.route('/signPostProfil/', methods=['POST'])
def signPostProfil():
    global utilisateurs

    if 'id' in session:
        if request.form['idSignalé'] != None:
            # on récupère les signalements de l'utilisateur
            user = utilisateurs[request.form['idSignalé']].toDict()
            sign = user['sign']
            motif = user['motif']

            # on check mtn si l'utilisateur a déjà signalé la demande
            if ObjectId(session['id']) in sign:
                # on supprime son signalement
                sign.remove(ObjectId(session['id']))
                index = next((i for i, item in enumerate(motif) if item.id == ObjectId(session['id'])), -1)
                del motif[index]

            else:
                # on ajoute son signalement
                sign.append(ObjectId(session['id']))
                motif.append({'id': ObjectId(session['id']), 'txt': request.form['Raison']})

            utilisateurs[request.form['idSignalé']].update()

            return 'sent'

        else:
            abort(403) # il manque l'id du message
    else:
        abort(401) # non autorisé

@app.route('/signPostDiscussion/', methods=['POST'])
def signPostDiscussion():
    global messages
    global groupes

    if 'id' in session:
        if request.form['idSignalé'] != None:
            # on récupère les signalements du groupe
            groupe = groupes[request.form['idSignalé']].toDict()
            sign = groupe['sign']
            motif = groupe['motif']

            # on check mtn si l'utilisateur a déjà signalé la demande
            if ObjectId(session['id']) in sign:
                # on supprime son signalement
                sign.remove(ObjectId(session['id']))
                index = next((i for i, item in enumerate(motif) if item['id'] == ObjectId(session['id'])), -1)
                del motif[index]

                grpMsg = [m.toDict() for m in messages.values() if m.id_groupe == ObjectId(request.form['idSignalé'])]
                for m in grpMsg:
                    mSign = m['sign']
                    mMotif = m['motif']

                    mSign.remove(ObjectId(session['id']))
                    mIndex = next((i for i, item in enumerate(mMotif) if item['id'] == ObjectId(session['id'])), -1)
                    del mMotif[mIndex]

                    messages[str(m['_id'])].update()

            else:
                # on ajoute son signalement
                sign.append(ObjectId(session['id']))
                motif.append({'id': ObjectId(session['id']), 'txt': request.form['Raison']})

                grpMsg = [m.toDict() for m in messages.values() if m.id_groupe == ObjectId(request.form['idSignalé'])]
                for m in grpMsg:
                    mSign = m['sign']
                    mMotif = m['motif']

                    mSign.append(ObjectId(session['id']))
                    mMotif.append({'id': ObjectId(session['id']), 'txt': "Discussion signalée pour : "+request.form['Raison']})

                    messages[str(m['_id'])].update()

            groupe = groupes[request.form['idSignalé']].update()

            return 'sent'

        else:
            abort(403) # il manque l'id du message
    else:
        abort(401) # non autorisé

@app.route('/signPostMsg/', methods=['POST'])
def signPostMsg():
    global messages
    global groupes

    if 'id' in session:
        if request.form['idSignalé'] != None and request.form['idMsgSignalé'] != None:
            # on récupère les signalements de la demande d'aide
            groupe = groupes[request.form['idSignalé']].toDict()
            sign = groupe['sign']
            motif = groupe['motif']
            message = messages[request.form['idMsgSignalé']].toDict()
            signMsg = message['sign']
            motifMsg = message['motif']

            # on check mtn si l'utilisateur a déjà signalé la demande
            if ObjectId(session['id']) in signMsg:
                # on retire son signalement
                signMsg.remove(ObjectId(session['id']))
                index = next((i for i, item in enumerate(motifMsg) if item['id'] == ObjectId(session['id'])), -1)
                del motifMsg[index]

            else:
                # on ajoute son signalement
                signMsg.append(ObjectId(session['id']))
                motifMsg.append({'id': ObjectId(session['id']), 'txt': request.form['Raison']})

                if not ObjectId(session['id']) in sign:
                    sign.append(ObjectId(session['id']))
                    motif.append({'id': ObjectId(session['id']), 'txt': "Message signalé : "+request.form['Raison']})

                    groupes[request.form['idSignalé']].update()

            messages[request.form['idMsgSignalé']].update()

            return 'sent'

        else:
            abort(403) # il manque l'id du message
    else:
        abort(401) # non autorisé

@app.route('/resoudre/<idPost>', methods=['POST'])
def resoudre(idPost):
    global demandes_aide

    if 'id' in session:
        if 'idPost' != None:
            demande = demandes_aide[idPost]

            # on check mtn si l'utilisateur a déjà liké la demande
            if demande.id_utilisateur == ObjectId(session['id']):
                # on update dans la DB
                demande.resolu = True

                demandes_aide[idPost].update()

                return "ok", 200
            else:
                abort(401) # non autorisé


        else:
            abort(403) # il manque l'id du message
    else:
        abort(401) # non autorisé


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
    global utilisateurs

    """Fetching a protected resource using an OAuth 2 token.
    """
    ENT_reply = OAuth2Session(client_id, token=session['oauth_token'])
    data = ENT_reply.get('https://ent.iledefrance.fr/auth/oauth2/userinfo').json()

    user = [u.toDict() for u in utilisateurs.values() if u.idENT == data['userId']]
    if len(user) > 0:
        user = user[0]
    else:
        user = None

    if user != None:
        session['id'] = str(user['_id'])
        session['pseudo'] = user['pseudo']
        session['couleur'] = user['couleur']
        session['type'] = user['type']

        if user['SanctionEnCour'] != "":
            if user['SanctionDuree'] < datetime.now():
                u = utilisateurs[user['_id']]
                u.SanctionEnCour = ''
                u.SanctionDuree = ''

                utilisateurs[user['_id']].update()

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

            _id = ObjectId()
            utilisateurs[str(_id)] = Utilisateur({"_id": _id, "idENT": data['userId'], "nom": data['lastName'], "prenom": data['firstName'], "pseudo": pseudo, 'nomImg': '', "dateInscription": datetime.now(), "birth_date": datetime.strptime(data['birthDate'], '%Y-%m-%d'), "classe": classe,
                                        "lycee": data['schoolName'], 'spes': [], 'langues': [], 'options': [], 'couleur': ['#e6445f', '#f3a6b3', '#afe2e7', '#f9d3d9'], 'type': data['type'], 'elementPublic': [], 'elementPrive': ['email', 'telephone', 'interets', 'birth_date', 'caractere'], "sign": [], "SanctionEnCour": "", 'xp': 0})
            utilisateurs[str(_id)].insert()

            user = utilisateurs[str(_id)].toDict()
            session['id'] = str(user['_id'])
            session['pseudo'] = user['pseudo']
            session['couleur'] = '#3f51b5'
            session['type'] = user['type']

            return redirect(url_for('profil'))

        elif data['type'] == 'ENSEIGNANT':
            pseudo = (data['username'].lower()).replace(' ', '_')

            _id = ObjectId()
            utilisateurs[str(_id)] = Utilisateur({"_id": _id, "idENT": data['userId'], "nom": data['lastName'], "prenom": data['firstName'], "pseudo": pseudo, "dateInscription": datetime.now(), "birth_date": datetime.strptime(
                data['birthDate'], '%Y-%m-%d'), "lycee": data['schoolName'], 'couleur': ['#e6445f', '#f3a6b3', '#afe2e7', '#f9d3d9'], 'type': data['type'], 'elementPublic': [], 'elementPrive': ['email', 'telephone', 'interets', 'birth_date', 'caractere'], "sign": [], "SanctionEnCour": "", 'xp': 0})
            utilisateurs[str(_id)].insert()

            user = utilisateurs[str(_id)]

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
