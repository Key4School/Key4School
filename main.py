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
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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

all_notifications = DB.db_notif.find()
for n in all_notifications:
    notifications[str(n['_id'])] = Notification(n)


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

def addXpModeration(userID: str, amount: int) -> None:
    global utilisateurs

    user = utilisateurs[userID]
    user.xpModeration += amount

    utilisateurs[userID].update()

    return

with open("list_ban_words.txt", "r", encoding='cp1252') as fichierBanWords:
    listeModeration = fichierBanWords.read().splitlines()

def automoderation(stringModerer: str) -> str:
    stringModerer2 =stringModerer
    for key in ['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}']:
            stringModerer2 = stringModerer2.replace(key," ")
            print (stringModerer2)
    for content in listeModeration:
        strReplace = ""
        for i in range (len(content)):
            strReplace += "*"
        if len(content) < 6:
            if stringModerer2[0:len(content)+1] == content+" ":
                stringModerer= stringModerer.replace(content, " "+strReplace+" ")
            if stringModerer2[-len(content)+1:] == " "+content:
                stringModerer= stringModerer.replace(content, " "+strReplace+" ")
            if stringModerer2 == content:
                stringModerer= stringModerer.replace(content, " "+strReplace+" ")
            content= " "+content+" "
        if  content in stringModerer2:
            stringModerer= stringModerer.replace(content, " "+strReplace+" ")

    return stringModerer


clientsNotif = {}

def sendNotif(type, id_groupe, id_msg, destinataires):
    global notifications

    if ObjectId(session['id']) in destinataires:
        destinataires.remove(ObjectId(session['id']))

    if len(destinataires) > 0:
        _id = ObjectId()
        notifications[str(_id)] = Notification({"_id": _id, "type": type, "id_groupe": id_groupe, "id_msg": id_msg,
                                        "date": datetime.now(), "destinataires": destinataires})
        notifications[str(_id)].insert()
        notification = notifications[str(_id)].toDict()

        serveur = 'smtp.gmail.com'
        port = '465'
        From = 'key4school@gmail.com'
        password = 'CtlLemeilleurGroupe'
        codage = 'utf-8'

        html = render_template("notification.html", notif=notification, similar=0)

        for user in notification['userDest']:
            if str(user['_id']) in clientsNotif:
                emit('newNotif', html, to=str(user['_id']))
            # elif user['email'] != "":
            #     # si l'user a autorisé les notifs par mail
            #     if (type == 'msg' and user['notifs']['messages']) or (type == 'demande' and user['notifs']['demandes']):
            #         # si un mail n'a pas déja été envoyé pour ce groupe
            #         if (type == 'msg' and len([notif for notif in notifications.values() if notif.id_groupe == id_groupe and notif.type == 'msg' and user in notif.destinataires]) == 0 ) or type == 'demande':
            #             To = user['email']
            #             msg = MIMEMultipart()
            #             msg['From'] = From
            #             msg['To'] = To
            #             msg['Subject'] = sujet
            #             msg['Charset'] = codage
            #
            #             # attache message texte
            #             msg.attach(MIMEText('message'.encode(codage),
            #                                 'plain', _charset=codage))
            #             # attache message HTML
            #             msg.attach(MIMEText('html'.encode(codage),
            #                                 'html', _charset=codage))
            #
            #             mailserver = smtplib.SMTP_SSL(serveur, port)
            #             mailserver.login(From, password)
            #             mailserver.sendmail(From, To, msg.as_string())
            #             mailserver.quit
# route temporaire
@app.route('/mail/')
def mail():
    if 'id' in session:
        return render_template("mail.html")
    else:
        return redirect(url_for('login'))


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
        clientsNotif[session['id']] = True
        join_room(session['id'])

        alreadySend = []
        notifs = [notif for id, notif in notifications.copy().items() if ObjectId(session['id']) in notif.destinataires and notif.toDict() != None]
        toSend = []
        for notif in notifs:
            if notif.id_groupe not in alreadySend:
                alreadySend.append(notif.id_groupe)
                toSend.append(notif)
        toSend.reverse()
        for notif in toSend:
            html = render_template("notification.html", notif=notif.toDict(), similar=len(notif.getSimilar(ObjectId(session['id']))))
            emit('newNotif', html, to=session['id'])


# Deconnexion au groupe pour recevoir les nouvelles notif
@socketio.on('disconnect')
def handleEvent_disconnect():
    if 'id' in session:
        if session['id'] in clientsNotif:
            clientsNotif.pop(session['id'])
            leave_room(session['id'])

@socketio.on('supprNotif')
def handleEvent_supprNotif(id):
    global notifications
    if 'id' in session:
        notification = notifications[id]
        for notif in notification.getSimilar(ObjectId(session['id'])):
            notif.supprUser(ObjectId(session['id']))
        notification.supprUser(ObjectId(session['id']))


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
    global notifications

    if 'id' in session:
        grp = sorted([groupe.toDict() for idGrp , groupe in groupes.items() if ObjectId(session['id']) in groupe.id_utilisateurs], key = lambda groupe: groupe['lastMsg']['date-envoi'] if groupe['lastMsg'] != None else datetime.min, reverse=True)
        user = utilisateurs[session['id']].toDict()
        users = sorted([u.toDict() for u in utilisateurs.values()], key = lambda u: u['pseudo'])

        if idGroupe != None:
            groupe = groupes[idGroupe]
            infoUtilisateurs = groupe.toDict()['utilisateurs']
            if ObjectId(session['id']) in groupe.toDict()['id-utilisateurs']: # verif autorization
                msgDb = groupe.getAllMessages()

            elif user['admin'] == True:
                msgDb = groupe.getAllMessagesSign()

            else:
                msgDb = None
                groupe = None
                infoUtilisateurs = None
            groupe = groupe.toDict()

            for notif in [notification for notification in notifications.values() if notification.id_groupe == ObjectId(idGroupe) and notification.type == 'msg' and ObjectId(session['id']) in notification.destinataires]:
                notif.supprUser(ObjectId(session['id']))

        else:
            msgDb = None
            groupe = None
            infoUtilisateurs = None

        return render_template("messages.html", msgDb=msgDb, grpUtilisateur=grp, idgroupe=idGroupe, infogroupe=groupe, infoUtilisateurs=infoUtilisateurs, users=users, sessionId=ObjectId(session['id']), user=user)

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
                if ObjectId(session['id']) in grp['id-utilisateurs']: # authorized
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
                        groupe = message['groupe']
                        sendNotif("msg", ObjectId(json['room']), _id, list(groupe['id-utilisateurs']))

                        users = groupe['utilisateurs']

                        ownHTML = render_template("widget_message.html", content=message, sessionId=ObjectId(session['id']), infogroupe=groupe, infoUtilisateurs=users, idgroupe=json['room'], user=utilisateurs[session['id']].toDict())
                        otherHTML = render_template("widget_message.html", content=message, sessionId=None, infogroupe=groupe, infoUtilisateurs=users, idgroupe=json['room'], user=utilisateurs[session['id']].toDict())

                        emit('newMsg', {'fromUser': session['id'], 'ownHTML': ownHTML, 'otherHTML': otherHTML}, to=json['room'])

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
    global utilisateurs
    global Groupe

    if 'id' in session:
        idGroupe = request.form['grp']
        user = utilisateurs[session['id']].toDict()
        msg = messages[request.form['msgSuppr']].toDict()
        groupe = groupes[request.form['grp']].toDict()
        sign=groupe['sign']
        motif = groupe['motif']
        # grp = Groupe[request.form['grp']].toDict()
        if user['admin'] or user['type']=="ENSEIGNANT" or msg['id-utilisateur']==ObjectId(session['id']) or ObjectId(session['id'] in grp['moderateurs']):
            if msg['sign'] != []:
                sign.remove(ObjectId(request.form['msgSuppr']))
                index = next((i for i, item in enumerate(motif) if item['id'] == ObjectId(request.form['msgSuppr'])), -1)
                del motif[index]
            messages[request.form['msgSuppr']].suppr()
            if request.form['audio'] == 'True':
                MyAudio = DB.db_files.find_one({'filename': request.form['audioName']})
                DB.db_files.delete_one({'_id': MyAudio['_id']})
                DB.db_chunks.delete_many({'files_id': MyAudio['_id']})

            groupes[request.form['grp']].update()

        return redirect(url_for('page_messages', idGroupe=idGroupe))

    else:
        return redirect(url_for('login'))

@app.route('/validationMsg/', methods=['POST'])
def validerMsg():
    global messages
    global groupes
    if 'id' in session:
        user = utilisateurs[session['id']].toDict()
        idGroupe = request.form['grp']
        if user['admin']:
            message = messages[request.form['msgVal']].toDict()
            signMsg = message['sign']
            motifMsg = message['motif']
            signMsg.clear()
            motifMsg.clear()
            groupe = groupes[request.form['grp']].toDict()
            sign = groupe['sign']
            motif = groupe['motif']
            print (sign)
            sign.remove(ObjectId(request.form['msgVal']))
            index = next((i for i, item in enumerate(motif) if item['id'] == ObjectId(request.form['msgVal'])), -1)
            del motif[index]

            groupes[request.form['grp']].update()
            messages[request.form['msgVal']].update()

        return redirect(url_for('page_messages', idGroupe=idGroupe))

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

        return redirect(url_for('page_messages', idGroupe=str(_id)))
    else:
        return redirect(url_for('login'))

@app.route('/updateGroupe/', methods=['POST'])
def updateGroupe():
    global groupes

    if 'id' in session:
        groupe = groupes[request.form['IdGroupe']]
        participants = groupe.toDict()['id-utilisateurs']

        if ObjectId(session['id']) in participants and ObjectId(session['id']) in groupe.toDict()['moderateurs']:
            for name, value in request.form.items():
                if name == 'IdGroupe':
                    pass
                else:
                    participants.append(ObjectId(name))
            groupe.id_utilisateurs = participants
            groupe.update()

        return redirect(url_for('page_messages', idGroupe=request.form['IdGroupe']))
    else:
        return redirect(url_for('login'))

@app.route('/virerParticipant/', methods=['POST'])
def virerParticipant():
    global utilisateurs
    global groupes

    if 'id' in session:
        groupe = groupes[request.form['idViréGrp']]
        moderateurs = groupe.toDict()['moderateurs']

        if ObjectId(session['id']) in moderateurs or request.form['idViré'] == session['id']:
            groupe.supprUser(ObjectId(request.form['idViré']))

            if request.form['idViré'] == session['id']:
                return redirect(url_for('page_messages'))
            else:
                return redirect(url_for('page_messages', idGroupe=request.form['idViréGrp']))
        else:
            return redirect(url_for('page_messages'))
    else:
        return redirect(url_for('login'))

@app.route('/modifRole/', methods=['POST'])
def modifRole():
    if 'id' in session:
        grp = groupes[request.form['idGrp']]
        modos = grp.toDict()['moderateurs']
        participants = grp.toDict()['id-utilisateurs']

        if ObjectId(session['id']) in modos and ObjectId(request.form['idModifié']) in participants:
            if ObjectId(request.form['idModifié']) in modos:
                modos.remove(ObjectId(request.form['idModifié']))
                grp.moderateurs = modos
                grp.update()

                return 'participant'

            else:
                modos.append(ObjectId(request.form['idModifié']))
                grp.moderateurs = modos
                grp.update()

                return 'admin'
        else:
            abort(401) # non autorisé
    else:
        abort(403) # doit se connecter

@app.route('/changeTheme/', methods=['POST'])
def changeTheme():
    global utilisateurs

    if 'id' in session:
        if int(request.form['couleur']) == 6:
            color2 = tuple(int(request.form['color2'].lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
            moyenne = '#%02x%02x%02x' % tuple((color+255)//2 for color in color2)
            couleurs = [request.form['color1'], request.form['color2'], request.form['color3'], moyenne]

        else:
            listColor = [['#00b7ff', '#a7ceff', '#94e1ff', '#d3e6ff'],
                        ['#ff0000', '#ffa8a8', '#ff9494', '#ffd3d3'],
                        ['#14db14', '#aeffa8', '#a0ff94', '#d6ffd3'],
                        ['#ffbb00', '#e8c959', '#ffe294', '#f3e4ac'],
                        ['#e6445f', '#f3a6b3', '#afe2e7', '#f9d3d9'],
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

        notifs = {}
        if request.form['notifs_demandes'] == 'yes':
            notifs['demandes'] = True
        else:
            notifs['demandes'] = False
        if request.form['notifs_messages'] == 'yes':
            notifs['messages'] = True
        else:
            notifs['messages'] = False
        user.notifs = notifs

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
    global notifications

    if 'id' in session:
        if request.method == 'GET':
            msg = demandes_aide[idMsg].toDict()

            for notif in [notification for notification in notifications.values() if notification.id_groupe == ObjectId(idMsg) and notification.type == 'demande' and ObjectId(session['id']) in notification.destinataires]:
                notif.supprUser(ObjectId(session['id']))

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
                    'likes': [],
                    'sign': [],
                })

                demandes_aide[idMsg].update()

                sendNotif("demande", ObjectId(idMsg), _id, [msg['idAuteur']])

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

@app.route('/updateDemand/', methods=['POST'])
def updateDemand():
    global utilisateurs
    global demandes_aide

    if 'id' in session:
        demand = demandes_aide[request.form['idDemandModif']]
        if ObjectId(session['id']) == demand.id_utilisateur:
            demand.contenu = request.form['txtModif']
            demand.update()
        return 'sent'
    else:
        return redirect(url_for('login'))

@app.route('/recherche/')
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
                    if d.matiere in user['matieres'] and ( SequenceMatcher(None, d.titre, search).ratio()>0.5 or SequenceMatcher(None, d.contenu, search).ratio()>0.5 )
                ], key = lambda d: ( SequenceMatcher(None, d['titre'], search).ratio() + SequenceMatcher(None, d['contenu'], search).ratio() ), reverse=True
            )

            # on récupère 3 utilisateurs correspondants à la recherche
            users = sorted(
                [u.toDict() for u in utilisateurs.values()
                    if SequenceMatcher(None, u.pseudo, search).ratio()>0.7 or SequenceMatcher(None, u.nom, search).ratio()>0.7 or SequenceMatcher(None, u.prenom, search).ratio()>0.7 or SequenceMatcher(None, u.lycee, search).ratio()>0.7
                        or ( 'email' in u.elementPublic and SequenceMatcher(None, u.email, search).ratio()>0.5 ) or ( 'telephone' in u.elementPublic and SequenceMatcher(None, u.telephone, search).ratio()>0.5 )
                ], key = lambda u: u['pseudo']
            )[:2]

            return render_template('recherche.html', results=result, users=users, search=search, user=user)

        else:
            return redirect(url_for('accueil'))
    else:
        return redirect(url_for('login'))


@app.route('/rechercheUser/')
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
    global Reponse

    if 'id' in session:
        utilisateur = utilisateurs[session['id']].toDict()

        if utilisateur['admin'] == True:
            if request.method == 'POST':
                if request.form['demandeBut'] == 'Suppr':
                    auteur = demandes_aide[request.form['idSuppr']].toDict()['idAuteur']
                    demandes_aide[request.form['idSuppr']].delete()
                    del demandes_aide[request.form['idSuppr']]
                    addXpModeration(str(auteur), 10)

                elif request.form['demandeBut'] == 'Val':
                    demande = demandes_aide[request.form['idVal']]
                    sign = demande.sign
                    if request.form['motif'] == "abusif":
                        for content in sign:
                            if "/" not in str(content):
                                addXpModeration(str(content), 5)
                    motif = demande.motif
                    for i in range (len(sign)):
                        if "/" not in str(sign[i]):
                            del sign[i]
                    for a in range (len(motif)):
                        if "/" not in str(motif[a]):
                            del motif[a]

                    demandes_aide[request.form['idVal']].update()

                elif request.form['demandeBut'] == 'ValUser':
                    user = utilisateurs[request.form['idValidé']]
                    if request.form['motif'] == "abusif":
                        for content in user.sign:
                                addXpModeration(str(content), 5)
                    user.sign = []
                    user.motif = []
                    utilisateurs[request.form['idValidé']].update()

                elif request.form['demandeBut'] == 'SupprRep':
                    demande = demandes_aide[request.form['idDemandSuppr']]
                    auteur = demandes_aide[request.form['idDemandSuppr']].toDict()['reponsesDict'][request.form['idSuppr']]['id-utilisateur']
                    addXpModeration(str(auteur), 5)
                    demande.reponses_associees.pop(request.form['idSuppr'])
                    signDemande = demande.sign
                    motifDemande = demande.motif
                    print (len(signDemande))
                    for i in range (len(signDemande)):
                        if str(request.form['idSuppr']+"/") in str(signDemande[i]):
                            del signDemande[i]
                    for a in range (len(motifDemande)):
                        if str(request.form['idSuppr']+"/") in str(motifDemande[a]):
                            del motifDemande[a]
                    demande.update()

                elif request.form['demandeBut'] == 'ValRep':
                    demande = demandes_aide[request.form['idDemandVal']]
                    signDemande = demande.sign
                    motifDemande = demande.motif
                    sign =  demandes_aide[request.form['idDemandVal']].toDict()['reponsesDict'][request.form['idVal']]['sign']
                    if request.form['motif'] == "abusif":
                        for content in sign :
                                addXpModeration(str(content), 5)
                    demandes_aide[request.form['idDemandVal']].toDict()['reponsesDict'][request.form['idVal']]['sign'].clear()
                    demandes_aide[request.form['idDemandVal']].toDict()['reponsesDict'][request.form['idVal']]['motif'].clear()
                    for i in range (len(signDemande)):
                        if str(request.form['idVal']+"/") in str(signDemande[i]):
                            del signDemande[i]
                    for a in range (len(motifDemande)):
                        if str(request.form['idVal']+"/") in str(motifDemande[a]):
                            del motifDemande[a]
                    demandes_aide[request.form['idDemandVal']].update()

                elif request.form['demandeBut'] == 'supprDisc':
                    groupe = groupes[request.form['idDiscSuppr']].toDict()
                    sign = groupe['sign']
                    motif = groupe['motif']
                    for auteur in groupe['id-utilisateurs'] :
                        addXpModeration(str(auteur), 10)

                    sign.clear()
                    motif.clear()
                    grpMsg = [m.toDict() for m in messages.values() if m.id_groupe == ObjectId(request.form['idDiscSuppr'])]
                    for m in grpMsg:
                        messages[str(m['_id'])].suppr()

                            # messages[str(m['_id'])].update()
                    groupes[request.form['idDiscSuppr']].update()

                elif request.form['demandeBut'] == 'valDisc':
                    groupe = groupes[request.form['idDiscVal']].toDict()
                    sign = groupe['sign']
                    motif = groupe['motif']
                    if request.form['motif'] == "abusif":
                        for content in sign:
                                addXpModeration(str(content), 5)
                        # on supprime son signalement
                    sign.clear()
                    motif.clear()
                    grpMsg = [m.toDict() for m in messages.values() if m.id_groupe == ObjectId(request.form['idDiscVal'])]
                    for m in grpMsg:
                        m['motif'].clear()
                        m['sign'].clear()
                        messages[str(m['_id'])].update()
                    groupes[request.form['idDiscVal']].update()


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
                addXpModeration(request.form['idSanctionné'], 50)

            elif request.form['SanctionType'] == 'ResetProfil':
                MyImage = DB.db_files.find({'filename': {'$regex': 'imgProfile' + request.form['idSanctionné']}})
                addXpModeration(request.form['idSanctionné'], 25)
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
                index = next((i for i, item in enumerate(motif) if item['id'] == ObjectId(session['id'])), -1)
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

@app.route('/signRepPost/', methods=['POST'])
def signRepPost():
    global demandes_aide
    if 'id' in session:
        if request.form['idSignalé'] != None and request.form['idDemandSignalé'] != None:
            # on récupère les signalements de la demande d'aide
            demande = demandes_aide[request.form['idDemandSignalé']].toDict()
            sign = demande['reponsesDict'][request.form['idSignalé']]['sign']
            motif = demande['reponsesDict'][request.form['idSignalé']]['motif']
            signDemand = demande['sign']
            motifDemand = demande['motif']

            if ObjectId(session['id']) in sign:
                # on supprime son signalement
                sign.remove(ObjectId(session['id']))
                index = next((i for i, item in enumerate(motif) if item['id'] == ObjectId(session['id'])), -1)
                del motif[index]
                signDemand.remove(request.form['idSignalé']+"/"+session['id'])
                index = next((i for i, item in enumerate(motifDemand) if item['id'] == str(request.form['idSignalé'])+"/"+str(session['id'])), -1)
                del motifDemand[index]

            else:
                # on ajoute son signalement
                sign.append(ObjectId(session['id'])) # on ajoute son signalement
                motif.append({'id': ObjectId(session['id']), 'txt': request.form['Raison']})
                signDemand.append(request.form['idSignalé']+"/"+session['id'])
                motifDemand.append({'id': request.form['idSignalé']+"/"+session['id'], 'txt': 'Réponse Signalée'})


            demandes_aide[request.form['idDemandSignalé']].update()
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
                index = next((i for i, item in enumerate(motif) if item['id'] == ObjectId(session['id'])), -1)
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
                sign.remove(ObjectId(request.form['idMsgSignalé']))
                index = next((i for i, item in enumerate(motif) if item['id'] == ObjectId(request.form['idMsgSignalé'])), -1)
                del motif[index]

            else:
                # on ajoute son signalement
                signMsg.append(ObjectId(session['id']))
                motifMsg.append({'id': ObjectId(session['id']), 'txt': request.form['Raison']})

                if not ObjectId(session['id']) in sign:
                    sign.append(ObjectId(request.form['idMsgSignalé']))
                    motif.append({'id': ObjectId(request.form['idMsgSignalé']), 'txt': "Message signalé : "+request.form['Raison']})

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
    global groupes

    """Fetching a protected resource using an OAuth 2 token.
    """
    ENT_reply = OAuth2Session(client_id, token=session['oauth_token'])
    data = ENT_reply.get('https://ent.iledefrance.fr/auth/oauth2/userinfo').json()
    data_plus = ENT_reply.get('https://ent.iledefrance.fr/directory/myinfos').json()

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

        u = utilisateurs[str(user['_id'])]
        if user['SanctionEnCour'] != "":
            if user['SanctionDuree'] < datetime.now():
                u.SanctionEnCour = ''
                u.SanctionDuree = ''

        if u.type == "ELEVE":
            classe = data_plus['classes'][0].split('$')[1]
            u.classe = classe
            nomClasse = f"{user['lycee']}/{classe}"
            group = [g for g in groupes.values() if g.nom == nomClasse and g.is_class == True]
            if len(group) > 0:
                group = group[0]
                if user['_id'] not in group.id_utilisateurs:
                    group.id_utilisateurs.append(user['_id'])
                    group.update()
            else:
                _id = ObjectId()
                groupes[str(_id)] = Groupe({'_id': _id, 'nom': nomClasse, 'is_class': True, 'id-utilisateurs': [user['_id']]})
                groupes[str(_id)].insert()
            # on retire l'user des anciens groupe de classe
            oldGroups = [g for g in groupes.values() if g.nom != nomClasse and g.is_class == True and user['_id'] in g.id_utilisateurs]
            for oldGroup in oldGroups:
                oldGroups.supprUser(user['_id'])

        if data_plus['email'] != '':
            u.email = data_plus['email']

        if 'mobile' in data_plus:
            if data_plus['mobile'] != "":
                u.telephone = data_plus['mobile']
        elif 'homePhone' in data_plus:
            if data_plus['homePhone'] != "":
                u.telephone = data_plus['homePhone']

        if data_plus['emailInternal'] != '':
            u.emailENT = data_plus['emailInternal']

        utilisateurs[str(user['_id'])].update()

        return redirect(url_for('accueil'))

    else:
        if data['type'] == "ELEVE":
            classe = data_plus['classes'][0].split('$')[1]
            pseudo = (data['username'].lower()).replace(' ', '_')
            tel = ''
            if 'mobile' in data_plus:
                if data_plus['mobile'] != "":
                    tel = data_plus['mobile']
            elif 'homePhone' in data_plus:
                if data_plus['homePhone'] != "":
                    tel = data_plus['homePhone']

            _id = ObjectId()
            utilisateurs[str(_id)] = Utilisateur({"_id": _id, "idENT": data['userId'], "nom": data['lastName'], "prenom": data['firstName'], "pseudo": pseudo, 'nomImg': '', "dateInscription": datetime.now(),
                                        "birth_date": datetime.strptime(data['birthDate'], '%Y-%m-%d'), "classe": classe, "email" : data_plus['email'], "telephone": tel, "emailENT": data_plus['emailInternal'],
                                        "lycee": data['schoolName'], 'spes': [], 'langues': [], 'options': [], 'couleur': ['#00b7ff', '#a7ceff', '#94e1ff', '#d3e6ff'], 'type': data['type'], 'elementPublic': [],
                                        'elementPrive': ['email', 'telephone', 'interets', 'birth_date', 'caractere'], "sign": [], "SanctionEnCour": "", 'xp': 0})
            utilisateurs[str(_id)].insert()

            user = utilisateurs[str(_id)].toDict()
            session['id'] = str(user['_id'])
            session['pseudo'] = user['pseudo']
            session['couleur'] = ['#00b7ff', '#a7ceff', '#94e1ff', '#d3e6ff']
            session['type'] = user['type']

            nomClasse = f"{data['schoolName']}/{classe}"
            group = [g for g in groupes.values() if g.nom == nomClasse and g.is_class == True]
            if len(group) > 0:
                group = group[0]
                if user['_id'] not in group.id_utilisateurs:
                    group.id_utilisateurs.append(user['_id'])
                    group.update()
            else:
                _id = ObjectId()
                groupes[str(_id)] = Groupe({'_id': _id, 'nom': nomClasse, 'is_class': True, 'id-utilisateurs': [user['_id']]})
                groupes[str(_id)].insert()

            return redirect(url_for('profil'))

        elif data['type'] == 'ENSEIGNANT':
            pseudo = (data['username'].lower()).replace(' ', '_')
            tel = ''
            if 'mobile' in data_plus:
                if data_plus['mobile'] != "":
                    tel = data_plus['mobile']
            elif 'homePhone' in data_plus:
                if data_plus['homePhone'] != "":
                    tel = data_plus['homePhone']

            _id = ObjectId()
            utilisateurs[str(_id)] = Utilisateur({"_id": _id, "idENT": data['userId'], "nom": data['lastName'], "prenom": data['firstName'], "pseudo": pseudo, "dateInscription": datetime.now(), "birth_date": datetime.strptime(
                data['birthDate'], '%Y-%m-%d'), "lycee": data['schoolName'], 'couleur': ['#00b7ff', '#a7ceff', '#94e1ff', '#d3e6ff'], 'type': data['type'], 'elementPublic': [], 'elementPrive': ['email', 'telephone', 'interets',
                'birth_date', 'caractere'], "email" : data_plus['email'], "telephone": tel, "emailENT": data_plus['emailInternal'], "sign": [], "SanctionEnCour": "", 'xp': 0, 'nomImg': ''})
            utilisateurs[str(_id)].insert()

            user = utilisateurs[str(_id)].toDict()

            session['id'] = str(user['_id'])
            session['pseudo'] = user['pseudo']
            session['couleur'] = ['#00b7ff', '#a7ceff', '#94e1ff', '#d3e6ff']
            session['type'] = user['type']

            return redirect(url_for('profil'))

        else:
            return redirect("https://ent.iledefrance.fr/timeline/timeline")


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
